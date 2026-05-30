# Kubernetes & Docker

> 2020-04-03

Kubernetes architecture deep dive — control plane components, node agents, and the Docker runtime model.

## Control Plane

The control plane makes global cluster decisions and responds to cluster events. Components can run on one or multiple machines; default deployment scripts co-locate all control plane components on a single machine (no user Pods on that node).

![Kubernetes Components](../../images/components-of-kubernetes.png)

### kube-apiserver

The front-end of the control plane, exposing the Kubernetes API externally. Horizontally scalable — deploy more instances behind a load balancer (e.g., dual-node LVS + Nginx forwarding traffic to API servers with weighted distribution).

### etcd

A distributed, highly-available key-value store ([etcd.io](https://etcd.io)) used to persist all Kubernetes cluster data. Production deployments require additional backup strategies beyond etcd's built-in HA.

### kube-scheduler

Analogous to OpenStack Nova's scheduler — selects an appropriate node for each newly-created Pod. Decision factors include:

- Combined resource requirements (CPU, memory)
- Hardware/software/policy constraints
- Affinity / anti-affinity specifications
- Data locality
- Inter-workload interference
- Deadlines

### kube-controller-manager

A single binary embedding multiple logically independent controllers:

| Controller | Responsibility |
|---|---|
| **Node Controller** | Detects and responds to node failures |
| **Replication Controller** | Maintains correct Pod count for replication-managed services |
| **Endpoint Controller** | Joins Endpoint objects to specified Services and Pods |
| **Service Account & Token Controllers** | Manages API access accounts and namespace-scoped tokens |

### cloud-controller-manager

Interfaces with the underlying cloud provider. Runs cloud-provider-specific control loops. Controllers that depend on cloud provider code:

| Controller | Cloud Interaction |
|---|---|
| **Node Controller** | Checks if stopped nodes have been released in the cloud |
| **Route Controller** | Configures routes in the underlying infrastructure |
| **Service Controller** | Creates, updates, deletes cloud load balancers |
| **Volume Controller** | Creates, attaches, mounts volumes; orchestrates with cloud provider |

Future versions will decouple cloud provider code from core Kubernetes.

## Node Components

### kubelet

An agent running on every cluster node, ensuring containers run in Pods as specified.

### kube-proxy

Network proxy implementing the Kubernetes Service abstraction — maintains network rules on nodes, enabling Pod-to-Pod and external-to-Pod communication.

### Container Runtime

Docker is the most common runtime. Kubernetes also supports containerd, CRI-O, and others via the Container Runtime Interface (CRI).

## Docker

Docker provides OS-level virtualization through:
- **Linux namespaces** — Process isolation (PID, network, mount, UTS, IPC, user, cgroup)
- **cgroups** — Resource limiting and accounting (CPU, memory, disk I/O, network)
- **Union filesystems** — Layered image construction (OverlayFS, AUFS)

## References

- [Kubernetes Documentation](https://kubernetes.io/)
