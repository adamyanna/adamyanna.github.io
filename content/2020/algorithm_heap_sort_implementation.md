# Algorithm: Heap Sort Implementation

> 2020-03-31

A deep dive into heap sort: the binary heap data structure, the heapify algorithm, a complete C implementation, rigorous time complexity analysis using summation of arithmetic-geometric series, and a comparison with merge-based approaches for merging sorted sequences.

## Merging Sorted Sequences

Before tackling heap sort itself, it is instructive to review related problems involving merging already-sorted sequences.

### Merge Two Sorted Linked Lists

Given two sorted linked lists `l1` and `l2`:

1. Compare the current node values of `l1` and `l2`.
2. Append the smaller node to the new result list by setting its `next` pointer.
3. Advance the pointer of whichever list contributed the node.
4. Continue (`while l1 and l2`) until one list is exhausted.
5. Append any remaining nodes from the non-empty list to the result.
6. Return the new list's `next` pointer (skipping the dummy head node).

**Time complexity:** O(M + N) where M and N are the lengths of the two input lists. Each node is visited exactly once.

### Merge K Sorted Linked Lists

**Pairwise merge approach:** Merge the k lists in pairs, round by round. After round 1, k/2 merged lists remain. After round 2, k/4 remain. This logarithmic reduction continues until a single merged list remains.

- k decreases exponentially: k, k/2, k/4, k/8, ...
- Each round processes N total nodes (the sum of lengths across all current lists)
- There are log k rounds
- **Total time complexity: O(N log k)**

This is substantially more efficient than repeatedly merging one list with the running result (which would cost O(N x k)).

### Merge N Sorted Arrays of Length M

Given n arrays, each of length m and already sorted:

**Brute force approach:** Concatenate all n arrays into a single (m x n) array, then apply any comparison-based sort. This costs O(mn log mn).

Sorting options for the concatenated array:
- **Quick sort** -- Pivot selection heavily influences performance. The median-of-three method (choosing the median of the first, middle, and last elements as the pivot) mitigates worst-case behavior on sorted or reverse-sorted inputs. Average-case analysis invokes the Master Theorem for recurrences.
- **Merge sort** -- Divide down to single elements, then merge upward. Predictable O(n log n) regardless of input distribution.
- **Heap sort** -- Build a heap structure from the array, then repeatedly extract the extremum. The subject of the remainder of this article.

## Divide and Conquer

Divide-and-Conquer is a fundamental algorithmic paradigm: decompose a problem into smaller sub-problems, solve each independently, then combine the results.

### Merge Sort as Divide-and-Conquer

Merge sort exemplifies the paradigm:

1. **Divide phase:** Recursively halve an array of length n. After log n divisions, the array is split into n single-element arrays (each trivially sorted by definition).

2. **Conquer phase:** Merge every pair of adjacent sorted sub-arrays using dual pointers (indices `i` and `j`). Compare the elements, place the smaller one into the result, and advance the corresponding pointer. Each merge pass processes all n elements, costing O(n). This merging repeats across log n levels (as sub-arrays double in size each level).

3. **Result:** O(n log n) total time complexity. Unlike quick sort, merge sort's performance is completely unaffected by input order -- no pivot selection means no degenerate case.

### Merging K Sorted Sub-sequences

Merging k already-sorted sub-sequences, each of length n, is effectively half of a merge sort -- only the conquer phase is needed since the sub-sequences are already sorted:

- Each pairwise merge across all k sequences costs O(nk)
- Reducing k sequences to 1 requires log k rounds
- **Optimal solution: O(nk log k)**

This is the lower bound for comparison-based merging of pre-sorted sequences.

## Heap Sort

Heap sort is a comparison-based sorting algorithm that uses the binary heap data structure. It belongs to the selection sort family. Its worst-case, best-case, and average-case time complexities are all O(n log n). It is **not a stable sort**: equal elements may change relative order.

### The Heap Data Structure

A heap is a **complete binary tree** satisfying the heap property:

**Max-heap:** Every parent node is greater than or equal to both of its children.
`arr[i] >= arr[2i + 1] && arr[i] >= arr[2i + 2]`

**Min-heap:** Every parent node is less than or equal to both of its children.
`arr[i] <= arr[2i + 1] && arr[i] <= arr[2i + 2]`

Example max-heap stored in an array:

| Index | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| Value | 50 | 40 | 30 | 30 | 35 | 20 | 25 |

This array represents the tree:

```
        50
      /    \
    40      30
   /  \    /  \
 30   35  20   25
```

In an array-based heap:
- Parent at index `i` has children at `2i + 1` (left) and `2i + 2` (right).
- A child at index `i` has its parent at `(i - 1) / 2` (integer division).
- The last non-leaf node is at index `n/2 - 1`.

### Algorithm Steps

1. **Build max-heap:** Rearrange the input array into a valid max-heap. After this step, the maximum value in the entire array sits at index 0 (the root).

2. **Extract maximum:** Swap the root element (current maximum) with the last element of the unsorted portion of the array. The last position now holds the sorted maximum and is excluded from further heap operations.

3. **Rebuild heap:** The new root may violate the heap property. Percolate it downward (sift-down / heapify) through the remaining n-1 elements to restore the max-heap.

4. **Repeat:** Apply steps 2 and 3 to the remaining unsorted portion (n-1, n-2, n-3, ... elements) until only one element remains -- the smallest, already in position.

### Detailed Heap Construction

Building the initial heap from an unsorted array:

1. **Start** from the last non-leaf node (at index `n/2 - 1`). For this node, compare it with its left and right children. If either child is larger, swap the node with the larger child. This promotes the largest value among the three to the parent position.

2. **Move backward** to the second-to-last non-leaf node. Repeat the comparison-and-swap process.

3. **Continue** through every non-leaf node, working from right to left, bottom to top. After processing all non-leaf nodes, the array satisfies the max-heap property.

4. **After the initial heap is built**, swap the root (maximum) with the last leaf node. Then sift the new root down through the reduced heap (size n-1) to restore the heap property.

If a swap occurs during sift-down, the percolation continues recursively into the affected subtree -- the swapped-down value may need to sink further until it finds its correct position.

### Time Complexity Analysis

#### Initial Heap Construction: O(n)

For a complete binary tree of height k, analyze the cost level by level:

- Level 1 (root): 1 node, may need k-1 comparisons
- Level 2: 2 nodes, each may need k-2 comparisons
- Level 3: 4 nodes, each may need k-3 comparisons
- ...
- Level i: 2^(i-1) nodes, each may need k-i comparisons

The total number of comparison operations in the worst case:

```
T(n) = 2^(k-2) x 1 + 2^(k-3) x 2 + 2^(k-4) x 3 + ... + 2^0 x (k-1)
```

Leaf nodes (level k) require zero comparisons in the initial build since they are already at the bottom and undergo no sift-down.

This is an arithmetic-geometric series. Summing it:

```
T(n) = 2^k - k - 1
```

For a complete binary tree: `2^k <= n < 2^(k+1)`, so `log(n+1) < k <= log n`.

Substituting: `T(n) = n - log n - 1`.

Therefore, building the initial heap costs **O(n)**. This is a counterintuitive but important result: constructing a heap from an arbitrary array is linear time, not O(n log n).

#### Rebuilding After Each Extraction: O(n log n)

After swapping the root with the last element, restoring the heap property via sift-down requires at most O(log n) operations (the height of the tree). This rebuild happens n-1 times.

```
T_rebuild(n) = (n - 1) x O(log n) = O(n log n)
```

#### Overall Complexity

```
T_heap_sort(n) = O(n) + O(n log n) = O(n log n)
```

This holds for the **worst case, best case, and average case** alike. Unlike quick sort, which degrades to O(n^2) on already-sorted input (with naive pivot selection), heap sort consistently delivers O(n log n) regardless of input distribution.

However, heap sort typically has a higher constant factor than quick sort in practice due to poor cache locality: accessing children at indices `2i+1` and `2i+2` jumps across the array, defeating CPU prefetching and causing more cache misses than the sequential access patterns of merge sort or the localized partitioning of quick sort.

## Complete C Implementation

```c
#include <stdio.h>

/*
 * _heapAdjust: Sift-down operation to maintain the max-heap property.
 *
 * Parameters:
 *   array — pointer to the array representing the heap
 *   i     — index of the element to potentially sift down
 *   len   — effective length of the heap (unsorted portion)
 *
 * The function assumes that the subtrees rooted at the children
 * of index i are already valid heaps. It propagates the element
 * at index i downward until the max-heap property is restored.
 */
void _heapAdjust(int *array, int i, int len) {
    int tmp = array[i];  // Save the element being sifted down

    // Start from the left child of i; iterate down the tree
    for (int k = 2 * i + 1; k < len; k = 2 * k + 1) {

        // If the right child exists and is larger, choose the right child
        if (array[k] < array[k + 1] && k + 1 < len) {
            k++;
        }

        // If the saved element is smaller than the larger child,
        // promote the child up to the current position
        if (tmp < array[k]) {
            array[i] = array[k];
            i = k;  // Continue sifting down from the child's position
        } else {
            break;  // Heap property is satisfied at this level
        }
    }

    array[i] = tmp;  // Place the saved element in its final position
}

int main() {
    int len = 9;
    int array[] = {5, 6, 3, 7, 8, 9, 1, 2, 4};

    // --- Phase 1: Build the initial max-heap ---
    // Start from the last non-leaf node (len/2 - 1) and work backward
    for (int i = len / 2 - 1; i >= 0; i--) {
        _heapAdjust(array, i, len);
    }

    // Print the heap after construction
    printf("After heap construction: ");
    for (int i = 0; i < 9; ++i) {
        printf("%d, ", *(array + i));
    }
    printf("\n");

    // --- Phase 2: Repeatedly extract the maximum ---
    for (int j = len - 1; j > 0; j--) {
        // Swap root (max) with the last element of the unsorted portion
        int t = array[0];
        array[0] = array[j];
        array[j] = t;

        // Restore the heap property for the reduced heap (size j)
        _heapAdjust(array, 0, j);
    }

    // Print the sorted array
    printf("After heap sort:        ");
    for (int i = 0; i < 9; ++i) {
        printf("%d, ", *(array + i));
    }
    printf("\n");

    return 0;
}
```

**Output:**

```
After heap construction: 9, 8, 5, 7, 6, 3, 1, 2, 4,
After heap sort:        1, 2, 3, 4, 5, 6, 7, 8, 9,
```

### How the Code Works

**`_heapAdjust` (sift-down):** The core operation. It takes a node at index `i` and percolates it downward until the subtree rooted at `i` satisfies the max-heap property. At each step, it identifies the larger of the two children, compares it with the current node, and swaps if the child is larger. The function then continues from the child's position. This is an in-place operation requiring no additional memory beyond the loop variable and temporary storage for the sifted element.

**Phase 1 (build):** Starting from the last non-leaf node (`len/2 - 1`) and iterating backward to index 0, `_heapAdjust` is called on each node. This ensures that by the time a given node is processed, its children are already roots of valid heaps -- the precondition `_heapAdjust` requires.

**Phase 2 (extract):** After the heap is built, the root (index 0) holds the maximum value. It is swapped with the last unsorted element (index `j`), and `_heapAdjust` is called on the root with the reduced heap size `j`. After n-1 such extractions, the array is sorted in ascending order.

## Heap Sort vs. Other Sorting Algorithms

| Algorithm | Best Case | Average Case | Worst Case | Stable | Space | Notes |
|---|---|---|---|---|---|---|
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | No | O(1) | In-place, consistent performance |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | Yes | O(n) | Requires auxiliary array |
| Quick Sort | O(n log n) | O(n log n) | O(n^2) | No | O(log n) | Fastest in practice (cache-friendly) |
| Insertion Sort | O(n) | O(n^2) | O(n^2) | Yes | O(1) | Excellent for small or nearly-sorted arrays |

Heap sort's advantages: guaranteed O(n log n) without the O(n) auxiliary space of merge sort. Its disadvantage: poor cache locality makes it slower in practice than well-implemented quick sort for typical inputs. It is often used in embedded systems and as a fallback in hybrid sorting algorithms (e.g., intro sort, which starts with quick sort and switches to heap sort if recursion depth exceeds `log n` to prevent worst-case behavior).
