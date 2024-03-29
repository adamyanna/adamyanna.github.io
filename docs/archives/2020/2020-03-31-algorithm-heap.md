---
title: Algorithm-heap 堆排序的实现
layout: default
parent: 2020
grand_parent: Archives
---

**Algorithm**
{: .label .label-blue }

**Heap**
{: .label .label-green }

**2020-03-29 10:00:00 +0800**
{: .label .label-yellow }



# algorithm-heap 堆排序的实现

## 合并2个有序序列，合并n个有序序列 
### 相关算法回顾
##### 合并2个有序链表为一个有序链表
* 比对l1和l2的大小，将最小的放在新链表的next上，更新l1或者l2，直到其中一个链表为空 while l1 and l2；最终返回新链表的next。T = M + N

##### 合并n个有序链表为一个有序链表
* 基于两个链表合并的算法，我们将k中每两个链表合并一次得出的新的集合再进行同样的操作，最终得到一个集合，T = kN 将 k 个链表配对并将同一对中的链表合并。第一轮合并以后， k 个链表被合并成了 k/2 个链表，平均长度为 2N/k 重复这一过程，直到我们得到了最终的有序链表。每次k的数目指数型下降，例如k k/2 k/4 k/8 S = Nlogk


## 简单暴力
##### n个长度都为m的有序数组，合并为一个有序数组
* 拼接所有数组，组成长度为m x n的新数组，对数组做时间复杂度为mnlogmn的排序算法
	* 快速排序 （基准数选择很大程度决定最终的时间复杂度，三数取中法，平均时间复杂度的计算方式需要带入“主定理”求解，详细可以回顾 [“我的算法训练学习曲线”](https://teddygoodman.github.io/2020/03/02/Algorithm-curve/)
	* 归并 （先分后治）
	* 堆排序，涉及堆的生成（大顶堆，小顶堆）


###### 归并的思想 divide-and-conquer
* 先分后治，分而治之，将一个目标问题分解为多个子问题，对各个子问题求解，最终合并子问题的结果就是分治的思想；
* 归并排序
	* 分：先将长度位n的序列，经过logn次“分”，分为n个单独的元素
	* 治：每两个相邻元素进行排序，一次结果的时间复杂度位O(n)，递归进行新的子问题或者说子序列的合并，i j双指针比较，每次将较小的更新到结果中，所有新的子问题的合并时间复杂度还是O(n)
	* 最终经过logn次平均时间复杂度为O(n)的运算，返回结果；
	* 归并的时间复杂度为O(nlogn)，而且不会出现和快速排序相似的基准数选取影响排序效率的问题；

* 在已经完成排序的k个长度为n的子序列的合并中，就是半个归并排序，只需要对已经完成排序的子问题做递归的治理就可以；
	* k个n长度的子问题，每次两两合并的总的时间复杂度为O(nk)
	* k个最终两两合并为1个，那么子问题到结果的治理过程经历了logk次
	* 那么此问题的最优解就是O(nklogk)


###### 堆排序的思想

* 堆排序是利用堆这种数据结构而设计的一种排序算法，属于一种选择排序，最坏，最好，平均时间复杂度均为O(nlogn)，属于不稳定排序；

* 堆
	* 一个完全二叉树
	
	* 大顶堆：每个结点的值都大于或者等于左右孩子结点的值

	* 小顶堆：每个结点的值都小于或者等于左右孩子节点的值
	
	  | 0    | 1    | 2    | 3    | 4    | 5    | 6    |
	  | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
	  | 50   | 40   | 30   | 30   | 35   | 20   | 25   |
	
	* 大顶堆 **arr[i] >= arr[2i+1] && arr[i] >= arr[2i+2]**
	* 小顶堆 **arr[i] <= arr[2i+1] && arr[i] <= arr[2i+2]**

* 堆排序的基本思想
  * 将待排序序列构造成一个大顶堆，整个序列的最大值就在堆顶的根节点
  * 将根节点元素和序列末尾元素交换，末尾就是待排序序列的最大值
  * 将剩余的n-1个元素构造成新的堆
  * 重复以上步骤，知道无元素在进行堆的构造
* 构造堆的过程
  1. 从最后一个非叶子结点开始，与其左右孩子进行调整，先左右，再上下，此处三个节点中权值最大的结点被升到第一个非叶子结点的位置；
  2. 按顺序找到第二个非叶子结点，重复第一步
  3. 按顺序找完所有的非叶子结点，则第一次构造完成；
* 构造完成后，将根节点和最后一个叶子结点交换，再对剩下的元素进行构造；
* 时间复杂度分析：
  * 初始化建堆的过程需要消耗的时间
    * O(n)l
      * 对于这个堆来说，每一个非叶子结点都需要，和它自己的左右孩子比较，如果发现小于孩子，将发生交换，如何没有就直接不再继续执行这个结点的调整；
      * 发生一次交换后，还会继续往剩下的子树进行交换；
      * 假设树的高度为k
      * 那么第i层的时间复杂度为：**2^( i -1 ) * (k -i)**，表示层有2^i-1个结点，每个结点向下比较最差的情况下需要执行k-1次；
      * 那么总时间就是 **2^( k -2 ) * 1 + 2^( k -3 ) * 2 + 2^( k - 4 ) * 3 + ... + 2 - (k -1) ** 叶子节点不进行交换；
      * 根据等差数列，最终结果为 **2^k - k - 1**， *又因为k为完全二叉树的深度，所以 (2^k) <=  n < (2^k  -1 )* ，所以 **log(n+1) < k <= logn** 
      * 最终的时间复杂度为 **n-logn -1**，所以建立堆的时间复杂度为O(n)
  * 每次交换首位元素后，对堆的重新整理的时间复杂度为 logn，共整理了n-1次，所以整理和交换的时间复杂度为 
    * **O(nlogn)**
  * 所以最终该算法的最差和平均时间复杂度都为**O(nlogn)**



```c
#include <stdio.h>

// make heap
// 原地算法
void _heapAdjust(int *array, int i, int len) {
	// 从最后一个非子叶子结点向前
	// 2*i+1 2*i+2 为元素i的左右孩子
	int tmp = array[i];
	for (int k=2*i+1 ; k < len; k=2*k+1) // 从第一个元素i的左孩子开始，每次更新
	{
		
		if (array[k] < array[k+1] && k+1<len) { // 右边子节点更大,则将k更新的右边
			k ++;
		}

		if (tmp < array[k])
		{
			array[i] = array[k];		// 将最大值更新到i
			i = k;						// 将下次更新的坐标更新为k
		}else{
			break;
		}
	}
	array[i] = tmp;		//将最终值放在最新的i处
}

int main() {
	int len = 9;
	int array[] = {5, 6, 3, 7, 8, 9, 1, 2, 4};
	for (int i = len/2 - 1; i >= 0; i--)
	{
		_heapAdjust(array, i, len);
	}

	for (int i = 0; i < 9; ++i)
	{
		printf("%d, ", *(array+i));
	}
	printf("\n");

	for (int j = len -1; j > 0; j--)
	{
		// printf("%d\n", j);

		int t = array[0];
		array[0] = array[j];
		array[j] = t;

		// for (int i = 0; i < 9; ++i)
		// {
		// 	printf("%d, ", *(array+i));
		// }
		// printf("\n");
		_heapAdjust(array, 0, j);
	}

	for (int i = 0; i < 9; ++i)
	{
		printf("%d, ", *(array+i));
	}
	return 0;
}
```



















