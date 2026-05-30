# Improving System Performance with ulimit

> 2018-10-22

A practical guide to using `ulimit` for resource constraint management on Linux systems.

## Overview

`ulimit` controls the resources available to processes spawned by the shell. It is a critical tuning knob for production services — especially for database servers, web servers, and any I/O-heavy workload.

## Resource Limits You Can Control

| Resource | Description |
|---|---|
| Core file size | Maximum size of kernel core dumps |
| Data segment size | Process data segment (heap) limit |
| File size | Maximum file size a process can create |
| Locked memory | Maximum memory that can be locked (mlock) |
| Resident set size | Maximum resident memory (RSS) |
| Open file descriptors (`nofile`) | Maximum number of open file descriptors |
| Stack size | Maximum stack segment size |
| CPU time | Maximum CPU time in seconds |
| Max user processes (`nproc`) | Maximum threads/processes per user |
| Virtual memory | Maximum virtual memory per process |

Hard and soft limits: **soft limits** can be raised by the user up to the **hard limit**, which requires root to increase.

## Usage

### Per-Session (Temporary)

Limits apply to the current shell and all child processes spawned from it. Lost on logout.

```bash
ulimit -n 65535       # Raise open file limit
ulimit -u 4096        # Raise max user processes
ulimit -a             # Show all current limits

```

### Persistent Per-User Limits

Edit `/etc/security/limits.conf`:

```

# domain  type  item   value
*         soft  nofile 65535
*         hard  nofile 65535
*         soft  nproc  4096
*         hard  nproc  4096

```

**Fields:**
- `domain`: username, group name (prefixed with `@`), or `*` for all
- `type`: `soft` or `hard`
- `item`: resource name (`nofile`, `nproc`, `cpu`, `stack`, etc.)
- `value`: the limit

### System-Wide Kernel Parameters

Located under `/proc/sys/`:

```bash
/proc/sys/kernel/pid_max           # Max process ID
/proc/sys/net/ipv4/ip_local_port_range  # Ephemeral port range
/proc/sys/fs/file-max              # System-wide max open files

```

Check and tune based on workload requirements. These are runtime parameters and reset on reboot unless persisted via `/etc/sysctl.conf` or `/etc/sysctl.d/`.
