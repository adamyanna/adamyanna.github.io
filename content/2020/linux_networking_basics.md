# Linux Networking Basics

> 2020-03-18

Core Linux networking concepts — TCP connection lifecycle, socket threading architecture, and IPv4/IPv6 dual-stack binding behavior.

## 1. TIME_WAIT State

A large number of TCP connections lingering in `TIME_WAIT` is common on high-traffic servers. This is the endpoint that initiated the active close waiting for any delayed packets. Tuning via `tcp_tw_reuse` or adjusting the `TIME_WAIT` duration can help, but understand the implications for packet ordering before changing defaults.

## 2. Multi-Threaded Socket Server

To achieve high concurrency, the server must handle client requests in parallel. The standard pattern:

1. `ServerSocket` accepts a connection → creates a new `socket`
2. Spawn a thread, hand the socket to it for processing
3. The main thread returns to `accept()` on the listening port

This keeps the accept loop responsive while worker threads handle I/O independently.

## 3. IPv6 Dual-Stack Behavior on Linux

An IPv6 socket **can** receive IPv4 packets if `IPV6_V6ONLY` is not set. The reverse is never true — an IPv4 socket cannot receive IPv6 traffic.

When binding to the unspecified addresses `0.0.0.0` and `::`, always **bind IPv6 first, then IPv4**. This ensures the IPv6 socket claims the dual-stack binding if `V6ONLY` is disabled, and the IPv4 binding follows as a fallback.
