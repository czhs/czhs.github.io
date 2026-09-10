# MLn — moved out to its own repo

**The MLn Reading Club is no longer built here.** On 2026-09-10 it was split out
into `mlnclub/mlnclub.github.io`, serving at <https://mlnclub.github.io>. The full
workflow — Luma sync, new weeks, paper audio, recap photos, seasons, the
announcement band — lives in that repo's `docs/claude/mln.md`. Work on the club
site there, not here.

## What is still here, and why

- **Redirects.** `/mln/`, `/mln/qr/` and `/mln/week-1/` … `/mln/week-18/` are all
  still served from this site as `layout: redirect` stubs (`_layouts/redirect.liquid`),
  one-for-one onto the new host. They exist because those URLs have been shared
  publicly for months — every Luma event description links to one, and there is a
  QR code pointing at `/mln/qr/`. **Do not delete them**, and if a week is ever
  renumbered over there, move its stub here to match.
- **Entry points.** The homepage club pill (`_pages/about.md`) and ringworld's
  sibling pill (`_layouts/ringworld_base.liquid`) now link to the absolute
  `https://mlnclub.github.io/`. The pill artwork (`assets/img/mln_*.png`) is still
  served from here, so those files stay.
- **Paper audio.** The accumulating `mln-audio` release is still on THIS repo, and
  the `recording:` URLs on the club site still point at it. Moving it would break
  every past week's player — leave it unless Chris asks.
- **The old build machinery** (`_data/mln.yml`, `_layouts/mln*.liquid`,
  `_includes/mln_*.liquid`, `assets/img/mln/`, `assets/video/mln/`) is still in the
  tree but no longer renders anything — the pages that used it are redirects now.
  It is a **stale duplicate**: editing `_data/mln.yml` here changes nothing and will
  silently diverge from the real one. Pruning it is a clean follow-up; until then,
  treat it as read-only history.
