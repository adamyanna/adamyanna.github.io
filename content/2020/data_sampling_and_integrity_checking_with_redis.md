# Data Sampling & Integrity Checking with Redis

> 2020-05-13

A production monitoring system must verify that every endpoint is reporting data on schedule and that the data is intact. This article walks through four architecture options — from a single-node prototype to a horizontally-scalable cluster — for building a data-sampling and integrity-checking audit system backed by Redis. All examples use Go and the `go-redis` library.

---

## 1. The Problem

A monitoring platform ingests metrics from thousands of endpoints. Each endpoint reports metrics at a fixed interval (e.g., 60 seconds). Two questions must be answered continuously:

1. **Coverage**: Are all expected endpoints reporting? Which ones have stopped?
2. **Integrity**: For those that are reporting, are the data points arriving on time without gaps?

Doing this inside the monitoring pipeline itself couples audit logic to ingestion, creating backpressure. The better approach is an out-of-band audit system that samples the incoming stream and validates independently.

---

## 2. Data Model

All four options share a common key schema derived from the monitoring taxonomy:

```
Key:   {endpoint} + {metric} + {tag}
       e.g., "server01&cpu_usage&region=us-east"

Value: Redis list of integers:
       [0] value       -- the metric value
       [1] timestamp   -- Unix epoch of the last reported sample
       [2] count       -- total samples received in the current window
```

If tags produce keys that exceed Redis's recommended key length, apply compression (e.g., hashing the tag portion with MD5 or xxHash).

---

## 3. Option 1: Single Node

The simplest approach: one writer and one reader sharing a Redis instance.

```
┌──────────────────┐     write      ┌─────────┐     read      ┌────────────────┐
│  monitor-torrent  │ ────────────► │  Redis  │ ◄──────────── │ monitor-patrol │
│  (ingestion side)  │               │         │               │  (audit side)   │
└──────────────────┘               └─────────┘               └────────────────┘
```

**monitor-torrent** holds persistent TCP connections to Redis. For each incoming metric:

1. Compute the key as `{endpoint}+{metric}+{tag}`
2. Update the list: set the value, set the timestamp, increment the count
3. The write is a `SET` or a Lua script that atomically updates all three fields

**monitor-patrol** periodically scans Redis and checks:
- Has the count advanced since the last check window?
- Is the timestamp within the expected range (not stale)?
- If a key is missing, has the endpoint stopped reporting?

**Challenges:**

| Problem | Impact |
|---------|--------|
| Single reader bottleneck | Scan latency grows linearly with key count |
| Multi-instance coordination | Distributed lock needed to avoid duplicate scans |
| Read distribution | How to partition the keyspace across patrol instances? |
| Hash-table iteration overhead | Each check cycle involves updating and scanning a large hash table, incurring goroutine context-switch and thread-safety overhead |

The core insight: the check itself is not computationally expensive (a few integer comparisons per key), but the iteration over a massive key space and the coordination between multiple patrol workers become the real bottleneck. **Stress-test the single-node path first** to locate the ceiling before adding distribution complexity.

---

## 4. Option 2: Horizontally Scalable Cluster

Add more patrol instances behind a Redis cluster:

```
                         ┌─────────┐
    ┌──────────────────► │  Redis  │ ◄──────────────────┐
    │                    │ Cluster │                     │
    │                    └─────────┘                     │
    │                          ▲                         │
    │                          │                         │
┌───┴──────────────┐  ┌───────┴───────┐  ┌──────────────┴───┐
│ monitor-torrent  │  │ monitor-patrol│  │ monitor-patrol   │
│    (writer)      │  │   instance 1  │  │   instance 2     │
└──────────────────┘  └───────────────┘  └──────────────────┘
```

**Design considerations:**

- The Redis cluster itself handles key sharding via hash slots — no application-level partitioning is strictly needed if keys are well-distributed.
- Patrol instances must divide the work. Options: assign key-prefix ranges, use Redis `SCAN` with different cursor starts, or implement a worker-queue pattern (push key batches into a Redis list, workers `LPOP`).
- Even with distribution, each patrol instance still iterates a large hash table. The bottleneck shifts from I/O to local concurrency: goroutine scheduling, lock contention on the local data structures, and the overhead of maintaining millions of per-key timestamps in memory.

**Recommendation:** profile a single patrol instance under realistic load to determine whether the bottleneck is CPU, memory bandwidth, or Redis I/O. Only add distribution if the single-instance ceiling is below the target.

---

## 5. Option 3: Offload Detection to Redis with Key Expiry

Instead of scanning the entire keyspace, let Redis itself detect gaps via key expiry:

**Data model (simplified):**

```
Key:   {endpoint} + {metric} + {tag}
Value: {timestamp}    -- single integer, not a list
TTL:   180 seconds    -- set on creation and refreshed on each update
```

**How it works:**

1. **monitor-torrent** writes each incoming metric as a key with a TTL of 180 seconds. If the key already exists, the `SET` (with `KEEPTTL` or re-set) refreshes the timestamp and resets the timer.
2. Redis keyspace notifications are enabled:
   ```
   notify-keyspace-events "AKE"
   ```
   - `A` = all events
   - `K` = keyspace events (`__keyspace@<db>__:<key>`)
   - `E` = keyevent events (`__keyevent@<db>__:<event>`)
3. A separate **event subscriber** process listens for:
   - `expired` -- a key's TTL elapsed without a refresh → **data gap detected**
   - `set` / `new` -- a previously missing key reappeared → **data recovered**
   - If a key expires and is never recreated → **data permanently lost**
4. The subscriber aggregates events, de-duplicates (multiple expiry events in a short window may signal the same outage), and records incidents to a relational database.

**Advantages:**
- No periodic scanning; Redis does the work of detecting staleness
- Zero application-level iteration over the key space
- Scaling is purely a Redis cluster concern — add shards as needed

**Caveats:**
- Keyspace notifications are fire-and-forget with no delivery guarantee. If the subscriber disconnects, events during the gap are lost.
- `expired` events may be delayed (Redis expiration is lazy + periodic). Do not rely on exact-second precision.
- The event stream can be noisy during network blips — implement a grace window and aggregation logic in the subscriber.

---

## 6. Option 4: Coverage-Based Sampling

This approach separates the concerns: sampling (what should be reporting?) from integrity (is it reporting on time?).

**Data model:**

```
Key:   {endpoint} + {metric}
Value: {timestamp}
```

**Design:**

1. **monitor-torrent** runs a timer (e.g., 20-minute window). For each incoming metric, it checks a **local in-memory map** keyed by `{endpoint}+{metric}`.
2. If the key is already present, skip the update — the endpoint/metric pair has already been sampled this window. This deduplicates millions of data points into a compact set of unique identifiers.
3. When the timer fires, the entire local map is flushed to Redis in a **single batch write**.
4. After the flush, the local map is cleared and the next window begins.

```
Time window (20 min)
├── t=0:   local map = {}
├── t=5:   event "server01&cpu_usage" → map["server01&cpu_usage"] = ts
├── t=10:  event "server01&cpu_usage" → already exists, skip
├── t=15:  event "server02&mem_usage" → map["server02&mem_usage"] = ts
├── t=20:  FLUSH entire map to Redis (pipeline batch)
│          clear local map
├── t=25:  ...
```

**The innovation:** sampling decouples throughput from cardinality. No matter how many data points arrive, the local map size is bounded by the number of unique endpoint×metric combinations, not the event rate.

**Benchmark results (1.4 million unique keys):**

| Metric | Value |
|--------|-------|
| Data objects | 1,400,000 |
| Mean flush time | 6–12 seconds |
| Benchmark runs | 5 consecutive |
| Consistency | 6–12 seconds across all runs |
| Redis version | Single instance, localhost |
| Client library | `go-redis` with pipeline |

---

## 7. Implementation: Go Benchmark Source

The full benchmark program that produced the results above. It queries a local API for endpoint and metric names, generates the Cartesian product as keys, then batch-writes them to Redis using a connection pool + pipeline.

```go
package benchmark

import (
    "encoding/json"
    "fmt"
    "github.com/go-redis/redis"
    "time"
)

// d_dev represents a monitored device.
type d_dev struct {
    Sysname string `json:"sysname"`
}

// metric represents a collection of metric names.
type metric struct {
    Metrics []string `json:"metric"`
}

func RedisBenchmark() {
    // --- Fetch the universe of endpoint names and metric names ---
    queryDevURL := "http://127.0.0.1:2345/data1?select=name"
    SysnameAll := GetSomething(queryDevURL, []d_dev{})

    queryTaskURL := "http://127.0.0.1:2345/data2?select=metric"
    MetricAll := GetSomething(queryTaskURL, []metric{})

    // --- Connection pool with tuned parameters ---
    c := redis.NewClient(&redis.Options{
        Addr:        "127.0.0.1:6380",
        Password:    "",
        DB:          0,
        MinIdleConns: 10,             // keep at least 10 idle connections
        IdleTimeout:  30 * time.Second, // close idle connections after 30s
        PoolSize:     120,            // maximum concurrent connections
    })

    // --- Generate the key space ---
    var AllData = make(map[string]int64)

    for _, sys := range (*SysnameAll).([]interface{}) {
        sysnamemap := sys.(map[string]interface{})
        for _, sysname := range sysnamemap {
            for _, ml := range (*MetricAll).([]interface{}) {
                for _, m := range ml.(map[string]interface{}) {
                    if m != nil {
                        for _, v := range m.([]interface{}) {
                            // Key format: {endpoint}&{metric}
                            AllData[sysname.(string)+"&"+v.(string)] = time.Now().Unix()
                        }
                    }
                }
            }
        }
    }

    fmt.Printf("Total unique keys to write: %d\n", len(AllData))

    // --- Verify connectivity ---
    pong, err := c.Ping().Result()
    if err != nil {
        fmt.Printf("Connection failed: %v\n", err)
        return
    }
    fmt.Printf("Connected: %s\n", pong)

    // --- Pipeline: bundle all SET commands into a single round-trip ---
    // go-redis pipelines send multiple Redis commands over one TCP write,
    // drastically reducing I/O overhead compared to per-command round-trips.
    p := c.Pipeline()

    // Warm-up key (optional, verifies pipeline is working)
    err = p.Set("endpoint+metric", time.Now().Unix(), 60*time.Second).Err()
    if err != nil {
        fmt.Printf("Pipeline initialization error: %v\n", err)
    }

    // Batch-write every key with a 60-second TTL
    for k, v := range AllData {
        err = p.Set(k, v, 60*time.Second).Err()
        if err != nil {
            fmt.Printf("Pipeline add error for key %s: %v\n", k, err)
        }
    }

    // Execute all commands and receive responses
    _, execErr := p.Exec()
    if execErr != nil {
        fmt.Printf("Pipeline execution error: %v\n", execErr)
    }

    fmt.Println("------ Benchmark complete ------")
}

// GetSomething performs an HTTP GET and unmarshals the JSON response
// into the provided slice type.
func GetSomething(url string, arr interface{}) *interface{} {
    resultByte, resultStatus, errj, _ := httputil.GetRequest(url, 60, nil, nil)
    if errj != nil || resultStatus != 200 {
        fmt.Printf("HTTP request failed: status=%d, error=%v, body=%s\n",
            resultStatus, errj, resultByte)
        return &arr
    }

    errj = json.Unmarshal(resultByte, &arr)
    if errj != nil {
        fmt.Printf("JSON unmarshal error: %v\n", errj)
    }

    return &arr
}
```

**Notes on the implementation:**

- The `Pipeline()` object accumulates commands in memory (no network calls) until `Exec()` is called. At that point, all commands are written to the TCP socket in a single `write()` system call, avoiding N individual round-trips.
- The connection pool parameters (`MinIdleConns`, `IdleTimeout`, `PoolSize`) are tuned for sustained throughput. Keeping idle connections warm avoids TCP handshake overhead on each burst.
- The local map `AllData` is built by computing the Cartesian product of endpoints and metrics. In production, this would come from a configuration database or service discovery.
- The 60-second TTL on each key mirrors Option 3's design — the key self-expires if not refreshed, providing a built-in staleness signal even without a patrol process.

---

## 8. Connection Pool Tuning

The benchmark's connection pool configuration is worth highlighting:

```go
redis.NewClient(&redis.Options{
    MinIdleConns: 10,              // Pre-warmed connections
    IdleTimeout:  30 * time.Second, // Close idle beyond this
    PoolSize:     120,             // Max concurrent connections
})
```

- `MinIdleConns` ensures that after a flush burst, 10 connections remain open for the next burst — no TCP handshake latency.
- `IdleTimeout` reclaims connections that sit unused, preventing file-descriptor exhaustion during quiet periods.
- `PoolSize` of 120 is sufficient to saturate a local Redis instance; reduce for remote Redis with higher RTT or increase for Redis Cluster where shards multiply the connection count.

---

## 9. Architecture Comparison

| Criterion | Option 1 (Single) | Option 2 (Cluster) | Option 3 (TTL+Events) | Option 4 (Sampling) |
|-----------|-------------------|--------------------|-----------------------|---------------------|
| Implementation complexity | Low | Medium | Medium | Medium |
| Scan load on Redis | High (full keyspace scan) | Medium (sharded scan) | None (event-driven) | Low (batch writes only) |
| Detection granularity | Per check cycle | Per check cycle | Near-real-time (TTL expiry) | Per sampling window |
| Delivery guarantee | Strong (synchronous) | Strong | Weak (fire-and-forget events) | Strong (map is written) |
| Best for | Prototyping, small datasets | Large datasets, multi-tenant | Gap detection with tolerance | Deduplicated coverage tracking |
| Scales with | Vertical (bigger Redis) | Horizontal (more shards + workers) | Horizontal (Redis Cluster) | Key cardinality, not event rate |

---

## 10. Key Takeaways

1. **Decouple sampling from integrity**. Option 4 separates "what exists" (sampling window) from "is it current" (integrity check). This is the cleanest separation of concerns.

2. **Pipeline for bulk writes**. The benchmark demonstrates that go-redis's pipeline reduces 1.4 million writes to a 6–12 second operation. Without pipelining, the same workload would take orders of magnitude longer.

3. **Redis can do the heavy lifting**. Option 3's TTL-and-notification design offloads staleness detection entirely to Redis, eliminating the need for application-level scanning.

4. **Know your bottleneck before distributing**. The core check operation (comparing a few integers) is not expensive. The real cost is key iteration, network round-trips, and goroutine coordination. Profile, then distribute.

5. **Connection pools matter**. A well-tuned pool with pre-warmed connections and reasonable idle timeouts is the difference between 6 seconds and 60 seconds for a bulk flush.
