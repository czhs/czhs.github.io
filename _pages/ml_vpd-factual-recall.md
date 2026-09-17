---
layout: portfolio_post
portfolio: ml
permalink: /ml/vpd-factual-recall/
project: vpd-factual-recall
standalone_title: "VPD factual recall — Chris Shi"
nav: false
---

<!-- The write-up is the repository's README, verbatim (the H1 dropped: the
     layout renders the title). Edit it upstream and re-copy rather than here. -->

<p class="rbx-post-src">From the repository README</p>

Goodfire's Variational Parameter Decomposition (VPD) rewrites every weight matrix of a
model as a sum of rank-one components and trains a causal-importance (CI) network that
switches components on per token. This repository ships one such decomposition of
`facebook/opt-125m` (55,296 components, 0.6% on per position) and asks a narrow question:
**does the decomposition, run at its own operating point, still recall what the model
knows?** It does not. The CI-masked forward loses factual recall (the two-shot "capital
of France is" drops from 0.76 to 0.06 and answers "London") and it loses rare-word
recall the same way (Hong `Kong` from 0.99 to 0.52, Kuala `Lumpur` from 0.99 to 0.04,
Vincent van `Gogh` from 0.96 to 0.001), while frequent continuations survive or improve
(In order `to` 0.81 to 0.99). Damage is governed by the answer token's corpus frequency,
not by whether the prediction needs a fact.

This repository holds the model, the data, the training recipe, and the scripts that
re-derive every number below in about a minute on one GPU.

## Results

All numbers are `P(answer | prompt)` at the last prompt position, original OPT-125m
versus the same weights run through the decomposition with the CI mask applied
(`delta = 0`). "All-on" (every component on, no mask) reproduces the original to within
0.002 nats of cross-entropy, so everything the mask loses is inside the decomposition.
Full distributions, ranks, and per-position traces: [`reference/probes.json`](https://github.com/czhs/vpd-factual-recall/blob/main/reference/probes.json).

<table>
  <thead>
    <tr>
      <th>prompt (answer)</th>
      <th style="text-align: right">original</th>
      <th style="text-align: right">CI-masked</th>
      <th style="text-align: right">rank</th>
      <th>CI-masked top-1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>The capital of Italy is Rome. The capital of Japan is Tokyo. The capital of France is (<code> Paris</code>)</td>
      <td style="text-align: right">0.761</td>
      <td style="text-align: right">0.057</td>
      <td style="text-align: right">1 → 2</td>
      <td><code> London</code> 0.250</td>
    </tr>
    <tr>
      <td>Rome is the capital of Italy. Tokyo is the capital of Japan. Paris is the capital of (<code> France</code>)</td>
      <td style="text-align: right">0.780</td>
      <td style="text-align: right">0.090</td>
      <td style="text-align: right">1 → 2</td>
      <td><code> England</code> 0.140</td>
    </tr>
    <tr>
      <td>Paris is the capital of (<code> France</code>), bare</td>
      <td style="text-align: right">0.323</td>
      <td style="text-align: right">0.119</td>
      <td style="text-align: right">2 → 2</td>
      <td><code> the</code></td>
    </tr>
    <tr>
      <td>The capital of France is (<code> Paris</code>), bare</td>
      <td style="text-align: right">0.007</td>
      <td style="text-align: right">0.00005</td>
      <td style="text-align: right">22 → 1543</td>
      <td><code> a</code></td>
    </tr>
    <tr>
      <td>...The capital of Greece is (<code> Athens</code>)</td>
      <td style="text-align: right">0.853</td>
      <td style="text-align: right">0.023</td>
      <td style="text-align: right">1 → 5</td>
      <td><code> Wales</code></td>
    </tr>
    <tr>
      <td>...The capital of Hungary is (<code> Budapest</code>)</td>
      <td style="text-align: right">0.859</td>
      <td style="text-align: right">0.003</td>
      <td style="text-align: right">1 → 42</td>
      <td><code> London</code></td>
    </tr>
    <tr>
      <td>...The capital of Kuwait is (<code> Kuwait</code>)</td>
      <td style="text-align: right">0.466</td>
      <td style="text-align: right">0.001</td>
      <td style="text-align: right">1 → 122</td>
      <td><code> London</code></td>
    </tr>
    <tr>
      <td>...The capital of England is (<code> London</code>)</td>
      <td style="text-align: right">0.608</td>
      <td style="text-align: right">0.517</td>
      <td style="text-align: right">1 → 1</td>
      <td><code> London</code></td>
    </tr>
    <tr>
      <td>The Chinese city of Hong (<code> Kong</code>)</td>
      <td style="text-align: right">0.988</td>
      <td style="text-align: right">0.518</td>
      <td style="text-align: right">1 → 1</td>
      <td><code> Kong</code></td>
    </tr>
    <tr>
      <td>The flight landed in Kuala (<code> Lumpur</code>)</td>
      <td style="text-align: right">0.990</td>
      <td style="text-align: right">0.040</td>
      <td style="text-align: right">1 → 1</td>
      <td><code> Lumpur</code></td>
    </tr>
    <tr>
      <td>A painting by Vincent van (<code> Go</code>gh)</td>
      <td style="text-align: right">0.956</td>
      <td style="text-align: right">0.001</td>
      <td style="text-align: right">1 → 102</td>
      <td><code> de</code></td>
    </tr>
    <tr>
      <td>He ordered a plate of macaroni and (<code> cheese</code>)</td>
      <td style="text-align: right">0.867</td>
      <td style="text-align: right">0.025</td>
      <td style="text-align: right">1 → 1</td>
      <td><code> cheese</code></td>
    </tr>
    <tr>
      <td>In the museum there was a xyl(<code>ophone</code>)</td>
      <td style="text-align: right">0.903</td>
      <td style="text-align: right">0.0005</td>
      <td style="text-align: right">1 → 244</td>
      <td></td>
    </tr>
    <tr>
      <td>The city of Los (<code> Angeles</code>)</td>
      <td style="text-align: right">0.950</td>
      <td style="text-align: right">0.692</td>
      <td style="text-align: right">1 → 1</td>
      <td><code> Angeles</code></td>
    </tr>
    <tr>
      <td>A patient with Alzheimer(<code>&#x27;s</code>)</td>
      <td style="text-align: right">0.697</td>
      <td style="text-align: right">0.647</td>
      <td style="text-align: right">1 → 1</td>
      <td><code>&#x27;s</code></td>
    </tr>
    <tr>
      <td>In order (<code> to</code>)</td>
      <td style="text-align: right">0.813</td>
      <td style="text-align: right">0.991</td>
      <td style="text-align: right">1 → 1</td>
      <td><code> to</code></td>
    </tr>
  </tbody>
</table>

The pattern over the whole battery (399 probe/condition rows, medians;
[`reference/battery_summary.json`](https://github.com/czhs/vpd-factual-recall/blob/main/reference/battery_summary.json)):

<table>
  <thead>
    <tr>
      <th>family</th>
      <th style="text-align: right">n</th>
      <th style="text-align: right">P all-on</th>
      <th style="text-align: right">P CI-masked</th>
      <th style="text-align: right">damage (nats)</th>
      <th style="text-align: right">random mask of the same size</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>world facts, two-shot (inventory)</td>
      <td style="text-align: right">59</td>
      <td style="text-align: right">0.628</td>
      <td style="text-align: right">0.032</td>
      <td style="text-align: right">−2.70</td>
      <td style="text-align: right">−11.9</td>
    </tr>
    <tr>
      <td>held-out world facts, two-shot</td>
      <td style="text-align: right">46</td>
      <td style="text-align: right">0.631</td>
      <td style="text-align: right">0.014</td>
      <td style="text-align: right">−3.86</td>
      <td style="text-align: right">−12.8</td>
    </tr>
    <tr>
      <td>multi-token entity names (Rio de <code> Janeiro</code>)</td>
      <td style="text-align: right">13</td>
      <td style="text-align: right">0.993</td>
      <td style="text-align: right">0.231</td>
      <td style="text-align: right">−1.44</td>
      <td style="text-align: right">−9.7</td>
    </tr>
    <tr>
      <td>collocations (Pros and <code> cons</code>)</td>
      <td style="text-align: right">14</td>
      <td style="text-align: right">0.898</td>
      <td style="text-align: right">0.166</td>
      <td style="text-align: right">−1.55</td>
      <td style="text-align: right">−12.0</td>
    </tr>
    <tr>
      <td>word-piece and rigid-name completions</td>
      <td style="text-align: right">82</td>
      <td style="text-align: right">0.861</td>
      <td style="text-align: right">0.026</td>
      <td style="text-align: right">−2.93</td>
      <td style="text-align: right">−10.3</td>
    </tr>
    <tr>
      <td>function-word slots (syntax controls)</td>
      <td style="text-align: right">11</td>
      <td style="text-align: right">0.573</td>
      <td style="text-align: right">0.828</td>
      <td style="text-align: right">+0.21</td>
      <td style="text-align: right">−8.0</td>
    </tr>
    <tr>
      <td>nonce subjects, same template</td>
      <td style="text-align: right">46</td>
      <td style="text-align: right">0.003</td>
      <td style="text-align: right">0.003</td>
      <td style="text-align: right">+0.27</td>
      <td style="text-align: right">−8.4</td>
    </tr>
  </tbody>
</table>

What decides the damage is the answer token's log unigram frequency in the training
corpus: r = 0.75 over the 125 known items (slope 0.68 nats per log-unit), r = 0.83
inside the relational facts alone and 0.66 inside the locally determined completions,
and r = 0.66 over 2,423 confident positions of held-out natural text, where the median
damage runs −5.5, −2.1, −0.95, −0.06, +0.06, +0.05 nats across log-frequency bins from
rarest to most frequent. Facts with frequent answers (England → London, −0.13 nats) barely
move; word-piece continuations with rare answers (xyl → ophone, −7.5 nats) die.

The decomposition itself ([`TRAINING.md`](https://github.com/czhs/vpd-factual-recall/blob/main/TRAINING.md)): 72 matrices (q, k, v, out, fc1,
fc2 of all 12 layers), 768 components each, 56,981 training steps on 128-token Pile
windows; exact reconstruction to 1.7e-4 max logit difference; all-on cross-entropy
3.319 against the original's 3.317 on held-out text; CI-masked 3.959; 339 to 344
components on per position (0.62%); 683 of 55,296 alive on Pile.

## Quick start

Tested on Linux with Python 3.10 and 3.13, one RTX 4090 (about 3 GB of GPU memory for
the analyses; the decomposition needs ~14 GB to retrain). Everything after `setup.sh`
runs in **under a minute**.

```bash
git clone https://github.com/czhs/vpd-factual-recall && cd vpd-factual-recall
bash setup.sh        # .venv + deps, downloads the checkpoint (818 MB) and corpus (139 MB) from the release, caches facebook/opt-125m, sanity check
bash reproduce.sh    # probes -> battery -> natural text -> figures -> check against reference/
```

`setup.sh` honours `TORCH_SPEC` / `TORCH_INDEX` for a specific CUDA build (the reference
machine used `TORCH_SPEC=torch==2.8.0 TORCH_INDEX=https://download.pytorch.org/whl/cu128`)
and `VFR_CKPT` / `VFR_PILE` / `VFR_RESULTS` to relocate the assets and outputs
([`vfr/paths.py`](https://github.com/czhs/vpd-factual-recall/blob/main/vfr/paths.py)).

**One prompt, four forwards, no scripts:**

```bash
source .venv/bin/activate && python -m vfr.sanity
```

prints `P(' Paris')` after the two-shot prompt under the original model (0.7605), the exact
reconstruction (0.7605), all components on (0.7736) and the CI mask (0.0567, rank 2 behind
` London`).

## What the pipeline does

<table>
  <thead>
    <tr>
      <th>step</th>
      <th>command</th>
      <th>notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>showcase probes</td>
      <td><code>python -m vfr.probe</code></td>
      <td>38 prompts ([<code>data/probes/showcase.jsonl</code>](https://github.com/czhs/vpd-factual-recall/blob/main/data/probes/showcase.jsonl)): top-10 next-token distributions under original / exact / all-on / CI-masked / random-matched forwards, per-position traces, gate counts → <code>results/probes.json</code></td>
    </tr>
    <tr>
      <td>frequency battery</td>
      <td><code>python -m vfr.battery</code></td>
      <td>194-item 2 x 2 battery (rare/frequent answer × relational/locally determined) + 113 inventory facts + 46 held-out facts with nonce twins → <code>results/battery.jsonl</code>, <code>battery_summary.json</code> (families, frequency-law fit, capital ladder)</td>
    </tr>
    <tr>
      <td>natural text</td>
      <td><code>python -m vfr.wild --n-windows 64</code></td>
      <td>every position of held-out 128-token Pile windows (the CI net's training regime) → <code>results/wild_positions.jsonl</code>, <code>wild_summary.json</code>, <code>wild_passages.json</code></td>
    </tr>
    <tr>
      <td>figures</td>
      <td><code>python -m vfr.figures</code> / <code>python -m vfr.figures_svg</code></td>
      <td>PNGs in <code>figures/</code> (matplotlib) and theme-aware SVG includes in <code>figures/svg/</code></td>
    </tr>
    <tr>
      <td>check</td>
      <td><code>python -m vfr.check</code></td>
      <td>compares <code>results/</code> with <code>reference/</code>: exact-reconstruction identity, per-probe log-probs within 0.05 nats, ranks, the frequency-law fit, per-family medians, natural-text cross-entropy</td>
    </tr>
    <tr>
      <td>retrain</td>
      <td><code>bash scripts/train_pileopt_long.sh</code></td>
      <td>the exact command that produced the checkpoint (4.5 h on a 4090); <code>python -m vfr.tokenize_pile</code> rebuilds the corpus from NeelNanda/pile-10k</td>
    </tr>
  </tbody>
</table>

**Reproduction log.** 2026-09-02, fresh clone on the reference machine (RTX 4090,
driver 535, system Python 3.10.12, `TORCH_SPEC=torch==2.8.0
TORCH_INDEX=https://download.pytorch.org/whl/cu128`): `setup.sh` built the venv,
downloaded and checksummed both release assets (41 s), and passed the sanity check;
`reproduce.sh` re-derived every number above and `vfr.check` passed 9/9 against
`reference/`. The 2026-08-14 campaign's numbers for the same probes agree to the third
decimal ([`reference/README.md`](https://github.com/czhs/vpd-factual-recall/blob/main/reference/README.md)). On other GPUs expect
log-probabilities to agree within ~0.01 nats, not bit-for-bit.

## Conventions worth knowing before writing new probes

- The CI transformer is **bidirectional** over the 128-token window, so prompts are never
  padded: `vfr.battery` batches only prompts of identical token length, and the answer is
  never inside the window (it is scored at the last prompt position).
- OPT's tokenizer auto-prepends BOS (id 2) and distinguishes `" Rome"` (one token) from
  `"Rome"` (two); answers carry their leading space, and multi-token answers are scored
  on their first piece and flagged (`answer_single_token`). Every probe is checked for
  BPE seam consistency (`tok(prompt + answer)` must equal `tok(prompt)` followed by the
  answer's first piece).
- "Damage" is `log P_cim(answer) − log P_allon(answer)` in nats; the random control is a
  mask with exactly CI's per-position, per-matrix active count (seeded), so "sparse" is
  never the explanation of anything.
- Zero-shot capitals sit at P ≈ 0.007 under this model (rank correct, buried under
  ` the`/` a`); the two-shot template lifts the same facts to P ≈ 0.66, which is why
  the factual probes are two-shot. The demonstrations never contain the scored answer.

## Layout

```
setup.sh, reproduce.sh        entry points (see above)
scripts/train_pileopt_long.sh retrain the decomposition from scratch
TRAINING.md                   the CI network, losses, schedule, every hyper-parameter, what the run converged to
vfr/                          the package; run modules with `python -m vfr.<name>`
  paths.py                    all locations; env-overridable
  decomp.py                   loads the checkpoint; original / exact / all-on / CI-masked / random forwards
  probe.py  battery.py  wild.py          the three analyses
  figures.py  figures_svg.py  check.py   figures and the reference check
  train_full_vpd.py  common.py           the training driver (VPD via vfr/nano)
  tokenize_pile.py  unigram.py           corpus and unigram table
  nano/run.py  nano/compat_2d.py         Goodfire's nano_param_decomp reference implementation (MIT, commit 53965b5e, unmodified) + the OPT 2-D shim
data/probes/                  showcase.jsonl, frequency_battery.jsonl, localization_set.jsonl, heldout_probes.jsonl, inventory_battery.jsonl
data/unigram_pile_opt.pt      unigram log-frequency table over the training corpus (50,272 tokens)
reference/                    the numbers in this README, the training log and config, the 2026-08-14 campaign's artifacts
figures/                      PNGs; figures/svg/ the site includes
artifacts/                    (downloaded by setup.sh) pileopt_long_ckpt.pt, pile_opt.pt
```

## Release assets

<table>
  <thead>
    <tr>
      <th>file</th>
      <th style="text-align: right">size</th>
      <th>sha256</th>
      <th>what</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>pileopt_long_ckpt.pt</code></td>
      <td style="text-align: right">818 MB</td>
      <td><code>00e608dd…482f49c</code></td>
      <td>the decomposition: <code>V</code>, <code>U</code> for 72 matrices (fp32), the CI network's state dict, <code>cfg</code>, <code>args</code>, <code>module_paths</code> (<code>torch.load(..., weights_only=True)</code>)</td>
    </tr>
    <tr>
      <td><code>pile_opt.pt</code></td>
      <td style="text-align: right">139 MB</td>
      <td><code>fd56a8a3…166012</code></td>
      <td>NeelNanda/pile-10k tokenized with OPT's tokenizer, 17,361,935 int64 tokens; the first 90% trained the decomposition</td>
    </tr>
  </tbody>
</table>

Full hashes in `setup.sh`. The target model is not stored; it is `facebook/opt-125m`
from the Hub, loaded in fp32 with eager attention.

## Provenance and license

The decomposition and the 2026-08-14 knowledge campaign (inventory, localization, two
adversarial verification passes) were produced in the VPD-Copying project; the campaign's
reports and raw files are in `reference/campaign/`. Code and data here are MIT
([`LICENSE`](https://github.com/czhs/vpd-factual-recall/blob/main/LICENSE)); `vfr/nano/run.py` is Goodfire's, MIT, vendored from
<https://github.com/goodfire-ai/param-decomp>.
