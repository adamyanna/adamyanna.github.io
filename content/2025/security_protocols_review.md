# Security Protocols Review

> 2025-03-12

A review of network security protocols — the OSI model as a transport foundation, SSL/TLS cryptographic mechanisms, version evolution, and the TLS 1.3 handshake.

## The OSI Model & TLS Placement

TLS operates at the **Presentation Layer** (Layer 6) of the OSI model, sitting between the application and transport layers. This positioning allows it to secure any application-layer protocol transparently.

| Layer | Name | Protocols / Technologies |
|---|---|---|
| 7 | Application | HTTP, SSH, DNS, SMTP |
| 6 | Presentation | **SSL / TLS** |
| 5 | Session | Sockets, RPC |
| 4 | Transport | TCP, UDP |
| 3 | Network | IP, ICMP |
| 2 | Data Link | Ethernet, Switches, Bridges |
| 1 | Physical | Fiber, Wireless, Copper |

TLS provides three guarantees for data in transit:

1. **Confidentiality** — symmetric encryption prevents eavesdropping
2. **Integrity** — MAC (Message Authentication Code) prevents tampering
3. **Authentication** — certificate chain validates server (and optionally client) identity

## SSL vs TLS

Secure Sockets Layer (SSL) was the original protocol developed by Netscape in the mid-1990s. TLS (Transport Layer Security) is its IETF-standardized successor. All SSL versions are now deprecated and considered insecure.

| Version | Status | Notes |
|---|---|---|
| SSL 2.0 | Deprecated (2011) | Vulnerable to downgrade and cipher-suite attacks |
| SSL 3.0 | Deprecated (2015) | POODLE attack (Padding Oracle On Downgraded Legacy Encryption) |
| TLS 1.0 | Deprecated (2021) | Weak CBC-mode ciphers; BEAST attack |
| TLS 1.1 | Deprecated (2021) | Limited adoption; superseded by TLS 1.2 |
| TLS 1.2 | Widely deployed | Strong AEAD ciphers (AES-GCM, ChaCha20-Poly1305); RSA and ECDHE key exchange |
| TLS 1.3 | Current (RFC 8446) | Removes legacy algorithms; 1-RTT handshake; mandatory forward secrecy |

## TLS 1.3 Handshake

TLS 1.3 reduced the handshake from 2 round-trips (TLS 1.2) to **1 round-trip** by eliminating the RSA key exchange and mandating Ephemeral Diffie-Hellman (ECDHE).

```
Client                                  Server
  │                                       │
  │ ──── ClientHello ──────────────────> │
  │      - Supported TLS versions         │
  │      - Cipher suites                  │
  │      - ECDHE key share                │
  │      - Random nonce                   │
  │                                       │
  │ <──── ServerHello ──────────────────  │
  │      - Chosen cipher suite            │
  │      - ECDHE key share                │
  │      - Certificate (X.509)            │
  │      - Server Finished                │
  │                                       │
  │ ──── Client Finished ──────────────> │
  │                                       │
  │ <==== Encrypted Application Data ====>│
  │                                       │
```

### Step-by-Step

**1. ClientHello**

The client sends its capabilities:
- Supported TLS versions (1.3, optionally 1.2 for downgrade)
- Cipher suites: AES-256-GCM, ChaCha20-Poly1305
- **Key share for ECDHE** — the client generates an ephemeral key pair and sends the public portion, enabling 0-RTT key agreement
- Random value for session uniqueness

**2. ServerHello**

The server responds with:
- The chosen cipher suite from the client's list
- **Its own ECDHE key share** — server's ephemeral public key
- Digital certificate (X.509) for authentication
- Server Finished (encrypted with the derived session key)

**3. Key Exchange & Session Key Derivation**

Both sides compute the shared secret using ECDHE:

```
Shared Secret = Server Key Share × Client Key Share (elliptic curve point multiplication)
Session Key  = HKDF(Shared Secret, Handshake Transcript)
```

The key properties of ECDHE:
- **Forward secrecy**: compromise of the server's long-term certificate key does not decrypt past sessions
- **Ephemeral**: fresh key pair per handshake, never stored or reused

**4. Finished Messages**

Both client and server exchange Finished messages encrypted with the derived session key, proving the handshake completed without tampering. Application data follows over the same encrypted channel.

## Cipher Suite Comparison

| Algorithm | TLS 1.2 | TLS 1.3 | Notes |
|---|---|---|---|
| RSA key exchange | Yes | Removed | No forward secrecy |
| ECDHE key exchange | Optional | Mandatory | Perfect forward secrecy |
| AES-CBC | Yes | Removed | Vulnerable to padding oracle attacks |
| AES-GCM | Yes | Yes | Authenticated encryption |
| ChaCha20-Poly1305 | Yes | Yes | AEAD for mobile/ARM devices |
| SHA-1 | Yes (legacy) | Removed | Collision attacks; replaced by SHA-256/384 |

## Best Practices

- **Minimum TLS 1.2** — reject TLS 1.0/1.1 connections; browsers dropped support in 2020-2021
- **HSTS** (HTTP Strict Transport Security) — force HTTPS via `Strict-Transport-Security` header
- **Certificate transparency** — monitor CT logs for misissued certificates
- **Automated renewal** — use ACME (Let's Encrypt) with 90-day certificate lifetimes
- **Key pinning** — avoid HPKP (deprecated); rely on CT and CAA records instead

## References

- [RFC 8446 — TLS 1.3](https://datatracker.ietf.org/doc/html/rfc8446)
- [SSL Labs Best Practices](https://github.com/ssllabs/research/wiki)
- [Mozilla Server Side TLS](https://wiki.mozilla.org/Security/Server_Side_TLS)
- [Let's Encrypt ACME Protocol](https://letsencrypt.org/docs/)
