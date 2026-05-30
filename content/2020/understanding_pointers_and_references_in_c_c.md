# Understanding Pointers and References in C/C++

> 2020-03-25

A deep dive into C pointers, C++ references, memory addressing, the compilation-stage symbol table, and the relationship between language abstractions and physical memory.

## Memory as a Hardware Abstraction

Memory is a one-dimensional linear array of M consecutive byte-sized units. Each byte has a unique **physical address**. The CPU's natural access mode is **physical addressing**. Data types larger than one byte are stored across contiguous addresses but referenced by a single starting address.

Each memory location has:
- A unique address for indexing
- A value stored at that address

## C Pointers

A **pointer** is a variable that stores a memory address.

Key operators:

| Operator | Name | Purpose |
|---|---|---|
| `&` | Address-of | Returns the address of any variable |
| `*` | Indirection (dereference) | Declares a pointer type; accesses the value at the pointed-to address |

### `&` — Three Semantics in C/C++

1. **Bitwise AND** — `a & b`
2. **Address-of** — `&a` (get the address of `a`)
3. **Reference declaration** (C++ only) — `int &ref = a`

### Pointer Fundamentals

```c
int a = 999;
int *b = &a;    // b stores the address of a
*b = 0;         // Dereference: write 0 to the address stored in b
                // a is now 0

```

### Compilation Perspective

At compile time, the symbol table maps variable names to addresses. Pointers are resolved during linking via relocation entries.

- A pointer variable stores an unsigned integer (the memory address in hex)
- Declaration: `type *name`
- An uninitialized pointer holds a **random address** — never dereference before assigning
- `NULL` pointer: `int *p = 0;` or `int *p = NULL;` — explicitly points nowhere, cannot be dereferenced

### Pointer to Pointer

```c
char s = 'f';
char *p1 = &s;      // p1 → s ('f')
char **p2 = &p1;    // p2 → p1 → s ('f')

printf("%c\n", *p1);   // 'f'
printf("%c\n", **p2);  // 'f' (double dereference)

```

### Pointer Arithmetic

Pointers support arithmetic (`+`, `-`, `++`, `--`) and relational operations (`<`, `>`, `==`). Pointer arithmetic scales by the size of the pointed-to type.

## C++ References

A **reference** is an alias for an existing variable — not a separate object. Key differences from pointers:

| | Pointer | Reference |
|---|---|---|
| Can be null | Yes (`nullptr` / `NULL`) | No — must bind at declaration |
| Can be reassigned | Yes | No — bound for lifetime |
| Requires dereference syntax | `*p` | Transparent (automatic) |
| Has its own address | Yes (`&p` is distinct) | No (`&ref` == address of target) |

### C++11: `nullptr`

```cpp
int *p = nullptr;  // Preferred over NULL/0 in C++11+

```

Always initialize pointers — if the target isn't known yet, use `nullptr`.
