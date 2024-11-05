---
title: Python Regular Expression[re]
layout: default
parent: III. Experience
grand_parent: Engineering
---

**RegularExpression**
{: .label .label-red }

# Python Regular Expression[re]

## EN version

| Syntax                                                            | Description                                                                                          | Character                                                                           | Expression Example  | Full Match Example         |
|-------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|---------------------|----------------------------|
| **General Characters**                                            |                                                                                                      |                                                                                     |                     |
| Match itself                                                      | Matches the character itself                                                                         | `abc`                                                                               | `abc`               | `abc`                      |
| `.`                                                               | Matches any character except a newline `\n`. In DOTALL mode, it can also match newlines.             | `a.c`                                                                               | `a.c`               | `abc`                      |
| `\`                                                               | Escape character, makes the following character literal. Use `\` to match special characters.        | `a\.c`                                                                              | `a\.c`              | `a.c`                      |
| `[ ... ]`                                                         | Character set (character class). Matches any character in the set. Can specify characters or ranges. | `a[bcd]e`                                                                           | `a[bcd]e`           | `abe`, `ace`, `ade`        |
|                                                                   | Special characters lose their meaning in character sets. Escape `-`, `]`, `^` if needed.             | `[a-c]`                                                                             | `[^abc]`            | Any character except `abc` |
| **Predefined Character Sets** (can also be used within `[ ... ]`) |                                                                                                      |                                                                                     |                     |
| `\d`                                                              | Matches a digit `[0-9]`                                                                              | `a\dc`                                                                              | `a\dc`              | `a1c`, `a3c`               |
| `\D`                                                              | Matches a non-digit `[^0-9]`                                                                         | `a\Dc`                                                                              | `a\Dc`              | `abc`, `axc`               |
| `\s`                                                              | Matches a whitespace character `[ \t\r\n\f\v]`                                                       | `a\sc`                                                                              | `a\sc`              | `a c`, `a\tc`              |
| `\S`                                                              | Matches a non-whitespace character `[^ \t\r\n\f\v]`                                                  | `a\Sc`                                                                              | `a\Sc`              | `abc`, `axc`               |
| `\w`                                                              | Matches a word character `[A-Za-z0-9_]`                                                              | `a\wc`                                                                              | `a\wc`              | `abc`, `a1c`               |
| `\W`                                                              | Matches a non-word character `[^A-Za-z0-9_]`                                                         | `a\Wc`                                                                              | `a\Wc`              | `a@c`                      |
| **Quantifiers** (used after a character or `( ... )`)             |                                                                                                      |                                                                                     |                     |
| `*`                                                               | Matches the preceding character 0 or more times                                                      | `abc*`                                                                              | `abc*`              | `ab`, `abc`, `abcc`        |
| `+`                                                               | Matches the preceding character 1 or more times                                                      | `abc+`                                                                              | `abc+`              | `abc`, `abcc`              |
| `?`                                                               | Matches the preceding character 0 or 1 time                                                          | `abc?`                                                                              | `abc?`              | `ab`, `abc`                |
| `{m}`                                                             | Matches the preceding character exactly m times                                                      | `ab{2}c`                                                                            | `ab{2}c`            | `abbc`                     |
| `{m,n}`                                                           | Matches the preceding character between m and n times, inclusive                                     | `ab{1,2}c`                                                                          | `ab{1,2}c`          | `abc`, `abbc`              |
| `*? +? ??`                                                        | Makes `* + ? {m,n}` non-greedy                                                                       | `a.*?`                                                                              | See examples below  | Non-greedy match           |
| **Boundary Matchers** (do not consume characters in the string)   |                                                                                                      |                                                                                     |                     |
| `^`                                                               | Matches the beginning of the string. In multiline mode, matches the start of each line.              | `^abc`                                                                              | `^abc`              | `abc`                      |
| `$`                                                               | Matches the end of the string. In multiline mode, matches the end of each line.                      | `abc$`                                                                              | `abc$`              | `abc`                      |
| `\A`                                                              | Matches only at the start of the string                                                              | `\Aabc`                                                                             | `\Aabc`             | `abc`                      |
| `\Z`                                                              | Matches only at the end of the string                                                                | `abc\Z`                                                                             | `abc\Z`             | `abc`                      |
| `\b`                                                              | Matches a word boundary                                                                              | `\babc\b`                                                                           | `\babc\b`           | `abc`                      |
| `\B`                                                              | Matches a non-word boundary                                                                          | `a\Bbc`                                                                             | `a\Bbc`             | `a@bc`                     |
| **Logical and Grouping**                                          |                                                                                                      |                                                                                     |                     |
| `                                                                 | `                                                                                                    | Matches either the expression on the left or right. Left side is tried first.       | `abc                | def`                       | `abc|def`                     | `abc`, `def`               |
| `( ... )`                                                         | Groups expressions and assigns a number from 1 onwards for backreferences                            | `(abc){2}`                                                                          | `(abc){2}`          | `abcabc`                   |
| `(?P<name> ... )`                                                 | Named group, provides an additional name for backreferences                                          |                                                                                     |                     |                            |
| `\<number>`                                                       | Refers to the group with the given number in backreference                                           | `(\d)abc\1`                                                                         | `(\d)abc\1`         | `1abc1`                    |
| `(?P=name)`                                                       | Refers to the named group in backreference                                                           |                                                                                     |                     |                            |
| **Special Constructs** (not counted as a group)                   |                                                                                                      |                                                                                     |                     |
| `(?: ... )`                                                       | Non-capturing group                                                                                  |                                                                                     |                     |                            |
| `(?iLmsux)`                                                       | Mode modifiers to alter matching behavior, can specify multiple                                      | `(?i)abc`                                                                           | `(?i)abc`           | `Abc`, `ABC`               |
| `(?# ... )`                                                       | Inline comment, ignored by the regex engine                                                          | `abc(?#comment)123`                                                                 | `abc(?#comment)123` | `abc123`                   |
| `(?= ... )`                                                       | Positive lookahead, does not consume characters                                                      | `a(?=\d)`                                                                           | `a(?=\d)`           | `a1`, `a2`                 |
| `(?! ... )`                                                       | Negative lookahead, does not consume characters                                                      | `a(?!\d)`                                                                           | `a(?!\d)`           | `a`, `ab`                  |
| `(?<= ... )`                                                      | Positive lookbehind                                                                                  | `(?<=\d)a`                                                                          | `(?<=\d)a`          | `1a`, `2a`                 |
| `(?<! ... )`                                                      | Negative lookbehind                                                                                  | `(?<!\d)a`                                                                          | `(?<!\d)a`          | `a`                        |
| `(?(id/name)yes-pattern                                           | no-pattern)`                                                                                         | Conditional matching, matches `yes-pattern` if the group matches, else `no-pattern` | `(\d)abc(?(1)\d     | abc)`                      | `1abc1`, `abcabc`   | |

## CN version

| 语法                             | 说明                                           | 字符                                                  | 表达式实例           | 完整匹配的字符串            |
|--------------------------------|----------------------------------------------|-----------------------------------------------------|-----------------|---------------------|
| **一般字符**                       |                                              |                                                     |                 |                     |
| 匹配自身                           | 匹配自身字符                                       | `abc`                                               | `abc`           | `abc`               |
| `.`                            | 匹配任意除换行符`\n`外的字符。在DOTALL模式中也能匹配换行符。          | `a.c`                                               | `a.c`           | `abc`               |
| `\`                            | 转义字符，使后一个字符恢复原意。如字符串中有特殊字符要匹配时，可用 `\` 转义     | `a\.c`                                              | `a\.c`          | `a.c`               |
| `[ ... ]`                      | 字符集（字符类），对应位置可以是字符集中任意字符。字符集可以列出字符或用范围表示。    | `a[bcd]e`                                           | `a[bcd]e`       | `abe`, `ace`, `ade` |
|                                | 特殊字符在字符集中失去原有含义。字符集中如需 `-`、`]`、`^`，需转义或调整位置。 | `[a-c]`                                             | `[^abc]`        | 除`abc`以外的字符         |
| **预定义字符集** （可以写在字符集`[ ... ]`中） |                                              |                                                     |                 |
| `\d`                           | 匹配数字 `[0-9]`                                 | `a\dc`                                              | `a\dc`          | `a1c`, `a3c`        |
| `\D`                           | 匹配非数字 `[^0-9]`                               | `a\Dc`                                              | `a\Dc`          | `abc`, `axc`        |
| `\s`                           | 匹配空白字符 `[ \t\r\n\f\v]`                       | `a\sc`                                              | `a\sc`          | `a c`, `a\tc`       |
| `\S`                           | 匹配非空白字符 `[^ \t\r\n\f\v]`                     | `a\Sc`                                              | `a\Sc`          | `abc`, `axc`        |
| `\w`                           | 匹配单词字符 `[A-Za-z0-9_]`                        | `a\wc`                                              | `a\wc`          | `abc`, `a1c`        |
| `\W`                           | 匹配非单词字符 `[^A-Za-z0-9_]`                      | `a\Wc`                                              | `a\Wc`          | `a@c`               |
| **数量词** （用在字符或`(...)`之后）       |                                              |                                                     |                 |
| `*`                            | 匹配前一个字符 0 次或多次                               | `abc*`                                              | `abc*`          | `ab`, `abc`, `abcc` |
| `+`                            | 匹配前一个字符 1 次或多次                               | `abc+`                                              | `abc+`          | `abc`, `abcc`       |
| `?`                            | 匹配前一个字符 0 次或 1 次                             | `abc?`                                              | `abc?`          | `ab`, `abc`         |
| `{m}`                          | 匹配前一个字符 m 次                                  | `ab{2}c`                                            | `ab{2}c`        | `abbc`              |
| `{m,n}`                        | 匹配前一个字符 m 至 n 次，m 或 n 可省略                    | `ab{1,2}c`                                          | `ab{1,2}c`      | `abc`, `abbc`       |
| `*? +? ??`                     | 使 `* + ? {m,n}` 变成非贪婪模式                      | `a.*?`                                              | 示例见下文           | 非贪婪匹配               |
| **边界匹配** （不消耗待匹配字符串中的字符）       |                                              |                                                     |                 |
| `^`                            | 匹配字符串开头，在多行模式中匹配每一行的开头                       | `^abc`                                              | `^abc`          | `abc`               |
| `$`                            | 匹配字符串末尾，在多行模式中匹配每一行的末尾                       | `abc$`                                              | `abc$`          | `abc`               |
| `\A`                           | 仅匹配字符串开头                                     | `\Aabc`                                             | `\Aabc`         | `abc`               |
| `\Z`                           | 仅匹配字符串末尾                                     | `abc\Z`                                             | `abc\Z`         | `abc`               |
| `\b`                           | 匹配单词边界                                       | `\babc\b`                                           | `\babc\b`       | `abc`               |
| `\B`                           | 匹配非单词边界                                      | `a\Bbc`                                             | `a\Bbc`         | `a@bc`              |
| **逻辑、分组**                      |                                              |                                                     |                 |
| `                              | `                                            | 代表左右表达式任意匹配一个，左表达式优先                                | `abc            | def`                | `abc|def`              | `abc`, `def`        |
| `( ... )`                      | 分组，编号从1开始，可使用编号引用                            | `(abc){2}`                                          | `(abc){2}`      | `abcabc`            |
| `(?P<name> ...)`               | 分组，除编号外再指定别名                                 |                                                     |                 |                     |
| `\<number>`                    | 引用编号为<number>的分组匹配到的字符串                      | `(\d)abc\1`                                         | `(\d)abc\1`     | `1abc1`             |
| `(?P=name)`                    | 引用别名为<name>的分组匹配到的字符串                        |                                                     |                 |                     |
| **特殊构造** （不作为分组）               |                                              |                                                     |                 |
| `(?: ...)`                     | 非捕获性分组                                       |                                                     |                 |                     |
| `(?iLmsux)`                    | 模式修饰符，用于调整匹配模式                               | `(?i)abc`                                           | `(?i)abc`       | `Abc`, `ABC`        |
| `(?# ...)`                     | 注释，`#` 后的内容会被忽略                              | `abc(?# comment)123`                                | `abc123`        | `abc123`            |
| `(?= ...)`                     | 正向预查，不消耗字符串内容                                | `a(?=\d)`                                           | `a(?=\d)`       | `a1`, `a2`          |
| `(?! ...)`                     | 负向预查，不消耗字符串内容                                | `a(?!\d)`                                           | `a(?!\d)`       | `a`, `ab`           |
| `(?<= ...)`                    | 正向后发断言                                       | `(?<=\d)a`                                          | `(?<=\d)a`      | `1a`, `2a`          |
| `(?<! ...)`                    | 负向后发断言                                       | `(?<!\d)a`                                          | `(?<!\d)a`      | `a`                 |
| `(?(id/name)yes-pattern        | no-pattern)`                                 | 条件判断，若编号或别名组匹配到字符则匹配 `yes-pattern` ，否则 `no-pattern` | `(\d)abc(?(1)\d | abc)`               | `1abc1`, `abcabc` | |





