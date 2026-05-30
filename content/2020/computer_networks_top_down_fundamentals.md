# Computer Networks: Top-Down Fundamentals

> 2020-03-16

A comprehensive review of _Computer Networking: A Top-Down Approach_ -- covering the OSI model, all five layers in depth, routing algorithms, TCP internals, network security, and I/O multiplexing.

---

## 1. Network Architecture Models

### OSI Seven-Layer Model

```
Application -> Presentation -> Session -> Transport -> Network -> Data Link -> Physical
```

### TCP/IP Five-Layer (Simplified) Model

```
Application -> Transport -> Network -> Link -> Physical
```

In practice the five-layer model is the workhorse of the Internet. Each layer provides services to the layer above and uses services from the layer below. The key insight: **routers and link-layer switches implement only the lower layers**, while end systems implement all five. This pushes complexity to the network edge.

| Layer | PDU Name | Protocols / Examples |
|-------|----------|---------------------|
| Application | Message | HTTP, DNS, SMTP, FTP |
| Transport | Segment (TCP) / Datagram (UDP) | TCP, UDP |
| Network | Datagram | IP, ICMP, OSPF, BGP |
| Link | Frame | Ethernet, Wi-Fi, PPP |
| Physical | Bit | Copper, fiber, radio |

### Encapsulation

```
Application-layer Message
  + Transport-layer Header = Segment
    + Network-layer Header = Datagram
      + Link-layer Header + Link-layer Trailer = Frame
```

Each layer adds its own header. The payload of a lower-layer frame is the upper-layer PDU. This wrapping process is called **encapsulation**.

---

## 2. Physical Layer Basics

### What the Physical Layer Does

The physical layer moves **individual bits** from one node to the next across a physical medium. It defines electrical, mechanical, and procedural interfaces.

### Media Types

| Type | Medium | Characteristics |
|------|--------|----------------|
| Twisted-Pair Copper | Guided | Cat 5e/6, up to 10 Gbps, used in Ethernet LANs |
| Coaxial Cable | Guided | Shared medium, used in cable Internet (DOCSIS) |
| Fiber Optic | Guided | Light pulses, up to 100+ Gbps, low error rate, long distance |
| Terrestrial Radio | Unguided | Wireless LAN (Wi-Fi), cellular, satellite |
| Satellite | Unguided | Geostationary (GEO) vs. Low-Earth Orbit (LEO) |

### Key Concepts

- **Bandwidth** (computing): maximum data transfer rate in bps
- **Bandwidth** (signal processing): range of frequencies in Hz
- **Propagation delay**: time for a bit to travel the physical distance (distance / propagation speed)
- **Transmission delay**: time to push all bits onto the link (packet length / link rate)

---

## 3. Application Layer

### 3.1 Principles of Network Applications

#### Application Architectures

- **Client-Server**: always-on server with fixed IP; clients communicate only with the server (e.g., Web, FTP)
- **P2P (Peer-to-Peer)**: direct communication between hosts; self-scaling property (e.g., BitTorrent)

#### Process Communication

Processes on different end systems communicate by exchanging **messages** across the network. A process sends/receives through a **socket** -- the software interface to the transport layer. The socket is the API between application and transport layer; the developer chooses:

1. Transport protocol (TCP or UDP)
2. Transport-layer parameters (buffer sizes, max segment size)

A process is addressed by `(IP address, port number)`.

#### Transport Services Required by Applications

| Requirement | Description |
|-------------|-------------|
| Reliable data transfer | No data loss, guaranteed delivery |
| Throughput | Minimum guaranteed rate (bandwidth-sensitive apps) |
| Timing | End-to-end delay bounds |
| Security | Encryption, authentication |

TCP provides reliability but no timing/throughput guarantees. UDP provides none of the above but is faster.

---

### 3.2 HTTP -- Hypertext Transfer Protocol

HTTP is the Web's application-layer protocol, defined in RFCs. It runs over TCP, uses port 80 (443 for HTTPS), and is **stateless** -- the server maintains no information about past client requests.

#### HTTP Request Message Format

```
METHOD  URL  HTTP/1.1\r\n
Host: www.example.com\r\n
Connection: keep-alive\r\n
User-Agent: Mozilla/5.0\r\n
Accept: text/html\r\n
\r\n
[Entity Body]
```

**Methods**: GET, POST, HEAD, PUT, DELETE, OPTIONS

#### HTTP Response Message Format

```
HTTP/1.1  200  OK\r\n
Date: Mon, 16 Mar 2020 10:00:00 GMT\r\n
Server: Apache/2.4\r\n
Last-Modified: Sun, 15 Mar 2020 09:00:00 GMT\r\n
Content-Length: 1234\r\n
Content-Type: text/html\r\n
\r\n
[Entity Body]
```

#### Common Status Codes

| Code | Phrase | Meaning |
|------|--------|---------|
| 200 | OK | Request succeeded |
| 301 | Moved Permanently | Resource relocated |
| 304 | Not Modified | Conditional GET, use cached copy |
| 400 | Bad Request | Malformed request |
| 404 | Not Found | Resource does not exist |
| 505 | HTTP Version Not Supported | |

#### Persistent vs. Non-Persistent Connections

- **Non-persistent (HTTP/1.0)**: each request/response uses a separate TCP connection; each object incurs 2 RTTs
- **Persistent (HTTP/1.1 default)**: multiple requests multiplexed on a single TCP connection; pipelining allows sending requests back-to-back without waiting

#### Cookies

HTTP is stateless, but cookies enable user tracking. Mechanism:
1. Server sends `Set-Cookie` header in response
2. Client stores cookie and includes it in future requests via `Cookie` header
3. Backend database ties the cookie identifier to user state

#### Web Caching (Proxy Server)

A **Web cache** (proxy server) sits between client and origin server. It satisfies HTTP requests from its local storage when possible, reducing response time and traffic load. Caches use **conditional GET** with `If-Modified-Since` header to validate freshness.

**CDN (Content Delivery Network)**: geographically distributed caches that localize traffic.

---

### 3.3 DNS -- Domain Name System

DNS maps hostnames to IP addresses. It is:
- A **distributed, hierarchical database**
- An application-layer protocol running over **UDP** on port **53**

#### DNS Hierarchy

```
Root DNS Servers
  -> Top-Level Domain (TLD) Servers (.com, .org, .net, country codes)
    -> Authoritative DNS Servers (organization-specific, e.g., amazon.com)
```

#### Query Types

- **Iterative query**: client queries server, server returns referral to another server
- **Recursive query**: client offloads resolution work to a single server

#### Resource Record Format

```
(Name, Value, Type, TTL)
```

| Type | Name | Value |
|------|------|-------|
| A | Hostname | IPv4 address |
| AAAA | Hostname | IPv6 address |
| NS | Domain | Authoritative name server hostname |
| CNAME | Alias | Canonical hostname |
| MX | Mail domain | Mail server hostname |

DNS also enables **load distribution** -- a set of IP addresses is rotated across responses.

---

### 3.4 SMTP -- Simple Mail Transfer Protocol

SMTP transfers mail from sender's mail server to recipient's mail server over TCP port **25**. Mail access protocols (POP3, IMAP) retrieve mail from the server.

SMTP vs HTTP:
- SMTP is a **push** protocol; HTTP is primarily **pull**
- SMTP requires messages in 7-bit ASCII; HTTP has no such restriction
- SMTP places all objects in a single message; HTTP encapsulates each object separately

---

### 3.5 FTP -- File Transfer Protocol

FTP uses **two parallel TCP connections**:
- **Control connection** (port 21): for commands, authentication, directory navigation
- **Data connection** (port 20): for actual file transfer

FTP is **stateful** (server tracks user session state -- current directory, authentication), while HTTP is **stateless**. FTP control information is sent **out-of-band**; HTTP headers are **in-band**.

---

### 3.6 Socket Programming

#### UDP Socket (Connectionless)

```python
# Python example
from socket import *
server = socket(AF_INET, SOCK_DGRAM)
server.bind(('', 12000))
message, client_addr = server.recvfrom(2048)
server.sendto(response.encode(), client_addr)
```

A UDP socket is identified by `(dest_IP, dest_port)`. All segments from different sources with the same destination arrive at the same socket.

#### TCP Socket (Connection-Oriented)

```python
from socket import *
server = socket(AF_INET, SOCK_STREAM)
server.bind(('', 12000))
server.listen(1)
conn_socket, addr = server.accept()  # new socket for this client
data = conn_socket.recv(1024)
conn_socket.send(response.encode())
conn_socket.close()
```

A TCP socket is identified by a **4-tuple**: `(src_IP, src_port, dest_IP, dest_port)`. The server uses a **welcome socket** for initial contact; each accepted connection gets its own **connection socket**.

---

## 4. Transport Layer

### 4.1 Transport-Layer Services

The transport layer provides **logical communication between processes** running on different hosts. The network layer provides host-to-host communication; the transport layer extends this to **process-to-process** communication.

Key functions:
- **Multiplexing/demultiplexing**: using port numbers to deliver segments to the correct socket
- **Error detection**: checksums
- **Reliable data transfer** (TCP): sequence numbers, ACKs, timer-based retransmission

IP's service model is **best-effort delivery** -- unreliable. TCP builds reliable data transfer **on top of** IP.

---

### 4.2 Multiplexing and Demultiplexing

Each transport-layer segment carries `(source_port, dest_port)`. The receiving transport layer uses the destination port to deliver the segment to the correct socket.

**UDP demultiplexing**: uses `(dest_IP, dest_port)` -- a 2-tuple

**TCP demultiplexing**: uses `(src_IP, src_port, dest_IP, dest_port)` -- a 4-tuple. Different source addresses/ports arrive at different sockets, enabling concurrent connections.

---

### 4.3 UDP -- User Datagram Protocol

UDP is a **lightweight**, **connectionless** transport protocol providing:
- Multiplexing/demultiplexing
- Checksum-based error detection (but no error recovery)

#### UDP Segment Structure

```
 0      7 8     15 16    23 24    31
+--------+--------+--------+--------+
|   Source Port   | Destination Port |
+--------+--------+--------+--------+
|    Length       |     Checksum     |
+--------+--------+--------+--------+
|              Data                  |
+------------------------------------+
```

Each field is 16 bits. The checksum is the 1's complement of the 1's complement sum of all 16-bit words (with overflow wraparound). A receiver computes the sum including the checksum; the result should be all 1s if error-free.

**Why use UDP?**
1. No connection establishment delay (no handshake)
2. No connection state at sender/receiver
3. Small header overhead (8 bytes vs. TCP's 20+ bytes)
4. No congestion control -- sender can pump data at any rate

Applications: DNS, SNMP, streaming media, real-time voice/video, RIP

The **end-to-end principle** justifies UDP's minimalism: functions that must be implemented end-to-end anyway should not be duplicated in lower layers.

---

### 4.4 Principles of Reliable Data Transfer

Building reliable delivery over an unreliable channel via:
- **Checksum**: detect bit errors
- **Sequence numbers**: identify segments, detect duplicates
- **ACKs / NAKs**: receiver feedback
- **Timers**: retransmit on timeout
- **Pipelining**: multiple in-flight segments

#### Evolution of RDT Protocols

**rdt1.0**: perfect channel -- nothing needed

**rdt2.0**: bit errors possible -- ACK/NAK + checksum. Stop-and-wait.

**rdt2.1/2.2**: handle corrupted ACK/NAK -- add sequence numbers

**rdt3.0**: bit errors + loss -- add timeout-based retransmission. Still stop-and-wait; utilization = (L/R) / (RTT + L/R), which is terrible over long RTT.

#### Pipelined Protocols

Allow multiple unacknowledged segments in flight.

**Go-Back-N (GBN)**:
- Sender: window of up to N consecutive unacknowledged segments
- Cumulative ACK: ACK(n) acknowledges all segments up to and including n
- Single timer for oldest unacked segment
- On timeout: retransmit ALL unacked segments in window
- Receiver: discards out-of-order segments (no buffering), sends ACK for last in-order

```
Sender window:
 [0][1][2][3][4][5][6][7]...
  ^base           ^nextseqnum
  <--- N=4 ------->
  (sent, unacked) (usable, unsent)
```

**Selective Repeat (SR)**:
- Each unacked segment has its own logical timer
- Individual ACKs for each correctly received segment
- Sender retransmits only lost segments
- Receiver buffers out-of-order segments
- Window size must be <= half the sequence number space to avoid ambiguity

#### RDT Mechanisms Summary

| Mechanism | Purpose |
|-----------|---------|
| Checksum | Detect bit-level corruption |
| Timer | Detect segment loss (timeout -> retransmit) |
| Sequence number | Order data, detect duplicates |
| ACK | Positive feedback from receiver |
| NAK | Negative feedback (explicit, or 3 duplicate ACKs) |
| Window / Pipelining | Improve utilization |

---

### 4.5 TCP In Depth

#### TCP Connection

- **Point-to-point**: single sender, single receiver
- **Full-duplex**: data flows bidirectionally on one connection
- **Three-way handshake** establishes the connection (see TCP State Machine below)
- Data is buffered in **send buffer** and **receive buffer**; TCP extracts data in chunks up to **MSS** (Maximum Segment Size), typically 1460 bytes (1500 MTU - 20 IP header - 20 TCP header)

#### TCP Segment Structure

```
 0          3 4          7 8                   15 16                  31
+------------+------------+---------------------+----------------------+
|        Source Port       |       Destination Port                     |
+--------------------------+--------------------------------------------+
|                          Sequence Number                              |
+----------------------------------------------------------------------+
|                        Acknowledgment Number                          |
+------------+------------+---+---+---+---+---+---+-------------------+
| Hdr Len|Rsv| U| A| P| R| S| F|          Receive Window               |
|        |   | R| C| S| S| Y| I|                                        |
|        |   | G| K| H| T| N| N|                                        |
+------------+------------+---+---+---+---+---+---+-------------------+
|       Checksum            |       Urgent Data Pointer                 |
+---------------------------+-------------------------------------------+
|                          Options (variable)                           |
+----------------------------------------------------------------------+
|                          Data                                         |
+----------------------------------------------------------------------+
```

Key fields:
- **Sequence number**: byte-stream offset of first data byte in this segment
- **Acknowledgment number**: next expected byte from the other side (cumulative ACK)
- **Receive window** (16 bits): available buffer space for flow control
- **Flags**: URG, ACK, PSH, RST, SYN, FIN -- each 1 bit
- **Header length** (4 bits): in 32-bit words, typically 5 (20 bytes)

#### Sequence Numbers and Cumulative ACK

TCP numbers each byte in the data stream. The sequence number of a segment is the byte-stream number of its first byte. The ACK number is the **next byte expected** by the receiver. TCP uses **cumulative acknowledgment** -- ACK(n) means all bytes up to n-1 have been received.

Out-of-order segments: TCP receivers typically buffer them rather than discard.

---

### 4.6 Round-Trip Time Estimation and Timeout

TCP maintains **EstimatedRTT** and **DevRTT**:

```
EstimatedRTT = (1 - alpha) * EstimatedRTT + alpha * SampleRTT    (alpha = 0.125)
DevRTT       = (1 - beta)  * DevRTT       + beta * |SampleRTT - EstimatedRTT|  (beta = 0.25)
TimeoutInterval = EstimatedRTT + 4 * DevRTT
```

Initial TimeoutInterval is 1 second. On timeout, the interval is **doubled** (exponential backoff) until a fresh ACK arrives, providing implicit congestion control.

---

### 4.7 Reliable Data Transfer in TCP

**Events at the sender**:
1. Data received from application -> encapsulate, send, start timer if not running
2. ACK received -> update `SendBase` (oldest unacked byte), restart timer for unacked data
3. Timeout -> retransmit the segment with smallest sequence number among unacked segments, double timeout interval

**Fast retransmit**: if sender receives **3 duplicate ACKs** for the same segment, it retransmits the missing segment **before** the timer expires. Three duplicate ACKs serve as an implicit NAK.

**Duplicate ACK generation at receiver**:
- Out-of-order segment arrives -> immediately send duplicate ACK for last in-order byte
- Gap filled -> send cumulative ACK covering up to highest contiguous byte

---

### 4.8 Flow Control

Flow control prevents the sender from overflowing the receiver's buffer.

```
RcvBuffer: configured receive buffer size
LastByteRcvd: last byte placed in buffer (in-order)
LastByteRead: last byte read by application

rwnd = RcvBuffer - (LastByteRcvd - LastByteRead)
```

The receiver advertises `rwnd` in the TCP header's **Receive Window** field.

Sender constraint: `LastByteSent - LastByteAcked <= rwnd`

When `rwnd = 0`, the sender periodically sends 1-byte probe segments to detect when the window reopens.

UDP has **no flow control** -- data can overflow the receive buffer.

---

### 4.9 TCP Connection Management and State Machine

#### Three-Way Handshake (Connection Establishment)

```
Client                              Server
  |                                   |
  |--- SYN, seq=client_isn ---------->|   Step 1: Client sends SYN
  |                                   |
  |<-- SYNACK, seq=server_isn,       |   Step 2: Server allocates buffers,
  |    ack=client_isn+1 --------------|           responds with SYNACK
  |                                   |
  |--- ACK, seq=client_isn+1,        |   Step 3: Client allocates buffers,
  |    ack=server_isn+1 (may carry data) ->     sends ACK (may include data)
  |                                   |
  |<======== Connection ESTABLISHED =======>|
```

#### Four-Way Teardown (Connection Termination)

```
Client                              Server
  |                                   |
  |--- FIN, seq=x -------------------->|   Step 1: Client initiates close
  |                                   |
  |<-- ACK, ack=x+1 -----------------|   Step 2: Server acknowledges FIN
  |                                   |
  |<-- FIN, seq=y -------------------|   Step 3: Server sends its FIN
  |                                   |
  |--- ACK, ack=y+1 ----------------->|   Step 4: Client acknowledges
  |                                   |
  |(TIME_WAIT: 2 MSL = ~60s)         |(CLOSED)
```

#### TCP State Machine Diagram

```
                              CLIENT                                    SERVER

                         +-----------+                            +-----------+
                         |  CLOSED   |                            |  CLOSED   |
                         +-----+-----+                            +-----+-----+
                               |                                         |
                        app: connect                      passive open: listen()
                        send SYN                             |              |
                               |                             v              |
                         +-----v------+                 +----+------+       |
                         |  SYN_SENT  |                 |  LISTEN   |       |
                         +-----+------+                 +----+------+       |
                               |                              |              |
                    recv SYN+ACK, send ACK           recv SYN, send SYN+ACK |
                               |                              |              |
                         +-----v------+                 +----v-------+      |
                         | ESTABLISHED|                 | SYN_RCVD   |      |
                         +--+------+--+                 +---------+--+      |
                            |      |                               |         |
              app: close    |      |  recv SYN+ACK, send ACK       |         |
              send FIN      |      +-------------------------------+         |
                            |                                                |
                    +-------v--------+                           recv ACK    |
                    |  FIN_WAIT_1    |                               |       |
                    +-------+--------+                               |       |
                            |                                        |       |
                     recv ACK                               +--------v-------+
                            |                               |  ESTABLISHED   |
                    +-------v--------+                      +--+----+----+---+
                    |  FIN_WAIT_2    |                         |    |    |
                    +-------+--------+            recv FIN     |    |    |
                            |                  send ACK        |    |    |
                     recv FIN                           +------v-+  |    |
                     send ACK                          |CLOSE_WAIT|  |    |
                            |                          +------+---+  |    |
                    +-------v--------+                        |       |    |
                    |   TIME_WAIT    |               app: close|       |    |
                    |  (2 MSL wait)  |               send FIN  |       |    |
                    +-------+--------+                        |       |    |
                            |                          +------v----+  |    |
                     timeout (2 MSL)                   | LAST_ACK  |  |    |
                            |                          +------+----+  |    |
                    +-------v--------+                        |       |    |
                    |    CLOSED      |                 recv ACK       |    |
                    +----------------+                        |       |    |
                                                      +-------v-------+   |
                                                      |    CLOSED     |<--+
                                                      +---------------+
```

**TIME_WAIT** (2 MSL, typically 60s) serves two purposes:
1. Ensure the last ACK is delivered; if lost, the server's FIN retransmission can be re-ACKed
2. Allow old duplicate segments from this connection to expire in the network before the same 4-tuple is reused

#### SYN Flood Attack and SYN Cookies

**SYN flood**: attacker sends many SYN segments without completing handshakes, exhausting server's half-open connection resources.

**SYN cookie defense**: server does NOT allocate resources on SYN. Instead, it computes a cryptographic hash of (src_IP, src_port, timestamp, secret) as the initial sequence number. When the ACK returns, the server verifies the hash. If valid, resources are allocated; if not, the SYN was spoofed and no resources were wasted.

---

### 4.10 Congestion Control

#### Causes and Costs of Congestion

When aggregate arrival rate nears link capacity:
1. **Large queuing delays** -- latency spikes
2. **Packet loss** -- buffers overflow, requiring retransmission
3. **Wasted upstream capacity** -- packets dropped downstream wasted prior forwarding effort
4. **Unnecessary retransmissions** -- due to large delays triggering spurious timeouts

#### TCP Congestion Control: AIMD

TCP uses **end-to-end** congestion control (no network assistance). The core principle is **Additive Increase, Multiplicative Decrease (AIMD)**:

- **Additive Increase**: per RTT, cwnd += 1 MSS (probe for bandwidth)
- **Multiplicative Decrease**: on loss event, cwnd = cwnd / 2 (back off)

The sending rate is constrained by:

```
LastByteSent - LastByteAcked <= min(cwnd, rwnd)
```

TCP infers congestion from loss events (timeout or 3 duplicate ACKs).

#### Three Phases of TCP Congestion Control

```
cwnd
 ^
 |     Slow Start          Congestion           Fast Recovery
 |     (exponential)        Avoidance          (after 3 dup ACKs)
 |        .                (linear +1 MSS/RTT)
 |       .|               ./
 |      . |             ./
 |     .  |           ./
 |    .   |         ./
 |   .    |  ssthresh---------------------+
 |  .     | .                             |
 | .      |.                              |
 |.       |                               |
 +----------------------------------------+-------> time
         |                               |
     timeout -> cwnd=1           3 dup ACKs -> cwnd/=2
     enter slow start            enter fast recovery
```

**Slow Start**:
- cwnd starts at 1 MSS
- Every ACK received: cwnd += 1 MSS -> doubles per RTT (exponential)
- Stops when cwnd >= ssthresh (slow start threshold), transitions to congestion avoidance
- On timeout: ssthresh = cwnd / 2, cwnd = 1 MSS, restart slow start

**Congestion Avoidance**:
- Per RTT: cwnd += 1 MSS (linear increase)
- Example: if cwnd = 10 MSS, each ACK adds 1/10 MSS; after all 10 ACKs, cwnd = 11 MSS
- On timeout: ssthresh = cwnd / 2, cwnd = 1 MSS, go to slow start
- On 3 duplicate ACKs: cwnd = cwnd / 2 + 3 MSS, ssthresh = cwnd / 2, go to fast recovery

**Fast Recovery** (TCP Reno):
- On each subsequent duplicate ACK: cwnd += 1 MSS
- When ACK arrives for the missing segment: cwnd = ssthresh (the value when fast recovery began), go to congestion avoidance
- On timeout: same as above (go to slow start)

#### TCP Throughput (Macroscopic)

Average throughput of a TCP connection: approximately `0.75 * W / RTT`, where W is the window size when loss occurs.

#### Fairness

UDP lacks congestion control -- it can starve TCP connections. Multiple parallel TCP connections grab a disproportionate share of bandwidth.

---

### 4.11 I/O Multiplexing: select, poll, epoll

Servers must monitor many sockets simultaneously. Three UNIX/Linux mechanisms:

#### select()

```c
int select(int nfds, fd_set *readfds, fd_set *writefds,
           fd_set *exceptfds, struct timeval *timeout);
```

- Monitors file descriptors for readability, writability, exceptions
- Modifies fd_sets in place (must reinitialize on each call)
- **Limitation**: max fd is `FD_SETSIZE` (typically 1024)
- O(n) complexity: kernel must scan all descriptors up to `nfds`

```c
fd_set readfds;
FD_ZERO(&readfds);
FD_SET(sockfd, &readfds);
select(sockfd + 1, &readfds, NULL, NULL, NULL);
if (FD_ISSET(sockfd, &readfds)) { /* ready to read */ }
```

#### poll()

```c
int poll(struct pollfd *fds, nfds_t nfds, int timeout);

struct pollfd {
    int   fd;         // file descriptor
    short events;     // requested events (POLLIN, POLLOUT, etc.)
    short revents;    // returned events
};
```

- Uses array of `pollfd` structs instead of bitmasks -> no `FD_SETSIZE` limit
- O(n) complexity: kernel scans entire array
- Cleaner API than select (separate input/output event fields)

```c
struct pollfd fds[2];
fds[0].fd = listen_fd;
fds[0].events = POLLIN;
poll(fds, 2, -1);
if (fds[0].revents & POLLIN) { /* new connection */ }
```

#### epoll (Linux)

```c
int epoll_create1(int flags);
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);
int epoll_wait(int epfd, struct epoll_event *events, int maxevents, int timeout);
```

- **Stateful**: descriptors registered once with `epoll_ctl`; kernel tracks interest list
- O(1) per ready descriptor: kernel places ready fds directly in the return array
- **Edge-triggered** (EPOLLET) and **level-triggered** modes
- Scales to tens of thousands of concurrent connections

```c
int epfd = epoll_create1(0);
struct epoll_event ev;
ev.events = EPOLLIN;   // level-triggered by default
ev.data.fd = listen_fd;
epoll_ctl(epfd, EPOLL_CTL_ADD, listen_fd, &ev);

struct epoll_event events[MAX_EVENTS];
int n = epoll_wait(epfd, events, MAX_EVENTS, -1);
for (int i = 0; i < n; i++) {
    if (events[i].data.fd == listen_fd) { /* accept new connection */ }
    else { /* handle data */ }
}
```

#### Comparison

| Feature | select | poll | epoll |
|---------|--------|------|-------|
| API complexity | Medium | Simple | Moderate |
| Max descriptors | FD_SETSIZE (~1024) | No hard limit | No hard limit |
| Performance | O(n) | O(n) | O(1) per ready fd |
| State | Stateless | Stateless | Stateful (kernel-maintained) |
| Trigger mode | Level | Level | Level + Edge |
| Descriptor copy | Full set each call | Full array each call | Once on registration |
| Best for | Legacy code | Portable, <1000 fds | High concurrency (>1000 fds) |

**Rule of thumb**: Use `poll` for portable code with moderate concurrency. Use `epoll` (Linux) / `kqueue` (BSD/macOS) for high-performance servers handling thousands of connections.

---

## 5. Network Layer

### 5.1 Forwarding and Routing

- **Forwarding**: moving a packet from an input link interface to the appropriate output link interface (data plane, implemented in hardware)
- **Routing**: determining the end-to-end path (control plane, implemented in software via routing algorithms)

Each router has a **forwarding table**. On packet arrival, the router checks the header field, looks up the output interface, and forwards the packet. The forwarding table is populated by the routing algorithm.

### 5.2 Network Service Models

| Service | Internet (Best-Effort) | ATM CBR | ATM ABR |
|---------|----------------------|---------|---------|
| Guaranteed delivery | No | Yes | Yes |
| Bounded delay | No | Yes | No |
| In-order delivery | No | Yes | Yes |
| Guaranteed min bandwidth | No | Yes (constant) | Yes (MCR) |
| Security | No (IPsec optional) | No | No |

The Internet provides only **best-effort service**.

### 5.3 Virtual Circuit vs. Datagram Networks

**Virtual Circuit (VC) Networks** (ATM, Frame Relay):
- Connection setup before data transfer (3 phases: setup, transfer, teardown)
- Each packet carries a VC number, not a full destination address
- Routers maintain per-connection state
- VC numbers change per-link (routers rewrite them)

**Datagram Networks** (Internet):
- No connection setup; each packet carries full destination address
- Routers have no per-connection state
- Forwarding based on destination address prefix match (longest prefix matching)

---

### 5.4 IPv4 Datagram Format

```
 0      3 4      7 8             15 16                            31
+------+------+------+-------------+-------------------------------+
|Vers  |HdrLen|TOS   |        Total Length (bytes)                 |
+------+------+------+-------------+-------------------------------+
|    Identification            |Flags|       Fragment Offset       |
+------------------------------+-----+-----------------------------+
|    TTL       |   Protocol    |      Header Checksum              |
+--------------+---------------+-----------------------------------+
|                        Source IP Address                         |
+-----------------------------------------------------------------+
|                     Destination IP Address                       |
+-----------------------------------------------------------------+
|                    Options (if any)                              |
+-----------------------------------------------------------------+
|                    Data (payload)                                |
+-----------------------------------------------------------------+
```

Key fields:
- **Version**: 4 for IPv4
- **Header Length**: in 32-bit words (typically 5 = 20 bytes)
- **Total Length**: header + data, max 65535
- **TTL** (Time-To-Live): decremented at each router; datagram discarded when TTL=0
- **Protocol**: 6 = TCP, 17 = UDP (the "glue" binding network to transport layer)
- **Header Checksum**: 1's complement sum of 16-bit header words, recomputed at each router (since TTL changes)

#### IP Fragmentation

Different link-layer protocols have different **MTU** (Maximum Transmission Unit) values (e.g., Ethernet: 1500 bytes, some WAN links: 576 bytes). When a datagram exceeds the outgoing link's MTU, it must be **fragmented**.

Each fragment:
- Carries the same **Identification** number
- Has **Fragment Offset** indicating its byte position within the original datagram
- Has the **Flag** bit: 1 for all fragments except the last

Reassembly occurs only at the destination host. If any fragment is lost, the entire datagram is discarded (TCP retransmits).

---

### 5.5 IPv4 Addressing

- 32-bit address, written in **dotted-decimal** notation: `192.168.1.1`
- An IP address is associated with a network **interface**, not a host
- **Subnet**: a set of interfaces that can communicate without passing through a router
- **CIDR** (Classless Interdomain Routing): `a.b.c.d/x`, where `x` prefix bits form the network portion
- **Subnet mask**: `/24` means the first 24 bits define the subnet

#### Address Aggregation

Using CIDR, a single prefix advertisement can cover multiple subnets -- reducing forwarding table size. This is called **route aggregation** or **route summarization**.

#### DHCP (Dynamic Host Configuration Protocol)

A **plug-and-play** protocol allowing hosts to obtain an IP address automatically. DHCP is a client-server protocol running over UDP (ports 67, 68).

**Four-step process**:
1. **DHCP Discover**: client broadcasts `255.255.255.255` from `0.0.0.0`
2. **DHCP Offer**: server responds with proposed IP, subnet mask, lease time
3. **DHCP Request**: client selects one offer and requests it
4. **DHCP ACK**: server confirms the assignment

DHCP also provides: default gateway (first-hop router), DNS server address, subnet mask.

#### NAT (Network Address Translation)

NAT-enabled routers hide an entire private network behind a single public IP. The router maintains a **NAT translation table**:

| WAN-side | LAN-side |
|----------|----------|
| `public_IP:port` | `private_IP:port` |

Outgoing: router rewrites source IP/port to its own public IP/port, records mapping.
Incoming: router uses destination port to look up the internal host and rewrites destination IP/port.

NAT supports up to ~60,000 simultaneous connections per public IP. However, it breaks the end-to-end principle and complicates P2P applications (requiring **NAT traversal** techniques or UPnP).

---

### 5.6 ICMP (Internet Control Message Protocol)

ICMP is used by hosts and routers to communicate network-layer information (error reporting, diagnostics). ICMP messages are carried as IP payload (protocol number 1).

Common ICMP types:

| Type | Code | Description |
|------|------|-------------|
| 0 | 0 | Echo Reply (ping response) |
| 3 | 0 | Destination Network Unreachable |
| 3 | 3 | Destination Port Unreachable |
| 4 | 0 | Source Quench (deprecated congestion control) |
| 8 | 0 | Echo Request (ping) |
| 11 | 0 | TTL Expired (traceroute) |

**ping**: sends ICMP Type 8 (Echo Request); receiver replies Type 0 (Echo Reply).

**traceroute**: sends UDP segments with incrementing TTL values. Each router that drops a segment (TTL=0) returns ICMP Type 11. The destination returns ICMP Type 3 Code 3 (Port Unreachable) since the UDP port is deliberately unused.

---

### 5.7 IPv6

IPv6 addresses the IPv4 address exhaustion problem and simplifies header processing.

```
 0      3 4           11 12          15 16          23 24           31
+------+---------------+---------------+-------------------------------+
|Vers  | Traffic Class |        Flow Label                              |
+------+---------------+---------------+-------------------------------+
|  Payload Length               |  Next Header    |  Hop Limit         |
+-------------------------------+---------------+-----------------------+
|                                                                       |
+                     Source Address (128 bits)                         +
|                                                                       |
+-----------------------------------------------------------------------+
|                                                                       |
+                   Destination Address (128 bits)                      +
|                                                                       |
+-----------------------------------------------------------------------+
|                    Data                                                |
+-----------------------------------------------------------------------+
```

Key differences from IPv4:
- **128-bit addresses** (vs. 32-bit)
- **Fixed 40-byte header** (no options field -- faster router processing)
- **No fragmentation at routers** -- routers drop oversized packets and send ICMP "Packet Too Big"
- **No header checksum** (redundant with transport-layer checksum; faster per-hop processing)
- **Flow label**: identify packets belonging to a flow needing special treatment (e.g., real-time)

**IPv4-to-IPv6 transition**:
- **Dual-stack**: nodes run both IPv4 and IPv6
- **Tunneling**: IPv6 datagram is carried as payload inside an IPv4 datagram across an IPv4-only region

---

### 5.8 Routing Algorithms

#### Classification

| Dimension | Types |
|-----------|-------|
| Information scope | **Global** (Link-State) vs. **Decentralized** (Distance-Vector) |
| Dynamics | **Static** vs. **Dynamic** |
| Load sensitivity | **Load-sensitive** vs. **Load-insensitive** |

#### Link-State (LS) Algorithm -- Dijkstra

Every node knows the complete network topology (via **link-state broadcast**). Each node runs Dijkstra's algorithm independently to compute shortest paths to all destinations.

```
// Dijkstra's algorithm
N' = {u}                    // set of nodes with known shortest path
for all nodes v:
    D(v) = c(u,v)           // cost from source u to v

while N' != N:
    find w not in N' with minimum D(w)
    N' = N' U {w}
    for all v neighbors of w not in N':
        D(v) = min(D(v), D(w) + c(w,v))
```

Complexity: O(n^2) naive, O(n log n) with heap. Susceptible to **oscillations** when link costs depend on traffic load.

Used by: **OSPF**

#### Distance-Vector (DV) Algorithm -- Bellman-Ford

Each node maintains a distance vector of estimated costs to all destinations. Nodes exchange vectors only with **direct neighbors**, iteratively updating:

```
// Bellman-Ford equation
Dx(y) = min_v { c(x,v) + Dv(y) }
```

- **Iterative**: process continues until no more updates
- **Asynchronous**: nodes do not operate in lockstep
- **Distributed**: each node uses only information from neighbors

Problems:
- **Count-to-infinity**: bad news travels slowly across the network
- **Routing loops**: two nodes forwarding packets back and forth
- **Mitigation**: **poisoned reverse** (advertise infinite cost to neighbor if that neighbor is the next hop to the destination) -- solves 2-node loops but not 3+

Used by: **RIP**, **BGP** (path-vector variant)

#### LS vs. DV Comparison

| Aspect | Link-State | Distance-Vector |
|--------|-----------|-----------------|
| Message complexity | O(|N||E|) | Varies, bounded |
| Convergence speed | O(n^2), fast | Can be slow (count-to-infinity) |
| Robustness | Each node computes independently; a faulty node affects only itself | A faulty node's errors propagate to all routers |
| Algorithm | Dijkstra | Bellman-Ford |

---

### 5.9 Hierarchical Routing and Autonomous Systems

The Internet is too large for flat routing. It is organized into **Autonomous Systems (AS)** -- groups of routers under a single administrative control.

Each AS can run its own **intra-AS routing protocol**:
- **RIP** (Routing Information Protocol)
- **OSPF** (Open Shortest Path First)
- **IS-IS**

Between ASes: **inter-AS routing protocol**:
- **BGP4** (Border Gateway Protocol)

**Gateway routers** sit at AS boundaries and forward packets to/from other ASes.

**Hot-potato routing**: within an AS, choose the gateway router with the lowest internal cost to exit the AS, regardless of the remaining path length -- "get the packet out of our AS as quickly as possible."

---

### 5.10 RIP -- Routing Information Protocol

- **Distance-vector protocol** with hop count as cost metric
- Maximum cost limited to **15 hops** (16 = infinity) -- limits RIP to small ASes
- Routers exchange **RIP response messages** (up to 25 destination subnets) every **30 seconds** via UDP port **520**
- If a neighbor is silent for **180 seconds**, it is marked as unreachable
- RIP is implemented as an **application-level process** (`routed`) running over UDP -- it is an application-layer protocol that performs network-layer functionality

RIP routing table entry: `(destination_subnet, next_router, hops_to_destination)`

---

### 5.11 OSPF -- Open Shortest Path First

- **Link-state protocol** using **Dijkstra's algorithm**
- Each router builds a complete topological map of the AS
- Routers **flood** link-state advertisements:
  - Periodically (at least every 30 minutes)
  - Immediately when a link state changes
- OSPF messages run directly over IP (protocol number **89**); OSPF implements its own reliable transfer
- **Advantages over RIP**:
  - **Security**: MD5 authentication between routers
  - **Multiple same-cost paths**: load balancing
  - **Hierarchical structure**: AS partitioned into **areas** for scalability
  - **Integrated multicast support**

#### OSPF Areas

```
         +-------+    +-------+    +-------+
         | Area 1|    |Area 2 |    | Area 3|
         +---+---+    +---+---+    +---+---+
             |            |            |
         +---+------------+------------+---+
         |        Backbone (Area 0)         |
         +---------------------------------+
```

- Each area runs its own LS algorithm; area topologies are invisible to other areas
- **Area border routers** connect areas to the backbone
- **Backbone (Area 0)**: routes traffic between areas, contains all area border routers

---

### 5.12 BGP -- Border Gateway Protocol

BGP is the **de facto standard** inter-AS routing protocol (BGP4).

#### BGP Basics

- **eBGP**: BGP session between routers in **different** ASes
- **iBGP**: BGP session between routers in the **same** AS
- BGP runs over TCP on port **179** (semi-permanent connections)
- Destination is a **CIDR prefix** (subnet or set of subnets)
- A route in BGP is a prefix with associated **BGP attributes**

#### Key BGP Attributes

- **AS-PATH**: list of ASes through which the route advertisement has passed (loop detection: reject routes with own ASN in path)
- **NEXT-HOP**: IP address of the router interface that begins the AS-PATH (the exit point from the current AS)

#### BGP Route Selection (in order)

1. **Highest local preference** (policy-based, configured locally)
2. **Shortest AS-PATH** (distance-vector metric using AS hop count)
3. **Closest NEXT-HOP** (lowest intra-AS cost, i.e., hot-potato routing)
4. **Lowest BGP router ID** (tiebreaker)

#### Routing Policy in BGP

AS relationships govern route advertisement:
- A **stub AS** (single-homed) advertises only its own prefixes
- A **provider AS** may not advertise routes learned from one provider to another provider (no free transit)
- Import/export filters enforce **peering agreements**

---

### 5.13 Broadcast and Multicast Routing

#### Broadcast Routing

Deliver a packet from a source to **all** other nodes.

Methods:
1. **N-way unicast**: source sends N copies -- inefficient
2. **Uncontrolled flooding**: broadcast storm in graphs with cycles
3. **Sequence-number-controlled flooding**: nodes track (source, seq#) to suppress duplicates
4. **Reverse Path Forwarding (RPF)**: forward only if packet arrived on the shortest-path interface to the source
5. **Spanning-tree broadcast**: construct a spanning tree; forward only along tree edges

#### Multicast Routing

Deliver packets to a **subset** of nodes (a multicast group). Uses **Class D** IP addresses (`224.0.0.0/4`).

- **IGMP** (Internet Group Management Protocol): hosts use IGMP to inform routers about group membership (join/leave)
- **DVMRP** (Distance Vector Multicast Routing Protocol): RPF-based source-specific trees
- **PIM** (Protocol Independent Multicast): two modes -- dense mode (flood-and-prune) and sparse mode (rendezvous-point-based)

---

## 6. Link Layer

### 6.1 Link Layer Services

The link layer transfers **frames** between **adjacent nodes** across a single link. Possible services:

| Service | Description |
|---------|-------------|
| Framing | Encapsulate network-layer datagram into link-layer frame |
| Link access | MAC protocol for shared-medium links |
| Reliable delivery | Optional (used on error-prone wireless links; rarely on wired) |
| Error detection/correction | CRC, parity checks |
| Flow control | Pace sender and receiver on the link |

### 6.2 Error Detection and Correction

- **Parity check**: single parity bit (detects odd number of bit errors), 2D parity (detects and corrects single bit errors)
- **Checksum**: sum of data words; used in IP/TCP/UDP
- **CRC (Cyclic Redundancy Check)**:
  - Treat data bits as a polynomial D
  - Sender and receiver agree on a generator polynomial G (r+1 bits)
  - Sender appends R (r bits) such that (D * 2^r XOR R) is divisible by G
  - Receiver divides the received frame by G; non-zero remainder = error detected
  - Commonly used in Ethernet, Wi-Fi (CRC-32)

### 6.3 Multiple Access Protocols

For **broadcast links** (shared medium), multiple nodes may transmit simultaneously, causing **collisions**.

#### Channel Partitioning

- **TDMA** (Time Division Multiple Access): divide time into slots, assign to nodes
- **FDMA** (Frequency Division Multiple Access): divide frequency spectrum, assign channels
- **CDMA** (Code Division Multiple Access): each node uses a unique code; nodes can transmit simultaneously

#### Random Access

- **ALOHA**: transmit immediately; if collision, retransmit after random delay
  - Pure ALOHA efficiency: ~18%
  - Slotted ALOHA: slots synchronized; efficiency: ~37%
- **CSMA** (Carrier Sense Multiple Access): listen before transmitting
  - **CSMA/CD** (Collision Detection): used in classic Ethernet; detect collision, abort, jam signal, exponential backoff
  - **CSMA/CA** (Collision Avoidance): used in Wi-Fi (802.11); collision detection is impossible due to hidden terminal problem, so proactive avoidance (RTS/CTS, ACKs)

#### Taking-Turns

- **Token passing**: a token circulates; only the token holder transmits
- **Polling**: a master node polls each node in turn

### 6.4 Ethernet (IEEE 802.3)

Dominant wired LAN technology.

#### Ethernet Frame Format

```
+-----+-----+------------+-----+------+-----+-----+
|Preamble|Dest MAC|Src MAC|Type | Data | CRC |
| 8 B |  6 B   |  6 B   | 2 B |46-1500B| 4 B |
+-----+--------+--------+-----+------+-----+-----+
```

- **Preamble** (8 bytes): clock synchronization
- **Destination/Source MAC** (6 bytes each): 48-bit addresses
- **Type** (2 bytes): indicates upper-layer protocol (0x0800 = IPv4, 0x0806 = ARP, 0x86DD = IPv6)
- **Data**: 46-1500 bytes (payload + padding)
- **CRC** (4 bytes): CRC-32 error detection

#### Ethernet MAC Address

- 48 bits, globally unique (first 24 bits = OUI assigned to manufacturer)
- Written as hex pairs: `00:1A:2B:3C:4D:5E`
- Broadcast address: `FF:FF:FF:FF:FF:FF`

### 6.5 ARP (Address Resolution Protocol)

Maps an IP address to a MAC address on a LAN.

```
Host A (192.168.1.5) wants to send to Host B (192.168.1.10):

1. A checks ARP table for B's IP -> not found
2. A broadcasts ARP Query: "Who has 192.168.1.10?"
3. B responds with ARP Reply: "192.168.1.10 is at 00:1A:2B:3C:4D:5E"
4. A caches the mapping and sends the datagram in an Ethernet frame to B's MAC
```

ARP is **plug-and-play**: no configuration needed. ARP entries timeout to handle changes.

### 6.6 Link-Layer Switches

#### Switch Operation

A switch is **transparent** to hosts -- plug-and-play, self-learning. It maintains a **switch table** mapping MAC addresses to output interfaces.

**Self-learning algorithm**:
1. On frame arrival, record `(source_MAC, arrival_interface, time)` in switch table
2. Look up destination MAC in switch table:
   - Found: forward frame only to the matching interface
   - Not found: **flood** to all interfaces except the arrival one

#### Switch vs. Router

| Aspect | Switch | Router |
|--------|--------|--------|
| Forwarding basis | MAC address (L2) | IP address (L3) |
| Isolation | Single broadcast domain | Separates broadcast domains |
| Spanning tree | Required to prevent loops | No loops (TTL + routing) |
| Speed | Hardware forwarding, wire-speed | Software/hardware, slower per-packet |
| Plug-and-play | Yes (self-learning) | Requires IP configuration |

---

## 7. Network Security Basics

### 7.1 Threat Categories

| Threat | Description | Example Attack |
|--------|-------------|---------------|
| Eavesdropping | Passive interception of communications | Packet sniffing |
| Modification | Active alteration of messages | Man-in-the-middle, TCP session hijacking |
| Impersonation | Masquerading as another entity | IP spoofing, DNS poisoning |
| Denial of Service | Overwhelming resources to prevent legitimate use | SYN flood, amplification attacks |

### 7.2 Cryptographic Foundations

#### Symmetric-Key Cryptography

Same key for encryption and decryption.

- **Block ciphers**: AES (128/192/256-bit keys), DES (obsolete)
- **Stream ciphers**: RC4
- **Cipher Block Chaining (CBC)**: XOR each plaintext block with previous ciphertext block before encryption (breaks patterns)

#### Public-Key Cryptography

Different keys for encryption (public) and decryption (private).

- **RSA**: based on computational difficulty of factoring large primes
  - `c = m^e mod n` (encrypt)
  - `m = c^d mod n` (decrypt)
- Used for key distribution, digital signatures

#### Hash Functions (Message Digests)

One-way function producing fixed-length output.

- **MD5**: 128-bit, broken (collisions feasible)
- **SHA-1**: 160-bit, deprecated
- **SHA-256 / SHA-3**: 256-bit, currently recommended

#### Digital Signatures

Signer encrypts a message digest with their private key; verifier decrypts with signer's public key and compares hash. Provides **authentication** and **non-repudiation**.

### 7.3 Transport-Layer Security (TLS/SSL)

TLS provides security services at the transport layer (technically in the application layer, between application and TCP):

- **Confidentiality**: symmetric encryption (session key negotiated via public-key handshake)
- **Integrity**: MAC (Message Authentication Code)
- **Authentication**: certificates (X.509) signed by Certificate Authorities (CAs)

TLS Handshake (simplified):
1. ClientHello (supported cipher suites, nonce)
2. ServerHello (chosen cipher suite, nonce, certificate with public key)
3. ClientKeyExchange (Pre-Master Secret encrypted with server's public key)
4. Both sides derive session keys from Master Secret
5. Finished messages (verify handshake integrity)

### 7.4 Network-Layer Security (IPsec)

IPsec provides security between any two network-layer entities (hosts or routers):
- **Authentication Header (AH)**: data integrity + source authentication
- **Encapsulating Security Payload (ESP)**: encryption + optional authentication
- **Security Associations (SA)**: unidirectional logical connections with agreed algorithms and keys

IPsec operates in two modes:
- **Transport mode**: only IP payload is encrypted; IP header is visible
- **Tunnel mode**: entire IP datagram is encrypted and encapsulated in a new IP header

### 7.5 Firewalls and Intrusion Detection

**Firewall**: filters packets based on rules (IP addresses, port numbers, protocol types). Can be:
- **Stateless packet filter**: decisions per-packet based on header fields
- **Stateful filter**: tracks TCP connection state (SYN, ESTABLISHED) and only allows legitimate flows

**IDS (Intrusion Detection System)**: performs **deep packet inspection**, examining both headers and payloads against known attack signatures. Positioned at the network perimeter.

---

## Summary Table

| Layer | Core Functions | Key Protocols | PDU |
|-------|---------------|---------------|-----|
| Application | Network application services | HTTP, DNS, SMTP, FTP | Message |
| Transport | Process-to-process delivery, reliability, congestion control | TCP, UDP | Segment / Datagram |
| Network | Host-to-host routing and forwarding | IP, ICMP, OSPF, BGP | Datagram |
| Link | Adjacent-node frame transfer, MAC, error detection | Ethernet, Wi-Fi, ARP | Frame |
| Physical | Bit transmission over physical medium | Copper, fiber, radio specs | Bit |

The Internet's design philosophy: **keep the core simple, push complexity to the edge**. IP provides minimal best-effort service; intelligence lives in end-system protocols (TCP, application logic).

---

## References

- Kurose, J. F., & Ross, K. W. _Computer Networking: A Top-Down Approach_
- RFC 793 (TCP), RFC 791 (IPv4), RFC 2460 (IPv6), RFC 2328 (OSPF), RFC 4271 (BGP)
- Stevens, W. R. _TCP/IP Illustrated, Volume 1_
- IEEE 802.3 (Ethernet), IEEE 802.11 (Wi-Fi)
