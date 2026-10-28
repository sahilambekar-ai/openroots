import ast,inspect,json,sys
from pathlib import Path
from fastapi.routing import APIRoute,iter_route_contexts
from app.main import api_v1
out=Path('/Users/sahil/Documents/work/openroots/audit-evidence/2026-10-27/functional-review');out.mkdir(parents=True,exist_ok=True)
rows=[]
def deps(d):
 return ([getattr(d.call,'__qualname__','')] if d.call else [])+[x for c in d.dependencies for x in deps(c)]
for r in iter_route_contexts(api_v1.routes):
 if not isinstance(r.original_route,APIRoute):continue
 f=r.endpoint
 source=inspect.getsource(f)
 tree=ast.parse(source)
 sql=[ast.unparse(n) for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='where']
 row=dict(path=r.path,methods=sorted(r.methods),file=inspect.getsourcefile(f).split('progressrooms-api/')[-1],line=inspect.getsourcelines(f)[1],handler=f.__name__,dependencies=deps(r.dependant),body=[dict(name=p.name,type=str(p.field_info.annotation)) for p in r.dependant.body_params],query=[p.name for p in r.dependant.query_params],filters=sql)
 rows.append(row)
(out/'routes.json').write_text(json.dumps(rows,indent=2))
print('Registered methods:',sum(len(r['methods']) for r in rows))
for row in rows:
 print(','.join(row['methods'])+' '+row['path']+' ['+','.join(sorted(set(row['dependencies'])-{'get_db','get_current_user','security_bearer'}))+']')
