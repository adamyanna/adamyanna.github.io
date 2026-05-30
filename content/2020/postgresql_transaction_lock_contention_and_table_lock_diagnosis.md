# PostgreSQL: Transaction Lock Contention & Table Lock Diagnosis

> 2020-05-13

Production incident — 200+ concurrent PostgreSQL processes contending for exclusive and row-exclusive locks on a single table, exhausting the connection pool. Root cause, fix, and diagnostic queries.

## Incident

200+ PostgreSQL processes accessed a procedural transaction within the same one-minute window. The transaction competed for two locks sequentially:

1. **RowExclusiveLock** — on the target rows
2. **ExclusiveLock** — on `t_device` table

While holding one lock and waiting for the other, the table became fully locked (`t_device`). No queries could access the table, and connections could not be released — hitting the pool's `max_connections` limit.

## Fix

Replaced the complex `mark_device` stored procedure with a simpler **agent heartbeat** approach. Device allocation logic was moved to the device sync function, eliminating the lock-heavy transaction.

## Diagnostic Queries

```sql
-- Count sessions waiting on locks
SELECT count(*) FROM pg_stat_activity WHERE wait_event_type = 'Lock';

-- Detail: which sessions are waiting, on what, and for how long
SELECT client_addr, client_port, wait_event_type, wait_event,
       state, query, backend_start, xact_start, query_start, state_change
FROM pg_stat_activity
WHERE wait_event_type = 'Lock';

-- All active sessions (both blocked and waiting)
SELECT count(*) FROM pg_stat_activity
WHERE wait_event_type IS NULL OR wait_event_type = 'Lock';

-- Exclude mark_device queries to identify competing workloads
SELECT client_addr, client_port, query,
       backend_start, xact_start, query_start, state_change,
       wait_event_type, wait_event, state
FROM pg_stat_activity
WHERE query NOT LIKE '%mark_device%';

-- Total active connections
SELECT count(*) FROM pg_stat_activity;

```
