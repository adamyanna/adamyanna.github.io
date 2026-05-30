# My Algorithm Learning Curve

> 2020-03-02

A curated problem-solving journal documenting my journey through algorithmic problem-solving -- key patterns, techniques, pitfalls, and LeetCode problems organized by difficulty and approach.

---

## Easy Problems

### 1. Two Sum
Find two numbers in an array that sum to the target.
- **Hash map (DP):** For each element, store visited values in a map. For value `v`, check if `target - v` exists. O(n).
- **Sort + two pointers:** Sort the array, then converge pointers from both ends toward the target. O(n log n).

### 2. Roman to Integer
Traverse the input string, convert each Roman numeral character to an integer and append to a temporary list. When the last element satisfies the subtractive rule (e.g., IV=4, IX=9), pop the previous value and subtract. Sum the list at the end. O(n).

### 3. Count Primes (Sieve of Eratosthenes)
Starting from `i²`, mark all multiples of `i` (stepping by `i`) as composite. The unmarked numbers that remain are primes. Time complexity: O(n log log n) by the prime distribution theorem and the fundamental theorem of calculus.

**Euler's Sieve (Linear Sieve):** Each composite number is marked exactly once by its smallest prime factor. Achieves O(n) time with no redundant marking.

### 4. Merge Two Sorted Lists
Compare `l1.val` vs `l2.val`, place the smaller one on the new list's next pointer, and advance the corresponding list. Continue until one list is exhausted (`while l1 and l2`). Return the new list's head (the node after the sentinel). O(m + n).

### 5. Remove Duplicates from Sorted Array
**Fast/Slow two pointers.** Both start at 0 and 1. If their values differ, advance the slow pointer and write the fast pointer's value. If equal, only advance the fast pointer. The slow pointer maintains the boundary of the deduplicated prefix. O(n), O(1) space.

### 6. Implement strStr() -- Substring Search
Single pass tracking the index of the first match. When characters match, accumulate; on mismatch, reset. Stop when the remaining string length is less than the needle length. O(n). For more advanced solutions, KMP achieves O(n + m).

### 7. Maximum Subarray
- **Greedy:** Maintain two variables: `current_window` (max subarray sum ending at the current position) and `global_max` (max seen so far). At each step: `current = max(current + nums[i], nums[i])`. O(n).
- **Sliding window / DP:** Equivalent to the greedy formulation. The DP state at position `i` is exactly the greedy `current_window`.
- **Divide and Conquer:** Compute max subarray crossing the midpoint, then recurse on left and right halves.

### 8. Merge Sorted Array (m + n elements, m-array has buffer)
**Two pointers from the end.** Compare the largest remaining element from each array and place it at the tail of the merged array. Use a third pointer to track the write position. When the n-array is fully consumed, the result is complete. O(m + n).

### 9. Symmetric Tree (Mirror Check)
- **Iterative BFS:** Collect nodes level by level; check whether each level's value array is palindromic.
- **Recursive:** Starting from root's left and right subtrees, verify `left.val == right.val`, then recurse on `(left.left, right.right)` AND `(left.right, right.left)`.

### 10. Path Sum
**Iterative BFS** using a queue storing `(node, remaining_sum)` tuples. Initialize with `(root, targetSum - root.val)`. On reaching any leaf, check whether `remaining == 0`. Return true if any leaf satisfies the condition.

### 11. Valid Palindrome
Two pointers from the start and end, skipping non-alphanumeric characters (`isalnum`). Converge until the pointers meet or cross. Compare characters case-insensitively at each step.

### 12. Intersection of Two Linked Lists
**Two-pointer trick.** Two pointers start simultaneously from each list's head. When one pointer reaches the end, switch it to the other list's head. They meet at the intersection point because both travel the same total distance: `m_shared_prefix + k_shared_suffix` for each list is the same when paths are swapped. Mathematically: `(m + k) + n = (n + k) + m`.

### 13. Excel Column Title (Number to Letters)
A base-26 problem, but there is no zero digit. When the remainder is 0, the digit must be 'Z' (representing 26). Handle this by treating `n % 26 == 0` as 'Z' and subtracting 26 from n before dividing.

### 14. Excel Column Number (Letters to Number)
```python
result = sum((ord(c) - 65 + 1) * (26 ** (len(s) - 1 - i)) for i, c in enumerate(s))
```

### 15. Rotate Array (Right by k, In-Place)
**Cyclic replacement.** Start at index 0: `nums[i] -> nums[i+k] -> nums[i+2k] -> ...`. When the cycle returns to the starting index, increment the start by 1 and repeat. Count replacements; stop when n elements have been moved. O(n) time, O(1) space.

### 16. Number of 1 Bits (Hamming Weight)
```python
count = 0
while n:
    count += 1
    n &= n - 1   # Clears the lowest set bit
```
For any binary number, `n - 1` flips the lowest 1 to 0 and all trailing 0s to 1s. AND-ing with `n` clears exactly that lowest 1.

### 17. Reverse Linked List
Pointer manipulation: (1) save `next` temporarily, (2) set `current.next = prev`, (3) advance `prev = current`, (4) advance `current = saved_next`. Repeat until current is null; `prev` is the new head.

### 18. Delete Node in a Linked List (given only the node to delete)
Swap the node's value with its next node's value, then set `node.next = node.next.next`. Effectively copies the next node into the current position and removes the next node.

### 19. First Unique Character in a String (lowercase only)
Two passes: first pass builds a frequency hash map and preserves insertion order in a separate list. Second pass iterates the ordered list and returns the index of the first character with count 1. O(n) time, O(26) = O(1) space.

### 20. String Compression (In-Place)
Read pointer and write pointer start together. When the read pointer encounters a different character than the previous one, the write pointer writes the compression count (if > 1), then writes the new character. The read pointer continues counting. Final length is the write pointer's position.

---

## Medium Problems

### Linked List Arithmetic

**Add Two Numbers (reverse-order digits):** Simulate grade-school addition digit by digit. For each position, sum `l1.val + l2.val + carry`. Advance both lists; if one is shorter, treat missing values as 0. When sum >= 10, set carry for next node. O(max(m, n)).

**Add Two Numbers II (forward-order digits):**
- **Stack approach:** Push both lists onto stacks. Pop and add (LIFO gives least-significant digit first). Build the result list from tail to head. O(m + n).
- **Recursive approach:** Compute list lengths, align by recursing on the longer list first. Recursion naturally propagates the carry upward.

### Two Sum / Three Sum / K Sum

**Three Sum (find all triplets summing to 0):** Sort the array (O(n log n)). For each non-positive element `nums[i]`, use two pointers on the subarray `nums[i+1:]` to find pairs summing to `-nums[i]`. Skip duplicates to avoid redundant triplets. O(n²).

General pattern: sort first, then reduce k-sum to (k-1)-sum via nested loops with two-pointer inner loop.

### Stack Problems

**Valid Parentheses:** Push left brackets onto a stack. For each right bracket, check if the stack is non-empty and the top matches. If the stack is empty when a right bracket arrives, or the top does not match, the string is invalid. At the end, the stack must be empty.

**Simplify Path:** Split the path by `/`. Use a stack: ignore `""` and `"."`; on `".."`, pop the top directory; otherwise push the directory name. Join the stack with `/`.

### Recursion and Backtracking

**Permutations (no duplicates):** For each position `start` through `n-1`, swap `start` with position `i`, then recurse on `start + 1`. After returning, swap back (backtrack) to restore the array for the next iteration.

**Permutations II (with duplicates):** Same approach, but before swapping, check a set to see whether `nums[i]` has already been placed at position `start` in this recursion level. Skip if duplicate.

### Matrix Problems

**Rotate Image (90 degrees clockwise, in-place):** Transpose the matrix (swap `matrix[i][j]` with `matrix[j][i]`), then reverse each row left-to-right. O(n²).

**Spiral Matrix (output in spiral order):** Simulate the spiral by repeatedly stripping the top row, right column, bottom row (reversed), and left column (reversed) from the matrix until one element remains.

**Set Matrix Zeroes (in-place, constant space):** Use the first row and first column as flags. First, record whether the first row and first column themselves contain zeros. Then scan the rest of the matrix: if `matrix[i][j] == 0`, set `matrix[i][0] = 0` and `matrix[0][j] = 0`. Finally, zero out rows and columns based on flags, then handle the first row and column.

### Tree Traversals (Inorder, Preorder, Postorder, Level-Order)

**Recursive DFS:**
- Preorder: `append(val) -> recurse left -> recurse right`
- Inorder: `recurse left -> append(val) -> recurse right`
- Postorder: `recurse left -> recurse right -> append(val)`

**Iterative DFS (stack):**
- Preorder: Push root. Pop, append value, push right then left.
- Inorder: Go leftmost, pushing each node. Pop, append value, move to right child. Repeat.
- Postorder: Same as preorder but push left then right; reverse the result array at the end.

**Level-Order (BFS):**
- Iterative: Queue stores nodes. Dequeue, append value, enqueue left, enqueue right.
- Recursive: Pass `level` parameter. Append value to `result[level]`, recurse on children with `level + 1`.

**Binary Tree Zigzag Level Order:** Same as level-order, but for odd levels, insert at position 0 (or reverse the level array before appending).

**Construct Binary Tree from Inorder and Postorder:** The last element of postorder is the root. Find its index in inorder; elements left of it form the left subtree, elements right form the right subtree. Recursively build: first process the right subtree (since postorder visits right before root), then the left. O(n).

**Flatten Binary Tree to Linked List:** Reverse postorder traversal (right, left, root). Maintain a `last` reference. For each node: set `node.right = last`, `node.left = None`, and update `last = node`.

### Dynamic Programming

**Decode Ways (count decodings of digit string):** Let `dp[i]` be the number of ways to decode the first `i` characters. For a valid single-digit decode (`1` to `9`), add `dp[i-1]`. For a valid two-digit decode (`10` to `26`), add `dp[i-2]`. Handle `0` carefully: `0` is only valid after `1` or `2`; otherwise the string cannot be decoded.

**House Robber I (no adjacent houses):** `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`. Two states: skip this house (take previous max) or rob this house (take two-back max plus current).

**House Robber II (circular):** The first and last houses are adjacent, so they cannot both be robbed. Run House Robber I twice: once on `nums[1:]` (skip first), once on `nums[:-1]` (skip last). Take the max.

**House Robber III (binary tree):** Postorder DFS. For each node, return `[not_rob, rob]`:
- `rob = node.val + left[not_rob] + right[not_rob]` -- rob current, cannot rob children.
- `not_rob = max(left) + max(right)` -- skip current, children are free to rob or not.

**Longest Increasing Subsequence:**
- DP: `dp[i]` = max length ending at index `i`. For each `j < i`, if `nums[j] < nums[i]`, `dp[i] = max(dp[i], dp[j] + 1)`. O(n²).
- DP + Binary Search: Maintain an array `tails` where `tails[k]` = the smallest possible tail value of an increasing subsequence of length `k+1`. For each `x`, binary-search `tails` for the first element `>= x` and replace it (or append if `x` is larger than all). O(n log n).

### Stock Problems (Unified DP Framework)

State definition: `dp[i][k][0/1]` where `i` is the day, `k` is remaining transactions, and `0/1` is whether you hold stock.

Base cases:
- `dp[-1][k][0] = 0` (no stock, before any day)
- `dp[-1][k][1] = -inf` (impossible to hold stock before any day)
- `dp[i][0][0] = 0`, `dp[i][0][1] = -inf` (no transactions left)

State transitions:
- `dp[i][k][0] = max(dp[i-1][k][0], dp[i-1][k][1] + prices[i])` -- rest or sell
- `dp[i][k][1] = max(dp[i-1][k][1], dp[i-1][k-1][0] - prices[i])` -- rest or buy

This framework covers all stock problems (Best Time I/II/III/IV, with cooldown, with transaction fee).

### Graph / Grid Problems

**Number of Islands (connected components in a 2D grid):** BFS or DFS from each unvisited '1'. Mark visited cells as '0' (in-place) to avoid revisiting. Each BFS/DFS initiation counts one island. O(m \* n).

**Battleships in a Board:** Simpler than general islands -- battleships are 1xN or Nx1 and do not touch. Count a cell `'X'` only if there is no `'X'` immediately above it AND no `'X'` immediately to its left. Single pass, O(m \* n).

**Word Search (find word in 2D grid, adjacent letters):** DFS from each cell matching the first letter. At each step, mark the cell as visited, recurse in four directions for the next letter, and restore the cell on backtrack. Return true when all letters are matched.

### Other Notable Medium Problems

**LRU Cache:** Doubly linked list + hash map. The list maintains access order (head = most recently used, tail = least recently used). The hash map provides O(1) node lookup. On `get`, move the node to head. On `put`, add to head; if over capacity, remove the tail node.

**Copy List with Random Pointer:** DFS with memoization. Hash map stores `original_node -> copied_node`. For each node: if already copied, return the copy; otherwise create a new node, store in map, then recursively copy `next` and `random`.

**Linked List Cycle Detection:** Fast/slow pointers. Fast moves two steps, slow moves one. If they meet, a cycle exists. If fast reaches null, no cycle.

**Find Peak Element (any peak, O(log n)):** Binary search. If `nums[mid] > nums[mid+1]`, the array is descending at `mid`, so a peak must exist in the left half (including `mid`). Otherwise, a peak must exist in the right half. Converge `l` and `r`.

**Kth Largest Element in an Array:** Quickselect. Partition around a pivot; if the pivot lands at `n - k`, return it. If it lands left of `n - k`, recurse on the right partition; otherwise recurse on the left. Average O(n), worst O(n²).

**Implement Queue using Stacks:** Two stacks -- `in_stack` for push, `out_stack` for pop/peek. When `out_stack` is empty, pop all elements from `in_stack` and push to `out_stack` (reversing order). Amortized O(1) per operation.

**Trie (Prefix Tree):** Each node is a dictionary mapping characters to child nodes. Insert: traverse/create nodes for each character; mark the end with a sentinel (`"#"`). Search: traverse; return true if the end sentinel is reached. StartsWith: traverse; return true as long as all characters are found (no sentinel needed).

**Binary Tree Right Side View / Populating Next Right Pointers:** Level-order traversal. For next-right pointers, connect nodes within each level from left to right before descending.

**Maximum Path Sum in Binary Tree:** Postorder DFS computing `max_gain(node)` = max single-branch path sum starting from node. At each node, `price_newpath = node.val + max(0, left_gain) + max(0, right_gain)`. Update global max. Return `node.val + max(0, left_gain, right_gain)` for the parent to use.

**Lowest Common Ancestor:**
- BST: If both p and q are less than root, go left. If both greater, go right. Otherwise root is the LCA.
- Binary Tree: DFS. Return the node if it matches p or q. If left and right both return non-null, current node is LCA. Otherwise propagate the non-null result upward.

**Product of Array Except Self:** Two passes. Left pass: `output[i] = output[i-1] * nums[i-1]` (product of everything to the left). Right pass: multiply by `right_product` tracking everything to the right. O(n) time, O(1) extra space.

**Container With Most Water / Trapping Rain Water:** Two-pointer convergence, moving the shorter wall inward (only a taller wall can increase area/water trapped).

**Sort Colors (Dutch National Flag, 0/1/2 in-place):** Three pointers: `p0` (boundary of 0s), `p2` (boundary of 2s), `curr` (current scanner). If `nums[curr] == 0`, swap with `p0` and advance both. If `nums[curr] == 2`, swap with `p2` and advance `p2` backward (do not advance `curr` -- the swapped-in value must be checked). If `nums[curr] == 1`, just advance `curr`. Stop when `curr > p2`.

**Jump Game:** Greedy from the back -- if you can reach the end from position `i`, the new "end" becomes `i`. Alternatively, track the furthest reachable position scanning forward.

**Merge Intervals / Burst Balloons:** Sort by the left boundary (or right boundary for min-arrows). After sorting, merge overlapping intervals in a single pass.

**Integer to English Words:** Divide into billions, millions, thousands, and the remainder. Each three-digit group is converted independently with helper functions for 1-9, 10-19, and 20-99 ranges. Combine with scale words.

**Bulb Switcher I:** A bulb `i` is toggled on every divisor of `i`. Only perfect squares have an odd number of divisors (others pair up). The answer is `floor(sqrt(n))` -- the count of perfect squares up to n.

**Bulb Switcher II:** Enumerate states. The first three lights determine all others (lights 5 and 6 mirror 3 and 2; light 4 is the XOR of switches affecting 1-3). For `m >= 3`, all possible states of the first three lights are achievable. Handle `m = 0, 1, 2` as special cases.

---

## Hard Problems

### Median of Two Sorted Arrays
Binary search on the shorter array to find a partition point where all elements on the left side of both arrays are <= all elements on the right side. The partition satisfies: `max(left_part) <= min(right_part)`. O(log(min(m, n))).

### Merge K Sorted Lists
Pairwise merging: merge lists in pairs, then merge the resulting lists. Each round halves the number of lists while doubling their average length. O(N log k) where N is the total number of nodes.

### Reverse Nodes in K-Group
Recursive approach: check whether k nodes remain. If yes, reverse the first k nodes (iteratively: repeatedly move `head.next` to the front of the segment). Recurse on the remainder. If fewer than k nodes remain, return the head unchanged.

### Search in Rotated Sorted Array
Single binary search. Compare `nums[mid]` with `nums[0]` to determine which side is sorted. Then check whether the target falls in the sorted side's range to decide which half to search next. O(log n).

### Serialize and Deserialize Binary Tree
Preorder traversal: serialize as `"val,left_subtree,right_subtree"`. Deserialize by consuming the first token as the root value, then recursively building left and right subtrees on the remaining tokens.

---

## Important Theorems and Concepts

### Master Theorem

For recurrences of the form `T(n) = a * T(n/b) + f(n)`:

- **Case 1:** If `f(n) = O(n^{log_b a - ε})` for some `ε > 0`, then `T(n) = Θ(n^{log_b a})`.
- **Case 2:** If `f(n) = Θ(n^{log_b a})`, then `T(n) = Θ(n^{log_b a} * log n)`.
- **Case 3:** If `f(n) = Ω(n^{log_b a + ε})` for some `ε > 0`, and `a * f(n/b) ≤ c * f(n)` for some `c < 1`, then `T(n) = Θ(f(n))`.

Example (Quicksort): `T(n) = 2T(n/2) + n` -- Case 2, `T(n) = Θ(n log n)`.

### Common Sorting Algorithms

- **Quicksort:** Choose pivot, partition, recurse on both sides. Average O(n log n) by Master Theorem.
- **Counting/Bucket Sort:** For numbers in a known range [0, k]. Create k buckets, count occurrences, expand. O(n + k).
- **Bubble Sort:** Repeatedly swap adjacent out-of-order pairs. Each pass bubbles the largest element to the end. O(n²).
- **Heap Sort:** Build a max-heap (or min-heap) from the unsorted array. Repeatedly swap the root (largest) with the last element, reduce heap size by 1, and sift down to restore the heap property. O(n log n).

### Fibonacci Numbers
Recursive: `fib(n) = fib(n-1) + fib(n-2)`. O(2^n) naive, O(n) with memoization, O(log n) with matrix exponentiation.

---

## Summary by Data Structure and Technique

| Category | Key Techniques |
|---|---|
| **Arrays** | Two pointers (fast/slow, converging, sliding window), binary search, sorting, prefix sums, cyclic replacement |
| **Strings** | Split/join, stack for matching, sliding window, KMP for substring search |
| **Linked Lists** | Dummy head, fast/slow pointers, in-place reversal, recursion for k-group manipulation |
| **Trees** | DFS (pre/in/post), BFS (level-order), recursion with return values, iterative with stack/queue |
| **Graphs** | BFS/DFS for connected components, in-place marking, adjacency traversal |
| **Dynamic Programming** | State definition, state transition equation, base cases, memoization, bottom-up tabulation |
| **Greedy** | Local optimal choice leads to global optimum; sorting + single pass is a common pattern |
| **Math** | Prime sieving, base conversion, greatest common divisor (Euclidean algorithm), digit manipulation |

### Python Implementation Note
Python's `list` is implemented as a C struct similar to C++ `std::vector` -- a contiguous array of object pointers with dynamic capacity. It is NOT a linked list. Operations like `pop(0)` are O(n); prefer `collections.deque` for O(1) pops from both ends, or use a reverse-indexing approach.
