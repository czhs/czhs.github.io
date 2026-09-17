# Robotics portfolio PDF — page contract

One landscape page per project (11 x 8.5 in), a cover with the table of contents
in front, in the /robotics/ site's own zine skin. The PDF is a deliverable Chris
hands to employers, so the tone is **decently professional**: restrained,
image-led, ruled grids, no gimmicks, no filler.

## The two rules that override everything

1. **No invented copy.** Every sentence, caption, label and note on a page is
   verbatim from one of two places, and nowhere else:
   - `_data/robotics.yml` — that project's `blurb`, `tagline`, `intro`,
     `build_notes`, `specs`, `links`, the `run` stations' `label`/`note`/`desc`/
     `tech`, every media `caption`, `gallery_title`, `sections[].title/note`.
   - `_pages/robotics_<slug>.md` — the page body (paragraphs, headings, bullet
     text, figure captions in that file). Read it with `cat`; Liquid tags and HTML
     comments are not content.
   You may **trim to real phrases** (drop whole sentences, cut a paragraph short
   at a sentence boundary, use a heading as a label) but never reword, merge,
   summarise, or add connective text. A blank caption in the data stays blank —
   show the image with no caption band. If a project has little copy, the page is
   image-led; do not pad it.
2. **Only that project's images.** `img/<basename>` for any still the data file
   or page stub attaches to the project (the build enforces the list), or
   `frames/<name>.jpg` for stills you cut from that project's clips in
   `assets/video/robotics/` with ffmpeg (name must start with the project's
   prefix, e.g. `frames/duck-walk-3s.jpg`). Never `pie-robot-broll-*` — that
   b-roll is password-gated on the site.

## What you write

`bin/robotics_pdf/pages/<slug>.html` — the **body only**. The build wraps it in the
masthead (number, title, date) and footer (the live URL, page number). Your
fragment is one block that fills the body: about **964 x 627 px**. Put an optional
`<style>` at the top, scoped under `#p-<slug>` so nothing leaks to other pages.

The stylesheet is `bin/robotics_pdf/style.css`; read it, it is the design system.
Primitives:

- `.grid` (CSS grid, `height:100%`; set `grid-template-columns/rows` inline, gap
  via `--g`), `.stack` (flex column), `.fill`, `.push` (margin-top:auto).
- `.lead` (the one large line — a `tagline`, else the `blurb`), `.prose` (10.5px
  body copy; `<p>` verbatim), `.eyebrow` (tiny mono, green), `.h` (small ruled
  heading — a section title or a `##` heading from the stub), `.note` (mono
  small), `.soft`.
- `.specs` (`<ul>` of mono chips from `specs`), `.links` (`<a>` rows: `<span>`
  label + `<span class="url">` the URL; make site-relative URLs absolute on
  `https://chrisshi.com`).
- `<figure class="fig"><img src="…"><figcaption>caption</figcaption></figure>` —
  one framed still; the image fills its grid cell and is cropped, so **give the
  row an explicit height** (`1fr`, px, `minmax(0,1fr)`) and steer the crop with
  `style="object-position: 50% 30%"`. Omit the figcaption if the caption is
  blank.
- `.contact` — ruled contact sheet (ink rules, no gutters): `--cols`, `--rows`
  or explicit templates; children are `<figure class="cell">` with the same
  img/figcaption shape. `<span class="cap-title">` inside a figcaption gives a
  bold sans line above the mono caption.
- `.run` — station strip for a `run:` block: `<div class="stn"><div
  class="stn-head"><span class="stn-num">01</span><span class="stn-label">…
  </span><span class="stn-note">…</span></div><img …><div class="stn-desc">…
  </div></div>`. Omit `.stn-note`/`.stn-desc` when the data has none.

Look at `pages/joust.html` — the reference page — before you start, and match
its density and hierarchy: one lead line, a short column of real copy, one
dominant image, then a ruled strip or sheet of supporting stills with their
captions. Portrait phone frames (720x1280) belong in tall cells or a strip of
three to five; landscape frames in wide cells. Text should never be smaller than
the sizes the classes set; if copy does not fit, cut whole sentences, do not
shrink type.

## Build, look, fix, repeat

```
python3 bin/robotics_pdf/build.py --only <slug> --png
```

writes `bin/robotics_pdf/out/only-<slug>/png/p-<slug>.png` (look at it with the
Read tool) and prints `layout: OK` or a list of issues: anything that runs past
the sheet, clipped text, a failed image, an image outside the project's media
set, a tiny image. **Do not finish with a single issue outstanding.** Then judge
the picture: is every image legible at its size, are crops on the subject (not a
wall, not a floor, not someone's legs — use `object-position`), is there dead
space or a crowded corner, does it read at a glance? Iterate until it looks like
a page from a printed portfolio.

Frames: `ffmpeg -v error -y -ss <sec> -i assets/video/robotics/<clip>.mp4
-frames:v 1 -q:v 3 bin/robotics_pdf/frames/<prefix>-<what>.jpg`. Cut a few
candidates, tile them with `magick montage -font
/System/Library/Fonts/Supplemental/Arial.ttf … -tile 5x -geometry 320x180+4+4`
into `bin/robotics_pdf/out/`, look, pick. A frame that shows the subject mid-action
beats the poster (posters are frame 0, usually the pose before anything happens).
Check the docs for crop rules before cutting: `docs/claude/robotics-ml-portfolio.md`
records which duck clips are published cropped and why (legs/hands out of frame).

## Report back

When done, reply with: the images used (and which are new frames, with clip +
timestamp), every piece of copy on the page and where each came from (data key
or stub paragraph), anything you trimmed, and the final `build.py` output.
