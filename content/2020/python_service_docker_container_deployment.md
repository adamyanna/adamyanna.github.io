# Python Service: Docker Container Deployment

> 2020-05-14

A practical guide to containerizing Python web services for production, from Dockerfile fundamentals through multi-service orchestration, logging, and high-availability deployment patterns -- illustrated with a real-world network monitoring microservice stack.

## Why Containerize Python Services?

Python web services face well-known deployment friction: interpreter version conflicts, system library mismatches, and the dreaded "it works on my machine" problem. Docker eliminates these by packaging the application with its entire runtime stack into a single, versioned artifact that runs identically on a developer laptop, a CI runner, or a production bare-metal host.

Beyond reproducibility, containers bring operational advantages that matter in production: process isolation, resource limits via cgroups, restart policies that replace supervisor daemons, and orchestration primitives (Swarm, Kubernetes) for zero-downtime rolling updates.

## Python Web Service Architecture in Containers

A typical containerized Python service stack consists of:

- **Application layer**: A WSGI/ASGI Python process (gunicorn, uvicorn) serving requests, often behind a lightweight proxy like Nginx.
- **Static assets**: Served by the reverse proxy or a CDN, not by the Python process.
- **Configuration**: Injected at runtime via environment variables or mounted config files -- never baked into the image.
- **Logs**: Written to stdout/stderr so the container runtime (Docker, containerd) can collect and forward them.
- **State**: Databases, caches, and queues run in separate containers or managed cloud services. The application container itself is stateless and disposable.

In the monitoring microservice example we will follow, three Python services run side by side:

| Service | Role |
|---|---|
| `nspmonitor` | Core network monitoring agent -- SNMP polling, health checks, metric collection |
| `lvxmonitor-proxy` | Reverse proxy aggregating results from multiple monitor agents |
| `pagwmonitor` | Optional packet-gateway monitor for VPP/NFV environments |

Each service runs in its own container, managed as a Docker Swarm stack, with logs rotated on the host and configuration mounted from a shared volume.

## Writing a Dockerfile for Python Apps

### Basic Single-Stage Dockerfile

```dockerfile
FROM python:3.8-slim

WORKDIR /app

# Install system dependencies first (rarely changes, good cache layer)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libsnmp-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (cached separately from app code)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8080

CMD ["python", "-m", "gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:application"]
```

The layer ordering matters. System packages and `pip install` change rarely, so they sit above the application code `COPY`. This means rebuilding after a code change reuses the cached dependency layers -- a 5-second build instead of 5 minutes.

### Multi-Stage Build for Smaller Images

Python images are large. A production image does not need gcc, header files, or the pip cache. Multi-stage builds copy only the runtime artifacts into a slim final image:

```dockerfile
# ---- Build Stage ----
FROM python:3.8-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---- Runtime Stage ----
FROM python:3.8-slim AS runtime

WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application
COPY . .

# Ensure scripts in .local/bin are on PATH
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8080
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:application"]
```

The final image drops gcc, dev headers, and build artifacts. Typical savings: 200-400 MB depending on the dependency tree.

### The Monitoring Service Image

The original deployment imports a pre-built image with SSH access for debugging:

```bash
docker import net_monitor_add_ssh.tar netmonitor:v1.0
```

For a modern approach, the Dockerfile for a Python monitoring agent would look like:

```dockerfile
FROM python:3.8-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    net-snmp \
    snmp-mibs-downloader \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agent/ /app/agent/
COPY etc/ /app/etc/

ENTRYPOINT ["python", "/app/agent/nsp/entry.py"]
```

## Dependency Management

### requirements.txt (Simplest)

```
# requirements.txt
flask==1.1.2
gunicorn==20.0.4
pysnmp==4.4.12
requests==2.23.0
pyyaml==5.3.1
```

Pin exact versions. A floating version like `flask>=1.0` will produce different images depending on when you build. Reproducibility demands exact pins.

Generate a pinned file from a loose spec:

```bash
pip freeze > requirements.txt
```

### Pipenv and Pipfile.lock

Pipenv adds deterministic locking (like `package-lock.json` for Node) and separates dev from production dependencies:

```bash
pipenv install flask gunicorn pysnmp
pipenv install --dev pytest black
pipenv lock   # generates Pipfile.lock with SHA256 hashes
```

In the Dockerfile, install only production dependencies:

```dockerfile
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile
```

`--deploy` ensures the lock file is up to date; `--ignore-pipfile` uses the lock file exclusively; `--system` installs to the system Python instead of a virtualenv (since the container is already isolated).

### Poetry (Alternative)

Poetry provides the same guarantees with a `pyproject.toml`:

```dockerfile
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev --no-interaction
```

## Docker Compose for Multi-Service Setups

The monitoring system uses three compose files, each defining one service, deployed together as a Docker Swarm stack. Below is a composite `docker-compose.yml` that captures the same architecture for local development:

```yaml
version: "3.8"

services:
  nspmonitor:
    image: netmonitor:v1.0
    networks:
      - monitor-net
    volumes:
      - /opt/netmon/agent:/app/agent
      - /opt/netmon/agent/nspmonitor/etc/${AZ:-SCA}:/app/etc
      - /var/log/nspmonitor:/var/log/nspmonitor
      - /etc/localtime:/etc/localtime:ro
    environment:
      - AZ=${AZ:-SCA}
      - LOG_LEVEL=INFO
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    command:
      - python
      - /app/agent/nsp/entry.py
      - --config-file=/app/etc/nspmonitor.ini
      - --log-file=/var/log/nspmonitor/nspmonitor.log

  lvxmonitor-proxy:
    image: netmonitor:v1.0
    networks:
      - monitor-net
    ports:
      - "8080:8080"
    volumes:
      - /opt/netmon/agent:/app/agent
      - /opt/netmon/agent/nspmonitor/etc/${AZ:-SCA}:/app/etc
      - /var/log/lvxmonitor:/var/log/lvxmonitor
      - /etc/localtime:/etc/localtime:ro
    environment:
      - AZ=${AZ:-SCA}
    deploy:
      replicas: 2
    command:
      - python
      - /app/agent/nginx/proxy.py
      - --config-file=/app/etc/lvxmonitor_proxy.conf
      - --log-file=/var/log/lvxmonitor/proxy.log

  pagwmonitor:
    image: netmonitor:v1.0
    networks:
      - monitor-net
    volumes:
      - /opt/netmon/agent:/app/agent
      - /opt/netmon/agent/nspmonitor/etc/${AZ:-SCA}:/app/etc
      - /var/log/nspmonitor:/var/log/nspmonitor
      - /etc/localtime:/etc/localtime:ro
    environment:
      - AZ=${AZ:-SCA}
    deploy:
      replicas: 1
    profiles:
      - pagw    # Only deployed in VPP-enabled regions
    command:
      - python
      - /app/agent/pagw/entry.py
      - --config-file=/app/etc/nspmonitor.ini
      - --log-file=/var/log/nspmonitor/pagwmonitor.log

networks:
  monitor-net:
    driver: overlay
```

Key design decisions visible here:

1. **Availability zone drilling**: The `${AZ}` variable selects region-specific config directories (`SCA`, `EFA`, etc.). One image, many regions.
2. **Shared volumes**: Application code lives on the host at `/opt/netmon/agent` and is mounted into containers. This allows updating code without rebuilding images -- useful during rapid iteration, but for production you would prefer immutable images.
3. **Host timezone**: Mounting `/etc/localtime:ro` ensures container timestamps match the host, critical for log correlation.
4. **Profiles for optional services**: `pagwmonitor` uses a Compose profile so it is only started in regions that have VPP infrastructure.
5. **Network isolation**: The `overlay` driver enables multi-host communication in Swarm mode.

### Deploying as a Swarm Stack

In production, the compose files are deployed via `docker stack deploy`:

```bash
cd /opt/netmon/agent/agent_updater/package/nspmonitor-1.2.5.dev57/docker-compose/

# Deploy NSP monitor
docker stack deploy -c nspmonitor-compose.yml nspmonitor_SCA

# Deploy proxy
docker stack deploy -c lvxmonitor-proxy-compose.yml lvxmonitor_proxy_SCA

# Optional: PAGW monitor (VPP products only)
docker stack deploy -c pagwmonitor-compose.yml pagwmonitor_SCA

# Verify all services running
docker service ls
docker service ps nspmonitor_SCA --no-trunc
```

## Environment Configuration

### Configuration File Strategy

The monitoring services use INI-style config files mounted from the host:

```ini
; /opt/netmon/agent/nspmonitor/etc/SCA/nspmonitor.ini
[agent]
zone = SCA
log_level = INFO
poll_interval = 60

[targets]
gateway = 10.0.1.1
dns_servers = 10.0.1.53,10.0.1.54

[output]
falcon_agent_port = 12050
```

Region-specific configs live in separate directories (`etc/SCA/`, `etc/EFA/`) with a `TEMPLATE/` directory serving as the baseline. New regions copy the template and edit IPs:

```bash
mkdir /opt/netmon/agent/agent_updater/updater/config/EFA/
cp /opt/netmon/agent/agent_updater/updater/config/SCA/config.json \
   /opt/netmon/agent/agent_updater/updater/config/EFA/
vim /opt/netmon/agent/agent_updater/updater/config/EFA/config.json
```

This pattern -- template + per-environment overrides -- is universal. Modern alternatives include:

- **Environment variables** for discrete values (`DB_HOST`, `API_KEY`)
- **Consul/Vault** for dynamic configuration and secrets
- **ConfigMap** objects in Kubernetes
- **.env files** with `python-dotenv` for local development

### Environment Variables in Compose

Use an `.env` file or shell exports to set the availability zone:

```bash
# .env
AZ=EFA
```

```bash
# Or inline
AZ=EFA docker stack deploy -c nspmonitor-compose.yml nspmonitor_EFA
```

## Logging and Monitoring Setup

### Application Logging

The Python entry points accept a `--log-file` argument. When omitted, logs go to stdout -- the preferred pattern for containerized services:

```python
# entry.py
import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument("--config-file", required=True)
parser.add_argument("--log-file", default=None)  # None = stdout
args = parser.parse_args()

logging.basicConfig(
    filename=args.log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
```

In the debug test container, operators intentionally drop `--log-file` to stream logs directly to the console:

```bash
docker run -i -t -d --network=host \
    -v /opt/netmon/:/app \
    -v /var/log/:/var/log/ \
    -v /etc/localtime:/etc/localtime \
    --name TESTPOD netmonitor:v1.0 /bin/bash

# Debug: remove --log-file to see output in real time
/usr/bin/python /app/agent/nsp/entry.py \
    --config-file=/app/etc/SCA/nspmonitor.ini
```

### Log Rotation on the Host

Docker containers should write to stdout/stderr for the runtime to manage. When writing to files on a mounted volume, logrotate prevents disk exhaustion:

```
# /etc/logrotate.d/nspmonitor
/var/log/nspmonitor/*.log {
    rotate 10
    size 50M
    missingok
    compress
    copytruncate
}
```

- `rotate 10`: Keep 10 rotated files before deleting the oldest.
- `size 50M`: Rotate when the file reaches 50 MB, not daily.
- `copytruncate`: Copy the file and truncate the original in place. Works without signaling the Python process. The alternative `postrotate` + signal approach requires the application to reopen its file handles.
- `compress`: Gzip rotated files to save disk space.
- `missingok`: Do not error if the log file does not exist yet.

### Health Checks and Monitoring

Verify the Open-Falcon agent is running on every host to collect system metrics:

```bash
# Check the Falcon agent port
netstat -antl | grep 12050

# Check processes
ps -aux | grep falcon
ps -aux | grep ops_updater
```

For the containerized services, Swarm provides built-in health monitoring:

```bash
# List all services and their replica states
docker service ls

# Inspect individual task status
docker service ps nspmonitor_SCA --no-trunc

# Tail logs for errors
tail -f /var/log/nspmonitor/nspmonitor.log | grep ERROR
```

## Host-Level Production Considerations

### Ulimit Tuning

Python services that open many network connections (monitoring agents polling hundreds of devices) can exhaust the default file descriptor limit (often 1024):

```bash
# Check current limits
ulimit -a

# /etc/security/limits.conf (persistent, per-user)
* - nproc 102400
* - nofile 102400

# /etc/sysctl.conf (system-wide maximum)
fs.file-max = 6815744

# Apply and reboot
reboot
```

Docker applies its own ulimit defaults. Override them per container in the compose file:

```yaml
services:
  nspmonitor:
    ulimits:
      nofile:
        soft: 102400
        hard: 102400
```

### NTP Time Synchronization

Distributed monitoring is useless with clock skew. Logs from different hosts must correlate, and SNMP polling timestamps must be accurate:

```bash
# Check current NTP status
systemctl status ntpd
ntptime

# Ensure /etc/ntp.conf points to regional NTP servers
# For Asia/Shanghai (UTC+8):
vim /etc/ntp.conf
systemctl restart ntpd
ntptime   # Verify synchronized
```

### DNS Resolution

Services in a monitoring stack resolve internal hostnames. Verify DNS is functional before deploying:

```bash
cat /etc/resolv.conf
# Should contain:
#   search cloud.pub
#   nameserver <dns_ip>

# Test resolution and connectivity
ping gateway-OpenFalcon.cloud.pub
telnet gateway-OpenFalcon.cloud.pub 12057
```

### YUM Repository Configuration

CentOS 7 hosts need working package repositories for initial Docker and SNMP tool installation:

```bash
yum clean all && yum makecache
# If errors occur, check /etc/yum.repos.d/*.repo
# Copy working .repo files from a known-good host in the same region
```

## Docker Swarm Cluster Setup

### Initializing a Three-Node HA Cluster

The original deployment uses a three-manager Swarm for high availability. Managers use the Raft consensus algorithm -- an odd number is required for quorum:

```bash
# Step 1: Initialize the first manager
docker swarm init --advertise-addr 10.0.0.1

# Output includes a join token. On the other two nodes:
docker swarm join --token SWMTKN-1-xxx 10.0.0.1:2377

# Step 2: Promote workers to managers (on the first manager)
docker node ls
docker node promote node-2 node-3

# Step 3: Verify
docker node ls
# All three should show MANAGER STATUS as "Reachable" or "Leader"
```

### Installing Docker on a Fresh CentOS 7 Host

The deployment script (`install.sh`) uses Docker's static binary package for offline/air-gapped environments:

```bash
# Files required in the same directory:
#   install.sh
#   add_manager.sh
#   docker-package.tar.gz

# Install Docker Engine on the first node
bash install.sh 10.0.0.1
# Records a join token -- copy the string after "--token"

# Add the second node as a manager
bash add_manager.sh SWMTKN-1-xxx 10.0.0.1:2377

# Verify cluster state
docker node ls
```

## Automated Deployment with Ansible

Once the Swarm cluster is running, Ansible automates configuration pushes and service deployment:

```bash
cd /opt/netmon/agent/agent_updater/ansible/playbooks/init
python init.py    # Initializes the Ansible environment

cd /opt/netmon/agent/agent_updater/updater
python updater.py EFA ansible   # Deploy to the EFA availability zone
```

This runs playbooks that:
1. Copy the latest `nspmonitor-xxx.tar.gz` to target hosts
2. Generate region-specific config files from templates
3. Execute `docker stack deploy` with the correct compose file and service name
4. Validate all services reach the running state

After config changes on one node, sync to peer nodes:

```bash
cd /opt/netmon/agent/
scp -r nspmonitor <other_agent_ip>:/opt/netmon/agent
```

## Version Updates and Rolling Deploys

Updating a running service without downtime:

```bash
# 1. Deploy the new package
tar -xvf nspmonitor_1.2.6.tar.gz
cp nspmonitor_1.2.6/nspmonitor /opt/netmon/agent/ -r

# 2. Trigger a rolling update (Swarm replaces tasks one at a time)
docker service update nspmonitor_agent --force

# 3. Verify new tasks are running
docker service ps nspmonitor_agent --no-trunc

# 4. Check logs for errors
tail -f /var/log/nspmonitor/nspmonitor.log
```

Swarm's default update order is one task at a time (`--update-parallelism 1`) with a 10-second delay between tasks. For a service with 2 replicas, this means zero downtime -- one replica always serves traffic while the other restarts.

## Debugging Containerized Python Services

When a service misbehaves, run an interactive test container sharing the host network and volumes:

```bash
docker run -i -t -d \
    --network=host \
    -v /opt/netmon/:/app \
    -v /var/log/:/var/log/ \
    -v /etc/localtime:/etc/localtime \
    --name TESTPOD \
    netmonitor:v1.0 /bin/bash
```

This gives you a shell inside the same environment as the production container, with access to the same files, network interfaces, and logs. Run the Python process manually, add print statements, or attach a debugger:

```bash
docker exec -it TESTPOD bash
/usr/bin/python /app/agent/nsp/entry.py \
    --config-file=/app/etc/SCA/nspmonitor.ini
# Logs now stream to the terminal
```

## Cluster Migration: 2-Node to 3-Node HA

Expanding from two to three managers. The process is destructive to the existing cluster -- plan a maintenance window:

```bash
# ---- Phase 1: Prepare the new node ----
# Run node initialization (SSH, Docker, ulimit, NTP, DNS) on the third host
# Install Docker and join it to the existing cluster as a worker

# ---- Phase 2: Teardown the 2-node cluster ----
docker service ls
docker service rm nspmonitor_agent lvxmonitor_proxy_SCA --force

docker node ls
docker node rm --force node-1 node-2

# ---- Phase 3: Create the 3-node cluster ----
# On the chosen leader:
docker swarm init --advertise-addr 10.0.0.1

# On the other two nodes:
docker swarm join --token SWMTKN-1-xxx 10.0.0.1:2377

# Promote to managers:
docker node promote node-2 node-3

# ---- Phase 4: Redeploy services ----
docker stack deploy -c nspmonitor-compose.yml nspmonitor
docker stack deploy -c lvxmonitor-proxy-compose.yml lvxmonitor_proxy_SCA
```

## Key Takeaways

1. **One image, many environments**: The same Docker image serves all availability zones. Region-specific behavior comes from mounted config files and environment variables, not image variants.
2. **Log to stdout by default**: Write log files to mounted volumes only when you need persistent, rotated access. In all other cases, emit structured logs to stdout and let the container runtime handle collection.
3. **Treat containers as immutable**: Updating code by swapping files under a mounted volume works in a pinch, but the long-term pattern is to build a new image and perform a rolling update.
4. **Odd number of managers**: Swarm's Raft consensus requires an odd number of managers (1, 3, 5) to avoid split-brain. Three is the practical minimum for production HA.
5. **Validate the host, not just the container**: NTP skew, exhausted file descriptors, or broken DNS on the host will manifest as mysterious application failures inside containers. The original runbook spends as many steps on host configuration as on Docker commands -- and rightly so.
6. **Test in situ**: The `TESTPOD` pattern -- running a throwaway container with `--network=host` and the same volume mounts -- is an effective debugging technique that does not disturb production services.
