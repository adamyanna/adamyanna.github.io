---
title: Postgresql HA & Loadblance - pgpool II
author: Teddy
date: 2018-10-23 19:00:00 +0800
categories: [实践, 实践记录]
tags: [Postgresql, Pgpool]
---


## Optional Solution
1. corosync & pacemaker & heartbeat script
> POC failed, centos 7.2 x64
2. pgpool II (middleware) & failover script & recovery script
> POC ... processing

## POC

### Env
*CentOS 7.2 x64*

### Installation
1. postgresql 9.6
2. pgpool II 96 v3.6.12

### Version
9.6 & 3.6

### Config

### Hot-standby
1. backup command
```
pg_basebackup -D .././. -F p -x -h primary_node -p 5432 -U postgres -P -v
```

### Check pool node status
```
psql -h primary_node -p9999 -U postgres postgres
```

### Pg_rewind command
```
su - postgres

pg_rewind --target-pgdata='/../../..' --source-server='host= port= dbname= user= password=' -P
```
> note: the target server must be primary server, postgresql won't let server to synchronize from standby server.

## issue

1. watchdog reject issue, correct `Other pgpool Connection Settings` pgpool_port and wd_port, default is 9999 and 9000.
> This issue will lead watchdog process down, watchdog heartbeat signal will be rejected.

2. correct the rwx permission for root and postgres user.

3. recovery issue

4. pg_rewind command for base time line synchronize

