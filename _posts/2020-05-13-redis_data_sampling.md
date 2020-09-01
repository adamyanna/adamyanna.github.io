---
title: Data Sampling [Redis]
author: Teddy
date: 2020-05-13 14:54:35 +0800
categories: [实践, 需求实现]
tags: [Go, Redis, Data-Sampling]
---

# 监控覆盖率检查和数据完整性检查【2020-4】

## 方案一，单节点

## 方案二，可横向扩展集群

![]({{ "/assets/img/posts/redis_data_sampling_1.png" | relative_url }})

### 方案：
monitor-torrent负责与redis保持连接，对应key更新当前数据value和最新的timestamp及count进行++，数据模型为
key = {endpoint} + {metric} + {tag}  注：遇到key中tag过长可以进行一定的压缩处理
value 为redis-list 值都为redis-integer
1) {value}
2) {timestamp}
3) {count}
monitor-patrol
1.	多个实例的情况下，需要考虑如何读取redis中的数据，如何触发读取；
a.	问题点
i.	读取过程的耗时问题
ii.	读取数据如何平均分配到多个节点
2.	 单个实例的情况下，如何快速的读取是比较严重的问题

所有对于数据断点的检查本身还是需要将数据保存在本机内存中，但是需要实现的双机的高可用，可以利用redis做监控覆盖检查；
对于数据的检查方式
1.	固定时段内计点
2.	每个map数据中的timestamp相见
利用redis完全可以实现第二点，但是第一种方式对于数据的完全丢失有监测作用，使用redis必然要考虑分布式锁；

问题的本质：
    断点监测的本质，就是在一个超大的哈希表中更新并检查当前一段时间的count值，对于这个检查的单个过程的执行指令并不多且不复杂，但是每次的检查涉及到哈希表的更新和协程的中断和上下文切换，线程安全和大量的上下文切换是需要考虑的主机计算资源压力点；
方案：
    需要进行严格的单节点程序的压力测试，以获取程序的瓶颈；

将比对和计算压力分摊到redis
思路描述：
* 使用redis 的可以设置元素过期的数据结构存储监控项
* 在redis 中使用原生的方法比对获取当前异常的监控

## 方案三，时间戳比对和数据对象未到达超时的开销分摊给redis
方案思路
1.	用monitor-torrent将监控数据对象以key-value形式写入redis集群
数据模型
key = {endpoint} + {metric} + {tag}  注：遇到key中tag过长可以进行一定的压缩处理
value {timestamp}
2.	redis中初始创建数据对象时，对每个key设置一定的超时，并配置超时通知事件，如180s，当数据对象的value在超时事件内没有发生更新时，表示当前数据发生了断点，当再次新建该key时，表示数据恢复，如果无新建表示数据丢失；
a.	需要订阅的通知事件
i.	key超时通知
ii.	key新建通知
3.	单独使用新的进程订阅redis的事件通知，对事件进行聚合和录入关系库；
横向扩展：只需要考虑redis集群的横向扩展；
1.	当前进度，redis写入测试阶段

## 方案四，监控覆盖率
方案描述
* 用monitor-torrent将监控数据对象以key-value形式写入redis集群
  * 数据模型
    * key: {endpoint} + {metric}
    * value: {timestamp}
* 写入方式是，monitor-torrent在一个时间段内（例如20分钟）的timer内将收到的endpoint和metric写入本地map，如果已经存在，则无需更新，这样就完成了20内对数据对象的取样；
* timer结束后，将该map全量写入redis集群
* redis批量写入测试

![]({{ "/assets/img/posts/redis_data_sampling_2.png" | relative_url }})

* benchmark结果
  * 一百四十万个数据对象完全的传输和写入耗时为6 ~12秒
  * 连续5次基准测试的耗时在6 ~12秒
* 实现方式
  * 创建连接池，并且保持TCP连接，此处可以自定义一个空闲的TCP连接保持时间，和最小空闲连接数据，及连接池最大连接数；
  * 初始化pipeline对象，go-redis通过将redis命令从多条TCP连接一次性发送到redis集群或者服务节点，大大减小了I/O开销；


####  基准测试源代码
```go
package benchmark
 
import (
   "code.test.com.cn/test-monitor/monitor/monitor-patrol/sdk/httputil"
   "encoding/json"
   "fmt"
   "github.com/go-redis/redis"
   "time"
)
 
type d_dev struct {
   Sysname       string           `json:"sysname"`
}
 
type metric struct {
   Metrics          []string      `json:"metric"`
}
 
func RedisBenchmark() {
 
 
   // get all data1
   queryDevUrl := "http://127.0.0.1:2345/data1?select=name"
   SysnameAll := GetSomething(queryDevUrl, []d_dev{})
   //fmt.Printf("SYSNAME: %s", SysnameAll)
 
   // get all data2
   queryTaskUrl := "http://127.0.0.1:2345/data2?select=metric"
   MetricAll := GetSomething(queryTaskUrl, []metric{})
   //fmt.Printf("Metric: %s", MetricAll)
 
   c := redis.NewClient(&redis.Options{
      Addr: "127.0.0.1:6380",
      Password: "",
      DB: 0,
      MinIdleConns: 10,
      IdleTimeout: 30 * time.Second,
      PoolSize: 120,
   })
 
   var AllData = make(map[string] int64)
 
    
   // generate key
   for _, sys := range (* SysnameAll).([]interface{}){
      sysnamemap := sys.(map[string]interface {})
      for _, sysname := range sysnamemap {
         for _, ml := range (* MetricAll).([]interface{}) {
            for _, m := range ml.(map[string]interface{}) {
               if m != nil {
                  for _, v := range m.([]interface{}) {
                     AllData[sysname.(string) + "&" + v.(string)] = time.Now().Unix()
                  }
               }
            }
         }
      }
   }
 
   fmt.Printf("LEN: %d\n", len(AllData))
 
 
   pong, err := c.Ping().Result()
   if err != nil {
      fmt.Print("no pong")
   }
 
   fmt.Printf("Connection: %s\n", pong)
 
   // 初始化pipeline对象，go-redis通过将redis命令从多条TCP连接一次性发送到redis集群或者服务节点，大大减小了I/O开销；
 
   p := c.Pipeline()
 
   err = p.Set("endpoint+metric", time.Now().Unix(), 60*time.Second).Err()
 
   for k, v := range AllData {
      err = p.Set(k, v, 60*time.Second).Err()
      if err != nil {
         fmt.Print(err)
      }
 
      //val, getErr := c.Get("endpoint+metric").Result()
      //
      //if getErr != redis.Nil {
      // val, getErr = c.Get("endpoint+metric").Result()
      // fmt.Printf("VALUE: %d", val)
      //}
      //
      //fmt.Printf("VALUE: %d", val)
   }
   p.Exec()
 
   fmt.Printf("------END------\n")
 
}
 
func GetSomething(url string, arr interface{}) (* interface{}) {
   // get all monitor device and metric
   resultByte , resultStatus , errj , _ := httputil.GetRequest(url, 60, nil , nil)
   if errj != nil && resultStatus != 200 {
      fmt.Printf("select failed, error=%s, response=%s", errj, resultByte)
   }else{
      //fmt.Printf("select succeed, response=%s", resultByte)
   }
 
   errj = json.Unmarshal(resultByte, &arr)
 
   if errj != nil {
      fmt.Print(errj)
   }
 
   return &arr
}
```