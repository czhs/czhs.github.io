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

A project with no `cover`/`video` renders as an "under construction" placeholder card.
`under_construction: true` at the top of the data file adds the sidebar badge.

Grid cards lazy-load their preview: the clip URL sits in `data-src` and is only
fetched on hover, so the grid costs one poster image per card on first paint. The
script no-ops under `prefers-reduced-motion` and on touch.

## Layout notes (2026-08-20 design pass)

- Detail pages are a shell grid: masthead across the top, sticky TOC rail on the
  left (≥1080px), content in `.rbx-main`. The rail is **built client-side** from
  whatever rendered — stations, section headings, the write-up's own `h2`s, the
  gallery, the b-roll — so pages need no per-page TOC data. It scroll-spies, and
  mirrors the run's `is-on`/`is-done` onto its rows (orange = flow state, per the
  design language). The chip TOC still renders under 1080px.
- The index sidebar carries a numbered project manifest (anchors to `#p-<slug>`
  cards). Card numbers = grid order = curation order.
- Design tokens (`--tape`, `--rail`, `--mono`) live on `body.rbx-site`; all other
  color comes off the `--global-*` theme vars, so both themes track the main site.

## Gotchas that cost time

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

## Content

Bodies, dates and captions are **Chris's to write** — do NOT fabricate write-ups,
specs, or dates ([content-rules](content-rules.md)). Captions may be lifted verbatim
from his own source filenames; otherwise leave them blank.

To add a project: append to `projects:` in the data file + add the
`_pages/<site>_<slug>.md` stub.
