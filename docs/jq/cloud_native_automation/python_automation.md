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

> 面相对象 & 解释器无需编译 & 实时运行结果 & 可以当作过程语言使用 (例如过程脚本, 不考虑类和对象，只需要实现简单的函数调用)

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

#### 2. Python Indentation `Python uses indentation to indicate a block of code.`
> Tabs or Spaces? Spaces are the preferred indentation method. Tabs should be used solely to remain consistent with code that is already indented with tabs. Python disallows mixing tabs and spaces for indentation.

> 冒号 + tab / 四个空行，来标识代码区块，如果使用 tab 需要全部项目内保持一直，一般建议使用 tab 输出四个空格的编辑器
```python
if 10 > 1:
    print("Hello")
```

#### 3. Object-oriented

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

---

## The Python Standard Library
https://docs.python.org/3/library/index.html
### os - Miscellaneous operating system interfaces
* Often use
> just import `library` no need handle path with `from` state

```python
import os
# get separator from OS, windows return \ linux & unix return / 
os.sep

# get os kernel name, windows return nt, linux & unix return posix
os.name

# get current work directory or current work path (initial directory is current py file's path)
os.getcwd()

# get current environment variable, for EXAMPLE: os.getenv('path')
os.getenv()
os.getenv('path')

# get & alter current environment variable
os.environ
print(os.environ['PATH'])
os.environ += '/usr/bin/zsh'
print(os.environ['PATH'])

os.environ # is type of python dict

# list for directory and file names for current work directory or input path
os.listdir()
os.listdir('/root')

# remove files
os.remove()
os.remove('/root/test.txt')

# run cmd or command line for system
os.system('ip addr')

# get current platform end with line, windows is \r \n, linux is \n, mac is \r
os.linesep

# split a path for file name and directory
path = '/root/test/test.txt'
print(os.path.split(path)[0])
print(os.path.split(path)[1])

# check is a string is file, return type of bool (boolean True or False)
os.path.isfile('root/test/test.txt')

# check if a string is path, return type of bool
os.path.isdir('/root')

# check if path exists, return type of bool
os.path.exists('/root')

# equivalent to: cd, change current working directory
os.chdir()

# get file size with byte, return float
os.path.getsize('/root/test.txt')

# get absolute path of a file
os.path.abspath()
os.path.abspath('test.txt')

# normalize file path, convert sep & etc
# get a clean string of path 
os.path.normpath()
print(os.path.normpath("/users/test//"))

# get a tuple of file and file extension, (go to #extra info 1)
print(os.path.splitext('/user/test/test.txt'))
# result >>>
('/user/test/test', '.txt')

# 
```

---

> *extra info 1*

|list| tuple |
|:---|:------|
|List are mutable| Tuples are immutable |
|Iterations are time-consuming| Iterations are comparatively Faster |
|Inserting and deleting items is easier with a list.| Accessing the elements is best accomplished with a tuple data type. |

---

### open - open file convert to python object to write and read
> open() function takes up to 3 parameters – the filename, the mode, and the encoding.

* `with`
> This is because the with statement calls 2 built-in methods behind the scene – __enter()__ and __exit()__.

> The __exit()__ method closes the file when the operation you specify is done.

```python
# open a file
this_file = open('text.txt')
print(this_file.read())
this_file.close()

with open('test.txt') as this_file:
    pass
    # do any reading or writing for the file

####################################################################
# with statement closes the file for you without you telling it to #
####################################################################

with open("hello.txt", "w") as my_file:
    my_file.write("Hello world \n")
    my_file.write("I hope you're doing well today \n")
    my_file.write("This is a text file \n")
    my_file.write("Have a nice time \n")

with open("hello.txt") as my_file:
    print(my_file.read())

# Output: 
# Hello world 
# I hope you're doing well today
# This is a text file
# Have a nice time
```

## Automation 3rd part Library
### 1. Web Server & Restful API
* requests
  - API request
* flask
  - lightweight API server
* json
  - json serializer (convert byte flow to json object)

### 2. DataBase Access - ORM
> ORM: Object–relational mapping, convert database relational data to objects of python
* pymongo
  - mongoDB (ORM) 

### 3. Cacheing System Access
* memcache
* redis

### 4. Linux Command Access
* ansible