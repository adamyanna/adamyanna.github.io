---
title: Python automation
layout: default
parent: Cloud Native Automation
grand_parent: Jq
---

# Python automation

## Basic

### What is Python
* object-oriented
* interpreter code at run time, no compile
* multiple platforms support
* also support use as procedural

> 面相对象 & 解释器无需编译 & 实时运行结果 & 可以当作过程语言使用，例如非过程脚本

* Deep Dive: [Understand the CPython interpreter implementation](https://adamyanna.github.io/docs/archives/2020/2020-04-13-cpython-implementation/#%E8%BF%9B%E5%85%A5%E6%BA%90%E4%BB%A3%E7%A0%81%E5%88%86%E6%9E%90%E4%B9%8B%E5%89%8D)

### Syntax

#### 1. Dot notation `[object we want to access][dot][attribute or method]` 
> Dot notation is a feature in object-oriented programming languages like Python that allows you to search an extensive database for an object's attributes and methods. In Python, dot notation is written as: [object we want to access][dot][attribute or method]
> 
> 点计法语法
> 
> 每一个模块，通过点后加变量名来获取变量值，例如 os.name
> 
> 每一个模块，通过点后加函数名称（必须加括号，无入参的情况下括号内为空）来获取函数结果，例如：os.getcwd()
```python
# get value from variable
object.var
# call method
object.this_is_a_method()
```

#### Python Indentation `Python uses indentation to indicate a block of code.`
> Tabs or Spaces? Spaces are the preferred indentation method. Tabs should be used solely to remain consistent with code that is already indented with tabs. Python disallows mixing tabs and spaces for indentation.

> 冒号 + tab / 四个空行，来标识代码区块，如果使用 tab 需要全部项目内保持一直，一般建议使用 tab 输出四个空格的编辑器
```python
if 10 > 1:
    print("Hello")
```

#### Object-oriented

> Class: A Class is like an object constructor or template, or a "blueprint" for creating objects.
> 
> Object: Almost everything in Python is an object, with its properties and methods. (including Class)
> 
> Instance: A implementation of Class, with all class properties but has specific values.
>
> Self: The self parameter is a reference to the current instance of the class, and is used to access variables that belongs to the class.
> 
> Method: Give input values to output result, with a Class, used by all instances.
> 
> Variable: Hold a specific type of value;


> 类：class HelloWorld
>
> 实例（类的实例）：定义一个类型表示定义了一种抽象，将这种抽象具体成一个可访问的内存对象的过程就是类的实例化：ob = HelloWorld()
> 
> 对象：object 任何类的实例，以及实例的方法、变量都可以被称作对象，python 根类就是 object，通常无需继承 
> 
> 方法 method：在类中 def 的一种接收入参和输出参数的函数，将其称为方法：method 
> 
> 函数 function：直接在 py 文件中定义的 def 函数，不属于任何类型和对象，直接就叫做 function

```python
# This is a Class definition
class ThisIsMyClass():
    def __init__(self, first_input_var):
        """
        three quota is Doc string for document purpose
        init: default method for Class to init a specific instance
        self: current instance itself
        first_var: initial variable from instance init
        self.first_var: class property
        """
        self.first_var = first_input_var

    def get_sum(self, second_var):
        """
        This is a method, with an input
        return: sum of current instance property first_var and new input
        """
        return self.first_var + second_var

ins = ThisIsMyClass(10)
result = ins.get_sum(100)
print("=> %d" % result)
```

* Deep Dive: [Python Classes and Objects](https://www.w3schools.com/python/python_classes.asp)

## The Python Standard Library
https://docs.python.org/3/library/index.html
* os - Miscellaneous operating system interfaces
  * Often use:
    * os.name
    * os.getcwd()
    * 



## Automation 3rd part Library
* requests - API test
* flash - lightweight API server 
* json - json serializer (convert byte flow to json object)
* pymongo - mongoDB (ORM)


## Used For
* Web Server & Restful API
* RPC
* DataBase Access
  * ORM: Object–relational mapping, convert database relational data to objects of python
* Linux Command Access
* Cacheing System Access