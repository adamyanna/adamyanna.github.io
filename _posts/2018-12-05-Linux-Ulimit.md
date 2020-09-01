---
title: 通过 ulimit 改善系统性能
author: Teddy
date: 2018-10-22 12:00:00 +0800
categories: [实践, 实践记录]
tags: [Linux]
---

# 通过 ulimit 改善系统性能

#  ulimit:
## ulimit用于限制shell启动进程所占用的资源
* 所创建的内核文件的大小
* 进程数据快的大小
* shell进程创建文件的大小
* 内存锁住的大小
* 常驻内存集的大小
* 打开文件描述符的数量
* 分配堆栈的最大大小
* CPU时间
* 单个用户最大线程数
* shell进程所能使用的最大虚拟内存
> 硬资源和软资源的限制

## 使用方式

1. 登录shell到终止会话之间，对资源进行限制
2. 写入文件，可以针对特定用户，进行长期固定的限制

* ulimit --help

## 有效范围

1. 作用范围：作用于用户**当前**shell进程派生的子进程

## 修改系统文件

1. 修改单一用户限制 /etc/security/limits.conf

> 文件格式：
> domain type item value
>> domain: user and group &amp; * stand for all
>> type: "soft" or "hard"
>> item: "cpu,stack,nofile,...."
>> value: just value

2. 修改应用对整个系统的限制 /proc/*

* /proc 目录下包含很多linux系统当前状态参数

> /proc/sys/kernel/pid_max 内核态进程最大进程数
> /proc/sys/net/ipv4/ip_local_post_range ipv4本地端口范围
> ...
>> 由文件名称进行配置参数状态的判断即可


