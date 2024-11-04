---
title: My Entire Career as a Coder in China [Reivew]
layout: default
parent: 2024
grand_parent: Archives
---

**Career**
{: .label .label-red }


# My Entire Career as a Coder in China [Reivew]

## Algorithm

- I - Array & Hashing
  * Deterministic Finite State Machine / Automaton
  * 2 Pointers
    * Binary Search
      * Sorting
      * Searching
      * Divide and Conquer
    * Sliding Window
  * Stack
  * Queues

- II - Linked Lists
  * Single Linked Lists
  * Double Linked Lists
  * Ring linked Lists

- III - Tree
  * Binary Tree
  * Tries[Prefix Tree]
  * Heap
  * Back Tracking

- IV - Graphs
  * BFS
  * DFS

- V - Dynamic Programming
  * Greedy Algorithms

- VI - Bitwise
- VII - Time Complexity
  * Understanding of Big-O notation and how to optimize solutions.

## System Design

* Distributed Systems
  * Load balancing
  * replication
  * sharding
  * consistency models
  * CDN
* Storage Systems
  * SQL vs NoSQL
  * databases (e.g., Cassandra, DynamoDB)
  * file systems
* Caching Strategies
  * Cache invalidation
  * distributed caches like Redis or Memcached
* Scalability
  * Horizontal vs Vertical scaling
  * message queues (e.g., Kafka, RabbitMQ)
* High Availability and Fault Tolerance
  * Data replication
  * fail over strategies
  * consensus protocols (like Paxos, Raft)

## Behavioral Interview

STAR

## Knowledge of Specific Technologies and Tools

* os hypervisor
	* KVM is a hypervisor
	* QEMU or Cloud Hypervisor are vm manager utilizing KVM as hypervisor.
* Kubernetes
* Terraform
* Ansible

## Scenario-Based Problem-Solving

## SRE

* Docker
  * fundamental engine basic
    * linux kernel namespace
      * Namespaces for fundamental Isolation
      * IPC - Inter-process communication
        * Signals
        * Anonymous Pipes
        * Named Pipes or FIFOs
      * Network
      * Mount
      * PID
      * User
      * UTS
      * `Cgroup`
      * System Call
        * `CLONE`
        * `UNSHARE`
        * `SETNS`
    * linux kernel control group
      * use `Cgroup` to do Resource Management
      * `CPU`
      * `blkio`
      * `memory`
      * `device`
      * `freezer`
    * linux union file system
      * Union File Systems for Layered Storage
      * manage layers in the container images
      * `OverlayFS` and `AUFS`.