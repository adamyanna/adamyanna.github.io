---
title: C programming language recap
layout: default
parent: 2020
grand_parent: Archives
---

**C&C++**
{: .label .label-blue }

**2020-03-16 10:00:00 +0800**
{: .label .label-yellow }


# C recap

###### This file is a recap of programming language C, prepare for C++ learning

```C
#include <stdio.h>  // 引入包含头文件

int main() {	// main 是程序执行的开始
	printf("%s\n", "shit happens");

	return 1;
}
```

### 通用高级语言，为Unix操作系统设计，以B语言为基础

* 结构化
* 处理底层活动
* C11，ISO标准

> /* GCC
> c源代码经过编译转为机器语言（CPU指令）
> 免费开源的编译器GNU的C/C++编译器
> https://gcc.gnu.org/
> https://github.com/gcc-mirror/gcc
> https://zh.wikipedia.org/wiki/GCC

> The GNU Compiler Collection includes front ends for C, C++, Objective-C, Fortran, Ada, Go, and D, as well as libraries for these languages (libstdc++,...). GCC was originally written as the compiler for the GNU operating system. The GNU system was developed to be 100% free software, free in the sense that it respects the user's freedom."GNU's Not Unix!"

> gcc-core、gcc-g++、binutils
> gcc、g++、ar、ranlib、dlltool 

> 编译原理
> LLVM GCC CLANG

> GNU make
> https://hacker-yhj.github.io/resources/gun_make.pdf
> https://www.gnu.org/software/make/manual/make.html#toc-Overview-of-make
> https://www.gnu.org/software/make/



### c程序

* 预处理函数指令

* 函数

* 变量

* 语句&表达式

* 注释

  > 简单了解编译
  > gcc xxx.c 
  > 生成 xxx.out 可执行文件
  > gcc x.c xx.c -o 



### tokens

* 分号
* 注释
* 识符 大写字母或小写字母或下划线开始，后面跟多个字母、下划线、数字
* 关键字，保留关键字
  * auto	变量自动声明
  * break 	跳出当前循环
  * case	switch分支
  * char	声明字符型变量或函数返回类型
  * const	定义常量
  * continue  从continue直接开始下一轮循环
  * default		switch的默认分支
  * do     循环语句执行体
  * double		双精度浮点数声明		64比特	8个字节
  * else	条件语句分支
  * enum	声明枚举类型
  * extern	声明变量或者函数再外部文件
  * float	声明福鼎类型		32比特 4个字节
  * for 	循环
  * goto	无条件跳转
  * if 		条件语句
  * int		整形声明
  * long	长整型声明
  * register	声明寄存器变量
  * return		返回
  * short	短整形
  * signed	声明有符号类型变量或者函数
  * static	静态变量
  * struct  声明结构体类型
  * switch  开关条件语句
  * typedef  给数据类型取别名
  * unsigned  声明无符号类型变量或函数
  * union     声明共用体类型
  * void	声明 无返回或无参数 无类型指针
  * volatile 	变量在执行中被隐含的改变
  * while	循环条件语句
  * _Bool
  * _Complex
  * _Imaginary
  * inline
  * restrict
  * _Alignof
  * _Atomic
  * _Generic
  * _Noreturn
  * _Static_assert
  * _Thread_local
  * 

### 数据类型，类型决定了占用的存储空间（详见体系结构）

1. 基本类型：算数类型，包括整数类型和浮点类型
2. 枚举类型：算术类型，用来定义程序中“只能赋予其一定的离散整数值的变量”
3. void类型：没有可用的值
4. 派生类型； 包括，指针类型、数组类型、结构类型、共用体类型和函数类型

* 数组类型和结构类型统称为聚合类型；

* 函数类型指的是函数返回值的类型；

* 整数类型

  * 类型				存储大小			值范围	A为65  a为97

  * char			1 byte			-128 到 127 或 0 到 255

  * unsigned char	1 byte			0 到 255	    无负值的字符型

  * signed char		1 byte			-128 到 127

  * int				2 或 4 byte		-32,768 到 32,767 或 -2,147,483,648 到 2,147,483,647 32比特位整型和64比特位整型

  * unsigned int	2 或 4 byte		0 到 65,535 或 0 到 4,294,967,295	无负值的整型

  * short			2 byte			-32,768 到 32,767	32比特位整型

  * unsigned short	2 byte			0 到 65,535			无负值的短整型

  * long			4 byte			-2,147,483,648 到 2,147,483,647		64比特位整型

  * unsigned long	4 byte			0 到 4,294,967,295			无负值的长整型

    > i686和x86_64中的存储大小不同，当前操作系统主要以x86_64为主	



* sizeof(type)

* 用来获取某个对象或类型的存储字节大小

* printf() 函数

  * format -- format 标签可被随后的附加参数中指定的值替换，并按需求进行格式化。

  * format 标签属性是 %[flags][width][.precision][length]specifier

    * 格式化输出

      * %d 十进制有符号整数

      * %u 十进制无符号整数

      * %f 浮点数

      * %s 字符串

      * %c 单个字符

      * %p 指针的值

      * %e 指数形式的浮点数

      * %x, %X 无符号以十六进制表示的整数

      * %o 无符号以八进制表示的整数

      * %g 把输出的值按照 %e 或者 %f 类型中输出长度较小的方式输出

      * %p 输出地址符

      * %lu 32位无符号整数

      * %llu 64位无符号整数

        >  https://www.runoob.com/cprogramming/c-function-printf.html

* 浮点类型

  * float		4 byte		1.2E-38 到 3.4E+38		6 位小数
  * double		8 byte		2.3E-308 到 1.7E+308		15 位小数
  * long double	16 byte		3.4E-4932 到 1.1E+4932	19 位小数
  * %E 为以指数形式输出单、双精度实数

* void类型

  * 指定没有可用值

  * 1. 函数返回为空
       function define以 void开头

    2. 函数参数为空
       不接受参数的函数；

    3. 指针指向void
       类型为void *的指针代表对象的地址，指向void的地址，也就是*xx存储了void在内存中的地址；

       

### C 变量

* 定义：变量是程序可操作的存储区的名称；

* C中每个变量都有特定类型，类型决定了变量存储的大小和布局，该范围内的值都可用存储在内存中；

* 变量的名称由字母+数字+下划线组成，以字母或者下划线开始，区分大小写；

  * char 		一个字节，8bit
  * int			整数时最自然的大小
  * float		格式：1bit符号，8bit指数，23bit小数
  * double		格式：1bit符号，11bit指数，52bit小数
  * void  		类型缺失

* C 变量定义

  * 变量定义就是告诉编译器在何处创建变量的存储，以及如何创建变量的存储；
  * 变量定义指定一个数据类型，并包含给类型的一个或者多个变量列表
  * type variable_list
  * 指定类型		变量名称列表

  

```C
int i, j, k;
extern int a = 1, b = 2;
//不带初始化的定义：带有静态存储时间的变量会被隐式初始化为NULL （所有字节的值都为0），其他变量初始值时未定义的；
```



### C 变量声明

* 变量声明向编译器保证变量以指定的类型和名称存在；
* 变量声明在编译时才有意义，在程序连接时编译器需要实际的变量声明；

1. 建立存储空间的变量声明，例如 int a
2. 不需要建立存储空间的变量声明，使用extern关键字声明比变量名而不定义它； extern int a，a被声明但是可能在其他文件中被定义；
   * 除了extern的情况外，变量都是被定义的；
   * 使用extern在一个文件中声明，在另一个文件中引用才会定义；

```C
extern int a;
int b;
```



### 左值和右值 Lvalues  Rvalues

1. 左值 lvalue ： 指向内存位置的表达式被称为左值表达式，可用出现在赋值号的左边或者右边
2. 右值 rvalue ： 存储在内存中的某些地址的数值，只能出现在赋值号的右边；例如，存储在内存某个地址的一个8bit ASC字符
   * 左值： 指向内存位置的表达式



### 常量

* 常量，字面量；
* 值在定义后不能修改；



* 整数常量
  * 十进制、八进制、十六进制的常量；
  * 前缀指定基数：0x或0X表示十六进制，0表示八进制，不带默认表示十进制；
  * 后缀U表示无符号整数（unsigned）
  * 后缀L表示长整数（long）
  * 后缀可用大写也可以小写；

* 浮点常量
  * 整数部分、小数点、小数部分、指数部分组成；
  * 使用小数形式或者指数形式来表示
  * 指数符合e\E
  * 指数形式要包括小数点或者指数

* 字符常量
  * 使用 ‘单引号’ 存储在char类型的变量里；指向内存地址的可操作区域的名称，指向内存地址的表达式
  * 转义符
    * \\	\ 字符
    * \'	' 字符
    * \"	" 字符
    * \?	? 字符
    * \a	警报铃声
    * \b	退格键
    * \f	换页符
    * \n	换行符
    * \r	回车
    * \t	水平制表符
    * \v	垂直制表符
    * \ooo	一到三位的八进制数
    * \xhh . . .	一个或多个数字的十六进制数



* 字符串常量
  * 字符串在“双引号中”



* 常量定义
  * #define
  * const
  * 代码规范：使用大写表示常量

```C
#define identifier value; // 预处理定义  标识符  值

#define TIMEOUT 30;

const type variable = value; // 常量定于 	类型定义	  变量名称（指向内存可操作区）  变量值（可操作区存储该值)
```




### 存储类

* 存储类定义C中变量和函数的范围（可见性）和生命周期；
* 放在所修饰的类型之前；
  * auto
  * register
  * static
  * extern



* auto存储类

  * 是所有局部变量的默认存储类；

  ```C
  {
  	int m;
  	auto int m; // 上面两个带有相同的存储类，auto只能用于函数内，只能修饰局部变量；
  }
  ```

  

* register 存储类

  * 定义存储在寄存器中而不是RAM中的局部变量；
  * 变量的最大size为寄存器的size；
  * 通常为1个词，不能对它应用一元“&” 运算符，因为变量没有内存位置

  ```C
  {
  	register int s; // 寄存器用于需要快速访问的变量，例如计数器
  // 定义‘register’ 并不会绝对将变量存储在寄存器内，取决于硬件的实际限制；
  }
  ```

  

* static 存储类

  * 编译器在程序生命周期内保持局部变量的存在，而不需要在每次进入和离开作用域时都进行创建和销毁；
    static 修饰局部变量可用在函数调用之间保持局部变量的值；
  * static 修饰符也可以用于全局变量，**修饰全局变量时，会使得变量的作用域限制在声明它的文件中；**
  * 全局声明的一个static变量或者方法，可以被任何函数或者方法调用；前提时这些变量和方法与static全局变量在同一个文件中；

  ```C
  static int c = 999; // 全局变量 - static 是默认的
  
  void func1(void) {
  	static int t = 1; // t 是函数func的局部变量，使用static后，该变量在函数第一次被调用时初始化，以后每次都不会在被重置；  // 在程序的生命周期内会永远保留该局部变量的值；
  	t ++;
  	printf("%d %d\n", t, c);
  }
  ```

  

* extern 存储类

  * extern 存储类用于提供一个全局变量的引用，全局变量被extern修饰后，在程序的所有文件都可见；
    使用extern，对于无法初始化的变量（相同变量名称已经在其他文件中定义过，extern声明会直接声明定义过的这个变量的地址），会把变量名指向之前定义过的一个存储位置；
  * 多个文件中定义了一个可以在其他文件中使用的全局变量或函数时，可以在其他文件中使用extern来得到已经定义的变量或函数的引用（引用就是存储了变量地址的表达式，而指针变量是存储了变量地址的变量的地址的表达式）

  ```C
  // main.c
  
  #include <stdio.h>
  
  int count;
  extern void fun_from_another_file(void);  //声明外部函数，函数定义在其他文件中
  
  int main(int argc, char const *argv[])
  {
  	/* 可以直接使用本文件定义的静态全局变量 count */
  	return 0;
  }
  
  // 该文件中可以使用定义的外部全局函数
  ```

  

### 运算符

* 算数运算符
* 关系运算符
* 逻辑运算符
* 位运算符
* 赋值运算符
* 杂项运算符



* 算数运算符

  * /	分子除以分母	 

  * %	取模运算符，整除后的余数 

  * ++	自增运算符，整数值增加 A++  

  * --	自减运算符，整数值减少 A--  

* 关系运算符
  * ==	检查两个操作数的值是否相等，如果相等则条件为真。	(A == B) 为假。
  * !=	检查两个操作数的值是否相等，如果不相等则条件为真。	(A != B) 为真。

>		检查左操作数的值是否大于右操作数的值，如果是则条件为真。	(A > B) 为假。
>	
>	<	检查左操作数的值是否小于右操作数的值，如果是则条件为真。	(A < B) 为真。
>	=	检查左操作数的值是否大于或等于右操作数的值，如果是则条件为真。	(A >= B) 为假。
>	<=	检查左操作数的值是否小于或等于右操作数的值，如果是则条件为真。	(A <= B) 为真。



* 逻辑运算符

  * &&	称为逻辑与运算符。如果两个操作数都非零，则条件为真。	(A && B) 为假。
  * ||	称为逻辑或运算符。如果两个操作数中有任意一个非零，则条件为真。	(A || B) 为真。
  * !	称为逻辑非运算符。用来逆转操作数的逻辑状态。如果条件为真则逻辑非运算符将使其为假。	!(A && B) 为真。

  

* 位运算符

  * &	

    * 按位与操作，按二进制位进行"与"运算。运算规则：

  * |	

    * 按位或运算符，按二进制位进行"或"运算。运算规则：

  * ^	

    * 异或运算符，按二进制位进行"异或"运算。运算规则： 寄存器中的加法运算，就是用异或，“二进制的不进位相加”

  * ~	

    * 取反运算符，按二进制位进行"取反"运算。运算规则：一个有符号二进制数的补码形式。

      > 原码：原码就是符号位加上真值的绝对值, 即用第一位表示符号, 其余位表示值. 比如如果是8位二进制:
      > 反码：正数的反码是其本身； 负数的反码是在其原码的基础上, 符号位不变，其余各个位取反.
      > 补码：正数的补码就是其本身； 负数的补码是在其原码的基础上, 符号位不变, 其余各位取反, 最后+1. (即在反码的基础上+1)
      > https://www.cnblogs.com/zhangziqiu/archive/2011/03/30/computercode.html
      > 机器中码的处理，体系结构

  * <<	

    * 二进制左移运算符。将一个运算对象的各二进制位全部左移若干位（左边的二进制位丢弃，右边补0）。	

  * \> \> 

    * 二进制右移运算符。将一个数的各二进制位全部右移若干位，正数左补0，负数左补1，右边丢弃。



### 赋值运算符

* =	简单的赋值运算符，把右边操作数的值赋给左边操作数	C = A + B 将把 A + B 的值赋给 C
* +=	加且赋值运算符，把右边操作数加上左边操作数的结果赋值给左边操作数	C += A 相当于 C = C + A
* -=	减且赋值运算符，把左边操作数减去右边操作数的结果赋值给左边操作数	C -= A 相当于 C = C - A
* *=	乘且赋值运算符，把右边操作数乘以左边操作数的结果赋值给左边操作数	C *= A 相当于 C = C * A
* /=	除且赋值运算符，把左边操作数除以右边操作数的结果赋值给左边操作数	C /= A 相当于 C = C / A
* %=	求模且赋值运算符，求两个操作数的模赋值给左边操作数	C %= A 相当于 C = C % A
* <<=	左移且赋值运算符	C <<= 2 等同于 C = C << 2
* \>\>=	右移且赋值运算符	C >>= 2 等同于 C = C >> 2
* &=	按位与且赋值运算符	C &= 2 等同于 C = C & 2
* ^=	按位异或且赋值运算符	C ^= 2 等同于 C = C ^2
* |=	按位或且赋值运算符	C |= 2 等同于 C = C | 2




### 杂项运算符

* sizeof()	返回变量的字节大小 	sizeof(a) 将返回 4，其中 a 是整数。
  &	返回变量的地址 取地址符	&a; 将给出变量的实际地址。
* \* 指向一个变量  指针变量声明	*a; 将指向一个变量。
  ? :	 三元表单式  条件表达式	如果条件为真 ? 则值为 X : 否则值为 Y   x == y ? return x : return y




### 运算符优先级

* 上到下 -> 高到低
  * 后缀 	() [] -> . ++ - -  	从左到右 
  * 一元 	+ - ! ~ ++ - - (type)* & sizeof 	从右到左 
  * 乘除 	* / % 	从左到右 
  * 加减 	+ - 	从左到右 
  * 移位 	<< >> 	从左到右 
  * 关系 	< <= > >= 	从左到右 
  * 相等 	== != 	从左到右 
  * 位与 AND 	& 	从左到右 
  * 位异或 XOR 	^ 	从左到右 
  * 位或 OR 	| 	从左到右 
  * 逻辑与 AND 	&& 	从左到右 
  * 逻辑或 OR 	|| 	从左到右 
  * 条件 	?: 	从右到左 
  * 赋值 	= += -= *= /= %=>>= <<= &= ^= |= 	从右到左 
  * 逗号 	, 	从左到右 

### 判断语句

* if
* if  else
* 嵌套if
* switch
* 嵌套switch
* condition ? block1 : block2;

```C
if ()
{

}else {

}

switch () {
	case :
	case :
	default :

}

// case 关键字后面必须是一个整数，或者是结果为整数的表达式，但不能包含任何变量，
```



### 循环

* while
* for
* do while 循环,检查条件放在尾部while中
* break
* continue
* goto

```C
while (){

}

do
{
	/* code */
} while (/* condition */);

// 无限循环

for ( ; ; )
{
	/* code */
}
//  Ctrl + C 发送终止信号
```



### 函数

* 每个函数包含一组执行特殊任务的语句
* 声明：函数名称、返回类型、参数定义：函数主题
* 内置函数
* function method

```C
return_type function_name( parameter list)
{
	body of functon
}
```

>  A parameter is a variable in a method definition.
>  When a method is called, the arguments are the data you pass into the method's parameters.
>  Parameter is variable in the declaration of function.
>  Argument is the actual value of this variable that gets passed to function.

* Argument：实参，函数调用时传入的实际参数，实际参数
* parameter：形参，函数定义时定义的参数名称，形式参数



### 函数调用

```C
function_name(parameter1, parameter2)
```

* 传值调用	该方法把参数的实际值复制给函数的形式参数。在这种情况下，修改函数内的形式参数不会影响实际参数。
* 引用调用	通过指针传递方式，形参为指向实参地址的指针，当对形参的指向操作时，就相当于对实参本身进行的操作。
* C 使用传值调用来传递参数。一般来说，这意味着函数内的代码不能改变用于调用函数的实际参数。

> 函数调用，直接传入参数的过程为传值调用
> 函数调用，传入指针变量的过程为引用调用，形参为指向实参的地址的指针；



### C 作用域规则

* 作用域是程序中定义的变量所存在的区域

1. 函数或者块内部的局部变量
2. 所有函数外部的全局变量
3. 形式参数的函数参数定义中

* 局部
* 全局
* 形式



* 局部

  * 某个函数或者块的内部声明的变量为“局部变量”
  * 只能被该函数或者该代码块使用
  * auto存储类

* 全局变量

  * 定义在函数的外部，程序顶部
  * 整个程序的生命周期内都有效
  * 在任意函数内部访问，可以使用static、extern存储类
  * 函数中，同名的局部变量和全局变量，函数会使用局部变量

* 形式参数

  * 函数声明和函数定义时，定义的入参，为形式参数
  * 在函数内部也是局部变量

* 初始化

  * 系统不会初始化局部变量

  * 系统会自动对全局变量进行初始化

    * | int     | 0    |
      | ------- | ---- |
      | char    | '\0' |
      | float   | 0    |
      | double  | 0    |
      | pointer | NULL |



### C数组

* 存储一个固定大小的相同类型元组的有序集合

* 通过索引访问元素

* 声明数组

  ```C
  type arrayName [arraySize] //一维数组，arraySize必须大于0
  double a1[10]
  char a2[10]
  int a3[10]
  char * a4[10]
  ```

* 数组初始化

  ```c
  int a1[] = {1, 2, 3};	//初始化大小为{}之间的数目
  int a2[5] = {1, 3};	// 初始化大小为5，index0为1，index1为3
  a2[4] = 9;
  a2[0] = 999;
  ```

* 多维数组

  ```C
  // 形式
  type name[size1][size2]; //二维数组
  type name[size1][size2][size3]; //三维数组
  
  //二维数组初始化
  int a[3][3] = {
      {1,2,3},
      {4,5,6},
      {7,8,9}
  }
  
  int a[3][3] = {
      1,2,3,4,5,6,7,8,9
  }
  ```

* 数组参数传递

  ```C
  // 指针
  void func(int *array){
      
  }
  
  // 形参传递拷贝
  void func(int array[10]) {
      
  }
  
  void func(int array[]){
      
  }
  
  // 函数返回数组
  int * func() {
      
  }
  ```

* 指针指向的数组

  * 数组名称： 指向数组中第一个元素的地址

  ```C
  double a[8]; // a 存储的是 a[0] 元素的地址，也就是a指向&a[0]
  double * p;
  p = balance;
  // 数组名称作为指针是合法的
  *(a + 4); // 使用间接访问运算符访问数组中的第5个元素，从a的地址向后4段地址 等同于 a[4]
  *(p) *(p+1) *(p+2)；
  ```

  

### 枚举 enum

* 基本数据类型

> 基本、枚举、void、派生

```C
enum 枚举名 {枚举元素1,枚举元素2,枚举元素3...};

enum WEEK {  //定义了一个类型为 WEEK 的枚举类型
    MON = 1,
    TUE,
    WED,
    THU,
    FRI,
    SAT,
    SUN
};

enum WEEK w; // 定义了 WEEK 枚举类型的一个变量

enum WEEK {  // 同时定义了类型为 WEEK 的枚举类型，和变量week
    MON = 1,
    TUE,
    WED,
    THU,
    FRI,
    SAT,
    SUN
} week;


enum {  // 省略枚举名， 直接定义变量week
    MON = 1,
    TUE,
    WED,
    THU,
    FRI,
    SAT,
    SUN
} week;

int main() {
    for (week = MON; week <= SUN; week ++) {
        printf("%d\n", week)
    }
}

// C中枚举为int 或者 unsigned int
```

* 第一个枚举成员的默认值为整型0，后面每一个成员在前一个成员+1；

* 可以在定义枚举的时候改变元素的值，其后的值还是会在前面的基础加1；

* 通过枚举类型定义枚举变量，枚举类中的元素可以直接赋值给枚举变量；

* 枚举列表中的 Mon、Tues、Wed 这些标识符的作用范围是全局的，不能再定义与它们名字相同的变量。

*  Mon、Tues、Wed 等都是常量，不能对它们赋值，只能将它们的值赋给其他的变量。

  >  枚举和宏其实非常类似：宏在预处理阶段将名字替换成对应的值，枚举在编译阶段将名字替换成对应的值。我们可以将枚举理解为编译阶段的宏。

  枚举的元素的访问方式，是将枚举变量

* 它们不占用数据区（常量区、全局数据区、栈区和堆区）的内存，而是直接被编译到命令里面，放到代码区，所以不能用`&`取得它们的地址。这就是枚举的本质。



### 指针



### 函数指针

* 指向函数的指针变量

```C
typedef int (*func)(int,int);  //函数指针的声明

int (* funcP)(int) = &anotherFunc; //声明一个函数指针，保持另一个函数的地址
```

* 回调函数
  * 函数指针作为某个函数的参数
  * 回调函数：将"函数指针"作为参数传入新的函数，新的函数执行时某种条件触发后，调用传入的函数；



### 字符串

* 使用NULL字符 **'\0'** 终止的一位**字符数组**
* 数组末尾存储了”空字符”，数组大小比存储的字符串大1

``` C
char string[] = 'hello';
char string[] = {'h', 'e', 'l', 'l', 'o','\0'}; //C 编译器会在初始化数组时，自动把 '\0' 放在字符串的末尾
```

* 字符串操作的函数

  | 函数 & 目的                                                  |
  | :----------------------------------------------------------- |
  | **strcpy(s1, s2);** 复制字符串 s2 到字符串 s1。              |
  | **strcat(s1, s2);** 连接字符串 s2 到字符串 s1 的末尾。       |
  | **strlen(s1);** 返回字符串 s1 的长度。                       |
  | **strcmp(s1, s2);** 如果 s1 和 s2 是相同的，则返回 0；如果 s1<s2 则返回小于 0；如果 s1>s2 则返回大于 0。 |
  | **strchr(s1, ch);** 返回一个指针，指向字符串 s1 中字符 ch 的第一次出现的位置。 |
  | **strstr(s1, s2);** 返回一个指针，指向字符串 s1 中字符串 s2 的第一次出现的位置。 |



### 结构体

* 允许存储不同类型的数据

* 结构的定义，必须使用struct语句，struct语句定义了一个包含多个成员的**新的数据类型**；

  ```C
  stuct tag {
      member-list
     	member-list
      ...
  } variable-list;
  
  // tag是结构体标签
  // member-list 是标准的变量定义
  // variable-list 结构变量，定义在结构的末尾，最后一个分后前，可以指定一个或多个结构变量；
  // tag、member-list、variable-list 这 3 部分至少要出现 2 个
  // 结构体类型、结构体变量、结构体成员
  
  // 没有类型标签
  struct
  {
      int a;
      char b;
      double c;
  } s1;
  
  // 没有声明变量
  struct SIMAPLE {
      int a;
      char b;
      double c;
  };
  
  // 声明结构体变量
  struct SIMPLE t1, t2[10], *t3;
  // 结构体SIMPLE变量，结构体SIMPLE变量赋值到t2数组索引10处，结构体SIMPLE指针类型变量
  
  // 使用typedef 创建结构体类型
  typedef struct
  {
      int a;
      char b;
      double c;
  } Simple2;
  
  ```

  * 结构体成员可以包含其他结构体；可以包含指向自己结构体类型的指针（链表，二叉树）；
  * 如果两个结构体互相包含，则需要对其中一个结构体进行不完整声明；

* 结构体变量的初始化

  * 结构体成员变量可以在定义时指定初始值；

* 访问结构成员

  * **(.)**, 成员访问运算符；来访问结构体的成员变量 

* 结构体作为函数参数

  * 指针类型传参或者变量类型传参

* 指向结构体的指针

  ```C
  struct NewStruct * s;
  s = &new1;
  // 指针指向成员变量
  s->title;
  printf("%s\n", s->title)
  ```

* 位域

  * 实现把一个字节的二进制bit划分为几个不同的区域，并且说明每个区域的位数；
  * 一个存储了指定比特数的成员变量的数据结构；
  * 每个域位有一个“域名”，允许按域名操作，实现把几个不同对象的二进制按照位域来表示；
    * 例如，状态开关，一个比特来表示 0， 1
    * 读取非标准文件格式

  ```C
  struct 位域结构名称
  {
      位域列表
  };
  
  struct B{
      int a:8;
      int b:4;
      int c:4;
  }data;
  // 类型B的变量data，共占用16比特，两个字节，域a占8位，域b占4位，域c占4位；
  ```

  * 一个位域存储在同一个字节中，如一个字节所剩空间不够存放另一位域时，则会从下一单元起存放该位域。也可以有意使某位域从下一单元开始。
  * 由于单个位域不允许跨两个字节，因此位域的长度不能大于一个字节的长度，也就是说不能超过8位二进位。如果最大长度大于计算机的整数字长，一些编译器可能会允许域的内存重叠，另外一些编译器可能会把大于一个域的部分存储在下一个字中。
  * 位域可以是无名位域，这时它只用来作填充或调整位置。**无名的位域是不能使用的**；

* 本质上是一种结构类型，成员按照二进制分配；

* 使用

  * ```
    位域变量名.位域名
    位域变量名->位域名
    ```



### C 共用体

* 共用体，允许成员共用相同的内存位置，且成员可以是不同类型；但是任何时间只能有一个成员**有值**

* 共用体，提供了一种在同一段内存空间存储不同类型的值的方式；

* 定义

  ```C
  union [union tag] {
      member definition;
      member definition;
      ...
  }[one or more union variables];
  
  // union tag 是可选择，定义一个union类型
  // 每个 member 都是标准的变量定义
  // 定位的末尾可以指定多个共用体变量
  
  // i f str
  union Data
  {
  	int i;
  	float f;
  	char str[20];
  } data;
  
  // Data类型的共用体可以存储一个整数，一个浮点数，或者一个字符串；可以在共用体中使用自定的数据结构
  // 共用体占用的内存要足够存储共用体中最大的成员
  ```

* 访问共用体成员

  * **(.)**, 成员访问运算符；来访问共用体内部的成员
  * 同一时间只有一个成员能够存储值，其他成员会指向数据类型默认值；

















































[C学习](http://c.biancheng.net/cpp)