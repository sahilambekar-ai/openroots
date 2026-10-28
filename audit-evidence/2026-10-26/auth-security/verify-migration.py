import os
import subprocess
import uuid
from pathlib import Path
import psycopg2

name = 'auth_migration_' + uuid.uuid4().hex[:12]
root = psycopg2.connect('postgresql://audit@127.0.0.1:65439/postgres')
root.autocommit = True
with root.cursor() as cur:
    cur.execute('CREATE DATABASE ' + name)
env = dict(os.environ, BREVO_ENABLED='false', SYNC_DATABASE_URL=f'postgresql://audit@127.0.0.1:65439/{name}')
python = str(Path('.venv/bin/python').absolute())
try:
    subprocess.run([python, '-m', 'alembic', 'upgrade', '032_zoom_meeting_mail'], env=env, check=True)
    conn = psycopg2.connect(env['SYNC_DATABASE_URL'])
    with conn, conn.cursor() as cur:
        cur.execute("""INSERT INTO users(id,email,full_name,role,is_active,is_superadmin,is_verified,account_status,
                    created_at,updated_at,password_hash) VALUES (%s,'migration@example.com','Migration','STUDENT',
                    true,false,true,'ACTIVE',now(),now(),'legacy-hash')""", (str(uuid.uuid4()),))
    subprocess.run([python, '-m', 'alembic', 'upgrade', 'head'], env=env, check=True)
    with conn, conn.cursor() as cur:
        cur.execute("SELECT session_version,password_hash FROM users WHERE email='migration@example.com'")
        assert cur.fetchone() == (0, 'legacy-hash')
        cur.execute('SELECT count(*) FROM auth_rate_limits')
        assert cur.fetchone()[0] == 0
    rollback = subprocess.run([python, '-m', 'alembic', 'downgrade', '032_zoom_meeting_mail'], env=env, capture_output=True, text=True)
    assert rollback.returncode != 0 and 'cannot be safely downgraded' in rollback.stderr
    with conn, conn.cursor() as cur:
        cur.execute('SELECT version_num FROM alembic_version')
        assert cur.fetchone()[0] == '033_auth_security'
        cur.execute("SELECT session_version FROM users WHERE email='migration@example.com'")
        assert cur.fetchone() == (0,)
    conn.close()
    print('PASS: upgrade 032 -> 033 preserves existing users/hashes and defaults version=0.')
    print('PASS: unsafe downgrade is blocked; revision and user data remain intact.')
finally:
    with root.cursor() as cur:
        cur.execute('DROP DATABASE ' + name + ' WITH (FORCE)')
    root.close()
    print('Disposable migration database removed.')
