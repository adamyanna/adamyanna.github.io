# Monitor System v1.5: Project Restructure

> 2020-05-14

A ground-up restructuring of the in-house monitoring platform — a Tornado-based Python system for multi-vendor network device telemetry. This article covers the component breakdown, agent-server model, heartbeat mechanism, high availability design, and all refactoring decisions that shaped the v1.5 architecture.

## Background and Motivation

The original system accumulated technical debt across several dimensions: API routes were scattered, metric processing logic intertwined with transport concerns, and vendor-specific code paths lacked a consistent abstraction. The v1.5 restructure addressed these by enforcing a layered architecture with clear data flow boundaries.

**Design goals for the restructure:**

- Separate API routing, data processing, and model layers
- Unify SNMP and NETCONF ingestion behind a single routing table
- Isolate vendor-specific processing into pluggable modules
- Introduce a heartbeat-based agent health model for device assignment
- Make the system horizontally scalable with stateless API servers and dedicated backend services

## High-Level Architecture

The system follows an **agent-server** model. Lightweight agents deployed across the network collect device metrics via SNMP, NETCONF, and custom protocol probes (HTTP, TCP, ping, process checks). Agents push raw data to the central server through REST endpoints (`.do` routes), which then normalizes, transforms, and forwards metrics to OpenFalcon for storage, visualization, and alerting.

```
Agent (per site/segment)               Central Server
┌─────────────────────┐              ┌──────────────────────────┐
│ SNMP collector      │─── .do ───▶  │ metric_process_api       │
│ NETCONF collector   │              │   ├── snmp_metric_api    │
│ Protocol probes     │              │   └── netconf_metric_api │
│ (ping/http/tcp)     │              ├──────────────────────────┤
└─────────────────────┘              │ core/metric/             │
                                     │   ├── vendor/ (per-vndr) │
                                     │   ├── protocol/          │
                                     │   └── wrapper/ → Falcon  │
                                     ├──────────────────────────┤
                                     │ OpenFalcon (tsdb+alert)  │
                                     └──────────────────────────┘
```

## API Routing Design

The restructure introduced a nested-routing convention. Each parent route maps to a handler table, where child routes specify a metric name and its processing function.

```python
"""
DES:
  Monitor project data processing entry point

  @API
  API = {
      "/monitor_upload/snmp/": MonitorUploadAPI,
  }
  Key: parent route
  Value: child route table for that parent

  @MonitorUploadAPI
  MonitorUploadAPI = {
      "xxx": {"metric": "x.xx", "handler": metric.xx.xxx}
  }
  Key: child route (the URL path suffix)
  Value: dict with keys "metric" (metric name string) and "handler"
         (processing function)
  Handler function signature must include: metric and data
"""
```

This design means adding a new vendor or protocol requires only:
1. Adding a vendor processing module under `core/metric/vendor/`
2. Adding a data wrapper under `core/metric/wrapper/vendor_wrapper/`
3. Registering the handler in the routing table

No changes to the API layer itself. The routing dispatch is entirely data-driven.

## Component Breakdown

### API Layer (`api/`)

Four sub-packages, each a self-contained Tornado request handler module:

| Package | Responsibility |
|---|---|
| `OpenFalcon_access_api` | All OpenFalcon interactions: alert group/template/user management, alarm name translation, metric data queries, alert silencing and un-silencing, alert view queries |
| `monitor_manage_api` | CRUD for agents, devices, and monitoring tasks against the `monitor-pg` PostgreSQL backend |
| `metric_process_api` | Raw data ingestion endpoints (`.do` suffix). Routes SNMP and NETCONF data per vendor |
| `third_access_api` | Third-party system integration, e.g., Zabbix circuit provisioning |

### Core Processing (`core/`)

The heart of the system, structured in four layers:

**`core/OpenFalcon/`** — Alert configuration engine. Receives calls from `OpenFalcon_access_api` and translates them into OpenFalcon's data model. Manages alert rule creation, template binding, and contact group association.

**`core/handlers/`** — Device information cache. Pre-loads device metadata into memory on server startup and refreshes on a configurable interval. All metric processing units query this cache rather than hitting the database directly, which is critical for throughput under high-frequency ingestion.

**`core/metric/`** — The metric processing pipeline. Three sub-layers:

- **`vendor/`** — Per-vendor raw data processing: Cisco (IOS/NX-OS), Huawei, H3C, Juniper, F5, Hillstone, Infoblox, Riverbed. Each module parses vendor-specific SNMP OID structures and NETCONF XML responses into a normalized intermediate format.
- **`protocol/`** — Custom protocol task processing: HTTP health checks, ICMP ping, TCP port checks, process monitoring. These are user-defined tasks (not device-bound), processed by dedicated handlers.
- **`wrapper/`** — Transforms normalized data into OpenFalcon's metric format. Includes common metric wrappers (CPU, memory, temperature), interface metric wrappers, protocol metric wrappers, and vendor-specific wrappers that handle proprietary MIBs.

**`core/model/`** — Data model definitions for both the OpenFalcon domain (`OpenFalcon_data_model.py`) and the internal monitor domain (`monitor_data_model.py`).

### Database Layer (`db/`)

A DAO-pattern database access module built on top of SQLAlchemy. Provides CRUD with merge support across:
- `device_manager_dao` — device lifecycle records
- `device_topo_dao` — network topology relationships
- `monitor_data_dao` — collected metric data
- `monitor_oper_dao` — operational records (device state changes)
- `monitor_task_dao` — agent task definitions
- `monitor_user_view_dao` — user-customized monitoring views

### Inventory (`inventory/`)

A registry of supported monitoring items and OIDs. Contains JSON files mapping vendor OIDs to metric names (e.g., `cisco_snmp.json`, `huawei_snmp.json`) and Python rule engines (`SnmpRule.py`, `NetconfRule.py`) that validate and dispatch collection tasks.

### Shared Modules (`pkg/`)

| Module | Purpose |
|---|---|
| `amqp` | RabbitMQ producer/consumer for async metric publishing; wraps `pika` with connection pooling and reconnection logic |
| `redis` | Redis read/write with connection management; used for agent heartbeat cache, temporary state, and rate limiting |
| `security` | RSA-based data encryption (`rsa_secure.py`) with key files for securing sensitive configuration and credentials in transit |
| `utils` | General-purpose toolkit: async helpers, daemon process management, date/time utilities, encryption utilities, file I/O, flow control, HTTP client, import helpers, file locking, structured logging, OS utilities, request helpers, result wrappers, thread helpers, time helpers |

### Configuration (`conf/`)

Multi-environment configuration: `conf.ini` (internal cloud), `conf_debug.ini` (development), `conf_efa.ini` (financial cloud), `conf_pub.ini` (public cloud). A central configuration registry (`__init__.py`) loads and validates all settings at startup.

## Entry Points and Service Model

The system runs as a set of independent processes, each with a dedicated entry point script:

| Entry Point | Service | Description |
|---|---|---|
| `run_server.py` | Web Server | Tornado HTTP server hosting all API routes; stateless, horizontally scalable |
| `run_agent_manager.py` | Agent Manager | Agent heartbeat monitoring and automatic device assignment/distribution |
| `run_cmdb_manager.py` | CMDB Sync | Periodic sync of device inventory from the CMDB into the monitoring database |
| `run_task_scheduler.py` | Task Scheduler | Unified entry for scheduled sync services (alarm translation, device lifecycle, task generation) |
| `run_service_debug.py` | Debug Runner | Runs all services in a single process for local development |

### Scheduled Services (`service/`)

These run under the task scheduler and implement periodic maintenance logic:

| Service | Function |
|---|---|
| `alarm_sync_service.py` | Synchronizes alarm name translations between OpenFalcon and internal systems |
| `cmdb_sync_service.py` | Pulls device inventory from CMDB and reconciles with the monitoring database |
| `device_distribution_service.py` | Inspects agent health status and redistributes devices among active agents |
| `device_manager_service.py` | Manages device lifecycle: onboarding, metadata updates, decommissioning |
| `monitor_oper_service.py` | Cleans up monitoring data for decommissioned devices, archives old records |
| `monitor_task_service.py` | Generates collection tasks for agents and syncs task configurations |

## Systemd Service Definitions

Each production service is managed by systemd:

```
etc/bin/
├── monitor-log.service       # Structured logging daemon
├── monitor-monitor.service   # Self-monitoring health checks
├── monitor-scheduler.service # Task scheduler process
└── monitor-server.service    # Web server process
```

## Agent Heartbeat and High Availability

Agents report heartbeat signals at a configurable interval through the metric ingestion endpoints. The `device_distribution_service` polls agent heartbeat timestamps from Redis:

1. If an agent misses N consecutive heartbeats, its devices enter an "unassigned" pool
2. The service selects a healthy agent from the same network segment (or nearest segment) and reassigns the orphaned devices
3. A dead-letter queue in RabbitMQ buffers undelivered metrics while reassignment is in progress, preventing data loss during failover

This heartbeat mechanism is the foundation of the system's high availability. The web server tier is stateless, so multiple `run_server.py` instances can sit behind a load balancer with session affinity. The agent manager and task scheduler are active-passive: only one instance of each runs at a time, with systemd handling restart-on-failure.

## Full Project Directory Tree

```
monitor/
├── __init__.py
├── api
│   ├── __init__.py
│   ├── OpenFalcon_access_api
│   │   ├── __init__.py
│   │   ├── alarm_group_manage_api.py        # Alert contact group management
│   │   ├── alarm_manage_api.py              # Alert lifecycle management
│   │   ├── alarm_template_manage_api.py     # Alert template & name translation
│   │   ├── alarm_user_manage_api.py         # Alert contact person management
│   │   ├── const.py                         # OpenFalcon API constants
│   │   └── falcon_handler_api.py            # Metric query, alert silence/view
│   ├── monitor_manage_api
│   │   ├── __init__.py
│   │   ├── agent_manage_api.py              # Agent CRUD (monitor-pg backed)
│   │   ├── device_manage_api.py             # Device CRUD
│   │   └── task_manage_api.py               # Task CRUD
│   ├── metric_process_api
│   │   ├── __init__.py
│   │   ├── netconf_metric_api.py            # NETCONF .do endpoints per vendor
│   │   └── snmp_metric_api.py               # SNMP .do endpoints per vendor
│   └── third_access_api
│       ├── __init__.py
│       └── zabbix_manage_api.py             # Zabbix circuit provisioning
├── conf
│   ├── __init__.py                          # Configuration registry
│   ├── conf.ini                             # Internal cloud
│   ├── conf_debug.ini                       # Development/test
│   ├── conf_efa.ini                         # Financial cloud
│   └── conf_pub.ini                         # Public cloud
├── core
│   ├── __init__.py
│   ├── OpenFalcon
│   │   ├── __init__.py
│   │   └── alarm_setting.py                 # Alert config engine (core)
│   ├── handlers
│   │   ├── __init__.py
│   │   └── device_info_handler.py           # Device cache pre-load & refresh
│   ├── metric
│   │   ├── __init__.py
│   │   ├── base.py                          # Base metric processor
│   │   ├── driver                           # Device driver implementations
│   │   │   ├── __init__.py
│   │   │   ├── cisco_firewall.py
│   │   │   ├── cisco_router.py
│   │   │   ├── cisco_switch.py
│   │   │   ├── h3c_switch.py
│   │   │   ├── huawei_switch.py
│   │   │   └── juniper_firewall.py
│   │   ├── protocol                         # Custom protocol task processing
│   │   │   ├── __init__.py
│   │   │   ├── http.py                      # HTTP health check tasks
│   │   │   ├── ping.py                      # ICMP ping tasks
│   │   │   ├── process.py                   # Process monitoring tasks
│   │   │   ├── snmp.py                      # SNMP custom OID tasks
│   │   │   └── tcp.py                       # TCP port check tasks
│   │   ├── publisher.py                     # Falcon data push (HTTP + RabbitMQ)
│   │   ├── vendor                           # Per-vendor raw data processing
│   │   │   ├── __init__.py
│   │   │   ├── cisco.py                     # Cisco IOS/NX-OS
│   │   │   ├── f5.py                        # F5 BIG-IP
│   │   │   ├── h3c.py                       # H3C Comware
│   │   │   ├── hillstone.py                 # Hillstone firewalls
│   │   │   ├── huawei.py                    # Huawei VRP
│   │   │   ├── infoblox.py                  # Infoblox DDI
│   │   │   ├── juniper.py                   # Juniper Junos
│   │   │   ├── nexus.py                     # Cisco Nexus NX-OS
│   │   │   └── riverbed.py                  # Riverbed Steelhead
│   │   └── wrapper                          # OpenFalcon format wrappers
│   │       ├── __init__.py
│   │       ├── common_metric.py             # Universal metric wrapper
│   │       ├── interface_metric.py          # Interface-level metric wrapper
│   │       ├── protocol_metric.py           # Protocol task metric wrapper
│   │       └── vendor_wrapper
│   │           ├── __init__.py
│   │           ├── cisco_metric.py
│   │           ├── f5_metric.py
│   │           ├── h3c_metric.py
│   │           ├── hillstone_metric.py
│   │           ├── huawei_metric.py
│   │           ├── infoblox_metric.py
│   │           ├── juniper_metric.py
│   │           ├── nexus_metric.py
│   │           └── riverbed_metric.py
│   └── model
│       ├── __init__.py
│       ├── OpenFalcon_data_model.py         # OpenFalcon domain model
│       └── monitor_data_model.py            # Internal monitor domain model
├── db
│   ├── __init__.py                          # DB access API (CRUD + merge)
│   ├── api.py                               # Connection & session management
│   ├── device_manager_dao.py
│   ├── device_topo_dao.py
│   ├── monitor_data_dao.py
│   ├── monitor_oper_dao.py
│   ├── monitor_task_dao.py
│   └── monitor_user_view_dao.py
├── inventory
│   ├── __init__.py
│   ├── cisco_snmp.json                      # Cisco OID → metric mappings
│   ├── huawei_snmp.json                     # Huawei OID → metric mappings
│   ├── NetconfRule.py                       # NETCONF collection rule engine
│   ├── SnmpRule.py                          # SNMP collection rule engine
│   └── TaskSupported.py                     # Supported task type registry
├── pkg
│   ├── __init__.py
│   ├── amqp
│   │   ├── __init__.py
│   │   ├── const.py                         # Exchange/queue/routing key constants
│   │   ├── metric_publisher.py              # Metric publishing to RabbitMQ
│   │   └── pika_util.py                     # pika connection pooling wrapper
│   ├── redis
│   │   ├── __init__.py
│   │   └── redis.py                         # Redis client wrapper
│   ├── security
│   │   ├── __init__.py
│   │   ├── key
│   │   │   ├── rsa.key                      # RSA private key
│   │   │   └── rsa.pub                      # RSA public key
│   │   └── rsa_secure.py                    # RSA encrypt/decrypt utilities
│   └── utils
│       ├── __init__.py
│       ├── async.py                         # Async execution helpers
│       ├── daemon.py                        # Daemon process management
│       ├── date_util.py                     # Date formatting & parsing
│       ├── encrypt_util.py                  # General encryption utilities
│       ├── file_util.py                     # File I/O helpers
│       ├── flow_util.py                     # Flow control (rate limiting, backoff)
│       ├── global_variable.py               # Global state management
│       ├── http_util.py                     # HTTP client wrapper
│       ├── import_util.py                   # Dynamic import utilities
│       ├── lock_util.py                     # File & distributed lock helpers
│       ├── logger.py                        # Structured logging
│       ├── os_util.py                       # OS-level utilities
│       ├── request_util.py                  # Tornado request helpers
│       ├── result.py                        # Standardized result wrapper
│       ├── thread_helper.py                 # Thread pool management
│       └── time_helper.py                   # Timezone & interval utilities
├── service
│   ├── __init__.py
│   ├── alarm_sync_service.py                # Alarm translation sync
│   ├── cmdb_sync_service.py                 # CMDB device sync
│   ├── device_distribution_service.py       # Agent heartbeat + device assignment
│   ├── device_manager_service.py            # Device lifecycle management
│   ├── monitor_oper_service.py              # Device sync & decommissioning
│   └── monitor_task_service.py              # Agent task generation & sync
├── run_agent_manager.py                     # Entry: agent health service
├── run_cmdb_manager.py                      # Entry: CMDB sync service
├── run_server.py                            # Entry: Tornado web server
├── run_service_debug.py                     # Entry: all services (debug mode)
├── run_task_scheduler.py                    # Entry: unified scheduler
├── etc
│   └── bin
│       ├── monitor-log.service
│       ├── monitor-monitor.service
│       ├── monitor-scheduler.service
│       └── monitor-server.service
├── docs
│   ├── api_docs
│   │   └── restful_api.yml                  # OpenAPI/Swagger spec
│   └── README.md
└── README
```

## Key Refactoring Decisions

1. **Routing table over decorator-based dispatch.** Instead of scattering `@route` decorators across files, the nested `API` dict convention keeps all routing visible in one place. This was chosen because the team needed to onboard new vendors quickly without understanding the full codebase.

2. **Vendor isolation.** Pre-v1.5, Cisco, Huawei, and H3C processing logic was interleaved in monolithic handler files. The restructure gives each vendor a dedicated module under `vendor/` and a corresponding wrapper under `wrapper/vendor_wrapper/`. Adding a new vendor now means adding two files and one routing entry — no existing code changes.

3. **Separate agent manager as a standalone process.** Originally, agent health checks ran inside the web server process, causing request latency spikes when Redis was slow. Extracting it into `run_agent_manager.py` isolates the health-check load and allows independent scaling.

4. **Pre-loaded device cache.** The `device_info_handler` loads all device metadata into a Python dictionary on startup and refreshes it periodically, rather than querying PostgreSQL on every metric ingestion. This reduces database load from thousands of queries per second to one query per refresh interval.

5. **AMQP as a buffer.** Metric publishing goes through RabbitMQ rather than being written synchronously. This decouples ingestion from storage, meaning a temporary OpenFalcon outage does not cause data loss — messages accumulate in the queue and are drained when OpenFalcon recovers.
