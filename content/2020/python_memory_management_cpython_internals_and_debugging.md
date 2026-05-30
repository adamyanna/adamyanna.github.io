# Python Memory Management: CPython Internals & Debugging

> 2020-03-25

Key investigation areas for CPython memory management, Tornado thread management, and low-level Python debugging with GCC/GDB.

## Research Questions

### 1. CPython Memory Management

How does CPython's memory allocator work under the hood? Key areas:
- `PyMem_Malloc` / `PyMem_Free` — Python's C-level memory API
- Reference counting and the generational garbage collector
- `ob_refcnt` field in `PyObject` — the foundation of CPython's memory lifecycle

### 2. Tornado Thread Management

How does Tornado's IOLoop interact with Python threads? Understanding `htop`-visible thread counts and GIL contention in async frameworks.

### 3. Python Memory Debugging

Tools and approaches:
- `tracemalloc` (Python 3.4+) — trace memory allocations per line
- `gc` module — `gc.get_objects()`, `gc.get_stats()`
- `objgraph` — visualize object references and leaks
- `gdb` with `python-debuginfo` — attach to live Python process

### 4. GCC Debug Toolchain

Compiling CPython with debug symbols and profiling hooks for memory analysis.
