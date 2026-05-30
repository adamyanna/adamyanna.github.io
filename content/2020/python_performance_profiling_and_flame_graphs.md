# Python Performance Profiling & Flame Graphs

> 2020-04-05

Production profiling of Python services with `cProfile` — collecting runtime statistics, analyzing call counts and cumulative time, and generating flame graphs.

## cProfile & profile

Python's built-in deterministic profilers. `cProfile` is the C-extension variant (lower overhead), recommended for production use.

### Command-Line Usage

```bash
python -m cProfile [-o output_file] [-s sort_order] myscript.py

```

| Flag | Purpose |
|---|---|
| `-o <file>` | Write raw stats to file (replaces `-s` output) |
| `-s <sort>` | Sort output by: `ncalls`, `cumtime`, `tottime`, etc. |

**Note:** `-s` has no effect when `-o` is specified — the output file contains raw stats; sorting is done at read time.

For long-running services, the profile file is only written on process termination. Send a termination signal (SIGTERM) after a representative capture window (e.g., 10–30 minutes).

### In-Code Usage

```python
import cProfile
import re
cProfile.run('re.compile("foo|bar")')

```

## Production Profiling Example

```bash
cd /opt/netmon/debug/monitor-server/monitor/

/home/monitor_server/bin/python -m cProfile -o result.out \
    /opt/netmon/debug/monitor-server/monitor/run_server.py \
    --config-file /opt/netmon/debug/monitor-server/monitor/conf/conf.ini \
    --port 51035 \
    >> /var/log/monitor-server/server_debug.log 2>&1 &

# Let the process handle requests for 10–30 minutes, then:
kill -TERM <PID>

```

## Analyzing Results with pstats

```python
#!/usr/bin/python
import pstats
import sys

input_f = sys.argv[1]
p = pstats.Stats(input_f)
p.sort_stats("ncalls", "cumtime")
p.print_stats()

```

### Sort Keys

| Key | Meaning |
|---|---|
| `ncalls` | Number of calls to the function/code block |
| `tottime` | Total time in the function (excludes sub-calls) |
| `percall` | `tottime` / `ncalls` |
| `cumtime` | Cumulative time including all sub-calls (recursive functions: total across all recursive invocations) |
| `percall` (cum) | `cumtime` / `ncalls` |
| `filename:lineno(function)` | Source location |

## Sample Output

```

Tue Apr 7 17:10:32 2020 cum.out

13445271 function calls (13371131 primitive calls) in 436.704 seconds

Ordered by: call count, cumulative time

ncalls    tottime  percall  cumtime  percall filename:lineno(function)
3726996   0.695    0.000    0.716    0.000   {method 'get' of 'dict' objects}
1710220   0.565    0.000    0.580    0.000   {isinstance}
1525540   0.191    0.000    0.192    0.000   {len}
959341    1.045    0.000    1.045    0.000   {_codecs.utf_8_decode}
959298    0.454    0.000    1.499    0.000   /home/monitor_server/...

```

## Flame Graphs

For visualization, use tools like:
- **[FlameGraph](https://github.com/brendangregg/FlameGraph)** (Brendan Gregg's Perl scripts)
- **frame-prof** — third-party Python module for flame graph output
- **py-spy** — sampling profiler, can attach to running processes
