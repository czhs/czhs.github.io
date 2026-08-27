# CLAUDE.md — Chris's personal site (al-folio, deploys from `main` via Actions)

Two rules that apply to everything, before any workflow:

1. **This repo is PUBLIC.** Nothing sensitive in commits, history, or docs — research
   post bodies publish encrypted; never `git add -A` (untracked local media).
2. **No AI-invented copy, exact attributions** — read
   [content-rules](docs/claude/content-rules.md) before writing any user-facing text.

Detailed workflows live in `docs/claude/` — **read the relevant file before working
on that area**:

| File | When |
|---|---|
| [site-basics](docs/claude/site-basics.md) | always useful: deploy/push semantics, local preview, local-only files, Jekyll gotchas |
| [content-rules](docs/claude/content-rules.md) | any user-facing copy |
| [mln](docs/claude/mln.md) | updating the MLn reading club: Luma sync, new weeks, paper audio, recap photos |
| [research-posts](docs/claude/research-posts.md) | turning an uploaded notebook PDF into a password-gated /research post |
| [ringworld](docs/claude/ringworld.md) | the /ringworld/ micro-site: posts, sessions, design decisions not to undo |
| [poems](docs/claude/poems.md) | the /76265/ poem directory: adding a poem from an uploaded PDF (public titles, gated bodies) |
| [robotics-ml-portfolio](docs/claude/robotics-ml-portfolio.md) | /robotics/ + /ml/ shells; the never-link-to-robotics rule |
| [hcl-ml](docs/claude/hcl-ml.md) | the gated /HCL-ML page: unified write-up, inline co-drafting editor + save server, publishing |
| [domain](docs/claude/domain.md) | chrisshi.com DNS / cutover |

Keep this file small: new workflows get their own file in `docs/claude/` plus one
table row here.
