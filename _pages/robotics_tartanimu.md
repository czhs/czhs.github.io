---
layout: portfolio_post
portfolio: robotics
permalink: /robotics/tartanimu/
project: tartanimu
standalone_title: "TartanIMU — Chris Shi"
nav: false
---

<!-- Media lead, same pattern as the gantry page: this project has no `run:` block,
     so the layout builds no hero and the lead figure lives here. The trajectory
     figure is deliberately NOT in the data file's `media` list to avoid showing
     it twice; the rest of the gallery still comes from _data/robotics.yml. -->

{% assign rbxd = site.data[page.portfolio] %}
{% if jekyll.environment == 'production' and rbxd.media_base %}{% assign mb = rbxd.media_base %}{% else %}{% assign mb = '' %}{% endif %}

<figure class="rbx-shot" style="margin: 0 0 2rem">
  <img class="rbx-shot-media" src="{% include portfolio_src.liquid path='assets/img/robotics/tartanimu-traj.jpg' base=mb %}" alt="Predicted trajectory against ground truth in six panels: X-Y, X-Z and 3D views, position error over time, per-axis position, and cumulative distance.">
  <figcaption class="rbx-shot-cap">The demo's own output on its bundled example — an iOS capture travelling about 45 m. Prediction against ground truth in three views; the bottom-left panel is the honest one, position error compounding over time.</figcaption>
</figure>

TartanIMU is a learned inertial odometry project in the AirLab at Carnegie
Mellon, where I did research from fall 2025 through the summer of 2026. The
problem is odometry from an IMU alone: take the raw stream — three axes of
acceleration, three of angular velocity — and recover the trajectory the sensor
travelled, with no camera, no GPS, nothing else.
The ambition is a foundation model for inertial data: one network trained across
four motion types — car, dog, drone, human — rather than a model tuned per
platform. I joined at the end of October 2025 to build the data side, and this
page is written from my engineering notebook, 28 October through the end of March:
preprocessing, training, evaluation, a public demo, and a long line of bugs.

An IMU is a drift machine, which is what makes the problem worth learning.
Position is acceleration integrated twice, so a constant accelerometer bias grows
quadratically in position, and every gyro error tilts the estimate of where
gravity points, which the double integration converts into position error too.
Pure integration is unusable within seconds; the learned bet is that motion has
structure — a walking gait, a drone's dynamics — that a network can use to hold
the drift down.

The model is the small part of that bet; the data is the project. And nothing on
the data side fails loudly. A mechanical build fails where you can hear it — a
binding carriage, a slipping belt. A dataset with gravity left in the
accelerometer does not crash: it loads cleanly, trains, converges, and quietly
teaches the model to fight a 9.8 m/s² lie. Almost every hard bug in this notebook
is of that species, which is why most of this page is about them.

## The data

The corpus is assembled from datasets that were never meant to agree with each
other — LaMar's iOS captures and the HelmetPoser helmet rig first, with Nymeria,
AMASS and TIC queued behind them, toward a sensor plan of six body-worn IMUs,
head first. Each source speaks its own dialect, and the translation is exact or
it is worthless:

- **Timestamps.** LaMar's are nanoseconds at roughly 100 Hz. My first bug on the
  project was reading them as milliseconds, which asked the resampler for about
  two billion samples.
- **Units.** HelmetPoser's accelerometer reports in g and has to be multiplied by
  9.8 before it is an acceleration.
- **Columns.** iOS logs raw acceleration and gravity in separate column groups,
  and a reader that misses part of the header shifts every column against its
  label — the file still parses, the shapes are still right, and the data is
  wrong.
- **Orientations.** Ground-truth quaternions arrive un-normalized, and the
  axis–angle conversion hid a Rodrigues-formula mistake: with a normalized axis
  the correct form is R = I + K sin θ + K²(1 − cos θ), and the code had the other
  variant.
- **Containers.** HelmetPoser ships as ROS bags, converted to ROS 2 db3 and split
  into CSV before the alignment script could read them.

Everything funnels through one gravity-frame alignment script — rotate each
sequence so gravity sits where the model expects it, from a supplied gravity
vector or one estimated on the spot — and out the other side comes a uniform npz
per sequence: timestamps, the six IMU channels, positions, quaternions.

## Looking at the data

The only reliable countermeasure is to look at everything, so I built the tools
to look with. `visualize_npz.py` renders a dashboard for any processed sequence —
the 3D trajectory coloured by time, position, Euler orientation, both raw sensor
streams — and its last panel is accelerometer magnitude plotted against a dashed
line at 9.81: a built-in gravity check, because that is the mistake that earned a
dedicated panel. Its sibling `visualize_live.py` is a Foxglove-style 3D viewer
that replays a sequence in the browser and can export itself as a single
self-contained HTML file. The dashboard figures at the bottom of this page are
one HelmetPoser sequence, 40,244 samples over 201.2 seconds.

## Gravity

Gravity is the villain of this notebook. An accelerometer at rest does not read
zero — it reads 9.8 m/s² of support force — and every dataset makes a private
decision about whether that has been subtracted and in which frame the residual
lives. A two-line note from a November training session says it plainly: _drone
is without gravity, car with gravity._ Get the convention wrong for one source
and the model still trains, on data where the strongest signal in the
accelerometer is a lie.

Whether to gravity-align at all was settled by experiment rather than argument:
the same model trained through two dataloaders, gravity-aligned and not, with the
full metric suite run on both, plus a second ablation on the dataloader's
frame-reference handling. Gravity still got the last word — see the audit below.

## Training

The model plan was deliberately boring, in the way that is a compliment: train an
LSTM first — not because an LSTM would win, but because a small recurrent model
is a fast way to find out whether the data is sound — then replace it with a
transformer once it is. First runs were 50 epochs, watched to convergence and
logged to Weights & Biases; splits were 21/6/3 trajectories for train/val/test,
assigned randomly rather than trial-aligned, with LaMar split 70/15/15. Training
ran on two machines at once — my own RTX 4090 and a lab box — with the master
data archive on Bridges-2 at the Pittsburgh Supercomputing Center and a lot of
deliberate rsync in between.

## Measuring drift

The evaluation is designed to expose drift, not average it away. Every held-out
trajectory is scored twice: cut into 5-metre segments, and whole. On the November
human-data evaluation that meant 9 test trajectories and 127 segments averaging
4.81 m, with segment ATE of 0.4045 m ± 0.2708, best 0.0114 m, worst 1.8337 m.

The pair of numbers worth staring at: the best full trajectory — a short walk
inside a mocap volume — closes at 0.0288 m of ATE, and the worst — a running
sequence 38 segments long, nearly 200 m — ends at 4.74 m. Same model. Over any
5-metre window the predictions are decent; with no loop closure and no external
fix, error compounds with distance, and reporting the segment number without the
full-trajectory number would be flattering and dishonest. The measurement code
got no immunity either — one of the notebook's bugs is the metric calculation
silently skipping the first data entry.

## The demo

The public face is the Hugging Face Space linked on this page, implemented in
early March: upload an npz in the project's format and it runs inference and
draws what you see at the top of this page — the sensor streams, the predicted
trajectory against ground truth, and the metrics. The model behind it is
deliberately modest, an overfit LaMar model: a demonstration that the pipeline
works end to end, not a claim about generalization.

The figures on this page are the demo's real output on its bundled example, an
iOS capture from January 2022: ATE 1.4684 m, translational RTE 0.2044 m, drift
RTE 0.2298 m, velocity RMSE 0.0903 m/s, inference in 0.35 s. The Space itself
runs on the free CPU tier, which could not finish that example in six minutes, so
these figures come from running the Space's own inference and plotting code on
the 4090 — same code, same weights, same example, faster silicon.

One wart is worth documenting because it looks exactly like a broken model: the
dataloader infers motion type from the parent directory's name — 1 car, 2 dog,
3 drone, 4 human — so the demo stages every upload into a `human/` directory
before inference. Hand it a bare file path instead and you get motion type 0 and
a bare `ValueError`.

## The audit

At the end of March the dataloader got a line-by-line audit, and everything it
found was the silent kind:

- **Gravity was never being subtracted in the body frame.** A stray line break
  had turned the compensation into an expression statement with no effect — valid
  Python, so nothing ever crashed — leaving a −9.8 m/s² bias in the accelerometer
  data on the code path every current config took. After months of treating
  gravity alignment as an experimental variable, on that path gravity was not
  being removed at all. Drones, which change attitude fastest, were hit hardest.
- **The outlier filter was eating the drone data.** A hard-coded 5.0 m/s velocity
  cap silently dropped any faster training sample, and drones routinely fly at
  5–15 m/s. Replaced with per-motion-type thresholds — 10 car, 8 dog, 15 drone,
  5 human.
- **A tensor compared against int keys.** The motion type arrived as a torch
  tensor, so a `dict.get()` keyed on Python ints never matched and quietly fell
  through to the default. One `.item()`.
- **A hard-coded stride**, `pos_gt[::200]`, where the sequence's own interval
  belonged — on a dead code path, fixed anyway.

Out of the audit came per-motion-type training configs in place of
one-size-fits-all: drone with gravity alignment on, higher augmentation noise and
a 3e-4 learning rate; car with lower augmentation and longer patience; dog with
higher augmentation for erratic motion; human — already the best performer — with
the rate lowered to 1.5e-4; all at 80 epochs.

## The work between the figures

The rest of the notebook is the part that never becomes a figure and decides
whether anything above it happens:

- **Moving data.** The archive lives at PSC and training happens on local GPUs,
  so transfers are resumable rsync with SSH keep-alives and compression off —
  tuned so a transfer that dies overnight resumes instead of restarting.
- **Remote development.** VS Code over SSH into the 4090 — the notebook's own
  note is that it "makes developing so much easier," written the same day it also
  records twelve hours of work.
- **Small, reviewable changes.** Code went in as described PRs of 100–200 lines,
  which is the size at which a labmate can actually review odometry code.
- **Debugging other people's data.** The cleanest diagnosis in the notebook is
  from array shapes alone: a teammate's processed sequence with timestamps and
  IMU at 1,125,387 rows but positions and quaternions at 1,124,253. A 1,134-row
  disagreement is not noise, it is a systematic truncation error upstream — named
  from the shapes, double-checked by re-zipping their CSVs with the preprocessing
  script's own function, and written up for them the same evening.

## What I took from it

- **Data engineering as the substance of ML research.** The model was never the
  bottleneck. Turning datasets that were never meant to agree into one honest
  training format — units, frames, timestamps, sample rates, gravity — is where
  the project was won or lost, and every convention was an opportunity to be
  silently wrong.
- **Debugging failures that do not announce themselves.** A converging loss curve
  proves almost nothing about the data under it. What caught real bugs here was
  overfit tests, controlled ablations, dashboards with a gravity check built in,
  and treating array shapes as evidence.
- **Evaluation that exposes the weakness.** Segment ATE next to full-trajectory
  ATE, 0.40 m next to 4.74 m — choosing metrics so drift has nowhere to hide, and
  publishing the unflattering number beside the flattering one.
- **Research infrastructure.** A supercomputing archive, local GPU boxes,
  resumable transfer between them, remote development over SSH, experiment
  tracking — the plumbing that keeps a multi-machine, multi-month project
  coherent.
- **Working inside a lab.** Weekly group meetings that set direction, work
  delivered as small reviewable PRs, and being the person teammates brought
  malformed data to.
- **Shipping in public.** The demo is small and its model is honestly labelled as
  overfit, but it is live, end to end, with its numbers printed next to it.
