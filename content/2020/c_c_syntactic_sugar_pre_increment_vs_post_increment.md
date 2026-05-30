# C/C++ Syntactic Sugar: Pre-Increment vs Post-Increment

> 2020-04-10

A minimal example illustrating the difference between `i++` and `++i` — one of the most fundamental pieces of C/C++ syntactic sugar.

## The Example

```cpp
#include <iostream>
using namespace std;

int main() {
    int a = 0;
    int b = (a++);
    cout << "a: " << a << ", b: " << b << endl;
    // Output: a: 1, b: 0

    a = 0;
    int c = (++a);
    cout << "a: " << a << ", c: " << c << endl;
    // Output: a: 1, c: 1
}

```

## Explanation

Both `a++` and `++a` increment `a` by 1. The difference lies in **what the expression itself evaluates to:**

| Expression | Value of expression | Value of `a` afterward |
|---|---|---|
| `b = a++` | `a` (the original value) | `a + 1` |
| `c = ++a` | `a + 1` (the incremented value) | `a + 1` |

- `a++` — the expression evaluates to the **original** `a`, then `a` is incremented (post-increment)
- `++a` — `a` is incremented **first**, and the expression evaluates to the new value (pre-increment)
