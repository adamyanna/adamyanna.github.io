---
title: Algorithm Everything
author: Teddy
date: 2020-02-18 10:00:00 +0800
categories: [实践, 算法训练]
tags: [Algorithm]
---

# 经验

## 1. 提问

1. 主要负责内容
>  云网络监控
2. 具体项目描述
>
3. 什么样的架构
> server+agent的分布式架构，每个可用去会规划两台裸金属的物理机作为监控agent节点，每台物理机会启动多个agent将采集压力负载到每个agent上，并且agent采用了心跳模式的高可用和监控；
4. 用了什么框架
> server使用的是python2的tornado框架
> tornado框架和核心是什么

> epoll
> epoll linux: linux多路复用技术可以处理数以百万计的socket句柄
> poll和select epoll的提升和区别
> 多路复用IO(I/O Multiplexing)

> 多路复用模型 select epoll
> 


> 句柄与普通指针的区别在于，指针包含的是引用对象的内存地址，而句柄则是由系统所管理的引用标识，该标识可以被系统重新定位到一个内存地址上。这种间接访问对象的模式增强了系统对引用对象的控制。（参见封装）。通俗的说就是我们调用句柄就是调用句柄所提供的服务，即句柄已经把它能做的操作都设定好了，我们只能在句柄所提供的操作范围内进行操作，但是普通指针的操作却多种多样，不受限制。
>

```python
# https://www.jiqizhixin.com/articles/2019-04-10-15
# 前面一部分Torando.ioloop是Tornado的核心模块ioloop模块，IOLoop是ioloop模块的一个类，current()是IOLoop类的一个方法，结果是返回一个当前线程的IOLoop的实例，start()也是IOLoop的方法，调用后开启循环。
tornado.ioloop.IOLoop.current().start()
```

5. 数据处理的模式

6. 负载均衡用了什么




# 基础

## 各种排序算法和查找算法
1. 快速排序
2. 冒泡排序
3. 选择排序
4. 直接插入排序
5. 归并排序
6. 堆排序
7. 希尔排序
8. 基数排序
9. 二叉树排序
10. 计数排序

1. 二分查找

## 数据结构基础

1. 队列
2. 栈
3. 链表
> 单向链表，双向链表，单向链表存储当前值和下一个节点的指针或着引用，双向链表会多存储一个前一个节点的指针或着引用。
4. 哈希表
5. 二分查找
6. 二叉树
> 二叉树搜索， 任意节点的左子树不空，则左子树上所有结点的值均小于它的根结点的值；
> 任意节点的右子树不空，则右子树上所有结点的值均大于它的根结点的值；
> 任意节点的左、右子树也分别为二叉查找树；
> 没有键值相等的节点。
> 二叉查找树相比于其他数据结构的优势在于查找、插入的时间复杂度较低。为O(log n)。二叉查找树是基础性数据结构，用于构建更为抽象的数据结构，如集合、multiset、关联数组等。

7. 图
图、连通图、图的基本算法：
数据结构中有三种关系，一对一，一对多，多对多
一对一： 线性结构数组、栈、队列、链表、哈希表
一对多：树结构，二叉树、三叉树
多对多：图


# TODO
二叉树的数据结构的实现和各种遍历方式

7. 二叉搜索树
8. N叉树

https://leetcode-cn.com/explore/


## 数据库

## shell

## 多线程

## 递归

## 机器学习

# 动手

https://teddygoodman.github.io/

# 进阶
* 动态规划
https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/solution/yi-ge-fang-fa-tuan-mie-6-dao-gu-piao-wen-ti-by-l-2/

* 递归：画出递归树 [递归树](https://www.cnblogs.com/wu8685/archive/2010/12/21/1912347.html)
* 

# 算法学习总结
> 常用方法总结：
> 贪心算法 贪心算法的思想是每一步都选择最佳解决方案，最终获得全局最佳的解决方案。
> 

> 常用时间复杂度：O(n log(n))   O(n^2) O(n) O(1) O(n^2) O(n+k) O(nk) O(n!) O(max(m, n)) O(log(m + n)) O(max(m, n))

### Company - Microsoft
1. 两数之和，给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。
```
Solution: 一次遍历 1. 初始化一个字典 2. 一次遍历 numns 并获取 target 与每个遍历值的差值 3. 检查差值是否在已经初始化的目标字典中，存在则返回字典值
> T: O(n) S: O(n)
```

2. 两数相加，给出两个 非空 的链表用来表示两个非负的整数。其中，它们各自的位数是按照 逆序 的方式存储的，并且它们的每个节点只能存储 一位 数字。两个数相加起来，则会返回一个新的链表来表示它们的和。(2 -> 4 -> 3) + (5 -> 6 -> 4) 输出：7 -> 0 -> 8
```
> Solution: 一次遍历，遍历次数为最长链表 1. 初始化一个结果链表 2. 使用while循环，操作两个链表（假设输入链表为m n），m和n都存在时，与结果非0相加，如果相加值大于10，则将结果的next设置为1，如果其中一个链表为空，则循环非空链表，并将值加到结果链表上
> T: O(max(m, n))  S: O(max(m, n))
```

3. 寻找两个有序数组的中位数, 给定两个大小为 m 和 n 的有序数组 nums1 和 nums2。请你找出这两个有序数组的中位数，并且要求算法的时间复杂度为 O(log(m + n)) 你可以假设 nums1 和 nums2 不会同时为空。(中位数，统计学，将一个集合划分为两个长度相等的子集，其中一个子集中的元素总是大于另一个子集中的元素。)
```
> Solution: 二叉树搜索算法，对num1和nums2生成两个排序树，并且对较短的排序树进行搜索，较短的树为m，比较树根的大小，如果m树小于n左子树树根，则m重新定义为m的又子树树根，反之亦然。算法实现方式类似于二分查找，最近结果时间复杂度接近O(log(max(m, n))),需要考虑边界条件，包括两个数组各自或者都为空的情况，和一个数组最大值小于另一个数组0索引值的情况。还需要考虑奇偶情况；
> T: O(log(max(m, n))) S: O(1) 存储静态变量，无需过多空间；
```

4. 买卖股票的最佳时机，给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。如果你最多只允许完成一笔交易（即买入和卖出一支股票），设计一个算法来计算你所能获取的最大利润。注意你不能在买入股票前卖出股票。如果最多可以完成两笔交易呢？？？
> 最大收益，最佳时机，一次交易机会
> 最大收益，最佳时机，最多两次交易机会
> 最大收益，最佳时机，无限次交易机会
> 买卖股票的最佳时机，交易k次，且 k < n /2
> 最佳买卖股票时机含冷冻期
> 买卖股票的最佳时机含手续费
```
> Solution: 简单动态规划，画图分析，将每天的股票价格表示在折线图中，所要求的结果就是峰值和谷值的差，一次交易为一次最大差值，两次交易为两次最大差值的和或者一次最大差值。解法：1. 初始化两个变量，来存储当前最低值和最大收益（最大差），一次遍历该数组，每次遇到小于最低值的就更新最低值，每次遇到与最低值差值大于变量值的就更新最大差值，最终得到最大收益；2. 如果最多有两次交易机会则，仿照方法1初始化两个最小值和最大值变量，分别代表第一次和第二次最低交易值和最大收益，第二次的最低交易值需要用最低值减去第一次的收入。
> Solution: 真正的动态规划，使用dp table(dynamic programming table)，动态规划表，首先使用状态表穷举所有可能性，例如此题中为每一天的状态，包含三个可变参数天数、到当前剩余交易次数、当前是否持有股票，该表中的最终参数为当天利润；完成穷举框架后定义出所有状态转移方程，根据状态转移方程求得最终的最大利润，最终需要做好base case和特殊情况的处理；
用状态的转移跟踪动态的变化：
状态穷举：
dp[i][k][0]: 表示第i天剩余k次交易的时候，没持有股票时手上的利润，两种可能延续了前一天没有股票，今天刚刚卖出股票，在这两种可能中找出最大值
dp[i][k][1]: 表示第i天剩余k次交易的时候，持有股票时手上的利润，两种可能延续了前一天持有的股票，今天刚买进股票，在这两种可能中找出最大值

base case：
dp[-1][k][0] = dp[i][0][0] = 0
dp[-1][k][1] = dp[i][0][1] = -infinity

状态转移方程：
dp[i][k][0] = max(dp[i-1][k][0], dp[i-1][k][1] + prices[i])
dp[i][k][1] = max(dp[i-1][k][1], dp[i-1][k-1][0] - prices[i])

> III: 题目三根据穷举状态可得到，需要对无法消除的影响变量k进行穷举，表现在算法中就是遍历，最终的算法结果可以进一步进行化简，从而实现4个变量保存状态的最大利润；
> T:O(n) S: O(1)

# Python 实现题目III 状态方程化简前
# 此时必须要考虑k对整体状态转移的影响，也就是k的次数会随着交易的次数降低，但是k也有可能出现还剩一次的情况但是已经得到了最大的收益了o

int max_k = 2;
int[][][] dp = new int[n][max_k + 1][2];
for (int i = 0; i < n; i++) {
    for (int k = max_k; k >= 1; k--) {
        if (i - 1 == -1) { 
            /* 处理 base case */
            dp[i][k][0] = 0;
            dp[i][k][1] = -prices[i];
            continue;
        /*处理 base case */ }
        dp[i][k][0] = max(dp[i-1][k][0], dp[i-1][k][1] + prices[i]);
        dp[i][k][1] = max(dp[i-1][k][1], dp[i-1][k-1][0] - prices[i]);
    }
}
// 穷举了 n × max_k × 2 个状态，正确。
return dp[n - 1][max_k][0];

[mindnode](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-iv/solution/yi-ge-tong-yong-fang-fa-tuan-mie-6-dao-gu-piao-w-5/)

# Python 实现题目III 状态方程化简后

fst_lower, sec_lower, fst_max, sec_max = sys.maxint, sys.maxint, 0, 0

for i in prices:
    if i < fst_lower:
        fst_lower = i
    if i - fst_lower > fst_max:
        fst_max = i - fst_lower

    if i - fst_max < sec_lower:
        sec_lower = i - fst_max
    if i - sec_lower > sec_max:
        sec_max = i - sec_lower

return sec_max


```

5. 给一个 C++ 程序，删除程序中的注释。在 C++ 中有两种注释风格，行内注释和块注释。
```
> Solution: 逐行考虑当前这一行会出现的情况有哪些：
我们需要逐行分析源代码。有两种情况，要么在一个注释内或者不在。
如果我们遇到注释块符号，而我们不在注释中，那么我们将跳过接下来的两个字符，并将状态更改为在注释中。
如果我们遇到注释块符号并且我们在注释中，那么我们将跳过接下来的两个字符并将状态更改为不在注释中。
如果我们遇到一个行注释且我们不在注释中，那么我们将忽略该行的其余部分。
如果我们不在注释中（并且它不是注释的开头），我们将记录所遇到的字符。
在每行的末尾，如果我们不在注释中，我们将记录该行。
> T: O(S)  S: O(S)      S表示代码的总字符长度

# python
class Solution(object):
    def removeComments(self, source):
        in_block = False
        ans = []
        for line in source:
            i = 0
            if not in_block:
                newline = []
            while i < len(line):
                if line[i:i+2] == '/*' and not in_block:
                    in_block = True
                    i += 1
                elif line[i:i+2] == '*/' and in_block:
                    in_block = False
                    i += 1
                elif not in_block and line[i:i+2] == '//':
                    break
                elif not in_block:
                    newline.append(line[i])
                i += 1
            if newline and not in_block:
                ans.append("".join(newline))

        return ans
```

6. 灯泡开关 Ⅱ
> 按位与   ( bitwise and of x and y )
> &  举例： 5&3 = 1  解释： 101  11 相同位仅为个位1 ，故结果为 1
> 按位或   ( bitwise or of x and y )
> |  举例： 5|3 = 7  解释： 101  11 出现1的位是 1 1 1，故结果为 111
> 按位异或 ( bitwise exclusive or of x and y )
> ^  举例： 5^3 = 6  解释： 101  11 对位相加(不进位)是 1 1 0，故结果为 110
> 按位反转 (the bits of x inverted )
> ~  举例： ~5 = -6  解释： 将二进制数+1之后乘以-1，即~x = -(x+1)，-(101 + 1) = -110
> 按位反转仅能用在数字前面。所以写成 3+~5 可以得到结果-3，写成3~5就出错了
> 按位左移 （ x shifted left by n bits ）
> << 举例:  5<<2 = 20 解释：101 向左移动2位得到 10100 ，即右面多出2位用0补
> 按位右移 （ x shifted right by n bits ）
>
> >> 举例： 5>>2 = 1  解释：101 向右移动2位得到 1，即去掉右面的2位
```
> Solution: 状态枚举，按位操作 
> 解法，首先列出前6个灯的所有可能性
> Light 1 = 1 + a + c + d
> Light 2 = 1 + a + b
> Light 3 = 1 + a + c
> Light 4 = 1 + a + b + d
> Light 5 = 1 + a + c
> Light 6 = 1 + a + b
> 前三个灯已经包含了所有会出现的可能性，第五个和第六个灯的状态和第三个第二个完全一致，第四个灯地状态等于前三种开关状态之和，也就是前三种状态完全决定了第四个灯的状态；
> 此时由上述分析可知，前三个灯的状态决定了全部灯在序列里状态的可能性，所以只需要分析前三个灯在所有操作次数的可能性所有情况
> 只需要考虑m分别为0，1，2的三种特殊情况下的前三灯的特殊状态，当m>=3的时候前三个灯将包括他所有可能的亮灭过程，分别为2，4，8；
> 重点：1.分析前三个灯决定了所有灯的状态，2.分析操作次数大于等于3的情况下前三个灯将包含其所有可能的状态，因为前三个灯最多操作的是三种操作叠加，所以当操作次数为3的情况下，前三灯的所有的情况都可以包括； 
> T: O(1) S: O(1)
# python 
class Solution(object):
    def flipLights(self, n, m):
        n = min(n, 3)
        if m == 0: return 1
        if m == 1: return [2, 3, 4][n-1]
        if m == 2: return [2, 4, 7][n-1]
        return [2, 4, 8][n-1
]
```

7. [灯泡开关 I](https://leetcode-cn.com/problems/bulb-switcher)
初始时有 n 个灯泡关闭。 第 1 轮，你打开所有的灯泡。 第 2 轮，每两个灯泡你关闭一次。 第 3 轮，每三个灯泡切换一次开关（如果关闭则开启，如果开启则关闭）。第 i 轮，每 i 个灯泡切换一次开关。 对于第 n 轮，你只切换最后一个灯泡的开关。 找出 n 轮后有多少个亮着的灯泡。
```
> Solution: 分析方法，画出自定义的n个灯泡的情况，不难发现，每个数字都有奇数个或者偶数个因数，比如9 1 9 3而12为1 12 3 4，从而可以看出只有奇数个因数的序号的灯泡会进行奇数次操作，最终结果为亮着的状态，而判断一个数字的因数是否为奇数个也很简单就是看该数字是否是平方数；答案为返回平方数的个数；
> T:  S:
```

8. 最大二叉树
> 给定一个不含重复元素的整数数组。一个以此数组构建的最大二叉树定义如下：
二叉树的根是数组中的最大元素。
左子树是通过数组中最大值左边部分构造出的最大二叉树。
右子树是通过数组中最大值右边部分构造出的最大二叉树。
通过给定的数组构建最大二叉树，并且输出这个树的根节点。
```
> Solution: 重点： 二叉树 递归
如何表示二叉树的数据结构 
Node(elem, lchild, rchild)
> T:  S:
```

9. 只有两个键的键盘
最初在一个记事本上只有一个字符 'A'。你每次可以对这个记事本进行两种操作：
Copy All (复制全部) : 你可以复制这个记事本中的所有字符(部分的复制是不允许的)。
Paste (粘贴) : 你可以粘贴你上一次复制的字符。
给定一个数字 n 。你需要使用最少的操作次数，在记事本中打印出恰好 n 个 'A'。输出能够打印出 n 个 'A' 的最少操作次数。
```
> Solution: 数学，素数分解
素数分解，素数分解的方法，例如一个自然数N，如果要求他的最小因数和且不限制他的因数数量，则将N分解因数且所有因数都为素数，因为x+y<=x*y; 最终所有素数的和就是最小因数和，此题的答案就是最小因数和-因数数量
python求解素数分解:
        result = 0
        pn_start = 2
        while n > 1:
            while n%pn_start == 0:
                result += pn_start
                n /= pn_start
            pn_start += 1
        return result

之所以不考虑copy这个无效操作多出来的1个操作数，是因为每次拷贝前已经存在一份拷贝了 a(n) = a(n-1) + [a(n) - 1]a(n-1), n-1次粘贴再加上已经存在的一份，所以每次操作都是n次；
> T: O(√n) S: O(1)   这里的最差时间复杂度是当一个数的素数因数正好是他的开方，这时候中间两行代码被执行到的次数最多和最后一行升序被执行的最多，也就是开方次；
```

10. 子串查询，KMP
```
> Solution:
> T:  S:
```

11. 字符串的排列
给定两个字符串 s1 和 s2，写一个函数来判断 s2 是否包含 s1 的排列。
换句话说，第一个字符串的排列之一是第二个字符串的子串。
```
> Solution: 滑动窗口思想
什么是滑动窗口：它是一个运行在一个大数组上的子列表，该数组是一个底层元素集合。
假设有数组 [a b c d e f g h ]，一个大小为 3 的 滑动窗口 在其上滑动，则有：
[a b c]
  [b c d]
    [c d e]
      [d e f]
        [e f g]
          [f g h]
一般情况下就是使用这个窗口在数组的 合法区间 内进行滑动，同时 动态地 记录一些有用的数据，很多情况下，能够极大地提高算法地效率。
本题求解思路：
暴力法就是生成s1的所有排列，也就是s1的全排列，在使用[KMP](https://en.wikipedia.org/wiki/Knuth–Morris–Pratt_algorithm)法再s2中进行子串搜索；
与kmp类似的方法是滑动窗口，通过子串在目标串的滑动过程中来记录窗口中的关键信息，从而实现算法时间复杂度的最优；

下面两种python的实现，都是根据窗口中现有的字符数目的前后匹配，时间上比较差；

# python 实现
    def checkInclusion(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: bool
        """
        # 解法1: 复杂窗口匹配法
        # 1. 在s1中找到所有字符的数量
        """
        char_map = {}
        for v in s1:
            if v not in char_map.iterkeys():
                char_map.update({v: 1})
            else:
                char_map.update({v: char_map[v] + 1})
        # 2. 通过滑动窗口匹配s1中的元素数量
        w_l= len(s1)
        i = 0
        max_l = []
        less_l = []
        while i < len(s2) - w_l + 1:
            if max_l and max_l[1] > 0:
                if s2[i+w_l-1] != max_l[0] and s2[i-1] == max_l[0]:
                    max_l[1] -= 1
                elif s2[i+w_l-1] == max_l[0] and s2[i-1] != max_l[0]:
                    max_l[1] += 1
                if max_l[1] > 0:
                    i += 1
                continue
            if less_l and less_l[1] > 0:
                if s2[i+w_l-1] == less_l[0] and s2[i-1] != less_l[0]:
                    less_l[1] -= 1
                elif s2[i+w_l-1] != less_l[0] and s2[i-1] == less_l[0]:
                    less_l[1] += 1
                if less_l[1] > 0:
                    i += 1
                continue
            tmp_count = {}
            j = i
            while j < w_l + i:
                if s2[j] not in char_map.iterkeys():
                    i = j
                    break

                if s2[j] not in tmp_count.iterkeys():
                    tmp_count.update({s2[j]: 1})
                else:
                    tmp_count.update({s2[j]: tmp_count[s2[j]] + 1})
                
                # # 窗口中元素过多
                v = s2[j]
                if tmp_count[v] > char_map[v]:
                    max_l = [v, tmp_count[v] - char_map[v]]
                    break
            
                # 窗口中元素过少(窗口中已经存在的元素数量与s中元素数量的差值大于了当前窗口的剩余长度)
                if char_map[v] - tmp_count[v] > w_l + i - j:
                    less_l = [v, char_map[v] - tmp_count[v] - (w_l + i - j)]
                j += 1
            i += 1
            if tmp_count == char_map:
                return True

        return False
        """
        
        # 解法2: 窗口前后元素更新比对法

        # 1. 在s1中找到所有字符的数量
        char_map = {}
        for v in s1:
            if v not in char_map.iterkeys():
                char_map.update({v: 1})
            else:
                char_map.update({v: char_map[v] + 1})

        window_size = len(s1)
        window_map = {}
        window_left = 0
        window_right = 0

        while window_right < len(s2):

            if s2[window_right] not in char_map.iterkeys():
                window_map = {}
                window_left = window_right + 1
                window_right = window_right + 1
                continue

            if s2[window_right] not in window_map.iterkeys():
                window_map.update({s2[window_right]: 1})
            else:
                window_map.update({s2[window_right]: window_map[s2[window_right]] + 1})

            window_right += 1

            if window_right - window_left > window_size:
                window_map[s2[window_left]] -= 1
                if window_map[s2[window_left]] == 0:
                    window_map.pop(s2[window_left])
                window_left += 1
            if window_map == char_map: return True
        return False
> T:  S:  #TODO 后续分析
```

12. 找树左下角的值
tree | depth-first-search | breadth-first-search
给定一个二叉树，在树的最后一行找到最左边的值。
```
TODO：
二叉树的各种遍历方式：
广度优先 队列
深度优先 栈
前序遍历
中序遍历
后序遍历
> Solution: 广度优先，深度优先；  二叉树的各种遍历方式：广度优先、深度优先、前序遍历、中序遍历、后序遍历
深度优先遍历：从根节点出发，沿着左子树方向进行纵向遍历，直到找到叶子节点为止。然后回溯到前一个节点，进行右子树节点的遍历，直到遍历完所有可达节点为止。
广度优先遍历：从根节点出发，在横向遍历二叉树层段节点的基础上纵向遍历二叉树的层次。
DFS实现：
数据结构：栈
父节点入栈，父节点出栈，先右子节点入栈，后左子节点入栈。递归遍历全部节点即可

BFS实现：
数据结构：队列
父节点入队，父节点出队列，先左子节点入队，后右子节点入队。递归遍历全部节点即可

# python 使用队列从右往左广度优先遍历，使用栈实现深度优先遍历并暂存长度

    def findBottomLeftValue(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        # 使用队列从右往左广度优先遍历整个树，输出最后一个元素就是最后一行最左边的元素
        queue_l = []
        queue_l.append(root)

        while queue_l:
            node = queue_l.pop(0)
            if node.right:
                queue_l.append(node.right)
            if node.left:
                queue_l.append(node.left)
            if not queue_l:
                return node.val


        # 使用栈实现深度优先遍历
> T:  S:
```

13. 用最少数量的箭引爆气球  xstart ≤ x ≤ xend，则该气球会被引爆 输入:[[10,16], [2,8], [1,6], [7,12]]  输出:2
```
> Solution: 考虑使用局部最优解或者说每一步都是最优解的贪心算法
> 常用方法总结：
> 贪心算法 贪心算法的思想是每一步都选择最佳解决方案，最终获得全局最佳的解决方案。
> 对于此题来说所有气球坐标最小和坐标最大的之间尽量使用最少的箭来引爆 对于每一个气球来说最好能找到与其坐标香蕉的气球，对每一个气球来说都是找到该气球下的最优解；
# python
        if not points:
            return 0
        points = sorted(points, key= lambda x:x[1])
        arr_n = 1
        end = points[0][1]

        for v1, v2 in points:
            if v1 > end:
                arr_n += 1
                end = v2

        return arr_n
# 在不使用排序的情况下，无法解决边界问题，因为全部气球的最左边或者最右边是整体的边界，如果遍历顺序导致边界情况在后来才被考虑到，可能就会导致边界被孤立，从而无法获得最优解：
        # 此题目 不排序情况下的实现方式
        # TODO
        # if not points:
        #     return 0
        # arr_range = [[points[0][0],points[0][1]]]
        # for v1, v2 in points:
        #     update = False
        #     for rv in arr_range:
        #         if rv[0] <= v1 <= rv[1] or rv[0] <= v2 <= rv[1] or v1 <= rv[0] <= v2 or v1 <= rv[1] <= v2:
        #             rv[0] = max(rv[0], v1)
        #             rv[1] = min(rv[1], v2)
        #             update = True
        #             break
        #     if not update: arr_range.append([v1, v2])
        # return len(arr_range)
无法满足的case：
[[3,9],[7,12],[3,8],[6,8],[9,10],[2,9],[0,9],[3,9],[0,6],[2,8]]
[!image]()
> T:  S:
```

14. 两数相加 II
给定两个非空链表来代表两个非负整数。数字最高位位于链表开始位置。它们的每个节点只存储单个数字。将这两数相加会返回一个新的链表。
```
> Solution:
此次的两数相加中不知道链表长度而且不能对链表进行直接反转之后进位相加，所有需要考虑从高位开始向低位对目的链表进行相加的情况：
解法1: 思想：暂存栈，存储之后pop相加
对L1 L2两个链表进行暂存存储在栈中，因为栈的push和pop操作又后进先出的特点，所以对两个栈进行相加并生成新的链表，就可以得到最终L1 L2之和的链表的结果；
解法2: 获取长度，对同位部分使用递归的方式相加，递归的return可以返回相加的进位，如此就可以处理进位的问题；
# pyothon 解法2
        # TODO
    # Mark - this is a python 3 implementation
    # finish python2 version and rewrite with stack push pop
    def addTwoNumbers(self, l1, l2):
        def add(num1, num2, i, j):
            if not i or not j:
                return 0
            if num1 > num2:
                temp = i.val + add(num1 - 1, num2, i.next, j)
            else:
                temp = i.val + j.val + add(num1, num2, i.next, j.next)
            i.val = temp % 10
            return temp // 10

        num1 = num2 = 0
        cur = l2
        while cur:
            num2 += 1
            cur = cur.next
        cur = l1
        while cur:
            num1 += 1
            cur = cur.next
        
        if num2 > num1:
            l1, l2 = l2, l1
            num2, num1 = num1, num2

        if add(num1,num2,l1, l2):
            l2 = ListNode(1)
            l2.next = l1
            l1 = l2
        return l1
> T:  S:
```

15. [压缩字符串](https://leetcode-cn.com/problems/string-compression/description/)

给定一组字符，使用[原地算法](https://baike.baidu.com/item/原地算法)将其压缩。
压缩后的长度必须始终小于或等于原数组长度。
数组的每个元素应该是长度为1 的**字符**（不是 int 整数类型）。
在完成[原地](https://baike.baidu.com/item/原地算法)**修改输入数组**后，返回数组的新长度。
使用O(1) 空间解决

原地算法：

> 在计算机科学中，一个原地算法（in-place algorithm）是一种使用小的，固定数量的额外之空间来转换资料的算法。当算法执行时，输入的资料通常会被要输出的部份覆盖掉。不是原地算法有时候称为非原地（not-in-place）或不得其所（out-of-place）。
>
> 在计算复杂性理论中，原地算法包含使用O(1)[空间复杂度](https://baike.baidu.com/item/空间复杂度)的所有算法，DSPACE(1)类型。这个类型是非常有限的；它与正规语言1相等。事实上，它甚至不包含上面所列的任何范例。

**示例：**

```
输入：
["a","b","b","b","b","b","b","b","b","b","b","b","b"]

输出：
返回4，输入数组的前4个字符应该是：["a","b","1","2"]。
```

```
> Solution: 解法1: 
1. 实现空间复杂度为1的原地算法
# python 使用暂存值存储索引值和重复字符的索引，并存储重复字符的字符
        # 实现空间复杂度为1的原地算法
        # 在python中使用切片无法实现原地算法，原地算法需要对原数组中的值进行修改，例如直接替换、pop、insert

        # count, j, i = 1, 0, 0
        # while i < len(chars) - 1:
        #     i += 1
        #     if chars[i] == chars[i - 1]:
        #         count += 1
        #         if j == 0: j = i
        #         if i == len(chars) - 1 and count > 1:
        #             count_l = str(count).split(",")
        #             chars = chars[0:j] + count_l
        #     else:
        #         if count > 1:
        #             count_l = str(count).split(",")
        #             chars = chars[0:j] + count_l + chars[i:]
        #             j = 0
        #             count = 1
        #             i = i - (i - j) + len(count_l)
        # print chars
        # return len(chars)

        # 实现空间复杂度为1的原地算法
        count, i = 1, 0
        while i < len(chars) - 1:
            i += 1
            if chars[i] == chars[i - 1]:
                chars.pop(i)
                i -= 1
                count += 1
                if i == len(chars) - 1 and count > 1:
                    chars.extend(list(str(count)))
                    break
            else:
                if count > 1:
                    count_l = list(str(count))
                    for v in count_l:
                        chars.insert(i, v)
                        i += 1
                    count = 1
        return len(chars)
        # 空间复杂度O(1) 使用3个常量存储
        # 时间复杂度O(N)
> T:  S:
```

16. [甲板上的战舰](https://leetcode-cn.com/problems/battleships-in-a-board/description/) 

给定一个二维的甲板， 请计算其中有多少艘战舰。 战舰用 `'X'`表示，空位用 `'.'`表示。 你需要遵守以下规则：

- 给你一个有效的甲板，仅由战舰或者空位组成。
- 战舰只能水平或者垂直放置。换句话说,战舰只能由 `1xN` (1 行, N 列)组成，或者 `Nx1` (N 行, 1 列)组成，其中N可以是任意大小。
- 两艘战舰之间至少有一个水平或垂直的空位分隔 - 即没有相邻的战舰。
类似题目：岛屿数量

```
> Solution: 图，图的搜索，DFS，BFS搜索算法
此题为在二维数组中寻找特殊条件的连通图（所有顶点都联通）的个数；

重点： 在一个无向图中找特殊条件的连通图

一次扫描整个二维数组，且使用静态变量存储返回值：
# Python
        count = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == "X":
                    if (i > 0 and board[i - 1][j] == "X") or (j > 0 and board[i][j - 1] == "X"):
                        continue
                    count += 1
        return count

> T: O(m*n) S: O(1)
```

17. [水壶问题](https://leetcode-cn.com/problems/water-and-jug-problem/description/)

有两个容量分别为 *x*升 和 *y*升 的水壶以及无限多的水。请判断能否通过使用这两个水壶，从而可以得到恰好 *z*升 的水？

如果可以，最后请用以上水壶中的一或两个来盛放取得的 *z升* 水。

你允许：

- 装满任意一个水壶
- 清空任意一个水壶
- 从一个水壶向另外一个水壶倒水，直到装满或者倒空

```
> Solution: 数学问题， 类似3加仑和4加仑的桶到处5加仑水的问题： 数学问题 裴蜀定理
任意两个正整数a，b的公约数d，有xa+yb = d的倍数，也就是此题中结果想要得到的水的容量需要满足他是两个水壶容量的公约数的倍数；

# python 
def _gcd(x, y):
    if y == 0: return x
    z = x % y
    return _gcd(y, z)

if (x == y != z and z!= 0) or (z > x + y): return False
if z == 0 or z % _gcd(x, y) == 0: return True
> T:  S:
```

18. [最长上升子序列](https://leetcode-cn.com/problems/longest-increasing-subsequence/description/)
给定一个无序的整数数组，找到其中最长上升子序列的长度。

示例:

输入: [10,9,2,5,3,7,101,18]
输出: 4 
解释: 最长的上升子序列是 [2,3,7,101]，它的长度是 4。
说明:

可能会有多种最长上升子序列的组合，你只需要输出对应的长度即可。
你算法的时间复杂度应该为 O(n2) 。
将算法的时间复杂度降低到 O(n log n) 
```
> Solution: n log n表示什么：首先logn的算法涉及到二分法，例如二分查找和二分搜索

解法： 使用dp，dynamic programming，动态规划的基本步骤是 1.定义当前动态需求的状态并建立状态方程 2.状态方程的建立需要考虑所有穷举的可能性 3. 考虑状态随变量变化的转移情况，建立状态转移方程；

解法1: 使用动态规划：
1. 状态定义： dp[i] 表示到索引i为止的最长升序序列的长度值
2. 状态转移：转移条件：序列索引上升，这时候需要考虑此索引前面每一个状态长度和当前值的关系得到最佳结果，如：比较当前值和该索引i前的每一个值的大小，如果出现大于前面索引值dp[j]的情况需要考虑在当前值和dp[j] + 1 中获取最大值，即表示最长升序

解法2 动态规划 + 二分查找
1. 对解法1中的状态定义换一个角度，解法1中的状态定义的长度为dp[i]的值，这里的状态定义将换成保存到i为止的升序（严格来说不是i-1处的真正的升序序列）序列，而1中的dp值就是现在的dp序列的长度；这样就可以在此dp序列上进行目标元素的替换从而不影响上一个序列的长度；
例如：2， 3， 4， 7， 10， 11， 6， 8， 9 ，10
i = 5， dp = 2，3，4，7，10，11
i = 6， dp = 2，3，4，6，10，11
这里状态的转移是将7替换成了6从而能够在目标序列中继续找升序序列，但是并没有影响当前找到的最大升序序列的长度，最终如果找到了新最小值（7被6替换表示，6替换了dp中第一个大于它自身的数字）从而得到了一个更长的序列例如找到最大数后append操作，最终新的长度也覆盖了上一次最长上升长度，而替换和append操作则可以使用二分查找的方式来实现；

这里的难点在于： dp数组会对当前最长的长度进行保留并且也会在每个索引的位置上讲后续升序的潜在可能性提高到最高，比如大于6的正整数比大于7的正整数多；
重点： dp数组，1. 保存了到当前索引的最大升序长度 2. 保存了当前索引前替换发生前的dp状态和替换后的双重状态；

2， 3， 4， 7， 10， 12， 6， 8， 9 ，11

1， 2， 3， 4， 5，  6，  4， 5， 6， 7  解法1中的dp状态

解法2中
2， 3， 4， 7， 10， 12 -》 2， 3， 4， 6， 10， 12
将7替换为6表示：
1. 等于解法1中7和7前面的长度还有参考价值，但是7本身没有参考价值，6处长度的更新（更新为4）就等于解法2中的替换；
2. 替换等效于解法1中的状态随着索引的不断转移，即使已经有大于自己的最长升序依然还在计算升序值，因为越小的值后面出现大于它的值的数量的概率越高；

# python

        #  DP + BS
        # dynamic programming + binary search
        dp = []
        for v in nums:
            if not dp or v >  dp[-1]:
                dp.append(v)
                continue
            i, j = 0, len(dp)
            # 二分查找找到第一个最大的，也就是大小最接近v而且大于v的数
            while i < j:
                m = (i + j) // 2  # // 表示对商向下取整
                if dp[m] < v: i = m + 1
                else: j = m
            #既保留前者状态又更新最新状态的替换
            dp[i] = v
        return len(dp)
> T:  S:
```

19. [缺失数字](https://leetcode-cn.com/problems/missing-number/description/)

    给定一个包含 0, 1, 2, ..., n 中 n 个数的序列，找出 0 .. n 中没有出现在序列中的那个数。

```
> Solution: 位运算，位运算中相同数字经过^异或运算后得到0，所以对整个序列好正常序列经过异或后的到的就是： 缺失值^目标序列最大值 而目标序列最大值正好就是目标序列的长度
傻瓜式解法：
1. 先排序然后在遍历，最差时间复杂度为 nlogn + n 所以就是nlogn
2. 使用一个哈希表，将检查出来的数字存储到哈希表中，因为哈希表的查询时间复杂度为1，所以最终结果的时间复杂度为n

# python 位运算
    def missingNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # 位运算
        # 异或，两个相同的数异或得到的结果为0
        miss_n = len(nums)
        for i in range(len(nums)):
            miss_n ^= i ^ nums[i]
        return miss_n

> T: O(n)  S: O(1) 一个常量存储缺失值的异或结果
```

20. [二叉树的序列化与反序列化](https://leetcode-cn.com/problems/serialize-and-deserialize-binary-tree/description/)

序列化是将一个数据结构或者对象转换为连续的比特位的操作，进而可以将转换后的数据存储在一个文件或者内存中，同时也可以通过网络传输到另一个计算机环境，采取相反方式重构得到原数据。

请设计一个算法来实现二叉树的序列化与反序列化。这里不限定你的序列 / 反序列化算法执行逻辑，你只需要保证一个二叉树可以被序列化为一个字符串并且将这个字符串反序列化为原始的树结构。

**示例:** 

```
你可以将以下二叉树：

    1
   / \
  2   3
     / \
    4   5

序列化为 "[1,2,3,null,null,4,5]"
```

```
> Solution:

# python class Codec:

    # 对二叉树使用深度优先遍历
    # 二叉树的DFS BFS
    # BFS:
    #         queue_l = []
        # queue_l.append(root)

        # while queue_l:
        #     node = queue_l.pop(0)
        #     if node.right:
        #         queue_l.append(node.right)
        #     if node.left:
        #         queue_l.append(node.left)
        #     if not queue_l:
        #         return node.val

    # 深度遍历
    # 不使用静态变量 使用递归
    def serialize(self, root):
        """Encodes a tree to a single string.
        
        :type root: TreeNode
        :rtype: str
        """
        
        def recursive_serializer(node, string):
            if node is None:
                string += "None,"
            else:
                string += str(node.val) + ","
                string = recursive_serializer(node.left, string)
                string = recursive_serializer(node.right, string)
            return string
        return recursive_serializer(root, '')


    # 反序列化，将数组转化成二叉树
    # 使用了递归实现了序列化，侧同理反序列化也使用递归
    def deserialize(self, data):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: TreeNode
        """

        def recursive_serializer(data):
            if data[0] == "None":
                data.pop(0)
                return None
            
            node = TreeNode(data[0])
            data.pop(0)
            node.left = recursive_serializer(data)
            node.right = recursive_serializer(data)
            return node

        return recursive_serializer(data.split(','))
> T:  S:
```



21. [整数转换英文表示](https://leetcode-cn.com/problems/integer-to-english-words/description/)



将非负整数转换为其对应的英文表示。可以保证给定输入小于 231 - 1 。

**示例 1:**

```
输入: 123
输出: "One Hundred Twenty Three"
```

**示例 2:**

```
输入: 12345
输出: "Twelve Thousand Three Hundred Forty Five"
```

**示例 3:**

```
输入: 1234567
输出: "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
```

**示例 4:**

```
输入: 1234567891
输出: "One Billion Two Hundred Thirty Four Million Five Hundred Sixty Seven Thousand Eight Hundred Ninety One"
```

```
> Solution: 分治

所有数字的英文表示：
1- 10
1: 'One',
2: 'Two',
3: 'Three',
4: 'Four',
5: 'Five',
6: 'Six',
7: 'Seven',
8: 'Eight',
9: 'Nine'

10 - 20
10: 'Ten',
11: 'Eleven',
12: 'Twelve',
13: 'Thirteen',
14: 'Fourteen',
15: 'Fifteen',
16: 'Sixteen',
17: 'Seventeen',
18: 'Eighteen',
19: 'Nineteen'

20 - 90
2: 'Twenty',
3: 'Thirty',
4: 'Forty',
5: 'Fifty',
6: 'Sixty',
7: 'Seventy',
8: 'Eighty',
9: 'Ninety'

 billion = 1，000，000，000
 million = 1，000，000
 thousand = 1，000

# python 实现，使用分而治之的方式，将数字按照英制的阿拉伯数字的划分方式，将其划分成每3个一组的方式在进一步划分；

分治具体的方法实现；
1. 每三位分出当前总数，题目要求是小于2**31 -1 = 1024 * 1024 * 1024 -1 所以可以确定需要转换的数在百万以内，确定数字的 bilion million thousand
2. 将每个3位的单位数前面的数字转换成因为，有三种转换方式第一10以内，第二100以内，第三999以内，并且不重复；
3. 将三种方法的函数实现并将进位的函数实现，题目就可以解出；

class Solution:
    def numberToWords(self, num):
        """
        :type num: int
        :rtype: str
        """
        def one(num):
            switcher = {
                1: 'One',
                2: 'Two',
                3: 'Three',
                4: 'Four',
                5: 'Five',
                6: 'Six',
                7: 'Seven',
                8: 'Eight',
                9: 'Nine'
            }
            return switcher.get(num)

        def two_less_20(num):
            switcher = {
                10: 'Ten',
                11: 'Eleven',
                12: 'Twelve',
                13: 'Thirteen',
                14: 'Fourteen',
                15: 'Fifteen',
                16: 'Sixteen',
                17: 'Seventeen',
                18: 'Eighteen',
                19: 'Nineteen'
            }
            return switcher.get(num)

        def ten(num):
            switcher = {
                2: 'Twenty',
                3: 'Thirty',
                4: 'Forty',
                5: 'Fifty',
                6: 'Sixty',
                7: 'Seventy',
                8: 'Eighty',
                9: 'Ninety'
            }
            return switcher.get(num)

                # 返回小于20的数字的英文表示
        def two(num):
            if not num:
                return ''
            elif num < 10:
                return one(num)
            elif num < 20:
                return two_less_20(num)
            else:
                tenner = num // 10
                rest = num - tenner * 10
                return ten(tenner) + ' ' + one(rest) if rest else ten(tenner)

                # 返回小于999的数字的英文表示，需要使用到hundred
        def three(num):
            hundred = num // 100
            rest = num - hundred * 100
            if hundred and rest:
                return one(hundred) + ' Hundred ' + two(rest) 
            elif not hundred and rest: 
                return two(rest)
            elif hundred and not rest:
                return one(hundred) + ' Hundred'

                # 按照进位划分当前的数字
        billion = num // 1000000000
        million = (num - billion * 1000000000) // 1000000
        thousand = (num - billion * 1000000000 - million * 1000000) // 1000
        rest = num - billion * 1000000000 - million * 1000000 - thousand * 1000

        if not num:
            return 'Zero'

        result = ''
        if billion:
            result = three(billion) + ' Billion'
        if million:
            result += ' ' if result else ''
            result += three(million) + ' Million'
        if thousand:
            result += ' ' if result else ''
            result += three(thousand) + ' Thousand'
        if rest:
            result += ' ' if result else ''
            result += three(rest)
        return result

> T:  S:
```

22. [各位相加](https://leetcode-cn.com/problems/add-digits/description/)

```
> Solution: 数学问题，只需要在草纸上进行退到即可得到答案

10x + y = z
x + y = z - 9x
a + b + c = z - (99a + 9b) = z - 9(11a + b)
e + f = z - 9(11a + b) - 9e = z - 9(11a + b + e)

由此可见，因为十进制总是9 + 1才进位，所以各位相加就是对9取余数；
但是由于9的倍数对9取余数为0，但是更具题目条件，所以需要返回9；

# python
class Solution(object):
    def addDigits(self, num):
        """
        :type num: int
        :rtype: int
        """
        if num == 0:
            return 0
        return num % 9 if num % 9 > 0 else 9
> T: O(1)  S: O(1) 
```

23. [除自身以外数组的乘积](https://leetcode-cn.com/problems/product-of-array-except-self/description/)

给定长度为 *n* 的整数数组 `nums`，其中 *n* > 1，返回输出数组 `output` ，其中 `output[i]` 等于 `nums` 中除 `nums[i]` 之外其余各元素的乘积。

**示例:**

```
输入: [1,2,3,4]
输出: [24,12,8,6]
```

**说明:** 请**不要使用除法，**且在 O(*n*) 时间复杂度内完成此题。

**进阶：**
你可以在常数空间复杂度内完成这个题目吗？（ 出于对空间复杂度分析的目的，输出数组**不被视为**额外空间。）

```
> Solution: 逻辑思维 数学
此题的解决方法需要考虑 1. 只能使用相乘 2. 需要在线性的时间和空间内解决 3. 要考虑遇到0的情况;
考虑：
a1, a2,  a3,      a4
1, 1*a1, 1*a1*a2, 1*a1*a2*a3

a1,                     a2,             a3,         a4
a4*1*a3*a1,     a4*1*a3     a4*1,       1

由于数组是线性结构，从两端同时分别遍历，最终的即可得到答案；

# python
        # a1, a2,  a3,      a4
        # 1, 1*a1, 1*a1*a2, 1*a1*a2*a3

        # a1,               a2,             a3,         a4
        # a4*1*a3*a1,       a4*1*a3,        a4*1,       1

        # 由于数组是线性结构，从两端同时分别遍历，最终的即可得到答案；

        l = len(nums)
        i = 0
        j = l - 1
        result = [1]*l
        while i != l -1:
            result[i+1] = result[i] * nums[i]
            i += 1
        p = 1
        while j != 0:
            p = nums[j] * p
            result[j -1] *= p 
            j -= 1
        return result

> T:  S:
```

24. [删除链表中的节点](https://leetcode-cn.com/problems/delete-node-in-a-linked-list/description/)

```
> Solution:

        t = node.next
        node.val = t.val
        node.next = t.next
        t = None

> T:  S:
```

25. [二叉树的最近公共祖先](https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-tree/description/)

```
> Solution: 递归，回溯
解法：
1. 对二叉树进行深度优先遍历并将每一个非叶子节点添加到缓存栈中
2. 当找到第一个匹配后，立即停止再向缓存栈中添加节点，因为此时的答案已经在栈中了
3. 递归回溯，将没有匹配的节点从缓存栈中移除
4. 找到第二个匹配项后，返回栈顶节点
@@ 需要考虑跟节点就是匹配节点的情况，需要考虑叶子节点的情况，需要考虑匹配节点本身就是答案的情况；

# Python

class Solution(object):
    def lowestCommonAncestor(self, root, p, q):
        """
        :type root: TreeNode
        :type p: TreeNode
        :type q: TreeNode
        :rtype: TreeNode
        """

        # BFS - Breadth first search    while loop
        # DFS - depth first search      recursive

        # recursive tree
        #       a
        #    b      z
        #  c   f
        # d  e

        stack = []
        find = []

        # 返回根结点
        if root == q or root == p:
            return root

        def depth_search(node, p, q):

            if node.val == p.val or node.val == q.val:
                # 找到第二个元素返回True，这时候整个递归都会返回，并且不再修改结果
                if find:
                    return True
                # 找到第一个元素后在find数组中标记
                # 并且将第一个找到的元素也考虑在可能的答案根结点上
                find.append(True)
                stack.append(node)
            
            # 考虑末尾节点，当节点为叶子节点时，直接对该节点返回False
            # 如果当前匹配第一次的节点就是叶子节点，需要将该节点移除缓存栈
            if node.left == None and node.right == None:
                if stack[-1] == node: stack.pop(-1)
                return False

            # 没有匹配的情况下，需要将每个非叶子节点加入缓存栈
            if not find: stack.append(node)

            # 对左右子树递归
            if node.left:
                if depth_search(node.left, p, q): return True
            if node.right:
                if depth_search(node.right, p ,q): return True

            # 如果没有一次匹配则回溯到本节点后从缓存栈移除
            # 如果当前节点就是缓存栈顶部节点，则移除，因为上面的左右子树递归没有找到第二个匹配项
            if not find or stack[-1] == node: stack.pop(-1)

        depth_search(root, p, q)
        return stack[-1]


> T: N S: N/2
```

26. [二叉搜索树的最近公共祖先](https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-search-tree/description/)

```
> Solution: 二叉树，完全二叉树，满二叉树、二叉搜索树（二叉查找树）

# 对于找到二搜索树的最近祖先，只需要考虑大于、小于、等于、包含跟节点四种情况即可，大于和小于需要更新跟节点

# python
class Solution(object):
    def lowestCommonAncestor(self, root, p, q):
        """
        :type root: TreeNode
        :type p: TreeNode
        :type q: TreeNode
        :rtype: TreeNode
        """


        while root:
            if p.val == root.val or q.val == root.val:
                return root
            elif p.val < root.val < q.val or q.val < root.val < p.val:
                return root
            elif p.val < root.val and q.val < root.val:
                root = root.left
            elif p.val > root.val and q.val > root.val:
                root = root.right
            else:
                pass
> T: 1  S: 1
```

---

---

---

### TODO: read and understand the meaning



26. [标签验证器](https://leetcode-cn.com/problems/tag-validator/description/)
**栈**
```
> Solution: html 代码验证工具，对于这样的特殊匹配的题目，需要注意栈和队列的使用
解法：
1. 遍历整段代码，将遇到的html标签放入栈中，如果遇到结束标签就可以对比栈定的开始标签元素；
2. 对于开始字符"<"，如果后面接的是！则为cdata的开始，如果不是那一定是一个开始标签或者结束标签
3. 对入栈和出栈的元素的对比的同时需要检查tag_name的合法性；
4. 结束时，检查栈是否为空，代码必须在栈不为空的时候出现，因为代码必须在标签的包裹中，最后一个标签之后不能有其他代码；以上条件都符合则就视为True

# java

public class Solution {
    Stack < String > stack = new Stack < > ();
    boolean contains_tag = false;
    public boolean isValidTagName(String s, boolean ending) {
        if (s.length() < 1 || s.length() > 9)
            return false;
        for (int i = 0; i < s.length(); i++) {
            if (!Character.isUpperCase(s.charAt(i)))
                return false;
        }
        if (ending) {
            if (!stack.isEmpty() && stack.peek().equals(s))
                stack.pop();
            else
                return false;
        } else {
            contains_tag = true;
            stack.push(s);
        }
        return true;
    }
    public boolean isValidCdata(String s) {
        return s.indexOf("[CDATA[") == 0;
    }
    public boolean isValid(String code) {
        if (code.charAt(0) != '<' || code.charAt(code.length() - 1) != '>')
            return false;
        for (int i = 0; i < code.length(); i++) {
            boolean ending = false;
            int closeindex;
            if(stack.isEmpty() && contains_tag)
                return false;
            if (code.charAt(i) == '<') {
                if (!stack.isEmpty() && code.charAt(i + 1) == '!') {
                    closeindex = code.indexOf("]]>", i + 1);
                    if (closeindex < 0 || !isValidCdata(code.substring(i + 2, closeindex)))
                        return false;
                } else {
                    if (code.charAt(i + 1) == '/') {
                        i++;
                        ending = true;
                    }
                    closeindex = code.indexOf('>', i + 1);
                    if (closeindex < 0 || !isValidTagName(code.substring(i + 1, closeindex), ending))
                        return false;
                }
                i = closeindex;
            }
        }
        return stack.isEmpty() && contains_tag;
    }
}

> T: N S: N
```


27. [用栈实现队列](https://leetcode-cn.com/problems/implement-queue-using-stacks/description/)
```
> Solution: Queue, Stack 一进一出两个栈实现队列，栈和队列的基础知识

Stack: push to top, peek/pop from top, size,is empty
Queue: push, pop, peek, empty

# [232] 用栈实现队列
#

# @lc code=start
class MyQueue(object):

    # stack
    # bottom [x, x, x, x] top

    # queue
    # top [x, x, x, x] bottom

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.stack_in = []
        self.stack_out = []
        

    def push(self, x):
        """
        Push element x to the back of queue.
        :type x: int
        :rtype: None
        """
        self.stack_in.append(x)
        print "IN %s" % self.stack_in
        print "OUT %s" % self.stack_out 
        

    def pop(self):
        """
        Removes the element from in front of queue and returns that element.
        :rtype: int
        """
        while self.stack_in:
            self.stack_out.append(self.stack_in.pop(-1))
        result = self.stack_out.pop(-1)
        while self.stack_out:
            self.stack_in.append(self.stack_out.pop(-1))

        print "IN %s" % self.stack_in
        print "OUT %s" % self.stack_out 
        return result
        
    def peek(self):
        """
        Get the front element.
        :rtype: int
        """
        while self.stack_in:
            self.stack_out.append(self.stack_in.pop(-1))
        result = self.stack_out[-1]
        while self.stack_out:
            self.stack_in.append(self.stack_out.pop(-1))
        print "IN %s" % self.stack_in
        print "OUT %s" % self.stack_out 
        return result

    def empty(self):
        """
        Returns whether the queue is empty.
        :rtype: bool
        """
        print "IN %s" % self.stack_in
        print "OUT %s" % self.stack_out 
        if len(self.stack_in) > 0:
            return False
        else:
            return True

> T:  S:
```

28. [旋转图像](https://leetcode-cn.com/problems/rotate-image/description/)

**TODO**

```
给定 matrix = 
[
  [1,2,3],
  [4,5,6],
  [7,8,9]
],
```

```
> Solution: 90度顺时针旋转矩阵，不能使用另外的空间，原地进行计算
解法： 1. 转置矩阵，然后左右翻转  2. 矩型转动；
1  2  3

4  5  6

7  8  9
# 方法2的python实现

# @lc code=start
quanshu


> T: N**2 S:
```

29. [最大子序和](https://leetcode-cn.com/problems/maximum-subarray/description/)
**TODO** [分治法](https://leetcode-cn.com/problems/maximum-subarray/solution/zui-da-zi-xu-he-by-leetcode/)

```
> Solution: 本题是分治算法的典型例子
# 贪心算法也可以求解，局部最优解，需要两个变量1存储当前窗口移动到的位置的最大值，第二个存储到当前节点为止的最大值；
-2 1 -3

索引为2: 当前点最大值 1-3  到该点为止最大值 1



        # 贪心
        # 滑动窗口
        # 分治


        window = 0
        result_max = - sys.maxint -1
        for v in nums:
            window += v
            window = max(window, v)
            result_max = max(window, result_max)
            
        return result_max


# 动态规划也可以求解
Kadane 算法

有两种标准 DP 方法适用于数组：
常数空间，沿数组移动并在原数组修改。
线性空间，首先沿 left->right 方向移动，然后再沿 right->left 方向移动。 合并结果。

1. 原地修改
2. 左右滑动窗口合并结果

使用原地修改，参考贪心算法，就是将当前窗口的最大值放在数组内，并且可以直接使用；


动态规划：
1. 定义状态，建立基本的状态
2. 更具变量的变化，建立状态转移方程
3. 根据状态转移方程求解


标准动态规划的代码如下：

class Solution {
    // 动态规划
    public int maxSubArray(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int ans = 0;

        // 1. 状态定义
        // dp[i] 表示前 i 个元素的最大连续子数组的和
        int[] dp = new int[nums.length];

        // 2. 状态初始化，数组中第一个元素的最大和就是第一个元素值
        dp[0] = nums[0];
        ans = nums[0];

        // 3. 状态转移
        // 转移方程：dp[i] = max(dp[i - 1], 0) + nums[i]
        //  dp 当前元素的值等于前一个元素值和 0 的最大值再加上 nums[i]
        for (int i = 1; i < nums.length; i++) {
            dp[i] = Math.max(dp[i - 1], 0) + nums[i];
            // 更新最大和
            ans = Math.max(ans, dp[i]);
        }

        return ans;
    }
}
以上代码的时间复杂度是 O(N)，空间复杂度也是 O(N)，实际上我们可以降低空间复杂度到 O(1)。

从上面的状态转移方程 dp[i] = max(dp[i - 1], 0) + nums[i] 看出，当前的状态的值只取决于前一个状态值，所以我们可以使用一个变量来代替 dp[i] 和 dp[i - 1]，如下代码：

class Solution {
    // 动态规划
    public int maxSubArray(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int ans = 0;

        // 使用 currSum 代替 dp[i]
        int currSum = nums[0];
        ans = nums[0];

        for (int i = 1; i < nums.length; i++) {
            currSum = Math.max(currSum, 0) + nums[i];
            // 更新最大和
            ans = Math.max(ans, currSum);
        }

        return ans;
    }
}
以上代码的时间复杂度是 O(N)，空间复杂度也是 O(1)

> T: N S: 1
```

30. [螺旋矩阵](https://leetcode-cn.com/problems/spiral-matrix/description/)

```
> Solution:

# python
        # 模拟旋转
        # TODO

        result = []
        while matrix:
            if not result:
                result = matrix.pop(0)
            else:
                result.extend(matrix.pop(0))
            if not matrix: return result
            for s in range(len(matrix)):
                result.append(matrix[s][-1])
                matrix[s].pop(-1)
            for _ in range(len(matrix[-1])):
                result.append(matrix[-1][-1])
                matrix[-1].pop(-1)

            while matrix and not matrix[-1]:
                matrix.pop(-1)
            for j in range(len(matrix)):
                result.append(matrix[len(matrix) - 1 - j][0])
                matrix[len(matrix) - 1 - j].pop(0)
                
            while matrix and not matrix[-1]:
                matrix.pop(-1)
        return result
> T:  S:
```

31. [跳跃游戏](https://leetcode-cn.com/problems/jump-game/description/)
**TODO**

```
> Solution:
解法： 反向思考，只要前面的任意一个点能到达终点，则这个点就是终点，继续向前寻找能到达终点的点，知道最终找完整个数组，如果此时终点在起点上，则返回True；

# 动态规划，自底向上，自顶向下
# 贪心

# python
# @lc code=start
class Solution(object):
    def canJump(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        # l = len(nums)
        # if l == 1:
        #     return True
        # for i in range(0, l):
        #     if i != l - 1 and nums[i] == 0:
        #         return False
        #     i = i + nums[i]
        #     if i == l - 1:
        #         return True
        #     if i > l -1:
        #         return False
        # 题目中指出数组中的元素代表能跳跃的最大长度  最大 最大 最大

        # 动态规划，自底向上，自顶向下


        # 贪心

        l = len(nums)
        position = l - 1
        if l == 1:
            return True
        for i in range(1, l):
            j = l - 1 - i
            if j + nums[j] >= position:
                position = j
        
        if position == 0:
            return True
        else:
            return False
        
> T:  S:
```

32. [合并区间](https://leetcode-cn.com/problems/merge-intervals/description/)

**箭射气球**

```
> Solution:

# python 
        if not intervals: return []
        intervals.sort(key=lambda x: x[0])
        result = []
        tmp = intervals[0]
        for v in intervals:
            if tmp[0] <= v[0] <= tmp[1]:
                tmp[1] = max(tmp[1], v[1])
            else:
                result.append(tmp)
                tmp = v
        result.append(tmp)

        return result

# 先排序在合并区间，此题目类似箭射气球
> T:  S:
```

33. [最长回文子串](https://leetcode-cn.com/problems/longest-palindromic-substring/description/)
**TODO**： 终极方法为Manacher 算法时间复杂度为 O(n) Manacher 算法
> Solution: 中心扩展发，回文子串是 aba 或者 bb 这样正反都相同的字符串，所以从找到这些的两种情况从中心向外扩展，直到中不再有相同元素为止，这样算法的最差时间复杂度就是N**2
> T:  S:
```python
        # A: find the same from start to end as start of iterable
        result = {}

        for i in range(len(s)):

            r = ""
            k = 0
            j = 0
            if i + 1 >= len(s):
                continue
            if s[i] == s[i+1]:
                j = i
                k = i + 1
                while j >= 0 and k < len(s) and s[j] == s[k]:
                    r = s[j] + r
                    r += s[k]
                    j -= 1
                    k += 1
            if r:
                result.update({len(r): r})
            if i - 1 >= 0 and i + 1 < len(s) and s[i-1] == s[i+1]:
                r = s[i]
                j = i - 1
                k = i + 1
                while j >= 0 and k < len(s) and s[j] == s[k]:
                    r = s[j] + r
                    r += s[k]
                    j -= 1
                    k += 1
            if r:
                result.update({len(r): r})
        print result
        if result:
            return result[max(result.keys())]
        elif s:
            return s[0]
        else:
            return ""
```

34. [字符串转换整数 (atoi)](https://leetcode-cn.com/problems/string-to-integer-atoi/description/)

> Solution: 两种解法，第一直接根据条件做一次遍历得到答案，且需要考虑特殊情况；
第二可以考虑使用正则表达式进行匹配获取答案

> T: N  S: 1 
```python
        # Anylize
        #  special: return 0
        # int32
        # 

        string = string.strip()
        if not string:
            return 0
        l = [str(i) for i in xrange(10)]
        o = ["-", "+"]
        result = ""
        for v in string:
            if v in o and not result:
                result += v
            elif v in l:
                result += v
            elif not result:
                return 0
            else:
                break
        if result == "+" or result == "-":
            return 0
        if not (-2 **31 <= int(result) <= 2**31 -1):
            if int(result) < 0:
                return -2 ** 31
            else:
                return 2 ** 31 -1
        return int(result)

# regular expresion
class Solution:
    def myAtoi(self, s: str) -> int:
        return max(min(int(*re.findall('^[\+\-]?\d+', s.lstrip())), 2**31 - 1), -2**31)
        
```

35. [罗马数字转整数](https://leetcode-cn.com/problems/roman-to-integer/description/)

> Solution:
> T:  S:
```python
        # Anylize:
        # 1. put cha and number into dict
        # 2. for the s and handle special case and get number

        result = []
        r_d = {
            "I" : 1,
            "V" : 5,
            "X" : 10,
            "L" : 50,
            "C" : 100,
            "D" : 500,
            "M" : 1000,
        }
        for i in s:
            m = 0
            if i in ["V", "X"] and result and result[len(result) - 1] == 1:
                m = 1
            elif i in ["L", "C"] and result and result[len(result) - 1] == 10:
                m = 10
            elif i in ["D", "M"] and result and result[len(result) - 1] == 100:
                m = 100
            else:
                pass
            if m != 0:
                result = result[:len(result) -1]
            v = r_d[i] - m
            result.append(v)
        sum = 0
        if not result:
            return 0
        else:
            for v in result:
                sum += int(v)
        return sum
```

36. [三数之和](https://leetcode-cn.com/problems/3sum/description/)

> Solution: 排序后，选定一个负值，使用双指针从选定值的后一个值和末尾元素开始，如果三数之和小于0则表示末尾值太大需要前移，同理大于0指针后移，最终将两个指针相遇前的所以满足结果保存在列表里；
> T:  N**2 S: 1
```python

        # sort and 2 points

        result = []
        nums.sort() #nlog(n)
        k = 0
        while nums and len(nums) > 2 and nums[k] <= 0 and k < len(nums) -1: # n
            if nums[k] > 0: break # 最外层循环只遍历小于等于0的值，如果遇到大于0的值直接跳出
            # 
            # 遇到重复直接前移一个元素，去除重复答案
            if k != 0 and nums[k] == nums[k-1]: k+=1; continue 
            i = k + 1
            j = len(nums) -1
            # 循环n次
            while i < j:
                s = nums[i] + nums[k] + nums[j]
                if s < 0:
                    i += 1
                    while i <j and nums[i] == nums[i - 1]: i += 1 # 去重
                elif s > 0:
                    j -= 1
                    while i < j and nums[j] == nums[j + 1]: j -= 1 # 去重
                else:
                    t = [nums[i], nums[k], nums[j]]
                    result.append(t)
                    i += 1
                    j -= 1
                    while i < j and nums[i] == nums[i - 1]: i += 1
                    while i < j and nums[j] == nums[j + 1]: j -= 1
            k += 1

        return result


    # T: nlog(n) + n**2  == n**2
```

37. [有效的括号](https://leetcode-cn.com/problems/valid-parentheses/description/)

> Solution:
> T:  S:
```python

```

38. [合并两个有序链表](https://leetcode-cn.com/problems/merge-two-sorted-lists/description/)

> Solution:
> T:  S:
```python

```

39. [合并K个排序链表](https://leetcode-cn.com/problems/merge-k-sorted-lists/description/)

> Solution:
> T:  S:
```python

```

40. [两两交换链表中的节点](https://leetcode-cn.com/problems/swap-nodes-in-pairs/description/)

> Solution:
> T:  S:
```python

```

41. [K 个一组翻转链表](https://leetcode-cn.com/problems/reverse-nodes-in-k-group/description/)

> Solution:
> T:  S:
```python

```

42. [删除排序数组中的重复项](https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array/description/)

> Solution:
> T:  S:
```python

```

43. [实现 strStr()](https://leetcode-cn.com/problems/implement-strstr/description/)

> Solution:
> T:  S:
```python

```

44. [搜索旋转排序数组](https://leetcode-cn.com/problems/search-in-rotated-sorted-array/description/)

> Solution:
> T:  S:
```python

```

45. [全排列](https://leetcode-cn.com/problems/permutations/description/)

> Solution:
> T:  S:
```python

```

46. [全排列 II](https://leetcode-cn.com/problems/permutations-ii/description/)

> Solution:
> T:  S:
```python

```

47. # [简化路径](https://leetcode-cn.com/problems/simplify-path/description/)

> Solution: 切忌切忌切忌 不能一上来就按照条件开始coding
在使用split和栈做存储的情况下，本题的效率和代码数量提高了一个量级，遇到这样的字符串分割的问题千万不能一个字符一个字符去过
> T: N S: N
```python
        # ❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌
        # path = list(path)
        # slash = [0] if path[0] == "/" else []
        # i = 0
        # while i < len(path):
        #     # 遇到//不处理
        #     i += 1
        #     if not (i +1 < len(path)): break
        #     if (path[i] == path[i-1] == "/"):
        #         path.pop(i)
        #         i -= 1
        #         continue
        #     elif path[i] == "/" and path[i-1] != "/":
        #         slash.append(i)
        #         continue
        #     if path[i] == "." and path[i + 1] == ".":
        #         if i + 2 < len(path):
        #             if len(slash) < 2:
        #                 path = path[i + 2:]
        #                 i = 0
        #             else:
        #                 path = path[:slash[-2]] + path[i + 2:]
        #                 i = slash[-2]
        #             slash.pop(-1)
        #         elif i + 2 == len(path):
        #             if len(slash) < 2:
        #                 path = path[:i]
        #             else:
        #                 path = path[:slash[-2]] + path[i + 2:]
        #     elif path[i] == "." and path[i + 1] != ".":
        #         path.pop(i)
        #         path.pop(i)
        #         i -= 1
        # while path[-1] == ".": path.pop(-1)
        # while len(path) > 1 and path[-1] == "/": path.pop(-1)
        # return "".join(path)
        # ❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌TRASH

        #解决方案： 栈  split("/")
        # 遇到这样的字符过滤的问题，一定要想到栈
                    
        stack = []
        l = path.split("/")
        for v in l:
            # case
            if not v:
                pass
            elif v == ".":
                pass
            elif v == '..':
                if stack: stack.pop(-1)
            else:
                stack.append(v)
        return "/" + "/".join(stack)
```

48. [矩阵置零](https://leetcode-cn.com/problems/set-matrix-zeroes/description/)

> Solution: 此题目的关键在于如何记录是那些行那些列需要全部置0，所有使用m+n的空间记录所有需要置0的行列，更加简单的方式是直接在第一行第一列记录 m n 所有要置0的行列，对第一行第一列只需要在最开始用两个常数或者布尔值记录是否含有0就可以
> T: m*n S: 1
```python
        # 常数空间
        # 以第一行第一列为标记点，先判断第一行第一列的情况，记录0的数量
        # 将其他数据中的0放在第一行第一列相应位置
        # 修改全部数据
        # 1 0 0 0
        # 0 1 0 1
        # 1 1 1 1
        # 0 1 1 0

        f_row = False
        f_column = False
        if 0 in matrix[0]: f_row = True
        for i in range(len(matrix)):
            if matrix[i][0] == 0: f_column = True
        
        for m in range(1, len(matrix)):
            for n in range(1, len(matrix[0])):
                if matrix[m][n] == 0:
                    matrix[0][n] = 0
                    matrix[m][0] = 0

        for x in range(1, len(matrix)):
            if matrix[x][0] == 0:
                for t in range(1, len(matrix[x])): matrix[x][t] = 0

        for y in range(1, len(matrix[0])):
            if matrix[0][y] == 0:
                for t in range(1, len(matrix)): matrix[t][y] = 0

        if f_row:
            for t in range(0, len(matrix[0])): matrix[0][t] = 0
        
        if f_column:
            for t in range(0, len(matrix)): matrix[t][0] = 0

        return matrix
```

49. [颜色分类](https://leetcode-cn.com/problems/sort-colors/description/)

本问题被称为 [荷兰国旗问题](https://en.wikipedia.org/wiki/Dutch_national_flag_problem)

> Solution: 不要使用insert和pop的方式，特殊情况难以处理；
> T:  S:
```python
        # 因为是线性数组，一次遍历使用双指针最为高效
        # 因为该题目为三中类型的元素
        # 所以需要双指针来跟踪边缘
        # 增加一个循环指针

        p = 0
        edge_l = 0
        edge_r = len(nums) - 1
        while p <= edge_r:
            if nums[p] == 0:
                #左边缘右移
                nums[p], nums[edge_l] = nums[edge_l], nums[p]
                edge_l += 1
                p += 1
            elif nums[p] == 2:
                #和右边缘护环
                nums[p], nums[edge_r] = nums[edge_r], nums[p]
                edge_r -= 1
            elif nums[p] == 1:
                p += 1

        return nums


        # 使用insert和pop方式

        if (1 not in nums and 2 not in nums) or (1 not in nums and 0 not in nums) or (0 not in nums and 2 not in nums):
            return nums
    
        i = 0
        count = 0
        while i < len(nums) and len(nums) > 1:
            if nums[i] == 0:
                nums.insert(0, 0)
                nums.pop(i + 1)
                i += 1
                if count: count = 0
            elif nums[i] == 2:
                if count >= len(nums) - i:
                    break
                nums.append(2)
                nums.pop(i)
                count += 1
            else:
                i += 1
                if count: count = 0

        return nums
```

50. [单词搜索](https://leetcode-cn.com/problems/word-search/description/)
**TODO**
> Solution: 在一个二维数组中找到一个单词，与前一个字母上下左右相邻的都可以做下一个元素；上下左右，只能是从这四个里面找下一个元素；
>
> 解法：类似图的深度优先遍历，一次找到和单词中第一个字母相同的字母，从第一个开始就开始用“递归”遍历，当未找到某个字母的时候，回溯在前一个字母，直到回溯回第一个字母还是没有找到结果，就开始对第二个找到的字母做同样的递归，递归需要注意：边界条件和return点，return决定了回溯的情况；对于已经找到的结果可以存储在栈中，python使用list来模拟栈；
>
> T: M*N  S:
>
> ```
> board =
> [
>   ['A','B','C','E'],
>   ['S','F','C','S'],
>   ['A','D','E','E']
> ]
> 
> 给定 word = "ABCCED", 返回 true.
> 给定 word = "SEE", 返回 true.
> 给定 word = "ABCB", 返回 false.
> ```
```python
class Solution(object):
    
    # 定义上下左右四个行走方向
    directs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    def exist(self, board, word):
        """
        :type board: List[List[str]]
        :type word: str
        :rtype: bool
        """
        m = len(board)
        if m == 0:
            return False
        n = len(board[0])
        mark = [[0 for _ in range(n)] for _ in range(m)]
                
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == word[0]:
                    # 将该元素标记为已使用
                    mark[i][j] = 1
                    if self.backtrack(i, j, mark, board, word[1:]) == True:
                        return True
                    else:
                        # 回溯
                        mark[i][j] = 0
        return False
        
        
    def backtrack(self, i, j, mark, board, word):
        if len(word) == 0:
            return True
        
        for direct in self.directs:
            cur_i = i + direct[0]
            cur_j = j + direct[1]
            
            if cur_i >= 0 and cur_i < len(board) and cur_j >= 0 and cur_j < len(board[0]) and board[cur_i][cur_j] == word[0]:
                # 如果是已经使用过的元素，忽略
                if mark[cur_i][cur_j] == 1:
                    continue
                # 将该元素标记为已使用
                mark[cur_i][cur_j] = 1
                if self.backtrack(cur_i, cur_j, mark, board, word[1:]) == True:
                    return True
                else:
                    # 回溯
                    mark[cur_i][cur_j] = 0
        return False
```

51. [解码方法](https://leetcode-cn.com/problems/decode-ways/description/)

> Solution: 本题的求解方式是动态规划，题目中没有明确指出对于0的处理情况， 所以需要考虑0值的处理问题，尤其是不符合规则出现的0；
>
> 动态规划： 
>
> 1. dp保存到点i为止出现的所有可能之和
> 2. 通过21～26和11～19可知，对于这种情况的i处的状态就是 dp[i] = dp[i -1] + dp[i-2],   其他情况就是 dp[i] = dp[i - 1]
> 3. 一次遍历并将条件带入状态转移方程，最终得到结果，特殊情况是0值的考虑
>
> T:  S:
```python
# 动态规划，找出dp[i] dp[i-1] dp[i-2] 之间的关系
        # 1 ~ 9 
        # 10 ~ 19 
        # 20 ~ 26
        # 226
        # i = 0: dp[0] = 1
        # i = 1: dp[1] = dp[0] + (if 2 < 6)
        # i = 2: dp[2] = dp[1] + ()

        # if s[0] == "0": return 0

        # 22619
        dp = []
        for i in range(len(s)):
            if i == 0:
                if s[0] != "0":
                    dp.append(1)
                else:
                    return 0
                continue
            if s[i] == "0":
                if s[i-1] == "1" or s[i-1] == "2":
                    if i == 1:
                        dp.append(dp[i-1])
                        continue
                    dp.append(dp[-2])
                    continue
                else:
                    return 0
            if s[i - 1] == "0":
                dp.append(dp[-1])
                continue
            if (s[i - 1] == "2" and s[i] <= "6") or (s[i - 1] == "1"):
                if i == 1:
                    dp.append(dp[i-1] + 1)
                    continue
                if dp[i -2] == "0":
                    dp.append(dp[i - 1] + 1)
                else:
                    dp.append(dp[i -1] + dp[i - 2])
            else:
                dp.append(dp[-1])
            print dp

        return dp[-1]
```

52. [二叉树的中序遍历](https://leetcode-cn.com/problems/binary-tree-inorder-traversal/description/)

> Solution: 二叉树的五种遍历方式，其中和跟节点在三点见顺序有关系的是中序遍历、前序遍历、后序遍历、BFS、DFS
>
> 前序遍历： 跟节点 〉左子树 〉右子树
>
> 中序遍历： 左子树 〉跟节点 〉右子树
>
> 后序遍历： 左子树 〉右子树 〉跟节点
>
> 本题目要求用迭代的方式求中序遍历
>
> T:  S:
```python
        # 在不使用递归的方式的情况下，使用栈来记录数据，完成中序
        # public class Solution {
        #     public List < Integer > inorderTraversal(TreeNode root) {
        #     List < Integer > res = new ArrayList < > ();
        #     Stack < TreeNode > stack = new Stack < > ();
        #     TreeNode curr = root;
        #     while (curr != null || !stack.isEmpty()) {
        #         while (curr != null) {
        #             stack.push(curr);
        #             curr = curr.left;
        #         }
        #         curr = stack.pop();
        #         res.add(curr.val);
        #         curr = curr.right;
        #     }
        #     return res;
        # }
        # 递归的方式
        # class Solution {
        #     public List < Integer > inorderTraversal(TreeNode root) {
        #         List < Integer > res = new ArrayList < > ();
        #         helper(root, res);
        #         return res;
        #     }

        #     public void helper(TreeNode root, List < Integer > res) {
        #         if (root != null) {
        #             if (root.left != null) {
        #                 helper(root.left, res);
        #             }
        #             res.add(root.val);
        #             if (root.right != null) {
        #                 helper(root.right, res);
        #             }
        #         }
        #     }
        # }
        #时间复杂度：O(n)O(n)。递归函数 T(n)=2⋅T(n/2)+1T(n)=2⋅T(n/2)+1。
        #    空间复杂度：最坏情况下需要空间O(n)O(n)，平均情况为O(log⁡n)O(logn)。
 

        stack = []
        result = []
        current = root
        while current or stack:
            # 找到当前节点的最左
            while current:
                stack.append(current)
                current = current.left
            # 当前节点的最左应该是遍历的第一个值
            # 外层循环将没有找到right的节点,将继续吧目标值更新为栈顶的值
            current = stack.pop(-1)
            result.append(current.val)
            # 寻找当前节点的第一个right，找到right后再对right做同样的一直找左子树的操作
            current = current.right
        return result

        # 时间复杂度： 假设结果长度为n，那么时间复杂度为n  空间复杂度 n

```

53. [验证二叉搜索树](https://leetcode-cn.com/problems/validate-binary-search-tree/description/)
给定一个二叉树，判断其是否是一个有效的二叉搜索树。

> Solution: 验证二叉搜索树，使用递归或者迭代的中序遍历，对遍历结果进行实时判断如果一点出现非升序元素则不是二叉搜索树
>
> 对于递归处理的方式，一定要考虑return的使用方式
>
> T:  S:
```python
        # 验证二叉搜索树
        # 解法：对二叉树做中序遍历，判断每次新加的值是否比前一个值大
        # 重要重要重要 ： 两个数相等也是不符合搜索二叉树的条件的


        # stack = []
        # result = []
        # current = root
        # while current or stack:
        #     # 找到当前节点的最左
        #     while current:
        #         stack.append(current)
        #         current = current.left
        #     # 当前节点的最左应该是遍历的第一个值
        #     # 外层循环将没有找到right的节点,将继续吧目标值更新为栈顶的值
        #     current = stack.pop(-1)
        #     if result and current.val <= result[-1]: return False
        #     result.append(current.val)
        #     # 寻找当前节点的第一个right，找到right后再对right做同样的一直找左子树的操作
        #     current = current.right
        # return True


        # 递归的方式实现
        # 使用递归对二叉树进行中序遍历，遍历的结果必须有序才符合条件
        # 遍历的每一次操作都需要对比

        def middle(node, res):
            if not node:
                return True
            if res and node.val <= res[-1]: return False
            if node.left: 
                if not middle(node.left, res): return False
            if res and node.val <= res[-1]: return False
            res.append(node.val)
            if node.right: 
                if not middle(node.right, res): return False
            return True
        
        res = []
        return middle(root, res)


        # 递归分析
        # 1. append + left
        # 2. append + left
        # x. 最左的所有节点都放在栈中了，拿出栈顶元素（栈顶元素就是树的左叶子节点）,将值放入结果中
        # x + 1. 回溯找到将右边的第一个节点，左同样的1到n的递归
```

54. [二叉树的层次遍历](https://leetcode-cn.com/problems/binary-tree-level-order-traversal/description/)

> Solution: 
>
> 本题解法为广度优先遍历
> 广度优先遍历需要使用到队列
> 如何控制分界线
>
> 控制分界线的方式是追踪当前每层实时的节点总数，2**n - last_nll * 2 - current_null
>
> 每层在满树的情况下的总数2的n次方 - 上一层为空的节点数*2 - 当前节点为空的数量
>
> 如果queue中有相同数目的元素则拷贝一份到答案数组；
>
> 分解条件的数学原因为： n > 1时候 总有： n - 1+ 2 < 2 * n   n -1 + 1 < 2 *n -1
>
> T:  S:
```python
        # 本题解法为广度优先遍历
        # 广度优先遍历需要使用到队列
        # 如何控制分界线

        queue = [root]
        result = []
        last_null = 0
        current_null = 0
        while queue and root:
            if len(queue) == 2**len(result) - last_null * 2 - current_null:
                last_null = last_null * 2 + current_null
                current_null = 0
                result.append([n.val for n in queue])
            node = queue.pop(0)
            if node.left:
                queue.append(node.left)
            else:
                current_null += 1
            if node.right:
                queue.append(node.right)
            else:
                current_null += 1

        return result
```

55. [二叉树的锯齿形层次遍历](https://leetcode-cn.com/problems/binary-tree-zigzag-level-order-traversal/description/)

> Solution: 本题和上一题基本完全一致，每层遍历顺序相反的二叉树BFS遍历为二维数组，只需要将读取队列中的值的步骤依赖当前层次的奇偶性就可以完成；
> T:  S:
```python
 # def findBottomLeftValue(self, root):
        # """
        # :type root: TreeNode
        # :rtype: int
        # """
        # # 使用队列从右往左广度优先遍历整个树，输出最后一个元素就是最后一行最左边的元素
        # queue_l = []
        # queue_l.append(root)

        # while queue_l:
        #     node = queue_l.pop(0)
        #     if node.right:
        #         queue_l.append(node.right)
        #     if node.left:
        #         queue_l.append(node.left)
        #     if not queue_l:
        #         return node.val

        # 本题解法为广度优先遍历
        # 广度优先遍历需要使用到队列
        # 如何控制分界线

        queue = [root]
        result = []
        last_null = 0
        current_null = 0
        while queue and root:
            if len(queue) == 2**len(result) - last_null * 2 - current_null:
                last_null = last_null * 2 + current_null
                current_null = 0
                result.append([n.val for n in queue])
            node = queue.pop(0)
            if node.left:
                queue.append(node.left)
            else:
                current_null += 1
            if node.right:
                queue.append(node.right)
            else:
                current_null += 1

        return result

```

56. [从中序与后序遍历序列构造二叉树](https://leetcode-cn.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/description/)

> Solution:
> T:  S:
```python
# 解法，从后序遍历中的末尾元素可以找到第一个根结点，找到该节点在中序遍历中的位置
        # 此时该位置前的元素为左孩子，后面的元素为又孩子
        # 递归继续对前后两个孩子进行同样操作

        # 难度： 1. 树的还原 2. 递归返回

        # TODO - recoding
        # 递归函数
        def helper(in_left, in_right):
            # if there is no elements to construct subtrees
            # 4. 第三步中的 index+1 in_right 当到达同一个点时也就是不可再分割是，就是index+1 > in_right，所以返回空
            if in_left > in_right:
                return None
            
            # pick up the last element as a root
            # 1. 从后序遍历中获取根结点，并生成根结点TreeNode
            val = postorder.pop()
            root = TreeNode(val)

            # root splits inorder list
            # into left and right subtrees
            # 2. 在中序遍历中找到根节点的索引值
            index = idx_map[val]
 
            
            # 3. 将根节点左右两边的值进行递归生成新的根节点和子树
            #    因为后续遍历找到根节点是从右边子树开始所以，先对右边左递归
            #    这里传入的参数有两个作用，第一用来限定递归次数也就是分割次数，第二使用来判断是否已经到达叶子节点

            # build right subtree
            root.right = helper(index + 1, in_right)
            # build left subtree
            root.left = helper(in_left, index - 1)
            return root
        # 最终递归结束后返回给第一次调用的根节点
        
        # build a hashmap value -> its index
        # 将list列表转换为哈希表，方便定位元素
        idx_map = {val:idx for idx, val in enumerate(inorder)} 
        return helper(0, len(inorder) - 1)

        # 时间复杂度分析：
        # 递归树分析   


        # 时间复杂度：
        # 由主定理考虑： 
        # T(n) = aT(n/b) + f(n) 表示将 T(n) 的问题分解为a个 T(n/b)，
        # 在每次递归中二叉树涉及到的规模为初始问题的两个子问题a=2，因为左右子树在递归中每次各计算一次所以这里b=2, 
        # logb(a) log以b为底的a表示问题被分解为a个子问题规模, O(n**logb(a))
        # f(n)


        # 空间复杂度：O(N)存储整棵树。

```

57. [路径总和](https://leetcode-cn.com/problems/path-sum/description/)

> Solution:
> T:  S:
```python
        # 二叉树的两种基本遍历
        # BFS 使用队列
        # DFS 使用栈

        # DFS 迭代 栈
        # 栈中的每一个元素都存储了到该元素位置的总和，所以迭代在不满足条件的情况下，深度遍历继续进行可以继续找目标值

        if not root:
            return False

        de = [(root, sum - root.val), ]
        while de:
            node, curr_sum = de.pop()
            if not node.left and not node.right and curr_sum == 0:  
                return True
            if node.right:
                de.append((node.right, curr_sum - node.right.val))
            if node.left:
                de.append((node.left, curr_sum - node.left.val))
        return False
```

58. [复制带随机指针的链表](https://leetcode-cn.com/problems/copy-list-with-random-pointer/description/)

> Solution:  用递归回溯的方式扫描整个链表，并存储已经创建的拷贝
> T:  N S: N
```python
        # 用来保存当前访问的节点深拷贝出来的新节点
        self.hash_map = {}

        def recursive_copy(head_node):
            if not head_node:
                return None

            # 1. hash_map 中保存了当前访问节点和初始化的拷贝节点
            # 如果不存在则证明该节点还没创建
            new_node = self.hash_map.get(head_node)
            if not new_node: 
                # 1. 拷贝值创建新节点， 并存入hash_map
                new_node = Node(head_node.val, None, None)
                self.hash_map.update({head_node: new_node})
            else:
                # 2. 在已经拷贝过的node里找到了已经新建的node就要直接返回，否则会导致循环递归，最终达到递归上限
                return new_node

            # 3. 拷贝自己的next，如果存在直接返回
            new_node.next = recursive_copy(head_node.next)
            # 4. 拷贝自己的random，如果存在直接返回
            new_node.random = recursive_copy(head_node.random)

            return new_node

        return recursive_copy(head)

```

59. [二叉树展开为链表](https://leetcode-cn.com/problems/flatten-binary-tree-to-linked-list/description/)

> Solution:
> T:  S:
```python
 # 94题 mirrors

        # 原地算法，直接将所有值接到节点的右子树

        # 使用后序遍历
        #     1
        #    / \
        #   2   5
        #  / \   \
        # 3   4   6

        #     1
        #    / \
        #   2   5
        #    \   \
        #     3   6
        #      \
        #       4

        # 1
        #  \
        #   2
        #    \
        #     3
        #      \
        #       4
        #        \
        #         5
        #          \
        #           6
        # 使用后续遍历，将第一个找到的右子树改为第一个找到的左子树的右孩子
        # 并递归活迭代

        # 递归

        # 改变方向的从右向左的后序遍历
        self.last_right = None # 上一个已经排到右边的节点，活着说上个已经完成转链表的节点
        def recursive_post(node):
            if not node: return
            recursive_post(node.right)
            recursive_post(node.left)
            node.right = self.last_right
            node.left = None
            self.last_right = node
        
        return recursive_post(root)


        # public void flatten(TreeNode root) { 
        #     Stack<TreeNode> toVisit = new Stack<>();
        #     TreeNode cur = root;
        #     TreeNode pre = null;

        #     while (cur != null || !toVisit.isEmpty()) {
        #         while (cur != null) {
        #             toVisit.push(cur); // 添加根节点
        #             cur = cur.right; // 递归添加右节点
        #         }
        #         cur = toVisit.peek(); // 已经访问到最右的节点了
        #         // 在不存在左节点或者右节点已经访问过的情况下，访问根节点
        #         if (cur.left == null || cur.left == pre) {
        #             toVisit.pop(); 
        #             /**************修改的地方***************/
        #             cur.right = pre;
        #             cur.left = null;
        #             /*************************************/
        #             pre = cur;
        #             cur = null;
        #         } else {
        #             cur = cur.left; // 左节点还没有访问过就先访问左节点
        #         }
        #     } 
        # }

        # de = [(root, sum - root.val), ]
        # while de:
        #     node, curr_sum = de.pop()
        #     if not node.left and not node.right and curr_sum == 0:  
        #         return True
        #     if node.right:
        #         de.append((node.right, curr_sum - node.right.val))
        #     if node.left:
        #         de.append((node.left, curr_sum - node.left.val))
        # return False
```

60. [填充每个节点的下一个右侧节点指针](https://leetcode-cn.com/problems/populating-next-right-pointers-in-each-node/description/)

> Solution:
> T:  S:
```python
def connect(self, root):
        """
        :type root: Node
        :rtype: Node
        """

        # 层序遍历，从最下层往最上层

        queue = [root]
        level = 0
        last_null = 0
        current_null = 0
        left_node = None
        while queue and root:
            if len(queue) == 2**level - last_null * 2 - current_null:
                last_null = last_null * 2 + current_null
                current_null = 0
                level += 1
                
                # 完全二叉树，不用考虑缺少的左右子树，所以可以忽略last_null和current_null
                for i in range(len(queue)-1):
                    queue[i].next = queue[i+1]
                left_node = queue[0]
            node = queue.pop(0)
            if node.left:
                queue.append(node.left)
            else:
                current_null += 1
            if node.right:
                queue.append(node.right)
            else:
                current_null += 1
            node.right = None
            if node != left_node: node.left = None

        return root
```

61.[填充每个节点的下一个右侧节点指针 II](https://leetcode-cn.com/problems/populating-next-right-pointers-in-each-node-ii/description/)

> Solution:
> T:  S:
```python
def connect(self, root):
        """
        :type root: Node
        :rtype: Node
        """
        queue = [root]
        level = 0
        last_null = 0
        current_null = 0
        left_node = None
        while queue and root:
            if len(queue) == 2**level - last_null * 2 - current_null:
                last_null = last_null * 2 + current_null
                current_null = 0
                level += 1
                
                # 完全二叉树，不用考虑缺少的左右子树，所以可以忽略last_null和current_null
                left_node = queue[-1]
                for i in range(len(queue)-1):
                    queue[i].next = queue[i+1]
                    if left_node == queue[-1] and (queue[i].left or queue[i].right): left_node = queue[i]
            node = queue.pop(0)
            if node.left:
                queue.append(node.left)
            else:
                current_null += 1
            if node.right:
                queue.append(node.right)
            else:
                current_null += 1
            if node == left_node:
                if node.left and node.right:
                    node.right = None
                continue
            node.left = None
            node.right = None


        return root
```

62. [复制带随机指针的链表](https://leetcode-cn.com/problems/copy-list-with-random-pointer/description/)

> Solution:
> T:  S:
```python
def copyRandomList(self, head):
        """
        :type head: Node
        :rtype: Node
        """
        # 用来保存当前访问的节点深拷贝出来的新节点
        self.hash_map = {}

        def recursive_copy(head_node):
            if not head_node:
                return None

            # 1. hash_map 中保存了当前访问节点和初始化的拷贝节点
            # 如果不存在则证明该节点还没创建
            new_node = self.hash_map.get(head_node)
            if not new_node: 
                # 1. 拷贝值创建新节点， 并存入hash_map
                new_node = Node(head_node.val, None, None)
                self.hash_map.update({head_node: new_node})
            else:
                # 2. 在已经拷贝过的node里找到了已经新建的node就要直接返回，否则会导致循环递归，最终达到递归上限
                return new_node

            # 3. 拷贝自己的next，如果存在直接返回
            new_node.next = recursive_copy(head_node.next)
            # 4. 拷贝自己的random，如果存在直接返回
            new_node.random = recursive_copy(head_node.random)

            return new_node

        return recursive_copy(head)
```

63. [环形链表](https://leetcode-cn.com/problems/linked-list-cycle/description/)

> Solution:
> T:  S:
>
> 
```python
if not head or not head.next:
            return False

        p1 = head
        p2 = head.next
        while p1 != p2:
            if not p1 or not p2 or not p2.next:
                return False
            p1 = p1.next
            p2 = p2.next.next

        return True
```

64. [LRU缓存机制](https://leetcode-cn.com/problems/lru-cache/description/)

> Solution:
> T:  S:
```python
from collections import OrderedDict
class LRUCache(OrderedDict):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key not in self:
            return - 1
        
        self.move_to_end(key)
        return self[key]

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: void
        """
        if key in self:
            self.move_to_end(key)
        self[key] = value
        if len(self) > self.capacity:
            self.popitem(last = False)
```

65. [翻转字符串里的单词](https://leetcode-cn.com/problems/reverse-words-in-a-string/description/)

> Solution:
> T:  S:
```python
        # python
        # 解法1: 先用strip，然后split，然后反向读取list在转为字符串
        # 解法2: 不使用额外n空间，先strip，然后在字符串前加两个空格，然后读取到第一个单词，
        # 将开始坐标和单词结束坐标的字符加到字符串末尾并删除，依次对所有单词做同样操作，直到找到末尾坐标（后面出现两个连续空格）
        # 解法3：不使用额外n空间，原地算法，双指针
```

66.

> Solution:
> T:  S:
```python
        # 使用迭代的二分查找或者递归的二分搜索的方法

        # 解法： 1. 递归
        # 找出二分搜索的中间点
        # 比较是否 中间点的值大于其后一个值，如果大于则证明，中间点位于一个局部下降的位置，
        # 那么它左边肯定有至少一个peek点，那么继续对左边做二分搜索
        # 如果，中间点的值小于其后面一个值，那么中间点在一个局部上升位置
        # 那么它右边肯定有一个peek，递归
        # 最终l r相等就可以得到结果

        #public class Solution {
        #     public int findPeakElement(int[] nums) {
        #         return search(nums, 0, nums.length - 1);
        #     }
        #     public int search(int[] nums, int l, int r) {
        #         if (l == r)
        #             return l;
        #         int mid = (l + r) / 2;
        #         if (nums[mid] > nums[mid + 1])
        #             return search(nums, l, mid);
        #         return search(nums, mid + 1, r);
        #     }
        # }


        def search_peek(nums, l, r):
            if l == r:
                return l

            middle = (l + r) /2
            # \  down from middle to middle + 1
            if nums[middle] > nums[middle + 1]:
                return search_peek(nums, l, middle)
            # / up from middle to middel +1
            else:
                return search_peek(nums, middle + 1, r)


        return search_peek(nums, 0, len(nums) -1)
```


> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```

> Solution:
> T:  S:
```python

```
---
---
# 所有重点题型

1. # [两数相加](https://leetcode-cn.com/problems/add-two-numbers/description/)

2. # [最长回文子串](https://leetcode-cn.com/problems/longest-palindromic-substring/description/)

3. # [字符串转换整数 (atoi)](https://leetcode-cn.com/problems/string-to-integer-atoi/description/)

4. # [三数之和](https://leetcode-cn.com/problems/3sum/description/)

5. # [合并K个排序链表](https://leetcode-cn.com/problems/merge-k-sorted-lists/description/)

6. # [两两交换链表中的节点](https://leetcode-cn.com/problems/swap-nodes-in-pairs/description/)

7. # [K 个一组翻转链表](https://leetcode-cn.com/problems/reverse-nodes-in-k-group/description/)

8. # [搜索旋转排序数组](https://leetcode-cn.com/problems/search-in-rotated-sorted-array/description/)

9. # [全排列](https://leetcode-cn.com/problems/permutations/description/)

10. # [全排列 II](https://leetcode-cn.com/problems/permutations-ii/description/)

11. # [旋转图像](https://leetcode-cn.com/problems/rotate-image/description/)

12. # [螺旋矩阵](https://leetcode-cn.com/problems/spiral-matrix/description/)

13. # [跳跃游戏](https://leetcode-cn.com/problems/jump-game/description/)

14. # [合并区间](https://leetcode-cn.com/problems/merge-intervals/description/)

15. # [简化路径](https://leetcode-cn.com/problems/simplify-path/description/)

16. # [矩阵置零](https://leetcode-cn.com/problems/set-matrix-zeroes/description/)

17. # [颜色分类](https://leetcode-cn.com/problems/sort-colors/description/)

18. # [单词搜索](https://leetcode-cn.com/problems/word-search/description/)

19. # [解码方法](https://leetcode-cn.com/problems/decode-ways/description/)

20. # [二叉树的中序遍历](https://leetcode-cn.com/problems/binary-tree-inorder-traversal/description/)

21. # [验证二叉搜索树](https://leetcode-cn.com/problems/validate-binary-search-tree/description/)

22. # [二叉树的层次遍历](https://leetcode-cn.com/problems/binary-tree-level-order-traversal/description/)

23. # [二叉树的锯齿形层次遍历](https://leetcode-cn.com/problems/binary-tree-zigzag-level-order-traversal/description/)

24. # [从中序与后序遍历序列构造二叉树](https://leetcode-cn.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/description/)

25. # [路径总和](https://leetcode-cn.com/problems/path-sum/description/)

26. # [二叉树展开为链表](https://leetcode-cn.com/problems/flatten-binary-tree-to-linked-list/description/)

27. # [填充每个节点的下一个右侧节点指针](https://leetcode-cn.com/problems/populating-next-right-pointers-in-each-node/description/)

28. # [填充每个节点的下一个右侧节点指针 II](https://leetcode-cn.com/problems/populating-next-right-pointers-in-each-node-ii/description/)

29. # [买卖股票的最佳时机-全部股票相关题目](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock/description/)

30. 

---
---




# 题目
https://leetcode-cn.com/problems/two-sum/solution/liang-shu-zhi-he-by-leetcode-2/
https://blog.csdn.net/l975764577/article/details/39399077
https://www.cnblogs.com/absfree/p/5463372.html
https://leetcode-cn.com/problems/add-two-numbers/solution/liang-shu-xiang-jia-by-leetcode/
https://leetcode-cn.com/problems/median-of-two-sorted-arrays/solution/xun-zhao-liang-ge-you-xu-shu-zu-de-zhong-wei-shu-b/
https://lufficc.com/blog/binary-search-tree
https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock/solution/mai-mai-gu-piao-de-zui-jia-shi-ji-by-leetcode/
https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock/solution/yi-ge-fang-fa-tuan-mie-6-dao-gu-piao-wen-ti-by-l-3/
https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-ii/solution/mai-mai-gu-piao-de-zui-jia-shi-ji-ii-by-leetcode/
https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-iii/solution/java-1ms-100dong-tai-gui-hua-li-yong-si-ge-bian-li/
https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-iv/solution/yi-ge-tong-yong-fang-fa-tuan-mie-6-dao-gu-piao-w-5/
https://gitee.com/x3code/algo-book
https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-iii/solution/java-1ms-100dong-tai-gui-hua-li-yong-si-ge-bian-li/
https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/
https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/solution/yi-ge-fang-fa-tuan-mie-6-dao-gu-piao-wen-ti-by-l-2/
https://gitee.com/labuladong/algo-book/blob/master/labuladong的算法小抄.pdf
https://stackoverflow.com/questions/7604966/maximum-and-minimum-values-for-ints
https://leetcode-cn.com/problems/remove-comments/solution/shan-chu-zhu-shi-by-leetcode/
https://leetcode-cn.com/problems/bulb-switcher-ii/solution/deng-pao-kai-guan-ii-by-leetcode/
https://leetcode-cn.com/problems/bulb-switcher/solution/you-jian-dan-li-zi-tui-li-rong-yi-li-jie-by-fall12/
https://www.geeksforgeeks.org/python-math-function-sqrt/
https://leetcode-cn.com/problems/maximum-binary-tree/solution/zui-da-er-cha-shu-by-leetcode/
https://xintiaohuiyi.gitbook.io/jynotebook/shu-ji/shu-ju-jie-gou-yu-suan-fa-zhi-mei/27-di-gui-shu-ff1a-ru-he-jie-zhu-shu-lai-qiu-jie-di-gui-suan-fa-de-shi-jian-fu-za-du-ff1f
https://leetcode-cn.com/problems/2-keys-keyboard/solution/zhi-you-liang-ge-jian-de-jian-pan-by-leetcode/
> 素数，指在大於1的自然数中，除了1和該数自身外，無法被其他自然数整除的数
https://leetcode-cn.com/problems/permutation-in-string/solution/chua-dong-chuang-kou-ji-you-hua-by-never_say_never/
https://juejin.im/post/5c74a2e2f265da2dea053355
https://leetcode-cn.com/problems/longest-palindromic-substring/solution/zui-chang-hui-wen-zi-chuan-by-leetcode/
https://leetcode-cn.com/problems/permutations-ii/solution/hui-su-suan-fa-python-dai-ma-java-dai-ma-by-liwe-2/
https://leetcode-cn.com/problems/permutations/solution/quan-pai-lie-by-leetcode/
https://blog.csdn.net/JonsTank2013/article/details/50898473
https://en.wikipedia.org/wiki/Knuth–Morris–Pratt_algorithm
https://leetcode-cn.com/problems/find-bottom-left-tree-value/solution/cong-you-dao-zuo-de-ceng-xu-bian-li-bu-xu-ji-lu-zh/
https://blog.csdn.net/mingwanganyu/article/details/72033122
https://leetcode.com/tag/breadth-first-search/
https://leetcode-cn.com/problems/add-two-numbers-ii/solution/python-di-gui-zhi-xing-yong-shi-52-ms-zai-suo-you-/
> 用最少数量的箭引爆气球
https://leetcode-cn.com/problems/add-two-numbers-ii/solution/python-di-gui-zhi-xing-yong-shi-52-ms-zai-suo-you-/
https://leetcode-cn.com/problems/string-compression/solution/ya-suo-zi-fu-chuan-by-leetcode/
https://leetcode-cn.com/problems/battleships-in-a-board/solution/cyu-yan-cai-yong-dfsfang-shi-ba-zhao-guo-de-zhan-j/
https://www.jianshu.com/p/70952b51f0c8
https://zhuanlan.zhihu.com/p/24986203
https://leetcode-cn.com/problems/first-unique-character-in-a-string/solution/zi-fu-chuan-zhong-de-di-yi-ge-wei-yi-zi-fu-by-leet/
https://leetcode-cn.com/problems/two-sum/solution/jing-xin-zong-jie-python3-de-san-chong-shi-xian-1b/
https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock/solution/yi-ge-fang-fa-tuan-mie-6-dao-gu-piao-wen-ti-by-l-3/
https://leetcode-cn.com/problems/3sum/solution/pai-xu-shuang-zhi-zhen-zhu-xing-jie-shi-python3-by/
https://leetcode-cn.com/problems/string-to-integer-atoi/solution/python-1xing-zheng-ze-biao-da-shi-by-knifezhu/
https://leetcode-cn.com/problems/longest-palindromic-substring/solution/zui-chang-hui-wen-zi-chuan-by-leetcode/
https://leetcode-cn.com/problems/merge-intervals/solution/he-bing-qu-jian-by-leetcode/
https://leetcode-cn.com/problems/jump-game/solution/tiao-yue-you-xi-by-leetcode/
https://leetcode-cn.com/problems/spiral-matrix/solution/luo-xuan-ju-zhen-by-leetcode/
https://leetcode-cn.com/problems/maximum-subarray/solution/zui-da-zi-xu-he-by-leetcode/
https://leetcode-cn.com/problems/rotate-image/solution/xuan-zhuan-tu-xiang-by-leetcode/
https://leetcode-cn.com/problems/implement-queue-using-stacks/solution/
https://leetcode-cn.com/problems/tag-validator/solution/biao-qian-yan-zheng-qi-by-leetcode/
https://leetcode-cn.com/problems/tag-validator/solution/biao-qian-yan-zheng-qi-by-leetcode/
https://leetcode-cn.com/problems/add-digits/solution/java-o1jie-fa-de-ge-ren-li-jie-by-liveforexperienc/
https://blog.csdn.net/xtj332/article/details/6639009
https://leetcode-cn.com/problems/integer-to-english-words/solution/zheng-shu-zhuan-huan-ying-wen-biao-shi-by-leetcode/
https://leetcode-cn.com/problems/serialize-and-deserialize-binary-tree/solution/er-cha-shu-de-xu-lie-hua-yu-fan-xu-lie-hua-by-leet/
https://leetcode-cn.com/problems/missing-number/solution/que-shi-shu-zi-by-leetcode/
https://leetcode-cn.com/problems/longest-increasing-subsequence/solution/zui-chang-shang-sheng-zi-xu-lie-dong-tai-gui-hua-2/


# 知识点
https://leetcode.com/tag/breadth-first-search/
https://www.jianshu.com/p/70952b51f0c8
http://data.biancheng.net/view/200.html
http://data.biancheng.net/view/201.html
https://wiki.jikexueyuan.com/project/easy-learn-algorithm/fast-sort.html
https://blog.csdn.net/Bone_ACE/article/details/46718683



基本算法的实现，烂熟于心：

二分搜索
二叉树的遍历：深度 前后后 广度 左右
基础动态规划
回溯
迭代
递归
图的 BFS、 DFS
Fib
分治
主定理
kmp 自动机



斐波那契数列的计算

主定理时间复杂度分析：
T(n)=aT(n/b)+f(n)

其中a≥1和b>1是常数，f(n)是渐近正函数。这个递推式将规模为n的问题分解为a个子问题，每个子问题的规模为n/b，a个子问题递归地求解，每个花费时间T(n/b)。函数f(n)包含了问题分解和子问题解合并的代价。

### 图，graph：
* 图：表示多对过的关系的数据结构，实现方式由一个数组和一个二维数字表示，二维数组表示图中每一个顶点与其他顶点之间的联通情况，一维数组表示的是图中每个顶点的值，序号和二维数组中的索引值相对应；

#### 基本概念：
* 弧头和弧尾
> 有向图中，无箭头一端的顶点通常被称为"初始点"或"弧尾"，箭头直线的顶点被称为"终端点"或"弧头"。

* 入度和出度

> 对于有向图中的一个顶点 V 来说，箭头指向 V 的弧的数量为 V 的入度（InDegree，记为 ID(V)）；箭头远离 V 的弧的数量为 V 的出度（OutDegree，记为OD(V)）。

* (V1,V2) 和 <V1,V2> 的区别
> 无向图中描述两顶点（V1 和 V2）之间的关系可以用 (V1,V2) 来表示，而有向图中描述从 V1 到 V2 的"单向"关系用 <V1,V2> 来表示。

> 由于图存储结构中顶点之间的关系是用线来表示的，因此 (V1,V2) 还可以用来表示无向图中连接 V1 和 V2 的线，又称为边；同样，<V1,V2> 也可用来表示有向图中从 V1 到 V2 带方向的线，又称为弧。

* 集合 VR 的含义

> 并且，图中习惯用 VR 表示图中所有顶点之间关系的集合。例如，图 1 中无向图的集合 VR={(v1,v2),(v1,v4),(v1,v3),(v3,v4)}，图 2 中有向图的集合 VR={<v1,v2>,<v1,v3>,<v3,v4>,<v4,v1>}。
路径和回路

* 无论是无向图还是有向图，从一个顶点到另一顶点途径的所有顶点组成的序列（包含这两个顶点），称为一条路径。如果路径中第一个顶点和最后一个顶点相同，则此路径称为"回路"（或"环"）。

* 并且，若路径中各顶点都不重复，此路径又被称为"简单路径"；同样，若回路中的顶点互不重复，此回路被称为"简单回路"（或简单环）。

* 在有向图中，每条路径或回路都是有方向的。
* 权和网的含义
> 在某些实际场景中，图中的每条边（或弧）会赋予一个实数来表示一定的含义，这种与边（或弧）相匹配的实数被称为"权"，而带权的图通常称为网。如图 3 所示，就是一个网结构：

* 无向图中，如果任意两个顶点之间都能够连通，则称此无向图为连通图。
* 若无向图不是连通图，但图中存储某个子图符合连通图的性质，则称该子图为连通分量。
* 由图中部分顶点和边构成的图为该图的一个子图，但这里的子图指的是图中"最大"的连通子图（也称"极大连通子图"）。

DFS:
```python
DFS_SEARCHED = set()


def dfs(graph, start):
    if start not in DFS_SEARCHED:
        print(start)
        DFS_SEARCHED.add(start)
    for node in graph[start]:
        if node not in DFS_SEARCHED:
            dfs(graph, node)


print('dfs:')
dfs(GRAPH, 'A')  # A B C I D G F E H
```



BFS:
```python
from collections import deque


GRAPH = {
    'A': ['B', 'F'],
    'B': ['C', 'I', 'G'],
    'C': ['B', 'I', 'D'],
    'D': ['C', 'I', 'G', 'H', 'E'],
    'E': ['D', 'H', 'F'],
    'F': ['A', 'G', 'E'],
    'G': ['B', 'F', 'H', 'D'],
    'H': ['G', 'D', 'E'],
    'I': ['B', 'C', 'D'],
}


class Queue(object):
    def __init__(self):
        self._deque = deque()

    def push(self, value):
        return self._deque.append(value)

    def pop(self):
        return self._deque.popleft()

    def __len__(self):
        return len(self._deque)


def bfs(graph, start):
    search_queue = Queue()
    search_queue.push(start)
    searched = set()
    while search_queue:   # 队列不为空就继续
        cur_node = search_queue.pop()
        if cur_node not in searched:
            yield cur_node
            searched.add(cur_node)
            for node in graph[cur_node]:
                search_queue.push(node)

print('bfs:')
bfs(GRAPH, 'A'
```





























