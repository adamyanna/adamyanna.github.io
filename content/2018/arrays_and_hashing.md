# Arrays & Hashing

> 2018

Arrays & Hashing

Übung macht den Meister

Roadmap

1. Contains Duplicate

Given an integer array nums, return true if any value appears at least twice in the array

using hash

Python

class Solution:
def containsDuplicate(self, nums: list[int]) -> bool:
hashset = set()

for n in nums:
if n in hashset:
return True
hashset.add(n)
return False

if __name__ == '__main__':
result = Solution().containsDuplicate([1,2,3,4,555,6,222,89,689435,12498,96783,123488,9098,6])
print("=> %s" % result)
Golang

without using hash

Python

# 1. loop initial nums and save value to another list
# 2. use binary search to find the same value
# 3. if has same value return true
# 4. if not just insert to binary search result index, between i & j
# 5. looping until last value, return False when finish all
# this is sorting problem, time => Nlogn
Golang

2. Two Sum

Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

Python

Golang

3.

{desc}

Python

Golang
