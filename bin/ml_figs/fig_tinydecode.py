"""Figures for the tinydecode card + gallery, drawn from the repo's OWN benchmark
output: the JSON that bench/latency.py dumps (per-run Stats, one step_ms per
decode step) and the lines bench/spec.py prints. Nothing is typed in by hand —
every number on these figures is read from those files.

    python3 fig_tinydecode.py <bench dir> [<out dir>]

<bench dir> holds bench-latency-3b.json, bench-latency-1b.json and bench-all.log
(the stdout of the run). Machine/model labels are read from the log header.
"""
import json
import os
import re
import statistics
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'bench')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'figs')
os.makedirs(OUT, exist_ok=True)



def register_site_mono():
    """JetBrains Mono, the site's machine face. matplotlib cannot read woff2, so
    the variable font under assets/fonts/ is decompressed to a TTF once (needs
    fontTools + brotli) into fonts/ next to this script; a staged TTF is used
    as is. Falls back to Menlo / DejaVu Sans Mono below if neither works."""
    font_dir = os.path.join(HERE, 'fonts')
    os.makedirs(font_dir, exist_ok=True)
    ttf = os.path.join(font_dir, 'JetBrainsMono-var.ttf')
    if not os.path.exists(ttf):
        for up in ['..', os.path.join('..', '..')]:
            woff2 = os.path.join(HERE, up, 'assets', 'fonts', 'jetbrains-mono-latin-var.woff2')
            if os.path.exists(woff2):
                try:
                    from fontTools.ttLib import TTFont
                    f = TTFont(woff2)
                    f.flavor = None
                    f.save(ttf)
                except Exception as e:  # noqa: BLE001
                    print('font conversion skipped:', e)
                break
    for fn in os.listdir(font_dir):
        if fn.endswith('.ttf'):
            font_manager.fontManager.addfont(os.path.join(font_dir, fn))


register_site_mono()

# zine palette (portfolio_styles.liquid literals)
IVORY = '#fffcf2'
INK = '#13261f'
FIELD = '#8fb2a4'
ACCENT = '#0f6046'
TAPE = '#e8590c'

MONO = None
for cand in ['JetBrains Mono', 'Menlo', 'DejaVu Sans Mono']:
    if any(f.name == cand for f in font_manager.fontManager.ttflist):
        MONO = cand
        break
print('mono font:', MONO)
plt.rcParams.update({
    'font.family': MONO or 'monospace',
    'text.color': INK,
    'axes.edgecolor': INK,
    'axes.labelcolor': INK,
    'xtick.color': INK,
    'ytick.color': INK,
    'figure.facecolor': IVORY,
    'axes.facecolor': IVORY,
    'savefig.facecolor': IVORY,
})


def mix(c, bg, t):
    c = np.array(matplotlib.colors.to_rgb(c))
    b = np.array(matplotlib.colors.to_rgb(bg))
    return tuple(t * c + (1 - t) * b)


SOFT = mix(INK, IVORY, 0.55)
GRID = mix(INK, IVORY, 0.14)

# ── read the bench output ────────────────────────────────────────────────────

log = open(os.path.join(BENCH, 'bench-all.log')).read()
gpu = re.search(r'^(NVIDIA [^,\n]+),', log, re.M).group(1).replace('NVIDIA GeForce ', '')
torch_v = re.search(r'^(\d+\.\d+\.\d+\+cu\d+) ', log, re.M).group(1)
print('gpu', gpu, 'torch', torch_v)

CONFIGS = ['eager, torch ops', 'eager, fused kernels', 'graphs, torch ops', 'graphs, fused kernels']
LABEL = {
    'eager, torch ops': 'eager · torch ops',
    'eager, fused kernels': 'eager · fused kernels',
    'graphs, torch ops': 'cuda graphs · torch ops',
    'graphs, fused kernels': 'cuda graphs · fused kernels',
}


def load(name):
    raw = json.load(open(os.path.join(BENCH, f'bench-latency-{name}.json')))
    out = {}
    for cfg in CONFIGS:
        runs = raw[cfg]
        steps = [ms for r in runs for ms in r['step_ms']]
        out[cfg] = dict(
            ttft=statistics.median(r['ttft_ms'] for r in runs),
            p50=statistics.median(steps),
            p99=sorted(steps)[int(0.99 * (len(steps) - 1))],
            tok_s=statistics.median(r['new_tokens'] / sum(r['step_ms']) * 1e3 for r in runs),
            trace=runs[0]['step_ms'],
            new=runs[0]['new_tokens'],
            nruns=len(runs),
        )
    return out


lat = {'3B': load('3b'), '1B': load('1b')}
MODEL = {'3B': 'Llama-3.2-3B-Instruct', '1B': 'Llama-3.2-1B-Instruct'}
for m, d in lat.items():
    for cfg in CONFIGS:
        r = d[cfg]
        print(f'{m} {cfg:24s} ttft {r["ttft"]:6.2f}  p50 {r["p50"]:6.2f}  p99 {r["p99"]:6.2f}  {r["tok_s"]:6.1f} tok/s  ({r["nruns"]} runs x {r["new"]} tokens)')

# spec sections from the log
spec = {}
for title, key in [('spec 3B draft 1B', 'draft'), ('spec 3B ngram', 'ngram')]:
    sec = log.split(f'=== {title}')[1].split('===')[0]
    base = float(re.search(r'plain decode: ([\d.]+) tok/s', sec).group(1))
    rows = re.findall(r'k=\s*(\d+)\s+accept\s+([\d.]+)%\s+([\d.]+) tok/s\s+\(([\d.]+)x\)', sec)
    spec[key] = dict(base=base, rows=[(int(k), float(a), float(t), float(x)) for k, a, t, x in rows])
    print(key, spec[key])

# ── 1. card cover: the 3B inter-token latency, four ways ─────────────────────

def bars(ax, d, big):
    names = [LABEL[c] for c in CONFIGS]
    p50 = [d[c]['p50'] for c in CONFIGS]
    p99 = [d[c]['p99'] for c in CONFIGS]
    tok = [d[c]['tok_s'] for c in CONFIGS]
    cols = [SOFT if 'torch' in c else TAPE for c in CONFIGS]
    y = np.arange(len(CONFIGS))[::-1]
    h = 0.62
    ax.barh(y, p50, height=h, color=cols, edgecolor=INK, linewidth=2 if big else 1.5, zorder=3)
    # p99 as an ink tick past the bar end
    for yi, a, b in zip(y, p50, p99):
        ax.plot([b, b], [yi - h / 2, yi + h / 2], color=INK, lw=2 if big else 1.5, zorder=4)
    for yi, a, t in zip(y, p50, tok):
        ax.text(a + max(p50) * 0.02, yi, f'{a:.2f} ms   {t:.0f} tok/s', va='center', ha='left',
                fontsize=13 if big else 10.5, fontweight='bold', color=INK, zorder=5)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=12.5 if big else 10.5)
    ax.tick_params(axis='y', length=0)
    ax.set_xlim(0, max(p99) * 1.62)
    ax.set_xlabel('inter-token latency, ms per decode step (bar: p50 · tick: p99)', fontsize=11 if big else 10)
    ax.grid(True, axis='x', color=GRID, lw=1, zorder=0)
    for s in ax.spines.values():
        s.set_linewidth(1.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


fig = plt.figure(figsize=(12, 9), dpi=100)
ax = fig.add_axes([0.285, 0.11, 0.69, 0.7])
bars(ax, lat['3B'], big=True)
fig.text(0.04, 0.955, 'bench/latency.py', fontsize=13, fontweight='bold', va='top')
fig.text(0.04, 0.905, f'{MODEL["3B"]} · bf16 · {gpu}\n{lat["3B"][CONFIGS[0]]["new"]} new tokens, median of {lat["3B"][CONFIGS[0]]["nruns"]} runs',
         fontsize=11, va='top', color=mix(INK, IVORY, 0.75), linespacing=1.5)
fig.savefig(os.path.join(OUT, 'tinydecode.jpg'), dpi=100, pil_kwargs={'quality': 92})  # the card cover
plt.close(fig)

# ── 2. gallery: both models + the per-step trace ─────────────────────────────

fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 6.4), dpi=100, gridspec_kw=dict(width_ratios=[1.1, 1], wspace=0.3))
# left: grouped bars, 3B and 1B
y = np.arange(len(CONFIGS))[::-1] * 1.0
h = 0.36
for k, (m, off) in enumerate([('3B', +0.2), ('1B', -0.2)]):
    d = lat[m]
    p50 = [d[c]['p50'] for c in CONFIGS]
    p99 = [d[c]['p99'] for c in CONFIGS]
    cols = [SOFT if 'torch' in c else TAPE for c in CONFIGS]
    alpha = 1.0 if m == '3B' else 0.55
    a1.barh(y + off, p50, height=h, color=cols, alpha=alpha, edgecolor=INK, linewidth=1.5, zorder=3)
    for yi, b in zip(y + off, p99):
        a1.plot([b, b], [yi - h / 2, yi + h / 2], color=INK, lw=1.5, zorder=4)
    for yi, a, t in zip(y + off, p50, [d[c]['tok_s'] for c in CONFIGS]):
        a1.text(a + 0.15, yi, f'{m}  {a:.2f} ms  {t:.0f} tok/s', va='center', ha='left', fontsize=9.5, color=INK, zorder=5)
a1.set_yticks(y)
a1.set_yticklabels([LABEL[c] for c in CONFIGS], fontsize=10.5)
a1.tick_params(axis='y', length=0)
a1.set_xlim(0, max(lat['3B'][c]['p99'] for c in CONFIGS) * 1.7)
a1.set_xlabel('inter-token latency, ms per decode step (bar: p50 · tick: p99)', fontsize=10)
a1.grid(True, axis='x', color=GRID, lw=1, zorder=0)
for s in a1.spines.values():
    s.set_linewidth(1.5)
a1.spines['top'].set_visible(False)
a1.spines['right'].set_visible(False)
a1.set_title(f'{MODEL["3B"]} (solid), {MODEL["1B"]} (faded)\n'
             f'bf16, {gpu}; {lat["3B"][CONFIGS[0]]["new"]} new tokens, median of {lat["3B"][CONFIGS[0]]["nruns"]} runs', fontsize=10.5, loc='left', pad=10)

# right: per-step latency of one 3B run per config
styles = {
    'eager, torch ops': dict(color=SOFT, lw=1.6, ls='-'),
    'eager, fused kernels': dict(color=TAPE, lw=1.6, ls='-'),
    'graphs, torch ops': dict(color=INK, lw=1.6, ls='--'),
    'graphs, fused kernels': dict(color=TAPE, lw=2.2, ls='--'),
}
for c in CONFIGS:
    tr = lat['3B'][c]['trace']
    a2.plot(range(1, len(tr) + 1), tr, label=LABEL[c], **styles[c])
a2.set_xlabel('decode step', fontsize=10)
a2.set_ylabel('ms', fontsize=10)
a2.set_xlim(1, len(lat['3B'][CONFIGS[0]]['trace']))
lo = min(min(lat['3B'][c]['trace']) for c in CONFIGS)
hi = max(max(lat['3B'][c]['trace']) for c in CONFIGS)
a2.set_ylim(lo * 0.9, hi * 1.08)
a2.grid(True, color=GRID, lw=1)
for s in a2.spines.values():
    s.set_linewidth(1.5)
a2.spines['top'].set_visible(False)
a2.spines['right'].set_visible(False)
a2.legend(frameon=True, fontsize=9, loc='upper right', edgecolor=INK, facecolor=IVORY, fancybox=False)
a2.set_title(f'{MODEL["3B"]}: every decode step of one run\n(a cuda event per step, synced once at the end)', fontsize=10.5, loc='left', pad=10)
fig.subplots_adjust(left=0.2, right=0.985, top=0.86, bottom=0.12)
fig.savefig(os.path.join(OUT, 'tinydecode-latency.png'), dpi=100)
plt.close(fig)

# ── 3. gallery: speculative decoding ─────────────────────────────────────────

fig, ax = plt.subplots(figsize=(14, 5.8), dpi=100)
ks = [r[0] for r in spec['draft']['rows']]
x = np.arange(len(ks))
w = 0.36
base = spec['draft']['base']
for off, key, col, lab in [(-0.2, 'draft', TAPE, f'draft model: {MODEL["1B"]}'), (+0.2, 'ngram', SOFT, 'n-gram prompt lookup (no second model)')]:
    rows = spec[key]['rows']
    tps = [r[2] for r in rows]
    acc = [r[1] for r in rows]
    ax.bar(x + off, tps, width=w, color=col, edgecolor=INK, linewidth=1.5, zorder=3, label=lab)
    for xi, t, a, r in zip(x + off, tps, acc, rows):
        ax.text(xi, t + 2.5, f'{t:.0f} tok/s  ({r[3]:.2f}x)\naccept {a:.0f}%', ha='center', va='bottom', fontsize=9.5, color=INK, linespacing=1.4)
ax.axhline(base, color=INK, lw=1.8, ls='--', zorder=2, label=f'plain decode, {base:.1f} tok/s')
ax.set_xticks(x)
ax.set_xticklabels([f'k = {k}' for k in ks], fontsize=11)
ax.tick_params(axis='x', length=0)
ax.set_ylabel('tok/s (median of 4 prompts)', fontsize=10)
ax.set_ylim(0, max(base, max(r[2] for r in spec['draft']['rows'])) * 1.32)
ax.grid(True, axis='y', color=GRID, lw=1, zorder=0)
for s in ax.spines.values():
    s.set_linewidth(1.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(frameon=True, fontsize=9.5, loc='upper right', edgecolor=INK, facecolor=IVORY, fancybox=False)
ax.set_title(f'bench/spec.py — target {MODEL["3B"]}, bf16, {gpu}; temperature 0, 128 new tokens, cuda graphs on; '
             f'k draft tokens per round', fontsize=10.5, loc='left', pad=10)
fig.subplots_adjust(left=0.06, right=0.985, top=0.88, bottom=0.1)
fig.savefig(os.path.join(OUT, 'tinydecode-spec.png'), dpi=100)
plt.close(fig)

with open(os.path.join(OUT, 'tinydecode-numbers.txt'), 'w') as f:
    f.write(f'gpu {gpu} torch {torch_v}\n')
    for m, d in lat.items():
        for cfg in CONFIGS:
            r = d[cfg]
            f.write(f'{m} {cfg}: ttft {r["ttft"]:.2f} p50 {r["p50"]:.2f} p99 {r["p99"]:.2f} tok/s {r["tok_s"]:.1f}\n')
    f.write(json.dumps(spec) + '\n')
print('done ->', OUT)
