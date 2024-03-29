---
title: 时序数据完整性的方法巡检工具
layout: default
parent: 2020
grand_parent: Archives
---

**Go**
{: .label .label-blue }

**RabbitMQ**
{: .label .label-green }

**Data-Patrol**
{: .label .label-purple }

**2020-05-13 17:46:51 +0800**
{: .label .label-yellow }

# 程序设计时序图

![]({{ "/assets/images/docs/data-patrol.png" | relative_url }})



## 如图所示：
1. 将监控数据接入消息队列后，监控数据可以进行多路复用，将监控数据接入审计工具；审计工具的主要功能包括：
   1. 监控数据每个采集间隔内的完整性；
   2. 监控数据是否发生完全丢失；
   3. 监控对象和其上报的监控指标是否覆盖全部初始配置。
2. 审计工具的实现方式，将每个监控项的10个单位内的时间戳放在缓存栈内，每经过一个周期，各个栈对应的线程会做数据完整性的检查；检查结果会通过相应的事件存储在数据库中；
1.	图为审计工具的时序图，图中以Golang的协程为基础单位，展示了数据处理的全部流程和并发情况；
2.	Consumer的协程会连接消息队列，实时接收消息并通过通信管道将消息分发到数量为1000的DataDistribution协程中，DataDistribution会对消息做相对应的拆封，将每个拆封后的数据发送到它对应监控对象的处理协程中，处理协程会做数据缓存并每个周期检测缓存栈，为了防止过多的协程导致阻塞和饥饿，每个协程会设置10分钟的超时，如果十分钟内没有进行数据处理，就会将自己杀掉，数据最终会发给事件上报的协程，从而实现事件的存储和前端展示；

[Source Code](https://github.com/TeddyGoodman)