# Beginning of 2020 -- Algorithm

**2020-01-08**

## Overview

This post collects my LeetCode algorithm practice from the start of 2020. The solutions are written in Python (with one Golang reference for comparison). Most problems are solved and working; a few are noted as partial or incomplete. The set covers backtracking, linked list manipulation, binary search, two-pointer techniques, string parsing, and stack-based validation. Each problem below includes a description, the approach taken, complexity analysis, and the full solution code.

---

## 1. Two Sum (#1)

**Problem:** Given an array of integers and a target, return the indices of the two numbers that add up to the target.

**Approach:** Hash map for O(n) single-pass lookup. Store each number's index in a dictionary; for each element, check if `target - num` already exists.

**Complexity:** Time O(n), Space O(n).

```python
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        seen = {}
        for i, n in enumerate(nums):
            complement = target - n
            if complement in seen:
                return [seen[complement], i]
            seen[n] = i
```

**Golang comparison** (same hash-map approach, included for reference):

```go
func twoSum(nums []int, target int) []int {
    tmp_map := make(map[int]int)
    for i, n := range nums {
        t := target - n
        if resultI, ok := tmp_map[t]; ok {
            return []int{i, resultI}
        }
        tmp_map[n] = i
    }
    return []int{0, 0}
}
```

---

## 2. Add Two Numbers (#2)

**Problem:** Two non-empty linked lists represent digits of two numbers in reverse order. Sum them and return the result as a linked list.

**Approach:** Iterate through both lists simultaneously, summing digits with a carry. When one list is exhausted, continue with the remaining list. The carry is stored in the next node's initial value (`Solution.r.next.val`), which is added to the next digit sum before deciding whether to carry again.

**Complexity:** Time O(max(n, m)), Space O(max(n, m)).

```python
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

        return result
```

---

## 3. Median of Two Sorted Arrays (#4) -- Partial

**Problem:** Find the median of two sorted arrays. The overall run time complexity target is O(log(m + n)).

**Approach:** This solution inserts elements of `nums2` into `nums1` using a binary-search-like scan to find the correct insertion index, then computes the median from the merged list. **Note: this is a partial solution.** The insertion-based approach runs in O(n * m) worst case and does not meet the O(log(m + n)) requirement. The code is kept as a record of the initial attempt. A proper O(log(m + n)) binary-partition solution remains TODO (see the inline comment).

**Complexity (this attempt):** Time O(n * m), Space O(1) in-place aside from the merged list.

```python
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
            return nums1[(len(nums1) - 1) // 2]
        else:
            mid = len(nums1) // 2
            return float((nums1[mid] + nums1[mid - 1]) / 2.0)

    # TODO: need to implement the O(log(m+n)) binary partition approach
```

---

## 4. Longest Palindromic Substring (#5)

**Problem:** Given a string `s`, return the longest palindromic substring.

**Approach:** Expand around centers. For each character, check two cases: odd-length palindrome (centered at one character) and even-length palindrome (centered between two identical adjacent characters). Track the longest result in a dictionary keyed by length.

**Complexity:** Time O(n^2), Space O(1) aside from result storage.

```python
class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        result = {}

        for i in range(len(s)):
            r = ""
            k = 0
            j = 0
            if i + 1 >= len(s):
                continue
            # Even-length palindrome
            if s[i] == s[i + 1]:
                j = i
                k = i + 1
                while j >= 0 and k < len(s) and s[j] == s[k]:
                    r = s[j] + r
                    r += s[k]
                    j -= 1
                    k += 1
            if r:
                result.update({len(r): r})
            # Odd-length palindrome
            if i - 1 >= 0 and i + 1 < len(s) and s[i - 1] == s[i + 1]:
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

        if result:
            return result[max(result.keys())]
        elif s:
            return s[0]
        else:
            return ""
```

---

## 5. String to Integer / atoi (#8)

**Problem:** Implement the `atoi` function: parse a string into a 32-bit signed integer, handling leading whitespace, optional sign, and digit extraction. Clamp overflow to INT_MIN/INT_MAX.

**Approach:** Strip whitespace, then iterate character by character collecting an optional sign followed by digits. Stop at the first non-digit character. Clamp the result to the 32-bit signed integer range.

**Complexity:** Time O(n), Space O(1).

```python
class Solution(object):
    def myAtoi(self, string):
        """
        :type str: str
        :rtype: int
        """
        string = string.strip()
        if not string:
            return 0
        digits = [str(i) for i in range(10)]
        operators = ["-", "+"]
        result = ""
        for v in string:
            if v in operators and not result:
                result += v
            elif v in digits:
                result += v
            elif not result:
                return 0
            else:
                break
        if result == "+" or result == "-":
            return 0
        val = int(result)
        if not (-2**31 <= val <= 2**31 - 1):
            if val < 0:
                return -2**31
            else:
                return 2**31 - 1
        return val
```

---

## 6. Roman to Integer (#13)

**Problem:** Convert a Roman numeral string to an integer. Input is guaranteed to be in the range 1 to 3999.

**Approach:** Map each Roman character to its value. Iterate left to right, checking for subtractive notation (e.g., IV, IX, XL, XC, CD, CM). When a subtractive pair is detected, subtract the left value from the right and remove the left value from the accumulated result.

**Complexity:** Time O(n), Space O(1).

```python
class Solution(object):
    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """
        result = []
        r_d = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000,
        }
        for i in s:
            m = 0
            if i in ["V", "X"] and result and result[-1] == 1:
                m = 1
            elif i in ["L", "C"] and result and result[-1] == 10:
                m = 10
            elif i in ["D", "M"] and result and result[-1] == 100:
                m = 100
            if m != 0:
                result = result[:-1]
            v = r_d[i] - m
            result.append(v)
        return sum(result)
```

---

## 7. 3Sum (#15)

**Problem:** Find all unique triplets in an array that sum to zero.

**Approach:** Sort the array, then fix one element and use two pointers to find complementary pairs. Skip duplicate values at each step to avoid redundant triplets.

**Complexity:** Time O(n^2), Space O(1) (excluding output).

```python
class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        result = []
        nums.sort()
        k = 0
        while nums and len(nums) > 2 and nums[k] <= 0 and k < len(nums) - 1:
            if nums[k] > 0:
                break
            if k != 0 and nums[k] == nums[k - 1]:
                k += 1
                continue
            i = k + 1
            j = len(nums) - 1
            while i < j:
                s = nums[i] + nums[k] + nums[j]
                if s < 0:
                    i += 1
                    while i < j and nums[i] == nums[i - 1]:
                        i += 1
                elif s > 0:
                    j -= 1
                    while i < j and nums[j] == nums[j + 1]:
                        j -= 1
                else:
                    result.append([nums[i], nums[k], nums[j]])
                    i += 1
                    j -= 1
                    while i < j and nums[i] == nums[i - 1]:
                        i += 1
                    while i < j and nums[j] == nums[j + 1]:
                        j -= 1
            k += 1
        return result
```

---

## 8. Valid Parentheses (#20)

**Problem:** Determine if a string of brackets `()`, `[]`, `{}` is valid (properly nested and closed).

**Approach:** Use a stack. Push left brackets; on encountering a right bracket, check that the top of the stack contains the matching left bracket. The approach encodes bracket types as integers (1, 2, 3) and direction as L/R.

**Complexity:** Time O(n), Space O(n).

```python
class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        stack = []
        q_dict = {
            "(": (1, "L"),
            ")": (1, "R"),
            "[": (2, "L"),
            "]": (2, "R"),
            "{": (3, "L"),
            "}": (3, "R"),
        }
        for v in s:
            if q_dict[v][1] == "R":
                if not stack:
                    return False
                else:
                    if q_dict[v][0] == stack[-1][0]:
                        stack.pop()
                    else:
                        return False
            else:
                stack.append(q_dict[v])
        return not stack
```

---

## 9. Merge Two Sorted Lists (#21)

**Problem:** Merge two sorted linked lists into one sorted linked list.

**Approach:** Choose the smaller head as the starting point, then splice nodes from the other list into position by iterating and comparing values. When one list is exhausted, append the remainder.

**Complexity:** Time O(n + m), Space O(1) in-place.

```python
class Solution(object):
    def mergeTwoLists(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        if not l1 and not l2:
            return None
        elif not l1 and l2:
            return l2
        elif l1 and not l2:
            return l1

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
            while head.next and tail and head.next.val >= tail.val:
                tmp = ListNode(tail.val)
                tmp.next = head.next
                head.next = tmp
                tail = tail.next
                if not tail:
                    break
            head = head.next
        return result
```

---

## 10. Merge k Sorted Lists (#23)

**Problem:** Merge k sorted linked lists into one sorted linked list.

**Approach:** Pairwise merging using the `mergeTwoLists` helper. Store list heads as (value, node) tuples sorted by value. Repeatedly merge the smallest and largest in the current batch until one remains.

**Complexity:** Time O(N log k) where N is the total number of nodes, Space O(k) for the working list.

```python
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
        while len(l_merge) > 1:
            i = 0
            new_l_merge = []
            while i < len(l_merge) // 2:
                new_l = self.mergeTwoLists(l_merge[i][1], l_merge[len(l_merge) - 1 - i][1])
                l_merge.pop(i)
                l_merge.pop(len(l_merge) - 1 - i)
                new_l_merge.append((new_l.val, new_l))
            if l_merge:
                new_l_merge.extend(l_merge)
            l_merge = new_l_merge
        return l_merge[0][1]

    def mergeTwoLists(self, l1, l2):
        # same implementation as Problem #21 above
        if not l1 and not l2:
            return None
        elif not l1 and l2:
            return l2
        elif l1 and not l2:
            return l1
        if l1.val < l2.val:
            head, tail = l1, l2
        else:
            head, tail = l2, l1
        result = head
        while head:
            if not head or not tail:
                break
            if not head.next and tail:
                head.next = tail
                break
            while head.next and tail and head.next.val >= tail.val:
                tmp = ListNode(tail.val)
                tmp.next = head.next
                head.next = tmp
                tail = tail.next
                if not tail:
                    break
            head = head.next
        return result
```

---

## 11. Swap Nodes in Pairs (#24)

**Problem:** Given a linked list, swap every two adjacent nodes and return the new head. The actual nodes must be swapped, not just the values.

**Approach:** Recursive approach. Swap the first two nodes, then recursively swap the rest and link the tail.

**Complexity:** Time O(n), Space O(n) recursion stack.

```python
class Solution(object):
    def swapPairs(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        if head is None or head.next is None:
            return head
        read_p = head.next
        head.next = self.swapPairs(read_p.next)
        read_p.next = head
        return read_p
```

---

## 12. Reverse Nodes in k-Group (#25)

**Problem:** Reverse the nodes of a linked list k at a time. If fewer than k nodes remain at the end, leave them as-is. No extra memory allocation (nodes must be re-linked).

**Approach:** Collect k nodes on a stack. Once k nodes are gathered, reverse them by relinking: `stack[i].next = stack[i-1]`. Attach the reversed group to the previous tail and continue. Any remaining group smaller than k is left in original order.

**Complexity:** Time O(n), Space O(k).

```python
class Solution(object):
    def reverseKGroup(self, head, k):
        """
        :type head: ListNode
        :type k: int
        :rtype: ListNode
        """
        if k == 0:
            return head
        if head is None or head.next is None:
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
                    if i - 1 == 0:
                        stack[i - 1].next = None
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

## 13. Remove Duplicates from Sorted Array (#26)

**Problem:** Remove duplicates from a sorted array in-place and return the new length. The relative order of unique elements must be preserved.

**Approach:** Two-pointer technique. A slow pointer `c` marks the boundary of deduplicated elements, a fast pointer `i` scans ahead. When a new distinct value is found, compact the segment.

**Complexity:** Time O(n), Space O(1).

```python
class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return 1
        i, c = 0, 0
        while i < len(nums) - 1:
            i += 1
            if nums[i] != nums[c]:
                if nums[c] == nums[c - 1]:
                    nums[c:i + 1] = [nums[i] for _ in range(c, i + 1)]
                c += 1
            else:
                if nums[c] != nums[c - 1]:
                    c = i
        if c == len(nums) - 1 and nums[c - 1] != nums[-1]:
            return len(nums)
        if c == 0:
            return 1
        return c
```

---

## 14. Implement strStr() (#28)

**Problem:** Return the index of the first occurrence of `needle` in `haystack`, or -1 if `needle` is not found.

**Approach:** Linear scan with a match pointer. When a potential start is found, compare subsequent characters against the needle until a mismatch or full match.

**Complexity:** Time O(n * m), Space O(1).

```python
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
                i += 1
                continue
            if c != -1:
                if len(needle) > len(haystack) - c:
                    c = -1
                    break
                if i - c == len(needle):
                    break
                if haystack[i] != needle[i - c]:
                    i = c
                    c = -1
            i += 1
        return c
```

---

## 15. Search in Rotated Sorted Array (#33)

**Problem:** Search for a target in a rotated sorted array (no duplicates). Return the index or -1. Must run in O(log n) time.

**Approach:** Modified binary search. Determine whether the middle element is in the left (larger) segment or the right (smaller) segment, then narrow the search range based on where the target must lie relative to the pivot.

**Complexity:** Time O(log n), Space O(1).

```python
class Solution(object):
    def search(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        length = len(nums)
        if not nums:
            return -1
        elif target == nums[length - 1]:
            return length - 1
        elif target == nums[0]:
            return 0
        elif nums[length - 1] < nums[0] and nums[length - 1] < target < nums[0]:
            return -1

        i, j = 0, length - 1
        while i <= j:
            m = i + (j - i) // 2
            if target == nums[m]:
                return m
            elif target == nums[i]:
                return i
            elif target == nums[j]:
                return j
            elif i == j:
                return -1

            if nums[length - 1] > nums[0]:
                # Array is not rotated - standard binary search
                if target < nums[m]:
                    j = m - 1
                else:
                    i = m + 1
            else:
                # Array is rotated
                if nums[m] > nums[length - 1]:
                    # Middle is in the left (larger) segment
                    if target < nums[m] and target < nums[0]:
                        i = m + 1
                    elif target < nums[m] and target > nums[0]:
                        j = m - 1
                    elif target > nums[m]:
                        i = m + 1
                elif nums[m] < nums[length - 1]:
                    # Middle is in the right (smaller) segment
                    if target < nums[m]:
                        j = m - 1
                    elif target > nums[m] and target > nums[0]:
                        j = m - 1
                    elif target > nums[m] and target < nums[0]:
                        i = m + 1
        return -1
```

---

## 16. Permutations (#46)

**Problem:** Given a collection of distinct integers, return all possible permutations.

**Approach:** Classic backtracking with in-place swapping. Fix the first position, swap in each remaining element, recursively generate permutations for the suffix, then swap back.

**Complexity:** Time O(n * n!), Space O(n!) for output, O(n) recursion depth.

```python
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

## 17. Permutations II (#47)

**Problem:** Given a collection of integers that may contain duplicates, return all unique permutations.

**Approach:** Backtracking with a pruning helper `do_swap` that checks whether the current element has already been placed at the target index (avoiding duplicate permutations from equal values). The array is sorted first to group duplicates together. An alternative, more standard approach (commented out inline) uses a `check` array to track which indices have been used, combined with a `nums[i] == nums[i-1] and check[i-1] == 0` pruning condition.

**Complexity:** Time O(n * n!), Space O(n!) for output.

```python
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
                if do_swap(nums, start, i):
                    nums[i], nums[start] = nums[start], nums[i]
                    backtrack(start + 1)
                    nums[i], nums[start] = nums[start], nums[i]

        nums.sort()
        n = len(nums)
        result = []
        backtrack()
        return result

    # Alternative approach (Python 3, better time complexity via check array):
    # def permuteUnique(self, nums):
    #     nums.sort()
    #     self.res = []
    #     check = [0 for _ in range(len(nums))]
    #     self.backtrack([], nums, check)
    #     return self.res
    #
    # def backtrack(self, sol, nums, check):
    #     if len(sol) == len(nums):
    #         self.res.append(sol)
    #         return
    #     for i in range(len(nums)):
    #         if check[i] == 1:
    #             continue
    #         if i > 0 and nums[i] == nums[i - 1] and check[i - 1] == 0:
    #             continue
    #         check[i] = 1
    #         self.backtrack(sol + [nums[i]], nums, check)
    #         check[i] = 0
```

---

## 18. Bulb Switcher II (#672) -- Partial / In Progress

**Problem:** There are n bulbs initially on. There are 4 buttons with different toggle patterns. Determine how many distinct configurations are possible after exactly m operations.

**Approach (work in progress):** Enumerate all combinations of operation counts `(m1, m2, m3, m4)` that sum to m, then simulate each combination by applying the corresponding toggle patterns (all, even-index, odd-index, every-3rd). Record the resulting light configuration. **Note: this solution is incomplete and marked TODO-fix.** The enumeration approach is correct in principle but the simulation currently re-derives the light state from scratch for each combination rather than using the mathematical properties that make the answer at most 8.

```python
class Solution(object):
    def flipLights(self, n, m):
        """
        :type n: int
        :type m: int
        :rtype: int
        """
        lights = [1 for _ in range(n)]
        result = []

        for m1 in range(m + 1):
            m234 = m - m1
            for m2 in range(m234 + 1):
                m34 = m234 - m2
                for m3 in range(m34 + 1):
                    m4 = m34 - m3
                    if m1 % 2 > 0:
                        lights = [0 for _ in range(n)]
                    if m2 % 2 > 0:
                        for i in range(n):
                            if (i + 1) % 2 == 0:
                                lights[i] = 1 - lights[i]
                    if m3 % 2 > 0:
                        for i in range(n):
                            if (i + 1) % 2 == 1:
                                lights[i] = 1 - lights[i]
                    if m4 % 2 > 0:
                        if n == 0:
                            continue
                        elif n in [1, 2, 3]:
                            lights[0] = 1 - lights[0]
                        else:
                            for k in range((n - 1) // 3 + 1):
                                lights[3 * k] = 1 - lights[3 * k]
                    r_l = ",".join([str(a) for a in lights])
                    result.append(r_l)
                    lights = [1 for _ in range(n)]

        return len(set(result))
```

---

## Summary

This set covers a broad range of foundational algorithm patterns: hash-map lookups (#1), linked list manipulation (#2, #21, #23, #24, #25), binary search and its rotated-array variant (#33), expand-around-center palindromes (#5), two-pointer triplets (#15), stack-based validation (#20), backtracking with pruning (#46, #47), string parsing (#8, #13, #28), in-place array deduplication (#26), and combinatorial enumeration (#672).

Solutions marked as partial (Median of Two Sorted Arrays #4, Bulb Switcher II #672) are retained as snapshots of the thinking process at the time.
