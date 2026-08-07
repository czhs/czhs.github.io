# ringworld — design

A micro-site for **ringworld**, a weekly mechanistic-interpretability hacker space in
Pittsburgh, hosted by CASI. It sits beside the MLn Reading Club micro-site and shares its
machinery: a Jekyll layout pair, a YAML data file, and card grids.

This document was written before implementation and has been updated to describe what
actually shipped. Where the built site diverged from the original plan, the reason is
recorded — those are the decisions most likely to get "fixed" back by someone who
doesn't know why.

## 1. What it is

- `/ringworld/` — a blog-led landing page. The blog is the main element; the sessions
  are the invitation beneath it.
- `/ringworld/<slug>/` — a post page per entry in the `ringworld` collection.
- Session cards link **straight to Luma**. There are no per-session detail pages.
- Cross-linked with MLn: each masthead carries the other club's mark.

Non-goals: no recaps or runbooks in this pass. MLn grew those over time; ringworld gets
a skeleton that can accept them later.

## 2. Palette

Sampled from the ringworld artwork. The dominant hues are cornflower blue (~215°) and
meadow olive (~65°) on warm paper cream, with lavender planets and gold stars as
sparkle accents. The paper base is shared with MLn so the two micro-sites read as a
family; the accent hue is the difference. MLn is green on cream, ringworld is blue.

| role | value |
| --- | --- |
| paper / background | `#FEF9F0` — the illustration's own background |
| card | `#FFFDF7` |
| text | `#24303F` |
| text, muted | `#5A6B80` |
| **primary accent** | `#3E6FB4` |
| secondary (meadow) | `#7C9A3C` |
| sparkle | `#8B6FC4` lavender · `#D99B3C` gold |
| hairline rules | `--rw-line`, `rgba(36, 48, 63, 0.14)` |
| **card edges** | `--rw-card-line`, `rgba(36, 48, 63, 0.24)` |
| dot grid | `rgba(36, 48, 63, 0.07)` |

**Two border tokens, deliberately.** The card fill is a near-match for the page cream,
so at `--rw-line` the card outlines disappeared and the cards stopped reading as cards.
Card surfaces (`.rw-post-card`, `.rw-tile-face`, `.rw-empty`, `.rw-post-cover`,
`.rw-post-foot`, `.rw-embed iframe`) use the heavier `--rw-card-line`; section rules and
tags keep the hairline.

**Light only.** The artwork is drawn on cream and is the whole page's ground; a dark
ringworld would be a bright cream poster floating in a hole. al-folio's `theme.js` still
stamps `data-theme` on `<html>`, so the light values are re-asserted for every value the
attribute can take, and `html:has(body.rw-site)` pins `color-scheme: light`. The rest of
the site keeps its toggle.

## 3. Files

```
_pages/ringworld.html               /ringworld/ — banner, hero, blog feed, sessions row
_ringworld/                         the blog collection, one .md per post
_ringworld/example-post.md          template, published: false
_data/ringworld.yml                 club metadata + the sessions list
_layouts/ringworld_base.liquid      html shell, masthead, footer
_layouts/ringworld_post.liquid      blog post page
_includes/ringworld_styles.liquid   scoped <style> block + the font <link>
_includes/ringworld_post_card.liquid  one blog card
_includes/ringworld_card.liquid     one session tile (flip card)
_scripts/cut_ringworld_sprites.py   re-cuts the sprites from the source sheets
```

Class prefix is `rw-` throughout, so nothing collides with the `mln-` rules that ship in
the same bundle.

### Artwork

```
assets/img/ringworld/banner.png     1800×514 hero artwork
assets/img/ringworld/mark.png       ring only, cream flood-filled to transparent
assets/img/ringworld/wordmark.png   hand lettering, alpha only
assets/img/ringworld/icon.png       512×512 square lockup (source art, unreferenced)
assets/img/ringworld/og.png         1200×630 social card
assets/img/ringworld/sprites/       31 kawaii characters — SESSIONS
assets/img/ringworld/posts/         5 watercolours — BLOG COVERS
assets/img/ringworld/sessions/      session photos (see its README)
assets/img/ringworld/source/        full-res originals, excluded from the build
assets/img/mln_mark.png             MLn dot ring, alpha only
assets/img/mln_wordmark.png         MLn serif lettering, alpha only
```

**Two art sets, don't mix them.** The kawaii sprites belong to the sessions — one per
session via `sprite:`, which is what tells otherwise-identical session cards apart. The
serious watercolours are blog covers, chosen to match LessWrong's register. A post
without a cover gets **no thumbnail** rather than a sprite; a character on a writeup
undersells it.

Source art lives in `assets/img/ringworld/source/` and is excluded in `_config.yml` — it
is ~5 MB and imagemagick would generate webp variants of every sheet. Re-cut the sprites
with `python3 _scripts/cut_ringworld_sprites.py` after editing a sheet.

## 4. Typography

| role | face | used for |
| --- | --- | --- |
| wordmark | the artwork's own hand lettering | masthead brand |
| display serif | Nanum Myeongjo 400 | hero + post titles |
| display sans | Quicksand 500–600 | card titles, section headings, FAQ |
| body | Nunito 300–700 | everything else |
| utility | the site's mono stack | eyebrows, chips, dates, tags |

One Google Fonts request from `ringworld_styles.liquid`, which only `ringworld_base`
includes — MLn and the main site keep Roboto and never fetch these. **The brand is never
set in a typeface:** both mastheads use their club's own drawn lettering as a CSS mask
over `currentColor`, so it takes the theme colour and inverts in dark mode.

## 5. Data schema

`_data/ringworld.yml` carries club metadata (`calendar_url`, `time`, `location`,
`location_note`, `host`, `host_url`, `blurb`, `share_note`) and a `sessions:` list:

```yaml
sessions:
  - num: 1
    slug: "kduzb3gz"           # luma.com/<slug> — the card links here
    evt: "evt-7loVUQIHc8aBiIk" # kept for reference; no embed any more
    date: "2026-08-30"
    sprite: ringworld          # a filename from sprites/, one per session
    title: "ringworld"
    description: |-            # verbatim from the Luma event
      …
    photo: /assets/img/ringworld/sessions/….jpg   # optional — makes the card flip
    photo_alt: …                                   # optional
    coming_soon: false                             # optional
```

Blog posts are one markdown file per post in `_ringworld/`, with `title`, `author`,
`author_url?`, `date`, `session?`, `description`, `cover?`. The layout is defaulted in
`_config.yml`, so a post's front matter only carries its own content. See
`_ringworld/example-post.md`.

## 6. Page behaviour

**`/ringworld/`** — full-bleed banner (the artwork's background matches the page and its
dot grid is continued in CSS, so it has no visible edge), hero title and lead, cadence
chips, a collapsible `What's this?` FAQ, then **the ringworld interpretability blog**,
then the **sessions** row.

The blog feed is a responsive grid of post cards. With no posts it shows an invitation,
not a blank.

The sessions row is a horizontally scrolling row of small cards, not a grid — the blog
is the page, and a long session history should never push it off the top. Order is next
session first (flagged `up next`), then other upcoming, then past newest-first.

**Session flip cards.** A session with a `photo:` flips on hover: character on the front,
photo on the back. Every tile shares the flip markup so there is one code path; a session
without a photo has no back face and never rotates. The affordance is stated once on the
sessions header ("hover to flip"), only when a session actually has a photo, and hidden
under `@media (hover: none)` where hover doesn't exist. An earlier ambient auto-flip was
cut — it got noisy with more than a couple of photo cards.

**`/ringworld/<slug>/`** — back link, eyebrow, serif title, byline, optional cover, the
post body, and a footer inviting the reader to post.

**Masthead** — the drawn ring and wordmark, then `Luma ↗`, then the sibling pill.

The hidden `#light-toggle` block from `mln_base.liquid` is carried over verbatim:
al-folio's `theme.js` binds listeners to those IDs on load, and a masthead without them
throws a null `addEventListener` that halts all page JS.

## 7. Copy

All body copy is existing text, not written for the site:

1. **The Luma event description**, verbatim, for the `What's this?` panel and session
   one. Its `When/Where` is the one edit: Luma's body says "201S Henry Street, Unit 1E"
   while its location field says 201 S Craig St — the same door from two sides — so the
   site states the Craig St address with the Henry St entrance as a note, and drops
   "tentatively" from the weekly cadence.
2. **The club blurb**, supplied directly, used as the hero lead and the page description
   meta. Single-sourced from `blurb:` in the data file.

The hero title — *A weekly hacker space for mechanistic interpretability.* — and the
first blog post are written for the site, since the Luma copy describes a general maker
space and doesn't carry the interp framing.

**On sourcing.** Reproducing Neel Nanda's *How To Become A Mechanistic Interpretability
Researcher* or the Socratica toolbox at length was declined: that is their writing, and
republishing it here would be a copyright problem and would read as ours. The first post
is built around both, quotes Neel briefly with attribution, and links out. If the
authors give permission, their text can be placed verbatim.

## 8. MLn cross-link

Both mastheads carry the sibling club's own mark in an emphasized pill, and the two land
on **the same pixel** so the link you just clicked is under your cursor when you arrive.
That required: the pill is the **last** nav item on both sites (so its right edge is
pinned by the shell), both shells are 940px, both mastheads are 62px tall, and both
pills share a fixed width and a fixed-width icon slot. `.rw-sibling` and `.mln-sibling`
must be kept in sync.

MLn also lost "Reading Club" from its masthead and gained a dashed cohosting banner above
its week grid, pointing at `contact_email` in `_data/mln.yml`.

## 9. Gotchas worth keeping

- **A new collection needs a server restart.** `jekyll serve --watch` does not reload
  `_config.yml`.
- **A future-dated collection doc is listed but never written.** `site.future` defaults
  to false and gates `Document#write?`, so the doc appears in `site.ringworld` (its feed
  card renders) while its page 404s. Date posts today or earlier.
- **Files whose names start with `_` are never copied to `_site`.**
- **A lazy image on a rotated backface never loads** — the browser treats it as not
  visible, so the card flips to a blank. The flip photo is not lazy.
- **A scroll container clips shadows.** `.rw-strip` is `overflow-x: auto`, so its padding
  must be at least as large as the shadow it contains (16/18/36px) or the blur is sliced
  into a hard edge. The `is-next` ring is `inset` for the same reason.
- **`mv` preserves mtimes**, so renaming an asset does not trigger Jekyll to re-copy it;
  `touch` the files.

## 10. Verification

- `/ringworld/`, `/ringworld/what-ringworld-is-for/`, `/mln/`, `/mln/week-N/` all render.
- The ringworld palette and fonts do not leak: `/mln/` and `/about/` still render
  forest/tan in Roboto and never request Nunito/Quicksand/Nanum Myeongjo.
- `/ringworld/` stays light with the OS set to dark and `data-theme="dark"` on `<html>`.
- Both sibling marks measure at the same viewport coordinate on each site.
- Responsive at 375px: banner scales, grids collapse to one column, nav doesn't wrap
  off-screen, no horizontal page overflow.
