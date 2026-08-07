# ringworld — design

A micro-site for **ringworld**, a weekly mechanistic-interpretability maker space in
Pittsburgh. It sits beside the MLn Reading Club micro-site and is built the same way:
a Jekyll layout pair, a YAML data file, and a card grid. This document specifies the
palette, file layout, data schema, copy, and the cross-link to MLn.

## 1. Goals

- A standalone `/ringworld/` micro-site with its own masthead, footer, and palette.
- A session archive that grows by appending a block to `_data/ringworld.yml`, exactly
  the way MLn weeks grow.
- One session live at launch: Sunday 30 August 2026.
- A `ringworld ↗` link in the MLn masthead, and a reciprocal `MLn ↗` link back.

Non-goals: no recaps, photo carousels, or runbooks in this pass. MLn grew those over
time; ringworld gets the skeleton that can accept them later.

## 2. Palette

Sampled from the ringworld artwork. The dominant hues are cornflower blue (~215°) and
meadow olive (~65°) on warm paper cream, with lavender planets and gold stars as
sparkle accents.

The paper base is shared with MLn so the two micro-sites read as a family; the accent
hue is the difference. MLn is green on cream, ringworld is blue on cream.

| role | value |
| --- | --- |
| paper / background | `#FEF9F0` |
| card | `#FFFDF7` |
| text | `#24303F` |
| text, muted | `#5A6B80` |
| **primary accent** | `#3E6FB4` |
| secondary (meadow) | `#7C9A3C` |
| sparkle (lavender) | `#8B6FC4` |
| sparkle (gold) | `#D99B3C` |
| divider | `rgba(36, 48, 63, 0.14)` |
| dot grid | `rgba(36, 48, 63, 0.07)` |

The paper value is the illustration's own background colour, so the banner has no
visible edge against the page.

`#3E6FB4` on `#FEF9F0` clears WCAG AA for body text. The meadow, lavender, and gold are
accents only — tags, rules, sparkles — never body text on paper.

**Light only.** The artwork is drawn on cream and is the whole page's ground; a dark
ringworld would be a bright cream poster floating in a hole. al-folio's `theme.js` still
stamps `data-theme` on `<html>` from the stored preference, so the light values are
re-asserted for every value that attribute can take rather than left to cascade, and
`html:has(body.rw-site)` pins `color-scheme: light`. The rest of the site keeps its
light/dark toggle.

The palette is declared as `--rw-*` custom properties scoped to `body.rw-site`, which
also rebind the al-folio `--global-*` variables the shared `head.liquid` and
`scripts.liquid` depend on. This mirrors how MLn styles are scoped and keeps the main
site's forest/tan theme untouched.

## 3. Files

```
_pages/ringworld.html              /ringworld/ — banner, hero, FAQ, session grid
_pages/rw_session1.md              /ringworld/session-1/
_data/ringworld.yml                calendar_url, location, sessions
_layouts/ringworld_base.liquid     html shell, masthead, footer
_layouts/ringworld.liquid          session detail page + Luma embed
_includes/ringworld_styles.liquid  scoped <style> block
_includes/ringworld_card.liquid    one session card for the grid
assets/img/ringworld/banner.png    1800×514 hero artwork
assets/img/ringworld/mark.png      480×263 ring only, cream flood-filled out
assets/img/ringworld/wordmark.png  564×141 hand lettering, alpha only
assets/img/ringworld/icon.png      512×512 square lockup, source art, unreferenced
assets/img/ringworld/og.png        1200×630 social card
```

Class prefix is `rw-` throughout, so nothing collides with the `mln-` rules that ship
in the same stylesheet bundle.

Images come from the Luma CDN originals
(`uploads/vc/e27a6b4c-…png` and `uploads/kl/b4830aad-…png`) rather than resampled
screenshots, and are committed to the repo so the site does not depend on Luma's CDN.
They are downscaled and palette-quantised, which is lossless enough for flat crayon
texture and takes the banner from 1.5 MB to under 400 KB.

`mark.png` and `wordmark.png` are cut from the square icon: the ring with its
surrounding cream flood-filled to transparent, and the hand lettering reduced to an
alpha-only shape. The wordmark is applied as a CSS mask over `currentColor` rather than
placed as an image, so it takes the text colour.

## 3a. Typography

| role | face | used for |
| --- | --- | --- |
| wordmark | the artwork's own hand lettering | masthead brand |
| display serif | Nanum Myeongjo 400 / 700 | hero + session titles |
| display sans | Quicksand 500–600 | card titles, section headings, FAQ summary |
| body | Nunito 300–700 | everything else |
| utility | the site's mono stack | eyebrows, chips, dates, tags |

Loaded in one Google Fonts request from `ringworld_styles.liquid`, which only
`ringworld_base.liquid` includes — MLn and the main site keep Roboto and never fetch
these. The brand is never set in a typeface: the masthead uses the drawn lettering
itself, so there is no font standing in for the logo.

## 4. Data schema

`_data/ringworld.yml`:

```yaml
calendar_url: https://luma.com/ringworld
location: 201 S Craig St, Unit 1E
location_note: enter from the Henry St side
sessions:
  - num: 1
    slug: "kduzb3gz"          # luma.com/<slug>
    evt: "evt-7loVUQIHc8aBiIk" # lu.ma/embed/event/<evt>/simple
    date: "2026-08-30"
    title: "ringworld"
    summary: "…"
    description: |-
      …
    cover: /assets/img/ringworld/icon.png   # optional; defaults to the icon
    tags: []                                 # optional
    coming_soon: false                       # optional
```

Fields match MLn's week schema where they overlap (`num`, `slug`, `evt`, `date`,
`title`, `summary`, `description`, `cover`, `tags`, `coming_soon`), so the card include
and the upcoming/past sort logic port over with only the prefix changed.

Because every session shares one cover by default, cards are differentiated by the
session number and date band rather than by thumbnail. A per-session `cover:` overrides
the default when a session gets its own art.

## 5. Page behaviour

**`/ringworld/`** — full-bleed banner, hero title and lead, a cadence chip row
(`Sundays · 4–7pm`, `two focus blocks · show-and-tell`, `follow on Luma ↗`), a
collapsible `What's this?` FAQ matching MLn's `<details>` pattern, then the session
grid.

The grid reuses MLn's ordering: sessions are split into upcoming and past against the
build date, the next session renders as a standalone card flagged `up next`, any further
upcoming sessions collapse behind a `+N more upcoming` toggle, and past sessions follow
newest-first.

**`/ringworld/session-N/`** — a back link, an eyebrow (`RINGWORLD · SESSION N`), the
session title, a description column, and an aside carrying the Luma embed iframe with a
plain-link fallback. Same two-column grid as `_layouts/mln.liquid`.

**Masthead** — the square icon as the brand mark, `ringworld` as the wordmark, and nav
items `Sessions` / `MLn ↗` / `Luma ↗`.

The hidden `#light-toggle` button block from `mln_base.liquid` is carried over verbatim.
al-folio's `theme.js` binds listeners to those IDs on load, and a micro-site masthead
without them throws a null `addEventListener` that halts all page JS.

## 6. Copy

All body copy is existing text, not written for the site. Two sources:

1. **The Luma event description**, used verbatim for the `What's this?` panel and for
   session one's description. Its `When/Where` is the one edit: Luma's body text says
   "(tentatively) 201S Henry Street, Unit 1E" while its location field says 201 S Craig
   St — the same door from two sides — so the site states the Craig St address with the
   Henry St entrance as a note, and drops "tentatively" from the weekly cadence.
2. **The club blurb**, supplied directly, used as the hero lead and as the page
   `description` meta. It lives in `_data/ringworld.yml` under `blurb:` so both readers
   stay in sync:

   > A friendly community of tinkerers in Pittsburgh, PA—we meet to work on side
   > projects every Sunday near CMU! Feel free to send a message or notif through Luma
   > if you need to get in contact!

The one line written for the site is the hero title — *A weekly maker space for
mechanistic interpretability.* — which carries the interp framing that the Luma copy,
written for a general maker space, does not.

Socratica's toolbox was considered as a copy source and not used: the wording on
`toolbox.socratica.info` is theirs to license, and the Luma description already carries
the same Socratica-lineage house style (the "don't network if you're here to network we
will be so sad" guidance is the tell). Anything wanted from Socratica verbatim should be
pasted in deliberately rather than scraped.

All of this is placeholder pending real copy.

## 7. MLn cross-link

`_layouts/mln_base.liquid` gains one nav item between `Weeks` and `Luma ↗`:

```html
<a href="{{ '/ringworld/' | relative_url }}">ringworld</a>
```

It is an internal link, so it takes no `↗` and no `target="_blank"`. It appears on
`/mln/` and on every `/mln/week-N/` page, since both use `mln_base`. The reciprocal
`MLn ↗` in the ringworld masthead is likewise internal.

This is the only edit to an existing file. Everything else is new.

## 8. Verification

- `bundle exec jekyll build` succeeds with no new warnings.
- `/ringworld/`, `/ringworld/session-1/`, `/mln/`, and `/mln/week-1/` all render.
- The ringworld banner, icon, and Luma embed load on the built pages.
- The `ringworld` nav item is present in the MLn masthead on both MLn pages.
- The ringworld palette and fonts do not leak: `/mln/` and `/about/` still render
  forest/tan in Roboto, and never request Nunito/Quicksand/Nanum Myeongjo.
- `/ringworld/` stays light with the OS set to dark and with `data-theme="dark"` on
  `<html>`.
- Responsive at 375px: banner scales, grid collapses to one column, nav does not wrap
  off-screen.
