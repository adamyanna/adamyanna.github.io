# C Programming Language Recap

> 2020-03-16

A C language refresher covering compilation, types, storage classes, operators, control flow, pointers, structs, and the C11 standard -- as preparation for C++.

---

## C History and Design Goals

C is a general-purpose, high-level language designed for the **Unix** operating system, based on the earlier **B** language. It is structured, capable of low-level hardware manipulation, and standardized as **C11** (ISO).

---

## GCC Compilation Pipeline

GCC (GNU Compiler Collection) compiles C source to machine code through four stages:

```
Preprocessor (.c) -> Compiler (.i) -> Assembler (.s) -> Linker (executable)
```

GCC was originally written for the GNU operating system ("GNU's Not Unix!"). It includes front ends for C, C++, Objective-C, Fortran, Ada, Go, and D. Key packages: `gcc-core`, `gcc-g++`, `binutils` (`gcc`, `g++`, `ar`, `ranlib`, `dlltool`).

```bash
gcc xxx.c              # produces a.out
gcc x.c xx.c -o out    # multi-file, named output
```

**LLVM** provides an alternative compiler infrastructure with its Clang front end.

---

## C Program Structure

```
Preprocessor directives -> Global declarations -> main() -> Functions
```

```c
#include <stdio.h>       // preprocessor: include header

int main() {              // program entry point
    printf("%s\n", "hello");
    return 0;
}
```

---

## Tokens

| Token | Description |
|---|---|
| **Semicolon `;`** | Statement terminator |
| **Comments** | `//` single-line, `/* ... */` multi-line |
| **Identifiers** | Start with letter or underscore, then letters/digits/underscores. Case-sensitive. |
| **Keywords** | Reserved words (see keyword tables at end of document) |

---

## Data Types

### Integer Types

| Type | Size | Range |
|---|---|---|
| `char` | 1 byte | -128 to 127, or 0 to 255 |
| `unsigned char` | 1 byte | 0 to 255 |
| `signed char` | 1 byte | -128 to 127 |
| `int` | 2 or 4 bytes | platform-dependent |
| `unsigned int` | 2 or 4 bytes | 0 to 4,294,967,295 (max) |
| `short` | 2 bytes | -32,768 to 32,767 |
| `unsigned short` | 2 bytes | 0 to 65,535 |
| `long` | 4 or 8 bytes | platform-dependent (x86_64: 8 bytes) |
| `unsigned long` | 4 or 8 bytes | 0 to 4,294,967,295 or larger |

On modern x86_64 systems, `long` is 8 bytes -- sizes differ from the older i686 ABI.

### Floating-Point Types

| Type | Size | Precision | Range |
|---|---|---|---|
| `float` | 4 bytes | 6 digits | 1.2E-38 to 3.4E+38 |
| `double` | 8 bytes | 15 digits | 2.3E-308 to 1.7E+308 |
| `long double` | 16 bytes | 19 digits | 3.4E-4932 to 1.1E+4932 |

IEEE 754 layout: 1 sign bit + exponent bits + fraction bits (float: 8+23, double: 11+52).

### `sizeof` and `printf` Format Specifiers

`sizeof(type)` returns storage size in bytes. `printf` uses `%[flags][width][.precision][length]specifier`:

| Specifier | Meaning | Specifier | Meaning |
|---|---|---|---|
| `%d` / `%u` | Signed / unsigned decimal int | `%f` / `%e` | Float / scientific notation |
| `%c` / `%s` | Single char / string | `%p` | Pointer address |
| `%x` / `%X` | Hex | `%o` | Octal |
| `%lu` / `%llu` | Unsigned long / long long | | |

### Type Categories

1. **Basic types** -- integer and floating-point arithmetic types
2. **Enumeration types** -- discrete integer-valued variables
3. **Void type** -- absence of value: empty returns, empty parameter lists (`int f(void)`), generic pointers (`void *`)
4. **Derived types** -- pointer, array, structure, union, and function types (arrays + structs are **aggregate types**)

---

## Variables: Definition vs. Declaration

- **Definition** allocates storage: `int a;`
- **Declaration** guarantees existence without allocation, via `extern`:
  ```c
  extern int a;   // declared here, defined in another file
  int b;          // both declared and defined
  ```

**Lvalue**: expression pointing to a memory location (can appear either side of `=`). **Rvalue**: a stored value (right side only).

---

## Constants

**Integer**: `0x`/`0X` = hex, `0` = octal, no prefix = decimal. Suffixes: `U` (unsigned), `L` (long).

**Floating-point**: decimal (`3.14`) or exponential (`3.14e0`) form.

**Character**: single-quoted, e.g. `'A'` (ASCII 65). Escape sequences: `\n` (newline), `\t` (tab), `\r` (CR), `\\` (backslash), `\'` (single quote), `\"` (double quote), `\0` (null), `\xhh` (hex), `\ooo` (octal).

**String**: double-quoted, auto-null-terminated with `'\0'`.

```c
#define TIMEOUT 30            // preprocessor macro
const int timeout = 30;       // typed constant (convention: UPPER_CASE)
```

---

## Storage Classes

Define **scope** (visibility) and **lifetime**. Precede the type specifier.

### `auto`
Default for local variables; block-scoped. `{ auto int m; }` is equivalent to `{ int m; }`.

### `register`
Hints for CPU register storage. Max size = one word. Cannot apply `&`. Common for counters; compiler may ignore.

### `static`
- **Local**: retains its value across function calls (initialized once, survives for program lifetime)
- **Global**: limits scope to the declaring file

```c
static int global_n = 999;

void fn(void) {
    static int t = 0;   // initialized once, persists across calls
    t++;
    printf("%d %d\n", t, global_n);
}
```

### `extern`
References a global variable or function defined in another file. Does not allocate storage.

```c
// file1.c                           // file2.c
int count;                           extern int count;   // references file1.c
extern void helper(void);            void helper(void) { ... }
```

---

## Operators

### Categories

| Category | Operators |
|---|---|
| Arithmetic | `+` `-` `*` `/` `%` `++` `--` |
| Relational | `==` `!=` `>` `<` `>=` `<=` |
| Logical | `&&` (AND), `\|\|` (OR), `!` (NOT) |
| Bitwise | `&` (AND), `\|` (OR), `^` (XOR), `~` (NOT), `<<` (left shift), `>>` (right shift) |
| Assignment | `=` `+=` `-=` `*=` `/=` `%=` `<<=` `>>=` `&=` `^=` `\|=` |
| Misc | `sizeof()`, `&` (address-of), `*` (dereference), `?:` (ternary: `cond ? a : b`) |

**Two's complement**: negative integers are stored as one's complement + 1. Bitwise ops reflect this.

### Operator Precedence (high to low)

| Category | Operators | Assoc. |
|---|---|---|
| Postfix | `()` `[]` `->` `.` `++` `--` | L->R |
| Unary | `+` `-` `!` `~` `++` `--` `(type)` `*` `&` `sizeof` | R->L |
| Multiplicative | `*` `/` `%` | L->R |
| Additive | `+` `-` | L->R |
| Shift | `<<` `>>` | L->R |
| Relational | `<` `<=` `>` `>=` | L->R |
| Equality | `==` `!=` | L->R |
| Bitwise AND / XOR / OR | `&` / `^` / `\|` | L->R |
| Logical AND / OR | `&&` / `\|\|` | L->R |
| Conditional | `?:` | R->L |
| Assignment | `=` `+=` `-=` ... | R->L |
| Comma | `,` | L->R |

---

## Control Flow

```c
// conditional
if (x > 0) { ... } else if (x < 0) { ... } else { ... }
int m = (x > y) ? x : y;

// switch (expression must be an integer)
switch (n) {
    case 1: /* ... */ break;
    default: /* ... */
}

// loops
while (cond) { ... }
do { ... } while (cond);
for (int i = 0; i < n; i++) { ... }

// flow
break;         // exit loop
continue;      // next iteration
goto label;    // unconditional jump (use sparingly)
```

---

## Functions

```c
return_type function_name(parameter_list) { /* body */ return val; }
```

- **Parameter**: formal variable in the definition. **Argument**: actual value passed at the call.
- C uses **call by value**: arguments are copied; the original is untouched.
- **Call by reference** is achieved by passing a pointer:

```c
void by_val(int x)  { x = 10; }      // original unchanged
void by_ref(int *x) { *x = 10; }     // original modified
```

---

## Scope Rules and Initialization

- **Local**: variables inside a block, accessible only there; **not** auto-initialized
- **Global**: variables outside all functions, survive for program lifetime; **auto-initialized** to 0 / `'\0'` / NULL
- **Formal parameters**: treated as local variables

---

## Arrays

```c
int a1[] = {1, 2, 3};          // size inferred
int a2[5] = {1, 3};            // remaining = 0
int m[3][3] = {{1,2,3},{4,5,6},{7,8,9}};
```

The array name is a pointer to the first element: `double *p = arr;` means `p == &arr[0]`. Pointer arithmetic: `*(arr + 4)` equals `arr[4]`.

**Passing arrays to functions**: `void f(int *arr)`, `void f(int arr[10])`, `void f(int arr[])` are all equivalent. Return: `int *f(void) { ... }`.

---

## Enumerations

Compile-time integer constants -- reside in the code section, so `&` cannot be applied.

```c
enum WEEK { MON=1, TUE, WED, THU, FRI, SAT, SUN };   // type only
enum WEEK { MON=1, TUE, WED, THU, FRI, SAT, SUN } w; // type + variable
enum { MON=1, TUE, WED, THU, FRI, SAT, SUN } w;      // variable only

for (enum WEEK d = MON; d <= SUN; d++)
    printf("%d\n", d);
```

First member defaults to 0; each subsequent member increments by 1. Member names are global constants and cannot be reused or assigned to.

---

## Pointers and Function Pointers

```c
int x = 10;
int *p = &x;         // p holds the address of x
*p = 20;             // dereference: x becomes 20
```

**Function pointers** store a function's address and enable **callbacks** -- passing a function pointer as an argument so the callee can invoke it when a condition is met:

```c
typedef int (*op)(int, int);            // function-pointer type
int (*fn_ptr)(int) = &another_func;     // assign

void for_each(int *arr, int len, void (*cb)(int)) {
    for (int i = 0; i < len; i++) cb(arr[i]);
}
```

---

## Strings

Null-terminated character arrays:

```c
char s[] = "hello";                      // compiler appends '\0'
char s[] = {'h','e','l','l','o','\0'};  // equivalent
```

| Function | Purpose |
|---|---|
| `strcpy(s1, s2)` | Copy s2 into s1 |
| `strcat(s1, s2)` | Concatenate s2 onto s1 |
| `strlen(s1)` | Length of s1 |
| `strcmp(s1, s2)` | Compare: 0 if equal, <0 if s1<s2, >0 if s1>s2 |
| `strchr(s1, ch)` | Pointer to first occurrence of `ch` |
| `strstr(s1, s2)` | Pointer to first occurrence of s2 |

---

## Structures

Groups members of different types. `tag`, `member-list`, `variable-list`: at least 2 of 3 required.

```c
struct Tag { int a; char b; double c; } var_list;

// Variants
struct { int a; char b; } s1;             // anonymous
struct SIMPLE { int a; char b; };          // tag only -- declare later
struct SIMPLE t1, t2[10], *t3;
typedef struct { int a; char b; } Simple2; // typedef
Simple2 s;
```

- **Member access**: `s.a` (dot), `ptr->a` (arrow for pointer-to-struct)
- Structs can contain other structs and self-referential pointers (lists, trees)
- For mutually recursive structs, use an incomplete declaration

### Bit Fields

Pack named bit-level fields within a word. Fields cannot span byte boundaries (max 8 bits each). Unnamed fields act as padding.

```c
struct BF { int a:8; int b:4; int c:4; } data;  // 16 bits total
data.a = 1;   // access by field name
```

Used for hardware flags, packing booleans, and parsing non-standard binary formats.

---

## Unions

A `union` lets different types share the same memory. Only one member holds a valid value at a time; size equals that of the largest member.

```c
union Data { int i; float f; char str[20]; } d;
d.i = 42;       // valid
d.f = 3.14;     // now f is valid, i is overwritten
```

Member access uses `.` or `->`.

---

## C Keywords by Category

### Storage and Type
`auto` `register` `static` `extern` `const` `volatile`
`void` `char` `int` `float` `double` `short` `long` `signed` `unsigned`
`enum` `struct` `union` `typedef`

### Control Flow
`if` `else` `switch` `case` `default` `for` `while` `do`
`break` `continue` `goto` `return`

### C11 Additions

| Keyword | Purpose |
|---|---|
| `_Bool` | Boolean type |
| `_Complex` | Complex numbers (`float _Complex`, `double _Complex`, `long double _Complex`) |
| `_Imaginary` | Imaginary number type |
| `inline` | Hint to inline the function body |
| `restrict` | Pointer aliasing guarantee (optimization hint) |
| `_Alignof` | Query type alignment |
| `_Atomic` | Atomic type for lock-free concurrent access |
| `_Generic` | Compile-time dispatch on type |
| `_Noreturn` | Function does not return |
| `_Static_assert` | Compile-time assertion |
| `_Thread_local` | Thread-local storage duration |

---

## References

- [GCC](https://gcc.gnu.org/) -- GNU Compiler Collection
- [GCC Mirror (GitHub)](https://github.com/gcc-mirror/gcc)
- [GNU Make Manual](https://www.gnu.org/software/make/manual/make.html)
- [LLVM](https://llvm.org/) -- compiler infrastructure with Clang
