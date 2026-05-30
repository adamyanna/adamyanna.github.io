# Linux Tools & Commands

> 2020-05-13

A quick-reference collection of Linux CLI tools for disk inspection, process management, DNS troubleshooting, regex, and find operations.

## Disk Usage by Directory

```bash
du -h --max-depth 1 | sort -hr

```

Recursively reports disk usage for directories one level deep, sorted by size (descending).

## Kill All Processes by Name

```bash
ps -ef | grep {NAME} | awk -F ' ' '{ print $2 }' | xargs kill -9

```

## DNS Cache Management

```bash
nscd -g                # View statistics
nscd -i hosts          # Invalidate hosts cache
rm -f /var/db/nscd/hosts
service nscd restart

```

To enable persistent DNS caching in `/etc/nscd.conf`:

```

enable-cache hosts yes

```

## Advanced Find

```bash
# Find and delete compiled Python files
find ../ -type f -name "*.py[co]" -delete

# Find directories by name
find / -name 'search_keyword' -type d

```

## Regex: Negative Match

**Sublime Text:**

```

^(?!.*InstanceId).+

```

Matches lines that do NOT contain `InstanceId`.

**Python:**

```python
import re
pattern = r'(?!.*pattern_to_exclude)'

```

For character sets like spaces and tabs, use `[\t ]` rather than `\s`.
