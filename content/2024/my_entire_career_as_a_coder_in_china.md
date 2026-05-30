# My Entire Career as a Coder in China

> 2024-10-09

A comprehensive retrospective covering the technical knowledge, system design patterns, infrastructure tooling, and interview preparation accumulated across a software engineering career in China — from algorithms to Kubernetes to SRE.

## Algorithms & Data Structures

A structured overview of the problem-solving toolkit built through years of LeetCode practice and competitive programming.

### I — Arrays & Hashing

Deterministic finite state machines (automata), two pointers, binary search, sorting, searching, divide and conquer, sliding window, stacks, and queues.

### II — Linked Lists

Single linked lists, double linked lists, and ring (circular) linked lists — traversal patterns, reversal, cycle detection (Floyd's algorithm), and merge operations.

### III — Trees

Binary trees, tries (prefix trees), heaps, and backtracking. Key patterns: DFS/BFS traversal, path sum problems, LCA (Lowest Common Ancestor), serialization/deserialization, and BST insertion/deletion.

### IV — Graphs

BFS and DFS traversal, topological sort, shortest path (Dijkstra, Bellman-Ford), union-find for connected components, and cycle detection in directed and undirected graphs.

### V — Dynamic Programming

Greedy algorithms, memoization vs tabulation, state transition modeling. Classic problems: knapsack variants, LCS, LIS, edit distance, matrix chain multiplication.

### VI — Bitwise Operations

Bit manipulation for performance optimization, XOR properties, bitmask DP, and integer overflow handling.

### VII — Time Complexity

Big-O notation mastery — analyzing nested loops, recursive calls, and amortized cost. Estimating runtime from constraints: O(n) for 10^8, O(n log n) for 10^6, O(n^2) for 10^4.

## System Design

### Distributed Systems

- **Load balancing** — Layer 4 (TCP) vs Layer 7 (HTTP), consistent hashing, least-connections, weighted round-robin
- **Replication** — leader-follower, multi-leader, leaderless (Dynamo-style); synchronous vs asynchronous replication
- **Sharding** — range-based, hash-based, directory-based; rebalancing strategies
- **Consistency models** — strong, eventual, causal, read-your-writes; the CAP theorem trade-off
- **CDN** — edge caching, cache hierarchies, TTL strategies, cache warming

### Storage Systems

- **SQL** — PostgreSQL and MySQL: B-tree indexing, query optimization, MVCC, connection pooling
- **NoSQL** — Cassandra (wide-column, LSM trees, tunable consistency), DynamoDB (key-value, on-demand scaling)
- **File systems** — distributed file systems (HDFS, Ceph), object storage (S3 API), block vs file vs object

### Caching Strategies

- Cache invalidation patterns: TTL, write-through, write-back, write-around
- Distributed caches: Redis (data structures, persistence, clustering), Memcached (simple, slab-based)
- Cache stampede protection: locking, probabilistic early recomputation

### Scalability

- **Horizontal vs vertical scaling** — scale-out trade-offs: stateless design, session management, data locality
- **Message queues** — Kafka (log-based, partitioned, consumer groups), RabbitMQ (exchange-based, flexible routing)
- **High availability** — N+1 redundancy, active-active vs active-passive, health checks, circuit breakers
- **Fault tolerance** — data replication, failover strategies, consensus protocols (Paxos, Raft)

## Infrastructure & Virtualization

### KVM & QEMU

KVM (Kernel-based Virtual Machine) is a **Type-1 hypervisor** built into the Linux kernel. It turns the kernel into a hypervisor by exposing `/dev/kvm` to userspace.

- **KVM** provides the CPU and memory virtualization via Intel VT-x / AMD-V hardware extensions
- **QEMU** (Quick Emulator) is the userspace component that provides device emulation (disk, network, PCI) and integrates with KVM for acceleration
- **Cloud Hypervisor** is a modern, Rust-based VMM designed for cloud-native workloads, also leveraging KVM

Key kernel features KVM depends on:

- **EPT (Extended Page Tables)** — hardware-accelerated guest memory translation
- **VPID (Virtual Processor Identifier)** — TLB tagging to avoid flushes on VM entry/exit
- **SR-IOV** — direct PCI device assignment to guests for near-native I/O performance

### Container Runtimes & Internals

#### Linux Kernel Namespaces (Isolation)

Namespaces provide the **isolation boundary** for containers. Each namespace type limits what a process can see:

| Namespace | Isolates | Relevant Syscall |
|---|---|---|
| **Mount** | File system mount points | `CLONE_NEWNS` |
| **PID** | Process IDs | `CLONE_NEWPID` |
| **Network** | Network interfaces, IP tables | `CLONE_NEWNET` |
| **UTS** | Hostname and domain name | `CLONE_NEWUTS` |
| **User** | UID/GID mapping | `CLONE_NEWUSER` |
| **IPC** | Inter-process communication (semaphores, message queues) | `CLONE_NEWIPC` |
| **Cgroup** | Control group view | `CLONE_NEWCGROUP` |

Key syscalls for namespace manipulation:

- `clone()` — create a child process in new namespaces
- `unshare()` — move the calling process into new namespaces
- `setns()` — join an existing namespace via a `/proc` file descriptor

#### Linux Control Groups (Resource Limits)

cgroups provide **resource accounting and limiting** for container workloads:

| Subsystem | Controls |
|---|---|
| **cpu** | CPU shares, quotas, and CFS bandwidth |
| **cpuset** | CPU core and memory node pinning |
| **memory** | Memory limits, OOM behavior, swap accounting |
| **blkio** | Block device I/O throttling and weighting |
| **devices** | Device node access control (`mknod`, `open`) |
| **freezer** | Suspend and resume process groups |

#### Union Filesystems (Layered Storage)

Union mount filesystems enable container image layers — each `RUN` instruction in a Dockerfile creates a new layer that stacks on previous ones:

- **OverlayFS** — the modern default; uses a merged view of `lowerdir` (read-only image layers) and `upperdir` (writable container layer)
- **AUFS** (Advanced multi-layered Unification Filesystem) — older, Docker's original union filesystem; now largely replaced by OverlayFS

```
┌─────────────────────────┐
│   Container (R/W layer) │ ← upperdir
├─────────────────────────┤
│   Image Layer 3         │
├─────────────────────────┤
│   Image Layer 2         │ ← lowerdir (merged)
├─────────────────────────┤
│   Image Layer 1 (Base)  │
└─────────────────────────┘
```

## Infrastructure as Code

- **Kubernetes** — pod lifecycle, controllers (Deployment, StatefulSet, DaemonSet, HPA), scheduling, RBAC, networking (CNI, Services, Ingress), storage (CSI, PV/PVC), etcd
- **Terraform** — declarative infrastructure provisioning, state management, modules, providers, plan/apply workflow
- **Ansible** — agentless configuration management, idempotent modules, playbooks, roles, inventory management

## SRE & Production Operations

Core SRE principles applied in practice:

- **SLOs & Error Budgets** — define the acceptable error rate; use the budget to gate releases and prioritize reliability work
- **Monitoring** — Prometheus metrics, Grafana dashboards, alerting with Alertmanager; the USE (Utilization, Saturation, Errors) and RED (Rate, Errors, Duration) methodologies
- **Incident Management** — blameless postmortems, runbooks, on-call rotation design
- **Capacity Planning** — load testing, traffic forecasting, auto-scaling policies

## Behavioral Interview — STAR Method

The **STAR** framework for structuring responses:

- **S**ituation — set the context: team, project, constraint, stake
- **T**ask — define the specific problem you owned and why it mattered
- **A**ction — describe what you did concretely; use "I" not "we"
- **R**esult — quantify impact: latency reduction, cost savings, reliability improvement

## Technologies & Tools Reference

| Domain | Tools |
|---|---|
| **OS / Hypervisor** | Linux, KVM, QEMU, Cloud Hypervisor |
| **Containers** | Docker, containerd, OverlayFS |
| **Orchestration** | Kubernetes, Helm, kubectl |
| **IaC** | Terraform, Ansible |
| **CI/CD** | Jenkins, GitHub Actions, ArgoCD |
| **Observability** | Prometheus, Grafana, Alertmanager |
| **Messaging** | Kafka, RabbitMQ |
| **Databases** | PostgreSQL, MySQL, Redis, Cassandra |
| **Languages** | Go, Python, C/C++, Bash |
