---
title: Python进程内存分析&大量内存占用的优化方案
author: Teddy
date: 2020-03-29 10:00:00 +0800
categories: [体系结构-语言, Python]
tags: [GDB-gcc-debug, jemalloc, ptmalloc2, TCMalloc]
---

# Python进程内存分析&大量内存占用的优化方案

## CPython预编译运行库

> - python-debuginfo-2.7.5-86.el7.x86_64
> - glibc-debuginfo-common-2.17-292.el7.x86_64
> - python-debuginfo-2.7.5-86.el7.x86_64

# monitor-server 内存分析，大量内存占用的优化方案

# 1. 当前程序状态

* 物理机
```
417593 root      20   0 4325700 1.946g   6724 S   8.9  0.8 891:53.36 python
641599 root      20   0 4322988 1.922g   6748 S   3.0  0.8   1219:54 python
641904 root      20   0 4328792 1.968g   6748 S   3.0  0.8   1359:53 python
641963 root      20   0 4327696 1.930g   6748 S   2.0  0.8   1263:28 python
```



* 虚拟机
```
609083 root      20   0 4123852   1.5g   1660 S   2.3  9.5 109:47.85 python
643875 root      20   0 4262180   1.7g   1284 S   1.3 11.0  89:58.01 python
643877 root      20   0 4192588   1.6g   1440 S   1.3 10.6  86:33.74 python
671562 root      20   0 4253364   1.7g   1704 S   1.0 10.8  69:23.61 python   
```



* 运行时间在1000小时左右的进程
 * 在裸金属中占用物理内存比例为0.8%，主机内存总大小为256GB，每个python进程占用大小为2GB左右
 * 在虚拟机中占用的物理内存大小9%~ 11%，主机内存总大小16GB，每个python进程占用内存大小为2GB左右
* 同一LISTEN端口，TCP服务保持的TCP长链接对应Socket数量
  * 虚拟机：80左右
  * 物理机：120 - 140左右
* 因为在LVS转发配置
  * 虚拟机 权重 20   单个进程的权重 20/10
  * 物理机 权重 100  单个进程的权重 100/30

# 2. server对交付报文的处理
* server处理HTTP报文的有效载荷数据大小为数bk到数百kb，服务器使用I/O多路复用，借助select(此处使用了linux的epoll)函数检查事件输入，进程通过监听描述符创建了80到140个连接描述符，并将数据交付给multiprocessing线程池中25个线程中空闲的线程，在文件的读写过程中，server的动态监控及接口监控等数据处理有一定复杂度的函数，会产生大量的数据拷贝和引用，并会创建很多对象（datamodel等）；

* python的垃圾回收发生的条件
 > https://docs.python.org/2/library/gc.html
 > 官方文档：The GC classifies objects into three generations depending on how many collection sweeps they have survived. New objects are placed in the youngest generation (generation 0). If an object survives a collection it is moved into the next older generation. Since generation 2 is the oldest generation, objects in that generation remain there after a collection. In order to decide when to run, the collector keeps track of the number object allocations and deallocations since the last collection. When the number of allocations minus the number of deallocations exceeds threshold0, collection starts. Initially only generation 0 is examined. If generation 0 has been examined more than threshold1 times since generation 1 has been examined, then generation 1 is examined as well. Similarly, threshold2 controls the number of collections of generation 1 before collecting generation 2.
* python内存管理的三层结构
  * generation 0：新建的对象
  * generation 1：垃圾回收后，任然存在引用，则归入1
  * generation 2：最老的无法被collection函数回收的对象
* 回收机制会在内存分配数量和取消分配数量的差值超过 一个特定的阈值 才会触发
* 通过gc模块，可以查看默认的阈值，且可以通过调用set_threshold函数，配置定制的阈值
```python
import gc
gc.get_threshold()　　#gc模块中查看阈值的方法
(700, 10, 10)
```
* 这里的解释是：阈值超过700时才会对g0的对象进行回收，每10次回收g0会发生1次回收g1，每10次回收g1会发生1次回收g2；
* gc模块提供主动触发垃圾回收的函数
```python
def collect(generation=None)
  collect([generation]) -> n
```


> With no arguments, run a full collection.  The optional argument
> may be an integer specifying which generation to collect.  A ValueError
> is raised if the generation number is invalid.

* 对于不传入参数的调用来说，会发起g0 g1 g2三代的全部的回收；
* CPython对C运行库提供的free函数的调用，也存在一定的条件
  * 第3层：最上层，用户对Python对象的直接操作
  * 第1层和第2层：内存池，有Python的接口函数PyMem_Malloc实现\-\-\-\-\-若请求分配的内存在1\~256字节之间就使用内存池管理系统进行分配，调用malloc函数分配内存，但是每次只会分配一块大小为256K的大块内存，不会调用free函数释放内存，将该内存块留在内存池中以便下次使用。
  * 第0层：大内存\-\-\-\-\-若请求分配的内存大于256K，malloc函数分配内存，free函数释放内存；

# 3. 动手操作，问题定位
## 中断运行的程序，输出无法回收的对象
> A list of objects which the collector found to be unreachable but could not be freed (uncollectable objects). By default, this list contains only objects with __del__() methods. 1 Objects that have __del__() methods and are part of a reference cycle cause the entire reference cycle to be uncollectable, including objects not necessarily in the cycle but reachable only from it. Python doesn’t collect such cycles automatically because, in general, it isn’t possible for Python to guess a safe order in which to run the __del__() methods. If you know a safe order, you can force the issue by examining the garbage list, and explicitly breaking cycles due to your objects within the list. Note that these objects are kept alive even so by virtue of being in the garbage list, so they should be removed from garbage too. For example, after breaking cycles, do del gc.garbage[:] to empty the list. It’s generally better to avoid the issue by not creating cycles containing objects with __del__() methods, and garbage can be examined in that case to verify that no such cycles are being created.

* pip install pyrasite
* pip show pyrasite

> Name: pyrasite
> Version: 2.0
> Summary: Inject code into a running Python process
> Home-page: http://pyrasite.com
> Author: Luke Macken

* 安装pyrasite工具，该工具可以中断正在运行的进程，并对进程进行注入和检查
* pyrasite-shell <pid>， 接下来就可以在<pid>的进程里调用任意的python代码, 来查看进程的状态.

* guppy 取得内存使用的各种对象占用情况，guppy 可以用来打印出各种对象各占用多少空间, 如果python进程中有没有释放的对象, 造成内存占用升高, 通过guppy可以查看出来:
* pip install guppy
```python
pyrasite-shell <pid>
from guppy import hpy
h = hpy()
h.heap()
```
* 运行此命令报错，暂时未定位原因，h.heap可以查看当前进程堆的内存分配情况，例如各种类型的对象占用的内存长度；
```
# Partition of a set of 48477 objects. Total size = 3265516 bytes.
#  Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
#      0  25773  53  1612820  49   1612820  49 str
#      1  11699  24   483960  15   2096780  64 tuple
#      2    174   0   241584   7   2338364  72 dict of module
#      3   3478   7   222592   7   2560956  78 types.CodeType
#      4   3296   7   184576   6   2745532  84 function
#      5    401   1   175112   5   2920644  89 dict of class
#      6    108   0    81888   3   3002532  92 dict (no owner)
#      7    114   0    79632   2   3082164  94 dict of type
#      8    117   0    51336   2   3133500  96 type
#      9    667   1    24012   1   3157512  97 __builtin__.wrapper_descriptor
# <76 more rows. Type e.g. '_.more' to view.>
h.iso(1,[],{})
# Partition of a set of 3 objects. Total size = 176 bytes.
#  Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
#      0      1  33      136  77       136  77 dict (no owner)
#      1      1  33       28  16       164  93 list
#      2      1  33       12   7       176 100 int
```


* 无法回收的对象
* python垃圾回收, 对象无法被垃圾回收(uncollectable object), 满足2个条件:
  1. 循环引用
  2. 循环引用的链上某个对象定义了__del__方法, 循环引用的一组对象被gc模块识别为可回收的, 但需要先调用每个对象上的__del__方法, 才能回收. 但用户自定义了__del__的对象, gc系统不知道应该先调用环上的哪个__del__. 因此无法回收这类对象.
* 不能回收的python对象会持续占据内存
* 查找uncollectable的对象:
```python
pyrasite-shell {PID}
>>> import gc
>>> gc.collect() # first run gc, find out uncollectable object and put them in gc.garbage
             # output number of object collected
>>> gc.garbage   # print all uncollectable objects
>>> []               # empty
```
> 如果在上面最后一步打印出了任何不能回收的对象, 则需要进一步查找循环引用链上在哪个对象上包含__del__方法.

* gdb查看python线程执行上下文及调用栈

* 安装python的debuginfo及gcc的debuginfo
* gdb python {PID}
```bash
(gdb) info threads
Id   Target Id         Frame 
 36   Thread 0x7f4b2bbad740 (LWP 404510) 0x00007f4b2a9e1e63 in epoll_wait () at ../sysdeps/unix/syscall-template.S:81
 35   Thread 0x7f4a7bb7a700 (LWP 412337) 0x00007f4b2b3c7afb in futex_abstimed_wait (cancel=true, private=<optimized out>, abstime=0x0, expected=0, futex=0x7f4a58000910)
   at ../nptl/sysdeps/unix/sysv/linux/sem_waitcommon.c:43
 34   Thread 0x7f4a7c37b700 (LWP 412248) 0x00007f4b2b3c7afb in futex_abstimed_wait (cancel=true, private=<optimized out>, abstime=0x0, expected=0, futex=0x7f4a54000b30)
   at ../nptl/sysdeps/unix/sysv/linux/sem_waitcommon.c:43
 33   Thread 0x7f4a7cb7c700 (LWP 410227) 0x00007f4b2b3c7afb in futex_abstimed_wait (cancel=true, private=<optimized out>, abstime=0x0, expected=0, futex=0x7f4a5c000b30)
   at ../nptl/sysdeps/unix/sysv/linux/sem_waitcommon.c:43
 32   Thread 0x7f4a7d37d700 (LWP 409187) 0x00007f4b2b3c7afb in futex_abstimed_wait (cancel=true, private=<optimized out>, abstime=0x0, expected=0, futex=0x7f4a6826fa50)
   at ../nptl/sysdeps/unix/sysv/linux/sem_waitcommon.c:43
 31   Thread 0x7f4a7dc3e700 (LWP 408137) 0x00007f4b2b3c7afb in futex_abstimed_wait (cancel=true, private=<optimized out>, abstime=0x0, expected=0, futex=0x7f4a70003470)
   at ../nptl/sysdeps/unix/sysv/linux/sem_waitcommon.c:43
 30   Thread 0x7f4a7e43f700 (LWP 406936) 0x00007f4b2b3c7afb in futex_abstimed_wait (cancel=true, private=<optimized out>, abstime=0x0, expected=0, futex=0x7f4a6c33ccc0)
   at ../nptl/sysdeps/unix/sysv/linux/sem_waitcommon.c:43
 29   Thread 0x7f4a8effd700 (LWP 405827) 0x00007f4b2b3c7afb in futex_abstimed_wait (cancel=true, private=<optimized out>, abstime=0x0, expected=0, futex=0x7f4a74811da0)
   at ../nptl/sysdeps/unix/sysv/linux/sem_waitcommon.c:43
 28   Thread 0x7f4a8f7fe700 (LWP 404586) 0x00007f4b2b3c7afb in futex_abstimed_wait (cancel=true, private=<optimized out>, abstime=0x0, expected=0, futex=0x7f4a80001b90)
   at ../nptl/sysdeps/unix/sysv/linux/sem_waitcommon.c:43
 27   Thread 0x7f4a8ffff700 (LWP 404585) 0x00007f4b2b3c7afb in futex_abstimed_wait (cancel=true, private=<optimized out>, abstime=0x0, expected=0, futex=0x7f4a88002620)
 ...
(gdb) thread 24
[Switching to thread 24 (Thread 0x7f4aadffb700 (LWP 404582))]
#0  0x00007f4b2b3c7afb in futex_abstimed_wait (cancel=true, private=<optimized out>, abstime=0x0, expected=0, futex=0x7f4a9c002050)
   at ../nptl/sysdeps/unix/sysv/linux/sem_waitcommon.c:43
43            err = lll_futex_wait (futex, expected, private);
(gdb) py-list
334            waiter.acquire()
335            self.__waiters.append(waiter)
336            saved_state = self._release_save()
337            try:    # restore state no matter what (e.g., KeyboardInterrupt)
338                if timeout is None:
>339                    waiter.acquire()
340                    if __debug__:
341                        self._note("%s.wait(): got it", self)
342                else:
343                    # Balancing act:  We can't afford a pure busy loop, so we
344                    # have to sleep; but if we sleep the whole timeout time,
(gdb) 
```
* 看到大量的线程处于 futex_abstimed_wait 状态，使用py-list查看代码后，发现当前该线程的ioloop处于等待状态，结合htop或者top命令，可以看到当前进程的25个线程大多数线程处于等待调度状态（饥饿状态），分析为server扩容后，单个进程的负载很大程度下降，导致对80\~140个范围内的已连接FD不需要频繁的线程上下文切换即可完成处理；

* 使用gcc debug 可以查看当前CPython的调用栈
```bash
0x00007f4b2b3c7afb in futex_abstimed_wait (cancel=true, private=<optimized out>, abstime=0x0, expected=0, futex=0x7f4a9c002050)
   at ../nptl/sysdeps/unix/sysv/linux/sem_waitcommon.c:43
#1  do_futex_wait (sem=sem@entry=0x7f4a9c002050, abstime=0x0) at ../nptl/sysdeps/unix/sysv/linux/sem_waitcommon.c:223
#2  0x00007f4b2b3c7b8f in __new_sem_wait_slow (sem=0x7f4a9c002050, abstime=0x0) at ../nptl/sysdeps/unix/sysv/linux/sem_waitcommon.c:292
#3  0x00007f4b2b3c7c2b in __new_sem_wait (sem=<optimized out>) at ../nptl/sysdeps/unix/sysv/linux/sem_wait.c:28
#4  0x00007f4b2b6e7795 in PyThread_acquire_lock (lock=0x7f4a9c002050, waitflag=1) at /usr/src/debug/Python-2.7.5/Python/thread_pthread.h:323
#5  0x00007f4b2b6eb482 in lock_PyThread_acquire_lock (self=0x7f4b1862a930, args=<optimized out>) at /usr/src/debug/Python-2.7.5/Modules/threadmodule.c:52
#6  0x00007f4b2b6bad40 in call_function (oparg=<optimized out>, pp_stack=0x7f4aadffa060) at /usr/src/debug/Python-2.7.5/Python/ceval.c:4408
#7  PyEval_EvalFrameEx (
   f=f@entry=Frame 0x7f4af4026420, for file /usr/lib64/python2.7/threading.py, line 339, in wait (self=<_Condition(_Verbose__verbose=False, _Condition__lock=<thread.lock at remote 0x7f4b18756f30>, acquire=<built-in method acquire of thread.lock object at remote 0x7f4b18756f30>, _Condition__waiters=[<thread.lock at remote 0x7f4b1862a3f0>, <thread.lock at remote 0x7f4b10aab750>, <thread.lock at remote 0x7f4b1862adb0>, <thread.lock at remote 0x7f4b1862ab10>, <thread.lock at remote 0x7f4b1862ae50>, <thread.lock at remote 0x7f4b1862abd0>, <thread.lock at remote 0x7f4b1862a4d0>, <thread.lock at remote 0x7f4b1862a930>, <thread.lock at remote 0x7f4b1862a8b0>, <thread.lock at remote 0x7f4b1862ae70>, <thread.lock at remote 0x7f4b1862a530>, <thread.lock at remote 0x7f4b1862ab90>, <thread.lock at remote 0x7f4b1862a8d0>, <thread.lock at remote 0x7f4b1862a9d0>, <thread.lock at remote 0x7f4b1862a150>, <thread.lock at remote 0x7f4b1862a290>, <thread.lock at remote 0x7f4b1862aad0>, <thread.lock at remote 0x7f4b1862ad30>, <thread.lock at r...(truncated), throwflag=throwflag@entry=0)
   at /usr/src/debug/Python-2.7.5/Python/ceval.c:3040
#8  0x00007f4b2b6bd08d in PyEval_EvalCodeEx (co=<optimized out>, globals=<optimized out>, locals=locals@entry=0x0, args=<optimized out>, argcount=1, kws=0x7f4aa800cd30, kwcount=0, 
   defs=0x7f4b1fe30188, defcount=2, closure=closure@entry=0x0) at /usr/src/debug/Python-2.7.5/Python/ceval.c:3640
#9  0x00007f4b2b6ba58c in fast_function (nk=<optimized out>, na=<optimized out>, n=<optimized out>, pp_stack=0x7f4aadffa270, func=<optimized out>)
   at /usr/src/debug/Python-2.7.5/Python/ceval.c:4504
#10 call_function (oparg=<optimized out>, pp_stack=0x7f4aadffa270) at /usr/src/debug/Python-2.7.5/Python/ceval.c:4429
#11 PyEval_EvalFrameEx (
   f=f@entry=Frame 0x7f4aa800cb80, for file /usr/lib64/python2.7/Queue.py, line 168, in get (self=<Queue(unfinished_tasks=47882, queue=<collections.deque at remote 0x7f4b0fed62f0>, maxsize=0, all_tasks_done=<_Condition(_Verbose__verbose=False, _Condition__lock=<thread.lock at remote 0x7f4b18756f30>, acquire=<built-in method acquire of thread.lock object at remote 0x7f4b18756f30>, _Condition__waiters=[], release=<built-in method release of thread.lock object at remote 0x7f4b18756f30>) at remote 0x7f4b177ab710>, mutex=<thread.lock at remote 0x7f4b18756f30>, not_full=<_Condition(_Verbose__verbose=False, _Condition__lock=<thread.lock at remote 0x7f4b18756f30>, acquire=<built-in method acquire of thread.lock object at remote 0x7f4b18756f30>, _Condition__waiters=[], release=<built-in method release of thread.lock object at remote 0x7f4b18756f30>) at remote 0x7f4b177ab790>, not_empty=<_Condition(_Verbose__verbose=False, _Condition__lock=<thread.lock at remote 0x7f4b18756f30>, acquire=<built-in method acquire of thread.lock objec...(truncated), throwflag=throwflag@entry=0)
   at /usr/src/debug/Python-2.7.5/Python/ceval.c:3040
#12 0x00007f4b2b6bd08d in PyEval_EvalCodeEx (co=<optimized out>, globals=<optimized out>, locals=locals@entry=0x0, args=<optimized out>, argcount=1, kws=0x7f4a9c000d58, kwcount=0, 
   defs=0x7f4b1f725800, defcount=2, closure=closure@entry=0x0) at /usr/src/debug/Python-2.7.5/Python/ceval.c:3640
#13 0x00007f4b2b6ba58c in fast_function (nk=<optimized out>, na=<optimized out>, n=<optimized out>, pp_stack=0x7f4aadffa480, func=<optimized out>)
   at /usr/src/debug/Python-2.7.5/Python/ceval.c:4504
#14 call_function (oparg=<optimized out>, pp_stack=0x7f4aadffa480) at /usr/src/debug/Python-2.7.5/Python/ceval.c:4429
```
* 通过调用栈可以看到，频繁出现的线程等待的信号量`/linux/sem_waitcommon.c`
* 如果发现某个线程有问题, 切换到那个线程上, 查看调用栈确定具体的执行步骤, 使用bt 命令:
* py-bt显示出python源码的调用栈, 调用参数, 以及所在行的代码.
```bash
#4 Waiting for a lock (e.g. GIL)
#5 Waiting for a lock (e.g. GIL)
#7 Frame 0x7f4af4026420, for file /usr/lib64/python2.7/threading.py, line 339, in wait (self=<_Condition(_Verbose__verbose=False, _Condition__lock=<thread.lock at remote 0x7f4b18756f30>, acquire=<built-in method acquire of thread.lock object at remote 0x7f4b18756f30>, _Condition__waiters=[<thread.lock at remote 0x7f4b1862a3f0>, <thread.lock at remote 0x7f4b10aab750>, <thread.lock at remote 0x7f4b1862adb0>, <thread.lock at remote 0x7f4b1862ab10>, <thread.lock at remote 0x7f4b1862ae50>, <thread.lock at remote 0x7f4b1862abd0>, <thread.lock at remote 0x7f4b1862a4d0>, <thread.lock at remote 0x7f4b1862a930>, <thread.lock at remote 0x7f4b1862a8b0>, <thread.lock at remote 0x7f4b1862ae70>, <thread.lock at remote 0x7f4b1862a530>, <thread.lock at remote 0x7f4b1862ab90>, <thread.lock at remote 0x7f4b1862a8d0>, <thread.lock at remote 0x7f4b1862a9d0>, <thread.lock at remote 0x7f4b1862a150>, <thread.lock at remote 0x7f4b1862a290>, <thread.lock at remote 0x7f4b1862aad0>, <thread.lock at remote 0x7f4b1862ad30>, <thread.lock at r...(truncated)
```


> coredump
> 如果要进行比较长时间的跟踪, 最好将python程序的进程信息全部coredump出来, 之后对core文件进行分析, 避免影响正在运行的程序.
> (gdb) generate-core-file
> 这条命令将当前gdb attach的程序dump到它的运行目录, 名字为core.<pid>, 然后再用gdb 加载这个core文件, 进行打印堆栈, 查看变量等分析, 无需attach到正在运行的程序:
>
> gdb python core.<pid>

> 其他命令
> 其他命令可以在gdb输入py<TAB><TAB> 看到, 和gdb的命令对应, 例如:
> (gdb) py
> py-bt               py-list             py-print            python
> py-down             py-locals           py-up               python-interactive
> py-up, py-down 可以用来移动到python调用站的上一个或下一个frame.
> py-locals 用来打印局部变量
> 等等等等. gdb里也可以用help命令查看帮助:

> (gdb) help py-print
> Look up the given python variable name, and print it
> 在这次追踪过程中, 用gdb-python排除了程序逻辑问题. 然后继续追踪内存泄漏问题:

* 可以结合mmap，及x\命令查看内存地址和程序计数器寄存器的情况

> 参考文档
> https://github.com/lmacken/pyrasite
> https://docs.python.org/2/library/gc.html
> https://www.cnblogs.com/geaozhang/p/7111961.html
> http://man7.org/linux/man-pages/man7/epoll.7.html
> https://linux.die.net/man/4/epoll
> https://blog.csdn.net/ljx0305/article/details/4065058
> https://drmingdrmer.github.io/tech/programming/2017/05/06/python-mem.html#不可回收对象的例子-
> https://blog.csdn.net/evsqiezi/article/details/8061176
> https://github.com/torvalds/linux/blob/master/net/ipv4/tcp.c
> https://juejin.im/post/5cfdd44a6fb9a07eb67d83e9
> https://blog.csdn.net/haoel/article/details/1602108
> https://mg.pov.lt/objgraph/
> http://guppy-pe.sourceforge.net/
> http://guppy-pe.sourceforge.net/heapy_tutorial.html
> https://www.cnblogs.com/chengliangsheng/p/3597010.html
> https://blog.csdn.net/gogoytgo/article/details/64130179


> https://github.com/google/tcmalloc
> https://github.com/jemalloc/jemalloc
> https://blog.csdn.net/junlon2006/article/details/77854898


# 4. 内存占用分析

* 针对monitor-server的情况
  1. 进程启动后，创建到权重占比的已连接描述符后（例如2的权重占总连接的80个左右，3.3占130左右），物理内存占用值会稳定到一个确定值，不会一直上涨，所有初步判断并没有循环引用或者内存泄漏；
  2. 在测试环境中，给动态监控的逻辑部分在请求处理完成返回前，做一次全generation的主动垃圾回收，程序启动后，物理内存的占用会有一定的下降，表现为在几个小时呢从700MB到1.5GB之间；
 * 初步结论，内存无泄漏且无对象的循环引用，主动的gc回收或者降低阈值并增加垃圾回收的频率，会一定程度的降低进程的物理内存的占用，大概可以下降测试前的20%\~30%;

* 考虑C底层预编译的运行库的内存管理算法
 * 生产环境的CentOS7.x 64默认提供的C运行库glibc的版本为2.17，其中malloc库的为ptmalloc2
 * Google提供的替代品：
  * TCMalloc is Google's customized implementation of C's malloc() and C++'s operator new used for memory allocation within our C and C++ code. TCMalloc is a fast, multi-threaded malloc implementation.
  * https://github.com/google/tcmalloc
 * FaceBook提供的替代品：
  * jemalloc is a general purpose malloc(3) implementation that emphasizes fragmentation avoidance and scalable concurrency support. 
  * https://github.com/jemalloc/jemalloc
  * https://www.facebook.com/jemalloc

 * 生产环境网络进过yum search后，找到了jemalloc X86_64的版本，而且可以直接yum安装，无需再次下载和编译；

# 5. 最终方案测试
* 在测试环境中，给动态监控的逻辑部分在请求处理完成返回前，做一次全generation的主动垃圾回收；

* 使用LD_PRELOAD，可以直接用jemalloc代替ptmalloc2，对python代码进行链接执行
 * 测试方式
 * LD_PRELOAD="/usr/lib64/libjemalloc.so" /home/monitor_server/bin/python /opt/netmon/service/monitor-server/monitor/run_server.py --config-file /opt/netmon/service/monitor-server/monitor/conf/conf.ini --port 51035 >> /var/log/monitor-server/server_debug.log 2>&1 &
 ```bash
 root      76913  76489 20 15:36 pts/1    01:17:10 /home/monitor_server/bin/python /opt/netmon/debug/monitor-server/monitor/run_server.py --config-file /opt/netmon/debug/monitor-server/monitor/conf/conf.ini --port 51035
 VmRSS:    522232 kB
  76913 root       20   0 1991M  518M  6736 R 113.  0.2  1h17:15 │        └─ python /opt/netmon/debug/monitor-server/monitor/run_server.py --config-file /opt/netmon/debug/monitor-serve
 ```

* 最终表现

 * 稳定运行15小时的server进行内存占用率维持在0.2%，物理内存的占用为500MB（上下不超过50MB），且添加了主动GC回收后，对单个逻辑核心的5分钟平均占用在50%（估计值）


# 6. 文档
[第三方模拟真实应用的算法测试-ptmalloc2-tcmalloc-hoard-jemalloc](http://ithare.com/testing-memory-allocators-ptmalloc2-tcmalloc-hoard-jemalloc-while-trying-to-simulate-real-world-loads/)
[I/O多路复用技术的简单介绍](https://segmentfault.com/a/1190000003063859)
[]()
[]()
[]()
