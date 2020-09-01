---
title: BeginningOf2020 - Algorithm
author: Teddy
date: 2020-01-20 10:00:00 +0800
categories: [实践, 算法训练]
tags: [BeginningOf2020, Algorithm]
---


```python
# [47] 全排列 II
#

# @lc code=start
class Solution(object):
    def permuteUnique(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """

        def do_swap(l, start, end):
            for i in range(start, end):
                if l[end] == l[i]:
                    return False
            return True


        def backtrack(start=0):
            if start == n:
                result.append(nums[:])
            for i in range(start, n):
                # if i > 0 and nums[i] == nums[i - 1] and pre[i] == 0:
                #     continue
                if do_swap(nums, start, i):
                    nums[i], nums[start] = nums[start], nums[i]
                    backtrack(start + 1)
                    nums[i], nums[start] = nums[start], nums[i]

        nums.sort()
        n = len(nums)
        result = []
        backtrack()
        return result
```

---

```python
# [1] 两数之和
#

# @lc code=start
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """


# Golang
# func twoSum(nums []int, target int) []int {
# 	tmp_map := make(map [int]int)
# 	for i, n := range nums {
# 		t := target - n
# 		if resultI, ok := tmp_map[t]; ok {
# 			return []int{i, resultI}
# 		}
# 		tmp_map[n] = i
# 	}
#     return []int{0, 0}
# }
```

---

```python
# [2] 两数相加
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    r = None
    
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        result = ListNode(0)
        Solution.r = result

        while True:

            if l1 and l2:
                t_sum = l1.val + l2.val

                l1 = l1.next
                l2 = l2.next
            elif not l1 and l2:
                t_sum = l2.val
                l2 = l2.next
            elif not l2 and l1:
                t_sum = l1.val
                l1 = l1.next
            else:
                t_sum = 0

            Solution.r.next = ListNode(0)

            if Solution.r.val != 0:
                t_sum = t_sum + Solution.r.val

            if t_sum >= 10:
                t_sum = t_sum - 10
                Solution.r.next.val = 1
            else:
                Solution.r.next.val = 0

            Solution.r.val = t_sum



            if not l1 and not l2:
                if Solution.r.next.val == 0:
                    Solution.r.next = None
                break

            Solution.r = Solution.r.next


        print result

        return result

```

---

```python
# [4] 寻找两个有序数组的中位数
#

# @lc code=start
class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        p = 0
        if nums1:
            for n2 in nums2:
                n = p
                m = len(nums1) - 1
                while True:
                    i = int((m - n) / 2) + n
                    if n == m:
                        if n2 > nums1[n]:
                            p = n + 1
                            break
                        else:
                            p = n
                            break
                    if n == m - 1:
                        if nums1[n] <= n2 <= nums1[m]:
                            p = n + 1
                            break
                        elif n2 < nums1[n]:
                            p = n
                            break
                        elif n2 > nums1[m]:
                            p = m + 1
                            break
                        else:
                            break
                    if n2 == nums1[i]:
                        p = i
                        break
                    elif n2 < nums1[i]:
                        m = i
                    else:
                        n = i
                nums1.insert(p, n2)
        else:
            nums1 = nums2
        if len(nums1) % 2 > 0:
            return nums1[int(len(nums1) - 1) / 2]
        else:
            return float((nums1[int(len(nums1) /2)] + (nums1[int(len(nums1) /2 - 1)])) / 2.0)

    # TODO need to do another alternative
```

---

```python
# [5] 最长回文子串
#

# @lc code=start
class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
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





        # last_i = len(s) -1
        # result = ""
        # for i in range(len(s)):
        #     if s[i] == s[last_i]
        #         last_i = last_i - 1
        #         result += s[i]
        #     else:
        #         if s[i + 1] == s[last_i]:
        #             continue
        #         elif s[i] == s[last_i -1]:
        #             last_i = last_i -1
        #         else:
        #             last_i = last_i -1

        # reutrn result

```

---

```python
# [8] 字符串转换整数 (atoi)
#

# @lc code=star
class Solution(object):
    def myAtoi(self, string):
        """
        :type str: str
        :rtype: int
        """
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
```

---

```python
# [13] 罗马数字转整数
#

# @lc code=start
class Solution(object):
    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """
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

---

```python
# [15] 三数之和
#

# @lc code=start
class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        # Anylize
        # 1. use set
        # 2. minimize the time
        # result = set()
        # result_dict = {}
        # for a in nums:
        #     result_dict.update({[a]: a})
        # for b in nums:
        #     for i in result_dict.iterkeys():
        #         result_dict[i] += b
        #         i.append(b)
        # for c in nums:
        #     for i in result_dict.iterkeys():
        #         result_dict[i] += c
        #         i.append(c)
        # print result_dict
        # for k, v in result_dict.iteritems():
        #     if v == 0:
        #         result.add(tuple(k))

        # return result


        # sort and 2 points

        result = []
        nums.sort()
        k = 0
        while nums and len(nums) > 2 and nums[k] <= 0 and k < len(nums) -1:
            if nums[k] > 0: break
            if k != 0 and nums[k] == nums[k-1]: k+=1; continue
            i = k + 1
            j = len(nums) -1
            while i < j:
                s = nums[i] + nums[k] + nums[j]
                if s < 0:
                    i += 1
                    while i <j and nums[i] == nums[i - 1]: i += 1
                elif s > 0:
                    j -= 1
                    while i < j and nums[j] == nums[j + 1]: j -= 1
                else:
                    t = [nums[i], nums[k], nums[j]]
                    result.append(t)
                    i += 1
                    j -= 1
                    while i < j and nums[i] == nums[i - 1]: i += 1
                    while i < j and nums[j] == nums[j + 1]: j -= 1
            k += 1

        return result
```

---

```python
# [20] 有效的括号
#

# @lc code=start
class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        # 1. from 0 to n > and find it's pair X
        # 1. L, R
        # 2. 1,2,3 reverse 3,2,1

        stack = []
        q_dict = {
            "(": (1, "L"),
            ")": (1, "R"),
            "[": (2, "L"),
            "]": (2, "R"),
            "{": (3, "L"),
            "}": (3, "R")
        }
        for v in s:
            if q_dict[v][1] == "R":
                if not stack:
                    return False
                else:
                    if q_dict[v][0] == stack[-1:][0][0]:
                        stack.pop(len(stack) - 1)
                    else:
                        return False
            else:
                stack.append(q_dict[v])
        if not stack:
            return True
        return False
```

---

```python
# [21] 合并两个有序链表
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def mergeTwoLists(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """

        # recontect len n m
        # method1 : read all and sort  time- fuckedup
        # method2 : sort insert into long

        # 1. l1 between l2
        # 2. l1 head of l2
        # 3. l1 tail of l2

        # l1 ---------
        # l2    ------

        if not l1 and not l2:
            return None
        elif not l1 and l2:
            return l2
        elif l1 and not l2:
            return l1
        else:
            pass

        if l1.val < l2.val:
            head = l1
            tail = l2
        else:
            head = l2
            tail = l1
        result = head
        while head:
            if not head or not tail:
                break
            if not head.next and tail:
                head.next = tail
                break
            while head.next.val >= tail.val:
                tmp = ListNode(tail.val)
                tmp.next = head.next
                head.next = tmp
                tail = tail.next
                if not tail and head:
                    break
            head = head.next
        return result

```

---

```python
# [23] 合并K个排序链表
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def mergeKLists(self, lists):
        """
        :type lists: List[ListNode]
        :rtype: ListNode
        """
        if not lists:
            return None
        l_merge = []
        for l in lists:
            if l:
                l_merge.append((l.val, l))
        if not l_merge:
            return None
        l_merge = sorted(l_merge, key=lambda k: k[0])
        print l_merge
        while len(l_merge) > 1:
            i = 0
            new_l_merge = []
            while i < len(l_merge) / 2:
                new_l = self.mergeTwoLists(l_merge[i][1], l_merge[len(l_merge) - 1 -i][1])
                l_merge.pop(i)
                l_merge.pop(len(l_merge) - 1 -i)
                new_l_merge.append((new_l.val, new_l))
            if l_merge:
                new_l_merge.extend(l_merge)
            l_merge = new_l_merge
        return l_merge[0][1]


    def mergeTwoLists(self, l1, l2):
        if not l1 and not l2:
            return None
        elif not l1 and l2:
            return l2
        elif l1 and not l2:
            return l1
        else:
            pass

        if l1.val < l2.val:
            head = l1
            tail = l2
        else:
            head = l2
            tail = l1
        result = head
        while head:
            if not head or not tail:
                break
            if not head.next and tail:
                head.next = tail
                break
            while head.next.val >= tail.val:
                tmp = ListNode(tail.val)
                tmp.next = head.next
                head.next = tmp
                tail = tail.next
                if not tail and head:
                    break
            head = head.next
        return result
```

---

```python
# [24] 两两交换链表中的节点
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def swapPairs(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        # recursive
        #
        #
        #
        if head == None or head.next == None:
            return head
        read_p = ListNode(0)
        read_p = head.next
        head.next = self.swapPairs(read_p.next)
        read_p.next = head
        return read_p
```

---

```python
# [25] K 个一组翻转链表
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def reverseKGroup(self, head, k):
        """
        :type head: ListNode
        :type k: int
        :rtype: ListNode
        """

        if k == 0:
            return head
        if head == None or head.next == None:
            return head
        stack = []
        first = None
        last = None
        while True:
            if not head and len(stack) < k:
                if not first:
                    return stack[0]
                last.next = stack[0]
                return first
            if len(stack) == k:
                i = k - 1
                while i > 0:
                    stack[i].next = stack[i - 1]
                    if i -1 == 0: stack[i -1].next = None
                    i -= 1
                if not last and not first:
                    first = stack[k - 1]
                else:
                    last.next = stack[k - 1]
                last = stack[0]
                stack = []
            if not head and not stack:
                return first
            stack.append(head)
            head = head.next
```

---

```python
# [26] 删除排序数组中的重复项
#

# @lc code=start
class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # 
        if not nums: return 0
        if len(nums) == 1: return 1
        i , c = 0, 0
        while i < len(nums) - 1:
            i += 1
            if nums[i] != nums[c]:
                if nums[c] == nums[c -1]:
                    nums[c:i + 1] = [nums[i] for _ in range(c, i + 1)]
                c += 1
            else:
                if nums[c] != nums[c -1]:
                    c = i
        if c == len(nums) - 1 and nums[c -1] != nums[len(nums) - 1]:
            return len(nums)
        if c == 0:
            return 1
        return c


        # Double pointer

        # @Time complexity: O(n)
        # @Space complexity: O(1)

```

---

```python
# [28] 实现 strStr()
#

# @lc code=start
class Solution(object):
    def strStr(self, haystack, needle):
        """
        :type haystack: str
        :type needle: str
        :rtype: int
        """
        if not needle:
            return 0
        i, c = 0, -1
        while i < len(haystack):
            if haystack[i] == needle[0] and c == -1:
                c = i
                continue
            if c != -1:
                if len(needle) > len(haystack) - c:
                    c = -1
                    break
                if i - c == len(needle):
                    break
                if haystack[i] != needle[i-c]:
                    i = c
                    c = -1
            i += 1
        return c
```

---

```python
# [33] 搜索旋转排序数组
#

# @lc code=start
class Solution(object):
    def search(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        # time complexity logN  

        # length = len(nums)
        # if target > nums[0]:
        #     i, j = 0, length / 4
        #     while j < length:
        #         if target == nums[j]:
        #             return j
        #         elif target < nums[j]:
        #             if j == i + 1 or i == j + 1:
        #                 return -1
        #             i = j
        #             j = j / 2                       
        #         else:
        #             if j == i + 1 or i == j + 1:
        #                 return -1
        #             i = j
        #             j = (length - 1 - j) / 2 + j
        # elif target < nums[length - 1]:
        #     i, j = 0, 3* length / 4
        #     while j < length:
        #         if target == nums[j]:
        #             return j
        #         elif target < nums[j]:
        #             if j == i + 1 or i == j + 1:
        #                 return -1
        #             i = j
        #             j = j / 2                       
        #         else:
        #             if j == i + 1 or i == j + 1:
        #                 return -1
        #             i = j
        #             j = (length - 1 - j) / 2 + j

        # elif target == nums[length - 1]:
        #     return length - 1
        # elif target == nums[0]:
        #     return 0
        # else:
        #     return -1


        length = len(nums)
        if not nums:
            return -1
        elif target == nums[length - 1]:
            return length - 1
        elif target == nums[0]:
            return 0
        elif nums[length - 1] < nums[0] and nums[length - 1] < target < nums[0]:
            return -1
        else:
            pass

        i, j = 0, length -1
        while i <= j:
            m = i + (j - i) / 2

            mt= target
            mV= "M %s" % nums[m]
            mI= "I %s" % nums[i]
            mJ= "J %s" % nums[j]

            if target == nums[m]:
                return m
            elif target == nums[i]:
                return i
            elif target == nums[j]:
                return j
            elif i == j:
                return -1

            if nums[length - 1] > nums[0]:
                # not rotated
                if target < nums[m]:
                    j = m -1
                else:
                    i = m + 1
            else:
                # rotated
                if nums[m] > nums[length -1]:
                    # middle in the left side
                    if target < nums[m] and target < nums[0]:
                        i = m + 1
                    elif target < nums[m] and target > nums[0]:
                        j = m - 1
                    elif target > nums[m]:
                        i = m + 1
                    else:
                        return -1
                elif nums[m] < nums[length -1]:
                    # middle in the right side
                    # or nums are not rotated
                    if target < nums[m]:
                        j = m - 1
                    elif target > nums[m] and target > nums[0]:
                        j = m - 1
                    elif target > nums[m] and target < nums[0]:
                        i = m + 1
                    else:
                        return -1

        return -1
```

---

```python
# [46] 全排列
#

# @lc code=start
class Solution(object):
    def permute(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """

        def backtrack(first=0):
            if first == n:
                result.append(nums[:])
            for i in range(first, n):
                nums[first], nums[i] = nums[i], nums[first]
                backtrack(first + 1)
                nums[first], nums[i] = nums[i], nums[first]
            
        n = len(nums)
        result = []
        backtrack()
        return result
```

---

```python
# [47] 全排列 II
#

# @lc code=start
class Solution(object):
    def permuteUnique(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """

        def do_swap(l, start, end):
            for i in range(start, end):
                if l[end] == l[i]:
                    return False
            return True


        def backtrack(start=0):
            if start == n:
                result.append(nums[:])
            for i in range(start, n):
                # if i > 0 and nums[i] == nums[i - 1] and pre[i] == 0:
                #     continue
                if do_swap(nums, start, i):
                    nums[i], nums[start] = nums[start], nums[i]
                    backtrack(start + 1)
                    nums[i], nums[start] = nums[start], nums[i]

        nums.sort()
        n = len(nums)
        result = []
        backtrack()
        return result

        

    
        # def backtrack(start=0):
        #     if start == n:
        #         # if nums not in result:
        #         result.append(nums[:])
        #     for i in range(start, n):
        #         if i + 1 < n and nums[i] == nums[i + 1]:
        #             continue
        #         if i==start and pre.get(i) and nums[:start] in pre.get(i):
        #             continue
        #         nums[i], nums[start] = nums[start], nums[i]
        #         if start ==i:
        #             if not pre.get(i):
        #                 pre[i] = [nums[:start]]
        #             else:
        #                 pre[i].append(nums[:start])
        #         backtrack(start + 1)
        #         nums[i], nums[start] = nums[start], nums[i]

        # pre = {}
        # n = len(nums)
        # result = []
        # backtrack()
        # return result


    # Python 3 time complexity great
    # class Solution:
    # def permuteUnique(self, nums: List[int]) -> List[List[int]]:
    #     nums.sort()
    #     self.res = []
    #     check = [0 for i in range(len(nums))]
        
    #     self.backtrack([], nums, check)
    #     return self.res
        
    # def backtrack(self, sol, nums, check):
    #     if len(sol) == len(nums):
    #         self.res.append(sol)
    #         return
        
    #     for i in range(len(nums)):
    #         if check[i] == 1:
    #             continue
    #         if i > 0 and nums[i] == nums[i-1] and check[i-1] == 0:
    #             continue
    #         check[i] = 1
    #         self.backtrack(sol+[nums[i]], nums, check)
    #         check[i] = 0

    # def permuteUnique(self, nums):
    #     nums.sort()
    #     self.res = []
    #     check = [0 for _ in range(len(nums))]

    #     self.backtrack([], nums, check)
    #     return self.res

    # def backtrack(self, sol, nums, check):
    #     if len(sol) == len(nums):
    #         self.res.append(sol)
    #         return

    #     for i in range(len(nums)):
    #         if check[i] == 1:
    ##             continue
    #         if i > 0 and nums[i] == nums[i - 1] and check[i - 1] == 0:
    #             continue
    #         check[i] = 1
    #         self.backtrack(sol + [nums[i]], nums, check)
    #         check[i] = 0
```

---

```python
# TODO - mark fix
# [672] 灯泡开关 Ⅱ
#

# @lc code=start
class Solution(object):
    def flipLights(self, n, m):
        """
        :type n: int
        :type m: int
        :rtype: int
        """
        lights = [1 for i in range(n)]
        result = []

        p = []

        for m1 in range(m + 1):
            m234 = m - m1
            for m2 in range(m234 +1):
                m34 = m234 - m2
                for m3 in range(m34 +1):
                    m4 = m34 - m3
                    if m1 % 2 > 0:
                        lights = [0 for i in range(n)]
                    if m2 % 2 > 0:
                        for i in range(0, n):
                            if (i+1) % 2 == 0:
                                if lights[i] == 0:
                                    lights[i] = 1
                                else:
                                    lights[i] = 0
                    if m3 % 2 > 0:
                        for i in range(0, n):
                            if (i + 1) % 2 == 1:
                                if lights[i] == 0:
                                    lights[i] = 1
                                else:
                                    lights[i] = 0
                    if m4 % 2 > 0:
                        if n == 0:
                            continue
                        elif n in [1, 2, 3]:
                            if lights[0] == 0:
                                lights[0] = 1
                            else:
                                lights[0] = 0
                        else:
                            for k in range(int((n - 1)/ 3) + 1):
                                if lights[3 *k] == 0:
                                    lights[3 * k] = 1
                                else:
                                    lights[3 * k] = 0
                    r_l = ",".join([str(a) for a in lights])
                    print m1, m2, m3, m4
                    p.append([m1, m2, m3, m4])
                    print "LIGHTS: %s" % lights
                    result.append(r_l)
                    lights = [1 for i in range(n)]

        print len(result)
        result = set(result)
        print len(result)

        print "P %s" % len(p)

        print result

        return len(result)
```

---

```python

```