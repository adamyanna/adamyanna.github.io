# Go Performance Profiling & Monitoring

> 2020-04-05

Production-grade Go performance profiling with `runtime/pprof` and `net/http/pprof` -- CPU profiling, heap analysis, goroutine stack tracing, flame graph generation, interactive analysis workflows, and Prometheus metrics exposure.

## Two Integration Methods

### Method 1: HTTP Endpoint (`net/http/pprof`)

The simplest approach: import the side-effect package and expose the default HTTP mux. This registers profiling routes under `/debug/pprof`.

```go
import _ "net/http/pprof"

func main() {
    go func() {
        http.ListenAndServe("0.0.0.0:8080", nil)
    }()
    // ... application logic
}
```

Browse to `http://ip:port/debug/pprof` to inspect live profiling data without restarting the process.

### Method 2: File Writer (`runtime/pprof`)

For programmatic control over when profiling starts and stops, use `runtime/pprof` with `io.Writer`. This writes CPU and heap profiles to files that can be analyzed offline:

```go
import "runtime/pprof"

pprof.StartCPUProfile(f)   // begin CPU sampling, writes to io.Writer
pprof.WriteHeapProfile(f)  // snapshot current heap state
```

This approach is preferred when profiling a specific execution window -- start CPU profiling before the critical section, stop it immediately after, and optionally force a GC before capturing the heap.

## Production Example: Combined Approach

The following code embeds both methods in a production service. CPU profiling writes to a file for the entire run; the HTTP endpoint remains available for interactive debugging; and a heap profile is captured on graceful shutdown.

```go
func main() {
    binaryAbsPath, _ := filepath.Abs(filepath.Dir(os.Args[0]))

    cpuProfile := filepath.Dir(binaryAbsPath) + "/cpu_monitor.prof"
    memProfile  := filepath.Dir(binaryAbsPath) + "/mem_monitor.prof"

    fmt.Printf("[monitor] CPU profile  -> %s\n", cpuProfile)
    fmt.Printf("[monitor] MEM profile  -> %s\n", memProfile)
    fmt.Printf("[monitor] HTTP pprof  -> 127.0.0.1:8080\n")

    f, err := os.Create(cpuProfile)
    if err != nil {
        fmt.Printf("could not create CPU profile: %s\n", err)
    }
    if err := pprof.StartCPUProfile(f); err != nil {
        fmt.Printf("could not start CPU profile: %s\n", err)
    }

    runtime.GOMAXPROCS(runtime.NumCPU())

    // Expose HTTP pprof concurrently
    go func() {
        http.ListenAndServe("0.0.0.0:8080", nil)
    }()

    // Run application with OS signal handling
    pg := &program{}
    if err := svc.Run(pg, syscall.SIGINT, syscall.SIGTERM,
        syscall.SIGKILL, syscall.SIGQUIT); err != nil {
        fmt.Printf("run exit with err: %s\n", err)

        pprof.StopCPUProfile()

        f, err := os.Create(memProfile)
        if err != nil {
            fmt.Printf("could not create memory profile: %s\n", err)
        }
        runtime.GC() // Force GC for the most accurate heap snapshot
        if err := pprof.WriteHeapProfile(f); err != nil {
            fmt.Printf("could not write memory profile: %s\n", err)
        }
        f.Close()

        os.Exit(2)
    }
}
```

Key details:
- `pprof.StartCPUProfile` continuously samples the program counter at a fixed rate (default 100 Hz) until `StopCPUProfile` is called.
- `runtime.GC()` before `WriteHeapProfile` ensures the snapshot reflects truly live objects, not ones awaiting collection.
- The HTTP endpoint is available concurrently for on-demand goroutine and heap inspection.

## Understanding `/debug/pprof` Output

When you visit `http://ip:port/debug/pprof`, you see a summary of available profiles:

```
/debug/pprof/

Types of profiles available:
Count Profile
4    allocs
0    block
0    cmdline
1054 goroutine
4    heap
0    mutex
0    profile
13   threadcreate
0    trace
full goroutine stack dump
```

Each profile type serves a distinct purpose:

### allocs
A sampling of **all** past memory allocations (both live and freed). Useful for understanding cumulative allocation pressure over the process lifetime.

### block
Stack traces that led to blocking on synchronization primitives (mutexes, channels). A zero value here means no goroutines were observed blocked during the sampling window. Enable with `runtime.SetBlockProfileRate(1)`.

### cmdline
The command-line invocation of the current program. Useful in containerized environments to confirm flags and arguments passed at launch.

### goroutine
Stack traces of **all** currently running goroutines. High goroutine counts (e.g., 1054 above) warrant investigation: are goroutines leaking? Are they blocked on channels that never receive?

### heap
A sampling of memory allocations for **live** objects. Add the `?gc=1` query parameter to trigger a GC before the sample is taken, ensuring the profile reflects only reachable objects.

### mutex
Stack traces of holders of contended mutexes. Enable with `runtime.SetMutexProfileFraction(1)`.

### profile
CPU profile. The default page returns a 30-second sample. Add `?seconds=N` to adjust the duration. After downloading the profile binary, analyze with `go tool pprof`.

### threadcreate
Stack traces that led to the creation of new OS threads. High thread counts may indicate libraries spawning threads without Go's goroutine scheduler.

### trace
A trace of program execution. Add `?seconds=N`. After downloading, use `go tool trace` for a rich timeline view of goroutine scheduling, GC events, and blocking operations.

### Full goroutine stack dump
`/debug/pprof/goroutine?debug=2` returns the full text stack trace of every goroutine -- identical to what you would see on a SIGQUIT.

## Interactive Analysis with `go tool pprof`

The `go tool pprof` command enters an interactive shell for exploring profiles. The typical workflow:

```bash
go tool pprof cpu_monitor.prof
```

Once inside the interactive shell, these commands drive the investigation:

| Command | Purpose |
|---|---|
| `top` | Output top entries by flat (self) time, sorted by `flat%` |
| `topN` | Show top N entries (e.g., `top20`) |
| `web` | Generate a visual call-graph SVG and open it in a browser |
| `web FuncName` | Filter the call graph to nodes related to `FuncName` |
| `call_tree` | Create a context-sensitive call tree showing caller-callee relationships |
| `list FuncName` | Show annotated source code for functions matching a regex, with time spent per line |
| `help` | Print all available commands |
| `o` | Show and change display options |
| `peek FuncName` | Show callers and callees of a matching function |

### Prerequisites for `web`

On Linux, the `web` command requires `graphviz` (for `dot`) and `xdg-utils` (for `xdg-open`):

```bash
yum install graphviz xdg-utils   # CentOS/RHEL
apt install graphviz xdg-utils   # Debian/Ubuntu
```

On macOS, install `graphviz` via Homebrew; `open` is used automatically.

### Analysis Workflow

A systematic approach to profiling:

1. **Identify the hot function** -- Run `top` to find which function consumes the highest percentage of CPU sampling time.
2. **Visualize the call graph** -- Use `web FuncName` to generate a call graph filtered to that function and its callers/callees. This reveals the full call chain contributing to the cost.
3. **Inspect the source** -- Use `list FuncName` to see annotated source code with per-line timing. Focus on the data structures and algorithms inside the hot function.
4. **Hypothesize and benchmark** -- Propose an optimization, then validate with `go test -bench` to measure the impact quantitatively. Compare before-and-after profiles.

This iterative loop -- top, web, list, optimize, benchmark -- is the fastest path to meaningful performance improvements.

## CPU Profile Analysis: A Real-World Example

Here is actual output from a production monitoring service after a ~4-second CPU profile:

```
$ go tool pprof cpu_monitor.prof
File: libc-2.17.so
Build ID: 8b2c421716985b927aa0caf2a05d0b1f452367f7
Type: cpu
Time: Nov 11, 2019 at 6:07pm (CST)
Duration: 3.89s, Total samples = 22.57s (580.86%)
Entering interactive mode (type "help" for commands, "o" for options)
(pprof) top
Showing nodes accounting for 12980ms, 57.51% of 22570ms total
Dropped 254 nodes (cum <= 112.85ms)
Showing top 10 nodes out of 132
      flat  flat%   sum%        cum   cum%
    4470ms 19.81% 19.81%     4500ms 19.94%  runtime.chanrecv
    2260ms 10.01% 29.82%     6730ms 29.82%  runtime.selectnbrecv
    1290ms  5.72% 35.53%     1330ms  5.89%  encoding/json.stateInString
    1060ms  4.70% 40.23%     2190ms  9.70%  encoding/json.(*decodeState).scanWhile
     930ms  4.12% 44.35%     2020ms  8.95%  encoding/json.checkValid
     620ms  2.75% 47.10%     7100ms 31.46%  encoding/json.(*decodeState).object
     600ms  2.66% 49.76%     3810ms 16.88%  .../handler/analyzer.UploadEventToDB
     600ms  2.66% 52.41%     1630ms  7.22%  runtime.scanobject
     580ms  2.57% 54.98%      580ms  2.57%  runtime.memmove
     570ms  2.53% 57.51%     4090ms 18.12%  .../handler/analyzer.UploadMonitorCoverageData
```

### Interpreting the Columns

| Column | Meaning |
|---|---|
| `flat` | Time spent **directly** in this function (self-time) |
| `flat%` | Percentage of total samples spent in this function |
| `sum%` | Cumulative percentage down to this row |
| `cum` | Time spent in this function **plus all functions it called** (inclusive time) |
| `cum%` | Cumulative percentage including callees |

### What This Profile Tells Us

- **`runtime.chanrecv` (19.81% flat)**: The dominant self-time is spent receiving from channels. This suggests the service is goroutine-heavy with significant channel communication overhead.
- **JSON decoding dominates cumulatively**: `encoding/json.(*decodeState).object` accounts for 31.46% cumulative -- nearly one-third of all CPU time flows through JSON object parsing. The `checkValid`, `scanWhile`, and `stateInString` entries confirm JSON deserialization is the primary CPU bottleneck.
- **`UploadEventToDB` and `UploadMonitorCoverageData`**: These application-level functions consume ~17-18% of cumulative CPU each, with significant time in runtime operations rather than self-logic -- they are I/O-bound or JSON-bound.

### Actionable Next Steps

For this profile, the investigation would proceed as follows:

1. Run `web encoding/json.(*decodeState).object` to see which callers feed the JSON object decoder.
2. If the callers are `UploadEventToDB` and `UploadMonitorCoverageData`, examine whether these receive large JSON payloads that could be pre-parsed or streamed incrementally.
3. Consider replacing `encoding/json` with `encoding/json` alternatives (e.g., `json-iterator/go`, `bytedance/sonic`, or hand-rolled unmarshaling) for the hot paths.
4. Write a `go test -bench` benchmark around the JSON parsing to quantify any improvement.

## Heap / Memory Profile Analysis

Memory profiles are analyzed the same way as CPU profiles, but the profile type affects the top-level metrics:

```bash
go tool pprof mem_monitor.prof
```

### Profile Flags

When starting pprof, you can specify which memory statistic to display:

| Flag | Description |
|---|---|
| `-inuse_space` (default) | Live heap bytes currently in use |
| `-inuse_objects` | Number of live heap objects |
| `-alloc_space` | Total bytes allocated (including freed) |
| `-alloc_objects` | Total objects allocated (including freed) |

These flags can also be changed inside the interactive shell with the `o` (options) command.

### Real-World Memory Profile

```
$ go tool pprof mem_monitor.prof
File: libc-2.17.so
Build ID: 8b2c421716985b927aa0caf2a05d0b1f452367f7
Type: inuse_space
Time: Nov 11, 2019 at 6:07pm (CST)
Entering interactive mode (type "help" for commands, "o" for options)
(pprof) top
Showing nodes accounting for 573.38MB, 98.95% of 579.46MB total
Dropped 32 nodes (cum <= 2.90MB)
Showing top 10 nodes out of 27
      flat  flat%   sum%        cum   cum%
  173.51MB 29.94% 29.94%   184.01MB 31.76%  encoding/json.(*decodeState).literalStore
  158.42MB 27.34% 57.28%   158.42MB 27.34%  reflect.unsafe_NewArray
  105.63MB 18.23% 75.51%   105.63MB 18.23%  .../analyzer.(*DataContainer).AppendMetricList
   64.00MB 11.05% 86.56%   201.35MB 34.75%  .../analyzer.(*Analyzer).DataDistribution
   23.72MB  4.09% 90.65%    29.72MB  5.13%  sync.(*Map).Store
   20.76MB  3.58% 94.23%    20.76MB  3.58%  .../amqp.(*Channel).recvContent
   10.50MB  1.81% 96.04%    10.50MB  1.81%  encoding/json.(*decodeState).convertNumber
    8.34MB  1.44% 97.48%     8.34MB  1.44%  .../amqp.(*reader).parseBodyFrame
    5.50MB  0.95% 98.43%     5.50MB  0.95%  sync.newEntry (inline)
    3.00MB  0.52% 98.95%     3.00MB  0.52%  runtime.malg
```

### What This Profile Tells Us

- **`literalStore` (29.94%) and `unsafe_NewArray` (27.34%)**: Together, JSON decoding and reflection allocate over half the live heap (57.28% summed). `literalStore` holds parsed JSON token values; `unsafe_NewArray` suggests `reflect.New` is being used to allocate slices of decoded structs.
- **`AppendMetricList` (18.23%) and `DataDistribution` (11.05%)**: The business logic for storing and distributing metric data accounts for another ~30% of live heap. `DataDistribution` has a high cumulative (34.75%), meaning much of the JSON allocation happens inside it.
- **`sync.(*Map).Store` (4.09%)**: The use of `sync.Map` for metric storage contributes modestly but is worth monitoring for growth over time.

### Optimization Strategies for This Profile

1. **Reduce JSON allocations**: Use `json.Decoder` with `UseNumber()` to avoid intermediate `float64` allocations, or switch to a zero-allocation JSON library.
2. **Pool byte slices**: If `literalStore` allocations come from repeated parsing of similar-sized payloads, use `sync.Pool` for the underlying buffers.
3. **Pre-size maps and slices**: `AppendMetricList` likely grows slices incrementally with `append`; pre-allocating with `make([]Metric, 0, expectedSize)` would reduce copy-and-grow overhead.
4. **Replace `sync.Map` with a sharded map**: `sync.Map` is optimized for read-heavy, stable-key workloads. For write-heavy metric ingestion, a sharded `map[K]V` with per-shard `sync.Mutex` often performs better.

## Flame Graphs

A flame graph is a visualization of profiler data where:
- The **x-axis** represents the proportion of samples (width = sample count).
- The **y-axis** represents the call stack depth.
- Each **rectangle** is a function; the top edge shows what is "on CPU."

### Generating Flame Graphs from Go Profiles

The `go tool pprof` tool can generate flame graphs directly (Go 1.11+) or via the Brendan Gregg Perl scripts.

**Option A: Built-in pprof web UI (Go 1.11+)**

```bash
go tool pprof -http=:8081 cpu_monitor.prof
```

Then open `http://localhost:8081/ui/flamegraph` in a browser. This provides an interactive flame graph with search and zoom.

**Option B: Generate an SVG flame graph**

```bash
go tool pprof -flame > flame.svg cpu_monitor.prof
```

**Option C: Classic FlameGraph scripts**

```bash
go tool pprof -raw cpu_monitor.prof | \
    stackcollapse-go.pl | \
    flamegraph.pl > flame.svg
```

### Reading Flame Graphs

- **Wide rectangles** at the top indicate CPU-heavy leaf functions. These are the functions doing the actual work.
- **Tall stacks** indicate deep call chains; these may signal excessive abstraction or middleware nesting.
- **The x-axis colors** are arbitrary and do not convey meaning; focus on width.
- **Click to zoom** (in the interactive UI) on a rectangle to drill into a specific call path.
- **Search** for function names to highlight them across the entire graph.

A flame graph of the CPU profile above would show `chanrecv` and JSON decoding as wide blocks near the top, with `DataDistribution` and `UploadEventToDB` as wide mid-stack frames feeding into them.

## Benchmarking and Optimization Loop

Once profiling identifies a bottleneck, benchmarking validates that your fix actually helps:

```go
func BenchmarkJSONUnmarshal(b *testing.B) {
    data := []byte(`{"field":"value","nested":{"key":123}}`)
    for i := 0; i < b.N; i++ {
        var v MyStruct
        json.Unmarshal(data, &v)
    }
}
```

```bash
go test -bench=. -benchmem -cpuprofile=cpu_bench.prof -memprofile=mem_bench.prof
```

The `-benchmem` flag reports allocations per iteration, and the profile files let you verify that your optimization moved the needle on the same functions identified in the production profile.

## Prometheus Integration

In addition to pprof, Go services can expose Prometheus metrics for continuous monitoring rather than ad-hoc profiling.

### Basic Setup

The Prometheus Go client provides an HTTP handler for the `/metrics` endpoint:

```go
import "github.com/prometheus/client_golang/prometheus/promhttp"

func main() {
    http.Handle("/metrics", promhttp.Handler())
    panic(http.ListenAndServe(":9090", nil))
}
```

### Using the Gin Prometheus Middleware

For Gin-based services, the `go-gin-prometheus` module automates metric collection:

```go
import (
    "github.com/gin-gonic/gin"
    "github.com/zsais/go-gin-prometheus"
)

func main() {
    r := gin.Default()
    p := ginprometheus.NewPrometheus("gin")
    p.Use(r)
    r.Run(":9090")
}
```

This exposes standard HTTP metrics (request count, duration, in-flight requests) plus Go runtime metrics (goroutines, memory, GC) at `/metrics`.

### Prometheus Server Configuration

On the Prometheus server side, add a scrape target in `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'go-service'
    static_configs:
      - targets: ['service-ip:9090']
```

Hot-reload the Prometheus configuration:

```bash
curl -X POST http://prometheus-ip:port/-/reload
```

### What Metrics to Watch

| Metric | What It Reveals |
|---|---|
| `go_goroutines` | Goroutine leaks over time |
| `go_memstats_alloc_bytes` | Live heap size |
| `go_memstats_gc_cpu_fraction` | % of CPU spent in GC |
| `go_gc_duration_seconds` | GC pause time distribution |
| `process_open_fds` | File descriptor leaks |
| `http_request_duration_seconds` | Latency at the service boundary |

Set up alerting on these metrics to detect capacity degradation before users notice.

## Summary

A production Go performance toolkit should include:

1. **HTTP pprof endpoint** (`net/http/pprof`) for always-on, zero-config introspection.
2. **File-based profiles** (`runtime/pprof`) for capturing specific execution windows.
3. **Interactive pprof analysis** (`top`, `web`, `list`) to drill into CPU and memory hot spots.
4. **Flame graphs** for visualizing call stacks and identifying wide, costly functions.
5. **Benchmarks** (`go test -bench`) to validate optimizations quantitatively.
6. **Prometheus metrics** for continuous monitoring and alerting.

The workflow is always the same: measure first, hypothesize, optimize, and measure again.

## References

- [runtime/pprof](https://golang.org/pkg/runtime/pprof/)
- [net/http/pprof](https://golang.org/pkg/net/http/pprof/)
- [go tool pprof documentation](https://github.com/google/pprof)
- [Prometheus Go client](https://github.com/prometheus/client_golang)
- [Prometheus Blog -- Instrumenting Go Code](https://blog.pvincent.io/2017/12/prometheus-blog-series-part-4-instrumenting-code-in-go-and-java/)
- [FlameGraph (Brendan Gregg)](https://github.com/brendangregg/FlameGraph)
