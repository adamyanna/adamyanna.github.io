# Knowledge Fragments: Tips & Snippets

> 2020-03-07

Quick-reference snippets across Python, Linux, and Windows — collected tips too small for their own pages.

## Python

### Reverse an Array

```python
list(reversed(a))          # reversed() returns an iterator
sorted(a, reverse=True)    # Sort descending
a[::-1]                    # Slice with step -1 (most Pythonic)

```

### Class Inheritance with `type`

Use the `class` keyword to modify an instance's type reference at runtime. See also: [Python Dynamic Class Generation HTTP API](Python-Dynamic-Class-Generation-HTTP-API.md).

## Linux

### CPU Info from `/proc`

```bash
# Physical CPU count
grep 'physical id' /proc/cpuinfo | sort -u | wc -l

# Core count
grep 'core id' /proc/cpuinfo | sort -u | wc -l

# Thread count
grep 'processor' /proc/cpuinfo | sort -u | wc -l

# CPU model
dmidecode -s processor-version

# Full CPU details
cat /proc/cpuinfo

```

### Set Timezone (CentOS 7)

```bash
# List all timezones
timedatectl list-timezones

# Set to Shanghai (UTC+8)
timedatectl set-timezone Asia/Shanghai

# Sync hardware clock to local time
timedatectl set-local-rtc 1  # 0 = UTC

```

### iptables Basics

```bash
iptables -t nat -L

```

### List Files with Absolute Paths

```bash
# Using sed
ls | sed "s:^:$(pwd)/:"

# Add prefix to every line
sed 's/^/string/g' file     # Prepend
sed 's/$/string/g' file     # Append

# Using find
find $PWD -maxdepth 1 | xargs ls -ld    # Non-recursive
find $PWD | xargs ls -ld                # Recursive (including hidden)

```

## Windows

### TCP Connection Inspection

```cmd
netstat -ant | findstr <PORT>
netstat -ano -p tcp | findstr 8080

```
