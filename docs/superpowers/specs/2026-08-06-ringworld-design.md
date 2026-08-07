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

| role | light | dark |
| --- | --- | --- |
| paper / background | `#FDF8EE` | `#141C28` |
| card | `#FFFCF5` | `#1D2838` |
| text | `#24303F` | `#E8EDF5` |
| text, muted | `#5A6B80` | `#A7B6C9` |
| **primary accent** | `#3E6FB4` | `#9CC0F0` |
| secondary (meadow) | `#7C9A3C` | `#B8CE7A` |
| sparkle (lavender) | `#8B6FC4` | `#B9A3DE` |
| sparkle (gold) | `#D99B3C` | `#E8B54D` |
| divider | `rgba(36, 48, 63, 0.14)` | `rgba(232, 237, 245, 0.16)` |

`#3E6FB4` on `#FDF8EE` clears WCAG AA for body text. The meadow, lavender, and gold are
accents only — tags, rules, sparkles — never body text on paper.

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
assets/img/ringworld/icon.png      1254×1254, from the Luma CDN original
assets/img/ringworld/banner.png    2345×670, from the Luma CDN original
assets/img/ringworld/og.png        1200×630 social card
```

Class prefix is `rw-` throughout, so nothing collides with the `mln-` rules that ship
in the same stylesheet bundle.

Images come from the Luma CDN originals
(`uploads/vc/e27a6b4c-…png` and `uploads/kl/b4830aad-…png`) rather than resampled
screenshots, and are committed to the repo so the site does not depend on Luma's CDN.

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

Broad and focused at once, the way LessWrong is: a real centre of gravity that in
practice admits almost anything, because what binds the room is the method rather than
the subject. Interpretability is the method — taking a system apart until you can say
what it is actually doing — and it turns out to travel. The Luma description's voice and
schedule are preserved; the subject is retargeted.

The copy should never read as a list of permitted hobbies. It states the through-line
once, plainly, and lets the breadth follow from it.

**Hero title:** A weekly maker space for mechanistic interpretability.

**Hero lead:** Sundays, 4–7pm. Interpretability is the habit of taking something apart
until you can say what it is actually doing — and the habit does not stop at neural
networks. Bring a probe, an SAE, an attention viz, a replication you have been meaning
to run. Bring the essay, the company, or the piece of music you are trying to understand
from the inside. Two focus blocks, a social break in the middle, optional show-and-tell
at the end.

**What's this?**

- A super warm group of folks working on things we don't normally have time for.
- The centre of gravity is mechanistic interpretability — circuits, probes, SAEs,
  in-context learning. That is what most of the room is doing, and it is what the room
  is good at helping with.
- It is not a restriction. Interpretability is a way of paying attention, not a topic
  list: writing, art, and startups are the same move aimed at different systems, and
  they belong here on their own terms rather than by exception.
- At the end there's an optional show-and-tell for people to talk about what they did.

**When/Where:** Sundays, 4–7pm, weekly. 201 S Craig St, Unit 1E — enter from the Henry
St side.

**Here's how it usually goes:** 4:15 introductions · 4:30–5:20 focus time · 5:20–5:40
social break · 5:40–6:30 focus time · 6:30 (optional) show and tell.

**Who's it for?** People who've been wanting to work on a passion of theirs — an interp
project, a paper replication, a novel, a company — but just haven't been able to find
the time or the motivation.

**Why:** We've been procrastinating too much on our side projects even though we have so
much fun doing them. We know we're not alone in this and want to keep others accountable
for working on what they're passionate about. We've also met a ton of really fun friends
by making things we care about.

**Rules/guidelines:**

- PLEASE DON'T work on your main thing (school or your job) — if you don't know what to
  work on, we're sure we can help you find something.
- Act like a host, include people in conversations, talk to people even if they're
  strangers, offer to help out and clean up, don't network — if you're here to network we
  will be so sad. Come to make stuff and find super fun friends :)
- Bring snacks if you're feeling kind!

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
- The ringworld palette does not leak: `/mln/` and `/about/` still render forest/tan.
- Light and dark mode both legible on `/ringworld/`.
- Responsive at 375px: banner scales, grid collapses to one column, nav does not wrap
  off-screen.
