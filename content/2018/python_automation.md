# Python Automation

> 2018

## What is Python

Python is an object-oriented, interpreted language — no compilation needed, runs in real time, and supports multiple platforms. It can also be used as a procedural language (e.g., for scripting without classes or objects, using simple function calls).

## Deep Dive: Understanding CPython Interpreter & Syntax

### 1. Dot Notation

Dot notation is a feature in object-oriented programming languages like Python that allows you to search an extensive database for an object's attributes and methods. In Python, dot notation is written as: `[object].[attribute or method]`

Each module exposes its variables through dot notation (e.g., `os.name`). Methods are called by appending the function name with parentheses after the dot (e.g., `os.getcwd()`).

```python
# Get value from variable
object.var
# Call method
object.this_is_a_method()

```

### 2. Python Indentation

Python uses indentation to indicate a block of code. Spaces are the preferred indentation method. Tabs should be used solely to remain consistent with code that is already indented with tabs. Python disallows mixing tabs and spaces for indentation.

Use a colon + tab or four spaces to identify code blocks. If using tabs, maintain consistency across the entire project. Editors configured to emit spaces when pressing Tab are generally recommended.

```python
if 10 > 1:
    print("Hello")

```

### 3. Object-Oriented Programming

- **Class**: A blueprint or template for creating objects (`class HelloWorld`)
- **Instance**: A concrete realization of a class — defining a type creates an abstraction; instantiating it allocates a memory-accessible object (`ob = HelloWorld()`)
- **Object**: Any class instance, its methods, and its variables. Python's root class is `object`; explicit inheritance is usually unnecessary
- **Method**: A `def` function within a class that accepts input parameters and returns output — referred to as a method
- **Function**: A `def` function defined directly in a `.py` file, not belonging to any class or object
- **Self**: The `self` parameter references the current instance of the class and is used to access variables belonging to that class
