# CPython Internals: Virtual Machine & Source Code Analysis

> 2020-04-13

A walkthrough of the CPython interpreter from source tree to bytecode execution, tracing the full compilation pipeline, the structure of code and frame objects, the evaluation loop, the thread state model, and the mechanics of the Global Interpreter Lock. Based on the CPython v3.8 and v2.7 source trees.

## What CPython Is

CPython is the reference implementation of the Python language — it is, broadly, **a program that executes programs**. Unlike a statically compiled language such as C, CPython does not produce a standalone machine-code binary. Instead it compiles Python source to an internal bytecode representation and executes it on a stack-based virtual machine.

To ground the discussion, recall the C program lifecycle:

```
Source → Preprocessor → Compiler → Assembler → Linker → ELF Binary
                                                          ↓
                                               fork() + execve()
                                               → task_struct in kernel
                                               → .init entry point called
```

The ELF binary contains machine code sections, format strings, jump tables, global/static variables, symbol tables, and debug information — all mapped into the process's virtual address space by the loader.

Python's lifecycle has three distinct phases instead:

1. **Initialization** — Allocate and initialize interpreter state, thread state, and runtime data structures (skipped in interactive mode)
2. **Compilation** — Parse `.py` source into an AST, build a symbol table, generate code objects
3. **Interpretation** — Execute bytecode instructions from code objects on the evaluation stack

## CPython Source Tree

Before tracing the execution path, here is a map of the CPython source repository:

| Directory | Purpose |
|---|---|
| `Doc/` | Official documentation source (published at docs.python.org) |
| `Grammar/` | EBNF grammar file for the Python language |
| `Include/` | Interpreter-wide C header files |
| `Lib/` | Standard library modules implemented in pure Python |
| `Mac/` | macOS-specific code (e.g., IDLE as an OS X application) |
| `Misc/` | Developer documentation and miscellaneous artifacts |
| `Modules/` | Standard library modules implemented in C |
| `Objects/` | C implementations of all built-in types (int, list, dict, etc.) |
| `PC/` | Windows-specific source code |
| `PCbuild/` | MSVC build files for the official Windows installers |
| `Parser/` | Parser implementation and AST node definitions |
| `Programs/` | C entry point executables, including the `main` function (pre-3.5 these lived in `Modules/`) |
| `Python/` | Core runtime: compiler, eval loop, built-in modules |
| `Tools/` | Maintenance and developer tooling |

## The Compilation Pipeline

The transformation from a `.py` source file to an executable code object passes through five stages:

```
Python source (.py)
       │
       ▼
  Parse tree           — tokenized and structured by the parser
       │
       ▼
  AST                   — abstract syntax tree generated from the parse tree
       │
       ▼
  Symbol table          — name resolution, scope analysis
       │
       ▼
  Control flow graph    — basic blocks and control flow edges
       │
       ▼
  Code object           — PyCodeObject, the VM-executable unit
```

Each Python source file is composed of code blocks: modules, function definitions, class definitions, and so on. The entire compilation process produces one code object per code block.

### Stage 1: Parse Tree

The parser (driven by the EBNF grammar in `Grammar/`) reads the source file and produces a concrete parse tree. This is a direct structural representation of the source text, preserving every token.

### Stage 2: Abstract Syntax Tree (AST)

The parse tree is converted into an AST — a higher-level representation that discards syntactic noise (commas, parentheses, colons) and captures semantic structure. The AST node definitions live in `Parser/Python.asdl`. For example, a function definition becomes an `ast.FunctionDef` node with children for the name, arguments, decorator list, and body.

### Stage 3: Symbol Table

The symbol table pass walks the AST and resolves names to their scopes. It determines which variables are local, which are free (captured from an enclosing scope), and which are global. This information is embedded in the code object and drives the `LOAD_FAST` / `STORE_FAST` vs. `LOAD_GLOBAL` / `STORE_GLOBAL` bytecode instruction selection.

### Stage 4: Control Flow Graph (CFG)

The AST is lowered into a control flow graph — a set of basic blocks connected by edges representing jumps, branches, and exception handlers. The CFG representation makes it straightforward to compute stack depth, resolve jump targets, and optimize redundant operations before bytecode emission.

### Stage 5: Code Object Generation

The CFG is assembled into a `PyCodeObject`. This is the unit of execution for the virtual machine.

## PyCodeObject Structure

A `PyCodeObject` is a complex C structure (analogous to `PyObject` in the CPython type system) allocated on the heap via `PyMem_NEW(type, n)` → `PyMem_MALLOC`. Key fields include:

| Field | Purpose |
|---|---|
| `co_stacksize` | Maximum evaluation stack depth required |
| `co_flags` | Bit flags encoding properties (e.g., `CO_NOFREE`, `CO_GENERATOR`) |
| `co_code` | The raw bytecode instruction sequence (a `bytes` object) |
| `co_consts` | Tuple of constants referenced by the bytecode |
| `co_names` | Tuple of names (variables, attributes) used in the code |
| `co_varnames` | Tuple of local variable names |
| `co_freevars` | Tuple of free variable names (closure captures) |
| `co_cellvars` | Tuple of cell variable names (variables captured by nested scopes) |
| `co_filename` | Source file name |
| `co_name` | Name of the code block (e.g., function name, `<module>`) |
| `co_lnotab` | Line number table mapping bytecode offsets to source lines |
| `co_zombieframe` | Pointer used during frame deallocation |

Once the `PyCodeObject` is created, the interpreter is ready to execute it.

## CPython Startup: From `main` to Execution

### Entry Point

The entry point lives in `Programs/python.c`:

```c
/* Minimal main program -- everything is loaded from the library */
#include "Python.h"
#include "pycore_pylifecycle.h"

#ifdef MS_WINDOWS
int
wmain(int argc, wchar_t **argv)
{
    return Py_Main(argc, argv);
}
#else
int
main(int argc, char **argv)
{
    return Py_BytesMain(argc, argv);
}
#endif
```

On Linux, execution flows: `main` → `Py_BytesMain` → `pymain_main(&args)`.

### `pymain_main` — Init and Run

`pymain_main` performs two major steps:

1. **`pymain_init`** — Initialize the runtime:
   - `_PyRuntime_Initialize()` — set up the global runtime state
   - `Py_InitializeFromConfig(&config)` — configure the interpreter from command-line flags and environment variables
   - On success (`_PyStatus_OK()`), clear the config reference and return

2. **`Py_RunMain`** — Dispatch to the appropriate execution mode:
   - `pymain_run_command(config->run_command, &cf)` — execute a `-c` string
   - `pymain_run_module(config->run_module, 1)` — execute a `-m` module
   - `pymain_run_module(L"__main__", 0)` — execute `__main__`
   - `pymain_run_file(config, &cf)` — execute a `.py` file
   - `pymain_run_stdin(config, &cf)` — execute from standard input

### File Execution Path

For `pymain_run_file`, the code path is:
- `PySys_Audit` — security audit check on the file
- `_Py_wfopen` — open the file with encoding detection
- `PyUnicode_FromWideChar` / `PyUnicode_EncodeFSDefault` — normalize to Unicode
- `PyRun_AnyFileExFlags(fp, filename_str, 1, cf)` — begin execution

`PyRun_AnyFileExFlags` checks for a cached `.pyc` file:
- If a valid `.pyc` exists: `run_pyc_file(pyc_fp, filename, d, d, flags)`
- Otherwise: `PyRun_FileExFlags(fp, filename, Py_file_input, d, d, closeit, flags)`

The two critical calls inside `PyRun_FileExFlags` are:
- **`PyParser_ASTFromFileObject(fp, filename, NULL, start, 0, 0, flags, NULL, arena)`** — parse the source file into an AST
- **`run_mod(mod, filename, globals, locals, flags, arena)`** — compile the AST to bytecode and launch the bytecode interpreter

## Frame Objects

Before code execution begins, the interpreter creates a **frame object** (`PyFrameObject`) from the code object. A frame object holds:

- The namespaces needed for execution: **locals**, **globals**, and **builtins**
- A reference to the **current thread state**
- The **evaluation stack** for bytecode operand passing
- A **block stack** for managing loops, `try`/`except` blocks, and `with` statements
- The **instruction pointer** (analogous to `rip` in x86)
- Internal bookkeeping for exception handling and generator suspension

The concept parallels C's call stack: when a C function's arguments cannot all fit in registers, the compiler allocates a stack frame by adjusting `rsp`. Similarly, a `PyFrameObject` is created on the runtime stack when a code object begins execution, with space reserved for local variables (initially empty) and operands.

### Frame lifecycle:

```
┌─────────────────────────────┐
│ Code object (heap)          │
│   co_code, co_consts, ...   │
└──────────┬──────────────────┘
           │ interpreter creates
           ▼
┌─────────────────────────────┐
│ Frame object (stack)        │
│   locals, globals, builtins │
│   eval stack, block stack   │
│   instruction pointer       │
│   → owns ref to code object │
└──────────┬──────────────────┘
           │ function call creates
           ▼
┌─────────────────────────────┐
│ New Frame object            │  ← pushed onto frame stack
│   (for the called function) │
└─────────────────────────────┘
```

## The Evaluation Loop

The heart of CPython is `PyEval_EvalFrameEx`, often called the **eval loop**. It is an infinite loop that:

1. Fetches the next bytecode instruction (two bytes: opcode + argument)
2. Dispatches to the corresponding handler via a giant `switch` statement
3. The handler manipulates the evaluation stack, reads/writes namespaces, and may create new objects on the heap
4. Loops back to step 1

Conceptually (massively simplified):

```
while (1) {
    opcode = NEXTOP();       // fetch next opcode
    oparg  = NEXTARG();      // fetch argument

    switch (opcode) {
        case LOAD_FAST:      PUSH(locals[oparg]);       break;
        case STORE_FAST:     locals[oparg] = POP();     break;
        case LOAD_GLOBAL:    PUSH(globals[name]);       break;
        case BINARY_ADD:     w = POP(); v = POP();
                             result = PyNumber_Add(v, w);
                             PUSH(result);              break;
        case CALL_FUNCTION:  call_function(oparg);      break;
        case RETURN_VALUE:   retval = POP(); goto exit; break;
        // ... hundreds more opcodes
    }
}
```

Each handler performs its task and returns control to the loop. The instruction pointer advances, and processing continues until a `RETURN_VALUE` opcode is reached or an exception is raised.

Instructions like `BUILD_LIST`, `BUILD_MAP`, and `BUILD_CLASS` allocate new Python objects on the heap. For example, when `BUILD_MAP` executes, it allocates a new `PyDictObject` — a hash table using **open addressing** for collision resolution with a load-factor-driven resize policy.

## Bytecode Instructions

CPython has its own instruction set architecture. These are **not** x86 (or any CPU-native) instructions — they are opcodes defined by the CPython virtual machine. The mapping from opcode names to numeric values is defined in `Include/opcode.h`.

The bytecode stream (stored in `co_code`) is a sequence of two-byte pairs: `[opcode][argument]`. Instructions with the `HAVE_ARGUMENT` flag consume the argument byte; others ignore it. Extended arguments (`EXTENDED_ARG`) allow arguments larger than 255 by chaining.

Example disassembly of `x = a + b`:

```
LOAD_FAST    0    (a)      # push local a onto stack
LOAD_FAST    1    (b)      # push local b onto stack
BINARY_ADD                 # pop a, b; push a + b
STORE_FAST   2    (x)      # pop result; store in local x
```

This stack-machine model is the same paradigm used by the Java Virtual Machine and the .NET CLR.

## Thread State Model

### Thread State Structure

`PyThreadState` is a C structure encapsulating an executing thread's context:

- `next` / `prev` — linked list pointers connecting all thread states in creation order
- `interp` — pointer to the owning `PyInterpreterState`
- `frame` — pointer to the currently executing `PyFrameObject`
- `thread_id` — the OS-level thread identifier
- `curexc_type`, `curexc_value`, `curexc_traceback` — current exception state

### Interpreter State Structure

`PyInterpreterState` is a simpler structure:

- `*next` — links to the next interpreter state in the process
- `*tstate_head` — head of the linked list of thread states belonging to this interpreter
- Remaining fields are shared by all cooperating threads within the interpreter

### Relationship Model

```
┌──────────────────────────────────────────────┐
│ Python Process (single OS process)           │
│  ┌────────────────────────────────────────┐  │
│  │ InterpreterState (1 or more)           │  │
│  │  ┌──────────────────────────────────┐  │  │
│  │  │ ThreadState (1 or more per IS)   │  │  │
│  │  │   ↕ mapped to                    │  │  │
│  │  │ OS Thread (kernel control flow)  │  │  │
│  │  └──────────────────────────────────┘  │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

The mapping between a `ThreadState` and an OS thread is established when Python's `threading` module instantiates a new thread. At any moment, **only the thread holding the GIL may execute bytecode in the virtual machine**. Even if the OS scheduler picks a thread that does not hold the GIL, that thread must spin or block until the GIL is released.

## The Global Interpreter Lock (GIL)

### Why the GIL Exists

The GIL is a deliberate design simplification, not an oversight:

1. **Reference counting** — Every `PyObject` carries a reference count (`ob_refcnt`). Without the GIL, every increment and decrement would require an atomic operation or a per-object lock, dramatically slowing down the common case. The GIL provides thread-safe reference counting at zero per-object overhead.

2. **C extension compatibility** — Much of CPython's standard library and third-party ecosystem relies on C extensions that are not thread-safe. The GIL ensures these extensions are never invoked concurrently without the author explicitly releasing the lock.

### GIL Implementation

The GIL is implemented with three primitives:

| Primitive | Type | Purpose |
|---|---|---|
| `gil_locked` | `bool` | Whether the GIL is currently held |
| `gil_mutex` | mutex | Protects access to `gil_locked` (held very briefly) |
| `gil_cond` | condition variable | Signals threads waiting for the GIL |

### GIL Behavior in the Eval Loop

Within `PyEval_EvalFrameEx`:

1. An internal flag `gil_drop_request` is checked on every iteration
2. After a configurable microsecond interval (set via `sys.setswitchinterval()`), `gil_drop_request` is set by a timer
3. The current thread detects the flag, voluntarily releases the GIL, and signals `gil_cond`
4. A waiting thread acquires the GIL and resumes execution

An additional flag, `eval_breaker`, ORs together multiple conditions (`gil_drop_request`, pending signals, pending calls, async exceptions) for a single efficient check per iteration.

### GIL Release Protocol

When a thread releases the GIL and `gil_drop_request` is set, the thread ensures another waiting thread actually gets scheduled. It does this by waiting on a condition variable (`switch_cond`) until `gil_last_holder` changes to a value other than its own thread state pointer. This prevents **latch-stealing** on multi-core machines, where the releasing thread speculatively reacquires the GIL before any other thread has a chance, making time slices effectively much longer than intended.

## Heap Management and Object Allocation

All Python objects (`PyObject` subclasses) are allocated on the heap. Each built-in type has a corresponding C implementation in `Objects/`:

- `dict` — a hash table using open addressing with collision resolution; resizes based on a load factor
- `list` — a dynamic array with overallocation for amortized O(1) append
- `str` — a compact string representation with multiple internal layouts (1-byte, 2-byte, 4-byte per character)

The memory allocator hierarchy is:
1. Python's `pymalloc` (arena → pool → block, optimized for small objects ≤ 512 bytes)
2. C's `malloc` (for large objects)
3. The OS virtual memory manager (`mmap` / `sbrk`)

Global variables and other objects created during bytecode execution are allocated on the heap and tracked by the garbage collector (reference counting + cyclic GC for container objects).

## Static vs. Dynamic Allocation in Perspective

In C, the compiler can determine the size of global and static variables at compile time — these go into `.data` and `.bss` sections of the object file. The linker relocates them into the executable's data segment, and the loader maps them into the process's read-write memory region.

CPython cannot do this. The interpreter has no advance knowledge of how many code blocks the `.py` file contains, how large they are, or what data structures the program will create. Everything must be dynamically allocated. The interpreter uses:

- **Stack allocation** for frame objects and temporary values during evaluation (with a known upper bound from `co_stacksize`)
- **Heap allocation** for all Python objects, code objects, and interpreter/thread state structures

This is the fundamental difference: a C compiler bakes memory layout into the binary; CPython constructs it at runtime.

## Putting It All Together

A summary of the full lifecycle for a `.py` file execution:

1. **Startup** — `Programs/python.c:main` → `Py_BytesMain` → `pymain_main` → `pymain_init` (initialize runtime) → `Py_RunMain` → `pymain_run_file`
2. **Parse** — `PyParser_ASTFromFileObject` reads the source, tokenizes it, and builds an AST
3. **Compile** — `run_mod` converts the AST to a control flow graph and emits a `PyCodeObject` containing bytecode
4. **Create frame** — The interpreter allocates a `PyFrameObject` on the stack, linked to the code object and the current thread state
5. **Execute** — `PyEval_EvalFrameEx` enters the eval loop, fetching and dispatching bytecode instructions
6. **Manage heap** — Objects created during execution (lists, dicts, instances) are allocated on the heap and managed by the memory allocator and garbage collector
7. **Thread coordination** — If multiple threads exist, the GIL serializes bytecode execution; threads voluntarily yield at `sys.getswitchinterval()` boundaries

Every one of these stages contains deep implementation complexity. This article covers the architecture at the level needed to navigate the source code and understand how the layers fit together. For detailed explorations, the references below are excellent starting points.

## References

- [CPython Developer Guide — Setup](https://devguide.python.org/setup/)
- [CPython Developer Guide — Exploring](https://devguide.python.org/exploring/)
- [CPython Source Repository](https://github.com/python/cpython)
- [Inside the Python VM (Chinese)](https://nanguage.gitbook.io/inside-python-vm-cn/untitled)
- [Python's Innards — Yaniv Aknin](https://tech.blog.aknin.name/2010/04/02/pythons-innards-introduction/)
