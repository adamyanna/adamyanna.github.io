# Core Knowledge Base 2020

> 2020-04-12

My 2020 learning roadmap and knowledge framework — a structured reference covering CS fundamentals, applied systems engineering, distributed systems, and practical skills developed across February through April 2020.

---

## I. Computer Science Fundamentals

### 1. Programming Languages

#### C/C++

**Pointers and References**

The compiler builds a **symbol table** during compilation used for relocation during linking. C pointers and C++ references operate differently in this process:

- `*` (indirection operator) — dereferences a pointer to access the value at its target address
- `&` (address-of operator) — yields the memory address of a variable
- C++ **references** are aliases — semantically identical to accessing the original variable name; they cannot be reassigned and must be initialized at declaration
- C **pointers** are address holders — they can be reassigned, set to `NULL`, and support pointer arithmetic

**Memory Layout**

From low address to high address:

| Segment | Contents | Permissions |
|---|---|---|
| `.init`, `.text`, `.rodata` | Code, read-only data (format strings, jump tables) | Read / Execute |
| `.data` | Initialized global and static variables | Read / Write |
| `.bss` | Uninitialized global and static variables (zero-filled) | Read / Write |
| Heap | `malloc`-allocated memory, grows upward | Read / Write |
| Shared libraries | Memory-mapped regions for `.so` / `.dylib` | Read / Execute |
| User stack | Runtime stack frames, grows downward | Read / Write |

**Memory Allocators**

- **glibc `malloc`** — general-purpose allocator based on ptmalloc2 (Doug Lea's `dlmalloc` derivative)
- **Google TCMalloc** — thread-caching allocator; per-thread caches reduce lock contention in multi-threaded programs
- **Facebook jemalloc** — arena-based allocator optimized for fragmentation resistance and heap profiling

**`static` Storage Class**

- `static` global variable → allocated in `.data` or `.bss`, scoped to the translation unit
- `static` local variable → allocated in `.data` or `.bss`, persists across function calls, scope limited to the function

**Red-Black Trees in `std::map`**

C++ `std::map` is typically implemented as a red-black tree — a self-balancing BST guaranteeing O(log n) for insert, delete, and lookup. The tree balances via color invariants and rotations without the strict rebalancing overhead of AVL trees.

#### Go

**Goroutines**

Goroutines are user-level lightweight threads multiplexed onto OS threads by the Go runtime scheduler (M:N model). Key properties:

- **Stack**: Starts at ~2 KB, grows and shrinks dynamically (unlike fixed-size OS thread stacks)
- **Context switch**: ~200 ns within the same CPU core (vs ~1-2 μs for kernel thread switch)
- **Scheduler**: Work-stealing scheduler — when an OS thread runs out of goroutines, it steals from another thread's run queue
- **Preemption**: Cooperative + signal-based preemption (Go 1.14+) at safe points

**Go GC**

Concurrent, tri-color mark-and-sweep with a **write barrier** to track pointer mutations during marking. Targets sub-millisecond pause times by doing the majority of work concurrently with application goroutines.

#### Python

**CPython Virtual Machine**

The execution pipeline from source to bytecode:

```
.py source → Parse Tree → AST → Symbol Table → Control Flow Graph → Code Object → Frame → Execution
```

1. **Compilation**: Source is compiled to `.pyc` bytecode (Python VM instructions, not x86)
2. **Code Object (`PyCodeObject`)**: Contains bytecode instructions, stack size, flags, constants, variable names — allocated on the heap
3. **Frame**: Created at execution time, holds namespaces (local, global, builtin), stack for bytecode evaluation, reference to the current thread state
4. **Execution Loop**: `PyEval_EvalFrameEx` — a giant switch statement dispatching each opcode

**Thread State & GIL**

```
Python Process
  └── Interpreter State (one or more)
        └── Thread State (one per OS thread)
              └── Frame (current execution context)
```

The **Global Interpreter Lock (GIL)** is a mutex (`gil_mutex`) protecting the CPython interpreter state:

- Only the thread holding the GIL can execute Python bytecode
- GIL is released during I/O operations (allowing other threads to run)
- `sys.getswitchinterval()` (default 5 ms) — the interpreter checks `gil_drop_request` every eval loop iteration
- **Why it exists**: Simplifies CPython internals (no fine-grained locks), protects reference counting, and accommodates non-thread-safe C extensions

**Python Object Internals**

| Type | Implementation |
|---|---|
| `dict` | Hash table with open addressing; resizes at ~2/3 load factor |
| `list` | Dynamic array of `PyObject*` pointers; overallocates for amortized O(1) append |
| `str` | Compact string representation (PEP 393) — 1, 2, or 4 bytes per character depending on max code point |

**Coroutines**

- `yield` — suspends a generator, saving its frame state
- `greenlet` — userspace context switching via `setjmp`/`longjmp` (or native swap on some platforms)
- `gevent` — monkey-patches stdlib to make blocking I/O cooperative (libev event loop)

#### Shell

Shell builtins execute within the shell process itself (no `fork`+`exec`). System calls like `read()`, `write()`, `open()` map to kernel syscall numbers — each syscall has a unique integer ID used as an index into the kernel's syscall jump table.

---

### 2. Computer Networks

**OSI 7-Layer Model**

| Layer | Name | Protocols / Units |
|---|---|---|
| 7 | Application | HTTP, SSH, DNS, SMTP |
| 6 | Presentation | SSL / TLS |
| 5 | Session | Sockets, RPC |
| 4 | Transport | TCP (segments), UDP (datagrams) |
| 3 | Network | IP (packets), ICMP, BGP |
| 2 | Data Link | Ethernet frames, MAC addressing, switches |
| 1 | Physical | Bits on wire, fiber, radio |

**TCP Deep Dive**

**Segment Structure**: Source port, destination port, sequence number, acknowledgment number, flags (SYN, ACK, FIN, RST, PSH, URG), window size, checksum, urgent pointer.

**Connection Lifecycle** (Three-Way Handshake, Four-Way Teardown):

```
Client                              Server
  │ ──── SYN (seq=x) ────────────> │  (1) Client: SYN_SENT
  │ <─── SYN+ACK (seq=y, ack=x+1)─ │  (2) Server: SYN_RCVD
  │ ──── ACK (ack=y+1) ──────────> │  (3) Both: ESTABLISHED

  │ ──── FIN (seq=u) ────────────> │  (4) Active close: FIN_WAIT1
  │ <─── ACK (ack=u+1) ──────────  │  (5) Passive close: CLOSE_WAIT
  │ <─── FIN (seq=v) ────────────  │  (6) Passive: LAST_ACK
  │ ──── ACK (ack=v+1) ──────────> │  (7) Active: TIME_WAIT (2MSL)
```

**TCP State Machine**

| State | Meaning |
|---|---|
| `LISTEN` | Server socket awaiting connection requests |
| `SYN_SENT` | Client sent SYN, awaiting SYN+ACK |
| `SYN_RCVD` | Server received SYN, sent SYN+ACK, awaiting ACK |
| `ESTABLISHED` | Connection open, bidirectional data flow |
| `FIN_WAIT1` | Active closer sent FIN, awaiting ACK |
| `FIN_WAIT2` | Active closer received ACK, awaiting remote FIN |
| `CLOSE_WAIT` | Passive closer received FIN, sent ACK, waiting for local `close()` |
| `LAST_ACK` | Passive closer sent FIN, awaiting final ACK |
| `TIME_WAIT` | Active closer received FIN, sent final ACK, waiting 2MSL (~60s) |

**Why TIME_WAIT Exists** (2MSL duration):

1. Ensures the final ACK is delivered — if lost, the peer retransmits its FIN and we can re-ACK
2. Allows all stale segments from this connection to expire from the network before the same 4-tuple is reused

**Reliable Transmission**

- **Sequence numbers** — track byte offsets in the stream
- **ACKs and retransmission** — unacknowledged segments are retransmitted after RTO (Retransmission Timeout)
- **Fast retransmit** — 3 duplicate ACKs trigger immediate retransmission without waiting for timeout
- **Selective ACK (SACK)** — acknowledges non-contiguous blocks, allowing targeted retransmission

**Flow Control**

Receiver advertises a **receive window** (rwnd) — the amount of free buffer space. The sender must not have more unacknowledged bytes in flight than the receiver's window.

**Congestion Control**

| Phase | Mechanism |
|---|---|
| Slow Start | cwnd starts small (~MSS), doubles each RTT until threshold |
| Congestion Avoidance | cwnd increases linearly (~1 MSS per RTT) |
| Fast Recovery | After 3 dup ACKs, halves cwnd, enters recovery without resetting to slow start |
| Timeout | Resets cwnd to MSS, enters slow start |

**UDP**

Connectionless, no congestion or flow control. 8-byte header (src port, dst port, length, checksum). Used for DNS, streaming media, QUIC.

**IP**

- **IPv4**: 20-byte header, 32-bit addresses, fragmentation supported at routers
- **IPv6**: 40-byte header, 128-bit addresses, fragmentation only at endpoints

**Network Architecture**

- **L2 switching**: Forwards frames by MAC address; no TTL modification
- **L3 routing**: Forwards packets by IP address; decrements TTL; BGP/OSPF for route propagation
- **Core / Aggregation / Access**: Three-tier campus network design

**TCP vs UDP Socket Multiplexing**

Linux socket multiplexing with `select`, `poll`, `epoll`:

| Mechanism | Max FDs | Complexity | Best For |
|---|---|---|---|
| `select` | 1024 (FD_SETSIZE) | O(n) scan | Legacy, small FD sets |
| `poll` | Unlimited | O(n) scan | Medium FD sets |
| `epoll` | Unlimited (`/proc/sys/fs/file-max`) | O(1) callback | High-concurrency servers |

`epoll` uses an event-driven callback model — `epoll_ctl()` registers interest, and the kernel fires callbacks when FDs become ready, avoiding the linear scan of `select`/`poll`.

---

### 3. Data Structures & Algorithms

#### Core Data Structures

| Structure | Underlying Implementation | Key Properties |
|---|---|---|
| Array | Contiguous memory | O(1) random access, O(n) insert/delete |
| Linked List | Chained nodes | O(1) insert/delete at head, O(n) search |
| Hash Table | Array + collision resolution | O(1) avg lookup, O(n) worst |
| Heap | Complete binary tree in array | O(log n) insert/extract, O(1) peek |
| Binary Search Tree | Linked nodes, ordered | O(log n) avg, O(n) worst (unbalanced) |
| Red-Black Tree | Self-balancing BST | O(log n) guaranteed |
| B+ Tree | Multi-way balanced tree | O(log_b n) — disk-optimized (databases) |
| Graph | Adjacency list / matrix | Varies by representation |
| Bitmap | Bit array | O(1) membership test |

#### Hash Table Collision Resolution

- **Chaining**: Each bucket points to a linked list — simple but cache-unfriendly
- **Open addressing**: Linear/quadratic probing or double hashing — cache-friendly but requires careful deletion (tombstones). CPython uses open addressing with a `dk_indices` array.

#### Sorting Algorithms & Stability

**Stability**: An algorithm is stable if equal elements preserve their relative order after sorting.

| Algorithm | Average | Worst | Space | Stable |
|---|---|---|---|---|
| Bubble Sort | O(n²) | O(n²) | O(1) | Yes |
| Insertion Sort | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(1) | No |
| Merge Sort | O(n log n) | O(n log n) | O(n) | Yes |
| Quicksort | O(n log n) | O(n²) | O(log n) | No |
| Heapsort | O(n log n) | O(n log n) | O(1) | No |
| Shell Sort | O(n log n) ~ O(n^(4/3)) | Depends on gap | O(1) | No |
| Radix Sort | O(d·n) | O(d·n) | O(n+k) | Yes |

**Why stability breaks in unstable sorts:**

- **Quicksort**: The pivot swap can reorder equal elements when `a[j]` exchanges with `a[center_index]`
- **Heapsort**: Parent-child swaps during heap construction don't preserve original order among equal keys
- **Selection sort**: Swapping the minimum element into position can jump over equal elements

#### Master Theorem

For recurrences of the form `T(n) = a·T(n/b) + f(n)`:

| Case | Condition | Result |
|---|---|---|
| 1 | f(n) = O(n^{log_b a - ε}) | T(n) = Θ(n^{log_b a}) |
| 2 | f(n) = Θ(n^{log_b a}) | T(n) = Θ(n^{log_b a} · log n) |
| 3 | f(n) = Ω(n^{log_b a + ε}) + regularity | T(n) = Θ(f(n)) |

**Example — Quicksort**: a=2, b=2, f(n)=n. Since n^{log_2 2}=n, this is Case 2 → T(n) = Θ(n log n).

#### Algorithmic Patterns

| Pattern | When to Use | Classic Problems |
|---|---|---|
| Two Pointers | Sorted arrays, linked lists | 3Sum, Container With Most Water |
| Sliding Window | Subarrays, substrings | Longest Substring Without Repeating Characters |
| Divide & Conquer | Recursive decomposition | Merge Sort, Quickselect |
| Dynamic Programming | Optimal substructure + overlapping subproblems | Knapsack, LCS, Edit Distance |
| Greedy | Local optimum = global optimum | Activity Selection, Huffman Coding |
| Backtracking | Exhaustive search with pruning | N-Queens, Permutations, Sudoku |
| BFS / DFS | Graph and tree traversal | Number of Islands, Word Ladder |
| Binary Search | Sorted search space | Search in Rotated Array, Find Peak |
| Bit Manipulation | XOR properties, bitsets | Single Number, Power of Two |

---

### 4. Operating Systems

#### Processes

A **process** is a running instance of a program — an address space plus one or more threads of execution.

- Created via `fork()` + `execve()`
- Terminated via `exit()` (voluntary), signal (involuntary), or `kill`
- Arranged in a process tree rooted at `init` (PID 1)
- Three states: **running**, **ready**, **blocked**

The kernel maintains a **process table** — an array of process control blocks (PCBs) containing PID, parent PID, program counter, register state, stack pointer, priority, signal mask, CPU time, and child CPU time.

**Interrupt Handling Flow:**

```
1. Hardware pushes PC onto kernel stack
2. Hardware loads new PC from interrupt vector
3. Assembly saves registers
4. Assembly sets up new stack
5. C interrupt service routine executes
6. Scheduler picks next process
7. C returns to assembly
8. Assembly starts new current process
```

#### Threads

Threads are the **kernel's unit of scheduling**. Unlike processes, threads within the same process share the address space.

| Property | User-Level Threads | Kernel-Level Threads |
|---|---|---|
| Scheduling | In-process runtime (faster) | Kernel scheduler (slower, more overhead) |
| Blocking | Blocks entire process | Blocks only the thread |
| Multi-core | No true parallelism | Yes |
| Context switch cost | ~tens of ns | ~1-2 μs |
| Implementation example | `greenlet`, Go goroutines (mixed model) | `pthreads`, Linux `clone()` |

**Pthreads (POSIX threads):**
- `pthread_create` — spawn a new thread
- `pthread_join` — wait for thread termination
- `pthread_exit` — terminate calling thread
- `pthread_yield` — voluntarily yield CPU

#### Scheduling Algorithms

| Algorithm | Type | Description |
|---|---|---|
| FCFS (First-Come, First-Served) | Non-preemptive | Process queue; simple but poor for interactive workloads |
| SJF (Shortest Job First) | Non-preemptive | Minimizes average turnaround time; requires knowing job length |
| SRTN (Shortest Remaining Time Next) | Preemptive | Preemptive version of SJF |
| Round Robin | Preemptive | Fixed time quantum (20-50 ms typical); fair but context-switch heavy |
| Priority Scheduling | Preemptive | Priority classes with round-robin within each class |
| Multi-Level Queue | Preemptive | Multiple queues with different scheduling policies per queue |
| CFS (Completely Fair Scheduler) | Preemptive | Linux default — red-black tree ordered by vruntime, O(log n) selection |

#### Concurrency & Mutual Exclusion

**Critical Section Requirements** (must satisfy all four):
1. No two processes can be simultaneously inside their critical sections
2. No assumptions about CPU count or speed
3. No process running outside its critical section may block another
4. No process must wait forever to enter its critical section (no starvation)

---

### 5. Computer Architecture

#### Program Structure

The **Instruction Set Architecture (ISA)** defines the boundary between software and hardware:
- **CISC (x86)**: Variable-length instructions, many addressing modes, microcode translation
- **RISC (ARM)**: Fixed-length instructions, load-store architecture, simpler decode

**Y86** — a simplified educational ISA modeling x86 with fewer instructions and addressing modes.

#### Compilation Pipeline

```
Source (.c) → Preprocessor (cpp) → Compiler (cc1) → Assembler (as) → Linker (ld) → Executable
```

1. **Preprocessing**: Expand `#include`, `#define`, conditional compilation
2. **Compilation**: C → assembly (IR optimization, code generation)
3. **Assembly**: Assembly → `.o` relocatable object file (machine code + relocation entries + symbol table)
4. **Linking**: Resolve symbols across `.o` files and shared libraries, produce executable

#### Exceptional Control Flow (ECF)

ECF occurs at every level of the system:
- **Hardware**: Interrupts and exceptions (page faults, divide-by-zero)
- **OS Kernel**: Context switches between processes via timer interrupts
- **Application**: Signals (`SIGINT`, `SIGSEGV`, `SIGCHLD`), non-local jumps (`setjmp`/`longjmp`)

**Exception Types:**

| Type | Cause | Return Behavior |
|---|---|---|
| Interrupt | I/O device signal | Returns to next instruction |
| Trap | Intentional (syscall) | Returns to next instruction |
| Fault | Potentially recoverable error | Returns to current instruction or aborts |
| Abort | Unrecoverable hardware error | Does not return |

**Process Memory Image** (Linux x86-64, low to high addresses):

```
0x00000000 ─── unmapped (guard page)
0x00400000 ─── .text  (code)
            ─── .rodata (read-only constants)
            ─── .data  (initialized globals)
            ─── .bss   (uninitialized globals, zeroed)
            ─── heap   → (grows upward via brk/sbrk, mmap)
            ─── ...
            ─── shared libraries (mmap'd .so files)
            ─── ...
0x7fff0000 ─── user stack ← (grows downward, %rsp points to top)
0x7fffffff ─── kernel space (inaccessible from user mode)
```

---

## II. Applied Systems

### 1. Databases

#### Relational (PostgreSQL)

- **B+Tree indexes**: All data in leaf nodes, internal nodes store keys only; leaf nodes linked for range scans
- **BRIN indexes**: Block Range INdex — stores min/max per block range; ~6848x smaller than BTree for large tables; ideal for naturally ordered data (timestamps, sequential IDs)
- **Row-level locking**: `ROW EXCLUSIVE LOCK` during updates; `ACCESS EXCLUSIVE LOCK` for DDL
- **MVCC**: Multi-Version Concurrency Control — readers don't block writers and vice versa; dead tuples cleaned by `VACUUM`

#### Caching (Redis)

- In-memory key-value store with optional persistence (RDB snapshots, AOF log)
- Data types: strings, lists, sets, sorted sets, hashes, streams
- Eviction policies: LRU, LFU, TTL-based, random
- Pub/sub for message broadcasting within Redis

#### Time-Series (InfluxDB)

- Purpose-built for timestamp-indexed metric data
- Storage engine (TSM — Time-Structured Merge Tree) optimized for append-heavy writes
- Continuous queries for automatic downsampling and rollups

### 2. Distributed Systems

**Core concepts:**

- **Horizontal scaling**: Add more nodes (vs. vertical: add more resources to one node)
- **Replication**: Copy data across nodes for durability and read scaling (leader-follower, multi-leader, leaderless)
- **Sharding / Partitioning**: Split data across nodes by key range or hash for write scaling
- **CAP Theorem**: Choose 2 of 3 — Consistency, Availability, Partition Tolerance (during a partition, you pick C or A)

**Tools & Patterns:**

- **ZooKeeper** — distributed coordination (leader election, service discovery, distributed locks)
- **Load balancers** — L4 (TCP: HAProxy, LVS) and L7 (HTTP: Nginx, Envoy)
- **Message queues** — Kafka (distributed log, partitioned, consumer groups), RabbitMQ (AMQP, flexible routing)
- **Distributed locks** — Redis `SET NX`, ZooKeeper ephemeral znodes, etcd lease-based locks

### 3. Containers

#### Docker Internals

Docker rests on three Linux kernel primitives:

**Namespaces (Isolation)** — Limit what a process can see:

| Namespace | Isolates |
|---|---|
| Mount (`CLONE_NEWNS`) | Filesystem mounts |
| PID (`CLONE_NEWPID`) | Process IDs |
| Network (`CLONE_NEWNET`) | Interfaces, routing, iptables |
| UTS (`CLONE_NEWUTS`) | Hostname, NIS domain |
| User (`CLONE_NEWUSER`) | UID/GID mapping |
| IPC (`CLONE_NEWIPC`) | SysV IPC, POSIX message queues |
| Cgroup (`CLONE_NEWCGROUP`) | cgroup hierarchy view |

**Control Groups (Resource Limits)** — Limit what a process can use:

- `cpu` / `cpuset` — CPU shares, quota, core pinning
- `memory` — Memory limit, OOM killer behavior
- `blkio` — Block I/O throttling
- `devices` — Device access control
- `freezer` — Suspend/resume container processes

**Union Filesystems (Layered Storage)**:

- **OverlayFS**: Merges `lowerdir` (read-only image layers) with `upperdir` (writable container layer); modern default
- **AUFS**: Docker's original union filesystem; largely deprecated

#### Kubernetes

- **Pod**: Smallest deployable unit — one or more containers sharing network and IPC namespace
- **Controller patterns**: Deployment (stateless), StatefulSet (stateful with stable identities), DaemonSet (one per node), Job/CronJob
- **Service**: Stable virtual IP and DNS for pod access; kube-proxy manages iptables/IPVS rules
- **Ingress**: L7 routing (HTTP host/path-based) to services
- **HPA**: Horizontal Pod Autoscaler — scales pods based on CPU/memory or custom metrics

### 4. Monitoring & Observability

| Tool | Role |
|---|---|
| **Prometheus** | Metrics collection, time-series storage (TSDB), PromQL queries, Alertmanager integration |
| **OpenFalcon** | Chinese-origin monitoring system; agent-based metric collection with transfer/judge/graph components |
| **Grafana** | Visualization frontend for Prometheus, InfluxDB, Elasticsearch, and others |
| **ELK Stack** | Elasticsearch (search/index), Logstash (ingest), Kibana (visualize) — for log-based observability |

### 5. Cloud Networking & SDN

- **SDN (Software-Defined Networking)**: Decouples control plane from data plane; centralized controller programs forwarding tables on switches
- **NFV (Network Function Virtualization)**: Replaces dedicated hardware appliances (firewalls, load balancers) with virtualized instances
- **LVS (Linux Virtual Server)**: Kernel-level L4 load balancing via IPVS
- **Nginx**: L7 reverse proxy — HTTP load balancing, TLS termination, caching
- **iptables**: Netfilter-based packet filtering and NAT (SNAT, DNAT)

---

## III. Practical Skills

### IaaS Infrastructure Development

Building cloud infrastructure control planes in Python and Go — compute (VM lifecycle), networking (VPC, subnet, security group), storage (block and object).

### Linux Operations

- **Load Average**: 1-min, 5-min, 15-min exponential moving averages of runnable + uninterruptible threads. For an N-core system, a load of N.0 means the CPUs are fully utilized. Target: 0.7 × N cores.
- **`/proc` and `/sys`**: Kernel interfaces for runtime introspection and tuning
- **System calls**: `strace` for tracing; `perf` for profiling
- **`ulimit`**: Per-process resource limits (open files, stack size, virtual memory)

### Algorithm Problem Sets

Classic problems and their underlying patterns:
- 8-Queens (backtracking)
- Kth Largest Element (quickselect / heap)
- Serialize and Deserialize Binary Tree (tree traversal + design)
- Merge k Sorted Lists (heap / divide-and-conquer)
- LRU Cache (hash map + doubly-linked list)

---

## IV. Open Source Code Study

| Project | Focus |
|---|---|
| **CPython** | Virtual machine execution loop, object model (`PyObject`), memory management (`obmalloc`), GIL implementation |
| **Redis** | Event loop (`ae`), data structure encoding (ziplist, skiplist, intset), persistence (RDB, AOF), replication |
| **TCMalloc** | Thread-local caches, central free list, page heap; avoids per-thread lock contention |
| **jemalloc** | Arena-based allocation, size classes, thread-caching, heap profiling, fragmentation resistance |

---

## V. Cloud Computing: Future & Trends

The evolution of cloud infrastructure follows a clear trajectory:

```
Virtualization (2000s) → Containers (2010s) → Serverless / FaaS (2020s)
```

**Serverless (FaaS)**: Developers write functions; the provider handles deployment, auto-scaling, load balancing, and billing per-invocation. AWS Lambda, Azure Functions, Google Cloud Functions.

**Key trends driving this shift:**

1. **Developer velocity** — less infrastructure to manage means faster iteration
2. **Cost efficiency** — pay-per-use eliminates idle resource cost
3. **Autoscaling granularity** — scale individual functions, not entire VMs or pods
4. **Observability challenge** — distributed tracing across ephemeral functions requires new tooling (OpenTelemetry, X-Ray)

**Beyond serverless**: Edge computing (Cloudflare Workers, AWS Lambda@Edge), WebAssembly as a lightweight runtime (WASI), and AI-driven resource optimization in cloud schedulers.

---

## VI. Miscellaneous Problem Sets

### Concurrency

**Thread ordering problem**: Given threads A (C1 → C2) and B (C3), enforce execution order C1 → C3 → C2 without busy-waiting:

```
Solution:
  - Two boolean flags: did_c1, did_c3 (initially false)
  - One mutex protecting flag writes
  - Thread A: wait for (did_c3==true) before executing C2; yield CPU if not ready
  - Thread B: wait for (did_c1==true) before executing C3; yield CPU if not ready
```

### Database Deadlocks

**Transfer scenario** (Account A → Account B): Two concurrent transactions updating both accounts in different order causes circular wait. Solution: always acquire locks in a consistent global order (e.g., by account ID).

### TCP TIME_WAIT

**Problem**: High connection churn leaves many sockets in TIME_WAIT (~60s), exhausting ephemeral ports.

**Mitigations:**
- `tcp_tw_reuse` — allow reusing TIME_WAIT sockets for outgoing connections (client-side)
- Connection pooling — reuse established connections instead of opening new ones
- Reduce `tcp_fin_timeout` — shortens the TIME_WAIT duration

### Network Architecture

**Switch**: Forwards frames by MAC address via internal switching matrix; learns MAC→port mappings; each port has dedicated bandwidth.

**Router**: Forwards packets by IP address; decrements TTL; runs routing protocols (OSPF, BGP); segments broadcast domains.

**NAT Types:**
- **SNAT** (Source NAT): Replaces source IP — used for outbound traffic from private to public network
- **DNAT** (Destination NAT): Replaces destination IP — used for inbound port forwarding to internal services
- `POSTROUTING` chain → SNAT (after routing decision, before egress)
- `PREROUTING` chain → DNAT (before routing decision, on ingress)

---

## References

- *Computer Systems: A Programmer's Perspective* (CSAPP) — Bryant & O'Hallaron
- *Computer Networking: A Top-Down Approach* — Kurose & Ross
- *Modern Operating Systems* — Tanenbaum
- *Introduction to Algorithms* (CLRS)
- [CPython Internals](cpython_internals_virtual_machine_and_source_code_analysis.md)
- [Algorithm: Heap Sort Implementation](algorithm_heap_sort_implementation.md)
- [My Algorithm Learning Curve](my_algorithm_learning_curve.md)
