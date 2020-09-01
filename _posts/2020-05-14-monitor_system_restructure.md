---
title: 监控系统1.5版本项目重组
author: Teddy
date: 2020-05-14 14:52:45 +0800
categories: [实践, 需求实现]
tags: [Monitor-System]
---

# 监控系统1.5版本项目重组

* 采集数据处理接口添加逻辑：
 
```python
"""
DES:
 监控项目数据处理入口
 
 @API
 API = {
 "/monitor_upload/snmp/": MonitorUploadAPI,
 }
 Key: 父级路由
 Value: 父级路由对应的子路由
 
 @MonitorUploadAPI
 MonitorUploadAPI = {
 "xxx": {"metric": "x.xx", "handler": metric.xx.xxx}
 }
 Key: 子路由
 Value: 监控项及处理函数
 metric: 监控项名称
 handler: 数据处理函数, 处理函数如参必须包含： metric 和 data
"""
```


```sh
├── monitor
│   ├── api                                            │ API管理
│   │   ├── OpenFalcon_access_api                           │ 与OpenFalcon进行交互的API, 告警联系组管理, 告警模版管理, 告警名称翻译, 告警联系人组管理, 采集数据查询, 告警解除及屏蔽, 告警视图查询
│   │   ├── monitor_manage_api                        │ 对monitor采集系统进行管理的API, 承载对monitor-pg的访问, 包括监控agent增删改查, 包括监控设备增删改查, 包括监控任务增删改查
│   │   ├── metric_process_api                         │ Agent原始采集数据上报API, 包括各厂商的netconf协议下的数据上报，API以.do结尾, 包括各厂商的snmp协议下的数据上报，API以.do结尾
│   │   └── third_access_api                           │ 第三方系统管理API, 包括zabbix线路添加相关API
│   ├── conf                                           │ 配置文件, 配置项注册
│   ├── core                                           │ 监控数据处理核心
│   │   ├── OpenFalcon                                      │ 核心OpenFalcon访问模块, 告警核心配置功能，接收OpenFalcon_access_api调用
│   │   ├── handlers                                   │ 核心处理模块, 包括设备信息缓存加载功能，server服务启动前预加载数据到缓存，并定时更新，由metric数据处理单元调用
│   │   ├── metric                                     │ 监控metric数据处理模块, 原始采集数据基础处理模块，由.do数据接收API直接调用，或由vendor protocol数据处理模块基础
│   │   │   ├── vendor                                 │ 设备类采集任务的原始采集数据处理模块
│   │   │   └── wrapper                                │ Falcon数据封装模块
│   │   └── model                                      │ 数据模型, OpenFalcon数据模型, monitor数据模型
│   ├── db                                             │ db访问模块
│   ├── inventory                                      │ 监控OID，监控项管理仓库
│   ├── pkg                                            │ 功能模块管理
│   │   ├── amqp                                       │ amqp模块，包括rabbitmq生成和消费
│   │   ├── redis                                      │ redis模块，包括redis写入和读取
│   │   ├── security                                   │ 数据加密模块
│   │   └── utils                                      │ 工具组件模块
│   ├── run_agent_manager.py                           │ 运行入口：agent状态检查设备分配服务
│   ├── run_cmdb_manager.py                            │ 运行入口：CMDB设备监控同步服务
│   ├── run_server.py                                  │ 运行入口：Web Server服务
│   ├── run_service_debug.py                           │ 运行入口：所有服务debug
│   ├── run_task_scheduler.py                          │ 运行入口：其他同步服务的统一入口
│   └── service                                        │ 定时同步服务管理模块
│       ├── alarm_sync_service.py                      │ 告警翻译同步服务
│       ├── cmdb_sync_service.py                       │ CMDB设备监控同步服务
│       ├── device_distribution_service.py             │ agent状态检查设备分配服务
│       ├── device_manager_service.py                  │ 设备基础信息管理服务
│       ├── monitor_oper_service.py                    │ 监控设备同步服务，移除下线设备等
│       └── monitor_task_service.py                    │ Agent执行任务生成及同步服务
├── docs                                               │ 文档

Project Structure:
 
 
├── monitor
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── OpenFalcon_access_api                           │ 与OpenFalcon进行交互的API
│   │   │   ├── __init__.py                            │
│   │   │   ├── alarm_group_manage_api.py              │ 告警联系组管理
│   │   │   ├── alarm_manage_api.py                    │
│   │   │   ├── alarm_template_manage_api.py           │ 告警模版管理, 告警名称翻译
│   │   │   ├── alarm_user_manage_api.py               │ 告警联系人组管理
│   │   │   ├── const.py                               │
│   │   │   └── falcon_handler_api.py                  │ 采集数据查询, 告警解除及屏蔽, 告警视图查询
│   │   ├── monitor_manage_api                        │ 对monitor采集系统进行管理的API, 承载对monitor-pg的访问
│   │   │   ├── __init__.py                            │
│   │   │   ├── agent_manage_api.py                    │ 包括监控agent增删改查
│   │   │   ├── device_manage_api.py                   │ 包括监控设备增删改查
│   │   │   └── task_manage_api.py                     │ 包括监控任务增删改查
│   │   ├── metric_process_api                         │ Agent原始采集数据上报API
│   │   │   ├── __init__.py                            │
│   │   │   ├── netconf_metric_api.py                  │ 包括各厂商的netconf协议下的数据上报，API以.do结尾
│   │   │   └── snmp_metric_api.py                     │ 包括各厂商的snmp协议下的数据上报，API以.do结尾
│   │   └── third_access_api                           │ 第三方系统管理API
│   │       ├── __init__.py                            │
│   │       └── zabbix_manage_api.py                   │ 包括zabbix线路添加相关API
│   ├── conf                                           │ 配置文件
│   │   ├── __init__.py                                │ 配置项注册
│   │   ├── conf.ini                                   │ 内部云配置文件
│   │   ├── conf_debug.ini                             │ 测试环境配置文件
│   │   ├── conf_efa.ini                               │ 金融云配置文件
│   │   ├── conf_pub.ini                               │ 公有云配置文件
│   ├── core                                           │ 监控数据处理核心
│   │   ├── __init__.py                                │
│   │   ├── OpenFalcon                                      │ 核心OpenFalcon访问模块
│   │   │   ├── __init__.py                            │
│   │   │   ├── alarm_setting.py                       │ 告警核心配置功能，接收OpenFalcon_access_api调用
│   │   ├── handlers                                   │ 核心处理模块
│   │   │   ├── __init__.py                            │
│   │   │   ├── device_info_handler.py                 │ 包括设备信息缓存加载功能，server服务启动前预加载数据到缓存，并定时更新，由metric数据处理单元调用
│   │   ├── metric                                     │ 监控metric数据处理模块
│   │   │   ├── __init__.py                            │
│   │   │   ├── base.py                                │ 原始采集数据基础处理模块，由.do数据接收API直接调用，或由vendor protocol数据处理模块基础
│   │   │   ├── driver                                 │
│   │   │   │   ├── __init__.py                        │
│   │   │   │   ├── cisco_firewall.py                  │
│   │   │   │   ├── cisco_router.py                    │
│   │   │   │   ├── cisco_switch.py                    │
│   │   │   │   ├── h3c_switch.py                      │
│   │   │   │   ├── huawei_switch.py                   │
│   │   │   │   └── juniper_firewall.py                │
│   │   │   ├── protocol                               │ 协议类采集任务的原始采集数据处理模块，该任务为用户自定义任务
│   │   │   │   ├── __init__.py                        │
│   │   │   │   ├── http.py                            │ http协议任务原始采集数据处理模块
│   │   │   │   ├── ping.py                            │ ping监控任务原始采集数据处理模块
│   │   │   │   ├── process.py                         │ 进程监控任务原始采集数据处理模块
│   │   │   │   ├── snmp.py                            │ snmp协议任务原始采集数据处理模块
│   │   │   │   └── tcp.py                             │ tcp协议任务原始采集数据处理模块
│   │   │   ├── publisher.py                           │ 已完成封装的Falcon数据推送模块，包括对OpenFalcon的http上报和rabbitmq的发布
│   │   │   ├── vendor                                 │ 设备类采集任务的原始采集数据处理模块
│   │   │   │   ├── __init__.py                        │
│   │   │   │   ├── cisco.py                           │ cisco 思科原始采集数据处理模块
│   │   │   │   ├── f5.py                              │ f5 原始采集数据处理模块
│   │   │   │   ├── h3c.py                             │ h3c 华三原始采集数据处理模块
│   │   │   │   ├── hillstone.py                       │ hillstone 山石原始采集数据处理模块
│   │   │   │   ├── huawei.py                          │ huawei 华为原始采集数据处理模块
│   │   │   │   ├── infoblox.py                        │ infoblox 原始采集数据处理模块
│   │   │   │   ├── juniper.py                         │ juniper 原始采集数据处理模块
│   │   │   │   ├── nexus.py                           │ nexus 原始采集数据处理模块
│   │   │   │   └── riverbed.py                        │ riverbed 原始采集数据处理模块
│   │   │   └── wrapper                                │ Falcon数据封装模块
│   │   │       ├── __init__.py                        │
│   │   │       ├── common_metric.py                   │ 通用数据封装模块
│   │   │       ├── interface_metric.py                │ 设备子接口数据封装模块
│   │   │       ├── protocol_metric.py                 │ 协议类数据封装模块
│   │   │       └── vendor_wrapper                     │ 厂商设备数据封装模块
│   │   │           ├── __init__.py                    │
│   │   │           ├── cisco_metric.py                │ cisco 设备数据封装模块
│   │   │           ├── f5_metric.py                   │ f5 设备数据封装模块
│   │   │           ├── h3c_metric.py                  │ h3c 设备数据封装模块
│   │   │           ├── hillstone_metric.py            │ hillstone 设备数据封装模块
│   │   │           ├── huawei_metric.py               │ huawei 设备数据封装模块
│   │   │           ├── infoblox_metric.py             │ infoblox 设备数据封装模块
│   │   │           ├── juniper_metric.py              │ juniper 设备数据封装模块
│   │   │           ├── nexus_metric.py                │ nexus 设备数据封装模块
│   │   │           └── riverbed_metric.py             │ riverbed 设备数据封装模块
│   │   └── model                                      │ 数据模型
│   │       ├── __init__.py                            │
│   │       ├── OpenFalcon_data_model.py                    │ OpenFalcon数据模型
│   │       └── monitorf_data_model.py                 │ monitor数据模型
│   ├── db                                             │ db访问模块
│   │   ├── __init__.py                                │ db访问API，包括增删改查及合并
│   │   ├── api.py                                     │
│   │   ├── device_manager_dao.py                      │
│   │   ├── device_topo_dao.py                         │
│   │   ├── monitor_data_dao.py                        │
│   │   ├── monitor_oper_dao.py                        │
│   │   ├── monitor_task_dao.py                        │
│   │   └── monitor_user_view_dao.py                   │
│   ├── inventory                                      │ 监控OID，监控项管理仓库
│   │   ├── __init__.py                                │
│   │   ├── cisico_snmp.json                           │
│   │   ├── huawei_snmp.json                           │
│   │   ├── NetconfRule.py                             │
│   │   ├── SnmpRule.py                                │
│   │   └── TaskSupported.py                           │
│   ├── pkg                                            │ 功能模块管理
│   │   ├── __init__.py                                │
│   │   ├── amqp                                       │ amqp模块，包括rabbitmq生成和消费
│   │   │   ├── __init__.py                            │
│   │   │   ├── const.py                               │
│   │   │   ├── metric_publisher.py                    │
│   │   │   ├── pika_util.py                           │
│   │   ├── redis                                      │ redis模块，包括redis写入和读取
│   │   │   ├── __init__.py                            │
│   │   │   ├── redis.py                               │
│   │   ├── security                                   │ 数据加密模块
│   │   │   ├── __init__.py                            │
│   │   │   ├── key                                    │
│   │   │   │   ├── rsa.key                            │
│   │   │   │   └── rsa.pub                            │
│   │   │   └── rsa_secure.py                          │
│   │   └── utils                                      │ 工具组件模块
│   │       ├── __init__.py                            │
│   │       ├── async.py                               │
│   │       ├── daemon.py                              │
│   │       ├── date_util.py                           │
│   │       ├── encrypt_util.py                        │
│   │       ├── file_util.py                           │
│   │       ├── flow_util.py                           │
│   │       ├── global_variable.py                     │
│   │       ├── http_util.py                           │
│   │       ├── import_util.py                         │
│   │       ├── lock_util.py                           │
│   │       ├── logger.py                              │
│   │       ├── os_util.py                             │
│   │       ├── request_util.py                        │
│   │       ├── result.py                              │
│   │       ├── temp.py                                │
│   │       ├── temp.txt                               │
│   │       ├── temp2.py                               │
│   │       ├── thread_helper.py                       │
│   │       ├── time_helper.py                         │
│   ├── run_agent_manager.py                           │ 运行入口：agent状态检查设备分配服务
│   ├── run_cmdb_manager.py                            │ 运行入口：CMDB设备监控同步服务
│   ├── run_server.py                                  │ 运行入口：Web Server服务
│   ├── run_service_debug.py                           │ 运行入口：所有服务debug
│   ├── run_task_scheduler.py                          │ 运行入口：其他同步服务的统一入口
│   └── service                                        │ 定时同步服务管理模块
│       ├── __init__.py                                │
│       ├── alarm_sync_service.py                      │ 告警翻译同步服务
│       ├── cmdb_sync_service.py                       │ CMDB设备监控同步服务
│       ├── device_distribution_service.py             │ agent状态检查设备分配服务
│       ├── device_manager_service.py                  │ 设备基础信息管理服务
│       ├── monitor_oper_service.py                    │ 监控设备同步服务，移除下线设备等
│       └── monitor_task_service.py                    │ Agent执行任务生成及同步服务
├── docs                                               │
│   ├── api_docs                                       │
│   │   └── restful_api.yml                            │
│   └── README.md                                      │
├── etc                                                │
│   └── bin                                            │
│       ├── monitor-log.service                       │
│       ├── monitor-monitor.service                   │
│       ├── monitor-scheduler.service                 │
│       └── monitor-server.service                    │
├── README                                             │
```
