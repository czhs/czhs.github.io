# ringworld — the /ringworld/ micro-site (a Socratica node)

Weekly maker space in Pittsburgh (Sundays 4–7pm, location TBD) and a **Socratica
node** (https://www.socratica.info/ — linked from the About panel and the footer).
The Luma event (https://luma.com/ringworld) is hosted by Chris Shi; **no CASI /
AI-safety / interp framing anywhere** — that was removed in the 2026-08-20 rework,
and the Luma copy is fully general. Sibling of MLn; reuses its machinery:
`_data/ringworld.yml`, `_layouts/ringworld_{base,post}.liquid`,
`_includes/ringworld_{styles,card,post_card}.liquid`, `rw-` prefix.

**Full spec kept current with what shipped:
`docs/superpowers/specs/2026-08-06-ringworld-design.md` — read it first** (palette
table, file map, gotchas; its 2026-08-20 addendum describes the current state).

## Static-landing mode (since 2026-08-20)

The page exists to show the club exists, nothing more: banner → hero (title, lead,
meta row with About panel) → footer. **No Luma links, no sessions strip, no blog.**
The machinery is parked, not deleted:

- Feed + sessions markup: git history of `_pages/ringworld.html` (pre-2026-08-20).
- `_pages/rw_projects.html` and `_ringworld/what-ringworld-is-for.md`: present but
  `published: false` — delete that line to bring each back.
- `_data/ringworld.yml` still carries `calendar_url`, `share_note`, `sessions`.
- The masthead nav is just the MLn sibling pill — still the LAST item, so the
  pixel contract below holds.

When the club runs publicly again, restore the sections and re-sync from Luma
(same `__NEXT_DATA__` recipe as [mln.md](mln.md); the old "Adding things" flow —
posts in `_ringworld/<slug>.md`, sessions appended to the yml, session photos in
`assets/img/ringworld/sessions/` with the flip-card lazy-load trap — is in this
file's git history and the spec).

## Homepage pills

`/` links to both clubs from `.home-links` in `_pages/about.md` — a stacked
index of three geometry-identical rows (Substack, MLn, ringworld), capped at
30rem, arrows pinned right. Structure + marks in `_layouts/about.liquid`, zine
spine colours in `_includes/zine_styles.liquid`. The rows all take the zine's
own box (ivory card, ink text, ink border); each club shows ONLY in its left
spine colour (tan / cornflower, like Substack's orange) and its mark + wordmark
art painted in the club's own ink (copied literal hexes; accessible names in
`aria-label`). Fully-painted foreign pills were tried 2026-08-20 and rejected
as not fitting the zine — don't bring them back.

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
  MLn's wordmark hairline vanishes below ~56×21 (the homepage and sibling pills use
  `mln_wordmark_small.png`, the alpha-dilated cut, for exactly this reason).
- **Two art sets, never mixed**: kawaii sprites (`sprites/`, one per session via
  `sprite:`) vs serious watercolours (`posts/`, blog covers). A post without a cover
  gets NO thumbnail, not a sprite.
- **The About panel is always open — no toggle** (2026-08-20): the page is
  info-only, so the old `About ringworld` `<details>` was retired; chips are a
  static row and `.rw-about` renders directly under them, one hairline under the
  block. Don't reintroduce an expander while the site stays a static landing.
  (MLn's `.mln-metarow` still uses the old pattern: toggle in flow, chips pinned
  top-right, same spot opens and closes — that one stands.)
- **Type**: Nanum Myeongjo (hero/post titles), Quicksand (card titles), Nunito
  (body) — loaded only for ringworld ("warmer" after Roboto read cold).
- **Two border tokens**: `--rw-card-line` (0.24) for card edges, `--rw-line` (0.14)
  for hairlines — cards vanish at the hairline value.

## Purpose & copy

The room's stated purpose (Chris, 2026-08-09): honest, exciting work with no penalty
for failing — that framing lives on in the parked `_ringworld/what-ringworld-is-for.md`
(bylined to the club, `author: ringworld`, no placeholder flag by request; now fully
general, no interp/CASI content). Hero is the single line "A Socratica node in
Pittsburgh". Body copy is existing text (the About panel is the Luma description
verbatim; blurb single-sourced from the data file); only the hero title was written
for the site. Reproducing Neel Nanda's guide / Socratica toolbox at length: declined,
stays declined — short attributed quotes + links only.
