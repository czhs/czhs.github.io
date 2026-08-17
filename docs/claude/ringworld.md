# ringworld — the /ringworld/ hacker-space micro-site

Weekly mechanistic-interpretability hacker space (Sundays 4–7pm, 201 S Craig St Unit
1E — Luma's body says "201S Henry Street": same door, two sides; site states Craig St
with Henry St entrance as a note). Hosted by CASI. Luma: https://luma.com/ringworld.
Sibling of MLn; reuses its machinery: `_data/ringworld.yml`,
`_layouts/ringworld_{base,post}.liquid`, `_includes/ringworld_{styles,card,post_card}.liquid`,
`rw-` prefix.

**Full spec kept current with what shipped:
`docs/superpowers/specs/2026-08-06-ringworld-design.md` — read it first** (palette
table, file map, gotchas).

## Adding things

- **Blog post**: one markdown file in `_ringworld/<slug>.md` → `/ringworld/<slug>/`
  (layout defaulted in `_config.yml`; copy `_ringworld/example-post.md`). Added by
  hand. Claude-drafted posts carry `placeholder: true`
  ([content-rules.md](content-rules.md)).
- **Session**: append a block to `_data/ringworld.yml` — no per-session pages, cards
  link to Luma. Manual sync; same `__NEXT_DATA__` recipe as [mln.md](mln.md).
- **Session photo**: drop in `assets/img/ringworld/sessions/`, set `photo:` — card
  becomes a hover flip card (flip photo must NOT be lazy: a lazy image on a rotated
  backface never loads).

## Decisions not to undo

- **Light mode only, deliberately** — the artwork is drawn on cream and is the page's
  ground. `theme.js` still stamps `data-theme`, so light values are re-asserted for
  every value it takes. Page background is the illustration's own cream `#FEF9F0`
  (don't round the hex) + matching CSS dot grid.
- **Neither masthead is set in type** — both clubs' wordmarks are artwork applied as
  alpha masks over `currentColor`. MLn's masthead no longer says "Reading Club"; two
  font-set wordmarks were rejected before this.
- **The two sibling cross-link pills land on the same pixel.** Each masthead's pill
  carries the OTHER club's mark, is the LAST nav item; both sites share a 940px
  shell, 62px masthead, fixed pill width + icon slot. `.rw-sibling`/`.mln-sibling`
  must stay in sync — changing shell width, masthead height, nav order, or pill
  padding on one site breaks the other. Color is free to differ; the box is not.
  Each pill is painted in the palette of the site it goes TO (copied literal hexes).
  Trap: al-folio's `main.css` sets `color` on bare `span`, beating inheritance — pin
  `color: inherit` or a currentColor mask renders in the host page's text color.
  MLn's wordmark hairline vanishes below ~56×21.
- **Two art sets, never mixed**: kawaii sprites (`sprites/`, one per session via
  `sprite:`) vs serious watercolours (`posts/`, blog covers). A post without a cover
  gets NO thumbnail, not a sprite.
- **One Luma link per site** (masthead only). **One meta row, not stacked bands**:
  `What's this?` in flow at left, chips absolutely pinned top-right — the toggle must
  open and close from the same spot; don't turn `.rw-metarow`/`.mln-metarow` back
  into a flex row. The About toggle is deliberately not labelled "What's this?"
  (the panel's own first heading says it).
- **Type**: Nanum Myeongjo (hero/post titles), Quicksand (card titles), Nunito
  (body) — loaded only for ringworld ("warmer" after Roboto read cold).
- **Two border tokens**: `--rw-card-line` (0.24) for card edges, `--rw-line` (0.14)
  for hairlines — cards vanish at the hairline value.

## Purpose & copy

The room's stated purpose (Chris, 2026-08-09): honest, exciting work with no penalty
for failing — drives `_ringworld/what-ringworld-is-for.md` (bylined to the club,
`author: ringworld`, no placeholder flag by request). Hero is the single line "A
weekly maker space for AI safety". Body copy is existing text (Luma verbatim, blurb
single-sourced from the data file); only the hero title was written for the site.
Reproducing Neel Nanda's guide / Socratica toolbox at length: declined, stays
declined — short attributed quotes + links only.
