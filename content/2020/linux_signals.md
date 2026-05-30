# Linux Signals

> 2020-04-09

Linux signal handling reference — `man signal` overview and key signal types for process control.

## Common Signals

| Signal | Value | Default Action | Description |
|---|---|---|---|
| `SIGINT` | 2 | Terminate | Interrupt from keyboard (Ctrl+C) |
| `SIGTERM` | 15 | Terminate | Graceful termination request |
| `SIGKILL` | 9 | Terminate (uncatchable) | Force kill |
| `SIGQUIT` | 3 | Core dump | Quit from keyboard (Ctrl+\\) |
| `SIGHUP` | 1 | Terminate | Hangup (terminal closed) |
| `SIGUSR1` | 10 | Terminate | User-defined signal 1 |
| `SIGUSR2` | 12 | Terminate | User-defined signal 2 |
| `SIGCHLD` | 17 | Ignore | Child process stopped or terminated |

## In Practice

Signals are the standard mechanism for process lifecycle management in Linux. Daemons typically handle `SIGTERM` for graceful shutdown and `SIGHUP` for configuration reload.

```c
#include <signal.h>

// Register handler
signal(SIGTERM, handle_shutdown);
signal(SIGHUP, handle_reload);

```
