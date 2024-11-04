---
title: Python Regular Expression[re]
layout: default
parent: III. Experience
grand_parent: Engineering
---

**RegularExpression**
{: .label .label-red }

# Python Regular Expression[re]

| Syntax                                                      | Description                                                                       | Character        | Example             | Complete Matching Characters |
|-------------------------------------------------------------|-----------------------------------------------------------------------------------|------------------|---------------------|------------------------------|
| **General Characters**                                      |
| Character itself                                            | Matches the character itself (excluding newline `\n`).                            | `abc`            | `abc`               | `abc`                        |
| `.`                                                         | Matches any character except for newline (in DOTALL mode, matches any character). | `a.c`            | `abc`               | `abc`                        |
| `\`                                                         | Escapes a character, making it literal (e.g., `\(`, `\*`, etc.)                   | `a\\c`           | `a\c`               | `a\c`                        |
| `[...]`                                                     | Matches any character within brackets, can also represent ranges (e.g., `[a-z]`). | `a[bcd]e`        | `abe`, `ace`, `ade` | `abe`                        |
| `[^...]`                                                    | Matches any character *not* within brackets.                                      | `a[^bcd]e`       | `afe`, `ahe`        | `afe`                        |
| `\|`                                                        | Alternation, matches either the preceding or following part.                      | `abc\|def`       | `abc`, `def`        | `abc`                        |
| `( ... )`                                                   | Groups a part of the expression, creating a capture group.                        | `(abc)de`        | `abcde`             | `abc`                        |
| `(?: ... )`                                                 | Non-capturing group; groups without capturing.                                    | `(?:abc)de`      | `abcde`             | `abc`                        |
| **Predefined Character Classes (usable inside `[ ... ]`)**  |
| `\d`                                                        | Digits `[0-9]`                                                                    | `a\dc`           | `a1c`, `a2c`        | `a1c`                        |
| `\D`                                                        | Non-digits `[^0-9]`                                                               | `a\Dc`           | `abc`, `a-c`        | `abc`                        |
| `\s`                                                        | Whitespace characters `[ \t\r\n\f\v]`                                             | `a\sc`           | `a c`               | `a c`                        |
| `\S`                                                        | Non-whitespace characters `[^\s]`                                                 | `a\Sc`           | `abc`               | `abc`                        |
| `\w`                                                        | Word characters `[A-Za-z0-9_]`                                                    | `a\wc`           | `abc`, `a_c`        | `abc`                        |
| `\W`                                                        | Non-word characters `[^\w]`                                                       | `a\Wc`           | `a@c`               | `a@c`                        |
| **Quantifiers (used after characters or groups `( ... )`)** |
| `*`                                                         | Matches 0 or more occurrences of the preceding character.                         | `abc*`           | `abc`, `abcc`       | `abc`                        |
| `+`                                                         | Matches 1 or more occurrences of the preceding character.                         | `abc+`           | `abcc`              | `abcc`                       |
| `?`                                                         | Matches 0 or 1 occurrences of the preceding character.                            | `abc?`           | `abc`               | `abc`                        |
| `{m}`                                                       | Matches exactly m occurrences of the preceding character.                         | `ab{2}c`         | `abbc`              | `abbc`                       |
| `{m,n}`                                                     | Matches m to n occurrences of the preceding character.                            | `ab{1,2}c`       | `abc`, `abbc`       | `abc`                        |
| `{m,}?`                                                     | Lazy version of `{m,n}`, matches as few as possible.                              |                  |                     |                              |
| **Boundary Assertions (do not consume characters)**         |
| `^`                                                         | Matches the start of the string.                                                  | `^abc`           | `abc`               | `abc`                        |
| `$`                                                         | Matches the end of the string.                                                    | `abc$`           | `abc`               | `abc`                        |
| `\A`                                                        | Matches the start of the string.                                                  | `\Aabc`          | `abc`               | `abc`                        |
| `\Z`                                                        | Matches the end of the string.                                                    | `abc\Z`          | `abc`               | `abc`                        |
| `\b`                                                        | Word boundary                                                                     | `a\b\bc`         | `abc`               | `abc`                        |
| `\B`                                                        | Non-word boundary                                                                 | `a\Bbc`          | `abbc`              | `abc`                        |
| **Grouping and Capturing**                                  |
| `( ... )`                                                   | Capturing group                                                                   | `abc(def)`       | `def`               | `abc`                        |
| `(?: ... )`                                                 | Non-capturing group                                                               | `(?:abc)def`     | `def`               | `abc`                        |
| `(?P<name> ... )`                                           | Named capturing group                                                             | `(?P<id>abc)def` | `abc`               | `abc`                        |
| `(?P=name)`                                                 | Backreference to named group                                                      | `(?P=id)\d`      |