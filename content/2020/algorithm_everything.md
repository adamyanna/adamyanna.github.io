# Algorithm Everything

> 2020-02-18

A comprehensive algorithm reference covering sorting algorithms, data structures, core techniques, and classic interview problems -- distilled from hands-on LeetCode practice and production system experience.

---

## Project Context

**Role:** Cloud network monitoring system.

**Architecture:** Server-agent distributed model. Each availability zone deploys two bare-metal physical hosts as monitoring agent nodes. Each host runs multiple agent processes to distribute collection load. Agents use a heartbeat-based HA mechanism for fault tolerance.

**Framework:** Server-side uses Python 2 Tornado. At its core, `tornado.ioloop.IOLoop.current().start()` runs the event loop. On Linux, Tornado leverages **epoll** for I/O multiplexing, capable of handling millions of socket handles concurrently.

### epoll vs select/poll

I/O multiplexing allows a single thread to monitor thousands of file descriptors. The critical difference:

| Mechanism | Strategy | Scalability |
|-----------|----------|-------------|
| select/poll | Linear scan of every FD per call | Degrades with FD count |
| epoll | Event-driven callback -- only ready FDs trigger notification | Scales to millions of FDs |

File descriptors vs handles: a pointer holds the raw memory address of the referenced object; a handle is a system-managed reference identifier that the system can relocate to a different memory address. This indirection gives the system control over how the referenced object is accessed.

---

## Sorting Algorithms

### Overview Table

| Algorithm | Best | Average | Worst | Space | Stable | In-Place |
|-----------|------|---------|-------|-------|--------|----------|
| Bubble Sort | O(n) | O(n^2) | O(n^2) | O(1) | Yes | Yes |
| Selection Sort | O(n^2) | O(n^2) | O(n^2) | O(1) | No | Yes |
| Insertion Sort | O(n) | O(n^2) | O(n^2) | O(1) | Yes | Yes |
| Shell Sort | O(n log n) | O(n log n)~O(n^2) | O(n^2) | O(1) | No | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n^2) | O(log n) | No | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No | Yes |
| Counting Sort | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes | No |
| Radix Sort | O(nk) | O(nk) | O(nk) | O(n + k) | Yes | No |
| Binary Tree Sort | O(n log n) | O(n log n) | O(n^2) | O(n) | Yes | No |

**Stable** means equal elements preserve their relative order after sorting. **In-place** means O(1) or O(log n) extra space.

### Simple Quadratic Sorts

**Bubble Sort** repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. After each pass, the largest unsorted element "bubbles" to its correct position. Best case O(n) when the array is already sorted (early termination via a swap flag).

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr
```

**Selection Sort** divides the array into a sorted and unsorted region. It repeatedly selects the smallest element from the unsorted region and swaps it with the leftmost unsorted element. Always O(n^2) regardless of input order because it does not short-circuit.

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

**Insertion Sort** builds the sorted array one element at a time by taking each element and inserting it into its correct position among the already-sorted prefix. Efficient for small arrays (used as fallback in Timsort) and nearly-sorted data. Achieves O(n) best case.

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

**Shell Sort** is a generalization of insertion sort that compares elements separated by a gap. It starts with a large gap and reduces it over multiple passes (using gap sequences like Hibbard or Knuth). As the gap shrinks, the array becomes progressively more sorted, and insertion sort becomes very efficient. Not stable.

### Efficient O(n log n) Sorts

**Quick Sort** picks a pivot element, partitions the array so that elements smaller than the pivot are on the left and larger on the right, then recursively sorts the two partitions. Average O(n log n) with excellent constant factors. Worst case O(n^2) occurs when the pivot is always the min or max (e.g., already sorted array with a poor pivot choice). Randomized pivot selection or median-of-three mitigates this.

```python
def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot = partition(arr, low, high)
        quick_sort(arr, low, pivot - 1)
        quick_sort(arr, pivot + 1, high)
    return arr

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

**Merge Sort** follows the divide-and-conquer paradigm: split the array in half, recursively sort each half, then merge the two sorted halves. Guaranteed O(n log n) regardless of input. Stable. The O(n) extra space for the merge step is the primary trade-off.

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Heap Sort** uses a binary heap data structure. Build a max-heap from the array in O(n), then repeatedly extract the maximum element and place it at the end of the array in O(log n) per extraction. In-place and O(n log n) guaranteed. Not stable because heap operations reorder elements arbitrarily.

```python
import heapq

def heap_sort(arr):
    heapq.heapify(arr)  # Build min-heap in O(n)
    return [heapq.heappop(arr) for _ in range(len(arr))]
```

### Non-Comparison Sorts

**Counting Sort** works by counting the occurrences of each distinct value, then computing cumulative counts to determine positions. O(n + k) time where k is the range of input values. Requires non-negative integers or a known range. Stable.

**Radix Sort** sorts numbers digit by digit, from least significant to most significant, using a stable sub-sort (usually counting sort) for each digit. O(nk) where k is the number of digits. Works well for integers and fixed-length strings.

**Binary Tree Sort** inserts all elements into a binary search tree, then performs an in-order traversal to output values in sorted order. Average O(n log n), but degrades to O(n^2) if the tree becomes unbalanced (e.g., already sorted input).

### Which Sort to Choose?

| Scenario | Recommended Algorithm |
|----------|----------------------|
| General purpose, in-place | Quick Sort |
| Stability required | Merge Sort or Timsort (Python/Java default) |
| Small constant factor, in-place | Heap Sort |
| Nearly sorted data | Insertion Sort |
| Small n (< 50) | Insertion Sort |
| Integer data with limited range | Counting Sort or Radix Sort |
| Linked list sorting | Merge Sort (no extra space needed) |

---

## Search Algorithms

### Binary Search

Finds the position of a target value within a **sorted array** in O(log n) time. Compares the target to the middle element, then discards the half that cannot contain the target.

```python
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

Binary search generalizes to any monotonic predicate: "find the first index where condition X is true." This pattern ("bisection") appears throughout algorithm problems.

---

## Data Structures

Understanding data relationships helps navigate the taxonomy:

| Relationship | Category | Examples |
|-------------|----------|----------|
| 1:1 | Linear | Array, Stack, Queue, Linked List, Hash Table |
| 1:N (hierarchical) | Tree | Binary Tree, BST, N-ary Tree, Heap, Trie |
| N:M (network) | Graph | Directed/Undirected, Weighted/Unweighted |

### Linear Structures

**Array**: Contiguous memory, O(1) random access, O(n) insertion/deletion (shifting required).

**Linked List**: Non-contiguous nodes storing a value and pointer(s). Singly linked: value + next pointer. Doubly linked: value + next + prev pointers. O(n) random access, O(1) insertion/deletion at a given node.

**Stack**: Last-In-First-Out (LIFO). Operations: push (top), pop (top), peek (top). Used for function call stacks, undo mechanisms, expression evaluation, and DFS.

**Queue**: First-In-First-Out (FIFO). Operations: enqueue (back), dequeue (front). Used for BFS, task scheduling, and buffering.

**Hash Table**: Maps keys to values using a hash function. Average O(1) insert/lookup/delete. Collisions resolved via chaining (linked lists per bucket) or open addressing (linear/quadratic probing). Worst-case O(n) if all keys hash to the same bucket.

### Tree Structures

**Binary Tree**: Each node has at most two children (left, right).

**Binary Search Tree (BST)**: For every node, all values in the left subtree are smaller and all values in the right subtree are larger. No duplicate keys. Search, insertion, and deletion are O(h) where h is the height -- O(log n) for a balanced tree, O(n) for a degenerate (linked-list) tree.

**Heap**: A complete binary tree satisfying the heap property: in a max-heap, every parent >= its children; in a min-heap, every parent <= its children. Implemented efficiently as an array. Used in priority queues and heap sort.

**N-ary Tree**: Nodes may have an arbitrary number of children. Common in file systems and organizational hierarchies.

### Graph

A graph G = (V, E) consists of vertices (nodes) and edges (connections). Represented via:

- **Adjacency matrix**: O(V^2) space, O(1) edge lookup. Good for dense graphs.
- **Adjacency list**: O(V + E) space. Preferred for most algorithms.

Key concepts:

- **Directed** vs **Undirected**: Edges have direction or not. Directed edges are arcs `<V1, V2>`; undirected edges are `(V1, V2)`.
- **In-degree / Out-degree**: For directed graphs, the number of edges pointing to / from a vertex.
- **Connected graph**: A path exists between every pair of vertices. A maximal connected subgraph is a **connected component**.
- **Path**: A sequence of vertices connected by edges. A **simple path** has no repeated vertices.
- **Cycle / Circuit**: A path that starts and ends at the same vertex.
- **Weight**: A real number assigned to an edge (e.g., distance, cost). A graph with weighted edges is a **network**.

---

## Core Algorithm Techniques

### Dynamic Programming

DP solves problems by breaking them into overlapping subproblems and caching results (memoization) to avoid redundant computation.

**Steps:**
1. Define the state: what variables capture the problem at any point?
2. Enumerate all possibilities for the state.
3. Derive the state transition equation.
4. Handle base cases.
5. Solve: bottom-up (tabulation) or top-down (memoization).

**Example: Stock Trading (Universal Template)**

The state `dp[i][k][0/1]` represents the maximum profit on day `i` with `k` transactions remaining and whether we hold stock (1) or not (0):

```
dp[i][k][0] = max(dp[i-1][k][0], dp[i-1][k][1] + prices[i])  # rest or sell
dp[i][k][1] = max(dp[i-1][k][1], dp[i-1][k-1][0] - prices[i]) # rest or buy
```

Base cases:
- `dp[-1][k][0] = 0` (no profit before any day)
- `dp[-1][k][1] = -inf` (cannot hold stock before day 0)
- `dp[i][0][0] = 0` (no transactions left, no stock)
- `dp[i][0][1] = -inf` (cannot hold stock with zero transactions remaining)

This template solves all six LeetCode stock problems (I: one trade, II: unlimited, III: at most two, IV: at most k, with cooldown, with transaction fee).

### Greedy Algorithms

Make the locally optimal choice at each step, hoping to reach a globally optimal solution. Greedy works when the problem exhibits:
- **Optimal substructure**: An optimal solution contains optimal solutions to subproblems.
- **Greedy choice property**: A locally optimal choice leads to a globally optimal solution.

Classic examples: interval scheduling (min arrows to burst balloons), Huffman coding, Dijkstra's shortest path, Kruskal's MST.

### Recursion and Recursion Trees

Draw a **recursion tree** to visualize recursive calls and their costs. Each node represents a subproblem; the tree's height is the recursion depth. This helps:
- Understand time complexity (sum costs across tree levels).
- Identify overlapping subproblems (opportunity for DP/memoization).
- Detect when a greedy approach suffices.

### Master Theorem

For recurrences of the form `T(n) = aT(n/b) + f(n)` where a >= 1, b > 1:

Let `c_crit = log_b(a)`:
- If `f(n) = O(n^c)` with `c < c_crit`: **T(n) = Theta(n^c_crit)**
- If `f(n) = Theta(n^c_crit * log^k n)`: **T(n) = Theta(n^c_crit * log^(k+1) n)**
- If `f(n) = Omega(n^c)` with `c > c_crit` and regularity holds: **T(n) = Theta(f(n))**

### Divide and Conquer

Split the problem into independent subproblems, solve each recursively, then combine results. Merge sort, quick sort, and binary search follow this pattern. The Master Theorem gives time complexity.

### Backtracking

Systematically explore all candidates, abandoning ("backtracking") a partial candidate as soon as it cannot lead to a valid solution. Used for permutations, combinations, and constraint satisfaction (N-Queens, Sudoku).

Key implementation pattern:
1. Make a choice.
2. Recurse.
3. Undo the choice (backtrack).

---

## Common Time Complexities

| Complexity | Name | Typical Scenario |
|-----------|------|-----------------|
| O(1) | Constant | Array access by index, hash table lookup |
| O(log n) | Logarithmic | Binary search, balanced tree operations |
| O(n) | Linear | Single pass through an array |
| O(n log n) | Linearithmic | Comparison-based sorting optimal |
| O(n^2) | Quadratic | Nested loops, simple DP |
| O(n^3) | Cubic | Triple nested loops, Floyd-Warshall |
| O(2^n) | Exponential | Exhaustive recursion on subsets |
| O(n!) | Factorial | Permutation generation (brute force) |
| O(n + k) | -- | Counting sort (k = value range) |
| O(nk) | -- | Radix sort (k = digit count) |

---

## Classic Interview Problems

### Binary Tree Traversals

Five fundamental traversal orders:

| Traversal | Order | Data Structure | Use Case |
|-----------|-------|---------------|----------|
| Pre-order | Root -> Left -> Right | Stack (DFS) | Serialization, prefix notation |
| In-order | Left -> Root -> Right | Stack (DFS) | BST yields sorted output |
| Post-order | Left -> Right -> Root | Stack (DFS) | Deletion, expression evaluation |
| Level-order | By level, left to right | Queue (BFS) | Shortest path in unweighted tree |
| Zigzag level-order | Alternating per level | Queue (BFS) | Aesthetic display |

**In-order (iterative):**

```python
def inorder_traversal(root):
    result, stack = [], []
    curr = root
    while curr or stack:
        while curr:                    # Reach leftmost node
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()             # Visit
        result.append(curr.val)
        curr = curr.right              # Move to right subtree
    return result
```

**Level-order (BFS):**

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

### Graph BFS and DFS

**BFS** finds the shortest path in an unweighted graph by exploring neighbors layer by layer.

**DFS** explores as far as possible along each branch before backtracking. Used for cycle detection, topological sort, and connected components.

```python
# BFS
from collections import deque

def bfs(graph, start):
    queue = deque([start])
    visited = set([start])
    while queue:
        node = queue.popleft()
        yield node
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# DFS (recursive)
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    yield node
    for neighbor in graph[node]:
        if neighbor not in visited:
            yield from dfs(graph, neighbor, visited)
```

### Problem-Solving Patterns

**Two Pointers**: Use `left` and `right` pointers moving toward each other (e.g., 3Sum, sorted two-sum, container with most water) or fast/slow pointers (linked list cycle detection, middle of linked list).

**Sliding Window**: Maintain a window `[left, right]` over an array, expanding and contracting based on a condition. Used for substring problems, fixed-sum subarrays, and string permutation matching. O(n) replaces brute-force O(n^2).

**Prefix Sum / Product**: Precompute cumulative values to answer range queries in O(1). Example: product of array except self uses left and right prefix products.

**Monotonic Stack / Queue**: Maintain a stack/queue with monotonic property to find next greater/smaller element in O(n).

### Key LeetCode Problems Covered

The original study covered ~66 problems. Here are the most instructive ones:

1. **Two Sum** -- Hash map for O(n) -- Foundational
2. **Add Two Numbers** -- Linked list digit-by-digit addition -- Pointer manipulation
3. **Median of Two Sorted Arrays** -- Binary search on shorter array -- O(log(min(m, n)))
4. **Best Time to Buy/Sell Stock (I-IV, cooldown, fee)** -- DP state template -- 6 problem variants
5. **Longest Palindromic Substring** -- Expand from center or Manacher's algorithm (O(n))
6. **3Sum** -- Sort + two pointers, O(n^2), careful deduplication
7. **Longest Increasing Subsequence** -- DP O(n^2) or DP + binary search O(n log n)
8. **LRU Cache** -- OrderedDict or hash map + doubly linked list
9. **Word Search** -- DFS with backtracking on a 2D grid, mark visited cells
10. **Max Subarray** -- Kadane's algorithm O(n), DP or greedy sliding window
11. **Lowest Common Ancestor** -- DFS with recursive search for BST (O(h)) or general binary tree
12. **Merge K Sorted Lists** -- Min-heap of size K or divide-and-conquer merge
13. **Permutations I/II** -- Backtracking with swap, deduplication via sorting/skip
14. **Sort Colors (Dutch National Flag)** -- Three-way partition with two pointers O(n)
15. **Set Matrix Zeroes** -- Use first row/column as markers, O(1) extra space
16. **Serialize and Deserialize Binary Tree** -- Pre-order DFS with null markers
17. **Flatten Binary Tree to Linked List** -- Post-order traversal (right-first) in-place
18. **Construct Tree from Inorder + Postorder** -- Recursive with hash map index lookup
19. **Jump Game** -- Greedy from end to start (reachability)
20. **Copy List with Random Pointer** -- Hash map for deep copy or interleaving O(1) space
21. **Linked List Cycle** -- Floyd's slow/fast pointer
22. **Valid Parentheses** -- Stack matching
23. **Simplify Path** -- Split on "/" and use a stack
24. **Roman to Integer** -- Subtraction pattern for special cases (IV=4, IX=9, etc.)
25. **String to Integer (atoi)** -- Single pass or regex, handle overflow
26. **Water and Jug Problem** -- Number theory, Bezout's theorem (GCD)
27. **Missing Number** -- XOR all indices and values, single pass O(n)
28. **Integer to English Words** -- Divide and conquer by groups of thousands
29. **Bulb Switcher** -- Square numbers have odd number of factors, return floor(sqrt(n))
30. **2 Keys Keyboard** -- Prime factorization sum

---

## Fundamentals to Master

These should be second nature for interviews:

- Binary search (iterative and recursive)
- Binary tree traversals (pre-order, in-order, post-order, level-order)
- Basic dynamic programming (Fibonacci, knapsack, stock problems)
- Backtracking and recursion
- Graph BFS and DFS
- Quick sort and merge sort implementations
- Divide and conquer with Master Theorem analysis
- KMP substring search
- Stack and queue implementations

---

## References

- [LeetCode Explore](https://leetcode.com/explore/)
- [Dynamic Programming Stock Problems -- Universal Template](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/solutions/)
- [KMP Algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm)
- [Dutch National Flag Problem](https://en.wikipedia.org/wiki/Dutch_national_flag_problem)
- [Master Theorem for Divide and Conquer](https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms))
