---
title: Linux网络基础
author: Teddy
date: 2020-03-16 10:00:00 +0800
categories: [体系结构-基础, Linux]
tags: [TODO, Linux, Network]
---

# Linux Network

## 1. TCP连接状态中大量客户处于TIME_WAIT


## 2. Linux的套接字线程

为了实现客户端请求的快速相应和快速处理，据是高并发，则必须使用多线程机制。主题思想是：serversocket通过accept建立一个socket，然后起一个线程，把这个socket扔给新建的线程进行处理，而serversocket所在的主线程，则继续去监听端口，以此实现多线程通信

Linux中的ipv6 实际上是可以处理 ipv4 的请求的当 V6ONLY 没有开启的时候，反之不然；

> If we have the unspecified IPv4 address (0.0.0.0) and
> the unspecified IPv6 address (::) is next, we need to
> swap the order of these in the list. We always try to
> bind to IPv6 first, then IPv4, since an IPv6 socket
> might be able to receive IPv4 packets if V6ONLY is not
> enabled, but never the other way around.