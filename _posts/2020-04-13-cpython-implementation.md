---
title: CPython源代码分析&虚拟机原理
author: Teddy
date: 2020-04-13 10:00:00 +0800
categories: [体系结构-底层, Python虚拟机底层实现]
tags: [CPython]
---

# CPython源代码分析&虚拟机原理

## 结合编译原理&CSAPP理解CPython底层实现，分支v3.8及v2.7

###### 本地追踪分支 master / 2.7 / 2.8



## 进入源代码分析之前

* CPython是python的解释器实现之一
* CPython在广义上讲，就是**”执行程序的程序“**
* 但是与传统静态语言（C）编译驱动程序不同的是
  * C程序声明周期简介（简单介绍，核心知识点在此处不展开）
    * C源代码经过预处理、编译、汇编、链接，最终生成可执行二进制，该二进制包含一系列的节，对应机器代码段、格式串、开关语句跳转表、全局变量、静态变量、符号表、调试信息等；
    * 可执行二进制经过fork和execve函数调用后，被加载进内存，并在操作系统栈的进程管理数据结构中创建一个 task_struck 任务结构来管理进程的基本信息；execve最终会指向.init初始化函数，也就是该程序的入口点；
    * 这样一个传统的可执行二进制就从源代码文件成为了一个由操作管理的正在执行的进程；
    
  * 概括来说，Python程序的执行包括3个阶段
    * 初始化（initialization）
      * 进行对python进程所需要的一系列数据结构的初始化，交互模式下不会进行这些数据的初始化
    * 编译（compling）
      * 将py源文件中ASCII代码，生成抽象语法树 AST（Abstract syntax tree），创建AST对象，创建符号表 symbol table以及生成 code objects；
    * 解释运行（interpreting）
      * 对栈中的字节码指令（Python Byte Code Instruction）上下文进行执行（code object）；
    
  * 解释器如果管理堆栈，如何创建和回收python源代码中的数据结构；

    * https://nanguage.gitbook.io/inside-python-vm-cn/untitled
    * https://tech.blog.aknin.name/2010/04/02/pythons-innards-introduction/

  * 解释器的本质

    * 

  * 解释器的堆内存段管理

  * 字节码指令、字节码指令的执行过程

  * CPython本质

    * 不讨论处理细节，只考虑核心过程，本质上，*CPython是一个*

    * CPython执行过程的高度概括：

      * 读取和检查py文件，并进行解释器和线程状态的初始化；

        * 解释器

          * 解释器状态是一个简单的结构体，结构体中的字段 
          * \*next 引用进程中的另一个解释器状态结构体；
          * \*tstate_head 引用正在执行的线程状态，多线程下引用全局解释器锁；
          * 其余字段有解释器状态所有合作线程共享；

        * 线程

          * 线程结构体包括 next 和 previous 指针，指向该线程之前和之后创建的线程状态；

          * interp字段指向线程状态所属于的解释器状态

          * frame字段为当前执行的栈帧

          * **本质**：

            *  线程状态只是一个数据结构，封装了正在执行的线程的某些状态；

            * 每个线程都与正在执行的python进程内的操作系统线程关联；

            * 关系

              * | Python进程                   | 单进程                                           |
                | ---------------------------- | ------------------------------------------------ |
                | 解释器状态                   | 单进程包含一个或者多个解释器状态                 |
                | 线程状态                     | 每个解释器状态包含一个或多个线程状态             |
                | 操作系统管理的线程（控制流） | 每个线程状态的数据结构映射到操作系统的执行线程上 |

              * 线程状态和OS线程如何映射：OS线程和线程状态在python的threading模块被实例化时创建

              * 所有线程中，同一时间内持有全局解释器锁的线程才能执行虚拟机中的代码对象；

                * 线程由操作系统的**线程控制块**进行调度和资源分派，但是即使系统调度当前没有持有GIL的线程运行，该线程也必须等待获取GIL；

                * 全局解释器锁GIL：

                  * 为了不在虚拟机内实现细颗粒度的各种锁，更明确精细的互斥锁会一定程序降低线程执行效率，简化了虚拟机的实现而存在；

                  *  由于引用计数，GIL提供了堆中对象的线程安全，并且CPython链接的部分共享库并非线程安全；

                  * CPython中GIL的实际工作过程：

                    > GIL 只是一个布尔变量（`gil_locked`），其访问受到互斥锁（`gil_mutex`）的保护，并且其更改由条件变量（`gil_cond`）发出信号。 `gil_mutex` 的使用时间很短，因此几乎没有竞争。在 GIL 保持线程中，主循环（`PyEval_EvalFrameEx`）必须能够根据另一个线程的需要释放 GIL。为此使用了一个临时的布尔变量（`gil_drop_request`），该变量在每次 eval 循环时都会检查。在 `gil_cond` 上等待间隔微秒后，将设置该变量。 【 实际上，使用了另一个临时的布尔变量（`eval_breaker`），该变量将多个条件进行或运算。由于 Python 仅在高速缓存相关的体系结构上运行，因此，可变布尔值就足以作为线程间信号传递的手段。】这鼓励了定义的周期性切换，但由于操作码可能需要花费任意时间来执行，因此不强制执行。用户可以使用Python API  `sys.{get,set}switchinterval()` 读取和修改时间间隔值。当一个线程释放 GIL 并设置了 `gil_drop_request` 时，该线程将确保安排另一个等待 GIL 的线程。它通过等待条件变量（`switch_cond`）直到 `gil_last_holder` 的值更改为其自己的线程状态指针以外的值来进行操作，这表明另一个线程能够使用 GIL。这是为了禁止多核计算机上的延迟潜伏行为，在多核计算机上，一个线程会推测性地释放 GIL，但仍然运行并最终成为第一个重新获取 GIL 的对象，这使得“时间片”比预期的长得多。

      * 将一系列python文件中的代码块进行**”编译“**，生成虚拟机字节码文件（pyc）

      * 其中CPython有一套自己的指令集，这些指令不同于x86指令集这样的直接面向x86架构的CPU的指令集合，这些指令面对CPython内部实现的指令处理过程，这个过程的集合就可以看作为一个虚拟的”机器（机器是泛指其实就是机器处理单元）“

      * 这些指令和参数共同组成了字节码文件，可以将这个字节码文件称为Python虚拟机上的*”经过汇编器汇编后的可重定向目标文件“*

        * 从python源文件到字节码文件的过程包括
          * 生成parse tree
          * parse tree转化为AST抽象语法树
          * 生成符号表
          * AST转化为control flow graph
          * 从control flow graph生成code object

      * Python每个文件中的程序代码由代码块构成，如模块、函数、类定义，CPython的整个编译过程就是从代码块生成**“代码对象的过程”**；

      * 代码对象PyCodeObject在CPython中也是一个和PyObject类似也是一个复杂的结构体，结构体中包含co_stacksize，co_flags，co_zombieframe等字段，被初始化的代码对象的结构体被存储在堆中（在PyMem_NEW(type, n)函数中调用PyMem_MALLOC函数在堆中分配内存空间）；

      * 此时，完成了PyCodeObject的创建之后，解释器启动，创建单个执行主线程(在python虚拟机的过程调用中如果创建新的线程和线程状态，就会堆GIL产生竞争)；

      * 堆中的代码对象的引用被传入解释器循环模块，在执行代码之前，解释器获取到当前代码对象后，会创建一个frame对象

        * frame 对象包含执行代码对象（局部，全局和内置）所需的所有名称空间，对当前执行线程的引用，用于求值字节码的堆栈以及其他对于执行字节码的内部信息；
        * frame对象的概念类似与C中的过程调用无法全部装载到寄存器中的时候，会在运行时栈中修改rsp指针分配栈帧；
        * frame对象在运行时栈中创建并保留部分成员的值，保留其他成员的栈空间，局部变量为空；

      * 类似与C的栈中的rip指针执行栈中的指令，Python虚拟机也在栈中进行过程的执行和返回，相应的指令有相应的过程进行处理（如指令：**`BUILD_LIST`**， **`BUILD_MAP`**， **`BUILD_CLASS`**），每个过程执行完成后，会从栈中弹出；

        >  C中的过程：程序开始阶段，运行时栈的rip（程序计数器指针）指针指向入口函数，然后开始执行，例如执行主函数Q的指令，该指令指向主函数内的过程调用的函数P，这是新的函数P在栈中分配了新的栈帧，该栈帧中的过程返回后，rip指针又指向Q中调用P的那条指令，此时这条指令指向P函数的返回值；

      * 在指令执行过程中创建的全局变量等PyObject也会在堆中初始化，每个数据结构的底层实现都有与之对应的C代码，如dict底层是一个使用**开放寻址法**解决冲突的散列表，并且有特殊的因子进行扩容；

    * 至此，CPython底层虚拟机的运行已经完成了**非常简洁的概括式讨论**，实际上每个部分的实现都有细节和复杂的思想在其中；

    

    > 程序的静态和动态存储空间分配：
    >
    > 1. 静态：编译器在编译阶段基于源代码就可以确定的数据大小
    > 2. 动态：只有在运行时才能确定的数据对象的大小
    >
    > C语言的编译过程中，对于全局或者静态变量这些在编译阶段确定大小的数据结构或为0值的数据结构，会被放入在编译和汇编完成后生成的可重定向目标文件中的.data节和.bss节，链接器会基于符号表中的重定位条目来将这两个节定位到可执行文件的相应的段中；最总装载程序会将这部分数据装载到该程序虚拟内存的读写段（静态区）；
    >
    > 对于一个被调用的过程，在寄存器无法满足参数存储的情况下，会在运行时栈中分配栈帧；
    >
    > 而对于调用malloc进行内存分配的变量会在运行时在堆中创建；
    >
    > 对于CPython程序而言，无法预知将要读取的python文件中的代码段的数量和大小，怎么才能将这些数据读入栈中；
    >
    > 编译器对栈空间分配的要求是：一个数据对象局限于某个过程，且当过程结束后这个对象不可访问；
    >
    > C++利用**”变长数组“**，大小依赖与被调用过程的一个或者多个参数值的数组来将未知大小的对象；
    >
    > 程序的执行过程在生命周期中讨论



## python 底层原理

```
Doc
    The official documentation. This is what https://docs.python.org/ uses. See also Building the documentation.
Grammar
    Contains the EBNF grammar file for Python.
Include
    Contains all interpreter-wide header files.
Lib
    The part of the standard library implemented in pure Python.
Mac
    Mac-specific code (e.g., using IDLE as an OS X application).
Misc
    Things that do not belong elsewhere. Typically this is varying kinds of developer-specific documentation.
Modules
    The part of the standard library (plus some other code) that is implemented in C.
Objects
    Code for all built-in types.
PC
    Windows-specific code.
PCbuild
    Build files for the version of MSVC currently used for the Windows installers provided on python.org.
Parser
    Code related to the parser. The definition of the AST nodes is also kept here.
Programs
    Source code for C executables, including the main function for the CPython interpreter (in versions prior to Python 3.5, these files are in the Modules directory).
Python
    The code that makes up the core CPython runtime. This includes the compiler, eval loop and various built-in modules.
Tools
    Various tools that are (or have been) used to maintain Python. 
```

### python脚本启动分析
#### CPython启动流程
* CPython的.init节包含的entry point为 Programs/python.c main函数，对于不同的平台win和unix/linux会调用不同的Py_Main函数
    * 以python3为例
```C
/* Minimal main program -- everything is loaded from the library */

#include "Python.h"
#include "pycore_pylifecycle.h"

#ifdef MS_WINDOWS
int
wmain(int argc, wchar_t **argv)
{
    return Py_Main(argc, argv);
}
#else
int
main(int argc, char **argv)
{
    return Py_BytesMain(argc, argv);
}
#endif
```
* 对当前操作系统环境进行判断后，Linux上调用Py_BytesMain函数
* Py_BytesMain 函数将输入文件的结构体引用传入pymain_main(&args)
* pymain_main 函数主要会执行一个 pymain_init 和 Py_RunMain
    * pymain_init主要负责
        * _PyRuntime_Initialize(); 初始化python的运行时环境
        * Py_InitializeFromConfig(&config); 初始化python配置文件
        * _PyStatus_OK(); 返回成功后
            * PyConfig_Clear(&config); 清楚配置文件引用
            * 返回status状态
    * 初始化完成后，运行Py_RunMain函数
        * pymain_run_python(int *exitcode), 该函数中比较核心的部分，创建解释器，并获取其结构体指针，配置输入文件路径等；
        * 运行函数分为5种不同的情况
            * pymain_run_command(config->run_command, &cf);
            * pymain_run_module(config->run_module, 1);
            * pymain_run_module(L"__main__", 0);
            * pymain_run_file(config, &cf);
            * pymain_run_stdin(config, &cf);
        * 其中pymain_run_file为运行python文件，对文件进行解释。
            * PySys_Audit 检查文件是否有错误，如果有直接输出并打印
            * _Py_wfopen fp 打开文件，将文件进行编码，这里会判断文件是否能打开
            * PyUnicode_FromWideChar PyUnicode_EncodeFSDefault 将行unicode编码
            * 最终对文件的所有检查和格式化完成后
                * 调用 int run = PyRun_AnyFileExFlags(fp, filename_str, 1, cf); 对文件进行解释执行
                    * PyRun_InteractiveLoopFlags(fp, filename, flags); 此处为执行交互模式
                    * PyRun_SimpleFileExFlags(fp, filename, closeit, flags);  此处为直接开始执行脚本文件
                        * PyObject *m, *d, *v; 创建模块，字典，执行返回值
                        * 判断pyc文件是否存在
                            * v = run_pyc_file(pyc_fp, filename, d, d, flags); 执行pyc文件
                            * v = PyRun_FileExFlags(fp, filename, Py_file_input, d, d, closeit, flags); 执行当前文件
                            * 核心代码
                                * mod = PyParser_ASTFromFileObject(fp, filename, NULL, start, 0, 0,flags, NULL, arena); 将python脚本文件解析为AST文件格式
                                * ret = run_mod(mod, filename, globals, locals, flags, arena); 将AST编译成字节码然后启动字节码解释器执行编译结果
                                * 
```C
    PyInterpreterState *interp = _PyInterpreterState_GET_UNSAFE();
        /* pymain_run_stdin() modify the config */
    PyConfig *config = &interp->config;

    if (config->run_command) {
        *exitcode = pymain_run_command(config->run_command, &cf);
    }
    else if (config->run_module) {
        *exitcode = pymain_run_module(config->run_module, 1);
    }
    else if (main_importer_path != NULL) {
        *exitcode = pymain_run_module(L"__main__", 0);
    }
    else if (config->run_filename != NULL) {
        *exitcode = pymain_run_file(config, &cf);
    }
    else {
        *exitcode = pymain_run_stdin(config, &cf);
    }

    pymain_repl(config, &cf, exitcode);
goto done;
```




[devguide.python](https://devguide.python.org/setup/)
[devguide.python/exploring](https://devguide.python.org/exploring/)
[cpython-source](https://github.com/python/cpython)


```Source

```