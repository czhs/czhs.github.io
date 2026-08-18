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
or its weeks read as the current one. Driven entirely by two keys at the top of
`_data/mln.yml`: `season_now` (the season running) and `season_recap`
(`season, from, until, line, length, video, poster`). Markup is `.mln-season` in
`_pages/mln.html`; CSS is the `season recap band` block in `mln_styles.liquid`.

- The rail pairs **`{season} — wrapped`** with **`{season_now} — now`**. That pairing
  is the point — drop `season_now` and the recap silently reads as current.
- `from`/`until` are the season's first and last meeting dates; the numbered week
  strip is filtered out of `weeks:` by that range, so it can't drift from the archive.
- **All strings are the reel's own on-screen copy** ([content-rules](content-rules.md)) —
  `line` is the reel's caption card verbatim. Don't write new copy for the band.
- Sources are ~1080x1920 and enormous (77 MB happened). Encode
  `-vf scale=810:1440 -crf 25 -preset slow -movflags +faststart`, aac 96k → ~13 MB.
  Keep crf ≤ 26: the dark paper **grain is the look**, and crf 28 halves the file but
  flattens it to banding. Committed to `assets/video/mln/` (published, unlike the
  audio) with `preload="none"`; poster is a still of the reel's own end card
  (`ffmpeg -ss <t> … -vf scale=810:1440` → `magick -quality 82 -strip`).
- Band colours are **sampled from the reel, not the theme** — the micro-site's pinned
  green is close enough to the reel's that the video would have no visible edge, so
  the panel is a mat one step darker (`--mln-mat`) with the reel on its true ground
  (`--mln-ground`). It deliberately doesn't track the theme vars; don't "fix" that.
- Seeking won't work against `python3 -m http.server` (it ignores `Range`) — that's
  the preview server, not the file. Pages serves Range fine.

Next season: swap `season_now`, then swap the whole `season_recap` block once its
reel exists.

## Adding a brand-new week, end to end

1. Sync from Luma (above) → new block in `_data/mln.yml` (verbatim copy) with the
   Monday `date`.
2. Add `_pages/mln_weekN.md` stub.
3. Audio/photos when they exist (above), with matching tags.
4. Local preview, then push; verify the deploy per
   [site-basics.md](site-basics.md).
