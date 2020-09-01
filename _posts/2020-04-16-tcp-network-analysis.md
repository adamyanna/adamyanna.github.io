---
title: 生产环境TCP网络问题分析
author: Teddy
date: 2020-04-16 10:00:00 +0800
categories: [实践, 问题分析]
tags: [TCP&IP, Network, Socket]
---

# 生产环境TCP网络问题分析

## 服务集群的TCP网络问题分析，涉及大量TIME_WAIT原因分析及解决方案

# 网络监控系统集群模型架构图

![]({{ "/assets/img/posts/network-monitoring-system-architecture.png" | relative_url }})


4月9日突发问题原因分析

* 流量突增导致monitor_server服务端发送到OpenFalcon的请求大量超时
	* 上报OpenFalcon请求超时的情况又导致server端大量socket的fd（连接描述符）指向的文件句柄大量处于close状态，导致server端不断地创建新的TCP连接，又由于短链接的问题导致了TIME_WAIT状态的TCP连接也大量激增；
	* Socket_used，TCP_alloc，TIME_WAIT，在监控面板中的波动趋势基本相同，因为大量新建的短链接，导致大量的socket都处于使用状态，短链接的断开又导致了大量的TIME_WAIT，但是又由于通过这些连接交付的数据无法快速写回响应，导致http超时断开，这里又导致了server内部处理错误code 500的日志输出；
* 情况的进一步恶化：
	* 当monitor_server 的 tornado web接收来自agent的大量请求时，由于接收agent数据以及处理数据和发送metric在同一条控制流中进行，这就导致tornado无法对创建的socket进行快速写回响应，又导致epoll无法实现连接的多路复用（复用连接写会对本地ng的响应），当本地nginx转发和server的listening端口，能创建的socket达到峰值时（因为端口数量有限65535，又由于一个socket是用{源ip} {源端口} {目的ip} {目的端口} 这个四元组来表示唯一性，所以socekt的创建有端口数量的限制，而且连接发起端占用的65535个端口要对应到30个listen端口上)，这就导致了健康检查发起的新的http请求无法写入socket（因为目的socket没有及时写回导致源端socket处于close，且无法新建TCP连接），这就导致了 看到的hc.do的接口没有任何反应（因为他的上下文在等待文件open的IO事件的调度），这就导致了ngnix自动移除了对当前server的转发；
    * nginx不断地移除server，只会导致问题更加恶化，因为agent端的数据请求不受后端server的影响，还在源源不断的进行发送；
    * 最终整个系统会一直处于一个nginx不断移除和加入server实例，且还是有持续大量http请求的超时、TCP新建、TIME_WAIT;
    * 此时后端的服务实例进入了恶性循环；



现存问题

登陆任意一台server
```bash
    netstat -npt | grep 127.0.0.1:51005   
        # agent到server的报文，使用了TCP短链接，经过二层转发后到达server；
        # 大量新创建的tcp连接和处于被动拆除状态LAST_ACK的连接
    netstat -ntp | grep 127.0.0.1 | grep 12057
        # 发送到回环地址的报文段，报文从server发送到nginx的12057端口，使用了TCP短连接，大量新创建的tcp连接和TIME_WAIT状态的连接
    netstat -npt | grep 127.0.0.1
        # OpenFalcon数据上报，使用了TCP短连接，大量新创建的tcp连接和TIME_WAIT状态的连接
    netstat -ntp | grep -E "127.0.0.1|127.0.0.1|127.0.0.1"
        # 发送到转存服务的报文段，使用了TCP短连接，大量新创建的tcp连接和TIME_WAIT状态的连接
```













