# Handoff — 2026-05-25

Status of the redesigned personal GitHub Pages site at the end of today's session.

## Project overview

A static HTML/CSS/JS SPA styled as an AI chat interface. No frameworks, no build step. Lives at `/Users/adamna/Developer/tmp_github_io/`.

**Core files:**
- `index.html` — all UI, search logic (lunr.js), markdown rendering (marked.js), syntax highlighting (highlight.js CDN), About page, theme toggle
- `server.py` — Python HTTP server on port 8080 with SPA routing (paths ending in `/` serve `index.html`)
- `search-index.json` — 74 documents, rebuilt today

## Conventions

- **Filenames**: `snake_case.md` derived from the h1 title of the markdown file. Lowercase, spaces → `_`, `&` → ` and `, all other non-alphanumeric → `_`, collapse multiple underscores.
- **Date format**: `> YYYY-MM-DD` in blockquote as first line after frontmatter
- **Content structure**: `content/YYYY/filename.md` — one folder per year
- **No year TOC files or Archives.md in search index** — excluded during index build

## What was completed today

### Content optimization (all years)
- **2025** (4 files): `kubernetes_hpa_controller.md`, `macos_setup_2025.md`, `security_protocols_review.md` — fully rewritten in professional English
- **2024** (3 files): `algorithm_study_plan_2024.md`, `my_entire_career_as_a_coder_in_china.md` — restructured
- **2023** (3 files): `live_migration_pre_copy_deep_dive_qemu_kvm.md` — expanded destination flow, added diagrams, added tuning parameters; `Archives.md` — proper index table
- **2020** (43 files): Major audit and rebuild — see below

### 2020 content audit and rebuild
Original migration had 33 of 43 files severely truncated (30-70% content loss). **21 files** were fully rebuilt today from the original Chinese sources into professional technical English:

| File | Before → After |
|---|---|
| `algorithm_everything.md` | 73 → 489 lines |
| `computer_systems_a_programmer_s_perspective_csapp.md` | 74 → 937 |
| `computer_networks_top_down_fundamentals.md` | 88 → 1,297 |
| `c_programming_language_recap.md` | 83 → 412 |
| `cloud_computing_qualification.md` | 106 → 530 |
| `beginningof2020_algorithm.md` | 135 → 897 |
| `python_dynamic_http_api_generation_via_type_for_monitor_metrics.md` | 73 → 393 |
| `python_and_cpython_core_internals.md` | 74 → 369 |
| `ansible_automation_guide.md` | 153 → 554 |
| `python_service_docker_container_deployment.md` | 135 → 637 |
| `monitor_system_v1_5_project_restructure.md` | 74 → 353 |
| `cpython_internals_virtual_machine_and_source_code_analysis.md` | 91 → 383 |
| `redis_source_code_analysis_and_internals.md` | 85 → 402 |
| `data_sampling_and_integrity_checking_with_redis.md` | 79 → 352 |
| `go_performance_profiling_and_monitoring.md` | 92 → 458 |
| `python_process_memory_analysis_and_optimization.md` | 85 → 461 |
| `red_black_trees_b_trees_and_database_indexing.md` | 66 → 239 |
| `my_algorithm_learning_curve.md` | 98 → 284 |
| `macos_configuration_guide.md` | 101 → 307 |
| `massive_data_programming_patterns.md` | 77 → 206 |
| `algorithm_heap_sort_implementation.md` | 78 → 283 |

### About page
- `content/about.md` — resume/profile page with custom CSS classes (`.about-header`, `.about-badges`, `.skill-grid`, etc.)
- Triggered by typing "about", "resume", or "cv" in the chat, or clicking the **About** link in the header
- `showAbout()` function in `index.html` handles the fetch/render

### Bug fixes
- **Search returned "Nothing for..."**: lunr field name mismatch (`builder.field('content')` → `builder.field('body')`) and data source mismatch (`e.content` → `e.body`) — fixed at lines ~353, 354, 449, 505
- **lunr query parsing**: punctuation like `:` in query terms was interpreted as field scoping. Fixed by stripping punctuation before adding wildcards: `query.replace(/[^\w\s]/g,' ').split(/\s+/).filter(Boolean).map(...)` at line ~371

### File naming
- All 66 files renamed from kebab-case to snake_case (derived from h1 titles)
- All cross-references in `.md` files updated
- Search index rebuilt after rename

## How to start

```bash
cd /Users/adamna/Developer/tmp_github_io
python3 server.py
# Site at http://localhost:8080
```

## Key code locations in index.html

| Feature | Approx. line |
|---|---|
| lunr search builder (field names) | ~350-360 |
| Query sanitization (punctuation strip) | ~370-375 |
| Autocomplete snippet (`r.body`) | ~449 |
| Result card snippet (`r.body`) | ~505 |
| `showAbout()` function | ~530-570 |
| Theme toggle CSS variables | `:root` and `[data-theme="light"]` |
| About-specific CSS classes | `.about-header` through `.skill-tags span` |

## Remaining / not done

- **Date-prefix naming convention**: User liked the idea of `YYYY-MM-DD-title-slug.md` but decision was postponed. Current convention stays as `snake_case_title.md`.
- **Small 2020 files**: A handful of originally-short files (~10-50 line Chinese notes) were translated to concise English. They're functionally complete but could be expanded if desired: `modern_operating_systems.md` (9 lines), `sumof2019_datainfluxpatrol.md` (17 lines), `linux_networking_basics.md` (25 lines), and a few others.
- **Missing image-only file**: `2020-05-18-tech-stack-planning-2020.md` was a 13-line image reference in the original — no textual content to migrate.
- **Browser testing**: Search and content loading verified via curl. Full browser smoke test not done today.

## Memory files

User preferences are stored in `/Users/adamna/.claude/projects/-Users-adamna-Developer-fran-ais-2026-docs/memory/`:
- `feedback_pushback.md` — Adam wants Claude to push back on bad ideas
- `feedback_horizon_sync.md` — root and roadmap index.html must stay in sync
- `feedback_filename_convention.md` — snake_case filenames from h1 title

## Original source

Original Chinese markdown files are at `/Users/adamna/Developer/adamyanna.github.io/docs/archives/`. These were the source of truth for the 2020 content rebuild.
