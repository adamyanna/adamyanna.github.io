---
title: Prometheus
author: Teddy
date: 2020-04-06 10:00:00 +0800
categories: [体系结构-应用, 监控系统]
tags: [TODO, Prometheus, OpenSource, Go]
---


# Prometheus

[prometheus.io](https://prometheus.io/docs/introduction/overview/)

![](/Users/teddyna/Develop/dev/teddygoodman.github.io/img/prometheus-architecture.png)



* Prometheus生态系统架构图 ecosystem components architecture
* 基本流程：
  * Prometheus Server从“采集器” Jobs / Exporters 中收集指标数据
  * Server同时会从推送网关“收集” 生命周期较短的任务采集指标
  * Server将数据指标存储在本地的，并进行一些规则匹配来对这些data，按照时间序列对数据和记录进行汇总，或者生成告警；
  * Prometheus可以对接Grafana进行时序数据的界面化展示-Dashboard；



## 组件技术栈、源代码分析

* exporters
  * 



## Prometheus + M3DB + Nginx + LVS 网络监控架构















