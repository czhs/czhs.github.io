# Site basics — deploy, local preview, local-only files

## Deploy model

- **This repo is PUBLIC.** Anything committed is world-readable, including history.
- Chris deploys by **pushing to `main`** (GitHub Actions builds and publishes). When he
  says "push," commit to `main` and push — do not branch (a branch wouldn't deploy).
  He says "push" explicitly when he wants it live.
- **Verify the deploy, not just the push.** The live URL is CDN-cached; a fresh
  `curl https://czhs.github.io/...` can show the previous build for minutes after
  `Deploy site` goes green. Confirm against `git show origin/gh-pages:<path>` (the
  built artifact). When polling the live page, guard on a string unique to the NEW
  state — a substring that also exists in the old page exits instantly and looks
  like success.

## Local preview

```
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 bundle exec jekyll serve --config _config.yml,_config_local.yml --port 4000
```

- The UTF-8 locale matters: without it the build dies early in `bibtex-ruby`'s lexer
  (`invalid byte sequence in US-ASCII`) and never writes pages.
- A full local `jekyll build` **fails at the end** with `Errno::EINVAL` from
  `jekyll-minifier` reading `robotics_media/*.MOV`. That's the gitignored local media,
  not a site bug — CI doesn't have those files, and `_site/` HTML is fully written
  before the crash, so it's still fine to inspect.
- `_config_local.yml` is the untracked local overlay (excludes `robotics_media/` so
  serve works). Don't commit it.
- Config/collection changes need a serve **restart**; everything else hot-reloads.
- The repo-wide `Prettier code formatter` CI job has long been failing on unrelated
  files (`_books/*`, `_includes/mln_card.liquid`) — check only that YOUR changed
  files pass.

## Local-only files — NEVER stage blindly

**Never `git add -A`** — stage explicit paths only. Intentionally untracked/gitignored:

- `robotics_media/` — multi-GB raw portfolio source.
- Portfolio web media: `assets/img/robotics/`, `assets/video/robotics/`,
  `assets/img/ml/`, `assets/video/ml/`. The `/robotics/` + `/ml/` PAGES are published
  as under-construction shells (`under_construction: true`, covers blanked); their
  media stays local until a project goes public (paths are wired in the data files'
  comments). MLn media (`assets/img/mln/`, `assets/video/mln/`) IS published.
- `local/` — local-only tooling; `bin/` is Jekyll-excluded but tracked.
- `_config_local.yml`, `.claude/` (machine-local settings/launch config).

When something should exist locally but never appear on GitHub, gitignore it in place
rather than moving it.

## Theme plumbing worth knowing

- Theme CSS vars are `--global-*` (bg, text, theme, divider, card-bg, hover-text) in
  `_sass/_themes.scss`; dark selector is `html[data-theme="dark"]`.
- `standalone_title` front-matter (hook in `_includes/metadata.liquid`) overrides the
  `"… | Chris Shi"` title suffix — used by the micro-sites.
- `jekyll-email-protect` auto-obfuscates `mailto:` links. Public contact email:
  `chrisshi@andrew.cmu.edu`.

## Jekyll gotchas that cost real time

- A **future-dated** collection doc is listed in the collection but its page is never
  written (`site.future` defaults false) — the card renders, the link 404s. Date
  today or earlier.
- Files starting with `_` are never copied to `_site`.
- `mv` preserves mtimes, so a renamed asset doesn't re-copy on watch; `touch` it.
- A lazy image on a rotated backface never loads (browser treats it as not visible).
- A scroll container clips shadows — padding must be ≥ the shadow blur, or use inset.
