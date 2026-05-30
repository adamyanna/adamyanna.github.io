# Massive Data Programming Patterns

> 2020-04-01

When datasets exceed available memory by orders of magnitude, conventional in-memory algorithms break down. This article covers two fundamental techniques -- Bitmap indexing and Divide-and-Conquer -- and extends them to a worked example: counting IP address frequencies in a 10-billion-line log file using only 100 MB of RAM. It also touches on B+Tree structures as used in database indexing for similar problems.

## Bitmap (Bitset)

A bitmap replaces multi-byte integers with a single bit at a calculated position within a byte array. Conceptually, it is a hash-based storage scheme where the hash function is simple modulo arithmetic.

### Core Insight

Consider storing five integers:

```c
int array[] = {1, 2, 3, 4, 5};
```

Using 32-bit integers, this occupies 5 x 4 = **20 bytes** in memory. With a bitmap, each integer maps to a single bit position within one or more bytes. The values 1 through 5 set bits 1 through 5:

| Bit Position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| Value | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |

`bitmap[0]` = 01111100 (binary) = 62 (decimal) = 0x3e (hex).

The same five integers now occupy **1 byte** instead of 20 bytes -- a 20x reduction for this tiny example, and the ratio grows with larger values.

### Implementation

```c
#include <stdio.h>

#define LEN 1
#define MASK 0xff        // 8 bits all set to 1
#define SHIFT 3          // division by 8 via bit shift

char bitmap[LEN];

void set(char i) {
    bitmap[i >> SHIFT] |= 1 << (i + 1);
}

int main(int argc, char const *argv[])
{
    int array[] = {1, 2, 3, 4, 5};
    for (int i = 0; i < 5; ++i)
    {
        set(array[i]);
    }
    int x = bitmap[0];
    while (x > 0) {
        printf("%d", x % 2);
        x = x / 2;
        if (x == 0)
        {
            printf("0 -- revert");
        }
    }
    printf("\n");
    printf("%d\n", bitmap[0]);
    printf("%x\n", bitmap[0]);
    printf("%d\n", sizeof(bitmap[0]));
    return 0;
}
```

### Indexing Formula

Two operations locate a value in a bitmap:

- **Index (which byte):** `value / size` or equivalently `value >> SHIFT` (where SHIFT = 3 for 8 bits per byte). This gives the byte offset within the bitmap array.

- **Position (which bit):** `value % size` determines which bit within that byte to set to 1. The modulo operation is the simplest possible hash function.

To retrieve a value, compute its position in the bitmap and test whether the corresponding bit is 1.

### Memory Reduction: Real-World Scale

Storing 4,000,000,000 IPv4 addresses:
- **Naive approach:** 4,000,000,000 x 4 bytes = 16,000,000,000 bytes = **16 GB**
- **Bitmap approach:** 4,000,000,000 bits = 500,000,000 bytes = **500 MB**

That is a **32x reduction** in memory footprint. This is the difference between requiring a high-end server and running on a modest laptop.

### Use Cases

**Membership testing:** Is a given integer present in the set? O(1) bit test.

**De-duplication:** Process a stream of values. For each value, check its bit. If already set, it is a duplicate; otherwise, set the bit and emit the value. The bitmap serves as a unique-seen filter.

**Sorting:** Iterating through the bitmap from position 0 to N and emitting values where the bit is 1 produces a sorted list of the original integers. This is essentially bucket sort with 1-bit buckets.

### Extension: 2-Bit Per Value Counting

To count how many times each value appears (distinguishing zero, one, and multiple occurrences), use **2 bits per value**:

| Bit Pattern | Meaning |
|---|---|
| `00` | Never appeared |
| `01` | Appeared exactly once |
| `10` | Appeared 2 or more times (duplicate) |

Implementation approach: use two parallel bitmaps (bitmap-A and bitmap-B), or pack 2-bit counters into a single byte array. When processing a value:
- If the 2-bit counter is `00`, set it to `01`
- If it is `01`, set it to `10`
- If it is `10`, leave it unchanged (already known duplicate)

For 250 million integers, this needs 500 million bits = ~60 MB, well within the memory constraints of typical interview problems.

## Divide and Conquer

When data absolutely cannot fit in memory -- even with bitmap compression -- the Divide-and-Conquer paradigm provides a general strategy. It mirrors the merge step of merge sort: split large problems into smaller, independently solvable ones, then combine the results.

### The I/O Constraint

For disk-backed processing, minimizing I/O operations is the primary performance driver:

| Storage Type | Average I/O Latency | Notes |
|---|---|---|
| HDD (mechanical) | 8-11 ms | Per 4 KB page; dominated by seek time of the physical read/write head |
| SSD (flash) | ~0.1 ms | Varies by interface (SATA vs NVMe) and NAND type |

Even modern SSDs are orders of magnitude slower than main memory access (~100 ns). The goal is to minimize the number of times each byte of data traverses the memory-disk boundary.

### Algorithm Structure

1. **Partition:** Split the large input file into smaller chunks that each fit within the available memory budget. The partitioning function should distribute records uniformly (e.g., hash-based on a key).

2. **Process independently:** Load each partition into memory, perform the required computation (sorting, counting, aggregation), and write the partial result to a temporary file.

3. **Merge:** Combine partial results into the final output. If partial results are already in the desired output format, merging may be a simple concatenation. If they need further aggregation, a final merge pass completes the process.

Total I/O cost is proportional to (number of partitions x operations per partition). Trade-offs exist between partition size (fewer, larger partitions mean more in-memory work) and partition count (more, smaller partitions mean more I/O rounds).

## Worked Example: IP Address Frequency Counter

This example brings together bitmap thinking and divide-and-conquer in a realistic scenario that appears frequently in systems design and engineering interviews.

### Problem Statement

- **Input:** A 10-billion-line log file. Each line contains exactly one IPv4 address.
- **Population:** 1 billion unique IP addresses, each appearing randomly and multiple times across the file.
- **Constraint:** The program may only use **100 MB** of main memory.
- **Output:** For each unique IP address, output the IP and its total occurrence count, as efficiently as possible.

### Analysis

**Storage requirements:**
- 1 billion unique IPs x 4 bytes each = **4 GB** for a naive sequential storage approach. This exceeds the 100 MB constraint by a factor of 40.
- A `uint32_t` (4 bytes) suffices to count occurrences of a single IP (max count = 2^32 - 1, far beyond any realistic scenario).

**Key observations:**
- IP addresses are randomly distributed throughout the log file.
- The 100 MB budget must accommodate both the data structure and any temporary buffers.
- 100 MB = 100,000,000 bytes. For 1 billion IPs at 4 bytes each, we need roughly 40 partitions.

### Solution: Two-Pass Partitioned Counting

#### Pass 1: Partition

1. Allocate a hash-based partitioning scheme: map each IPv4 address to a partition index using `ip_value % 400`, yielding 400 partitions.

2. Initialize 400 output buffers within the 100 MB memory space (approximately 25 MB per buffer on average, though in practice buffers share the space sequentially).

3. Read the log file line by line. For each IP address:
   - Convert the dotted-quad notation to a 32-bit integer
   - Compute `partition = ip_int % 400`
   - Append the IP to the corresponding in-memory buffer
   - When a buffer reaches capacity, flush it to the corresponding temporary file on disk, then clear the buffer

4. After processing all 10 billion lines, 400 temporary files exist, each containing a subset of the IP addresses. Since the partitioning function is deterministic, all occurrences of a given IP land in the same partition file.

**I/O cost for Pass 1:** Each of the 400 partitions is flushed to disk and read back. In the average case, this requires approximately 40 x 400 = 16,000 I/O operations for writes and an equal number for reads in Pass 2, totaling roughly **160 seconds** on a mechanical HDD (at ~10 ms per I/O).

#### Pass 2: Count and Output

1. For each of the 400 temporary files (each approximately 25 MB in the average case):
   - Load the file into memory
   - Sort the IP addresses (using quick sort or merge sort; merge sort is preferred for its predictable O(n log n) behavior regardless of input distribution)
   - Traverse the sorted array: count consecutive occurrences of each IP, output `<ip, count>` pairs to the final output file

2. Delete the temporary files after processing.

**I/O cost for Pass 2:** Each partition file is read once and results written once. This requires approximately 400 x 2 = 800 I/O operations, roughly **8 seconds** on a mechanical HDD.

### Total Performance

Combining bitmap-inspired memory discipline with divide-and-conquer partitioning, the entire 10-billion-line processing job completes in a matter of minutes -- on hardware orders of magnitude cheaper than what a naive approach would require. The key insight is that hash-based partitioning guarantees all occurrences of a given key land in the same partition, allowing each partition to be processed independently and the partial results trivially concatenated.

## B+Tree Structures for Massive Data

Another approach to massive data handling, as used in database systems like MySQL with the InnoDB storage engine, leverages B+Tree indexes:

- **Root and internal nodes** reside in memory, containing keys and child pointers.
- **Leaf nodes** reside on disk, containing the actual data (or pointers to data rows).
- A search traverses from root to leaf with **one I/O operation** at the leaf level.
- Due to **disk locality and read-ahead**, a single I/O fetches a contiguous range of data, not just a single record.

This structure enables efficient range queries (`WHERE id BETWEEN x AND y`) and ordered scans without loading the entire dataset into memory. The B+Tree's fan-out (high branching factor) minimizes tree depth, keeping the number of I/O operations per query extremely low -- typically 2 to 4 for tables with billions of rows.

The B+Tree approach complements the bitmap and divide-and-conquer patterns: B+Trees excel at indexed, random-access workloads, while the earlier patterns target batch, full-scan processing tasks.

---

**Further reading:** [Comprehensive Collection of Massive Data Processing Interview Questions](https://blog.csdn.net/v_july_v/article/details/6685962)
