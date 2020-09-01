---
title: pg数据库过程事务执行的锁竞争导致锁表
author: Teddy
date: 2020-05-13 15:43:29 +0800
categories: [实践, 需求实现]
tags: [PostgreSQL]
---

# pg数据库过程事务执行的锁竞争导致锁表



> 问题描述：pg数据库200+进程在同一分钟内对过程事务进行访问，事务在执行过程中会先后竞争 exclusive 和 raw exclusive 两个锁，由于持有锁并等待锁导致数据库锁表（t_device）, 被锁数据表无法进行任何操作和访问；且连接无法释放导致数据库访问连接达到pool的max值；



## 修复方案：

1.	将mark_device的复杂过程事务改为 agent heart beat的心跳上报；
2.	将监控设备的分配逻辑迁移到监控设备同步的功能上进行；

查询SQL

```sql
select count(*) from pg_stat_activity where wait_event_type = 'Lock';
select client_addr,client_port,wait_event_type,wait_event,state,query,backend_start,xact_start,query_start,state_change from pg_stat_activity where wait_event_type = 'Lock';
select count(*) from pg_stat_activity where wait_event_type is NULL OR wait_event_type = 'Lock';
select client_addr,client_port,backend_start,xact_start,query_start,state_change,wait_event_type,wait_event,state,query from pg_stat_activity where wait_event_type is NULL OR wait_event_type = 'Lock';
select count(*) from pg_stat_activity;
select client_addr,client_port,backend_start,xact_start,query_start,state_change,wait_event_type,wait_event,state,query from pg_stat_activity;
select client_addr,client_port,query,backend_start,xact_start,query_start,state_change,wait_event_type,wait_event,state from pg_stat_activity WHERE query NOT LIKE '%mark_device%';
```




锁表连接数

![]({{ "/assets/img/posts/pg-dead-lock_1.png" | relative_url }})

![]({{ "/assets/img/posts/pg-dead-lock_2.png" | relative_url }})