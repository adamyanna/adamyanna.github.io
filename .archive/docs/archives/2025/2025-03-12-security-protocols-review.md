---
title: Security Protocols Review
layout: default
parent: 2025
grand_parent: Archives
---

# Security Protocols

## SSL/TLS (Secure Sockets Layer/ Transport Layer Security)

> Network Open Systems Interconnection (OSI) model
* Application Layer: HTTP/ SSH/ DNS
* Presentation Layer: SSL
* Session Layer: Sockets
* Trasport Layer: TCP/ UDP
* Network Layer: IP
* Data Link Layer: Ethernet, Switch, Bridge
* Physic Layer: Fiber/ Wireless

- SSL/ TLS are cryptographic protocols to secure data trasmission over network
- preventing: eavesdropping, tampering, forgery
- Keep data integrity through authentication

> Secure Sockets Layer (SSL) is a communication protocol, or set of rules, that creates a secure connection between two devices or applications on a network. It’s important to establish trust and authenticate the other party before you share credentials or data over the internet.

- **SSL is an older technology that contains some security flaws. Transport Layer Security (TLS) is the upgraded version of SSL that fixes existing SSL vulnerabilities. TLS authenticates more efficiently and continues to support encrypted communication channels.**

Version | Status | Notes
SSL 2.0 | Deprecated | Vulnerable to attacks
SSL 3.0 | Deprecated | POODLE attack
TLS 1.0 | Deprecated | Weak cryptographic algorithms
TLS 1.1 | Deprecated | Not widely supported anymore
TLS 1.2 | In Use | Strong security, widely adopted
TLS 1.3 | Latest | Faster, removes outdated algorithms, no RSA key exchange

### TLS 1.3 Handshake Workflow

📌 **1. ClientHello**

🔹 The Client(Browser, Application) sends:
- Supported TLS versions
- Cipher suites (AES-GCM, ChaCha20-Poly1305)
- Key share for ECDHE
- Random value for session uniqueness

📌 **2. ServerHello**

🔹 The server responds with:
- Chosen cipher suite
- Chosen ECDHE key share
- Random value
- Digital certificate (for authentication)

📌 **3. Key Exchange & Session Key Derivation**

🔹 Both client & server compute the shared secret uing the ECDHE algorithm:
- The server's key share + client's key share = Pre-Master Secret
- The shared secret is used to derive the session key for encryption


📌 **4. Finished Messages**

🔹 Client Finished
- Client sends a message encrypted with the session key to verify handshake completion

🔹 Server Finished
- Server sends a similar encrypted message to confirm everything is secure


### TLS 1.3

🎯 Faster reconnection using session tickets
🎯 TLS 1.3 is Faster:
- 1 round trip Handshake Steps
- Only ECDHE Key Exchange
- Only use strong Cipher suites
- 0-RTT Session Resumption


### 📌 Summary

🔹 TLS 1.3 is faster, more secure, and simpler
🔹 Uses only forward-secret key exchanges (ECDHE)
🔹 Eliminates outdated, weak algorithms
🔹 Supports 0-RTT session resumption for fast reconnects

## Kerberos

* Secure network authentication protocol that provides strong authentication for client-server applications
* Used in
	- Windows Activce Directory
	- Linux Authentication
	- Enterprise Applications
* Ticket-based authentication system
	- No plaintext passwords sent over the network
	- Single Sign-On -> Authenticate once & access multiple services
	- Mutual authentication -> Client and server verify each other

### Kerberos Workflow

* Client
	- requesting authentication
* Key Distribution Center (KDC)
	- Central authentication server
* Authentication Server (AS)
	- Issues initial Ticket Granting Ticket(TGT)
* Ticket Granting Server (TGS)
	- Issues service tickets
* Service Server (SS)
	- The server

📌 **1. Authentication Request (AS-REQ)**
* Client sends request to **Authentication Server(AS)**
	- Username
	- Timestamp

📌 **2. Authentication Reply (AS-REP)**
* AS verifies user identity & check use exists
* AS generates a **Ticket Granting Ticket** and encrypts it
	- Secret session key (only known by AS & user)
	- User hashed password as an encryption key
* TGT
	- session key
	- expiration time
	- client's identity

📌 **3. Request for Service Ticket (TGS-REQ)**
* 3.1 Client sends **TGT** to **Ticket Granting Server (TGS)**
* 3.2 Client requests **Service ticket** for specific resource
* 3.3 TGS verifies **TGT's validity** & **expiration**

📌 **4. Service Ticket Issuance (TGS-REP)**
* **TGS** issues a service ticket, includes:
	- Client identity
	- Service session key
	- Timestamp & Expiration time

> Client now has a **Valid service ticket** to access the requested resource

📌 **5. Service Access (AP-REQ & AP-REP)**
* Client sends **Service ticket** to **Service Server**
* **Service Server** decrypts and verifies the ticket
* If Everything is Valid:
	- Server grants access to requested resource
	- Mutual authentication can occur if needed

### Kerberos Vulnerabilities & Attacks

🚨 **1. Pass-the-Ticket Attack**
	- Attackers steal valid tickets and reuse them to gain access.
	- Mitigation: Use short-lived tickets + session monitoring.

🚨 **2. Golden Ticket Attack**
	- Attackers forge a master TGT using the KRBTGT account.
	- Mitigation: Regularly rotate KRBTGT passwords.

🚨 **3. Silver Ticket Attack**
	- Attackers forge service tickets without needing a TGT.
	- Mitigation: Enable mutual authentication.

🚨 **4. Replay Attacks**
	- Attackers capture and resend old tickets.
	- Mitigation: Use timestamps & short-lived tickets.

Feature | Kerberos | SSL/TLS
Purpose | User authentication | Secure communication
Authentication | Ticket-based | Certificate-based
Encryption | AES, DES | AES, ChaCha20, RSA
Session Management | Ticket renewal | Session keys
Use Case | Enterprise authentication | Web security (HTTPS, VPN)


### 📌 Summary

🔹 Kerberos is a secure authentication protocol used in Windows AD, Linux, and enterprise networks.
🔹 It uses tickets instead of passwords, ensuring secure authentication and Single Sign-On (SSO).
🔹 Key features: Mutual authentication, ticket expiration, and strong encryption.
🔹 Common attacks: Golden Ticket, Pass-the-Ticket, and replay attacks.
🔹 Used in Windows, Linux, enterprise applications, and secure network services.



























