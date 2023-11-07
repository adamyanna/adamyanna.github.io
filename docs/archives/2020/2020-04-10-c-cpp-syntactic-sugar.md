---
title: C/C++ Syntactic sugar 语法糖
layout: default
parent: 2020
grand_parent: Archives
---

**C&C++**
{: .label .label-blue }

**Syntactic-Sugar**
{: .label .label-green }

**2020-04-10 10:00:00 +0800**
{: .label .label-yellow }


# C/C++ Syntactic sugar 语法糖

```c++
//Syntactic sugar

#include <iostream>
using namespace std;

int main() {
	// 语法糖
	int a = 0;
	int b = (a++);

	cout << "a: " << a << ", b: " << b << endl;

	a = 0;
	int c = (++a);

	cout << "a: " << a << ", c: " << c << endl;

	/* a++ 和 ++a 都是对a的单调递增，
	但是(a++)和(++a)这两个表达式本身返回值不一样

	++和++i之后都会让i自增

	i++这个整体依然是i
	++i这个整体是i+1
	*/
}
```