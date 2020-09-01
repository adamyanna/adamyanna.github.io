---
title: Python&CPython核心
author: Teddy
date: 2020-04-26 10:00:00 +0800
categories: [体系结构-语言, Python]
tags: [CPython, Python]
---

# Python&CPython核心
> "生成器与协程、CPython虚拟机原理、CPython解释器原理、内存管理与引用计数与优化、高级第三方库、Python语法魔术"

# CPython核心

## I. 虚拟机工作原理&CPython源代码&工作方式
# Evaluation Loop **ceval.c**
* Python虚拟机的 **核心部分**，迭代执行python字节码指令；迭代执行的实现依靠 **for** 循环；
* Python/ceval.c 模块，包含实现执行部分的核心代码，核心函数为 **PyEval_EvalFrameEx**，该函数中包含执行循环；
* ceval.c 模块会针对不同的平台或者操作系统类型，进行对线程和虚拟机有不同的优化；

# 执行循环的工作原理
* 执行前的准备工作 initialization & prepare context
    * **_PyEval_EvalCodeWithName**
        * 代码对象从代码块创建，在python源代码中，代码块包含函数、模块、类、装饰器等等；
        * 从代码块创建的代码对象会经过一连串的函数调用 run_mod -> PyEval_EvalCode -> PyEval_EvalCodeEx -> _PyEval_EvalCodeWithName -> PyEval_EvalFrameEx
        * _PyEval_EvalCodeWithName 的过程包括
            * 初始化“帧对象”，用来提供执行“代码对象”的上下文
            * 为“frame fast locals” 添加 *dict* 关键词
            * 为 “fastlocals” 添加位置参数 *positional arguments* （python函数中的*args类型的参数）
            * 将 无位置变量序列 *non-positional variable sequence* 和 无关键词参数 *non-keyword arguments* 添加到 **fastlocals数组**，这些变量都被存放在 **元组** 类型的数据结构中；（python函数中的*args，**kwargs类型的参数）
            * 检查代码块是否有提供或是否重复提供 kwargs 类型的参数；
            * 检查是否缺少*args位置参数，如果发现缺少则抛出错误
            * 添加默认参数到 *fastlocals* 数组
            * 初始化存储空间和单元变量（storage and cell variables）并拷贝空闲变量数组到当前帧中；
    
* 循环的执行 Evaluation Loop
    * 始化过程完成后，PyEval_EvalFrameEx会以参数的形式调用帧（frame object）；
    
    * PyEval_EvalFrameEx 会进行C的优化，例如宏和计算gotos；
    
    * Evaluation Loop中的核心重要变量 （ceval.c）
        * \*\*stack_pointer，引用下一个要执行的“执行帧”的空闲槽（free slot）； 
        * \*next_instr，引用执行循环需要执行的下一个指令；可以将该变量视为C程序内存中栈帧的程序计数器指针`%rip`
        * opcode，引用当前正在执行的opcode或者将要执行的opcode
        * oparg，引用当前执行或将要执行的opcode所需参数
        * why，执行循环 Evaluation Loop 是一个无线循环 - for(;;)，执行循环需要跳出或终止条件，该变量引用当前要跳出循环的原因；例如跳出循环的原因是因为代码快函数的返回，该变量则应用“WHY_RETURN”状态；
        * fastlocals，引用保存了本地变量的数组
        * freevars，引用，变量名称列表，但是这些名称在代码块中并没有被定义；
        * retval，引用代码快的返回值；
        * co，引用了代码对象，参考虚拟机原理，该对象保存着执行循环的“字节码指令”和过程变量；
        * names，引用了“执行帧对象”的代码块中所有值的名称；
        * consts，引用了代码对象中使用的常量；
        > 回顾虚拟机字节码 python vm bytecode instruction
        > 字节码长度为 16bit，Python虚拟机使用小端法（最低最前，大多数机器都是用小端法表示地址，16进制的最低有效位存储从虚拟内存低地址位开始存储）
        > 字节码包含两个字节，第一个字节存放OPARG，第二个字节存放OPCODE；
        
        | 8bit  | 8bit   |
        | ----- | ------ |
        | OPARG | OPCODE |
        
        
    
    * 重要的C宏
        * TARGET(op) 定义`#define TARGET(op)` ，扩展为case op，将当前要执行的字节码和代码快的实现进行匹配；
        * DISPATCH，扩展为 continue，和宏 - FAST_DISPATCH，用来处理执行循环执行完该opcode之后的“控制流”；
        * FAST_DISPATH，扩展为跳入fast_next_opcode标签；
    * 处理字节码相关的C宏
        * INSTR_OFFSET()，这个宏在当前的指令数组中为指令提供“字偏移”
        * NEXTOPARG()，这个宏用来更新下一个要执行的指令和过程变量的opcode和oparg变量；
    * 执行循环过程分析



## II. 内存管理和底层数据结构的实现及数据结构的内存分配、回收、扩容 “heap”
### 优化
* 最小开销的python代码中变量创建和管理
* Py_INCREF和Py_DECREF了，它们都是内存管理函数。CPython使用引用计数来管理对象的生命周期。一旦新建引用指向对象，那么Py_INCREF会将对象的引用递增，一旦引用超出作用域，Py_INCREF就会递减对象的引用。
* 垃圾回收分析

    * python的垃圾回收发生的条件

      >  https://docs.python.org/2/library/gc.html
      > 官方文档：The GC classifies objects into three generations depending on how many collection sweeps they have survived. New objects are placed in the youngest generation (generation 0). If an object survives a collection it is moved into the next older generation. Since generation 2 is the oldest generation, objects in that generation remain there after a collection. In order to decide when to run, the collector keeps track of the number object allocations and deallocations since the last collection. When the number of allocations minus the number of deallocations exceeds threshold0, collection starts. Initially only generation 0 is examined. If generation 0 has been examined more than threshold1 times since generation 1 has been examined, then generation 1 is examined as well. Similarly, threshold2 controls the number of collections of generation 1 before collecting generation 2.

    * python内存管理的三层结构

      * generation 0：新建的对象

      * generation 1：垃圾回收后，任然存在引用，则归入1

      * generation 2：最老的无法被collection函数回收的对象

     * 回收机制会在内存分配数量和取消分配数量的差值超过 一个特定的阈值 才会触发

     * 通过gc模块，可以查看默认的阈值，且可以通过调用set_threshold函数，配置定制的阈值
 ```python
 import gc
 gc.get_threshold()  #gc模块中查看阈值的方法
 (700, 10, 10)
 ```
 * 这里的解释是：阈值超过700时才会对g0的对象进行回收，每10次回收g0会发生1次回收g1，每10次回收g1会发生1次回收g2；
 * gc模块提供主动触发垃圾回收的函数
 ```python
 def collect(generation=None)
    collect([generation]) -> n
 ```
    > With no arguments, run a full collection.  The optional argument
    may be an integer specifying which generation to collect.  A ValueError
    is raised if the generation number is invalid.
    * 对于不传入参数的调用来说，会发起g0 g1 g2三代的全部的回收；
    
    * CPython对C运行库提供的free函数的调用，也存在一定的条件
     * 第3层：最上层，用户对Python对象的直接操作
  * 第1层和第2层：内存池，有Python的接口函数PyMem_Malloc实现\-\-\-\-\-若请求分配的内存在1\~256字节之间就使用内存池管理系统进行分配，调用malloc函数分配内存，但是每次只会分配一块大小为256K的大块内存，不会调用free函数释放内存，将该内存块留在内存池中以便下次使用。
    * 第0层：大内存\-\-\-\-\-若请求分配的内存大于256K，malloc函数分配内存，free函数释放内存；

## III. 生成器和协程 generator & coroutine
### 生成器对象 generator

```c
/* _PyGenObject_HEAD defines the initial segment of generator
   and coroutine objects. */
#define _PyGenObject_HEAD(prefix)                                           \
    PyObject_HEAD                                                           \、
    /* Note: gi_frame can be NULL if the generator is "finished" */         \
    struct _frame *prefix##_frame;                                          \
    /* True if generator is being executed. */                              \
    char prefix##_running;                                                  \
    /* The code object backing the generator */                             \
    PyObject *prefix##_code;                                                \
    /* List of weak reference. */                                           \
    PyObject *prefix##_weakreflist;                                         \
    /* Name of the generator. */                                            \
    PyObject *prefix##_name;                                                \
    /* Qualified name of the generator. */                                  \
    PyObject *prefix##_qualname;                                            \
    _PyErr_StackItem prefix##_exc_state;

typedef struct {
    /* The gi_ prefix is intended to remind of generator-iterator. */
    _PyGenObject_HEAD(gi)
} PyGenObject;
```

* 结构底层定义为 _PyGenObject_HEAD, 结构体对象为PyGenObject
    * 在生成器对象中包含了 帧对象的引用 和 代码对象的引用，回顾python虚拟机实现可知，代码对象在运行时会生成帧对象，解释器对帧对象进行执行，其中包含了代码对象中的Python虚拟机指令和过程变量；
    * 运行的生成器提供了 “suspended”阻塞 和 “resumed”就绪 的状态切换的功能；
    * 定义的属性包括和宏
        * *prefix\#\#_frame
            * 帧对象，包含生成器对象的代码对象引用，用来执行该对象
        * prefix\#\#_running
            * 布尔值，用来确定当前的生成器是否还在运行
        * *prefix\#\#_code
            * 代码对象引用，生成器用来执行的对象
        * *prefix\#\#_name
            * 生成器名称
        * *prefix\#\#_qualname
            * “qualified” 的名称，多数情况下和_name相同；

* 生成器和协程运行原理
    * 生成器通过对内置next python函数的调用来执行，当遇到yield python内置表达式时，生成器会发生阻塞；
    * 生成器如何保存和获取执行状态，又是怎样在遇到特定的状态是对当前的执行进行状态的更新的
        * 如何保存执行状态
            * 生成器对象中保存着当前帧对象的引用，该引用中包含了所有生成器需要执行的上下文（代码对象），通过对帧对象的引用，生成器可以捕获执行过程中的所有状态；（状态可以指过程的python虚拟机指令及变量）
        * yield 表达式
            * 生成器的执行过程中，在遇到yield语句时会发生主动放弃或让出当前执行时间片，然后Python虚拟机会对当前的生成器的状态进行保存，时间片发生轮转；
        * 生成器如何完成调度（这里的调度就是生成器的阻塞和就绪的状态切换，且生成器需要主动放弃当前执行的权限，或者说执行的时间片）
            * next内置函数，当生成器调用next内置函数，next函数的主要作用是对已经发生阻塞的生成器恢复执行，该函数会完成两个作用
                1. 对当前的指针 "tp_iternext" 解除引用，"tp_iternext" 可以理解为python虚拟机的程序计数器指针，每个运行的线程或者生成器对象在执行期间都会引用程序计数器，从而告诉虚拟机下一条要执行的指令；
                2. 随机调用 "tp_iternext" 程序计数器关联的任何其他函数，对于当前线程的其他生成器来说，会调用 gen_iternext -> gen_send_ex，最终通过该函数的调用会重新执行之前被阻塞的生成器；
            * 通过以上两种方式生成器/协程实现了在Python虚拟机内部的时间片轮转；
        * Python的生成器同样支持参数传递；

### 调度

## IV. 线程状态对象&CIL结构对象&解释器对象
### 调度

## V. 对象&对象管理

## VI. 内置方法的高级用法
### 数据模型 
* [datamodel](https://docs.python.org/3/reference/datamodel.html)
* 元类 `__metaclass__`
    * [datamodel](https://docs.python.org/3/reference/datamodel.html)
    * python中默认情况下，类型由type()函数构成，类的主体会创建一个新的namespace用于执行，类名会和type(name, bases, namespace)进行绑定；
    * python可以在类声明行中传递 `metaclass keyword argument` 实现元类，或者通过对传递了该参数的类进行继承，原来需要继承自type；
    * 元类就是其父类继承自type的类型（子孙类都可以实现元类）；
    * 类定义中指定的任何其他关键字参数都将传递到下面描述的所有元类操作；
    * 当类定义被执行后，发生了以下的步骤：
        * MRO 入口处理
        * 确定该类型适当的元类
        * 准备类型的命名空间
        * 执行类型主体
        * 类型对象呗创建并返回

```python
class Singleton(type):
    __instance = {}
    def __int__(self, *args, **kwargs):
        super(Singleton, self).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instance:
            cls.__instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instance[cls]

class Publisher():

    __metaclass__ = Singleton
    def __init__(self):
        pass

class Meta(type):
    pass

class MyClass(metaclass=Meta):
    pass

class MySubclass(MyClass):
    pass
```

* 抽象基类 `ABC`
* `__class__`
    * 该方法可以访问当前实例的类，通过该函数可以修改一个实例对象对某个类的引用；
* `__new__`
    * 静态方法，在python的语法中，一切皆对象，`__new__` 方法用来创建新的类的实例，该方法的调用中，cls也就是类对象要作为第一个参数，其他参数用来传递给`__new__`来构造新的对象，新的对象可能是类的实例，也可能是一个新的类型；
    * 在 `__new__` 实现中，如果需要实现对父类的调用，可以使用 `super().__new__(cls[, ...])` 并且需要传入父类所需要的基本参数，获得父类实例后再进行任何其他修改；
    * 在 `__new__` 实现中，如果需要实现对父类的类对象调用，可以使用 `super(xxx, cls).__new__(cls[, ...])` ，可以获得新的类型，对于在对象构造期间调用 `__new __（）` 并返回cls的实例或子类，则将像 `__init __（self [，...]）` 一样调用新实例的 `__init __（）` 方法，其中self是新实例，而 其余参数与传递给对象构造函数的参数相同。
    * 如果`__new__()`, 方法调用没有返回任何实例或者子类，那么新实例的`__init __（）`方法就不会被调用；
    * `__new__` 核心作用
        * 主要是允许 **不可变** 类型的子类，自定义的创建实例；
        * 也用来实现自定义的类和其属性的实现；
        * 通常也被自定义元类覆盖。

```python
    def __new__(cls, **kwargs):
        new_cls = super(DataModel, cls).__new__(cls)
        for k, v in kwargs.iteritems():
            if hasattr(DataModel, k):
                setattr(new_cls, k, v)
        return new_cls
```
* `__init__`
    * 在实例创建完成后调用（通过`__new __（）`），但在实例返回给调用方之前被调用。 参数是传递给类构造函数表达式的参数。 如果基类具有`__init __（）`方法，则派生类的`__init __（）`方法（如果有）必须显式调用它，以确保实例的基类部分的正确初始化。 例如：`super（）.__ init __（[args ...]）。`
    * 子类中如果想要调用父类的`__init __（）`方法，必须在`__init __（）`中通过`super（）`显示的调用；
    * 因为`__new __（）`和`__init __（）`在构造对象时一起工作（`__new __（）`来创建它，而`__init __（）`来对其进行自定义），所以`__init __（）`不能返回任何非`None`值； 这样做将导致在运行时引发`TypeError`。
* `__call__`
    * 该方法会在一个对象被当做函数调用的情况下，调用，`object.__call__(self[, args...]), object()` 
    * 通过在类中定义__call __（）方法，可以使任意类的实例成为可调用的。
    * python的任何对象都可以使用`callable()`来判断是否可调用，对于不可调用的对象，只需要在对象中实现`__call__`方法，例如在元类中实现call方法，则继承元类的子类在生成实例时就会调用；
* 总结
    * 单例的多种实现方式在类中重写`__new __（）`，类继承元类，并在元类中使用`__call__()` 方法实现，装饰器实现；
    * There is no fucking magic, all the implementation are from CPython pyobjectclass;

```python
class Singleton(type):
    __instance = {}

    def __call__(cls):
        print "metaclass __call__"
        if cls not in cls.__instance:
            cls.__instance[cls] = super(Singleton, cls).__call__()
        return cls.__instance[cls]


class BasicSub(object):
    __metaclass__ = Singleton

    def __init__(self):
        print "__init__"
        super(BasicSub, self).__init__()

    def __new__(cls):
        print "__new__"
        self = super(cls, BasicSub).__new__(cls)
        return self

    def __call__(self):
        print "__call__"

a = BasicSub()
a()
```

## VII. 高级第三方库的实现
### Web框架
### 并发框架
* futures
* Gevent
    * 基于C的高性能事件循环模型库libev，实现的基于API和网络相关任务的并发模型；
* greenlet

### C实现的第三方库

https://github.com/python/cpython/blob/master/Python/ceval.c

https://www.cnblogs.com/qdhxhz/p/9757390.html

https://redis.io/commands

openstack https://blog.csdn.net/dylloveyou/article/details/80698420

socket fd https://www.cnblogs.com/DengGao/p/file_symbol.html

mmap https://www.cnblogs.com/huxiao-tee/p/4660352.html

## VIII. 

# Python Runtime Services
[Runtime Services](https://docs.python.org/3/library/python.html)

