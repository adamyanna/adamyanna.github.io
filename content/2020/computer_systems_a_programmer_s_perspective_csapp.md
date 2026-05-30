# Computer Systems: A Programmer's Perspective (CSAPP)

> 2020-03-27

Comprehensive study notes from Bryant & O'Hallaron's _CSAPP_ — how computer systems work from a programmer's viewpoint. The core methodology: **do it** — solve concrete problems on real systems. All code compiled with GCC and tested on Linux.

---

## Overview

CSAPP examines the full lifecycle of a program: how source code becomes an executing process, how data is represented in hardware, how the processor and memory hierarchy execute instructions, and how the operating system manages hardware resources. Each chapter builds a layer of the abstraction stack.

| Chapter | Topic |
|---|---|
| 1 | A Tour of Computer Systems |
| 2 | Representing and Manipulating Information |
| 3 | Machine-Level Representation of Programs |
| 4 | Processor Architecture |
| 5 | Optimizing Program Performance |
| 6 | The Memory Hierarchy |
| 7 | Linking |
| 8 | Exceptional Control Flow |
| 9 | Virtual Memory |
| 10 | System-Level I/O |
| 11 | Network Programming |
| 12 | Concurrent Programming |

---

## Chapter 1: A Tour of Computer Systems

### 1.1 Information = Bits + Context

A source file is a text file created by an editor. Its content — a source program — is fundamentally a sequence of bits, organized into bytes (8 bits each). In ASCII, each character maps to a unique integer: `a` = 97, `A` = 65. Files composed exclusively of ASCII characters are **text files**; all others are **binary files**.

A critical principle: **all information in a system** — disk files, memory contents, user data, network packets — is represented as a sequence of bits. What distinguishes a byte sequence as an integer, a floating-point number, or a machine instruction is **context**: the interpretation applied by the program reading those bytes.

Numeric machine representations are always **finite approximations** of real values.

### 1.2 The Compilation System

A C program undergoes four stages of translation, collectively called the **compilation system**:

```
hello.c  ──[Preprocessor (cpp)]──→ hello.i  (modified source, text)
hello.i  ──[Compiler (ccl)]──────→ hello.s  (assembly, text)
hello.s  ──[Assembler (as)]──────→ hello.o  (relocatable object, binary)
hello.o  ──[Linker (ld)]─────────→ hello    (executable object, binary)
```

**Preprocessing phase.** The C preprocessor (`cpp`) handles directives like `#include` by inserting header file contents directly into the source text. The output is a `.i` file — still human-readable text.

**Compilation phase.** The compiler (`ccl`) translates the `.i` file into `.s` — assembly language. Assembly provides a common output language across different high-level languages and compilers. Each line describes one low-level machine instruction in text form.

**Assembly phase.** The assembler (`as`) translates `.s` into machine-language instructions, packaging them as a **relocatable object program** — a binary `.o` file containing the instruction encoding of `main`.

**Linking phase.** The linker (`ld`) merges the program's object file with pre-compiled library object files (e.g., `printf.o` from the standard C library). The result is an **executable object file**, ready to be loaded into memory and executed.

The GCC compiler driver orchestrates all four phases. GNU (GNU's Not Unix) provides: Emacs editor, GCC compiler, GDB debugger, assembler, linker, and binary utilities.

### 1.3 Why Understand the Compilation System

Understanding how programs are compiled and executed helps in three areas:

- **Optimize performance** (Chapters 3, 5, 6): `switch` vs `if-else` efficiency, function call overhead, `while` vs `for`, pointer reference vs array indexing, loop sum in a local variable vs by-reference parameter.
- **Avoid linker errors** (Chapter 7): unresolved references, static vs global variables, duplicate global names across `.c` files, static vs dynamic libraries, library order on the command line.
- **Prevent security vulnerabilities**: buffer overflow (Chapter 3), stack frame exploitation.

### 1.4 Hardware Organization

A typical system consists of four components connected by buses:

#### 1. Bus
A collection of electrical conduits running through the entire system, carrying **information bytes** between components. Buses transfer fixed-size chunks called **words**. Word size is a fundamental system parameter: 4 bytes on 32-bit machines, 8 bytes on 64-bit machines.

#### 2. I/O Devices
Each I/O device connects to the I/O bus through a **controller** (chipset on the motherboard) or an **adapter** (card plugged into a slot). Both serve the same purpose: transferring information between the I/O bus and the I/O device.

#### 3. Main Memory
A temporary storage device implemented with **DRAM** (Dynamic Random Access Memory) chips. Logically organized as a one-dimensional linear array of bytes, each with a unique **physical address**. This is called **physical addressing**.

#### 4. Processor (CPU)
The engine that interprets and executes instructions stored in main memory. Key components:

| Component | Role |
|---|---|
| **Program Counter (PC)** | A register holding the memory address of the next instruction |
| **Register File** | Small storage device with multiple word-sized registers, each with a unique name |
| **ALU** (Arithmetic/Logic Unit) | Computes new data and address values |

The processor's execution model (defined by the **Instruction Set Architecture**, e.g., Intel or ARM) follows a strict sequential cycle:
1. Fetch: read instruction from memory at the address in PC
2. Decode: interpret the bits of the instruction
3. Execute: perform the operation indicated by the instruction
4. Update PC to point to the next instruction

Core CPU operations:
- **Load**: copy a byte or word from main memory into a register
- **Store**: copy a byte or word from a register to a main memory location
- **Operate**: copy two register values to the ALU, compute, store result back to a register
- **Jump**: extract a word from the instruction and copy it to the PC

The **ISA** (Instruction Set Architecture) describes the effect of each machine instruction (the abstraction, covered in Chapter 4). The **microarchitecture** is the processor's actual hardware implementation.

#### Running `./hello`

The shell reads the keystrokes into a register, then into memory. Upon pressing Enter, the shell executes a series of instructions to load the `hello` executable — using **Direct Memory Access (DMA)** to copy data from disk to main memory without passing through the processor. Once loaded, the processor executes `main`'s machine instructions, copying output bytes from main memory to the register file, then to the display device.

### 1.5 Caches

Systems spend enormous time moving information between locations: disk to main memory, main memory to registers, registers to the processing unit. **Cache memory** serves as a staging area for data the processor is likely to need soon.

| Cache Level | Technology | Size | Latency (relative) |
|---|---|---|---|
| L1 | SRAM | Tens of thousands of bytes | ~1x (register speed) |
| L2 | SRAM | Hundreds of thousands to millions of bytes | ~5x L1 |
| L3 | SRAM | Several megabytes | ~5-10x L2 (still 5-10x faster than main memory) |

The key insight: combine a large, slow memory with a small, fast cache, exploiting **locality** — the tendency of programs to access data and code in localized regions. By keeping frequently accessed data in cache, most memory operations complete at cache speed, improving performance by an order of magnitude.

### 1.6 The Memory Hierarchy

The memory hierarchy organizes storage devices by speed, cost, and capacity:

| Level | Storage | Role |
|---|---|---|
| L0 | Registers | Hold words from L1 cache |
| L1 | L1 Cache (SRAM) | Holds cache lines from L2 |
| L2 | L2 Cache (SRAM) | Holds cache lines from L3 |
| L3 | L3 Cache (SRAM) | Holds cache lines from main memory |
| L4 | Main Memory (DRAM) | Holds disk blocks from local disks |
| L5 | Local Secondary Storage (SSD/HDD) | Holds files from remote servers |
| L6 | Remote Secondary Storage (Distributed FS, Web) | |

The fundamental principle: **each level acts as a cache for the level below it**. Higher levels are faster but smaller; lower levels are larger but slower.

### 1.7 Operating System Abstractions

The operating system serves two purposes:
1. Protects hardware from misuse by runaway applications
2. Provides a uniform, simple interface to complex and diverse hardware

Three fundamental abstractions:

#### Processes
A **process** is the OS abstraction of a running program. Multiple processes can run **concurrently** — their instructions interleaved in time. On multi-core processors, they run in parallel.

**Context switching** is the mechanism: the OS saves the current process's state (PC, register file values, main memory contents) — its **context** — and restores the next process's context. The new process resumes exactly where it left off.

The **kernel** is the collection of code and data structures the OS uses to manage all processes. A process transitions into kernel mode via a **system call** — the only entry point from user mode to kernel mode.

#### Threads
A process can consist of multiple **threads** of execution, each running in the process's context and sharing the same code and global data. (Covered in detail in Chapter 12.)

#### Virtual Memory
Virtual memory gives each process the illusion of exclusive access to main memory. Every process sees the same uniform **virtual address space**:

| Region | Description |
|---|---|
| Kernel virtual memory | Reserved for the OS; invisible to user code |
| User stack | Created at runtime; grows and shrinks with function calls |
| Memory-mapped region for shared libraries | e.g., `printf`, math library |
| Runtime heap | Created by `malloc`; expands and contracts dynamically |
| Read/write data segment (.data, .bss) | Global and static variables |
| Read-only code segment (.init, .text, .rodata) | Program instructions |

The stack grows downward (from high addresses to low addresses). The heap grows upward. Between them lies the memory-mapped region for shared libraries.

#### Files
A **file** is simply a sequence of bytes. In Unix, **everything is a file**: disks, keyboards, displays, network adapters. All I/O is performed through a small set of Unix I/O system calls, giving applications a uniform view of every I/O device.

### 1.8 Network Communication

From a single system's perspective, the network is just another I/O device. The system copies bytes from main memory to the network adapter; data flows across the network to another machine; the receiving system copies incoming data into its main memory. Network programming is detailed in Chapter 11.

### 1.9 Key Themes

#### Amdahl's Law

When accelerating part of a system, the overall speedup depends on both how much that part is improved and its fraction of total execution time. To significantly speed up the entire system, you must improve the performance of a very large fraction of it.

```
S = 1 / ((1 - a) + a / k)
```

where `a` is the fraction of execution time affected by the improvement, and `k` is the speedup factor of that improvement.

#### Concurrency and Parallelism

- **Concurrency**: a system with multiple simultaneous activities.
- **Parallelism**: using concurrency to make a system run faster. Parallelism operates at multiple levels:

**Thread-Level Parallelism.** Built on the process abstraction. Multiple threads execute within a single process. **Hyperthreading** (simultaneous multi-threading) allows a single CPU core to execute multiple control flows — the CPU has multiple copies of the PC and register file, sharing other hardware like the floating-point unit. An 8-core hyperthreaded processor can execute up to 16 threads in parallel.

**Instruction-Level Parallelism.** Modern processors execute multiple instructions simultaneously through **pipelining** — dividing instruction execution into stages, with different stages of different instructions operating in parallel. **Superscalar** processors sustain execution rates faster than one instruction per clock cycle.

**SIMD (Single Instruction, Multiple Data).** A single instruction performs multiple operations in parallel. For example, one instruction adds 8 pairs of single-precision floats simultaneously. GCC supports SIMD through special vector data types.

---

## Chapter 2: Representing and Manipulating Information

Modern computers represent information using three encoding schemes:

| Encoding | Description | Properties |
|---|---|---|
| **Unsigned** | Traditional binary representation | Non-negative numbers; exact for a small range |
| **Two's Complement** | Signed integer representation | Positive, negative, and zero |
| **Floating Point** | IEEE 754; base-2 scientific notation | Wider range but **approximate**; not associative |

Key insights: integer arithmetic is exact over a limited range; floating-point arithmetic is approximate over a wider range. Overflow occurs when a result exceeds the representable range. Floating-point operations are **not associative** due to finite precision.

### 2.1 Information Storage

A **byte** (8 bits) is the smallest addressable unit of memory. Programs view memory as a massive byte array — **virtual memory**. Each byte has a unique **address**; the set of all addresses is the **virtual address space**.

A C pointer's value is always the virtual address of the first byte of some storage block. The C compiler associates type information with each pointer and generates different machine-level code based on that type — but the actual machine code contains **no type information**. Every program object is simply a block of bytes; every program is itself a sequence of bytes.

#### Hexadecimal Notation

A single byte ranges from `00000000` to `11111111` in binary, `0` to `255` in decimal, and `00` to `FF` in hexadecimal. Conversion between binary and hex: group bits into nibbles of 4. For powers of two (`x = 2^n`): write `n = i + 4j` where `0 <= i <= 3`; the hex representation is `2^i` followed by `j` zeros. Example: `2048 = 2^11`; `11 = 3 + 4*2`; hex = `0x800`.

#### Word Size

The **word size** is the nominal size of pointer data. It determines the maximum virtual address space: a `w`-bit machine can address `0` to `2^w - 1` bytes. 32-bit systems limit virtual memory to 4 GB; 64-bit systems theoretically support 16 EB. The "32-bit" or "64-bit" designation refers to how the program was **compiled**, not the hardware it runs on.

Fixed-width integer types (`int32_t`, `int64_t`, etc. from `<stdint.h>`) provide platform-independent sizes and are the best way to control data representation.

#### Byte Ordering (Endianness)

For multi-byte objects, the address is the **lowest** byte address. Two conventions exist for ordering bytes in memory:

| Convention | Rule | Example: `0x01234567` at address `0x100` |
|---|---|---|
| **Little Endian** | Least significant byte first | `0x100: 67, 0x101: 45, 0x102: 23, 0x103: 01` |
| **Big Endian** | Most significant byte first | `0x100: 01, 0x101: 23, 0x102: 45, 0x103: 67` |

Intel-compatible machines use **little endian**. Network protocols mandate a standard byte order to ensure interoperability — senders convert from their internal representation.

C allows viewing an object through a type different from its declared type using **casts** or **unions**. For example, `(unsigned char *) &x` treats an integer `x` as a sequence of bytes.

#### Boolean Algebra and Bit-Level Operations

C supports bitwise Boolean operations on any integer type:

| Operator | Meaning |
|---|---|
| `~` | NOT (one's complement) |
| `&` | AND |
| `\|` | OR |
| `^` | XOR (Exclusive OR) |

**Masking** is a fundamental technique: `x & 0xFF` extracts the least significant byte; `~0` generates an all-ones mask.

**Logical operators** (`&&`, `||`, `!`) treat any nonzero value as `TRUE` and evaluate to `0` or `1`. They differ from bitwise operators except when restricted to single-bit values.

#### Shift Operations

| Shift | Operator | Effect |
|---|---|---|
| Left | `x << k` | Shift left `k` bits; fill right with `k` zeros; discard high `k` bits |
| Logical Right | `x >> k` (unsigned) | Shift right `k` bits; fill left with `k` zeros |
| Arithmetic Right | `x >> k` (signed) | Shift right `k` bits; fill left with `k` copies of the sign bit |

Almost all compilers and machines use arithmetic right shifts for signed types and logical right shifts for unsigned types.

### 2.2 Integer Representation

#### Unsigned Encoding (B2U)

The function `B2U_w` maps a `w`-bit vector `[x_{w-1}, ..., x_0]` to an integer:

```
B2U_w(x) = sum(x_i * 2^i) for i = 0 to w-1
```

Range: `0` to `2^w - 1`. This is a bijection — every bit vector maps to a unique unsigned value, and vice versa.

#### Two's Complement Encoding (B2T)

The most significant bit carries **negative weight**:

```
B2T_w(x) = -x_{w-1} * 2^{w-1} + sum(x_i * 2^i) for i = 0 to w-2
```

Range: `-2^{w-1}` (TMin) to `2^{w-1} - 1` (TMax). The range is **asymmetric** — TMin has no positive counterpart. For `w = 4`: TMin = -8, TMax = 7.

To compute the two's complement negation: invert all bits and add 1.

#### Conversions Between Signed and Unsigned

C casts between signed and unsigned preserve the **bit pattern** — only the interpretation changes:

- Values in `[0, TMax_w]`: identical in both unsigned and two's complement.
- Negative values (two's complement) become large positive values (unsigned): `T2U_w(x) = x + 2^w`.
- Large unsigned values (> TMax) become negative: `U2T_w(u) = u - 2^w`.

**Critical pitfall**: C implicitly converts signed to unsigned in mixed expressions. `-1 < 0U` evaluates to **false** because `-1` is implicitly cast to the unsigned value `2^32 - 1`.

**Recommendation**: avoid unsigned types unless treating words as bit collections (flags, bitmaps). Java uses only signed integers precisely to sidestep this class of bugs.

#### Sign Extension and Truncation

**Extension** (converting to a wider type):
- Unsigned: zero extension (pad with zeros).
- Two's complement: sign extension (pad with copies of the sign bit). `B2T_w(x) = B2T_{w'}(x')` — the value is preserved.

**Truncation** (converting to a narrower type, dropping high `w-k` bits):
- Unsigned: `x mod 2^k`.
- Two's complement: first treat as unsigned truncation `(x mod 2^k)`, then apply `U2T_k`.

### 2.3 Integer Arithmetic

All integer arithmetic on fixed-width types is effectively **modular arithmetic** modulo `2^w`.

#### Unsigned Addition

```
x +_w^u y = x + y          if x + y < 2^w         (normal)
          = x + y - 2^w    if x + y >= 2^w        (overflow)
```

Overflow occurs when the result cannot fit in `w` bits. C does **not** signal overflow as an error. Detect it by checking if the sum is less than either operand.

#### Two's Complement Addition

The bit-level representation of two's complement addition is **identical** to unsigned addition — the same machine instruction serves both. The difference is in overflow detection:

| Condition | Result |
|---|---|
| `x > 0, y > 0, sum <= 0` | Positive overflow (subtract `2^w`) |
| `x < 0, y < 0, sum >= 0` | Negative overflow (add `2^w`) |

The additive inverse of `x` in two's complement: `-x` for `x > TMin_w`; `TMin_w` is its own inverse (since `TMin_w + TMin_w = -2^w + 2^w = 0 mod 2^w`).

#### Multiplication

Both unsigned and two's complement multiplication truncate the full `2w`-bit product to `w` bits. The bit-level representation is **identical** for both encodings:

```
x *_w^u y = (x * y) mod 2^w         (unsigned)
x *_w^t y = U2T_w((x * y) mod 2^w)  (two's complement)
```

#### Multiplying by Constants

Multiplication is typically more expensive (in clock cycles) than addition, subtraction, or bit-level operations. Compilers replace multiplication by constants with combinations of **shifts, additions, and subtractions**:

```
x * 14  →  (x << 3) + (x << 2) + (x << 1)    or    (x << 4) - (x << 1)
```

#### Dividing by Powers of Two

Integer division is even slower (30+ cycles on many machines). Division by powers of two uses **right shifts**:

- **Unsigned**: logical right shift. `x >> k` gives `floor(x / 2^k)`.
- **Two's complement** (non-negative): arithmetic right shift works identically to unsigned.
- **Two's complement** (negative): arithmetic right shift rounds **down** (toward -inf), but we want rounding **toward zero**. Fix with a **bias**: add `(1 << k) - 1` before shifting.

```c
(x < 0 ? x + (1 << k) - 1 : x) >> k   // divides x by 2^k, rounding toward zero
```

### 2.4 Floating Point

All computers follow the **IEEE 754** floating-point standard.

#### Binary Fractions

A binary fraction `b_m ... b_1 b_0 . b_{-1} ... b_{-n}` represents:

```
sum(b_i * 2^i)   for i = -n to m
```

Shifting the binary point left divides by 2; shifting right multiplies by 2. Only numbers of the form `x * 2^y` can be represented exactly — others are approximated. Increasing bit length improves precision.

#### IEEE 754 Representation

```
V = (-1)^s * M * 2^E
```

| Field | Bit Width (Single) | Bit Width (Double) | Description |
|---|---|---|---|
| `s` | 1 | 1 | Sign bit (0 = positive, 1 = negative) |
| `exp` | 8 | 11 | Encodes exponent E |
| `frac` | 23 | 52 | Encodes significand M |

Three cases based on the `exp` field:

**1. Normalized Values** (`exp` is neither all-0s nor all-1s):
- `E = e - Bias`, where `Bias = 2^{k-1} - 1` (127 for single, 1023 for double)
- `M = 1 + f`, where `f` is the fractional value `0.f_{n-1}...f_0`
- This provides the "implicit leading 1" for free — an extra bit of precision.

**2. Denormalized Values** (`exp` = all 0s):
- `E = 1 - Bias`, `M = f` (no implicit leading 1)
- Represent zero (both `exp` and `frac` are 0; sign bit gives +0 and -0)
- Represent numbers very close to zero (gradual underflow)

**3. Special Values** (`exp` = all 1s):
- `frac` = 0: infinity (+/- depending on sign bit). Represents overflow (e.g., `1.0 / 0.0`).
- `frac` != 0: **NaN** (Not a Number). Represents undefined results (e.g., `sqrt(-1)`, `inf - inf`).

#### Rounding

IEEE 754 specifies four rounding modes. The default is **round-to-even** (round-to-nearest), which avoids statistical bias in computations.

#### Floating-Point Arithmetic Properties

- **Commutative**: `x + y = y + x`, `x * y = y * x`
- **NOT associative**: `(x + y) + z != x + (y + z)` in general, due to rounding
- **Monotonic**: if `a >= b`, then `x + a >= x + b` (unless NaN is involved)

---

## Chapter 3: Machine-Level Programming (x86-64)

### The Programmer-Visible State

The x86-64 architecture exposes:

| Component | Description |
|---|---|
| **Program Counter** | `%rip` — address of next instruction |
| **Integer Register File** | 16 named 64-bit registers (`%rax`, `%rbx`, `%rcx`, `%rdx`, `%rsi`, `%rdi`, `%rbp`, `%rsp`, `%r8`–`%r15`) |
| **Condition Codes** | Status flags: CF (carry), ZF (zero), SF (sign), OF (overflow) |
| **Vector Registers** | SSE/AVX registers for floating-point and SIMD operations |

### Data Movement and Addressing

The `mov` family of instructions transfers data. Operand types:

- **Immediate**: constant value (`$0x1F`)
- **Register**: contents of a register (`%rax`)
- **Memory reference**: address computed from `Imm + R[base] + R[index] * Scale` (scale = 1, 2, 4, or 8)

| Instruction | Effect |
|---|---|
| `movq S, D` | Move 8 bytes from source to destination |
| `movl S, D` | Move 4 bytes |
| `pushq S` | Decrement `%rsp` by 8, store S at new `%rsp` |
| `popq D` | Load from `%rsp`, increment `%rsp` by 8 |

### Arithmetic and Logical Instructions

| Instruction | Effect |
|---|---|
| `addq S, D` | D = D + S |
| `subq S, D` | D = D - S |
| `imulq S, D` | D = D * S |
| `salq k, D` | D = D << k (left shift) |
| `sarq k, D` | D = D >> k (arithmetic right shift) |
| `andq S, D` | D = D & S |
| `xorq S, D` | D = D ^ S |

### Control Flow

**Condition codes** are set by arithmetic instructions and the `cmpq`/`testq` instructions. Conditional jumps inspect condition codes:

| Jump | Condition |
|---|---|
| `je` / `jz` | Equal / Zero |
| `jne` / `jnz` | Not equal / Not zero |
| `jg` | Greater (signed) |
| `jl` | Less (signed) |
| `ja` | Above (unsigned) |
| `jb` | Below (unsigned) |

Modern compilers often translate `if-else` into **conditional moves** (`cmov`) to avoid branch misprediction penalties.

### Procedures and the Stack

The **stack** is a region of memory managed with a last-in-first-out discipline. It grows toward lower addresses. `%rsp` points to the top of the stack. `pushq` and `popq` add and remove data.

A **stack frame** holds a procedure's saved registers, local variables, and argument build area. When procedure P calls Q:
1. P places arguments (beyond the first 6) on the stack
2. P executes `call Q`, which pushes the return address and jumps to Q
3. Q allocates its stack frame by decrementing `%rsp`
4. Q executes its body
5. Q restores `%rsp` and executes `ret`, popping the return address into `%rip`

The first six integer/pointer arguments pass through registers: `%rdi`, `%rsi`, `%rdx`, `%rcx`, `%r8`, `%r9`. The return value goes in `%rax`. **Callee-saved** registers (`%rbx`, `%rbp`, `%r12`–`%r15`) must be preserved across calls; **caller-saved** registers may be clobbered.

| Typical Stack Layout |
|---|
| Arguments 7+ (caller's frame) |
| Return address |
| Saved registers |
| Local variables |
| Argument build area (for calls this procedure makes) |
| `%rsp` -> |

### Buffer Overflow

C does not perform bounds checking on array accesses. When a procedure writes beyond the bounds of a stack-allocated buffer, it can corrupt the **return address** stored on the stack. Attackers exploit this by overwriting the return address to redirect execution to malicious code.

Defenses: stack canaries (a random value placed before the return address, checked before `ret`), address space layout randomization (ASLR), and non-executable stack segments (NX bit).

---

## Chapter 4: Processor Architecture

### The Y86-64 Instruction Set

CSAPP introduces a simplified instruction set, **Y86-64**, as a teaching model. It is a subset of x86-64 with a cleaner encoding. Instructions include: `halt`, `nop`, `rrmovq`, `irmovq`, `rmmovq`, `mrmovq`, `OPq` (add/sub/and/xor), `jXX` (jumps), `cmovXX` (conditional moves), `call`, `ret`, `pushq`, `popq`.

### Sequential Implementation (SEQ)

A non-pipelined processor processes one complete instruction at a time through six stages:

| Stage | Action |
|---|---|
| **Fetch** | Read instruction from memory using PC; compute next PC |
| **Decode** | Read register file operands |
| **Execute** | ALU computes result or effective address; set condition codes |
| **Memory** | Read from or write to data memory |
| **Write Back** | Write result to register file |
| **PC Update** | Set PC to the next instruction address |

### Pipelining

Pipelining increases throughput by overlapping the execution of multiple instructions. Each instruction still takes the same total latency, but the processor completes one instruction per clock cycle (ideally).

However, pipelining introduces **hazards**:

| Hazard Type | Cause | Resolution |
|---|---|---|
| **Data hazard** | Instruction depends on result of a prior instruction still in the pipeline | Forwarding (bypassing), stalling |
| **Control hazard** | Next instruction address unknown until a branch/jump resolves | Branch prediction, stalling |

The **PIPE** implementation adds pipeline registers between stages and forwarding paths to resolve data hazards without stalling whenever possible. Load-use hazards (using a loaded value in the very next instruction) still require a one-cycle stall.

---

## Chapter 5: Optimizing Program Performance

The primary goal: write code that compilers can optimize effectively, and understand where manual optimization matters.

### Compiler Limitations

Compilers are conservative. They cannot apply optimizations that might change program behavior, including:
- Reordering floating-point operations (not associative)
- Eliminating function calls with side effects
- Optimizing across modules without whole-program analysis
- Optimizing through pointer aliasing (two pointers may reference the same memory)

### Key Optimization Techniques

- **Reduce procedure calls**: move repeated calls out of loops
- **Eliminate unnecessary memory references**: accumulate in registers, not memory
- **Exploit locality**: organize loops to access data sequentially in memory
- **Loop unrolling**: reduce loop overhead and expose instruction-level parallelism
- **Use SIMD**: process multiple data elements per instruction

### Performance Measurement

Modern processors are complex adaptive systems. Clock-cycle counting must account for: cache misses, branch mispredictions, instruction-level parallelism limits, and memory bandwidth constraints. Use cycle-accurate profiling tools.

---

## Chapter 6: The Memory Hierarchy

### 6.1 Storage Technologies

**SRAM** (Static RAM): fast, expensive, used for caches. Stores each bit in a bistable flip-flop cell. Does not need refresh. Access time: a few clock cycles.

**DRAM** (Dynamic RAM): slower, cheaper, used for main memory. Stores each bit as charge on a capacitor — leaks over time, must be refreshed periodically. Access time: tens to hundreds of cycles.

| Technology | Speed | Density | Cost | Usage |
|---|---|---|---|---|
| SRAM | Fastest | Lowest | Highest | L1/L2/L3 caches |
| DRAM | Moderate | Moderate | Moderate | Main memory |
| SSD/HDD | Slowest | Highest | Lowest | Persistent storage |

### 6.2 Locality

Locality is the principle that programs tend to reference data items that are:
- **Temporal locality**: recently referenced items are likely to be referenced again soon (e.g., loop induction variables).
- **Spatial locality**: items near recently referenced items are likely to be referenced soon (e.g., sequential array access, consecutive instructions).

Programs with **good locality** access most of their data from higher (faster) levels of the memory hierarchy. Programs with poor locality pay the penalty of frequent slower-level accesses.

**Stride** matters: accessing every `k`-th element of an array (`stride-k`) degrades spatial locality. Stride-1 access patterns maximize locality.

### 6.3 The Memory Hierarchy

The hierarchy is organized into **levels**, each acting as a cache for the level below:

```
Registers  ←  L1 Cache  ←  L2 Cache  ←  L3 Cache  ←  Main Memory  ←  Disk
(fastest)                                                              (slowest)
```

### 6.4 Cache Organization

A cache is organized as `(S, E, B, m)` where:
- `S = 2^s`: number of sets
- `E`: number of lines per set (associativity)
- `B = 2^b`: block size in bytes
- `m`: address width in bits
- Cache capacity: `C = S * E * B` (data only, excluding tags and valid bits)

An `m`-bit address is partitioned as:

```
| t (tag bits) | s (set index bits) | b (block offset bits) |
```

Cache lookup: use `s` to select the set, compare `t` against each line's tag in the set. If the valid bit is set and the tag matches: **cache hit**. Otherwise: **cache miss** — fetch the block from the next level, potentially evicting a victim block.

#### Cache Types by Associativity

| Type | E | Miss Rate | Hardware Complexity |
|---|---|---|---|
| **Direct-mapped** | 1 | Highest | Simplest |
| **Set-associative** | 2-8 | Moderate | Moderate |
| **Fully associative** | C/B | Lowest | Highest (impractical for large caches) |

#### Cache Misses

| Miss Type | Cause |
|---|---|
| **Cold (compulsory)** | First access to a block — inevitable |
| **Capacity** | Working set exceeds cache size |
| **Conflict** | Multiple blocks map to the same set (only in direct-mapped or low-associativity caches) |

#### Writing Strategies

| Strategy | Behavior |
|---|---|
| **Write-through** | Write to cache AND immediately to next level. Simple but slow. |
| **Write-back** | Write only to cache, defer write to next level until eviction. Uses a **dirty bit** per line. |

---

## Chapter 7: Linking

**Linking** is the process of collecting and combining code and data fragments into a single file, which can then be loaded into memory and executed. Linking occurs at three possible times:
1. **Compile time** — static linking
2. **Load time** — the loader links shared libraries when the program starts
3. **Run time** — the application invokes the dynamic linker explicitly

Linking enables **separate compilation**: large applications are decomposed into manageable modules, each compiled independently. Changing one module requires only recompiling that module and re-linking.

### The Compiler Driver

Invoking GCC runs the following sequence:
1. C preprocessor (`cpp`): `main.c` -> `main.i` (ASCII intermediate)
2. C compiler (`ccl`): `main.i` -> `main.s` (ASCII assembly)
3. Assembler (`as`): `main.s` -> `main.o` (relocatable object file)
4. Linker (`ld`): `main.o` + system object files -> executable

### Object File Formats

| Format | Platform |
|---|---|
| ELF (Executable and Linkable Format) | Linux, modern Unix |
| PE (Portable Executable) | Windows |
| Mach-O | macOS |

### Relocatable Object File (ELF)

An ELF relocatable object file contains multiple **sections** — contiguous byte sequences:

| Section | Contents |
|---|---|
| `.text` | Compiled machine code |
| `.rodata` | Read-only data (format strings, jump tables) |
| `.data` | **Initialized** global and static variables |
| `.bss` | **Uninitialized** and zero-initialized global/static variables (placeholder — no disk space) |
| `.symtab` | Symbol table: function and global variable definitions and references |
| `.rel.text` | Relocation entries for `.text` — code references that need address patching |
| `.rel.data` | Relocation entries for initialized data |
| `.debug` | Debugging symbols (present with `-g` flag) |
| `.line` | Line number to instruction address mapping (with `-g`) |
| `.strtab` | String table (symbol names, section names) |

Local (stack-allocated) variables do **not** appear in `.symtab`. They are managed at runtime on the stack.

### Symbols and Symbol Tables

Symbols are classified as:

| Type | Definition | Example |
|---|---|---|
| **Global** | Defined by module `m`, referenced by others | Non-static C functions, global variables |
| **External** | Defined by another module, referenced by `m` | `printf`, variables from other `.c` files |
| **Local** | Defined and referenced only within `m` | `static` functions, `static` global variables |

The `static` keyword in C serves as a visibility modifier: `static` functions and global variables are **private** to their module — analogous to `private` in C++/Java.

### Symbol Resolution and Relocation

The linker performs two main tasks:

1. **Symbol resolution**: associate each **symbol reference** with exactly one **symbol definition** from the input object files.

2. **Relocation**:
   - Merge same-type sections from all input modules into **aggregate sections**.
   - Assign runtime memory addresses to each section and each symbol.
   - Patch every symbol reference to point to its assigned runtime address, guided by **relocation entries** (`.rel.text`, `.rel.data`).

Relocation types:
- **PC-relative**: the reference is encoded as an offset from the current `%rip`. The linker computes: `target_address - (reference_address + offset_size)`.
- **Absolute**: the reference is a 32-bit absolute address; the linker fills in the target's runtime address directly.

### The Executable Object File

The final executable contains a contiguous binary image, organized into **segments** for efficient loading:

| Segment | Permissions | Sections |
|---|---|---|
| Code segment | Read + Execute | ELF header, program header table, `.init`, `.text`, `.rodata` |
| Data segment | Read + Write | `.data`, `.bss` |

The **program header table** describes how chunks of the file map to memory segments, including segment start addresses, sizes, and required alignment.

### Loading

The **loader** copies code and data from the executable file on disk into memory and jumps to the **entry point** (`_start`, which eventually calls `main`). Key details:
- Code segment starts at approximately `0x400000`.
- The heap follows the data segment and grows upward (`malloc`).
- The user stack starts near the maximum legal user address (`2^48 - 1` on 64-bit Linux) and grows downward.
- The kernel resides above the stack, invisible to user code.
- **ASLR** (Address Space Layout Randomization) randomizes stack, heap, and shared library addresses on each run to impede attacks.

During loading, the loader only copies **header information** from disk. Actual page data is fetched on demand via the virtual memory system.

### Static Libraries

A **static library** (`.a` archive file) packages related relocatable object modules into a single file. At link time, the linker copies only **referenced** modules into the executable. Static libraries eliminate the need to specify dozens of individual `.o` files.

### Dynamic Linking (Shared Libraries)

A **shared library** (`.so`) is an object module that can be loaded at any memory address and linked with a program at **load time** or **run time**. Advantages over static libraries:
- A single `.so` file serves all programs — no code duplication on disk or in memory.
- Multiple running processes share the same `.text` section in physical memory.
- Libraries can be updated independently of applications.

---

## Chapter 8: Exceptional Control Flow (ECF)

The processor's **control flow** is the sequence of PC values (instruction addresses). **Exceptional Control Flow** refers to abrupt changes in control flow that occur at all levels of a computer system:

| Level | ECF Mechanism |
|---|---|
| Hardware | Interrupts, traps, faults |
| Operating System | Context switches between processes |
| Application | Signals, nonlocal jumps (`setjmp`/`longjmp`) |

ECF is the fundamental mechanism the OS uses for I/O, process management, and virtual memory.

### 8.1 Exceptions

An **exception** is a transfer of control to the OS kernel in response to an **event** (a change in processor state). The processor uses an **exception table** (a jump table) to dispatch to the appropriate **exception handler**.

Exception classes:

| Class | Cause | Async/Sync | Return Behavior |
|---|---|---|---|
| **Interrupt** | Signal from I/O device | Async | Returns to next instruction |
| **Trap** | Intentional (system call) | Sync | Returns to next instruction |
| **Fault** | Potentially recoverable error | Sync | May return to current instruction (e.g., page fault) |
| **Abort** | Unrecoverable error | Sync | Never returns (halts program) |

**System calls** (e.g., `read`, `fork`, `execve`, `exit`) are implemented as traps. The `syscall` instruction triggers a trap; the handler decodes the system call number and dispatches to the appropriate kernel routine.

### 8.2 Processes

The OS provides the illusion that each program has exclusive use of the processor through **logical control flow** — interleaving execution of multiple processes via context switching.

Process lifecycle:
1. A parent process creates a child via `fork()`. The child is a (near) duplicate.
2. The child optionally calls `execve()` to replace its address space with a new program.
3. The parent may `wait()` for the child to terminate.
4. A process terminates via `exit()` or by returning from `main`.

### 8.3 Signals

Signals are a limited form of inter-process communication. A signal notifies a process that an event has occurred. The receiving process can: ignore the signal, terminate, or catch it with a user-defined **signal handler**.

---

## Chapter 9: Virtual Memory

Virtual memory provides three key capabilities:
1. **Caching**: uses main memory as a cache for disk storage — only actively used pages reside in memory.
2. **Memory management**: each process gets a uniform, private virtual address space.
3. **Memory protection**: page tables enforce read/write/execute permissions.

### Address Translation

The **Memory Management Unit (MMU)** translates virtual addresses to physical addresses using a **page table** stored in memory. Key concepts:

- Virtual address space is divided into fixed-size **pages** (typically 4 KB).
- Physical memory is divided into same-sized **page frames**.
- The page table maps virtual pages to physical page frames.
- A **Translation Lookaside Buffer (TLB)** caches recent translations inside the MMU.

A virtual address is split into: **VPN** (Virtual Page Number) + **VPO** (Virtual Page Offset). The VPN indexes the page table to find the **PPN** (Physical Page Number); the VPO becomes the **PPO** (Physical Page Offset) and is identical to the VPO.

### Multi-Level Page Tables

A single flat page table for a 64-bit address space would be impractically large. Hierarchical (multi-level) page tables reduce memory overhead by only allocating subtables for used regions of the virtual address space.

### Memory Mapping

Linux initializes process virtual memory by **mapping** regions to files on disk:
- The code segment maps to the executable file.
- Shared libraries map to `.so` files.
- Anonymous mappings (heap, stack) are backed by the **swap file**.

The `mmap()` system call creates new memory mappings programmatically.

### Page Faults

A **page fault** occurs when the MMU finds that a virtual page is not cached in physical memory (valid bit = 0 in the PTE). The OS page fault handler:
1. Selects a victim page frame (possibly writing it to disk if dirty).
2. Loads the requested page from disk into the freed frame.
3. Updates the page table entry and restarts the faulting instruction.

### Dynamic Memory Allocation

The heap is managed by an **allocator** (e.g., `malloc`/`free`). The allocator maintains the heap as a collection of blocks — some allocated, some free. Key challenges:
- Minimizing **internal fragmentation** (wasted space inside allocated blocks).
- Minimizing **external fragmentation** (free memory scattered in unusable small chunks).
- Balancing throughput and memory utilization.

Allocator strategies: implicit free lists, explicit free lists, segregated free lists. The buddy system and slab allocators are practical optimizations.

---

## Chapter 10: System-Level I/O

Unix I/O is based on the **file** abstraction. All I/O devices are modeled as files, accessed through a uniform interface:

| Operation | System Call | Description |
|---|---|---|
| Open | `open()` / `fopen()` | Open or create a file; returns a file descriptor |
| Close | `close()` / `fclose()` | Release the file descriptor |
| Read | `read()` / `fread()` | Copy bytes from file into memory |
| Write | `write()` / `fwrite()` | Copy bytes from memory to file |
| Seek | `lseek()` / `fseek()` | Change the current file position |

Key concepts:
- **File descriptor**: a small integer identifying an open file. `0` = stdin, `1` = stdout, `2` = stderr.
- **File position**: offset into the file where the next read/write occurs.
- The kernel maintains a **file table** shared across processes (after `fork`).
- Standard I/O (`stdio.h`) provides buffered wrappers around Unix I/O for efficiency.

---

## Chapter 11: Network Programming

The CSAPP network programming model builds on the **client-server** paradigm. Every network application is a pair: a server manages a resource; clients request access.

### The Sockets Interface

```c
// Server
int listenfd = socket(AF_INET, SOCK_STREAM, 0);   // Create socket
bind(listenfd, (struct sockaddr *)&addr, sizeof(addr));  // Bind to port
listen(listenfd, BACKLOG);                         // Listen for connections
int connfd = accept(listenfd, NULL, NULL);         // Accept client
// Use connfd for I/O...

// Client
int clientfd = socket(AF_INET, SOCK_STREAM, 0);
connect(clientfd, (struct sockaddr *)&addr, sizeof(addr));
// Use clientfd for I/O...
```

### HTTP

A miniature HTTP server is a capstone project. The protocol is text-based:
- Request: `GET /path HTTP/1.1\r\nHost: hostname\r\n\r\n`
- Response: `HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html>...</html>`

The server serves static content (files) and optionally dynamic content (CGI — Common Gateway Interface).

---

## Chapter 12: Concurrent Programming

Concurrent programming deals with applications that use multiple concurrent logical control flows. Approaches:

| Approach | Mechanism | Characteristics |
|---|---|---|
| **Process-based** | `fork()`, IPC | Separate address spaces; high overhead; robust isolation |
| **Event-based** | `select()`/`epoll()`, state machines | Single thread; no synchronization needed; complex control flow |
| **Thread-based** | POSIX threads (`pthread`) | Shared address space; lightweight; requires synchronization |

### Thread Synchronization

Shared data accessed by multiple threads must be protected from **race conditions** — program behavior depends on thread scheduling timing.

**Semaphores** (`sem_wait`, `sem_post`): integer counters supporting atomic decrement (P) and increment (V) operations. Used for:
- Mutual exclusion (binary semaphore / mutex)
- Signaling between threads
- Resource counting

Common pitfalls:
- **Deadlock**: threads wait for each other in a cycle (e.g., each holding one lock while waiting for another).
- **Starvation**: a thread never gets access to a shared resource.
- **Data races**: unsynchronized concurrent access to shared data.

The producer-consumer and readers-writers problems are classic synchronization exercises that illustrate these challenges.

### Thread-Safe Functions

A function is **thread-safe** if it produces correct results when called concurrently from multiple threads. Classes:
1. Not thread-safe (e.g., functions using static local variables).
2. Thread-safe but not reentrant (e.g., using mutexes — a signal handler calling them could deadlock).
3. Reentrant: no shared state; can be safely called from signal handlers.

---

## Study Roadmap

CSAPP rewards systematic study:

1. **Chapter 1**: Read for the big picture — the full program lifecycle.
2. **Chapters 2-3**: Core material. Work through the practice problems. Write small C programs and examine their disassembly (`objdump -d`).
3. **Chapters 4-5**: Understand pipelining conceptually; focus optimization efforts on real programs you maintain.
4. **Chapter 6**: Run `valgrind --tool=cachegrind` on your code to observe cache behavior. Rewrite loops to exploit spatial locality.
5. **Chapter 7**: Read `man ld`, `man elf`. Use `readelf`, `objdump`, `nm` to inspect your own binaries.
6. **Chapter 8-9**: Write a simple shell. Implement `malloc` and `free`. Understanding ECF and virtual memory transforms how you debug crashes and performance problems.
7. **Chapters 10-12**: Build the echo server, the HTTP server, and a concurrent version. This ties everything together: I/O, networking, threads, and synchronization all in one project.

---

*The text's home: [csapp.cs.cmu.edu](https://csapp.cs.cmu.edu/)*
