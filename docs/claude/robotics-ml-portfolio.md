# /robotics/ and /ml/ — portfolio micro-sites

Standalone portfolio micro-sites Chris shares directly with employers.

**Hard constraint: the personal site must NEVER link to `/robotics/`** — not navbar,
homepage, or pokedex. All robotics pages carry `nav: false`. The link is one-way:
robotics links back to `/` ("Personal Website" in its sidebar). This is the inverse
of MLn's one-way rule.

## Architecture

Data-driven, shared across both sites: `_data/robotics.yml` + `_data/ml.yml` drive
everything; layouts `_layouts/portfolio*.liquid` + `_includes/portfolio_styles.liquid`;
pages `_pages/{robotics,ml}.html` + `_pages/{robotics,ml}_<slug>.md` (thin — front
matter plus the write-up, nothing else needed).

Per project in the data file:

| key             | does                                                                                                                                 |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `cover`         | 4:3 still for the grid card                                                                                                          |
| `poster`        | still matching the hero video's own aspect                                                                                           |
| `video`         | hero clip; **also plays on hover** on the grid card                                                                                  |
| `media`         | gallery on the detail page — list of `{video, poster}` or `{image}`, each with `caption`, optional `wide: true` for a full-width row |
| `date`, `links` | card/detail metadata; `links` renders the pill row                                                                                   |
| `gallery_title` | optional heading over the gallery (e.g. "Footage"); also adds the chip-TOC/rail entry pointing at it                                 |

A project with no `cover`/`video` renders as an "under construction" placeholder card.
`under_construction: true` at the top of the data file adds the sidebar badge.

Grid cards lazy-load their preview: the clip URL sits in `data-src` and is only
fetched on hover, so the grid costs one poster image per card on first paint. The
script no-ops under `prefers-reduced-motion` and on touch. Cards also play on
their own, one at a time at random — but **never while any card is hovered or
focused**: hovering stops the ambient clip elsewhere and pauses the picker until
the pointer leaves (Chris, 2026-09-04).

## Design language (2026-08-26 zine re-skin; structure from the 2026-08-20 pass)

Both micro-sites now wear the **main site's zine skin**: one ivory sheet with an
8px ink border on the seafoam field, Plus Jakarta Sans for prose/display (name and
titles at weight 800), JetBrains Mono strictly for machine labelling. Fonts are
the same self-hosted files as the zine (preloaded in `portfolio_base.liquid`;
head.liquid no longer emits Google Fonts for `portfolio` layouts). The palette is
the zine's **seafoam, fixed** — literals copied from `zine_palette.liquid` into
`portfolio_styles.liquid` (keep in sync), no dark mode, `--global-*` remapped on
`body.rbx-site` so strays track it. Zine shape rules apply: squared corners, hard
offset shadows, **no transform under the cursor**. Orange stays reserved for flow
state.

- **No signature intro** (removed 2026-09-04 at Chris's request — "remove the
  signature on the robotics page"; don't re-add it). The full-screen
  self-drawing "Chris Shi" overlay and its SVG include are gone; the
  Hershey-Script generator still lives in `local/sig/sig_gen.py` (gitignored)
  if it is ever wanted back.
- **The window** (2026-09-04, after "i dont like the website scrolls a bit before
  with the website background strip at the top, the whole design needs to be
  tightened"): the ink frame is no longer a border on a sheet that scrolls — it
  is `.rbx-window` in `portfolio_base.liquid`, a `position: fixed` frame with
  the field ring painted by its `box-shadow` spread, and the sheet is the body
  itself, scrolling beneath it. `--frame` (ring + frame width) is what content
  must clear: sticky tops and every `scroll-margin-top` are
  `calc(var(--frame) + …)`. The theme's back-to-top button is hidden here.
- **Ruled grid**: the index is a contact sheet, not floating cards — no
  gutters; each card carries its bottom rule, the left card of a pair its
  right rule, the grid the outer edge; covers bleed to the rules and captions
  sit in a band. Hover is a faint field tint on the cell, tape on the number,
  a rule under the title; there is no offset shadow because cells touch. Cards
  reveal fade-only so the rules never move. An odd last card gets a filler
  cell (`::after`) so the bottom rule stays complete.
- **Sidebar**: `site_label` as a mono eyebrow over the name, the name at
  display size, 3px rules over the index and the links, links set in mono
  uppercase (wayfinding, so the machine face).
- **No asterisk mark** (removed 2026-09-04, "remove the asterisk above my name"):
  the four-line star glyph that sat above the sidebar name and beside the name in
  the detail masthead is gone; the masthead name text is still the link back to
  the index.
- **No ticker**: the capability ticker that shipped with the re-skin was removed
  the same day at Chris's request ("i dont like the scrolling bar") — don't
  re-add it. The sidebar's `about` line and `skills` list were removed from
  `_data/robotics.yml` on 2026-09-04, also at his request; the layout still
  renders them if a data file carries them. The sidebar and TOC rail also
  hide their scrollbar rails (still scrollable).
- **Reveals**: `html.rbx-armed` lands pre-paint (only when motion allowed), an
  IntersectionObserver in `portfolio_base.liquid` stamps `.is-in`; `.rbx-ready`
  is added right after arming (it used to wait for the signature intro). `[data-rv]`+`--rv` = per-element
  stagger; 10px rise on a 0.7s expo-out curve — bigger/snappier read as choppy.
  Sidebar children fade only (translating them flashes a scrollbar).
- Detail pages are a shell grid: masthead across the top, sticky TOC rail on the
  left (≥1080px), content in `.rbx-main`. The rail is **built client-side** from
  whatever rendered — stations, section headings, the write-up's own `h2`s, the
  gallery — so pages need no per-page TOC data. The b-roll section is
  deliberately NOT in it (Chris, 2026-09-04). It scroll-spies, and
  mirrors the run's `is-on`/`is-done` onto its rows (orange = flow state). The
  chip TOC still renders under 1080px.
- The index sidebar carries a numbered project manifest (anchors to `#p-<slug>`
  cards). Card numbers = grid order = curation order.

## Gotchas that cost time

- **Anything injected after load that carries a reveal class (`.rbx-shot`,
  `[data-rv]`, …) starts at opacity 0 and stays there** unless the observer in
  `portfolio_base.liquid` is told about it — dispatch
  `rbx:reveal` with `{ detail: { root } }` after injecting. The unlocked
  pie-robot b-roll was invisible for two weeks this way (2026-08-26 reveal
  system → found 2026-09-04, "the b-roll seems to be broken").

- Gallery grid needs `align-items: start`. The footage mixes portrait phone video
  with landscape CAD stills; the default `stretch` leaves a dead gap under whichever
  tile is shorter.
- Don't clamp gallery media height — a portrait clip just letterboxes.
- Card still is `cover | default: poster`, not the reverse: a portrait poster
  cropped into the 4:3 card loses the subject.

## Media

Real images/video go in `assets/img/robotics/` + `assets/video/robotics/` (and the
`ml` equivalents), which are **gitignored** — see [site-basics](site-basics.md).
Raw source lives in `robotics_media/` (multi-GB, also gitignored).

**Publishing means uploading to the `robotics-media` GitHub release, never
committing** (2026-08-20, the MLn paper-audio trick — assets live outside git and
the Pages budget). How it's wired:

- `media_base:` in `_data/robotics.yml` holds the release download prefix. In
  **production** builds (`jekyll.environment`), `_includes/portfolio_src.liquid`
  rewrites every media path to `media_base + basename`; locally the same paths
  serve from the gitignored dirs, so preview works offline. Because release
  assets are a flat namespace, **basenames must stay unique** across img+video.
- Publish/replace: `gh release upload robotics-media <files> [--clobber]`. The
  release must contain every file the data file references — the b-roll clips
  referenced only inside the encrypted payload included (upload the whole dir).
- The b-roll gate remaps `assets/{img,video}/robotics/...` paths inside the
  decrypted HTML onto `media_base` at runtime, so the ciphertext never needs
  re-encrypting when hosting moves.
- GitHub serves release assets as `application/octet-stream` behind a 302 —
  browsers sniff and play them fine in `<video>`/`<img>` (MLn verified `<audio>`
  plus range requests earlier).

## Playback gotchas (the "flash artifact")

Chris reported a flash on many clips (2026-08-20). The clips and posters were
innocent — posters are pixel-exact frame-0 extracts once you compare in the same
color range (limited-range video YAVG vs full-range JPEG YAVG differs by
`(Y-16)/219*255`; don't re-diagnose that). The real causes, both presentation:

- **Never rewind a clip while it is visible.** The card script reset
  `currentTime = 0` in `stop()`, mid-fade-out — a visible snap on every
  hover-end and ambient stop. Rewind belongs in `start()`, while the preview is
  still at opacity 0, and station players only rewind a clip that has played
  (`v.currentTime > 0`) so a fresh poster never drops early.
- **Never cross-fade cover and preview simultaneously.** Both semi-transparent
  mid-fade let the page background glow through (≈25% at midpoint). The cover
  stays opaque; only the preview fades in on top.

Encoding used for the web clips: `libx264 -crf 26 -preset slow`, long side capped
at 1280, `-an`, `+faststart`.

Finding the good moments in a long static-camera recording: score _localised_
change while the whole frame is quiet (camera parked). Scoring whole-frame change
just surfaces people walking past and the camera being picked up.

## Duck renders

The Duck project's clips are **MuJoCo renders of the open-source Open Duck Mini v2**
(<https://github.com/apirrone/Open_Duck_Mini>), not footage of the physical build —
label them as renders and keep the upstream credit. The rig lives outside the repo
in the session scratchpad: a studio scene that includes the project's own
`robot.xml`, kinematic posing (no dynamics, so nothing topples), feet re-planted on
the floor every frame, and a camera auto-framed from the rendered silhouette.
Standing pose is taken verbatim from the robot's runtime `HWI.init_pos`.

Loops are built only from sin/cos of integer multiples of `2*pi*t` so they close
seamlessly.

**Physical plausibility is checked, not eyeballed** (`validate.py` in the rig dir).
Two rules, both of which authored curves break constantly:

- _Feet stay on the floor._ The rig plants the lowest foot vertex and then applies
  `dz`, so a positive `dz` hovers the whole robot and a negative one drives its
  feet through the floor. Hardware can only raise its body by straightening its
  legs — use `rig.rise(dh)` instead, which is calibrated against the real leg
  geometry (about −10 mm to +13 mm). One foot lifting is fine when the action
  means it; both feet leaving the ground is a jump.
- _Nothing outruns the servos._ The Feetech servos cap at **5.24 rad/s**
  (`max_motor_velocity` in the robot's own runtime). Over that and the motion
  reads as a teleport. Aim under ~4.7 so a re-check doesn't creep back over.

Judge the seam **relative to the clip's own motion**, not against a fixed number.
A wrap only pops if the last→first step is bigger than a typical frame-to-frame
step; on a fast clip a large absolute seam is just one more ordinary frame. The
bounciest loop here measures a seam of 1.92 against a median frame step of 2.22 —
invisible — while a slow clip with a seam of 0.75 is the one closest to showing.

**Camera, or how to give the duck a face.** Its two coloured lenses sit at the
bottom of circular bores in the upper plate of the wedge head, and those bores
point forward and slightly _down_. So the camera has to look _up_ into them:
near-frontal azimuth (~175–186) with **positive** elevation. Shot from the
default three-quarter-and-above angle the lenses render zero coloured pixels —
the head is a blank grey wedge and the robot has no face at card size.

Do not score this by counting saturated pixels over the head: from behind-ish
azimuths that mostly counts the yellow antenna-holder discs, so the metric
rewards shooting the duck's back. Count green and blue only, or isolate the lens
geoms the way `Rig.robot_mask` isolates the robot (hide them, render, diff).

## Duck card cover

`duck-card.jpg` (2026-09-16, "get a better cover for the duck") is the real
robot standing, **cut out of its background** and set on the sheet's ivory
(#fffcf2): `bin/robotics_pdf/frames/duck-standing-cutout.png` scaled 1.46x to
612×756 and centred on a 1200×900 card, robot top at 10% of the height. It
replaced `duck-cover.jpg` — the same instant of `duck-stands-free.mp4` (16.5 s,
`crop=720:540:10:30`) as a plain frame — because Chris ruled out his legs and
then his socks in any picture, and every frame of the robot standing has both
behind it. A real-photo alternative was cut and rejected as the card: the robot
face-up on the bench (`duck-face-mounted.mp4` 8.25 s, `crop=600:450:0:475`
scaled 2x) reads as wiring, not a biped; it is kept at
`bin/robotics_pdf/out/cand-duck-card/duck-card-bench-alternative.jpg` locally.
Not a render, on purpose: the card has no caption to say so. The PDF cover
sheet uses the same card (`COVER_STILL` in build.py is empty again).

## Robot Dog and Pie Robot card covers (2026-09-16)

Chris: "for robot dog also use an actual photo of the dog" (this supersedes the
2026-09-04 "cover image is the CAD"). `robot-dog-card.jpg` is
`robotics_media/Dog/final_dancing.MOV` frame 174 (5.806 s), `crop=1200:900:550:60`
at 1:1 (no resampling), light unsharp — the sharpest frame of the dance's only
fully upright pause; the CAD render (`robot-dog.jpg`) stays as the detail page's
lead figure. `pie-robot-card.jpg` replaces `pie-robot.jpg` (a soft 720×540 crop
of the door-open frame): `robotics_media/Pie Day Bot/IMG_9022.MOV` at 227.71 s
(1080×1920 upright after its −90° rotation tag), `crop=1080:810:0:520`, scaled
1080×810 → 1200×900 (an 11% upscale; every raw recording is 1080 wide), light
unsharp — the arm in the open microwave with the cup just placed on the
turntable, inside a 0.6 s pause where the arm is still. Candidate sheets and
scores for all three cards are under `bin/robotics_pdf/out/cand-*-card/`
(gitignored). All three new cards were uploaded to the `robotics-media` release
the same day; the old `duck-cover.jpg`, `pie-robot.jpg`, `robot-dog.jpg` assets
stay on the release (`robot-dog.jpg` is still the detail page's lead poster
pattern's neighbour; the other two are simply unreferenced now).

## Duck build footage

The real-build half of the Duck page is cut from 18 parked-camera recordings
Chris made 2025-07-10 → 2025-07-20 plus a later "Test Runs" session, all
uploaded unlisted to YouTube. Several links he sent are **re-uploads of the same
recording** — match by exact duration before scanning one twice. Their titles
carry true wall-clock times and correct the dates: Soldering Pi0 2W is
2025-07-15 19:24, the IMU/breakout session 2025-07-17 14:25, Wiring IMU
2025-07-17 23:54, the battery pack 2025-07-19 12:21.

Provenance for every published clip, so any of them can be re-cut or re-trimmed:

| clip                 | source video id | in–out          |
| -------------------- | --------------- | --------------- |
| `duck-servos-row`    | rAhlPlxkDxw     | 0:38:50–0:39:03 |
| `duck-servo-lens`    | rAhlPlxkDxw     | 1:21:26–1:21:34 |
| `duck-cable-taut`    | fO7611h1tWY     | 0:05:06–0:05:18 |
| `duck-solder-pi`     | 0e6U15X6shE     | 0:50:10–0:50:18 |
| `duck-solder-board`  | GR5xH0AR-9Y     | 0:24:29–0:24:44 |
| `duck-plate-held`    | GR5xH0AR-9Y     | 2:09:31–2:09:39 |
| `duck-pack-dressing` | do4Ut-umoRg     | 1:34:22–1:34:40 |
| `duck-face-mounted`  | do4Ut-umoRg     | 1:35:58–1:36:14 |
| `duck-stands-free`   | gbBtn4WpPdw     | 0:54:04–0:54:21 |
| `duck-walk` (hero)   | P7CkNshfkWI     | 1:05:16–1:05:31 |

Two clips are published **cropped**, so a re-cut has to re-apply the crop. Chris is
seated in both shots with his legs, feet and the controller in frame (cropped out
2026-08-20). `duck-walk` uses `crop=370:570:230:150`: his socks start at y≈570 and
the robot's own sweep runs down to y≈660, so no full-width bottom cut can lose the
legs without clipping the robot — only a tight crop onto the sweep does both.
`duck-surge-topple` uses `crop=600:672:0:0` plus `-t 12.2`; full width works there,
but a hand reaches in to pick the robot up from ~12.3s and rises above any usable
crop line, so the clip now ends on the landing instead of the pickup.

**The robot moving under its own power is in `P7CkNshfkWI` ("Test Runs")**,
and nowhere else. It is a **teleoperation** session — a game controller with a
lit blue LED is in Chris's hand from 0:10:01 — driven in five bouts, of which
only the last is a sustained walk: upright from 1:04:13 to 1:05:59 without
falling, setting off at 1:04:36, travelling in bursts, turning a quarter circle
and walking out of frame. No hands-free clip may start before **1:04:13**; a
spotting hand is at or beside the robot until 1:04:12.6. Because the camera
looks almost straight down the body occludes the legs, so alternating footfalls
were never resolved — say "moving under its own power", and reserve "walking"
for 1:04–1:06.

**A false positive to learn from.** An earlier pass published `_fELXUy8f9w`
0:41:45 as the first powered motion: the robot stood on the bench, hands came
away, and a leg swung a repeating arc for two minutes. It was wrong, and the
reasoning is the trap — **a leg hanging from a hip joint is a pendulum, so a
fixed period is what passive swinging looks like**, and hands out of frame only
rules out a _visible_ hand, not support from below. To call motion powered,
show that it is _driven_: amplitude that does not decay (a free pendulum's
does), motion against gravity, coordinated joints, whole-body translation, or a
state change you can point at. On the real walk the discriminator that settled
it was blob area falling ninefold as the robot receded — drift cannot change
apparent size.

`gbBtn4WpPdw` was shot with the phone on its side: the picture sits **90° CCW**
inside the pillarbox, so it needs `transpose=2` after the crop. Everything else
is upright. Most recordings are portrait letterboxed inside 1920x1080, so the
real picture is only 600x1068 — don't upscale them to a 1280 tile.

**The recording titles are not all accurate.** `GR5xH0AR-9Y` is uploaded as
"Soldering IMU and Breakout Board pt.1" but is actually **soldering the
microphone** — Chris's correction, so the page's station says microphone while
the docs keep the YouTube title for lookup. Treat the other titles as claims to
check rather than facts, and note that its 33-second "pt.2" contains nothing at
all.

Two component labels are legible at source resolution and were read off the
frames, not inferred: `STS3215 / 7.4V` (FEETECH) on the servo at rAhlPlxkDxw
1:21:29, and `HEXTRONIK / HXT900` at GR5xH0AR-9Y 2:09:31. The blue tape labels
in the same recording read as joint names and IDs ("head yaw 32", "right knee
13"). Verify before any of it becomes copy.

**Sampling long recordings: `fps=1/N` lies about time.** ffmpeg's `fps` filter
emits its first frame half a step in, so a frame labelled `n*step` actually
sits at `n*step + step/2` — 10 s out when sampling every 20 s. Add the half
step when labelling, or every timestamp handed to a cutter is early.

## TartanIMU figures

The card art is **real output from the demo's own model**, not a screenshot of the
UI: the Space (<https://huggingface.co/spaces/HongyiShi/TartanIMU-Demo>) is on
free-tier CPU and a single example did not return in six minutes, so inference was
run on the `hshi4090` box instead and the figures pulled back.

How to redo it: `snapshot_download(repo_type="space")` the Space onto the 4090,
stub `gradio` (app.py only needs `gr.Error` at import), then call the Space's own
`run_inference` / `make_imu_figure` / `make_trajectory_figure` so the plots are
identical to what the demo would draw. Its extra deps are `wandb einops pypose
termcolor rich transformations`.

**The gotcha:** the dataloader infers motion type from the file's **parent
directory name** (1 car / 2 dog / 3 drone / 4 human) — which is why `predict()`
stages every upload into a `human/` dir. Hand it the raw `examples/…npz` path and
you get motion type 0 and a bare `ValueError: Unknown motion type: 0` that looks
like a broken model. `run_inference` returns `(traj, net_attr, inference_time)`,
not just the trajectory dict.

Measured on the bundled `LIN_ios_2022-01-19` example: ATE 1.4684 m, translational
RTE 0.2044 m, drift RTE 0.2298 m, velocity RMSE 0.0903 m/s, inference 0.35 s.

## TartanIMU write-up

Drafted 2026-08-20 at Chris's direction, in the gantry-page voice, from his own
engineering notebook (`TartanIMU - Chris - Engineering Notebook.pdf`, a
group-meeting log 2025-10-28 → 2026-03-31). Every number on the page traces to
that PDF or to this file — do not "improve" figures from memory. Deliberately
left out of the public page: teammates' names, hostnames/IPs/passwords the
notebook contains (it has several — never quote the notebook wholesale), and
lab-internal plans (benchmark paper, competition/withheld-ground-truth ideas).
The end-of-March dataloader audit described on the page was a Claude-assisted
session in the notebook's screenshot; the page phrases it neutrally ("the
dataloader got a line-by-line audit") — Chris to decide if he wants the tool
credited. Chris confirmed (2026-08-20) naming the AirLab and stating his
research span there as fall 2025 through summer 2026 — that span is his own
statement, wider than the notebook's 10/28→3/31 window, and the card date
matches it ("Fall 2025 – Summer 2026").

## Robot Jousting (joust)

Added 2026-09-15 at Chris's request ("add robo jousting to my personal website
robotics portfolio as the first item") — the first project in `_data/robotics.yml`
(grid order = curation order), page `_pages/robotics_joust.md`, at `/robotics/joust/`.

Chris's brief while it was built: "mostly focus on the robotics rather than the
gameplay which should be minimal" — so the entry carries **no game screencaps**;
the crowd/phone side is carried by the intro text and the demo clip only. Also:
"make new media as well as you see fit to make it look super good"; "when doing
animations try to use the calibrated versions when possible to make the blades hit
each other"; "I really like the cinematic moving camera/drone camera during the
sword swings makes it super cool". Future renders should keep to that brief: blades
that actually meet, one continuously moving camera.

**Copy rule for this entry.** Every prose string — blurb, tagline, intro,
build_notes, the run's `desc`/`tech`, section notes, the page body — is verbatim
from one of three places: Chris's own write-up at `/robo-jousting/`
(`_pages/robo-jousting.md` on main), the footage sidecar captions he edited
(`hackcmu26/video/footage/*.json`, each marked "user-edited, use as is"), or
`robot-jousting/README.md`. Captions on the new MuJoCo renders only describe what
the render shows. No prose comes from anywhere else.

Source material lives outside this repo, in `/Users/hshi/Desktop/hackcmu26/video/`:
real phone footage in `footage/` (HEVC 1920x1080 `.mov`, upright, with sidecar
`.json` captions), the 1080p MuJoCo/CAD masters in `clips/` (documented in
`clips/README.md`), stills in `stills/`.

Web files are `assets/video/robotics/joust-*.mp4` + `assets/img/robotics/joust-*.jpg`
— gitignored, published to the `robotics-media` release like everything else; every
basename carries the `joust-` prefix so the flat release namespace stays unique.
Encode: `libx264 -crf 26 -preset slow`, 1280 wide, `-an`, `+faststart`; posters are
frame-0 extracts.

Provenance, so any clip can be re-cut:

| web file | source |
| --- | --- |
| `joust-blockhigh` | `robot_exchange_blockhigh.mov` |
| `joust-blockmid` | `robot_exchange_blockmid.mov` |
| `joust-attackleft` | `robot_exchange_attackleft_blockright.mov` |
| `joust-bout` | `robot_full_bout.mov` from 1.5 s at 3x (`setpts=PTS/3`, 12.4 s) |
| `joust-calibration` | `robot_bts_calibration.mov` |
| `joust-rig` | `robot_bts_hardware.mov` |
| `joust-expo` | `assets/img/robo-jousting/tilt_demo.mp4` (the crowd demo; video stream copied, audio dropped) |
| `joust-hero` | the three exchange `.mov`s concatenated (the card's hover clip) |
| `joust.jpg` (card cover) | `robot_exchange_blockhigh.mov` at 2.6 s, `crop=1440:1080:240:0` scaled to 1200x900 |
| `joust-sim-orbit` / `-clash` / `-reel` / `-cad-blades` / `-cad-wrists` | `clips/sim_orbit_engarde` / `sim_clash` / `sim_reel_moves` / `cad_blades_turntable` / `cad_wrists` |
| `joust-sim-pipeline.jpg` | `stills/sim_pipeline_still.png` |
| `joust-cad-fang.jpg` | `assets/img/robo-jousting/full_arm_8in_fang.webp` on main |

**New renders (2026-09-15)**, made by
`/Users/hshi/Desktop/hackcmu26/video/render/shot8_portfolio.py` (run from
`robot-jousting/sim` with `../.venv/bin/python`; modes `probe` / `twins` / `bout`;
per-beat carriage spacing lives in `shot8_spacing.json` next to it): masters
`clips/sim_twin_blockhigh.mp4`, `clips/sim_twin_blockmid.mp4`,
`clips/sim_twin_attackleft.mp4`, `clips/sim_bout.mp4` → web `joust-sim-twin-*` and
`joust-sim-bout`. Every arm motion replays `arm/motions_tuned.json` unchanged; the
bout chains `EN_GARDE_OPENER`, the three beats (carriages charge in to the beat
spacing, arms return to REST while carriages back off to 0.11 m retraction) and
`SAMURAI_FINISH`, with smootherstep blends between them. Camera: one continuous
flight per clip, keyed in output time through a time-parameterised (Barry-Goldman)
Catmull-Rom, with 4x slow motion for 0.5 s around each blade contact and a
0.7–0.9 s frozen-time orbit at the contact instant.

**"Calibrated" spacing.** There are no separate calibrated motion files — the
collision-intent doc (`robot-jousting/docs/collision_intent.md`) describes
hand-calibrated contact poses. The probe measured closest blade-axis distance
against carriage retraction, and the spacing per exchange was chosen so the blades
genuinely touch: chop vs. high bar at 0.060 m retraction (0.667 m between pan
axes: 0.05 cm, real blade-on-blade contact); chop vs. low guard at 0.0315 m
(0.61 m, `pair.py`'s spacing — the chop's tip rests on the guard hand, the designed
"hit lands"); low slash vs. right guard at 0.0315 m (0.61 m: blades meet, one
contact sample). At the real charge-in stop (0.5469 m) the chop misses the high bar
by 6 cm and the slash drives through the guard, so don't render those at 0.

Gotchas: `shot_common.build` recompiles the scene, so any new render script has to
go through it (it calls `arena.finish_model`). Camera azimuth 90 puts arm A
(yellow, red blade — the attacker in all three filmed exchanges) on the LEFT,
matching the real footage. MuJoCo's contact `dist` is negative for penetration, and
a fast sweep into a held guard can show up to ~1 cm for a single sample — why the
closer spacings were rejected. The contact instant each flight freezes on is the FIRST
blade-on-anything contact inside the beat (falling back to the blades' closest
approach) — for the chop into the low guard the blades never meet, the tip lands on
the gripper, and the closest blade-to-blade approach is at the end of the hold,
which put a camera key out of order on the first pass. Keep every elevation
negative: a positive elevation is a lens below the target, which for a low contact
point put it under the floor plane and rendered the far arm as a grey ghost
(`Cam.mjcam` now clamps the lens to 10 cm off the floor).

Links row on the page: Code (`github.com/avnithv/robot-jousting`), Write-up
(`/robo-jousting/` — linking from robotics to the main site is allowed; the reverse
never is), Trailer (`youtu.be/Ol8j64tkMzg`), Demo (`youtu.be/c6h_7mXpHWY`).

## The portfolio PDF (2026-09-16)

`assets/pdf/chris-shi-robotics-portfolio.pdf` is a one-page-per-project PDF
edition of /robotics/ — a cover with the table of contents, then one landscape
page per project, in the zine skin — linked from the sidebar as "Portfolio PDF"
(a `.pdf` link opens in a new tab like an external one; `portfolio.liquid`).
Chris asked for it 2026-09-16: "custom made PDF, 1 page per project, laid out
nicely and visually lots of images, cover with table of contents, not like a
CV", and "keep it decently professional".

Built by `bin/robotics_pdf/build.py` (tracked; `out/` and `frames/` are
gitignored) from HTML rendered through Playwright's Chromium:

- `style.css` is the design system — the portfolio palette/type literals
  copied from `portfolio_styles.liquid` (keep in sync), 11 x 8.5 in pages as
  1056 x 816 CSS px, primitives `.fig` / `.contact` / `.run` / `.lead` /
  `.prose` / `.specs` / `.links`. `CONTRACT.md` is the page contract.
- `pages/<slug>.html` is each project page's **body only**; the build writes
  the masthead (number, title, date from the data file), the footer (the live
  page URL, page number) and the cover (index rows + a contact sheet of the
  covers) from `_data/robotics.yml`, so order, titles and dates have one source.
- Images: `img/<basename>` = `assets/img/robotics/`, or `frames/<name>.jpg`
  cut from the published web clips with ffmpeg (posters are frame 0, the
  contact/action frame is usually mid-clip). The build **rejects** an image the
  data file does not attach to that project, and the gated pie b-roll always.
- Copy on every page is verbatim from the data file or the page stub, trimmed
  to whole sentences — same rule as the site ([content-rules](content-rules.md)).
- The build measures every element after layout and refuses (`exit 2`) if
  anything runs past its sheet, is clipped, failed to load, or is tiny; the
  PDF page count must equal the number of `.page` sections (an 816px page that
  spills makes a blank extra page). `--only <slug> --png` renders one page to
  `out/only-<slug>/png/` for review; `--png` renders them all.
- Regenerate + publish: `python3 bin/robotics_pdf/build.py && cp
  bin/robotics_pdf/out/robotics-portfolio.pdf assets/pdf/chris-shi-robotics-portfolio.pdf`,
  then commit the PDF (about 5 MB, in git like the other assets/pdf files —
  not on the media release, so it opens inline at chrisshi.com).
  The pages were written 2026-09-16 by one agent per project, the joust page
  first as the reference for density and hierarchy.
- **No legs, no socks** (Chris, 2026-09-16, while the duck page was built: "I
  dont want my legs in it", then "remove the socks while youre at it"). The
  duck page's standing robot is a subject cutout of `duck-stands-free` at
  16.5 s — macOS Vision's `VNGenerateForegroundInstanceMaskRequest`
  (`tools/cutout.swift`, which also records the sock rectangles) isolated
  robot + socks, then the socks were erased with rectangle alpha masks in PIL
  — the finished PNG is the one tracked file under `frames/` — and
  it sits on the ivory sheet with `object-fit: contain`. `COVER_STILL` in
  build.py swaps the cover sheet's duck cell for a Test Runs frame with
  neither, since the site's `duck-cover.jpg` card still shows both. Frames
  from the `surge-topple` and `walk` clips are already cropped clear of him.

## Content

Bodies, dates and captions are **Chris's to write** — do NOT fabricate write-ups,
specs, or dates ([content-rules](content-rules.md)). Credit quantifiers matter:
the Robot Dog and Hack 100 pages were team builds, and on 2026-09-04 Chris asked
for "all"/"every"/"self-designed" claims to be softened ("many of them
self-designed", "partly self-designed CAD", "some of the parts") without stating
who did what — keep new copy on those pages to that standard. Captions may be lifted verbatim
from his own source filenames; otherwise leave them blank.

To add a project: append to `projects:` in the data file + add the
`_pages/<site>_<slug>.md` stub.
