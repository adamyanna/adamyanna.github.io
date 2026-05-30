# adamyanna.github.io

Personal site — static SPA styled as an AI chat interface. No frameworks, no build step, no Jekyll.

**Live:** [adamyan

na.github.io](https://adamyan

na.github.io/)

## Stack

- **Search:** [lunr.js](https://lunrjs.com/) — client-side full-text search over `search-index.json`
- **Render:** [marked.js](https://marked.js.org/) — markdown → HTML
- **Syntax:** [highlight.js](https://highlightjs.org/) (CDN) — code blocks
- **Theme:** CSS custom properties, `data-theme="dark"` / `"light"`, persisted in `localStorage`
- **Hosting:** GitHub Pages (static, `.nojekyll` disables Jekyll processing)

## Content

```
content/
  about.md              # resume / profile
  YYYY/
    title_slug.md       # one file per post
images/                  # inline images referenced in posts
search-index.json        # pre-built lunr index (74 docs)
```

**Conventions:**
- Filenames: `snake_case.md` derived from the h1 title
- Date: `> YYYY-MM-DD` blockquote as first line after title
- Cross-references: `../../images/filename.png` from content files

## Chat commands

| Input | Action |
|---|---|
| `vie` | Redirect to encrypted pages (`/vie/`) |
| `about` / `resume` / `cv` | Load resume |
| `experience` / `skills` / `contact` / `education` | Quick facts |
| Any search term | Full-text search across all posts |
| Click timeline cell | Browse by month |

## Local dev

```bash
python3 server.py          # serves at http://localhost:8080
```

No build step — edit HTML/JS/CSS directly.

## Deploy

Push to `master`. GitHub Pages serves the repo root as-is (Jekyll skipped via `.nojekyll`).

The encrypted `vie/` sub-site is deployed separately by a GitHub Action in the [adamyan

na/vie](https://github.com/adamyan

na/vie) repo.

## Archive

Original Chinese source files and pre-migration assets preserved in `.archive/`.
