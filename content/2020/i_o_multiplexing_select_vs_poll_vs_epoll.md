# I/O Multiplexing: select vs poll vs epoll

> 2020-04-20

A comparison of the three Linux I/O multiplexing mechanisms — select, poll, and epoll — focusing on the architectural differences that make epoll the default choice for high-concurrency servers.

## Core Difference

**select / poll:** The kernel scans **all** monitored file descriptors every time the process calls into `select()` or `poll()`. This is a linear scan — O(n) per invocation.

**epoll:** The process registers file descriptors once via `epoll_ctl()`. When an FD becomes ready, the kernel triggers a **callback** mechanism that immediately activates it. When the process calls `epoll_wait()`, it's notified directly — no scan of inactive descriptors. This is epoll's defining advantage.

## Why epoll Wins

### 1. No FD Limit

`select()` imposes a hard limit on the number of file descriptors a process can monitor (`FD_SETSIZE`, typically 1024). For servers with many concurrent connections, this is a dealbreaker. While a multi-process approach (à la Apache) can work around it, process creation on Linux is not free, and inter-process data synchronization is far less efficient than thread-level synchronization.

`epoll` has no such limit — the ceiling is the system's maximum open files, which on a 1 GB RAM machine is roughly 100,000 (check via `cat /proc/sys/fs/file-max`).

### 2. O(1) Ready-FD Detection

`epoll`'s performance does not degrade as the number of monitored FDs grows. Because it uses per-FD callbacks rather than polling, **only ready FDs trigger notification**. `select` and `poll` must iterate the entire FD set regardless of how many are active.

### 3. The Idle Connection Killer

If you have few idle or dead connections, `epoll`'s advantage over `select`/`poll` is modest. But when a server holds **thousands of mostly-idle connections** (the typical long-poll / WebSocket / connection-pooling scenario), `epoll` dramatically outperforms the alternatives.

## Summary

| | select | poll | epoll |
|---|---|---|---|
| FD limit | Fixed (1024) | No fixed limit | No fixed limit (system file max) |
| Scan strategy | Linear scan all FDs | Linear scan all FDs | Callback — only ready FDs |
| Performance vs FD count | Degrades linearly | Degrades linearly | Near-constant |
| Registration model | Per-call | Per-call | Once via `epoll_ctl()` |
