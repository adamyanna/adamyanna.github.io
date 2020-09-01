---
title: Golang性能分析和监控
author: Teddy
date: 2020-04-05 10:00:00 +0800
categories: [体系结构-语言, Golang]
tags: [Go, Go-pprof, Flamegraph]
---

# Golang性能分析和监控

## tool pprof 和 package pprof
    * [pprof](https://golang.org/pkg/runtime/pprof/)
    * 通过HTTP服务提供运行时的性能分析数据（统计数据）
    * 通过使用go tool pprof可以对数据进行特殊的格式化，以满足分析需求
    * 包导入的方式
        * `import "net/http/pprof"`
    * http定位器访问方式
        * `/debug/pprof`


## 实践过程

```go
func main() {

 //c := make(chan os.Signal)
 //signal.Notify(c)

 binaryAbsPath, _ := filepath.Abs(filepath.Dir(os.Args[0]))

 // @ golang performance test
 fmt.Printf("[monitor-patrol] Performance CPU, %s/cpu_monitor.prof...\n", filepath.Dir(binaryAbsPath))
 fmt.Printf("[monitor-patrol] Performance MEM, %s/mem_monitor.prof...\n", filepath.Dir(binaryAbsPath))
 fmt.Printf("[monitor-patrol] Performance monitor, contect to 127.0.0.1:8080 to check...\n")

 cpuProFile := filepath.Dir(binaryAbsPath) + "/cpu_monitor.prof"
 memProFile := filepath.Dir(binaryAbsPath) + "/mem_monitor.prof"

 // @ Windows debug
 //cpuProFile := "./cpu_monitor.prof"
 //memProFile := "./mem_monitor.prof"

 f, err := os.Create(cpuProFile)
 if err != nil {
  fmt.Printf("could not create CPU profile: %s", err)
 }
 if err := pprof.StartCPUProfile(f); err != nil {  //监控cpu
  fmt.Printf("could not start CPU profile: %s", err)
 }

 runtime.GOMAXPROCS(runtime.NumCPU())


 go func() {
  http.ListenAndServe("0.0.0.0:8080", nil)
 }()

 pg := &program{}
 if err := svc.Run(pg, syscall.SIGINT, syscall.SIGTERM, syscall.SIGKILL, syscall.SIGQUIT); err != nil {
  fmt.Printf("run exit with err:%s", err)
  fmt.Printf("Main END\n")
  //
  pprof.StopCPUProfile()
  //
  f, err := os.Create(memProFile)
  if err != nil {
   fmt.Printf("could not create memory profile: %s", err)
  }
  runtime.GC() // GC，获取最新的数据信息
  if err := pprof.WriteHeapProfile(f); err != nil {  // 写入内存信息
   fmt.Printf("could not write memory profile: %s", err)
  }
  f.Close()
  fmt.Printf("Main END\n")
  //
  os.Exit(2)
 } else {
  log.Logger.Info("bye :-)")
 }
}
```
### 方式一
* 使用方式是通过import直接导入 `_ "net/http/pprof"`
* 然后通过http的package直接启动监听服务 `http.ListenAndServe()`
* 通过浏览器可以直接访问 `http://ip:port/debug/pprof` 来查看当前的性能采样情况

### 方式二
* 通过 io package的writer，创建并调用i/o写入性能采样数据
    `pprof.StartCPUProfile(f)`
    `pprof.WriteHeapProfile(f)`
* 程序结束退出后，可以直接访问生成的cpu和heap文件

##### debug/pprof 内容
```
/debug/pprof/

Types of profiles available:
Count Profile
4 allocs
0 block
0 cmdline
1054 goroutine
4 heap
0 mutex
0 profile
13 threadcreate
0 trace
full goroutine stack dump 
Profile Descriptions:

allocs: A sampling of all past memory allocations
block: Stack traces that led to blocking on synchronization primitives
cmdline: The command line invocation of the current program
goroutine: Stack traces of all current goroutines
heap: A sampling of memory allocations of live objects. You can specify the gc GET parameter to run GC before taking the heap sample.
mutex: Stack traces of holders of contended mutexes
profile: CPU profile. You can specify the duration in the seconds GET parameter. After you get the profile file, use the go tool pprof command to investigate the profile.
threadcreate: Stack traces that led to the creation of new OS threads
trace: A trace of execution of the current program. You can specify the duration in the seconds GET parameter. After you get the trace file, use the go tool trace command to investigate the trace.
```

* allocs
    * 对程序声明周期内所有分配的内存的抽样
* block
    * 因为堆栈跟踪导致对“同步原语”的阻塞
* cmdline
    * 当前程序的命令行调用
* goroutine
    * 当前所有的go协程的堆栈追踪
* heap
    * 当前堆内存中处于“存活”状态的对象的抽样，可以在运行抽样，特别的指定想要垃圾回收的对象
* mutex
    * 对“互斥锁”的持有对象的堆栈跟踪
* profile
    * CPU 的性能描述数据
    * 如果使用了StartCPUProfile写入文件的方式，在http服务中无法下载该文件，对该文件的查看方式
    * 使用 `go tool pprof` 命令进入交互式环境，使用top命令查看调用时长等；
        * 典型的命令
            * top              Outputs top entries in text form
            * web              Visualize graph through web browser
            * call_tree        Create a context-sensitive call tree
            * list             Output annotated source for functions matching regexp
        * 使用`help`命令查看详情
        * 使用`web`命令生成可视化的svg调用树，也可以使用`web Func`来过滤执行函数相关的调用树；
            > CentOS下必须安装 xdg-utils 和 graphviz   
        * top+[数量值]，可以查看占用CPU采样时间的函数的行数，例如默认top为top10，就只看占用CPU采样时间最长的10个函数调用；
        * 组合使用：
            1. 使用top命令找到占据CPU采样时间最多的函数调用
            2. 再通过 web 函数名 生成该函数的调用树的图谱，查看调用关系，找到调用该函数的父级函数
            3. 使用 list 父级函数 查看该函数的具体代码实现，通过对函数内部使用的数据结构和处理判断对CPU发生大量占用的点；
            4. 思路：通过结合top和web命令找到导致占用大量抽样的关键函数，分析函数内部实现，和其涉及到的数据结构和算法；对该函数的优化可以结合go test benchmark的基准测试来测试优化后的性能；
        ```Bash
    [root@CNSZ049589 /]# go tool pprof optcpu_monitor.prof 
    File: libc-2.17.so
    Build ID: 8b2c421716985b927aa0caf2a05d0b1f452367f7
    Type: cpu
    Time: Nov 11, 2019 at 6:07pm (CST)
    Duration: 3.89s, Total samples = 22.57s (580.86%)
    Entering interactive mode (type "help" for commands, "o" for options)
    (pprof) top
    Showing nodes accounting for 12980ms, 57.51% of 22570ms total
    Dropped 254 nodes (cum <= 112.85ms)
    Showing top 10 nodes out of 132
      flat  flat%   sum%        cum   cum%
    4470ms 19.81% 19.81%     4500ms 19.94%  runtime.chanrecv
    2260ms 10.01% 29.82%     6730ms 29.82%  runtime.selectnbrecv
    1290ms  5.72% 35.53%     1330ms  5.89%  encoding/json.stateInString
    1060ms  4.70% 40.23%     2190ms  9.70%  encoding/json.(*decodeState).scanWhile
     930ms  4.12% 44.35%     2020ms  8.95%  encoding/json.checkValid
     620ms  2.75% 47.10%     7100ms 31.46%  encoding/json.(*decodeState).object
     600ms  2.66% 49.76%     3810ms 16.88%  code.test.com.cn/test-monitor/monitor/monitor-patrol/handler/analyzer.UploadEventToDB
     600ms  2.66% 52.41%     1630ms  7.22%  runtime.scanobject
     580ms  2.57% 54.98%      580ms  2.57%  runtime.memmove
     570ms  2.53% 57.51%     4090ms 18.12%  code.test.com.cn/test-monitor/monitor/monitor-patrol/handler/analyzer.UploadMonitorCoverageData
    ```
* threadcreate
    * 对于从操作系统创建的新的线程的堆栈堆栈跟踪
* 当前程序执行的跟踪。 您可以在秒GET参数中指定持续时间。 获取跟踪文件后，使用go工具trace命令调查跟踪。

* 内存分析
```
[root@CNSZ049589 /]# go tool pprof optmem_monitor.prof 
File: libc-2.17.so
Build ID: 8b2c421716985b927aa0caf2a05d0b1f452367f7
Type: inuse_space
Time: Nov 11, 2019 at 6:07pm (CST)
Entering interactive mode (type "help" for commands, "o" for options)
(pprof) top
Showing nodes accounting for 573.38MB, 98.95% of 579.46MB total
Dropped 32 nodes (cum <= 2.90MB)
Showing top 10 nodes out of 27
      flat  flat%   sum%        cum   cum%
  173.51MB 29.94% 29.94%   184.01MB 31.76%  encoding/json.(*decodeState).literalStore
  158.42MB 27.34% 57.28%   158.42MB 27.34%  reflect.unsafe_NewArray
  105.63MB 18.23% 75.51%   105.63MB 18.23%  code.test.com.cn/test-monitor/monitor/monitor-patrol/handler/analyzer.(*DataContainer).AppendMetricList
      64MB 11.05% 86.56%   201.35MB 34.75%  code.test.com.cn/test-monitor/monitor/monitor-patrol/handler/analyzer.(*Analyzer).DataDistribution
   23.72MB  4.09% 90.65%    29.72MB  5.13%  sync.(*Map).Store
   20.76MB  3.58% 94.23%    20.76MB  3.58%  code.test.com.cn/test-monitor/monitor/monitor-patrol/vendor/github.com/streadway/amqp.(*Channel).recvContent
   10.50MB  1.81% 96.04%    10.50MB  1.81%  encoding/json.(*decodeState).convertNumber
    8.34MB  1.44% 97.48%     8.34MB  1.44%  code.test.com.cn/test-monitor/monitor/monitor-patrol/vendor/github.com/streadway/amqp.(*reader).parseBodyFrame
    5.50MB  0.95% 98.43%     5.50MB  0.95%  sync.newEntry (inline)
       3MB  0.52% 98.95%        3MB  0.52%  runtime.malg
```
* memprofile 就是堆采样数据，使用参数结合 go tool pprof 来查看内存情况
    * --inuse_objects 来显示使用的堆的对象的个数
    * --alloc_objects 分配的堆对象个数
    * --alloc_space   分配的堆内存大小
* 使用web 生成可视化文件，查看内存分配；

### Prometheus
* Prometheus client内置了golang metrics暴露的handler，只需要简单调用即可实现
* 使用metrics即可定位metrics指标的采集数据
* 使用模块**"github.com/zsais/go-gin-prometheus"**
```golang
package main

import (
    "github.com/prometheus/client_golang/prometheus/promhttp"
    "net/http"
)

func main() {
    http.Handle("/metrics", promhttp.Handler())
    panic(http.ListenAndServe(":9090", nil))
}
```
* 访问http://localhost:9090/metrics 即可。
* 同时可以通过Prometheus来采集此Endpoint暴露出来的数据，也可以进行自定义数据的采集
  * prometheus修改yaml配置文件，增加新的job和job指标静态描述
  * 进行配置重载 `curl -X POST http://ip:port/-/reload`
* 参考文档
  * https://blog.pvincent.io/2017/12/prometheus-blog-series-part-4-instrumenting-code-in-go-and-java/



