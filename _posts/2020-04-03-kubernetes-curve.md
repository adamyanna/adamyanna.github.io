---
title: Kubernetes & Docker
author: Teddy
date: 2020-04-10 10:00:00 +0800
categories: [体系结构-应用, 容器]
tags: [TODO, Kubernetes, Docker]
---


# Kubernetes & Docker

https://kubernetes.io/

* Kubernetes is  an open-source system for automating deployment, scaling, and management of containerized applications;
* kubernetes components architecture

![](/Users/teddyna/Develop/dev/teddygoodman.github.io/img/components-of-kubernetes.png)

* 控制面

  * 控制平面，用来对整个集群作出决策，并监测和响应集群产生的事件；
  * 控制平面的组件可以运行再一台或者多台机器上，默认的部署脚本，提供所有控制平面的组件部署并运行在同一台机器上，并且不会将用户创建的容器或者pod服务创建在已经部署了控制组件的机器上；

* 各个组件的简单介绍及功能

  * kube-apiserver

    * **kube API服务器是整个控制平面前端**，将kubernetes的API接口提供给外部进行访问；
    * 该服务提供横向的伸缩和扩容，通过在更多机器实例上部署kube-apiserver，来提供接口对外访问的负载均衡，当然这里的负载均衡需要其他组件参与，例如双结点的LVS+Nginx做负载均衡转发，并将外部访问的报文段转发到不同权重的API服务节点上；

  * etcd

    * [etcd.io](https://etcd.io/)
    * 分布式且高可用的 key-value 存储系统，用来对分布式系统的关键及重要数据做持久化；
    * 在kubernetes架构中，用于对kubernetes产生的集群数据做持久化；
    * etcd提供高可用，kubernetes后端的集群数据的持久化存储对应生产环境来说，还需要更多的数据备份方式；

  * kube-scheduler

    * kubernetes管理的微服务的最小单位是一个Pod
    * 类似于Openstack的Nova的scheduler对新建虚拟机的调度，kube-scheduler对新创建的Pod进行调度，用来选择一个适合的节点来运行该Pod；
    * 这里的适合的节点取决于多个**因素**
      * 单一的组合的资源需求
      * 硬件/软件/策略的约束
      * 亲和力/反亲和力 的规格 ？
      * 数据的局部性
      * 内部任务之间的影响和干扰
      * 截止日期

  * Kube-controller-manager

    * 控制平面的控制器，单独的进程运行控制器/管理者

    * 该控制器进程的源程序中包含多个**“功能独立”**的控制器，kubernetes为了进一步简化复杂性，将这些功能独立的控制器编译到同一个可运行指令的二进制文件；

    * 该进程中包括的**”功能独立“**的控制器：

      * Node Controller：负责对节点的异常（节点服务崩溃）进行事件回调和响应；

      * Replication Controller：负载管理和维护Pod的个数，这些Pod用来承载系统中复制控制器的对象（也就是复制的服务）？；

      * Endpoint Controller：负责将Endpoint对象，加入到一个指定的服务或者Pod中；

      * Service Account & Token Controllers：管理和创建用于API访问的用户，和用户Token，这些Token用不同的命名空间进行区分；

        > 命名空间的概念，一个命名空间用来声明一个区域或者范围，该范围内包含该命名空间独一无二的身份验证或者程序变量、方法等；

  * cloud-controller-manager

    * 云控制器，用来和底层云环境进行交互；

    * 运行 cloud-provider-specific 控制器循环，在启动前，必须disable不适用的controller loops；

      > --cloud-provider = external
      >
      > 当前版本的kubernetes核心代码对”云服务提供商“的代码在功能上有所依赖；
      >
      > 未来版本中，”云服务提供商“将自己管理云厂商的代码段，在运行kubernetes期间和 cloud-controller-manager 进行链接；

    * 对于云提供商的代码有所依赖的控制器包括：

      * Node Controller
        *  通过云供应商来检查已经停止的节点，是否在环境中已经被释放；
      * Route Controller
        *  为底层基础设施配置路由
      * Service Controller
        * 用来创建、更新、删除、云供应商提供的负载均衡产品
      * Volume Controller
        * 用来创建、附加、挂在”卷“，和云提供商交互进行”卷“的编排；

* Node Components

  * 节点组件，运行在kubernetes集群的每一个节点上，**用来维护运行的Pods并为Kubernetes提供运行时环境**
  * Kubelet
    * 运行在集群中的每个节点上的agent，用于确保容器运行在Pod中；
    * 

