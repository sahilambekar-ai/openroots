# Database review — 2026-10-27

PostgreSQL PostgreSQL 16.15 on aarch64-apple-darwin27.0.0, compiled by Apple clang version 21.0.0 (clang-2100.1.1.101), 64-bit

## Scope and evidence

- Native PostgreSQL 16.15 built from official source; SHA256 verified. Installed only under `/private/tmp/item6-pg16`; UTF8/C locale, without ICU/readline/zlib. This is PostgreSQL16 SQL/driver verification on macOS, not execution of the Linux Alpine container or production collation/configuration.
- Ordinary Alembic upgrade to `034_support_indexes` and check pass. Standard metadata comparison has no differences. Models contain 55 tables; backup restoration compares row counts and canonical row-content hashes for those 55 plus `alembic_version`. A separate fixture database is created and removed.
- 174 catalog constraints are validated in the fresh synthetic schema; no invalid indexes. Tests cover foreign-key rejection, duplicate email/single-admin rejection, same-studio teacher assignment, CASCADE/SET NULL, migration failure atomicity, safe 034 reversal/re-upgrade and refusal to cross auth revision033.
- Real deployment backup script is exercised through a local Compose-command adapter using actual PostgreSQL16 tools. Checksum/private permissions/no-overwrite/failure cleanup and restoration verify selected populated auth, support, financial and nested webhook records. Empty tables are included too. Live service restoration is not claimed.

## Query plans

Synthetic data: 100 tenants, 10,000 users, 2,000 classes, 100,000 support tickets/occurrences/enrollments/email deliveries each, and 50,000 orders/payments each. ANALYZE runs before measurement. These are single local warm-cache plan samples, not latency targets or load-test percentiles. Statements reproduce core access predicates/projections; eager-loading queries, API serialization and network/provider overhead are excluded.

| Query | Execution ms |
|---|---:|
| student_support | 0.015 |
| studio_open_support | 0.051 |
| studio_month_schedule | 0.091 |
| session_active_enrollment_count | 0.016 |
| student_studio_enrollments | 0.008 |
| studio_collected_payments | 4.261 |
| due_meeting_email_batch | 0.545 |

Without the student-support index, the same ownership lookup scans the full ticket table in 2.677 ms; with it the bitmap index scan returns ten rows. This rollback-only experiment changes only the synthetic schema.

Schedule, support and student-enrollment paths use existing/new indexes. The payment aggregate selects a hash join with a sequential payment scan (50,000 rows) and tenant-indexed orders; no extra index was added based on this single scale. The mail batch uses its status index and sorts 1,000 eligible rows. Raw plans retain buffers, actual rows and SQL.

## Review outcomes and limits

034 resolves the reported support index drift transactionally with bounded lock/statement waits. Failure rolls back, including when a manually created index conflicts. It uses ordinary index DDL and needs a quiet window on large real tables. Historical rollback functions are inventoried; many destroy data or do not reverse backfills/provider state. Auth033 deliberately blocks unsafe downgrade. Use compatible forward fixes or a coherent pre-release restore with signing-key rotation.

The FK/index inventory identifies 23 candidate constraints without a matching full leading-column index; several already have useful partial/individual-column indexes. This is a review list, not 23 demonstrated slow queries or a recommendation to index them all. Profile deletion/join workloads before further indexing. Database FKs/checks do not encode every cross-table business/tenant rule or replace API authorization; this review does not introduce row-level security. No production data, bloat, statistics, grants or host configuration was inspected.

UAT source now makes a private database archive/checksum a pre-migration gate. A TOC check alone is not a restore guarantee. Restores remain explicit operator actions. Host backup frequency, encryption, off-host retention, WAL/PITR, compatible file-volume/key backups and measured recovery objectives remain deployment/recovery work; see the maintained [runbook](/Users/sahil/Documents/work/openroots/progressrooms/progressrooms-api/deploy/DATABASE_RECOVERY.md). CI gates are configured but have not run remotely.

Sources: [official PostgreSQL16.15 source](https://www.postgresql.org/ftp/source/v16.15/), [PostgreSQL16 pg_dump](https://www.postgresql.org/docs/16/app-pgdump.html), [backup and restore](https://www.postgresql.org/docs/16/backup.html). No live-provider calls, production migrations, pushes or deployments occurred.
