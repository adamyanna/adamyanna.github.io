# Red-Black Trees, B-Trees, and Database Indexing

> 2020-04-02

Study notes from _Introduction to Algorithms_ (CLRS, 3rd Edition) -- Chapters 13 (Red-Black Trees) and 18 (B-Trees), plus practical B+Tree indexing as used in MySQL and PostgreSQL.

---

## Part 1: Red-Black Trees (Chapter 13)

A **red-black tree** is a binary search tree that guarantees O(log n) worst-case dynamic-set operations by enforcing approximate balance. For a standard BST, the basic dynamic-set operations (SEARCH, PREDECESSOR, SUCCESSOR, MINIMUM, MAXIMUM, INSERT, DELETE) all run in O(h) where h is the tree height. When h is small these operations are fast, but when the tree degenerates, they perform no better than a linked list. Red-black trees solve this.

### Node Attributes

Each node carries five attributes: `color`, `key`, `left`, `right`, and `p` (parent). If a node has no child or parent, the corresponding pointer attribute holds the value NIL. NIL is treated as a pointer to the tree's leaf (sentinel) nodes; nodes carrying actual keys are considered internal nodes.

### The Five Red-Black Properties

1. Every node is either red or black.
2. The root is **black**.
3. Every leaf (NIL) is **black**.
4. If a node is **red**, then both its children are **black**.
5. For each node, all simple paths from the node to descendant leaves contain the same number of **black nodes**.

A red-black tree is exactly a binary search tree satisfying all five properties. Property 4 ensures that no path can contain two consecutive red nodes, and property 5 ensures uniform black-node counts across all descending paths. Together these guarantee that no path is more than twice as long as any other -- the tree is **approximately balanced**.

### Black-Height

The number of black nodes on any simple path from a given node down to a leaf is that node's **black-height** (bh). By property 5, all descending paths from a given node share the same black-height. The tree's black-height is the black-height of the root.

A red-black tree with n internal nodes has height at most 2 lg(n+1). All dynamic-set operations therefore run in O(log n) worst-case.

### Rotations: The Core Mechanism

Insertion and deletion in a red-black tree may temporarily violate the red-black properties. The tree is repaired using two operations:

**Left Rotation (on node x):**
Assume x's right child y is not NIL. The rotation "pivots" around the edge from x to y: y becomes the new root of the subtree, x becomes y's left child, and y's former left child becomes x's right child. All BST ordering is preserved.

**Right Rotation (on node y):**
The symmetric inverse of left rotation. Assume y's left child x is not NIL. After rotation, x becomes the subtree root, y becomes x's right child, and x's former right child becomes y's left child.

Rotations run in O(1) time and change only pointer references -- no key comparisons are needed.

### Insertion Fixup Overview

Insert a new node (colored red) as in a normal BST. This may violate property 2 (root must be black) or property 4 (no two consecutive reds). The fixup procedure handles three cases for a red node z whose parent is also red:

1. **z's uncle is red:** Recolor parent, uncle, and grandparent. Move the problem two levels up by setting z = grandparent.
2. **z's uncle is black, and z is a right child:** Left-rotate around z's parent, transforming into case 3.
3. **z's uncle is black, and z is a left child:** Right-rotate around grandparent and recolor.

After at most O(log n) recolorings and at most 2 rotations, all properties are restored. The root is colored black as a final step.

### Deletion Fixup Overview

Deleting a node from a red-black tree is more complex than insertion. The procedure first removes the node using standard BST deletion, tracking the color of the actually removed node. If the removed node was black, a "double-black" problem is introduced that must be resolved through four cases involving the sibling of the deficient node (recoloring and rotations). The full detail is covered in CLRS Chapter 13.

Red-black trees are used extensively in practice: the Linux kernel's Completely Fair Scheduler (CFS), the implementation of `std::map` and `std::set` in C++, and Java's `TreeMap` and `TreeSet` all rely on red-black trees.

---

## Part 2: B-Trees (Chapter 18)

B-trees are balanced search trees designed for **disk and other direct-access auxiliary storage devices**. Like red-black trees, they support O(log n) operations, but they dramatically reduce the number of disk I/O operations -- the true bottleneck when working with large datasets.

### Why B-Trees?

A B-tree node can hold many keys -- from a handful to thousands -- depending on the disk unit characteristics. The **branching factor** (the base of the logarithm) can be very large, so the actual tree height is much smaller than a red-black tree for the same number of elements. The strict height of a B-tree is O(log n), but with a large branching factor the constant factor is tiny.

### m-Order B-Tree Structure

- A B-tree is a balanced multi-way search tree.
- An m-order B-tree means each node has at most m children.
- Keywords are distributed across the entire tree; each keyword appears in exactly one node.
- Search begins at the root, compares keys to find the correct range, follows the corresponding child pointer, and repeats until the key is found or a leaf is reached.
- Search terminating at a non-leaf node returns immediately (unlike B+Tree).
- Search performance is equivalent to binary search over an ordered keyword set.

### Insertion and the Split Operation

B-tree insertion always happens at a leaf node. The procedure:

1. Search down the tree to find the appropriate leaf position.
2. If the leaf has room (fewer than m-1 keys), insert the new key in sorted order.
3. If the leaf is **full** (has m-1 keys), it must be **split**:
   - Create a new node. Move the upper half of the full node's keys to the new node.
   - Promote the **median key** up to the parent node.
   - If the parent is also full, the split propagates upward. In the worst case, splitting cascades all the way to the root, and the tree grows by one level.

### Deletion: Merge and Transfer

Deleting a key may cause a node to **underflow** (fewer than the minimum number of keys). This is repaired by:

- **Transfer (borrow):** If an adjacent sibling has surplus keys, "rotate" a key through the parent -- the parent key moves down into the deficient node, and a sibling key is promoted to the parent.
- **Merge:** If neither sibling has surplus keys, merge the deficient node with a sibling and demote the separator key from the parent. This reduces the parent's key count and may trigger further underflow upward.

These operations are what allow B-trees to maintain their balance invariant: **all leaves are at the same depth**. This property is what guarantees O(log n) performance consistently, unlike a standard BST that can degrade.

### B-Tree Variants in Database Systems

- **B-Tree (aka B-Tree):** The notation "B-tree" and "B-Tree" are equivalent. Both refer to Bayer and McCreight's original balanced multi-way search tree.
- **B+Tree:** All data in leaves; internal nodes are pure index. Used by MySQL (InnoDB, MyISAM) and PostgreSQL.
- **B*Tree:** A variant where nodes are kept at least 2/3 full (vs. 1/2 for standard B-tree), achieved by redistributing keys between siblings before splitting.

---

## Part 3: B+Tree and Indexing Principles

### B+Tree vs B-Tree

The B+Tree is the variant used in practice for database indexing. Key differences:

| Aspect | B-Tree | B+Tree |
|---|---|---|
| Keyword storage | Distributed across all nodes | All keywords stored only in leaf nodes |
| Internal nodes | Store data and serve as index | Serve purely as index (contain only subtree max/min keys) |
| Leaf linkage | Leaves are not linked | Leaves form a **sorted linked list** |
| Search termination | Can terminate at internal nodes | Always traverses to a leaf |
| Range queries | Require tree re-traversal | Sequential scan via leaf pointers |

In a B+Tree, internal nodes are non-data "index" nodes containing only the minimum or maximum key of their subtree. A search that matches a key in an internal node does not stop there -- it continues down to the leaf. Every query, whether successful or not, travels a full root-to-leaf path.

### Sequential Access Pointers

Relational databases optimize the classic B+Tree by adding **sequential access pointers** between adjacent leaf nodes. Each leaf points to its immediate successor, forming a sorted doubly linked list at the leaf level.

This dramatically improves **range scan** performance. Consider:

```sql
SELECT * FROM t WHERE key BETWEEN 'A' AND 'F';
```

After a single root-to-leaf descent to find 'A', the engine simply follows the leaf-level linked list to 'F' and returns all intervening data. One tree-height traversal retrieves the entire range -- no need to revisit internal nodes.

---

## Part 4: Computer Storage Principles

Understanding why B+Trees work so well requires understanding how computers read from disk.

### Main Memory (DRAM)

The computer virtualizes main memory as a one-dimensional linear array of fixed-length cells. Physically, main memory is DRAM (Dynamic Random Access Memory). Read operations place a physical address on the address bus; the memory controller decodes the signal, locates the storage unit, and places the data on the data bus. Write operations place both address and data on their respective buses. Access time is linear with respect to the number of accesses.

### Disk Access

A disk consists of multiple platters and read/write heads. Each platter surface has concentric **tracks**; tracks at the same radius across all platters form a **cylinder**. Tracks are divided radially into **sectors** -- the minimum storage unit on disk.

Reading data involves: the system sends a logical address to the disk controller, the controller translates it to a physical address (cylinder, head, sector), the read/write head seeks to the correct track (**seek time**, roughly 8-10 ms), and the disk rotates to position the target sector under the head (**rotational latency**).

### The Principle of Locality

Disks improve throughput by **pre-reading** -- when only one byte is requested, the disk reads a contiguous block starting from that position into memory. This works because of the **principle of locality**: when a piece of data is accessed, nearby data is likely to be accessed soon after.

### Pages

The operating system divides disk storage into equal-sized logical blocks called **pages** (typically 4 KB each). Main memory and disk exchange data in units of pages. When a program requests data not present in main memory, a **page fault** occurs: the OS signals the disk controller to read the starting address and several consecutive pages into memory, then the fault handler returns and the program continues.

---

## Part 5: Index Performance Analysis

### B-Tree (B-Tree is B-Tree; the "-" is historical notation)

For a B-Tree index, each retrieval traverses from root to leaf. With tree height h, each search visits h nodes. By exploiting the OS's disk pre-reading principle, we size each node to exactly **one page** (4 KB), so each node requires exactly **one I/O operation** to fully load. When a new node is allocated, we request one page of space, ensuring the node is page-aligned in physical storage.

Since the root node typically resides in main memory, a B-Tree search requires at most **h - 1 I/O operations**. The asymptotic complexity is:

```
O(h) = O(log_d N)
```

where h is tree height and d is the tree's degree (maximum children per node). In practice, d is usually well over 100, so h is typically less than 3. Most B-Tree searches require no more than **3 disk I/Os**.

### Red-Black Tree

A red-black tree is a binary search tree; its height h is significantly larger than a B-tree's for the same n. More critically, logically adjacent nodes (parent and child) may be far apart in physical storage, so the principle of locality does not apply. The I/O complexity is also O(h), but with a far larger h and no pre-reading benefit. Red-black trees are poor choices for disk-resident data.

### B+Tree

B+Trees are even better for external-memory indexing because of the relationship between the node's **out-degree d** and what the node must store:

```cpp
d_max = floor(pagesize / (keysize + datasize + pointsize));
```

In a B+Tree, internal nodes drop the `data` field -- they store only `(key, pointer)` pairs. This means each internal node can hold more keys, giving the tree a higher out-degree. A higher d means each I/O operation brings more index information into memory, further reducing tree height and I/O count.

---

## Part 6: MySQL Index Implementation

MySQL supports multiple storage engines. The two most prominent -- MyISAM and InnoDB -- implement indexes differently.

### MyISAM Engine (Non-Clustered Index)

MyISAM uses B+Tree for its index structure. The **leaf node's data field stores the physical address of the data record**, not the record itself. MyISAM supports two index types:

- **Primary index (PRIMARY KEY):** Key must be unique. A table may exist without one.
- **Secondary index:** User-created search indexes; keys may be duplicated.

Structurally, both use B+Trees with the root node resident in memory. The retrieval process: (1) search the B+Tree for the key, (2) upon reaching the leaf, extract the data record's address from the leaf's value field, (3) read the record from that disk address into memory.

This design is called **non-clustered** -- data and index are stored separately, linked by pointers.

### InnoDB Engine (Clustered Index)

InnoDB also uses B+Tree, but with two critical differences:

**1. The table data itself is organized as a B+Tree index.** The leaf node's value field contains the **complete data record**, and the index key is the **primary key**. In other words, the InnoDB table data file is itself the primary key index. This is a **clustered index** -- data rows are physically organized by primary key order.

Because table data is clustered on the primary key, InnoDB **requires every table to have a primary key, and it must be unique**. If you do not explicitly declare one, MySQL will: (a) select the first column that can uniquely identify each row, or (b) if none exists, auto-generate a hidden 6-byte integer column as the primary key.

**2. Secondary index leaf nodes store the primary key value, not a physical address.** This means InnoDB secondary indexes reference the primary key as their leaf data. To retrieve a record via a secondary index, InnoDB performs **two B+Tree searches**: first the secondary index to find the primary key, then the primary (clustered) index to retrieve the full row. This double-lookup is roughly half as efficient as a direct primary key search.

### Practical Implications

Understanding engine internals leads to actionable design rules:

1. **Avoid overlong primary keys.** Since every secondary index leaf stores a copy of the primary key, long primary keys bloat every secondary index on the table.

2. **Use monotonic (auto-increment) fields as primary keys in InnoDB.** The InnoDB data file itself is a B+Tree. Inserting a new record with a non-monotonic primary key forces the B+Tree to perform frequent node splits and rebalancing to maintain order -- this is extremely inefficient. An auto-increment integer ensures new records are always appended at the rightmost leaf, minimizing page splits.

3. **Prefer InnoDB's clustered design for primary-key lookups.** A single B+Tree traversal retrieves the complete row -- no secondary address lookup is needed.

---

## Summary

| Tree | Height | I/O Complexity | Best Use |
|---|---|---|---|
| Red-Black Tree | O(log_2 n) | O(log_2 n) | In-memory data structures |
| B-Tree | O(log_d n), d > 100 | O(log_d n), typically ≤ 3 I/Os | Disk-resident indexes |
| B+Tree | O(log_d n), higher d than B-Tree | O(log_d n), range-optimized via leaf links | Database indexes (MySQL, PostgreSQL) |

The progression from red-black tree to B-tree to B+tree is a story of optimizing for the physical reality of storage: memory is fast and random-access, while disk is slow and sequential-access. Each refinement in the tree structure aligns the logical data organization more closely with how the hardware actually reads and writes data.

Reference: [Zhihu article on B+Tree indexing](https://zhuanlan.zhihu.com/p/77383599)
