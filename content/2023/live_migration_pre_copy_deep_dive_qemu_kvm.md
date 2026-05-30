# Live Migration: Pre-Copy Deep Dive (QEMU/KVM)

> 2023-01-02

A technical walkthrough of the pre-copy live migration flow in QEMU/KVM via libvirt — the migration state machine, memory page tracking with dirty bitmaps, the communication protocol between source and destination hosts, and how the algorithm converges without service interruption.

## Pre-Copy Algorithm Overview

Pre-copy migration transfers a running VM's memory state to a destination host **while the VM continues executing** on the source, minimizing downtime to the final convergence phase:

1. **Initial full transfer** — all RAM pages copied from source to destination while the VM runs
2. **Dirty-page iterations** — pages modified during transfer are re-sent in successive rounds
3. **Convergence** — when the dirty-page rate drops below the available network bandwidth, the VM is briefly paused for the final transfer
4. **Cutover** — remaining dirty pages + CPU/device state are sent, and execution resumes on the destination

```
Source (running)                              Destination (ready)
      │                                               │
      │ ──── Round 1: all RAM pages ──────────────> │
      │ ──── Round 2: dirty pages ────────────────> │
      │ ──── Round 3: fewer dirty pages ──────────> │
      │                    ...                       │
      │ ──── Final: pause VM, send remaining ─────> │
      │                                               │
      ✕ (VM stopped)                          ▶ (VM resumes)
```

## Core Migration Phases

The live migration process follows a well-defined state machine coordinated by libvirt across source and destination QEMU instances.

### High-Level libvirt Flow

1. **Client (compute agent)** connects to the **source** `libvirtd`
2. Client connects to the **destination** `libvirtd`
3. `domainMigrateBegin3` — prepare source (open migration ports, allocate resources)
4. `domainMigratePrepare3` — prepare destination (validate compatibility, start listening)
5. `domainMigratePerform3` — execute the migration, streaming data from source → destination

### QEMU-Level Call Chain

```
qemuDomainMigratePerform3
  → qemuMigrationPerform
    → qemuMigrationPerformPhase
      → doNativeMigrate
        → qemuMigrationRun
          → qemuMonitorSetMigrationSpeed
          → qemuMigrationConnect
          → qemuMonitorMigrateToHost
            → qemuMonitorJSONMigrate
              → qmp_migrate (QEMU QMP command)
```

### Migration Phase Breakdown

| Phase | Source | Destination |
|---|---|---|
| **Setup** | `qmp_migrate` → `tcp_start_outgoing_migration` → `migrate_fd_connect` | `qemu_start_incoming_migration` → `tcp_start_incoming_migration` → `process_incoming_migration_co` |
| **Iterate** | `migration_thread` → `qemu_savevm_state_begin` → `qemu_savevm_state_pending` → `qemu_savevm_state_iterate` | `qemu_loadvm_state` |
| **Complete** | `migration_completion` → `vm_stop` | `cpu_synchronize_all_post_init` → `vm_start` |

## Source-Side Migration Flow

### 1. Connection Establishment

**`tcp_start_outgoing_migration`** — Opens a TCP socket to the destination libvirtd. The socket fd is passed into QEMU userspace.

**`migrate_fd_connect`** — QEMU receives the fd and initializes internal migration state. A new `MigrationIncomingState` is created on the destination side.

### 2. Migration Thread (Main Loop)

The `migration_thread` function drives the entire transfer:

```
migration_thread()
  ├── qemu_savevm_state_header()      // Send migration header (version, capabilities)
  ├── qemu_savevm_state_setup()       // Prepare device state for migration
  └── while (!converged):
       ├── qemu_savevm_state_pending() // Estimate remaining data
       ├── qemu_savevm_state_iterate() // Send one round of dirty pages
       └── check_bandwidth_vs_dirty_rate()
```

The loop terminates when the estimated remaining dirty data + convergence threshold is below the available bandwidth, triggering the final stop-and-copy phase.

### 3. Completion

`migration_completion` pauses the VM (`vm_stop`), sends the final dirty pages and device state, then signals the destination to take over.

## Destination-Side Flow

### 1. Connection Setup

**`qemu_start_incoming_migration`** — Destination QEMU enters migration mode, waiting for an incoming connection.

**`tcp_start_incoming_migration`** — Binds a TCP socket and waits for the source to connect.

### 2. Migration Coroutine

**`process_incoming_migration_co`** — A QEMU coroutine that:
- Reads the migration stream header from the source
- Spawns **decompression threads** via `migrate_decompress_threads_create` for parallel page decompression (when compression is enabled)
- Iterates through incoming pages, decompressing and loading into destination RAM

### 3. State Reconstruction

**`qemu_loadvm_state`** — The main state loader. Processes each section of the incoming stream:
- **RAM sections** — loaded via `ram_load`, populating destination guest memory
- **Device sections** — restored via per-device `load_state` handlers
- **CPU state** — loaded in the final phase before VM start

### 4. Cutover

**`cpu_synchronize_all_post_init`** — Brings destination vCPUs into a consistent state matching the source's final CPU context.

**`vm_start`** — The VM resumes execution on the destination host. The entire cutover window (VM paused → VM resumed) is typically under 100ms for well-tuned workloads.

## KVM Memory Management

Understanding the four address spaces is critical to tracing how migration serializes guest memory.

| Abbreviation | Layer | Meaning |
|---|---|---|
| GVA | Guest VM | Guest Virtual Address — what the guest OS sees |
| GPA | Guest VM | Guest Physical Address — guest's view of physical RAM |
| HVA | Host (QEMU) | Host Virtual Address — QEMU's mmap of guest RAM in userspace |
| HPA | Host (Kernel) | Host Physical Address — actual physical RAM page |

### Key Data Structures

**KVMSlot** — Userspace (QEMU) representation mapping a GPA region to QEMU's host virtual address space:

```c
typedef struct KVMSlot {
    hwaddr      start_addr;   // Guest physical start address
    ram_addr_t  memory_size;  // Size of this memory region
    void       *ram;          // QEMU userspace pointer (HVA)
    int         slot;         // KVM slot ID
    int         flags;
} KVMSlot;
```

**kvm_memory_slot** — Kernel-side descriptor with dirty tracking:

```c
struct kvm_memory_slot {
    gfn_t       base_gfn;         // Guest frame number (GPA >> PAGE_SHIFT)
    unsigned long npages;         // Number of pages in this slot
    unsigned long flags;
    unsigned long *rmap;          // Reverse mapping (GPA → HPA lookups)
    unsigned long *dirty_bitmap;  // Dirty page bitmap for live migration
    struct {
        unsigned long rmap_pde;
        int write_count;
    } *lpage_info[KVM_NR_PAGE_SIZES - 1];
    unsigned long userspace_addr; // QEMU userspace address (HVA)
    int user_alloc;
};
```

### Dirty Page Tracking

The dirty bitmap is the core data structure enabling pre-copy migration:

- **Write protection**: When migration begins, all guest pages are write-protected via EPT (Extended Page Tables)
- **Page fault**: A guest write triggers an EPT violation, KVM marks the page in `dirty_bitmap`, then clears the write protection for subsequent writes
- **Iteration**: QEMU reads `dirty_bitmap` via `KVM_GET_DIRTY_LOG` ioctl after each iteration, transmits the marked pages, then atomically clears the bitmap for the next round
- **Convergence heuristic**: Migration converges when `dirty_rate < max_downtime_allowed * bandwidth` — the remaining dirty data can be transferred within the acceptable pause window

```
Iteration 1: ████████████████  (all pages dirty, full transfer)
Iteration 2: ████░░░░░░░░░░░░  (some pages re-dirtied)
Iteration 3: ██░░░░░░░░░░░░░░  (fewer pages re-dirtied)
Iteration 4: █░░░░░░░░░░░░░░░  (converged — pause and final transfer)
```

## Tuning Parameters

| Parameter | Effect |
|---|---|
| `migrate_set_speed` | Cap bandwidth (in MB/s) to avoid saturating the network link |
| `migrate_set_downtime` | Target max downtime in seconds — lower = more iterations, tighter convergence |
| `xbzrle_cache_size` | XBZRLE (delta compression) cache — reduces transferred data for write-heavy VMs |
| `multifd_channels` | Multi-FD (parallel sockets) — scales migration bandwidth across CPU cores |
| `postcopy_ram` | Enable post-copy mode as fallback after pre-copy iterations |

## References

- QEMU source: `migration/migration.c`, `migration/savevm.c`, `migration/ram.c`
- Linux KVM: `virt/kvm/kvm_main.c` (`KVM_GET_DIRTY_LOG` ioctl)
- libvirt: `src/qemu/qemu_migration.c`, `src/qemu/qemu_migration_params.c`
- [QEMU Migration Documentation](https://wiki.qemu.org/Features/Migration)
