# Python Process Memory Analysis & Optimization

> 2020-03-30

Diagnosing and resolving excessive memory usage in long-running Python 2.7 production processes -- process introspection with pyrasite and GDB, garbage collection internals, CPython's three-layer memory allocator, and replacing ptmalloc2 with jemalloc via LD_PRELOAD.

## Production Baseline

### Physical Host (256 GB RAM)

Each Python process hovers around 2 GB RSS after hundreds of hours of uptime:

```
  PID    VIRT     RES     CPU%  MEM%  UPTIME
417593  4.33 GB  1.95 GB   8.9   0.8   891 hrs
641599  4.32 GB  1.92 GB   3.0   0.8  1219 hrs
641904  4.33 GB  1.97 GB   3.0   0.8  1359 hrs
641963  4.33 GB  1.93 GB   2.0   0.8  1263 hrs
```

On bare metal, 2 GB per process is 0.8% of total memory -- barely noticeable. But virtual machines tell a different story.

### Virtual Machine (16 GB RAM)

```
  PID    VIRT     RES     CPU%  MEM%  UPTIME
609083  4.12 GB  1.5 GB    2.3   9.5   109 hrs
643875  4.26 GB  1.7 GB    1.3  11.0    89 hrs
643877  4.19 GB  1.6 GB    1.3  10.6    86 hrs
671562  4.25 GB  1.7 GB    1.0  10.8    69 hrs
```

On a 16 GB VM, each process consumes 9-11% of total memory. With multiple processes per VM, this rapidly becomes the dominant resource consumer.

### Connection Distribution

The LVS (Linux Virtual Server) load balancer distributes traffic by weight:

| Environment | TCP Long Connections | LVS Weight | Per-Process Weight |
|---|---|---|---|
| VM | ~80 | 20 | 2 |
| Physical | ~120-140 | 100 | ~3.3 |

The number of persistent TCP connections per process scales with the LVS weight, which directly affects the volume of in-flight data and associated allocations.

## Workload Profile

The server handles HTTP payloads ranging from hundreds of bytes to several hundred KB. Its architecture:

- **I/O multiplexing** via Linux `epoll`, with `select`-based abstraction in Python.
- **80-140 connected file descriptors** per process, correlating with LVS weight.
- **25-thread `multiprocessing` pool** for CPU-bound work offloaded from the I/O loop.
- **Heavy data transformation**: metric parsing, dynamic monitoring calculations, and file I/O all produce significant intermediate objects -- dicts, lists, and custom data model instances.

The combination of long-running connections, thread-pool dispatch, and object-heavy processing creates continuous allocation pressure on the Python heap.

## Python Garbage Collection Internals

### Three-Generation Model

Python's GC (from the [official CPython 2.7 docs](https://docs.python.org/2/library/gc.html)) classifies objects into three generations based on how many collection sweeps they have survived:

- **Generation 0**: Newly allocated objects. Collected most frequently.
- **Generation 1**: Objects that survived one generation-0 collection.
- **Generation 2**: Objects that survived multiple collections. Collected least frequently.

### Collection Thresholds

Collection does NOT run on every allocation. Instead, the collector tracks the delta between total allocations and total deallocations since the last collection. When this delta exceeds `threshold0`, collection begins -- starting with generation 0 only:

```python
import gc
gc.get_threshold()
# (700, 10, 10)
```

The meaning of `(700, 10, 10)`:

1. When `allocations - deallocations` exceeds 700, generation 0 is collected.
2. Every 10 generation-0 collections triggers one generation-1 collection.
3. Every 10 generation-1 collections triggers one generation-2 collection.

In other words, generation 2 is only collected once every 7000 (10 x 700) allocations. For a process handling thousands of requests per hour, this means generation 2 objects can persist for a very long time.

### Manual Collection

The `gc` module exposes `collect()` for forcing garbage collection on demand:

```python
def collect(generation=None):
    """collect([generation]) -> n

    With no arguments, run a full collection. The optional argument
    may be an integer specifying which generation to collect. A
    ValueError is raised if the generation number is invalid."""
```

Calling `gc.collect()` with no arguments triggers collection of all three generations and returns the number of unreachable objects found.

### Why Long-Running Processes Grow

Objects that survive the first few collection sweeps are promoted to generation 2, where they can sit for hours or days before another sweep reaches them. In a process running for 1000+ hours, generation 2 accumulates many objects that are technically unreachable but have not yet triggered the inter-generational threshold. This is the primary mechanism behind the gradual memory growth observed in production, rather than a true leak.

Lowering the thresholds or periodically calling `gc.collect()` can reduce peak memory, but at the cost of more frequent GC pauses.

## CPython's Three-Layer Memory Model

Understanding CPython's memory architecture is critical for diagnosing why `free()` does not always return memory to the operating system:

### Layer 3: Python Object API
The topmost layer -- user code creating and manipulating Python objects (`dict`, `list`, `str`, custom class instances). Allocations at this layer delegate to the memory pool (Layer 1/2) for small objects.

### Layer 1 and 2: Memory Pool (PyMem_Malloc)
For allocation requests between **1 and 256 bytes**, CPython uses its internal memory pool manager (`PyMem_Malloc`). The pool manager:
- Calls `malloc()` to obtain large 256 KB **arenas** from the OS.
- Subdivides arenas into fixed-size blocks matching the requested allocation size.
- When an object is freed, the block is returned to the pool but the arena is **not** released back to the OS via `free()`.
- The arena is held in reserve for future allocations.

This means that once CPython's memory pool grows, it does not shrink back down -- `free()` is simply never called on the cached arenas. This is by design: it avoids fragmentation and syscall overhead for repeated small allocations.

### Layer 0: Large Allocations (>256 KB)
For allocation requests larger than 256 KB, CPython bypasses the memory pool entirely and calls `malloc()` directly. When such objects are freed, `free()` is called immediately, returning memory to the OS.

### Practical Consequence

A process that allocates many small objects (dicts, strings, tuples) during startup or under peak load will grow its arena pool permanently. Even after those objects are garbage-collected, the underlying memory remains allocated from the OS's perspective. The RSS (Resident Set Size) will not decrease; it will plateau at the peak arena usage.

This is why RSS stabilizes at ~2 GB in our case: the arena pool has reached a steady state matching the workload's allocation pattern.

## Hands-On Investigation: Attaching to a Running Process

### pyrasite: Code Injection into Live Processes

[pyrasite](https://github.com/lmacken/pyrasite) injects Python code into a running process without restarting it:

```bash
pip install pyrasite
pyrasite-shell <pid>
```

Once inside the shell, you can execute arbitrary Python in the target process's interpreter -- inspect variables, trigger garbage collection, and profile memory.

### guppy/heapy: Heap Object Profiling

[guppy](http://guppy-pe.sourceforge.net/) provides `heapy`, a tool for analyzing the Python heap and showing object counts and sizes by type:

```python
# Inside pyrasite-shell
from guppy import hpy
h = hpy()
h.heap()
```

Example output from a running process:

```
# Partition of a set of 48477 objects. Total size = 3265516 bytes.
#  Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
#      0  25773  53  1612820  49   1612820  49 str
#      1  11699  24   483960  15   2096780  64 tuple
#      2    174   0   241584   7   2338364  72 dict of module
#      3   3478   7   222592   7   2560956  78 types.CodeType
#      4   3296   7   184576   6   2745532  84 function
#      5    401   1   175112   5   2920644  89 dict of class
#      6    108   0    81888   3   3002532  92 dict (no owner)
#      7    114   0    79632   2   3082164  94 dict of type
#      8    117   0    51336   2   3133500  96 type
#      9    667   1    24012   1   3157512  97 __builtin__.wrapper_descriptor
# <76 more rows. Type e.g. '_.more' to view.>
```

The `iso()` method drills into specific objects:

```python
h.iso(1, [], {})
# Partition of a set of 3 objects. Total size = 176 bytes.
#  Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
#      0      1  33      136  77       136  77 dict (no owner)
#      1      1  33       28  16       164  93 list
#      2      1  33       12   7       176 100 int
```

This is particularly useful for spotting unexpected object types consuming disproportionate memory.

### Uncollectable Objects: gc.garbage

Some objects cannot be reclaimed even by full GC. The conditions are:

1. A **reference cycle** exists among a group of objects.
2. At least one object in the cycle defines a `__del__()` method.

The GC recognizes the cycle as garbage, but cannot determine a safe order to call `__del__()` on each object. As a result, the entire cycle -- including objects that do NOT define `__del__` but are reachable only through the cycle -- is moved into `gc.garbage` and **never freed**.

```python
# Inside pyrasite-shell
import gc
gc.collect()   # Run full collection; returns count of collected objects
gc.garbage     # Inspect uncollectable objects
# []
```

An empty `gc.garbage` list means no uncollectable cycles exist -- a strong signal that the memory growth is NOT caused by reference cycles with custom finalizers. This rules out a common class of "true" leaks.

If `gc.garbage` were non-empty, the investigation would proceed by examining each object's `__del__` method, breaking the cycle explicitly, then calling `del gc.garbage[:]` to release them.

### tracemalloc (Python 3.4+)

For Python 3, the built-in `tracemalloc` module provides per-line allocation tracking:

```python
import tracemalloc
tracemalloc.start()
# ... run application code ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

This pinpoints the exact source lines responsible for the most allocations -- invaluable for targeted optimization.

### objgraph

[objgraph](https://mg.pov.lt/objgraph/) visualizes object reference chains, making it easier to understand why specific objects are kept alive:

```python
import objgraph
objgraph.show_most_common_types()
# Find what references a specific object
objgraph.show_backrefs([my_object], filename='backrefs.png')
```

## GDB Debugging: Thread and Call Stack Analysis

When Python-level introspection is not enough, GDB with debug info can inspect the C runtime and CPython internals directly.

### Installing Debug Symbols

```bash
yum install python-debuginfo-2.7.5-86.el7.x86_64
yum install glibc-debuginfo-common-2.17-292.el7.x86_64
yum install gdb
```

### Attaching to a Running Process

```bash
gdb python <pid>
```

### Listing Threads

```gdb
(gdb) info threads
  Id   Target Id         Frame
  36   Thread 0x7f4b2bbad740 (LWP 404510) epoll_wait () at syscall-template.S:81
  35   Thread 0x7f4a7bb7a700 (LWP 412337) futex_abstimed_wait () at sem_waitcommon.c:43
  34   Thread 0x7f4a7c37b700 (LWP 412248) futex_abstimed_wait () at sem_waitcommon.c:43
  33   Thread 0x7f4a7cb7c700 (LWP 410227) futex_abstimed_wait () at sem_waitcommon.c:43
  32   Thread 0x7f4a7d37d700 (LWP 409187) futex_abstimed_wait () at sem_waitcommon.c:43
  ...
```

Observations from the production system:
- **Thread 36** (the I/O thread) is parked in `epoll_wait` -- expected behavior for the event loop waiting on file descriptors.
- **Threads 32-35** are blocked in `futex_abstimed_wait` -- these are the multiprocessing pool threads waiting for work items on a semaphore. They are idle, not stuck.
- After scaling up server capacity (increasing the number of processes sharing the same LVS weight), each process handles fewer connections, so threads spend more time idle. The high idle-thread count is a consequence of over-provisioning, not a bug.

### Switching Threads and Inspecting Python Source

```gdb
(gdb) thread 24
[Switching to thread 24 (Thread 0x7f4aadffb700 (LWP 404582))]
(gdb) py-list
334            waiter.acquire()
335            self.__waiters.append(waiter)
336            saved_state = self._release_save()
337            try:
338                if timeout is None:
>339                    waiter.acquire()
340                    if __debug__:
341                        self._note("%s.wait(): got it", self)
342                else:
343                    # Balancing act...
```

The `py-list` command shows Python source at the current execution point, with a `>` marker on the active line. Here thread 24 is inside `threading.Condition.wait()`, blocked on `waiter.acquire()` -- waiting for a signal on a condition variable. This is normal behavior for a thread-pool worker awaiting a task from the input queue.

### Python-Level Backtrace

```gdb
(gdb) py-bt
#4 Waiting for a lock (e.g. GIL)
#5 Waiting for a lock (e.g. GIL)
#7 Frame 0x7f4af4026420, for file /usr/lib64/python2.7/threading.py,
     line 339, in wait (self=<_Condition(...)>)
```

`py-bt` shows the Python call stack with parameter values. Combined with `py-list`, it reveals exactly what each thread is doing at the Python level.

### C-Level Backtrace

```gdb
(gdb) bt
#0  futex_abstimed_wait () at sem_waitcommon.c:43
#1  do_futex_wait () at sem_waitcommon.c:223
#2  __new_sem_wait_slow () at sem_waitcommon.c:292
#3  __new_sem_wait () at sem_wait.c:28
#4  PyThread_acquire_lock () at thread_pthread.h:323
#5  lock_PyThread_acquire_lock () at threadmodule.c:52
#6  call_function () at ceval.c:4408
#7  PyEval_EvalFrameEx () at ceval.c:3040
#8  PyEval_EvalCodeEx () at ceval.c:3640
```

The C backtrace confirms the thread is blocked on a POSIX semaphore (`sem_wait`) called through Python's thread lock API. The full chain: Python `Condition.wait()` -> `thread.lock.acquire()` -> `PyThread_acquire_lock()` -> `sem_wait()` -> `futex_abstimed_wait()` in glibc.

### Other GDB Python Extensions

| Command | Purpose |
|---|---|
| `py-bt` | Python-level backtrace with argument values |
| `py-list` | Show Python source around the current line |
| `py-up` / `py-down` | Move up/down one Python frame |
| `py-locals` | Print local variables in the current Python frame |
| `py-print <var>` | Look up and print a Python variable by name |
| `python-interactive` | Drop into an interactive Python REPL inside the process |

### Generating a Core Dump for Offline Analysis

Attaching GDB to a live process incurs a SIGSTOP pause. For extended analysis, generate a core dump and detach:

```gdb
(gdb) generate-core-file
```

This writes `core.<pid>` to the working directory. You can then load it offline:

```bash
gdb python core.<pid>
```

Core dumps are especially useful for investigating intermittent issues where you cannot risk pausing the production process for more than a few seconds.

## Memory Analysis Findings

### Investigation Results for This Service

1. **No memory leak**: RSS stabilizes at a plateau after startup and does not climb indefinitely. The growth from 700 MB at startup to ~1.5 GB over several hours is normal arena pool expansion -- not a leak.
2. **No uncollectable objects**: `gc.garbage` is consistently empty. No reference cycles with `__del__` exist in the codebase.
3. **Thread behavior is normal**: The `futex_abstimed_wait` threads are idle thread-pool workers, not deadlocked. After server capacity was increased, threads spend more time idle because each process handles fewer connections.

### GC Tuning Experiment

In a test environment, adding an explicit `gc.collect()` call at the end of each request handler (before returning the response) reduced steady-state RSS by **20-30%**. The trade-off is increased CPU time spent in GC -- roughly 50% of a single core at 5-minute average.

This confirms that the memory growth is GC-policy-driven, not a leak: objects that would have been promoted to generation 2 are instead collected while still in generation 0 or 1.

## Memory Allocator Options

Beyond Python's GC, the C runtime's `malloc` implementation directly affects fragmentation and RSS behavior.

### ptmalloc2 (glibc default, CentOS 7)

The default allocator in glibc 2.17. Uses multiple **arenas** (one per thread for contention reduction), with each arena managing its own free lists. Under multi-threaded workloads with mixed allocation sizes, arenas can fragment -- small free blocks become unusable for larger requests, causing the allocator to request more memory from the OS despite technically having enough total free space.

### jemalloc (Facebook)

[jemalloc](https://github.com/jemalloc/jemalloc) emphasizes:
- **Fragmentation avoidance**: size classes and thread-local caches minimize inter-thread contention while reducing unusable free-block gaps.
- **Scalable concurrency**: per-thread caches avoid the arena-lock contention that ptmalloc2 suffers under multi-threaded workloads.
- **Detailed statistics**: `malloc_stats_print()` provides runtime introspection into allocation patterns, fragmentation, and thread cache usage.

Available via `yum` on CentOS 7 as `jemalloc.x86_64`, no compilation required.

### TCMalloc (Google)

[TCMalloc](https://github.com/google/tcmalloc) uses:
- **Thread-caching**: each thread caches small allocations locally, batching deallocations back to the central heap.
- **Aggressive memory reuse**: deallocated memory is quickly recycled for new allocations of similar size.
- **Low overhead sampling**: built-in heap profiling without requiring a separate profiler library.

However, TCMalloc typically requires compilation from source on CentOS 7, making jemalloc the more practical drop-in replacement.

### Comparison Summary

| Allocator | Fragmentation | Multi-Thread | Availability (CentOS 7) |
|---|---|---|---|
| **ptmalloc2** | Can fragment under mixed-size, high-concurrency loads | Arena per thread; lock contention possible | Default, glibc 2.17 |
| **jemalloc** | Good; size classes and thread caching reduce fragmentation | Excellent; per-thread caches | `yum install jemalloc` |
| **TCMalloc** | Good; aggressive reuse minimizes fragmentation | Excellent; per-thread caching | Compile from source |

For this Python workload -- 25 threads, mixed small (strings, dicts) and medium (payload buffers) allocations -- jemalloc's fragmentation resistance makes it the best fit among readily available options.

## Final Solution: GC Tuning + jemalloc via LD_PRELOAD

The two-part optimization applied in testing:

### Part 1: Explicit Full GC

At the end of each request handler's processing, before returning the response to the I/O loop:

```python
import gc
gc.collect()  # Full collection of all three generations
```

### Part 2: Replace ptmalloc2 with jemalloc

Use LD_PRELOAD to dynamically link jemalloc instead of the default ptmalloc2 at process start:

```bash
LD_PRELOAD="/usr/lib64/libjemalloc.so" \
    /home/monitor_server/bin/python \
    /opt/netmon/service/monitor-server/monitor/run_server.py \
    --config-file /opt/netmon/service/monitor-server/monitor/conf/conf.ini \
    --port 51035 \
    >> /var/log/monitor-server/server_debug.log 2>&1 &
```

No code changes or recompilation required -- the dynamic linker intercepts all `malloc()`/`free()` calls and routes them through jemalloc.

### Results (15-Hour Stability Test)

| Metric | Before (ptmalloc2) | After (jemalloc + active GC) |
|---|---|---|
| **RSS** | ~2.0 GB | ~500 MB (+/- 50 MB) |
| **Memory % of total** | 0.8% (physical) / 9-11% (VM) | ~0.2% (physical) |
| **Stability** | Stable plateau at 2 GB | Stable plateau at 500 MB |
| **CPU overhead** | Baseline | ~50% of one core (5-min average) |

The combination of jemalloc and active GC reduced RSS by roughly 75%, from 2 GB to 500 MB. On virtual machines where memory is scarce, this difference is critical -- freeing 1.5 GB per process enables higher process density or additional services on the same host.

The CPU cost (~50% of one logical core at 5-minute average) is acceptable for this workload, given that memory was the binding constraint on VMs.

### Key Insight

The dramatic reduction was NOT just about GC. Replacing ptmalloc2 with jemalloc was the larger contributor: ptmalloc2's arena-based design retains memory in per-thread arenas even after Python frees objects. jemalloc's thread-caching and more aggressive return-to-OS policy allowed freed arenas to actually be released back to the kernel, shrinking RSS substantially.

## Recommendations for Similar Workloads

1. **Profile before tuning**: Use `pyrasite` + `guppy` to understand what types of objects dominate the heap. Rule out uncollectable cycles with `gc.garbage`.
2. **Lower GC thresholds as a first step**: `gc.set_threshold(500, 5, 5)` triggers more frequent collection without the CPU cost of per-request full GC.
3. **Consider jemalloc via LD_PRELOAD**: This is a zero-code-change, low-risk optimization. Test in staging first to confirm no regressions in throughput or latency.
4. **Monitor with RSS, not VIRT**: Virtual memory size is misleading on Linux. Track RSS (resident set size) and PSS (proportional set size, accounting for shared libraries) for accurate memory budgeting.
5. **For Python 3, prefer `tracemalloc`** over guppy for allocation tracking -- it is built-in, faster, and provides source-line granularity.
6. **Schedule periodic `gc.collect()` during idle windows** rather than on every request if the per-request overhead is too high. This balances memory pressure and CPU cost.

## References

- [pyrasite -- Inject code into a running Python process](https://github.com/lmacken/pyrasite)
- [Python 2.7 gc module documentation](https://docs.python.org/2/library/gc.html)
- [guppy/heapy -- Python heap analysis](http://guppy-pe.sourceforge.net/)
- [objgraph -- Python object reference graph visualization](https://mg.pov.lt/objgraph/)
- [jemalloc -- General-purpose scalable malloc implementation](https://github.com/jemalloc/jemalloc)
- [TCMalloc -- Google's customized malloc](https://github.com/google/tcmalloc)
- [Testing Memory Allocators: ptmalloc2 vs TCMalloc vs Hoard vs jemalloc](http://ithare.com/testing-memory-allocators-ptmalloc2-tcmalloc-hoard-jemalloc-while-trying-to-simulate-real-world-loads/)
- [Linux epoll man page](http://man7.org/linux/man-pages/man7/epoll.7.html)
- [Python Memory Management Deep Dive (drmingdrmer)](https://drmingdrmer.github.io/tech/programming/2017/05/06/python-mem.html)
- [I/O Multiplexing Overview (Chinese)](https://segmentfault.com/a/1190000003063859)
