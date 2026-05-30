# V2ray + Nginx Configuration

> 2018-12-05

A complete guide to setting up V2ray with Nginx reverse proxy, HTTPS/TLS certificates, and WebSocket tunneling.

## Architecture

Nginx handles TLS termination and forwards WebSocket connections to the V2ray backend over localhost. This provides a TLS-wrapped tunnel that is harder to fingerprint.

## Prerequisites

1. A domain name with DNS A record pointing to your server
2. CentOS/RHEL with YUM configured
3. Install base packages: `nginx`, `wget`, `socat`

## Installation

### 1. Install V2ray

```bash
wget https://install.direct/go.sh && bash go.sh

```

### 2. Generate TLS Certificate via ACME

```bash
curl https://get.acme.sh | sh
~/.acme.sh/acme.sh --issue -d www.example.com --standalone -k ec-256
~/.acme.sh/acme.sh --installcert -d www.example.com \
  --fullchainpath /etc/v2ray/v2ray.crt \
  --keypath /etc/v2ray/v2ray.key --ecc

```

### 3. Enable SELinux Internal Forwarding

```bash
setsebool -P httpd_can_network_connect 1

```

## Configuration Files

### V2ray Server Config (`/etc/v2ray/config.json`)

```json
{
  "inbound": {
    "port": 12057,
    "listen": "127.0.0.1",
    "protocol": "vmess",
    "settings": {
      "clients": [
        {
          "id": "<uuidgen>",
          "alterId": 64
        }
      ]
    },
    "streamSettings": {
      "network": "ws",
      "wsSettings": {
        "path": "/<path>"
      }
    }
  },
  "outbound": {
    "protocol": "freedom",
    "settings": {}
  }
}

```

### Nginx Reverse Proxy Config

```nginx
server {
    listen 443 ssl;
    ssl on;
    ssl_certificate     /etc/v2ray/v2ray.crt;
    ssl_certificate_key /etc/v2ray/v2ray.key;
    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers         HIGH:!aNULL:!MD5;
    server_name         <my.domain.name>;

    location /<path> {
        proxy_redirect off;
        proxy_pass http://127.0.0.1:12057;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $http_host;
    }
}

```

## Cloud Provider Notes

- **AWS / AWS Lightsail**: Straightforward deployment; standard VPS setup.
- **Google Cloud**: For best experience, create an IPv6-enabled load balancer. Configure HTTPS forwarding to two or more instances in the same availability zone (e.g., Taiwan or Hong Kong). Note: some Google Cloud IP ranges (30.35.x.x) experience intermittent connectivity issues in certain regions depending on GFW conditions at the time.
