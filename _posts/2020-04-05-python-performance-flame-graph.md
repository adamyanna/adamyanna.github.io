---
title: Python性能分析和火焰图
author: Teddy
date: 2020-04-05 10:00:00 +0800
categories: [体系结构-语言, Python]
tags: [Python, Flamegraph]
---

# Python性能分析和火焰图

## cProfile和profile为python程序提供的性能分析工具
* profile提供一组**统计信息**，用来描述对于一个函数或者一个代码块的被调用次数或者执行次数和执行所花费的时间；
* 对于这些统计信息，可以使用python的pstats模块，使用不同类型的参数进行输出，或者使用第三方的模块输入火焰图，例如frameprof；
* [python2.7-cProfile](https://docs.python.org/2/library/profile.html#module-cProfile)

## 使用方式
* 运行命令中添加cProfile模块，来生产统计信息
  `python -m cProfile [-o output_file] [-s sort_order] myscript.py`
    * -o表示程序生命周期结束后的输出文件
    * -s表示指定一个参数来进行排序，例如使用函数被调用次数排序ncalls，或者使用累积时间cumtime
    * -s参数在有-o输出文件的情况下，不会生效，因为输出文件包含原始的统计数据，需要再次读取和排序
    * 当程序终止后才能生成文件，对于循环执行的进程或者服务，需要手动发送前台进程强制终止信号；
* 在程序中导入cProfile使用
```python
import cProfile
import re
cProfile.run('re.compile("foo|bar")')
```
  

## 实践
* 使用cProfile启动python服务
```Bash
 cd /opt/netmon/debug/monitor-server/monitor/
 /home/monitor_server/bin/python -m cProfile -o result.out  /opt/netmon/debug/monitor-server/monitor/run_server.py --config-file /opt/netmon/debug/monitor-server/monitor/conf/conf.ini --port 51035 >> /var/log/monitor-server/server_debug.log 2>&1
```
 
* 服务启动后，标准输出和标准错误都会追加到/var/log/monitor-server/server_debug.log
* 等待后端服务的进程执行一定的时间，例如10\~30分钟，已经处理了相当一部分请求，将进程强制终止，得到result.out文件；
* 对result.out文件进行输出，可以直接使用python和pstats模块，或者使用脚本输出；

```python
 #!/usr/bin/python
 
 import pstats
 import sys
 
 input_f = sys.argv[1]
 p = pstats.Stats(input_f)
 #p.sort_stats("cumulative", "name")
 p.sort_stats("ncalls", "cumtime")
 p.print_stats()
```

* 支持的排序方式有：
    * ncalls 
    * 函数或者代码块被调用的次数
    * tottime 
    * 在函数中执行所使用的总时长，但是该时间会排除调用子功能所花费的时间
    * percall 
    * tottime 除以 ncalls的商的值
    * cumtime 
    * 函数包含其子函数的总累积调用时间，对于递归函数同样适用，为递归函数的全部递归次数的执行总时长
    * percall 
    * cumtime 除以 ncalls 的商的值
    * Filename
    * 每个函数所在文件及开始行号

* 输出结果：
```
 [root@cnsz036678 monitor]# python output_pstats.py cum.out | head -n 100
 Tue Apr  7 17:10:32 2020    cum.out
 
          13445271 function calls (13371131 primitive calls) in 436.704 seconds
 
    Ordered by: call count, cumulative time
 
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   3726996    0.695    0.000    0.716    0.000 {method 'get' of 'dict' objects}
 1710220/1710218    0.565    0.000    0.580    0.000 {isinstance}
 1525540/1524061    0.191    0.000    0.192    0.000 {len}
    959341    1.045    0.000    1.045    0.000 {_codecs.utf_8_decode}
    959298    0.454    0.000    1.499    0.000 /home/monitor_server/lib64/python2.7/encodings/utf_8.py:15(decode)
    706968    0.595    0.000    0.926    0.000 /home/monitor_server/lib/python2.7/site-packages/oslo_config/cfg.py:2940(_get)
    706966    0.476    0.000    1.402    0.000 /home/monitor_server/lib/python2.7/site-packages/oslo_config/cfg.py:2509(__getattr__)
    706958    1.753    0.000    2.011    0.000 /opt/netmon/debug/monitor-server/monitor/core/handlers/device_info_handler.py:36(_format_speed)
    191741    0.034    0.000    0.034    0.000 {method 'append' of 'list' objects}
    176914    0.020    0.000    0.020    0.000 {ord}
    136071    0.042    0.000    0.042    0.000 {method 'seek' of 'cStringIO.StringO' objects}
     71548    0.034    0.000    0.034    0.000 {method 'endswith' of 'str' objects}
     66992    0.024    0.000    0.024    0.000 {method 'readline' of 'cStringIO.StringO' objects}
 59707/7204    0.367    0.000    2.729    0.000 /home/monitor_server/lib/python2.7/site-packages/redis/connection.py:283(read_response)
     59707    0.192    0.000    1.554    0.000 /home/monitor_server/lib/python2.7/site-packages/redis/connection.py:210(readline)
     59707    0.011    0.000    0.011    0.000 /home/monitor_server/lib/python2.7/site-packages/redis/_compat.py:126(byte_to_chr)
     53938    0.022    0.000    0.022    0.000 /home/monitor_server/lib/python2.7/site-packages/redis/connection.py:162(length)
     52878    0.072    0.000    0.393    0.000 {method 'decode' of 'str' objects}
     52564    0.034    0.000    0.034    0.000 {method 'read' of 'cStringIO.StringO' objects}
     52490    0.069    0.000    0.466    0.000 /home/monitor_server/lib/python2.7/site-packages/redis/connection.py:122(decode)
     52482    0.175    0.000    0.313    0.000 /home/monitor_server/lib/python2.7/site-packages/redis/connection.py:193(read)
     51196    0.068    0.000    0.081    0.000 /home/monitor_server/lib64/python2.7/sre_parse.py:183(__next)
     46852    0.030    0.000    0.103    0.000 /home/monitor_server/lib64/python2.7/sre_parse.py:202(get)
     44246    0.019    0.000    0.019    0.000 /home/monitor_server/lib/python2.7/site-packages/yaml/reader.py:87(peek)
     33628    0.020    0.000    0.020    0.000 {getattr}
     26234   15.935    0.001   16.355    0.001 {eval}
     25679    0.013    0.000    0.018    0.000 /home/monitor_server/lib64/python2.7/sre_parse.py:139(append)
 25451/25148    0.030    0.000    0.154    0.000 {method 'join' of 'str' objects}
     25357    0.017    0.000    0.017    0.000 {range}
```
* 该进程接入测试数据进行简单的分析后，初步结论
    * 现在通过一些测试，能看出来一部分问题出现的可能，第一是json解析的操作耗时，第二是 IOString 结构体底层的过多的处理，第三是getattr方式来定位对象函数
    * 需要更多实际生产环境导致程序大量接口超时的数据模拟；

## 火焰图
* 使用flameprof来生成火焰图
* 安装
  * `pip install flameprof`
* 简单使用：
  * `flameprof result_2.cum.out > cum.svg`
```bash
flameprof --help
usage: flameprof.py [-h] [--width WIDTH] [--row-height ROW_HEIGHT]
                  [--font-size FONT_SIZE] [--threshold THRESHOLD]
                  [--format {svg,log}] [--log-mult LOG_MULT] [--version]
                  [-r] [-m] [--cpu] [-o OUT] [--wsgi-out-dir WSGI_OUT_DIR]
                  [--wsgi-format WSGI_FORMAT]
                  stats
```
  * 使用help产看具体用法
    * [pypi-flameprof](https://pypi.org/project/flameprof/)
    * [flamegraphs](http://www.brendangregg.com/flamegraphs.html)
  
* 如何快速看懂火焰图
    * [看懂火焰图](http://www.ruanyifeng.com/blog/2017/09/flame-graph.html)
* 通常性能分析工具会返回 CPU 正在执行的指令对应的函数名以及调用栈（stack）
* 通常，它的执行频率是 99Hz（每秒99次），如果99次都返回同一个函数名，那就说明 CPU 这一秒钟都在执行同一个函数，可能存在性能问题。（CPU每秒执行指令的次数取决于CPU内频和外频以及晶振频率）
* y 轴表示调用栈，每一层都是一个函数。调用栈越深，火焰就越高，顶部就是正在执行的函数，下方都是它的父函数。
* x 轴表示抽样数，如果一个函数在 x 轴占据的宽度越宽，就表示它被抽到的次数多，即执行的时间长。注意，x 轴不代表时间，而是所有的调用栈合并后，按字母顺序排列的。
* 火焰图就是看顶层的哪个函数占据的宽度最大。只要有"平顶"（plateaus），就表示该函数可能存在性能问题。
* 颜色没有特殊含义，因为火焰图表示的是 CPU 的繁忙程度，所以一般选择暖色调。



