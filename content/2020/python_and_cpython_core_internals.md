# Python & CPython Core Internals

> 2020-04-26

A deep walkthrough of CPython internals: the object model, the evaluation loop (`ceval.c`), bytecode compilation and execution, memory management and garbage collection, the GIL, generators and coroutines, and the Python data model — targeting experienced developers who want to understand what happens after `python myscript.py`.

---

## I. The Python Object Model

### PyObject: Everything Is an Object

At the C level, every Python value is a `PyObject*`. The base struct is minimal:

```c
typedef struct _object {
    Py_ssize_t ob_refcnt;       // reference count
    PyTypeObject *ob_type;      // pointer to type object
} PyObject;
```

Every Python object — integers, strings, functions, classes, modules — begins with these two fields. The type pointer forms the backbone of dynamic dispatch: `obj->ob_type->tp_method` is how the interpreter resolves method calls. `PyTypeObject` extends this base, adding slots for every standard operation:

```c
typedef struct _typeobject {
    PyObject_VAR_HEAD                // ob_refcnt + ob_type + ob_size
    const char *tp_name;
    Py_ssize_t tp_basicsize, tp_itemsize;
    destructor tp_dealloc;
    printfunc tp_print;
    getattrfunc tp_getattr;
    setattrfunc tp_setattr;
    newfunc tp_new;
    initproc tp_init;
    allocfunc tp_alloc;
    // ... many more slots (repr, hash, call, iter, etc.)
} PyTypeObject;
```

`type` is itself an instance of `type` — the classic metaclass bootstrap. In CPython, `PyType_Type` is the metaclass for all built-in types; `type->ob_type == &PyType_Type` closes the circularity.

### Reference Counting

CPython uses reference counting as its primary memory strategy. Two macros govern object lifetimes:

```c
#define Py_INCREF(op)  ((op)->ob_refcnt++)
#define Py_DECREF(op)  if (--(op)->ob_refcnt != 0) ; else _Py_Dealloc(op)
```

When a new reference to an object is created (assignment, function call, appending to a list), `Py_INCREF` is called. When a reference goes out of scope, `Py_DECREF` decrements the count. At zero, `_Py_Dealloc` frees the object via the type's `tp_dealloc` slot.

A common pitfall is reference ownership. Functions returning a "**new reference**" (ob_refcnt already 1) transfer ownership to the caller. Functions returning a "**borrowed reference**" do not increment the count — the caller must `Py_INCREF` if it needs to hold on. CPython code relies on `Py_XINCREF`/`Py_XDECREF` (NULL-safe variants) and careful reference management to avoid use-after-free and leaks.

---

## II. Bytecode Compilation and Execution

### From Source to Bytecode

The compilation pipeline:

```
source.py → tokenizer → parser → AST → compiler → code object (bytecode)
```

1. **Tokenizer** (`Parser/tokenize.c`): Converts raw source into a token stream.
2. **Parser** (`Parser/parser.c`, PEG parser since 3.9): Builds a concrete syntax tree, then an abstract syntax tree (AST).
3. **Compiler** (`Python/compile.c`): Walks the AST and emits bytecode into a `PyCodeObject`.

The `compile()` built-in and `dis` module expose this pipeline:

```python
>>> def add(a, b): return a + b
...
>>> add.__code__.co_varnames, add.__code__.co_code
(('a', 'b'), b'|\x00|\x01\x17\x00S\x00')
>>> import dis; dis.dis(add)
  1           0 LOAD_FAST                0 (a)
              2 LOAD_FAST                1 (b)
              4 BINARY_ADD
              6 RETURN_VALUE
```

### Code Objects (`PyCodeObject`)

A code object is a frozen, immutable container of compiled code, defined as `PyCodeObject` with fields for argument counts (`co_argcount`, `co_kwonlyargcount`, `co_nlocals`, `co_stacksize`, `co_flags`), the bytecode bytes (`co_code`), tuples of constants, names, variable names, free/cell variables (`co_consts`, `co_names`, `co_varnames`, `co_freevars`, `co_cellvars`), and debug info (`co_filename`, `co_name`, `co_firstlineno`, `co_lnotab`/`co_linetable`).

### Bytecode Instruction Format

Each instruction is **16 bits** (2 bytes), stored in **little-endian**:

```
┌──────────┬──────────┐
│ OPARG    │ OPCODE   │
│ 8 bits   │ 8 bits   │
└──────────┴──────────┘
```

`EXTENDED_ARG` prefixes chain with the following instruction to form larger opargs. Since Python 3.6, wordcode uses 2-byte units for natural instruction alignment.

---

## III. Frame Objects and the Interpreter Loop

### Frame Objects (`PyFrameObject`)

A frame object (`PyFrameObject`) provides execution context: it holds a back-pointer to the caller (`f_back`), the code object being executed (`f_code`), builtins/globals/locals namespaces, an evaluation stack (`f_valuestack`, `f_stacktop`), and the current instruction and line numbers (`f_lasti`, `f_lineno`). Every function call allocates a frame, binds arguments, and pushes it onto the call stack.

The call chain from source to execution:

```
run_mod → PyEval_EvalCode → PyEval_EvalCodeEx
       → _PyEval_EvalCodeWithName → PyEval_EvalFrameEx
```

`_PyEval_EvalCodeWithName` creates the frame, binds keyword and positional arguments (`*args`, `**kwargs` stored as tuples) into `fastlocals`, checks for missing required args and duplicate kwargs, populates defaults, and initializes cell variables for closures.

### The Core Evaluation Loop (`Python/ceval.c`)

`PyEval_EvalFrameEx` is the main interpreter loop — a giant `for (;;)` switch dispatch processing one bytecode instruction per iteration. It uses **computed gotos** (GCC/Clang extension) as an optimization over plain `switch/case`, turning the dispatch table into an array of label addresses for direct jumps.

Key variables inside the loop:

| Variable | Role |
|---|---|
| `*stack_pointer` | Next free slot in the evaluation stack |
| `*next_instr` | Program counter — next bytecode instruction (analogous to `%rip` on x86-64) |
| `opcode`, `oparg` | Currently executing opcode and its argument |
| `why` | Loop exit reason: `WHY_RETURN`, `WHY_YIELD`, `WHY_EXCEPTION` |
| `fastlocals` | Array of local variables |
| `retval` | Holds the block's return value |
| `co` | The code object (bytecode + metadata) |
| `names`, `consts` | Names and constants referenced in the code block |

Key C macros:

| Macro | Expansion | Purpose |
|---|---|---|
| `TARGET(op)` | `case op:` | Dispatch entry — matches a specific opcode |
| `DISPATCH()` | `continue` | Proceed to next opcode |
| `FAST_DISPATCH()` | `goto fast_next_opcode` | Optimized dispatch — skips bounds/tracing checks on hot paths |
| `NEXTOPARG()` | — | Advances `next_instr`, sets `opcode`/`oparg` |
| `INSTR_OFFSET()` | — | Computes word offset in the instruction array |

A simplified sketch of the loop:

```c
PyObject* PyEval_EvalFrameEx(PyFrameObject *f, int throwflag) {
    for (;;) {
        switch (NEXTOPARG()) {
            TARGET(LOAD_FAST): {
                PyObject *v = GETLOCAL(oparg); Py_INCREF(v);
                PUSH(v); FAST_DISPATCH();
            }
            TARGET(BINARY_ADD): {
                PyObject *right = POP(), *left = TOP(), *res = PyNumber_Add(left, right);
                Py_DECREF(left); Py_DECREF(right);
                SET_TOP(res); DISPATCH();
            }
            TARGET(RETURN_VALUE):
                retval = POP(); why = WHY_RETURN; goto fast_block_end;
            // ... 100+ more opcodes ...
        }
    }
}
```

### The Specializing Adaptive Interpreter (Python 3.11+)

Python 3.11 introduced an adaptive specializing interpreter. When a bytecode instruction is executed repeatedly, the interpreter may replace it with a specialized version tailored to the observed types (e.g., `BINARY_ADD` becomes `BINARY_ADD_INT` if both operands are consistently `int`). Guard checks verify the type assumptions, and on mismatch the instruction is deoptimized back to the generic form. This is conceptually similar to inline caching in Smalltalk and hidden classes in V8.

---

## IV. Memory Management and Garbage Collection

### The Three-Layer Allocation Strategy

CPython's memory allocator (`Python/obmalloc.c`) has three tiers:

| Layer | Range | Mechanism |
|---|---|---|
| Layer 0 (raw) | > 256 KB | `malloc()`/`free()` directly from the OS |
| Layer 1 (pool) | 1–256 bytes | Arena-based pool allocator: 256 KB arenas subdivided into pools and blocks. Memory is never returned to the OS — held for reuse |
| Layer 2 (PyMem API) | All sizes | `PyMem_Malloc`/`PyMem_Free` — Python's internal API wrapping the layers below |

For small objects (the vast majority), the pool allocator avoids calling `malloc` for every `int` or list element.

### Generational Garbage Collection

Reference counting handles most deallocation but **cannot handle reference cycles** (e.g., `a.next = b; b.prev = a`). CPython supplements it with a generational GC (`Modules/gcmodule.c`):

| Generation | Description |
|---|---|
| Generation 0 | New objects — collected most frequently |
| Generation 1 | Objects that survived a gen-0 collection |
| Generation 2 | Oldest objects — collected least frequently |

A collection triggers when `(allocations - deallocations) > threshold[0]`. Default thresholds from `gc.get_threshold()` are `(700, 10, 10)`:

- Gen-0 collection runs when the allocation delta exceeds 700.
- Every 10 gen-0 collections triggers 1 gen-1 collection.
- Every 10 gen-1 collections triggers 1 gen-2 collection.

```python
import gc
gc.get_threshold()           # (700, 10, 10)
gc.set_threshold(1000, 5, 5) # custom thresholds
gc.collect()                 # force full collection (all generations)
gc.collect(generation=0)     # collect only gen-0
```

The GC traverses container objects (`tp_traverse` slot) to detect and break cycles. Immutable scalars (`int`, `str`, `float`) are not tracked — they cannot form cycles.

### Memory Optimizations

- **Small integer interning**: Integers from -5 to 256 are preallocated and shared. `a = 100; b = 100; a is b` is `True`.
- **String interning**: Identifiers and short strings are interned in a global dictionary. Compile-time identical string constants compare equal by identity.
- **Freelists**: `PyListObject`, `PyDictObject`, `PyFrameObject` reuse recently freed instances via bounded freelists, avoiding `malloc`/`free` churn.

---

## V. The Global Interpreter Lock (GIL)

### Purpose and Mechanism

The GIL is a mutex protecting CPython's internal state from concurrent access. Only the thread holding the GIL may execute Python bytecode. It lives inside `PyInterpreterState` as a condition-variable-based lock: waiting threads block on `gil_cond`, and the holder periodically releases it (every 15 ms by default, configurable via `sys.setswitchinterval()`) to let other threads acquire it.

### Why the GIL Exists

CPython's reference counting is not atomic. Without the GIL, two threads could simultaneously `Py_DECREF` the same object, causing double-free or use-after-free. Making every `INCREF`/`DECREF` atomic would be prohibitively expensive. The GIL trades CPU-bound parallelism for a simple memory model and excellent single-threaded performance.

### Release and Acquisition

```c
Py_BEGIN_ALLOW_THREADS
// ... blocking I/O (read(), select(), ...) — GIL released ...
Py_END_ALLOW_THREADS
```

These macros save the thread state, release the GIL, and restore it afterward. I/O-bound threads achieve concurrency because one thread can execute Python code while another is blocked in `read()`.

### Thread State and the GIL-Free Future

Each thread has a `PyThreadState` containing the interpreter state pointer, current frame, exception triple (`curexc_type`/`value`/`traceback`), recursion depth, and tracing flags. Thread states form a linked list off the interpreter state, allowing the GIL to be passed between threads.

PEP 703 (accepted for 3.13) and PEP 684 (per-interpreter GIL) lay the groundwork for optional GIL-free execution using biased reference counting and a stop-the-world cycle collector. This is an ongoing, multi-year effort.

---

## VI. Generators and Coroutines

### Generator Objects (`PyGenObject`)

Generators are the foundation of lazy iteration and async/await. The C struct uses the `_PyGenObject_HEAD(gi)` macro which expands to include a suspended `gi_frame` (`NULL` when exhausted), a `gi_running` boolean, the backing `gi_code`, name/qualname, and exception state.

### Suspension and Resumption

When a generator hits `yield`, the evaluation loop sets `why = WHY_YIELD` and returns control to the caller — but the frame object persists inside the generator, holding its execution stack, locals, and instruction pointer (`f_lasti`). This is what makes generators resumable.

Calling `next(gen)` triggers the iteration protocol:
1. `tp_iternext` resolves on the generator object.
2. `gen_iternext` calls `gen_send_ex(gen, Py_None, ...)`.
3. `gen_send_ex` re-enters `PyEval_EvalFrameEx` with the saved frame.
4. Execution resumes at the instruction after `YIELD_VALUE`.

### Sending Values

```python
def accumulator():
    total = 0
    while True:
        total += (yield total)

acc = accumulator()
next(acc)           # prime → 0
acc.send(10)        # → 10
acc.send(5)         # → 15
```

`send()` calls `gen_send_ex` which pushes the value onto the generator's evaluation stack as the "result" of the `yield` expression.

### Coroutines (Async/Await)

Coroutines extend the generator mechanism. They use the same `PyGenObject` struct but carry the `CO_COROUTINE` flag on their code object. `await` compiles to a `YIELD_FROM`-like bytecode; the event loop drives coroutine scheduling.

---

## VII. Python Data Model Internals

### Object Construction: `__new__` and `__init__`

When you write `MyClass(a, b)`, CPython calls `type.__call__` in `Objects/typeobject.c`:

```c
static PyObject *
type_call(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    PyObject *obj = type->tp_new(type, args, kwds);  // __new__
    if (obj != NULL && PyType_IsSubtype(Py_TYPE(obj), type))
        type->tp_init(obj, args, kwds);               // __init__
    return obj;
}
```

Key rules:
- `__new__` is a static method receiving the class; it returns a new (typically uninitialized) instance.
- `__init__` is called on the instance returned by `__new__` — but only if it is an instance of the class. If `__new__` returns something else, `__init__` is skipped.
- `__init__` must return `None`; any other return value raises `TypeError`.

### Metaclasses

A metaclass is a class whose instances are classes. `type` is the default metaclass. Custom metaclasses subclass `type`:

```python
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self, uri):
        self.uri = uri

db1 = Database("postgres://...")
db2 = Database("postgres://...")
assert db1 is db2  # same instance
```

When a class definition executes, CPython:
1. Resolves the metaclass (explicit `metaclass=` or inherited from bases).
2. Prepares the class namespace via `metaclass.__prepare__`.
3. Executes the class body in that namespace.
4. Calls `metaclass(name, bases, namespace)` to construct the class object.

### `__call__`, Callables, and Abstract Base Classes

Any object with a `tp_call` slot (defines `__call__`) is callable — functions, classes (their `tp_call` constructs instances), and custom objects. At the C level, `PyObject_Call` resolves `ob_type->tp_call`. ABCs override `__instancecheck__` and `__subclasscheck__` on `ABCMeta`; `isinstance(obj, MyABC)` invokes `MyABC.__instancecheck__(obj)`, enabling arbitrary interface conformance logic.

---

## VIII. Key Source Files

| File | Purpose |
|---|---|
| `Python/ceval.c` | Main evaluation loop |
| `Python/compile.c` | Bytecode compiler |
| `Objects/object.c` | Base `PyObject` implementation |
| `Objects/typeobject.c` | Type and metaclass implementation |
| `Objects/listobject.c`, `dictobject.c` | List and dict implementations |
| `Objects/genobject.c` | Generator and coroutine objects |
| `Objects/frameobject.c` | Frame object implementation |
| `Objects/unicodeobject.c`, `longobject.c` | String and arbitrary-precision int |
| `Python/pystate.c` | Interpreter and thread state management |
| `Modules/gcmodule.c` | Garbage collector |
| `Python/obmalloc.c` | Small-object memory allocator |

---

## IX. Key Takeaways

1. **Everything is a `PyObject*`** — the type system, reference counting, and dispatch all rest on the two-field header (`ob_refcnt` + `ob_type`).
2. **The evaluation loop is a giant `for(;;)` switch** — `ceval.c` dispatches 16-bit bytecode instructions via computed gotos. Python 3.11+ adds adaptive specialization for hot paths.
3. **Frames are the execution context** — every call pushes a `PyFrameObject` carrying its own stack, locals, and instruction pointer. Generators persist frames across `yield` suspension.
4. **Memory management is two-tier** — reference counting handles most deallocation; the generational GC handles cycles with configurable thresholds. A pool allocator minimizes `malloc` overhead for small objects.
5. **The GIL is a tradeoff** — it simplifies the memory model and enables excellent single-threaded performance, serializing CPU-bound Python threads. I/O-bound threads release the GIL during blocking calls.
6. **Generators are persisted frames** — `yield` saves the frame; `next()` / `send()` re-enter the evaluation loop at the saved instruction. Coroutines extend this with `await` and event-loop scheduling.
7. **There is no magic** — metaclasses, descriptors, `__new__`, `__call__`, and ABCs are all implemented through slot dispatch in `PyTypeObject`. Mastering the C structs demystifies the entire language.
