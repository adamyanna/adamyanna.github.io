---
title: V2ray Nginx 配置
author: Teddy
date: 2018-12-05 12:00:00 +0800
categories: [实践, 实践记录]
tags: [V2ray]
---

# V2ray Nginx 配置
> "Nginx内网转发，https证书配置，V2ray代理配置"


## V2ray installation and nginx setup

### Simple Installation process

* 配置一个域名，提前配置DNS解析
```bash
domain=""
```

* 安装V2ray二进制，提前配置YUM源，makecache，安装wget, nginx, socat
```bash
wget https://install.direct/go.sh && bash go.sh
```

* 生成https证书，certificate
```bash
curl https://get.acme.sh | sh
~/.acme.sh/acme.sh --issue -d www.maclabx.ml --standalone -k ec-256
~/.acme.sh/acme.sh --installcert -d www.maclabx.ml --fullchainpath /etc/v2ray/v2ray.crt --keypath /etc/v2ray/v2ray.key --ecc
```

* 开启内网转发，selinux inner forwarding
```bash
setsebool -P httpd_can_network_connect 1
```


### Config file

* v2ray service config.json
```json
{
  "inbound": {
    "port": 12057,
    "listen":"127.0.0.1",
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

* nginx config
```conf
server {
  listen  443 ssl;
  ssl on;
  ssl_certificate       /etc/v2ray/v2ray.crt;
  ssl_certificate_key   /etc/v2ray/v2ray.key;
  ssl_protocols         TLSv1 TLSv1.1 TLSv1.2;
  ssl_ciphers           HIGH:!aNULL:!MD5;
  server_name           <my.domain.name>;
        location /<path> {
        proxy_redirect off;
        proxy_pass http://127.0.0.1:<forwording_port>;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $http_host;
        }
}
```

## Cloud services

* AWS & AWS lightsail

* Google cloud

> POC
> 如果想获取做好的体验，在Google cloud上开启一个ipv6的负载均衡，配置负载均衡的https转发到TW或者HK的同一AZ的两台以上实例
> Google cloud 30.35 网段每天有很多时间段无法访问，拜GFW所赐
>
