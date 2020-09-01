---
title: Python实现动态生成类的http接口-monitor动态监控项
author: Teddy
date: 2020-03-24 10:00:00 +0800
categories: [实践, 需求实现]
tags: [Python]
---

# 项目背景
* 采集厂商网络硬件设备基础指标，封装OpenFalcon数据结构
* 参与开发人数：1人

# 监控系统动态监控
* 需要实现的目标：
	* 数据库监控表项动态管理监控项数据处理、封装接口
	* 新增监控项由对于处理规则处理，项目的新监控项开发只需要编写规则函数和录入监控项字段即可

## 1. API 处理和报文解析
* 项目启动，导入文件后，解释器会执行 RouteRegister.registerAPI()
* 文件路经 `monitor/monitor-server/monitor/api/metric_api/dynamic_router_api.py`

1. 从数据库获取动态监控表项的字段
2. 根据获取回来的字段生成对于HTTP接口和类

* 此文件的执行入口是`RouteRegister.registerAPI()`，需要关注
	1. 使用了项目统一实现的 `@get_mapping` 装饰器，实现了RESTfulAPI的路经(路由)注册
	2. 因为python的type底层为c结构体，此处使用type函数，实现type的new，call，init方法，返回一个类的引用，且该引用会在装饰器中存储在全局的变量中，内存地址在可分配地址段，“堆”；
	3. 从数据库获取回来的数据保存在每个类的静态变量中
	4. tornado API 接收socket调用后，会执行process函数
	5. process函数实现原始数据处理的对象，并将从数据库表项获取的字段做初始化
	6. 调用DynamicMetricDataHandler的对象报文处理函数（此处http接收报文的载荷部分为json format）

* cpython source _typeobject `https://github.com/python/cpython/blob/master/Objects/typeobject.c`
```c
typedef struct _typeobject {
    int ob_refcnt;                        //引用计数
    struct _typeobject *ob_type;         // 类型对象
    int ob_size;                          //变长对象的长度，如len（list）， len(str), len(dict)，int类型没有该属性
    const char *tp_name; /* For printing, in format "<module>.<name>" */   // 变量的类型名字 如<class 'int'>    <class 'type'>
    Py_ssize_t tp_basicsize, tp_itemsize; /* For allocation */

    // .......
}
```

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2019-10-30 15:32
# @Author   : NAYAN
# @Site     : 
# @File     : snmp_metric_api_v2.py
# @Software : PyCharm

"""
DES:
    监控项目数据处理入口

    @API
    1. 从数据库t_snmp_task中全量拉取监控项
    2. 根据拉取得数据生成对应的数据上报API
    3. API关联到相应的数据处理函数
"""

MONITOR_ITEM_TB = "t_monitor_item"


from tornado import escape
from monitor.core.handlers import get_mapping, BaseHandler
from monitor.pkg.utils.logger import LOG
from monitor.core.metric.dynamic.dynamic import DynamicMetricDataHandler
from monitor.core.handlers.agent_error_handler import MetricErrorHandler
from monitor.db import api


class RouteRegister(object):

    metric_taks = {

    }

    @staticmethod
    def bindRouteToMetircDataHandler(__route, __des, monitor_item):
        """

        :param __route:
        :param __des:
        :param monitor_item:
        :return:
        """
        @get_mapping(__route, __des)
        class MonitorMetricAPI(BaseHandler):

            _metric = ""

            def process(self):
                """

                :return:
                """
                try:
                    body = self.request.body
                    content_type = self.request.headers.get("Content-Type", "")
                    if content_type.startswith('application/json'):
                        data = escape.json_decode(body)
                        try:
                            dynamic= DynamicMetricDataHandler(monitor_item=MonitorMetricAPI._metric)
                            did_send_metric = dynamic.handler_distributor(metric_raw=data)
                            if did_send_metric:
                                return 1, 'success', {}
                            else:
                                return 0, 'failed', {}
                        except Exception as e:
                            LOG.error("Dynamic metric data handler bind filed! error=%s" % (e))
                            return 0, 'failed', {}
                except Exception as e:
                    return 0, 'failed', {"Message": str(e)}

        if not monitor_item:
            return None
        MonitorMetricAPI._metric = monitor_item
        new_class_name = "".join([v[0].upper() + v[1:] for v in __route.split("/")[-1].split("_")])
        return type(new_class_name, (MonitorMetricAPI,), {})

    @staticmethod
    def registerAPI():
        raw_tasks = RouteRegister.loadAllAPIFromInventory()
        LOG.info("[Register Monitor Item API From DB...]")
        for raw in raw_tasks:
            if raw and raw.get('OpenFalcon_upload'): #
                __route = str(raw["upload_api"])
                __des = str(raw["desc"])
                LOG.info("[Upload API]: %s" % __route)
                RouteRegister.bindRouteToMetircDataHandler(__route, __des, raw)

    @staticmethod
    def loadAllAPIFromInventory():
        data = api.pg_query(MONITOR_ITEM_TB)
        LOG.info("[ITEM DATA] %s" % data)
        return data


@get_mapping('/monitor_upload/metric_error_handler.do', '')
class ErrorHandler(BaseHandler):
    def process(self):
        try:
            body = self.request.body
            content_type = self.request.headers.get("Content-Type", "")
            if content_type.startswith('application/json'):
                data = escape.json_decode(body)
                MetricErrorHandler.process_metric_error(data)
            return 1, 'success', {}
        except Exception as e:
            return 0, 'failed', {"Message": str(e)}

RouteRegister.registerAPI()

```


## 2. 规则映射数据处理

* 实现了对不同类型规则的处理逻辑；
1. 单OID处理：一个OID为采集对象，采集结果为单一类型数据，例如整型、浮点类型、字符、字符串、数组
2. 多OID处理：一个OID为采集对象，采集结果为多行数据，数据类型一致，例如带索引的分组交换机接口或硬件端口
3. 多OID多处理：多个OID为采集对象，采集结果可能为每个OID一个单一结果，或者每个OID多个结果，具体规则函数会对这样的报文做处理；


### 动态监控项表的字段结构

```pgsql
+-------------+---------------------+------+-----+---------+---------------------------------+
| Field       | Type                | Null | Key | description 	   							 |
+-------------+---------------------+------+-----+---------+---------------------------------+
| id  	      | varchar 			| NO   | PRI | 主键，唯一监控项名称，包含小写字母和下划线       |
| vendor      | varchar 			| NO   | 	 | 厂商								         |
| type        | varchar 			| NO   | 	 | 设备类型 （链路交换机，路由器，防火墙）         |
| model       | jsonb   			| YES  | 	 | 设备型号 厂商定义       			         |
| series      | jsonb               | YES  | 	 | 设备系列 厂商定义						     |
| metric 	  | varchar 			| NO   | 	 | 采集数据名称，元数据描述			 	         |
| metric_type | int4		        | NO   |     | 采集数据类型（处理） 0表示普通数据，1表示增量数据 |
| upload_api  | varchar 	        | NO   |     | 原始数据上报RESTful接口						 |
| task        | jsonb               | NO   |     | agent端执行的采集任务定义			         |
| desc        | varchar             | YES  | 	 | 描述								         |
| OpenFalcon_upload| bool                | NO   |     | 是否将数据发送到 OpenFalcon 平台			         |
| update_time | timestamp	        | NO   |     | 记录更新时间								 |
| interval    | int4                | YES  |     | agent执行采集的时间间隔				         |
+-------------+---------------------+------+-----+---------+---------------------------------+
```

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2019-10-31 14:57
# @Author   : NAYAN
# @Site     : 
# @File     : dynamic.py
# @Software : PyCharm

"""
动态监控项处理
    1. 从数据库t_monitor_item表拉取监控项
    2. 由监控项生成API和监控处理对象(class)
    3. 监控处理对象将调用相应的动态处理函数
    4. 动态处理函数会根据 task_operation 判断数据处理函数的类型，包括单数据处理，批量数据处理，表达式处理三种
    5. 监控数据部分会有两个处理函数，第一个是tags的配置，第二个是value的处理


"""

from monitor.core.handlers.device_info_handler import DeviceInfo
from monitor.pkg.utils.import_util import LOG
from monitor.core.model.monitor_data_model import MonitorItemDataModel
from monitor.core.model import monitor_data_model as DModle
from monitor.core.metric.dynamic.dynamic_rules import ValueRules
from monitor.core.metric.dynamic.dynamic_rules import TagRules
from monitor.core.metric.dynamic.dynamic_rules import OperationRules
from monitor.core.metric.publisher import Falcon

LogPrefix = "[Dynamic Monitor]"
DefaultValue = -1

Metric_Value_Type = {
    1: "int",
    0: "float",
    -1: "counter"
}

Metric_Type = {
    1: "GAUGE",
    0: "GAUGE",
    -1: "COUNTER"
}


class DynamicMetricDataHandler(object):
    """
    @metric_item
        监控项数据结构，用来生成监控项上报API和处理函数

    @metric_raw
        Agent上报的原始监控数据
    """

    def __init__(self, monitor_item=None):
        """

        :param monitor_item:
        """

        mon_object = MonitorItemDataModel(**monitor_item)

        self._mon_object = mon_object  # @监控对象
        self._vendor = mon_object.vendor  # @设备厂商
        self._type = mon_object.type  # @设备类型
        self._model = mon_object.model  # @设备型号
        self._series = mon_object.series  # @设备型号所属系列
        self._metric = mon_object.metric  # @监控项名称m
        self._metric_type = mon_object.metric_type  # @是否计数器
        self._upload_api = mon_object.upload_api  # @上报接口
        self._OpenFalcon_upload = mon_object.OpenFalcon_upload  # @是否上报OpenFalcon
        self._des = mon_object.description  # @监控项描述
        self._task = mon_object.task  # @监控项对应监控任务

        self.manage_ip = DModle.DEFAULT_STRING
        self.raw_data = DModle.DEFAULT_JSON_DIC
        self.timestamp = DModle.DEFAULT_INTEGER
        self.sysname = DModle.DEFAULT_STRING
        self.step = DModle.DEFAULT_INTEGER

        self.oid_data = {}

    def _parse_metric_raw(self, metric_raw):
        """
        @@@ Handle Agent upload original DATA
        :param metric_raw:
        @example:
        {
            "content": null,
            "host": null,
            "protocol": null,
            "scheduler": null,
            "timestamp": 1572574430,
            "company": null,
            "interval": null,
            "id": null,
            "response": {
                "get": {
                    "1.3.6.1.4.1.2636.3.1.13.1.8.9.1.0.0": {
                        "oid_index": "",
                        "oid": "enterprises.2636.3.1.13.1.8.9.1.0.0",
                        "snmp_type": "GAUGE",
                        "value": "1"
                    }
                }
            }
        }

        @@ Agent采集数据结构
            "content":  @采集job内容
            "host":     @采集对象管理ip
            "protocol": @采集使用的网络协议
            "scheduler": @采集是否为周期interval || once
            "timestamp": @采集数据的时间戳
            "company":   @采集设备的厂商
            "interval":  @采集的时间间隔
            "id":        @采集任务的唯一ID
        :return:
        """
        try:
            if not self._metric:  ##TODO Value Check and LOG IT!!!!!!!!!!!!!!!!!!!!!!!!
                LOG.error("%s metric item data parse failed, error=" % LogPrefix)
                return
            if not metric_raw:
                LOG.error("%s metric raw parse failed, error=" % LogPrefix)
                return

            self.manage_ip = metric_raw.get("host")
            self.raw_data = metric_raw.get("response")
            self.timestamp = metric_raw.get("timestamp")
            self.step = int(metric_raw.get("interval"))
            self.sysname = DeviceInfo.devs[self.manage_ip].get('sysname')
            # self.sysname = "abcd"
            if not self.sysname:
                raise Exception("get sysname failed!")
            return True
        except Exception as e:
            LOG.exception(self._error_handler(err_des="parse raw metric error", exp=e))
            return False

    def _error_handler(self, err_des="", exp=None):
        """
        @@@ Error handler
        :param e:
        :return: Error msg
        # LOG.error(self._error_handler(err_des="", exp=e))
        """
        e_msg = '%s monitor item data process error, device=[ip=%s, sysname=%s, vendor=%s, type=%s, model=%s, series=%s, metric=%s], err_msg=%s, exp=%s' \
                % (LogPrefix, self.manage_ip, self.sysname, self._vendor, self._type, self._model, self._series,
                   self._metric, err_des, exp)

        return e_msg

    def _is_value_valid(self, value):
        """
        @@@ SNMP error handler
            @TIMEOUT
            @UNKNOWN
            @NO_SUCH_INSTANCE
            @UNDETERMINED_TYPE_ERROR
            @Connection_Error
            @Undetermined_Type_Error
        :param value:
        :return:
        """
        if value or isinstance(value, (int, float)):
            return True
        elif isinstance(value, (str, unicode)):
            return True
            # TODO check snmp error value   TIMEOUT   UNKNOWN OBJECTID  NO_SUCH_INSTANCE   NO_SUCH_OBJECTID
            # except EasySNMPTimeoutError:
            # LOG.error("%s request snmp error TIMEOUT.oid=%s" % (self.hostname, oids))
            # except EasySNMPUnknownObjectIDError:
            # LOG.error("%s request snmp error UNKNOWN OBJECTID.oid=%s" % (self.hostname, oids))
            #
            # except (EasySNMPNoSuchObjectError, EasySNMPNoSuchInstanceError):
            # LOG.error("%s request snmp error NO_SUCH_INSTANCE OR NO_SUCH_OBJECTID.oid=%s" % (self.hostname, oids))
            #
            # except EasySNMPUndeterminedTypeError:
            # LOG.error("%s request snmp error UNDETERMINED_TYPE_ERROR.oid=%s" % (self.hostname, oids))
            # except EasySNMPConnectionError:
            # LOG.error("%s request snmp error Connection_Error.oid=%s" % (self.hostname, oids))
            # except EasySNMPUndeterminedTypeError:
            # LOG.error("%s request snmp error Undetermined_Type_Error.oid=%s" % (self.hostname, oids))
        else:
            return False

    def _process_value_rule(self, rule_name, **kwargs):
        """
        @@@ Matching the value process rule
        :param rule_name:
        :param kwargs:
        :return:
        """
        ## ToDO NO SUCN rule

        r = ValueRules()
        func = getattr(r, rule_name)
        return func(manage_ip=self.manage_ip, **kwargs)

    def _process_tag_rule(self, rule_name, **kwargs):
        """
        @@@ Tags handler
            @ Tags get attr from raw content
        :param tags:
        :return:
        """
        r = TagRules()
        func = getattr(r, rule_name)
        return func(manage_ip=self.manage_ip, **kwargs)

    def _process_opera_rule(self, rule_name, **kwargs):
        """
        @@@ Matching the operation process rule
        :param rule_name:
        :param kwargs:
        :return:
        """
        r = OperationRules()
        func = getattr(r, rule_name)
        return func(manage_ip=self.manage_ip, **kwargs)

    def _raw_data_wrapper(self):
        """
        :wrapper: wrap raw data to a dic, oid as key
        :return:
        {
            "1.3.6.1.4.1.2636.3.1.13.1.8.9.1.0.0": [
                {
                    "oid_index": "",
                    "oid": "enterprises.2636.3.1.13.1.8.9.1.0.0",
                    "snmp_type": "GAUGE",
                    "value": "1"
                }...
            ],
            ""1.3.6.1.4.1.2636.3.1.13.1.8.9.1.0.1": [
                {
                    "oid_index": "",
                    "oid": "enterprises.2636.3.1.13.1.8.9.1.0.1",
                    "snmp_type": "GAUGE",
                    "value": "1"
                }...
            ]...
        }
        """
        oid_data = {}
        for method, oid_dic in self.raw_data.items():
            for oid, oid_value in oid_dic.items():
                if not isinstance(oid_value, (list)):
                    oid_value = [oid_value]
                oid_data.update({oid: oid_value})
        self.oid_data = oid_data

    def handler_distributor(self, metric_raw=None):
        """
        @self._task
        {
            "snmp_task":{
                "oid": {
                    'get': [],
                    'bulk': [],
                    'walk': [],
                    'getnext': []
                },
                "value_rule": "",
                "tag_rule": "",
                "opera_rule": ""
            }
        }
        @@@ Rules
        :rule:三种采集数据处理规则，规则都在task_content中
        1. value_rule           值处理规则，对上报数值进行处理，比如从字符串中截取监控指标
        2. tag_rule             标签处理规则，如对根据接口索引获取接口速率和名称并添加到上报tags中
        3. opera_rule           运算操作规则，对多个oid取回值进行运算处理获取监控指标，比如对metric_raw中的值进行加减乘除

        @@@ Handlers
        :handler: 三种OID处理规则
        1. snmp_single          单值处理，task中只有一个操作方法和一个oid，采集结果也只有单一值(例如：get操作单一oid)
        2. snmp_batch           批量处理，task中只有一个操作方法和一个oid，采集结果会有索引(例如：walk操作单一oid)
        3. snmp_multi           多值处理，task中有多个操作方法或多个oid，采集结果会有多种值或多种索引(例如：风别walk操作三个oid)

        :param metric_raw:
        :return:
            @@True      数据处理成功发送OpenFalcon
            @@False     数据处理失败写入日志
        """

        try:
            did_parse_data = self._parse_metric_raw(metric_raw)
            if not did_parse_data:
                return False
            if not self._task:
                LOG.error(self._error_handler(err_des="monitor item task empty"))
                return False
            # @ task handler caller
            for task_type, task_content in self._task.iteritems():

                # @SNMP task
                if task_type == "snmp_task":

                    self._raw_data_wrapper()

                    if len(self.oid_data.values()):
                        # 多oid多值
                        if len(self.oid_data) > 1:
                            return self.snmp_multi_monitor_item_handler(task_content)
                        # 单oid多值
                        if len(self.oid_data.values()[0]) > 1:
                            return self.snmp_batch_monitor_item_handler(task_content)
                        else:
                            return self.snmp_single_monitor_item_handler(task_content)

                # @Netconf task
                elif task_type == "netconf_task":
                    pass
                else:
                    LOG.error("%s monitor task type not supported!" % LogPrefix)
        except Exception as e:
            LOG.exception(self._error_handler(exp=e))

    def snmp_single_monitor_item_handler(self, task_content):
        """

        :param metric_raw:
        @metric_raw["response"]
        "response": {
                "get": {
                    "1.3.6.1.4.1.2636.3.1.13.1.8.9.1.0.0": {
                        "oid_index": "",
                        "oid": "enterprises.2636.3.1.13.1.8.9.1.0.0",
                        "snmp_type": "GAUGE",
                        "value": "1"
                    }
                }
            }
        :return: Bool
        """
        task_value_rule = task_content.get("value_rule")
        task_tag_rule = task_content.get("tag_rule")

        try:
            if len(self.raw_data) > 1 or len(self.raw_data.values()) > 1:
                raise Exception("upload data is not single value")
            else:
                oid_dic = self.raw_data.values()[0]
                oid_content_dic = oid_dic.values()[0]

                if isinstance(oid_content_dic, dict):
                    value = oid_content_dic.get("value")
                elif isinstance(oid_content_dic, list) and len(oid_content_dic) > 0:
                    value = oid_content_dic[0].get("value")
                    oid_content_dic = oid_content_dic[0]
                else:
                    value = None
                tags = None

                if value and self._is_value_valid(value):

                    # process rules
                    # 1. value rule
                    if task_value_rule:
                        value = self._process_value_rule(task_value_rule, value=value, sysname=self.sysname)

                    # 2. tag rule
                    if task_tag_rule:
                        tags = self._process_tag_rule(task_tag_rule, oid_content=oid_content_dic)

                    return self.metrics_sender(value, tags)
                else:
                    return False
        except Exception as e:
            LOG.exception(self._error_handler(err_des="single value process failed", exp=e))

    def snmp_batch_monitor_item_handler(self, task_content):
        """
        :rule:三个处理规则，规则都在task_content中
        1. value_rule           值处理规则，对上报数值进行处理，比如从字符串中截取监控指标
        2. tag_rule             标签处理规则，如对根据接口索引获取接口速率和名称并添加到上报tags中
        3. operation_rule       运算操作规则，对多个oid取回值进行运算处理获取监控指标，比如对metric_raw中的值进行加减乘除

        @@ 基于metric索引批量处理监控数据
        :param metric_raw:
        @example
        @metric_raw["response"]
        "response": {
            "walk": {
                "1.3.6.1.2.1.2.2.1.14": [
                    {
                        "oid_index": "1",
                        "oid": "ifInErrors",
                        "value": "0",
                        "snmp_type": "COUNTER"
                    },
                    {
                        "oid_index": "4",
                        "oid": "ifInErrors",
                        "value": "0",
                        "snmp_type": "COUNTER"
                    },
                    {
                        "oid_index": "5",
                        "oid": "ifInErrors",
                        "value": "0",
                        "snmp_type": "COUNTER"
                    }
                ]
            }
        }
        :param task_content:
        :return:
        """

        task_value_rule = task_content.get("value_rule")
        task_tag_rule = task_content.get("tag_rule")

        try:
            if len(self.raw_data) > 1:
                raise Exception("upload data format error")
            else:
                oid_dic = self.raw_data.values()[0]
                oid_content_list = oid_dic.values()[0]

                ret_res = []
                for oid_content_dic in oid_content_list:
                    if isinstance(oid_content_dic, dict):
                        value = oid_content_dic.get("value")
                        if value == "2147483647":
                            value = "0"
                        tags = "index={}".format(oid_content_dic.get("oid_index"))
                        if value and self._is_value_valid(value):
                            # process rules
                            # 1. value rule
                            if task_value_rule:
                                value = self._process_value_rule(task_value_rule, value=value, sysname=self.sysname)
                            # 2. tag rule
                            if task_tag_rule:
                                tags = self._process_tag_rule(task_tag_rule, oid_content=oid_content_dic)
                            if not tags:
                                continue
                            res = self.metrics_sender(value, tags)
                            ret_res.append(res)
                  
                if False in ret_res or len(ret_res) == 0:
                    return False
                else:
                    return True
        except Exception as e:
            LOG.exception(self._error_handler(err_des="batch value process failed", exp=e))

    def snmp_multi_monitor_item_handler(self, task_content):
        """

        :param metric_raw:
        @example
        @metric_raw["response"]
        "response": {
            "walk": {
                "1.3.6.1.2.1.2.2.1.14": [
                    {
                        "oid_index": "1",
                        "oid": "ifInErrors",
                        "value": "0",
                        "snmp_type": "COUNTER"
                    }...
                ],
                ""1.3.6.1.2.1.2.2.1.15": [
                    {
                        "oid_index": "1",
                        "oid": "",
                        "value": "0",
                        "snmp_type": "COUNTER"
                    }...
                ], ...
            }
        }
        :param task_content:
        :return:
            [{"value": "", "tags": ""}, {"value": "", "tags": ""}, ...]
        """

        task_opera_rule = task_content.get("opera_rule")

        try:
            if task_opera_rule:
                result = self._process_opera_rule(task_opera_rule, raw_data=self.raw_data.values()[0])
                #LOG.debug("multi task name=" + task_opera_rule + ",result metric length=" + str(len(result)))
                did_send = False
                for v in result:
                    did_send = self.metrics_sender(v["value"], v["tags"])
                return did_send
            return False

        except Exception as e:
            LOG.exception(self._error_handler(err_des="get multi value process failed", exp=e))

    def metrics_sender(self, value, tags):
        """

        @@Tags
            1. 检查tag字段，如果有值则调用 _match_tags_handler
            2. 如果为空，侧检查index_tag是否有值
            3. 如果有值，侧使用tags="%s/%s" %(index_tag, index)
            4. 如果为空，侧无tags

        :param metric:
        :param title:
        :return:
        """
        __OpenFalcon_metric_type = Metric_Type[self._metric_type]
        __v_type = Metric_Value_Type[self._metric_type]

        if __v_type == "float":
            value = float(value)
        else:
            value = int(value)
        try:
            m = {
                "endpoint": self.sysname,
                "metric": self._metric,
                "timestamp": self.timestamp,
                "step": self.step,
                "value": value,
                "counterType": __OpenFalcon_metric_type,
                "tags": tags
            }
            # LOG.info("[DEBUG Send] %s" % m)
            Falcon.send([m])
        except Exception as e:
            LOG.exception("parser OpenFalcon metric failed, e=%s" % e)
        return True

    @staticmethod
    def common_data_handler(func):
        """

        :param func:
        :return:
        """

        def monitor_wrapper(*args, **kwargs):
            """

            :param args:
            :param kwargs:
            :return:
            """
            try:
                value = func(*args, **kwargs)
                data_dic = dict()
                data_dic["type"] = args[1]
                value = value if value else -1
                data_dic["val"] = value if isinstance(value, (float, int)) else int(value)
                return data_dic
            except Exception as e:
                LOG.exception('get error, e=%s' % e)
                raise e

        return monitor_wrapper

```

## 3. 执行任务和处理规则

* agent所要执行的任务定义和处理规则定义

```python
 MonitorTaskJsonDic = {
        "snmp_task": {              #@SNMP采集任务
            "oid": {                #@采集OID和执行方式-同步到job.content中并关联设备
                'get': [],
                'bulk': [],
                'walk': [],
                'getnext': []
            },
            "tag_rule": "",        #@数标签处理规则
            "opera_rule": "",       #@多数据处理规则
            "value_rule": ""        #@采集值处理规则-如：从字符串中匹配整形并转为百分比
        }
    }
```

* 此处定义一个snmp_task，agent根据此task来执行采集和上报数据
* 规则处理函数会接收 agent采集返回报文的json对象的 response 部分
``` json
"response": {
            "walk": {
                "1.3.6.1.2.1.2.2.1.14": [
                    {
                        "oid_index": "1",
                        "oid": "ifInErrors",
                        "value": "0",
                        "snmp_type": "COUNTER"
                    },
                    {
                        "oid_index": "4",
                        "oid": "ifInErrors",
                        "value": "0",
                        "snmp_type": "COUNTER"
                    },
                    {
                        "oid_index": "5",
                        "oid": "ifInErrors",
                        "value": "0",
                        "snmp_type": "COUNTER"
                    }
                ]
            }
        }
```

* 规则定义
1. 在task中定义tag_rule, value_rule, opera_rule，处理函数会自动将数据和处理规则进行动态匹配，当有新报文段交付后，会触发对应的规则函数；
2. 规则匹配顺序为：ValueRules， TagRules， OperationRules
3. 规则选用建议
	1. 如果采集结果为单一结果，例如"value": "35"，使用ValueRules，将该字符串进行处理，比如"35%",或0.35；
	2. 如果采集结果携带索引，对其值的处理结果可以参考1，对索引值可以使用TagRules，将索引处理为特定的标签，标识一条唯一的数据，并且该标签还可以携带其他和数据相关的属性；
	3. 对于多种采集OID对象和多种结果的类型，只使用自定义的OperationRules
	> 部分ValueRules，TagRules可以对数据做通用处理
```python
class ValueRules(object):
class TagRules(object):
class OperationRules(object):
```

## 4. 新监控项开发

* 如何添加一个新的监控项 （测试环境）
1. 添加数据记录到动态监控表，根据每个字段名称定义相应的字段；
	* vendor，type，model，series 设备相关，用来定义那些厂商哪些类型哪些型号的设备要”被agent执行新增的监控项任务“
	* id，metric，metric_type，upload_api，用来定义一个唯一的监控项，和监控项在dashboard和rrd数据库中的名称，且包含唯一一个为此监控项创建的上传RESTful接口
	* task 定义采集任务，agent执行什么样的任务；定义处理规则，采集回来的数据要被映射到哪些自定义的规则函数上
	* interval agent对设备多久进行一次采集，”UDP“报文段交互

2. 数据都定义完成后，编写你的规则函数
	* 函数名称要和task中定义的函数名称一致
	* 函数所属要的类，要和task中给定的一致
	* 函数入参固定
		* ValueRules 	  manage_ip=None, value=None, sysname=None
		* TagRules 		  manage_ip=None, oid_content=None
		* OperationRules  manage_ip=None, raw_data=None
	* 处理逻辑，manage_ip为设备在各自AS的子网中的管理IP地址，采集回来的数据为其他参数
		* value 		采集唯一值
		* sysname  		设备名称
		* oidcontent 	python列表类型，列表中包含多个采集结果字典，例如
		```python
		[
                    {
                        "oid_index": "1",
                        "oid": "ifInErrors",
                        "value": "0",
                        "snmp_type": "COUNTER"
                    },
                    {
                        "oid_index": "4",
                        "oid": "ifInErrors",
                        "value": "0",
                        "snmp_type": "COUNTER"
                    },
                    {
                        "oid_index": "5",
                        "oid": "ifInErrors",
                        "value": "0",
                        "snmp_type": "COUNTER"
                    }
                ]
		```
		* raw_data 		报文中json对象的response部分的全部数据

	* 处理规则的返回值
		* ValueRules 		返回处理后的value
		* TagsRules		    返回固定格式的Tags字符串，字符串中的标签字符用"="和","分隔
		* OperationRules    返回处理完成后的所有数据的列表，列表中为相同结构的字典 包含"value"和"tags"，例如
		```python
		[{"value": , "tags"},{"value": , "tags"},{"value": , "tags"}]
		```
		> 其中tags格式依然固定，value可以是整型或者浮点类型

3. 完成规则函数编写后，数据上报部分有独立线程来自动完成，无需关注；

## 5. 调试

* agent和server的调试，请移步单元测试文档



