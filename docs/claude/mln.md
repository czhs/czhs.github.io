# MLn — updating the reading-club micro-site (the frequent workflow)

The MLn Reading Club micro-site lives at `/mln/` (framed as its own website, not a blog
tab). Single source of truth: `_data/mln.yml` (every card on `/mln/` + each
`/mln/week-N/` page) plus a thin stub `_pages/mln_weekN.md` per week. External source
of truth: the Luma calendar https://luma.com/mln. All copy is **verbatim from Luma**
([content-rules.md](content-rules.md)).

## Architecture

- `_data/mln.yml` — `calendar_url`, `contact_url` (unused since 2026-08-09), `weeks:`
  list. Week fields: `num, date, slug, evt, title, cover, summary, description,
  reading[]` (`{title, url}`), optional `tags`, `recording`, `symposium: true`,
  `coming_soon: true`. No `status:` field (removed 2026-07-01) — everything derives
  from `date` at build time.
- `_layouts/mln_base.liquid` — standalone shell (keeps `head.liquid`/`scripts.liquid`,
  replaces blog chrome with the MLn masthead/footer). `_pages/mln.html` — landing +
  grid logic. `_layouts/mln.liquid` — per-week detail (looks up by `page.week`).
  `_includes/mln_styles.liquid` — all CSS. `_includes/mln_card.liquid` — card markup.
  `_includes/mln_runbook.liquid` — kept but not included anywhere.
- Stubs: front matter only (`layout: mln`, `permalink: /mln/week-N/`, `week: N`,
  `standalone_title`) — except weeks with body content (e.g. week 4's systolic-array
  interactive; symposium week's sign-up link).
- **Permalinks `/mln/` and `/mln/week-N/` must NOT change** (shared publicly).
  Navigation is one-way: homepage links into MLn; the only link out is the footer
  "by Chris Shi" (plus the ringworld sibling pill — see
  [ringworld.md](ringworld.md) for the pixel-alignment contract).

## Grid behavior (all derived from `date`)

Reverse-chronological by `date`, NOT by `num`. Only the next meeting shows as its own
card ("reading now"); other upcoming weeks collapse behind a dropdown mosaic card that
sits first: `[dropdown] [coming week] [past…]`; expanding inserts future weeks between
dropdown and coming card (JS toggles `.mln-expanded`).

## Syncing from Luma (manual by request — helper script deleted 2026-06-30)

`curl -fsSL https://luma.com/mln` and each event page `https://luma.com/<slug>`; parse
`__NEXT_DATA__` JSON (`props.pageProps.initialData.data`). On an event page,
`start_at`/`url`/`api_id`/`cover_url`/`name` live under `...data.event`, but
`description_mirror` is a SIBLING of `event` — reading it off the event dict silently
returns None.

Hard-won rules, all real incidents:

- **Diff `data.event_start_ats`** (on the calendar page — holds ALL dates, past and
  upcoming) against the `date:`s in `_data/mln.yml` FIRST. A site date with no Luma
  date is a phantom week to delete (and renumber after). Gaps are real breaks — don't
  invent placeholder weeks (five-week August 2026 break was real).
- **Match site weeks to Luma by title + date, NEVER by `#N` or evt-id.** Luma
  renumbers every `#` on insert/remove; skips numbers outright; recreates events with
  new slug/evt (and sometimes hands the OLD slug to a DIFFERENT topic); moves dates
  while keeping evt; deletes placeholders same-day. Re-pull slug/evt/cover/date/name
  for every upcoming week every sync.
- **Site `num` is the honest chronological Monday counter**, not Luma's `#N` (the
  unnumbered Symposium week broke the equality permanently). On insert/remove:
  renumber `num` in the yml and rename/retitle every affected `_pages/mln_weekN.md`
  stub (permalink + `week:` + `standalone_title`); add/delete stubs as needed.
- Covers change after the fact — re-pull, don't assume stable.
- `description_mirror` is ProseMirror JSON — walk `content` nodes for text, pull
  `link` marks' `href` for reading URLs. The "Welcome to Week N:" header is often a
  stale copy-paste — use the event `name` for the title.
- Keep yml descriptions clean like existing entries: summary = the leading
  question(s); description = questions + body prose ending at "Join us at CASI…".
  Drop Luma boilerplate (📖 Reading Recommendations, When/Where, etc.). Reading-list
  `title` = paper title + authors/org, not raw anchor text.
- **Symposium-style special weeks**: `symposium: true`, no `reading:` — drives
  confetti + festive card flag (`_includes/mln_confetti.liquid`, `.is-symposium`,
  gated on `coming.symposium` / `w.symposium`).

## Coming-soon placeholder weeks

Block = `{ num, coming_soon: true, date, title: "Paper to be announced", summary }`.
Card shows dashed "coming soon" flag + striped TBA thumb (guards in `mln_card.liquid`
and `_layouts/mln.liquid`). If Luma schedules the event before the paper is picked,
keep `coming_soon: true` and add `slug` + `evt` — the page gains its RSVP iframe and
the card shows the real date; do NOT copy Luma's recycled cover onto it.

## Paper audio (GitHub release, never committed)

Audio lives on the single accumulating release tagged `mln-audio` — NOT in
`assets/audio/` (Pages has a 1 GB site cap + 100 GB/mo bandwidth; release assets are
outside both). Workflow:

1. Source mp3s arrive in `/Users/hshi/Desktop/MLn/elevenaudio/audios/`, renamed by
   Chris after the paper.
2. Rename to `mln-week-N-<topic>.mp3` (asset name = URL).
3. `gh release upload mln-audio <file>`.
4. Set `recording: "https://github.com/czhs/czhs.github.io/releases/download/mln-audio/<file>"`
   in the yml + add the `paper audio` tag.

Gotchas: served as `application/octet-stream` — browsers play it fine, Range/seek
works (verified). Sources can be enormous (5.5 h / 299 MB happened) — verify length
by sampling `mean_volume` at offsets before assuming a glitch; week 12 was re-encoded
`ffmpeg -c:a libmp3lame -b:a 32k -ac 1 -ar 22050`. Chris sometimes trims — ask, don't
guess a cut point. ~168 MB of pre-migration audio is still in git history (no rewrite
authorized). Older weeks vary in bitrate.

## Recap photos, tags, carousels

Tags on a week render icons via the `case` in `mln_card.liquid`: `photos`→📷 (group/
candid/food), `board notes`→📝 (whiteboard/flip-chart discussion boards),
`visualization`→📊, `demo`→🕹️, `paper audio`→🎙️; unknown → ✦. Combine as an array.

Adding a photo: convert (often HEIC from `~/Downloads/`) with
`magick "IMG.HEIC" -auto-orient -resize 1600x1600\> -quality 82 -strip assets/img/mln/weekN-recap.jpg`,
then in the stub body a `<figure class="mln-recap">` (full-width, uncropped — use it,
not `.mln-gallery` which crops 4:3, for anything that must stay legible/portrait).

Many-media weeks use `.mln-carousel` (pure CSS, manual only, no autoplay): hidden
radios ~ slides (figures) + thumbs (labels); first `checked` radio = first slide (put
the group photo first); slides may be img / linked img / `<video controls
preload="none">` (▶ badge via `.mln-thumb-play`). CSS covers up to 6 slides — radios,
slides, thumbs are matched by `nth-of-type`, keep counts in sync.

## Season recap reel (the band above the grid on `/mln/`)

The archive spans more than one season, so a season that has ended must be labelled
or its weeks read as the current one. **One recap band is not enough** — asked for
just the band, the club still didn't read as being in a new phase, because the grid
below it was an undifferentiated run of cards. It takes both: the band, and season
dividers inside the grid.

Everything derives from `seasons:` at the top of `_data/mln.yml` — **newest first**,
each entry just `name` + `start`. A week belongs to the newest season that opened on
or before it, so seasons need no end date and can't overlap or leave a gap. `start`
is the boundary, **not necessarily a meeting**: Fall 2026 opens Mon Aug 24, a Monday
with no session, because that is where the summer/fall break falls. Adding a season
is one entry; nothing else needs touching.

- **Which season is current is derived, never a key**: it is the season of the NEXT
  meeting, not of today's date. That difference is the whole point at a break — for
  the week between the last summer Monday and the first fall one, a date lookup still
  answers "Summer" while the club is plainly already in fall. It also means nothing
  has to be flipped by hand when a season turns over.
- **Dividers** (`_includes/mln_season_divider.liquid`, `.mln-grid-season`): full-width
  rows in the grid, `{season} ──── now | wrapped`. `_includes/mln_season_of.liquid`
  resolves a date to a season and leaks `season_of` to the caller (Jekyll includes
  share page scope) — that is what lets the grid's three passes share one
  `shown_season` pointer. The whole run is strictly newest→oldest, so one pointer is
  enough. The lead divider goes before the dropdown card and is NOT collapsible (the
  dropdown stands in for the weeks it hides); dividers inside the future run take
  `far=true`. The row is a block wrapping a flex inner — `.mln-far-week` is toggled
  with `display: block`, so a flex `li` loses its layout when revealed.
- **Recap bar** (`_includes/mln_season_recap.liquid`, `.mln-reel-*`): emitted by the
  divider include, so a season's heading and its reel arrive together. `season_recap`
  is `season, line, length, video, poster`; `season` must match a name in `seasons:`.
  It is a **bar, not a panel** — ~185px shut. One mat holding two rows: the clickable
  bar (a `<details>`, same device as the hero's "About the club" — no JS, keyboard
  free) and the season's weeks as a row of **Luma covers in polaroid frames**, one per
  week, linked, with the week number in the print's chin. The covers are the index —
  same art as each week's card below — and they replaced a row of numbered ticks.
  That row sits **outside `<summary>`** on purpose: a summary is one click target, and
  links nested in it both follow and toggle. Its range is read back out of `seasons:`
  (walking newest-first, the entry before the recap's is the one that ended it), so no
  dates are restated and it can't drift.
- **The bar is `mln-reel-`, NOT `mln-recap-`** — `.mln-recap` is already the week pages'
  full-width photo figure, and its `.mln-recap img { border-radius: 12px }` reached into
  the bar and rounded the corners clean off 46px prints. Two more traps in the same
  spot: al-folio rounds bare `img` site-wide (the prints set `border-radius: 0`), and
  the ratio must be on the `<img>` itself — `height: 100%` against a parent sized only
  by `aspect-ratio` collapsed for some covers and the prints came out mixed heights.
- **All strings are the reel's own on-screen copy** ([content-rules](content-rules.md)) —
  `line` is the reel's caption card verbatim. Don't write new copy for the bar.
- Sources are ~1080x1920 and enormous (77 MB happened). Encode
  `-vf scale=810:1440 -crf 25 -preset slow -movflags +faststart`, aac 96k → ~13 MB.
  Keep crf ≤ 26: the dark paper **grain is the look**, and crf 28 halves the file but
  flattens it to banding. Committed to `assets/video/mln/` (published, unlike the
  audio) with `preload="none"` behind the shut bar — nothing is fetched until it is
  opened; poster is a still of the reel's own end card
  (`ffmpeg -ss <t> … -vf scale=810:1440` → `magick -quality 82 -strip`).
- Bar colours are **sampled from the reel, not the theme** — the micro-site's pinned
  green is close enough to the reel's that the video would have no visible edge, so
  the mat is one step darker (`--mln-mat`) with the reel on its true ground
  (`--mln-ground`). It deliberately doesn't track the theme vars; don't "fix" that.
- Seeking won't work against `python3 -m http.server` (it ignores `Range`) — that's
  the preview server, not the file. Pages serves Range fine.

Next season: add its entry to `seasons:` (the dividers and the "now" marker follow on
their own), then swap the whole `season_recap` block once its reel exists.

## Adding a brand-new week, end to end

1. Sync from Luma (above) → new block in `_data/mln.yml` (verbatim copy) with the
   Monday `date`.
2. Add `_pages/mln_weekN.md` stub.
3. Audio/photos when they exist (above), with matching tags.
4. Local preview, then push; verify the deploy per
   [site-basics.md](site-basics.md).
