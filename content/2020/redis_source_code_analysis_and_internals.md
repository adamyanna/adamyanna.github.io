# Redis: Source Code Analysis & Internals

> 2020-03-31

A deep dive into Redis internals: compilation from source, the event-driven I/O model (ae event loop), core data structure encodings (sds, dict, ziplist, skiplist, intset), persistence engines (RDB, AOF), replication, Sentinel high availability, and Redis Cluster sharding.

---

## 1. Compilation & Installation

Building Redis from source on CentOS 7.4 (or any Linux distribution):

```bash
# Download latest stable release from https://redis.io

# Required static libraries are linked in:
#   - libhiredis    (C client library)
#   - libjemalloc   (memory allocator)
#   - liblua / lua-static (embedded Lua engine)

# The makefile resides in src/.
# GCC is invoked as the driver: preprocessor → compiler → assembler → linker.
make

# If linking fails due to stale object files or missing dependencies:
make distclean
make
```

After compilation, the interactive setup script configures the runtime:

```bash
cd utils
./install_server.sh
# Follow the prompts: port, config file, log file, data directory, executable path

# The script installs an init.d service; on systemd hosts:
systemctl start redis
systemctl enable redis
systemctl status redis
```

The resulting binaries include:
- `redis-server` -- the main daemon
- `redis-cli` -- command-line client
- `redis-benchmark` -- throughput/latency testing
- `redis-check-rdb` / `redis-check-aof` -- persistence repair tools
- `redis-sentinel` -- Sentinel binary (symlink to redis-server)

---

## 2. Architecture: The Event Loop (ae)

Redis is single-threaded and event-driven. All client commands, replication streams, and periodic tasks are processed through a single event loop implemented in `ae.c` / `ae.h`.

### 2.1 aeEventLoop Design

The `ae` library abstracts the underlying I/O multiplexer (`epoll` on Linux, `kqueue` on macOS, `select` as fallback). Its core data structures:

```
aeEventLoop
  ├── fileEvents[]      -- fd → {mask, rfileProc, wfileProc}
  ├── timeEvents[]      -- ordered list of {when_sec, when_ms, timeProc}
  ├── firedEvents[]     -- events ready for processing
  ├── beforesleep       -- callback invoked before each sleep cycle
  └── apidata           -- platform-specific multiplexer state (epoll fd, etc.)
```

### 2.2 Processing Cycle

```
while (server is running):
    1. beforesleep()       -- flush AOF, send queued replies, run cluster cron
    2. aeProcessEvents()   -- epoll_wait (or equivalent), dispatch file events
    3. aeTimeEvents()      -- invoke expired time events (serverCron, etc.)
```

This design yields predictable latency because there are no locks, no context switches during command processing, and each command is a small, atomic CPU burst. The trade-off is that a single slow operation (e.g., `KEYS *` or a large `DEL`) blocks the entire event loop.

### 2.3 I/O Threading (Redis 6+)

Starting with Redis 6, an optional threaded I/O layer delegates socket reads/writes to worker threads while command execution remains single-threaded. This is configured through:

```
io-threads 4
io-threads-do-reads yes
```

Threaded I/O amortizes `read()`/`write()` syscall overhead across multiple connections but preserves the atomicity guarantees of single-threaded command execution.

---

## 3. Core Data Structure Encodings

Redis uses memory-efficient internal encodings that adapt based on data size. The key types:

### 3.1 SDS -- Simple Dynamic Strings (`sds.h`, `sds.c`)

A drop-in replacement for C `char*` with O(1) length, binary safety, and buffer-overflow protection:

```
struct sdshdr {
    uint32_t len;        // current string length
    uint32_t alloc;      // allocated capacity (excluding header and null terminator)
    unsigned char flags;  // encoding type (sdshdr5/8/16/32/64)
    char buf[];           // the actual bytes (null-terminated for C interop)
};
```

Key properties:
- O(1) `strlen` via the `len` field (no scanning for `\0`)
- Pre-allocation and lazy freeing reduce `realloc` churn
- Binary-safe: embedded null bytes are fine
- Compatible with standard C string functions via the guaranteed null terminator

### 3.2 Dict -- Hash Table (`dict.h`, `dict.c`)

Redis's core dictionary uses separate chaining with incremental rehashing:

```
typedef struct dict {
    dictType *type;         // type-specific function table
    dictEntry **ht_table[2]; // two hash tables (ht[0] active, ht[1] for rehash)
    unsigned long ht_used[2];
    long rehashidx;          // -1 if not rehashing, else index of next bucket
    int iterators;           // number of safe iterators preventing rehash step
} dict;
```

Incremental rehashing: instead of copying the entire table at once (which would block the event loop), Redis spreads the work across subsequent `dictAdd`/`dictFind`/`dictDelete` calls and a server cron task. Each step rehashes `n` buckets from `ht[0]` to `ht[1]`. This is why a `BGSAVE` on a large dataset does not cause a latency spike.

The hash function is MurmurHash2 for keys (Redis 5+) and SipHash for hash-slot computation (protection against hash-collision DoS).

### 3.3 Ziplist -- Compact Sequential List (`ziplist.c`)

A doubly-linked list stored in a single contiguous memory block:

```
<zlbytes> <zltail> <zllen> <entry> <entry> ... <entry> <zlend>
```

Each entry encodes its previous-entry length and its own length as variable-length integers, followed by the payload. Ziplist is used as the small-representation encoding for:
- Lists (replaced by quicklist since Redis 3.2)
- Hashes (when field count < `hash-max-ziplist-entries` and value size < `hash-max-ziplist-value`)
- Sorted Sets (when element count < `zset-max-ziplist-entries`)

Advantages: excellent cache locality, minimal per-element overhead. Disadvantages: O(n) insertion/deletion because subsequent entries must be shifted; cascading updates when entry lengths change.

### 3.4 Quicklist (Redis 3.2+)

A linked list of ziplists, replacing the old linkedlist + ziplist dual encoding for the List type:

```
quicklist
  ├── head → quicklistNode (ziplist)
  ├── tail → quicklistNode (ziplist)
  ├── count  -- total elements across all nodes
  └── len    -- number of nodes
```

Each node holds a ziplist of up to `list-max-ziplist-size` elements. A configurable fill factor controls compression of interior nodes (LZF) to trade CPU for memory on rarely-accessed middle portions of long lists.

### 3.5 Skiplist -- Probabilistic Index Structure (`server.h` -- `zskiplist`)

Used by Sorted Sets for the large-representation encoding. A skiplist is a multi-level linked list where each node is promoted to higher levels with a fixed probability (typically 0.25):

```
zskiplist
  ├── header → zskiplistNode (sentinel, max level)
  ├── tail
  ├── length   -- element count
  └── level    -- current max level

zskiplistNode
  ├── ele       -- SDS string (member)
  ├── score     -- double (sort key)
  ├── backward  -- pointer to previous node
  └── level[]   -- array of {forward pointer, span} per level
```

Query complexity: O(log n) expected (probabilistic balancing). Range queries walk forward at the lowest level after finding the starting point via higher levels. The `span` field on each forward pointer enables O(log n) `ZRANK` / `ZRANGE` by tracking the number of elements skipped between nodes at each level.

### 3.6 Intset -- Integer Set (`intset.c`)

A sorted array of unique integers stored in a contiguous block:

```
typedef struct intset {
    uint32_t encoding;  // INTSET_ENC_INT16, _INT32, or _INT64
    uint32_t length;     // number of elements
    int8_t contents[];   // actual data (type determined by encoding)
} intset;
```

Used as the small representation for Sets when all members are integers and the set cardinality is below `set-max-intset-entries`. O(log n) search via binary search. Insertion upgrades the encoding width if a new value exceeds the current range, copying and widening every element.

---

## 4. Data Types & Dual Encodings

| Type | Small Encoding | Large Encoding | Threshold Config |
|------|---------------|----------------|------------------|
| String | embedded (≤44 bytes) | raw SDS | -- |
| List | quicklist (ziplist nodes) | -- (always quicklist) | `list-max-ziplist-size` |
| Set | intset | dict (with NULL values) | `set-max-intset-entries` |
| Sorted Set | ziplist | dict + skiplist (dual) | `zset-max-ziplist-entries` |
| Hash | ziplist | dict | `hash-max-ziplist-entries` |

The dual encoding for Sorted Sets (dict + skiplist) warrants special attention. The dict maps member → score for O(1) lookups, while the skiplist maintains the score ordering for O(log n) range queries. Both structures share the same objects (member strings, score values) to avoid duplication. The trade-off is ~2x memory overhead compared to the ziplist encoding, accepted only when the set exceeds the threshold.

---

## 5. Persistence

### 5.1 RDB -- Point-in-Time Snapshots

RDB serializes the dataset to a compact binary file (`dump.rdb`) at a specific point in time. Triggered by:

- `SAVE` -- synchronous, blocks the server
- `BGSAVE` -- forks a child process that writes the RDB while the parent continues serving requests
- `save <seconds> <changes>` -- automatic triggering from `redis.conf`

The forked child uses copy-on-write memory, so memory usage can spike up to 2x during a save if the parent is heavily mutating keys. The RDB format encodes type-by-type with length-prefixed strings, integer-encoded lengths, and ziplist-style compact representations.

### 5.2 AOF -- Append-Only File

AOF logs every write operation as an equivalent Redis command. Rewriting (`BGREWRITEAOF`) compacts the log by forking a child that writes the minimal command sequence needed to reconstruct the current dataset, replacing the old AOF atomically.

fsync strategies:
- `appendfsync always` -- fsync after every command (safest, slowest)
- `appendfsync everysec` -- fsync once per second (good compromise, default)
- `appendfsync no` -- let the OS decide (fastest, riskiest)

### 5.3 RDB+AOF Hybrid (Redis 5+)

`aof-use-rdb-preamble yes`: the AOF rewrite child first writes an RDB snapshot of the current state, then appends AOF commands for operations that occurred during the rewrite. On restart, the RDB portion loads fast, and the AOF tail is replayed. This combines the fast startup of RDB with the durability of AOF.

---

## 6. Replication

Redis replication follows a master-replica model:

1. **Full resynchronization**: When a replica first connects (or after a replication timeout), the master forks a child to produce an RDB. The master buffers all write commands during RDB generation in a **replication backlog** (a fixed-size circular buffer). The replica loads the RDB, then replays backlogged commands.

2. **Partial resynchronization** (`PSYNC`): If a replica reconnects and its last-seen replication offset still falls within the backlog, only the missed commands are streamed. This avoids a full RDB transfer.

3. The replication backlog is sized by `repl-backlog-size` (default 1 MB). A larger backlog tolerates longer disconnections without needing a full sync.

4. Replicas are read-only by default. Writes to replicas are rejected unless `replica-read-only no` is set.

5. **Replication ID**: Each master generates a unique `replid` at startup. The `replid2` field stores the previous master's ID after a failover, enabling safe partial sync to the new master.

---

## 7. Sentinel -- High Availability

Redis Sentinel is a distributed monitoring and failover system:

- **Monitoring**: Each Sentinel instance periodically PINGs masters and replicas.
- **Subjective down (SDOWN)**: A single Sentinel declares a master unreachable after `down-after-milliseconds`.
- **Objective down (ODOWN)**: `quorum` Sentinels agree the master is down.
- **Failover**: Sentinels elect a leader (Raft-style voting). The leader selects the best replica (by priority, replication offset, and run ID), promotes it to master, and reconfigures all remaining replicas to replicate from the new master.
- Sentinel itself is a special execution mode of `redis-server` (launched via `redis-sentinel` or `redis-server --sentinel`).
- Clients use `SENTINEL get-master-addr-by-name` or Sentinel-aware client libraries to discover the current master.

---

## 8. Redis Cluster

### 8.1 Hash Slot Partitioning

The keyspace is divided into **16,384 hash slots**:

```
slot = CRC16(key) % 16384
```

Hash tags (`{...}`) constrain which part of the key is hashed, enabling co-location of related keys:

```
user:{1000}:profile  →  CRC16("1000") % 16384
user:{1000}:sessions →  CRC16("1000") % 16384  // same slot
```

### 8.2 Consistent Hashing vs. Hash Slots

| Approach | Node Addition | Key Remapping | Implementation |
|----------|--------------|---------------|----------------|
| Consistent Hashing | Rebalances ~K/n keys | Ring-based, virtual nodes | Client-side (or proxy) |
| Hash Slots (Redis) | Rebalances entire slots | Slot-level granularity | Server-side (cluster bus) |

With hash slots, adding a node means migrating entire slots (groups of keys) rather than individual keys. This is implemented via `CLUSTER SETSLOT ... MIGRATING`/`IMPORTING` and `MIGRATE` commands, which atomically transfer keys between nodes.

### 8.3 Cluster Bus

Every cluster node maintains a TCP connection to every other node (full mesh) over the cluster bus (port + 10000). This gossip protocol propagates:
- Node liveness (PING/PONG with gossip sections)
- Slot-to-node assignments
- Configuration epochs
- Failover votes

### 8.4 Client Routing

Clients receive `MOVED` redirects when a key belongs to a different node. Smart clients (like the `-c` flag in redis-cli or client libraries) cache the slot-to-node mapping and redirect transparently. During slot migration, `ASK` redirects tell the client to query the importing node for a specific key followed by `ASKING`.

---

## 9. Redis CLI Reference

```bash
redis-cli [OPTIONS] [cmd [arg ...]]

# Connection
-h <hostname>    Server hostname (default: 127.0.0.1)
-p <port>        Server port (default: 6379)
-s <socket>      Unix socket (overrides hostname and port)
-a <password>    Password (or use REDISCLI_AUTH env var)
-u <uri>         Connection URI
-n <db>          Database number (0–15)

# Mode
-c               Cluster mode (follow -ASK and -MOVED redirects)
-x               Read last argument from STDIN

# Output Formatting
--raw            Raw reply formatting (default when STDOUT is not a TTY)
--csv            CSV output
--no-raw         Force formatted output even in pipes

# Profiling & Monitoring
--stat           Rolling server stats (memory, clients, keys, ops/sec)
--latency        Continuous latency sampling (server round-trip)
--latency-history Track latency over time (default interval 15s)
--latency-dist   Latency histogram (requires 256-color terminal)
--intrinsic-latency <sec>  Measure system (kernel/scheduler) latency floor
--bigkeys        Sample keys to find those with many elements
--memkeys        Sample keys to find those consuming the most memory
--hotkeys        Sample keys for access-frequency hot spots (LFU only)

# Repetition & Timing
-r <repeat>      Execute command N times
-i <interval>    Delay between repeated commands in seconds (0.1 = 100ms)

# Data Transfer
--rdb <file>     Transfer an RDB snapshot from remote server to local file
--pipe           Pipe raw Redis protocol from STDIN to server (bulk loading)
--pipe-timeout <n>  Abort if no reply within <n> seconds in --pipe mode

# Scripting
--eval <file>    Execute a Lua script with key/value arguments
--ldb            Lua debugger mode
--ldb-sync-mode  Synchronous Lua debugger (server blocks, no rollback)

# Cluster Management
--cluster <cmd>  Cluster manager commands (create, add-node, reshard, etc.)
```



## 10. Client Libraries

- **Go**: [go-redis](https://github.com/go-redis/redis) -- type-safe, connection-pooled, cluster-aware
- **Python**: [redis-py](https://github.com/redis/redis-py) -- the reference client with async support
- **Java**: [Jedis](https://github.com/xetorthio/jedis), [Lettuce](https://github.com/lettuce-io/lettuce-core) -- async/reactive with netty
- **Node.js**: [ioredis](https://github.com/luin/ioredis) -- full cluster/Sentinel support
- **C**: [hiredis](https://github.com/redis/hiredis) -- the official C client (also used internally by Redis)

---

## 11. ACL System (Redis 6+)

```
ACL LIST                       -- list all ACL rules
ACL SETUSER <user> ...         -- create/modify a user
ACL DELUSER <user>             -- delete a user
ACL SAVE                       -- persist ACL rules to config
ACL LOAD                       -- reload from config
ACL WHOAMI                     -- show current user
ACL CAT                        -- list command categories

# Example: read-only user with access to a single key pattern
ACL SETUSER reporter on >secretpass ~monitoring:* +@read +@connection -@dangerous
```

Users can be restricted by password, key prefix (`~pattern`), allowed/denied commands (`+@category`, `-command`), and channel patterns for Pub/Sub.

---

## 12. Key Takeaways

- The **single-threaded event loop** is Redis's defining architectural choice: it eliminates locking overhead and guarantees atomicity, but mandates that every command be fast (O(1) or O(log n)).
- **Dual encodings** (memory-efficient small representation, performance-oriented large representation) allow Redis to serve both caching and data-structure use cases without wasting memory.
- **Incremental rehashing** in the dict and the **lazy-free** mechanisms (Redis 4+) keep the event loop responsive during internal maintenance.
- **Persistence** is a spectrum: pure RDB (fast restart, data-loss window), pure AOF (durable, larger/rewrite), or hybrid (best of both).
- **Replication + Sentinel + Cluster** form a layered high-availability stack: replicate for read scaling and durability, Sentinel for automated failover, Cluster for horizontal write scaling.

---

## Source Code

[redis/redis on GitHub](https://github.com/redis/redis)
