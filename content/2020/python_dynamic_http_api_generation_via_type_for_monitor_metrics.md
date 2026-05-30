# Python: Dynamic HTTP API Generation via `type()` for Monitor Metrics

> 2020-03-24

How to generate HTTP API endpoints dynamically from database-driven monitor configurations -- using Python's `type()` metaclass, Tornado routing, and OpenFalcon data structures. Adding a new monitoring item requires only a rule function and a database row -- zero API boilerplate.

## 1. Project Background

The system collects baseline metrics (CPU, memory, interface counters, errors) from network hardware devices -- switches, routers, firewalls across multiple vendors -- via SNMP and packages them into the OpenFalcon monitoring format. It was developed by a single developer.

**Core requirement:** monitoring items are managed entirely through a database table. Adding a new item should require nothing more than writing a processing rule function and inserting a row into that table -- no new handler classes, no manual route registration.

## 2. Dynamic API Generation Concept

The conventional approach of writing a handler class per metric and registering each in a routing table becomes unmaintainable as metrics multiply. The dynamic approach flipsthis: the *database* is the single source of truth. At startup, `RouteRegister.registerAPI()` queries the `t_monitor_item` table and for each row:

1. Creates a new Python class at runtime using `type()`
2. Registers it with the Tornado HTTP router via a `@get_mapping` decorator
3. Binds the class to `DynamicMetricDataHandler` which understands that metric's processing rules uniquely

The result: each monitoring item gets its own RESTful API endpoint, generated on the fly, without any static code.

## 3. Python's `type()` Metaclass

Python's `type` is the default metaclass. Writing `class Foo: pass` internally calls `type('Foo', (object,), {})`. Under the hood, `type` is a C struct in CPython -- `_typeobject` in `Objects/typeobject.c`:

```c
typedef struct _typeobject {
    int ob_refcnt;                    // Reference count
    struct _typeobject *ob_type;      // Type object pointer
    int ob_size;                      // Variable-length size (len)
    const char *tp_name;              // For printing, "<module>.<name>"
    Py_ssize_t tp_basicsize, tp_itemsize; // Allocation sizes
};
```

The key insight: `type()` returns a real class reference, allocated on the heap, that can be stored in a global registry and dispatched by the web framework like any statically defined class. This project uses:

```python
type(new_class_name, (MonitorMetricAPI,), {})
```

This creates a class inheriting from `MonitorMetricAPI` (which inherits from Tornado's `BaseHandler`), with the `_metric` class attribute pre-set to the database row before `type()` is called. The class inherits `process()` and all its behavior.

## 4. Route Registration -- Full Implementation

The entry point is `RouteRegister.registerAPI()`, called at module import time from `monitor/monitor-server/monitor/api/metric_api/dynamic_router_api.py`.

**Step 1 -- Load all items from the database:**

```python
@staticmethod
def loadAllAPIFromInventory():
    data = api.pg_query(MONITOR_ITEM_TB)
    return data
```

**Step 2 -- For each item, generate a class and bind a route:**

```python
@staticmethod
def registerAPI():
    raw_tasks = RouteRegister.loadAllAPIFromInventory()
    for raw in raw_tasks:
        if raw and raw.get('OpenFalcon_upload'):
            __route = str(raw["upload_api"])
            __des = str(raw["desc"])
            RouteRegister.bindRouteToMetircDataHandler(__route, __des, raw)
```

**Step 3 -- The core dynamic class factory:**

```python
@staticmethod
def bindRouteToMetircDataHandler(__route, __des, monitor_item):
    @get_mapping(__route, __des)        # Registers URL route with Tornado
    class MonitorMetricAPI(BaseHandler):
        _metric = ""

        def process(self):
            try:
                body = self.request.body
                content_type = self.request.headers.get("Content-Type", "")
                if content_type.startswith('application/json'):
                    data = escape.json_decode(body)
                    try:
                        dynamic = DynamicMetricDataHandler(
                            monitor_item=MonitorMetricAPI._metric
                        )
                        did_send_metric = dynamic.handler_distributor(
                            metric_raw=data
                        )
                        if did_send_metric:
                            return 1, 'success', {}
                        else:
                            return 0, 'failed', {}
                    except Exception as e:
                        LOG.error(
                            "Dynamic metric data handler bind failed! error=%s" % e
                        )
                        return 0, 'failed', {}
            except Exception as e:
                return 0, 'failed', {"Message": str(e)}

    if not monitor_item:
        return None
    MonitorMetricAPI._metric = monitor_item  # Bind DB fields to class before type()
    new_class_name = "".join(
        [v[0].upper() + v[1:] for v in __route.split("/")[-1].split("_")]
    )
    return type(new_class_name, (MonitorMetricAPI,), {})
```

Key design points:

- `@get_mapping` is the project's unified RESTful route decorator -- it registers the URL (e.g., `/monitor_upload/cpu_usage.do`) with Tornado's application router at decoration time.
- `MonitorMetricAPI._metric` is set to the full monitor item dictionary *after* the class body is defined but *before* `type()` creates the permanent subclass. The database fields are baked into each class as a static variable, accessible at request time with no additional database query.
- The class name is derived by converting the URL's last segment from `snake_case` to `PascalCase`: `/monitor_upload/if_in_errors.do` becomes class `IfInErrors`.
- In Tornado, `process()` is the handler entry point. It JSON-decodes the body, instantiates `DynamicMetricDataHandler` with the stored configuration, and delegates to `handler_distributor()`.

## 5. Database Table Structure (`t_monitor_item`)

Each row fully defines one monitoring item:

| Field | Type | Description |
|---|---|---|
| `id` | varchar | Primary key; unique item name (lowercase, underscores) |
| `vendor` | varchar | Device vendor |
| `type` | varchar | Device type (switch, router, firewall) |
| `model` | jsonb | Device model (vendor-defined) |
| `series` | jsonb | Device series (vendor-defined) |
| `metric` | varchar | Metric name used as OpenFalcon key and in dashboards/RRD |
| `metric_type` | int4 | `0` = gauge, `1` = gauge (incremental), `-1` = counter |
| `upload_api` | varchar | RESTful endpoint for agent data upload |
| `task` | jsonb | Agent collection task definition AND processing rules |
| `desc` | varchar | Human-readable description |
| `OpenFalcon_upload` | bool | Whether to forward data to OpenFalcon |
| `update_time` | timestamp | Last update time |
| `interval` | int4 | Agent collection interval in seconds |

The `task` JSONB column is the dual-purpose core: it encodes both what the agent should collect and how the server should process the results.

## 6. Task Definition Structure

```python
MonitorTaskJsonDic = {
    "snmp_task": {
        "oid": {
            'get': [],      # Single-value GET
            'bulk': [],     # Bulk GET
            'walk': [],     # Table WALK
            'getnext': []   # GETNEXT
        },
        "tag_rule": "",     # Tag processing rule name
        "opera_rule": "",   # Multi-OID operation rule name
        "value_rule": ""    # Value processing rule name
    }
}
```

The `oid` sub-document is synchronized into the agent's job configuration and associated with specific devices. Support for additional protocols (e.g., `netconf_task`) follows the same structure.

## 7. DynamicMetricDataHandler -- The Processing Engine

Located at `monitor/core/metric/dynamic/dynamic.py`. It receives a monitor item configuration and a raw JSON payload from the agent, then orchestrates parsing, rule matching, and metric dispatch.

### Initialization

```python
class DynamicMetricDataHandler(object):
    def __init__(self, monitor_item=None):
        mon_object = MonitorItemDataModel(**monitor_item)
        self._vendor = mon_object.vendor
        self._type = mon_object.type
        self._metric = mon_object.metric
        self._metric_type = mon_object.metric_type
        self._task = mon_object.task
        # ... other DB fields ...
        self.manage_ip = ""
        self.raw_data = {}
        self.timestamp = 0
        self.sysname = ""
        self.step = 0
        self.oid_data = {}
```

The constructor unpacks the database row via `MonitorItemDataModel` and initializes runtime fields to be populated from the agent payload.

### Raw Data Parsing

`_parse_metric_raw()` extracts standard fields from the agent's JSON payload:

```json
{
    "host": "10.0.0.1",
    "protocol": "snmp",
    "timestamp": 1572574430,
    "interval": 60,
    "response": {
        "get": {
            "1.3.6.1.4.1.2636.3.1.13.1.8.9.1.0.0": {
                "oid_index": "",
                "oid": "enterprises.2636.3.1.13.1.8.9.1.0.0",
                "snmp_type": "GAUGE",
                "value": "1"
            }
        }
    }
}
```

Mapping: `host` -> `manage_ip`, `response` -> `raw_data`, `timestamp` -> `timestamp`, `interval` -> `step`. The `sysname` is resolved from a `DeviceInfo` cache keyed by management IP.

### Raw Data Wrapper

`_raw_data_wrapper()` normalizes the response by iterating over each SNMP method key (`"get"`, `"walk"`, etc.) and each OID within, building a flat `{oid: [result_objects]}` dictionary. Single dict results are wrapped in a list for uniform downstream handling.

### Dispatcher

`handler_distributor()` inspects the task type and the structure of parsed OID data, then routes to one of three handlers:

```python
def handler_distributor(self, metric_raw=None):
    # ... parse raw data ...
    for task_type, task_content in self._task.iteritems():
        if task_type == "snmp_task":
            self._raw_data_wrapper()
            if len(self.oid_data.values()):
                if len(self.oid_data) > 1:
                    return self.snmp_multi_monitor_item_handler(task_content)
                if len(self.oid_data.values()[0]) > 1:
                    return self.snmp_batch_monitor_item_handler(task_content)
                else:
                    return self.snmp_single_monitor_item_handler(task_content)
        elif task_type == "netconf_task":
            pass  # Extension point
```

## 8. Three SNMP Processing Patterns

### 8.1 Single OID (`snmp_single`)

For SNMP GET returning one OID with one result. Extracts the `value` field, applies value/tag rules, and sends to OpenFalcon. Example -- CPU utilization:

```json
"response": {
    "get": {
        "1.3.6.1.4.1.2636.3.1.13.1.8.9.1.0.0": {
            "oid_index": "",
            "oid": "enterprises.2636.3.1.13.1.8.9.1.0.0",
            "snmp_type": "GAUGE",
            "value": "35"
        }
    }
}
```

### 8.2 Batch OID (`snmp_batch`)

For SNMP WALK returning one OID with multiple indexed results (distinguished by `oid_index`). Iterates over all result objects, builds a tag from each index (e.g., `"index=5"`), applies rules per object, and batch-sends. Example:

```json
"response": {
    "walk": {
        "1.3.6.1.2.1.2.2.1.14": [
            {"oid_index": "1", "oid": "ifInErrors", "value": "0", "snmp_type": "COUNTER"},
            {"oid_index": "4", "oid": "ifInErrors", "value": "0", "snmp_type": "COUNTER"},
            {"oid_index": "5", "oid": "ifInErrors", "value": "5", "snmp_type": "COUNTER"}
        ]
    }
}
```

Special handling: SNMP counter values of `"2147483647"` (max 32-bit signed int) are treated as zero.

### 8.3 Multi-OID (`snmp_multi`)

For multiple OIDs (e.g., separate WALKs for `ifInOctets` and `ifOutOctets`) requiring arithmetic combination. Delegates entirely to an `opera_rule` function which receives the full raw response and returns `[{value, tags}, ...]`. This is the most flexible pattern -- the operation rule performs arbitrary computation (e.g., bandwidth utilization as `(ifInOctets + ifOutOctets) * 8 / ifSpeed`).

## 9. Rule Engine -- Dynamic Dispatch

Three rule categories, each implemented as a class with `getattr()`-dispatched methods:

### ValueRules

Signature: `func(manage_ip, value, sysname)`. Transforms raw values -- parsing integers from strings with units (`"35%"` -> `35`), converting percentages to decimals, applying vendor-specific normalizations.

### TagRules

Signature: `func(manage_ip, oid_content)`. Generates tag strings in `"key1=value1,key2=value2"` format. Examples: mapping interface indices to interface names, attaching device role/location metadata.

### OperationRules

Signature: `func(manage_ip, raw_data)`. Handles cross-OID arithmetic. Receives all OID data and returns `[{value, tags}, {value, tags}, ...]`. Custom logic per metric.

### Dispatch Mechanism

```python
def _process_value_rule(self, rule_name, **kwargs):
    r = ValueRules()
    func = getattr(r, rule_name)
    return func(manage_ip=self.manage_ip, **kwargs)
```

Adding a new rule is adding a new method on the appropriate class -- no registry changes, no configuration files.

### Rule Execution Order and Selection

Rules apply: **ValueRules** -> **TagRules** -> **OperationRules** (multi-OID only).

| Scenario | Rule(s) to use |
|---|---|
| Single-value result (`"value": "35"`) | ValueRules |
| Indexed results with per-entry metadata | ValueRules + TagRules |
| Multiple OIDs needing combined computation | OperationRules only |

Generic ValueRules and TagRules can be reused across monitoring items.

## 10. Metrics Sender -- OpenFalcon Integration

`metrics_sender()` packages data into OpenFalcon's transfer format and publishes via `Falcon.send()`:

```python
def metrics_sender(self, value, tags):
    __OpenFalcon_metric_type = Metric_Type[self._metric_type]
    __v_type = Metric_Value_Type[self._metric_type]

    if __v_type == "float":
        value = float(value)
    else:
        value = int(value)

    m = {
        "endpoint": self.sysname,
        "metric": self._metric,
        "timestamp": self.timestamp,
        "step": self.step,
        "value": value,
        "counterType": __OpenFalcon_metric_type,
        "tags": tags
    }
    Falcon.send([m])
    return True
```

Metric type mappings:

```python
Metric_Value_Type = {1: "int", 0: "float", -1: "counter"}
Metric_Type = {1: "GAUGE", 0: "GAUGE", -1: "COUNTER"}
```

## 11. End-to-End Data Flow

1. **Agent polls device** via SNMP (GET/GETNEXT/WALK/BULK) using OIDs from `task.oid`
2. **Agent packages** results into JSON with metadata (host, timestamp, interval) and SNMP response nested under method keys
3. **Agent POSTs** to the dynamically generated endpoint (`upload_api` field)
4. **Tornado routes** to the dynamically created `MonitorMetricAPI` subclass
5. **`process()` instantiates** `DynamicMetricDataHandler` with the baked-in config
6. **Dispatcher inspects** the response structure and routes to single/batch/multi handler
7. **Rules execute** in order: value transform -> tag generation -> cross-OID computation
8. **`metrics_sender()` formats** the result as OpenFalcon metric and publishes

## 12. Error Handling

Multiple layers protect against data corruption:
- **SNMP-level errors** (TIMEOUT, UNKNOWN OID, NO_SUCH_INSTANCE, CONNECTION_ERROR, UNDETERMINED_TYPE_ERROR) are caught and logged with OID and host context
- **`_is_value_valid()`** rejects empty values and SNMP error keywords before rule processing
- **Structured error logging** (`_error_handler`) produces messages with device IP, sysname, vendor, type, model, series, and metric name -- enabling precise debugging of which device/metric combination failed
- All handlers catch exceptions, log them, and return `False` rather than crashing

## 13. Adding a New Monitoring Item

**Step 1 -- Insert a database row** with `vendor`, `type`, `model` (device targeting), `id`, `metric`, `metric_type`, `upload_api` (metric identity), `task` (collection + processing rules as JSONB), and `interval` (polling frequency).

**Step 2 -- Write rule functions if needed.** If the task references new rule names:

- **ValueRules**: receives `manage_ip`, `value`, `sysname`. Returns processed value.
- **TagRules**: receives `manage_ip`, `oid_content`. Returns `"key=value,key=value"` string.
- **OperationRules**: receives `manage_ip`, `raw_data`. Returns `[{value, tags}, ...]`.

**Step 3 -- Deploy.** The server loads all items at startup via `registerAPI()`. A periodic DB re-poll could enable hot-reload without restart.

## 14. Design Summary

- **Zero boilerplate**: New metrics are a DB row plus optional rule method -- no handler classes, no route config
- **Database as single source of truth**: Metrics, routes, rules, and collection tasks in one table -- enabling audit, replication, and programmatic management
- **Pluggable rule engine**: `getattr()` dispatch means new rules are new methods on existing classes
- **Protocol-agnostic**: Dispatcher supports `snmp_task`, `netconf_task`, and future protocols via the same structure

## References

- [CPython typeobject.c source](https://github.com/python/cpython/blob/master/Objects/typeobject.c)
