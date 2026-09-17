"""Figures for the autodidact card + gallery, produced by running the repo's own
code (examples/spiral.py's setup verbatim, examples/train_gpt.py's loop verbatim)
and drawing the results in the portfolio's zine palette. Nothing here is drawn by
hand: the decision regions come from the trained MLP, the loss curve from the
training loop, the graph from walking Tensor._prev on the README's own expression.
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'autodidact')
sys.path.insert(0, REPO)
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figs')
os.makedirs(OUT, exist_ok=True)

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


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
from matplotlib.patches import Rectangle

import autodidact as ad
from autodidact import Tensor, nn, optim, F

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
    """t of c over bg (like CSS color-mix)."""
    c = np.array(matplotlib.colors.to_rgb(c))
    b = np.array(matplotlib.colors.to_rgb(bg))
    return tuple(t * c + (1 - t) * b)


# ── 1. spiral: examples/spiral.py, verbatim setup ────────────────────────────

def spiral(n=100, k=3, noise=0.2):
    # the cs231n toy dataset: k arms, n points each
    x = np.zeros((n * k, 2), np.float32)
    y = np.zeros(n * k, np.int64)
    for j in range(k):
        r = np.linspace(0, 1, n)
        t = np.linspace(j * 4, (j + 1) * 4, n) + np.random.randn(n) * noise
        x[j * n:(j + 1) * n] = np.c_[r * np.sin(t), r * np.cos(t)]
        y[j * n:(j + 1) * n] = j
    return x, y


np.random.seed(0)
x, y = spiral()
xtr, ytr, xva, yva = ad.data.split(x, y, frac=0.8)
xtr_t, xva_t = Tensor(xtr), Tensor(xva)

model = nn.Sequential(nn.Linear(2, 64), nn.ReLU(), nn.Linear(64, 3))
opt = optim.Adam(model.parameters(), lr=1e-2)

sp_loss, sp_acc, sp_step = [], [], []
for step in range(1, 501):
    loss = F.cross_entropy(model(xtr_t), ytr)
    opt.zero_grad()
    loss.backward()
    opt.step()
    sp_loss.append(loss.item())
    if step % 50 == 0:
        with ad.no_grad():
            acc = (model(xva_t).data.argmax(-1) == yva).mean()
        sp_acc.append(acc)
        sp_step.append(step)
        print(f'step {step:4d}  loss {loss.item():.4f}  val acc {acc:.3f}')
final_acc = sp_acc[-1]

# decision regions from the trained model
g = np.linspace(-1.25, 1.25, 400, dtype=np.float32)
gx, gy = np.meshgrid(g, g)
grid = np.c_[gx.ravel(), gy.ravel()]
with ad.no_grad():
    logits = model(Tensor(grid)).data
pred = logits.argmax(-1).reshape(gx.shape)

CLASS = [ACCENT, TAPE, INK]
region_cmap = matplotlib.colors.ListedColormap([mix(c, IVORY, 0.22) for c in CLASS])


def draw_spiral(ax, show_label=True):
    ax.imshow(pred, origin='lower', extent=(g[0], g[-1], g[0], g[-1]), cmap=region_cmap,
              interpolation='nearest', aspect='equal')
    for j, c in enumerate(CLASS):
        m = y == j
        ax.scatter(x[m, 0], x[m, 1], s=22, c=c, edgecolors=IVORY, linewidths=0.8, zorder=3)
    ax.set_xlim(g[0], g[-1])
    ax.set_ylim(g[0], g[-1])
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_linewidth(3)
        s.set_color(INK)
    if show_label:
        ax.text(0.03, 0.965, f'examples/spiral.py\nstep 500  loss {sp_loss[-1]:.4f}  val acc {final_acc:.3f}',
                transform=ax.transAxes, va='top', ha='left', fontsize=10.5, color=INK,
                bbox=dict(boxstyle='square,pad=0.45', fc=IVORY, ec=INK, lw=1.5))


# card cover, 1200x900
fig = plt.figure(figsize=(12, 9), dpi=100)
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
ax.set_facecolor(IVORY)
ax.axis('off')
# the square plot sits in the 4:3 frame, flanked by ivory
inner = fig.add_axes([(1 - 0.75 * 0.96) / 2, 0.02, 0.75 * 0.96, 0.96])
draw_spiral(inner)
fig.savefig(os.path.join(OUT, 'autodidact.jpg'), dpi=100, pil_kwargs={'quality': 92})  # the card cover
plt.close(fig)

# gallery: spiral + curves side by side
fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 6.4), dpi=100, gridspec_kw=dict(width_ratios=[1, 1.15], wspace=0.14))
draw_spiral(a1)
a2.plot(range(1, 501), sp_loss, color=INK, lw=2.2, label='train loss')
a2.set_xlabel('step', fontsize=11)
a2.set_ylabel('cross-entropy', fontsize=11)
a2.set_xlim(0, 500)
a2.set_ylim(0, max(sp_loss) * 1.05)
a2.grid(True, color=mix(INK, IVORY, 0.14), lw=1)
a2b = a2.twinx()
a2b.plot(sp_step, sp_acc, color=TAPE, lw=2.2, marker='s', ms=6, markerfacecolor=IVORY, markeredgewidth=2, label='val acc')
a2b.set_ylim(0, 1.02)
a2b.set_ylabel('val acc', fontsize=11, color=TAPE)
a2b.tick_params(axis='y', colors=TAPE)
for s in list(a2.spines.values()) + list(a2b.spines.values()):
    s.set_linewidth(1.5)
a2.spines['top'].set_visible(False)
a2b.spines['top'].set_visible(False)
a2.set_title('Adam, lr 1e-2, 500 steps on 240 points; 60 held out', fontsize=11, loc='left', pad=10)
fig.subplots_adjust(left=0.04, right=0.93, top=0.9, bottom=0.1)
fig.savefig(os.path.join(OUT, 'autodidact-spiral.png'), dpi=100)
plt.close(fig)

# ── 2. train_gpt.py, verbatim loop ───────────────────────────────────────────

TEXT = """i wanted to know what actually happens inside backward, so i wrote one.
a tensor is a numpy array, a gradient, and a pointer to the op that made it.
every op records its parents and a closure that turns the output gradient into
input gradients. backward walks the graph in reverse topological order and adds
things up. that is really all there is to it, but the details bite.
broadcasting means gradients have to be summed back to the shape they came from.
matmul over batches is the same trick wearing a different hat. softmax wants the
max subtracted or it blows up. indexing with repeated indices has to accumulate,
not overwrite. once the ops are right, everything above them is bookkeeping:
modules, optimizers, a small transformer. the transformer is the fun part.
attention is a few matmuls and a mask. it is slow in numpy and that is fine.
the point was never speed. the point was to stop treating backward as magic.
"""
steps, block, batch, n_layer, n_head, n_embd, lr = 300, 32, 16, 2, 4, 64, 3e-3
chars = sorted(set(TEXT))
stoi = {c: i for i, c in enumerate(chars)}
data = np.array([stoi[c] for c in TEXT], np.int64)
np.random.seed(0)
gpt = nn.GPT(len(chars), block, n_layer, n_head, n_embd, dropout=0.1)
n_params = sum(p.size for p in gpt.parameters())
print(f'{len(TEXT)} chars, vocab {len(chars)}; {n_params / 1e3:.1f}k params')
gopt = optim.AdamW(gpt.parameters(), lr=lr, weight_decay=0.1)
g_loss, g_lr, g_t = [], [], []
t0 = time.time()
for step in range(steps):
    gopt.lr = optim.cosine_lr(step, warmup=20, total=steps, lr=lr, lr_min=lr / 10)
    xb, yb = ad.data.windows(data, block, batch)
    _, loss = gpt(xb, yb)
    gopt.zero_grad()
    loss.backward()
    gopt.step()
    g_loss.append(loss.item())
    g_lr.append(gopt.lr)
    g_t.append(time.time() - t0)
print(f'final loss {g_loss[-1]:.3f} in {g_t[-1]:.1f}s')
gpt.eval()
sample = gpt.generate(data[None, :8], 120, temperature=0.8, top_k=10)[0]
sample_txt = ''.join(chars[i] for i in sample)
print('---\n' + sample_txt)

fig, ax = plt.subplots(figsize=(14, 5.6), dpi=100)
ax.plot(range(steps), g_loss, color=INK, lw=2, label='train loss')
ax.set_xlabel('step', fontsize=11)
ax.set_ylabel('cross-entropy (nats)', fontsize=11)
ax.set_xlim(0, steps - 1)
ax.set_ylim(0, max(g_loss) * 1.05)
ax.grid(True, color=mix(INK, IVORY, 0.14), lw=1)
axb = ax.twinx()
axb.plot(range(steps), g_lr, color=TAPE, lw=2, ls='--', label='lr')
axb.set_ylabel('learning rate', fontsize=11, color=TAPE)
axb.tick_params(axis='y', colors=TAPE)
axb.set_ylim(0, lr * 1.1)
axb.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1e'))
for s in list(ax.spines.values()) + list(axb.spines.values()):
    s.set_linewidth(1.5)
ax.spines['top'].set_visible(False)
axb.spines['top'].set_visible(False)
ax.set_title(f'examples/train_gpt.py — {n_layer} layers, {n_head} heads, d={n_embd}; {n_params / 1e3:.1f}k params, '
             f'{len(TEXT)} chars, vocab {len(chars)}; {steps} steps in {g_t[-1]:.1f}s on one CPU thread',
             fontsize=11, loc='left', pad=10)
fig.subplots_adjust(left=0.06, right=0.92, top=0.88, bottom=0.13)
fig.savefig(os.path.join(OUT, 'autodidact-gpt-loss.png'), dpi=100)
plt.close(fig)

# ── 3. the graph: README's own expression, walked through Tensor._prev ───────

x = ad.randn(3, 4, requires_grad=True)
yv = ((x @ x.T).tanh() * 2 + x[:, :3].exp()).log_softmax(-1).sum()

nodes, edges = {}, []
stack = [yv]
while stack:
    t = stack.pop()
    if id(t) in nodes:
        continue
    if t._backward is not None:
        q = getattr(t._backward, '__qualname__', '')
        name = q.split('.<locals>')[0].split('.')[-1] if q else 'op'
        kind = 'op'
    elif t.requires_grad:
        name, kind = 'x', 'leaf'
    else:
        name, kind = (repr(float(t.data)) if t.data.size == 1 else 'const'), 'const'
    nodes[id(t)] = dict(t=t, name=name, kind=kind, shape=tuple(t.shape))
    for p in t._prev:
        edges.append((id(p), id(t)))
        stack.append(p)

# depth = longest path from a leaf
children = {k: [] for k in nodes}
indeg = {k: 0 for k in nodes}
for a, b in edges:
    children[a].append(b)
    indeg[b] += 1
depth = {k: 0 for k in nodes}
order = [k for k in nodes if indeg[k] == 0]
seen = set(order)
i = 0
while i < len(order):
    k = order[i]
    i += 1
    for c in children[k]:
        depth[c] = max(depth[c], depth[k] + 1)
        indeg[c] -= 1
        if indeg[c] == 0:
            order.append(c)
cols = {}
for k in order:
    cols.setdefault(depth[k], []).append(k)
ncol = max(cols) + 1
pos = {}
for d, ks in cols.items():
    n = len(ks)
    for j, k in enumerate(ks):
        pos[k] = (d, (j - (n - 1) / 2))
print('graph:', len(nodes), 'nodes,', len(edges), 'edges,', ncol, 'columns')
for k in order:
    print('  ', depth[k], nodes[k]['name'], nodes[k]['shape'])

fig, ax = plt.subplots(figsize=(14, 6.2), dpi=100)
ax.set_xlim(-0.7, ncol - 0.3)
ymax = max(abs(p[1]) for p in pos.values()) + 0.75
ax.set_ylim(-ymax, ymax)
ax.axis('off')
BW, BH = 0.74, 0.66
for a, b in edges:
    (xa, ya), (xb, yb) = pos[a], pos[b]
    ax.annotate('', xy=(xb - BW / 2, yb), xytext=(xa + BW / 2, ya),
                arrowprops=dict(arrowstyle='-|>', color=mix(INK, IVORY, 0.55), lw=1.6, shrinkA=0, shrinkB=0,
                                connectionstyle='arc3,rad=0.0'))
for k, n in nodes.items():
    px, py = pos[k]
    is_root = k == id(yv)
    fc = TAPE if is_root else (IVORY if n['kind'] != 'leaf' else mix(ACCENT, IVORY, 0.25))
    ec = INK if n['kind'] != 'const' else mix(INK, IVORY, 0.4)
    lw = 2.4 if n['kind'] != 'const' else 1.4
    ax.add_patch(Rectangle((px - BW / 2, py - BH / 2), BW, BH, fc=fc, ec=ec, lw=lw, zorder=3))
    if n['kind'] != 'const':
        ax.add_patch(Rectangle((px - BW / 2 + 0.05, py - BH / 2 - 0.05), BW, BH, fc=mix(INK, IVORY, 0.55), ec='none', zorder=2))
    label = n['name'] if n['kind'] != 'leaf' else 'x'
    shp = '×'.join(str(s) for s in n['shape']) if n['shape'] else 'scalar'
    ax.text(px, py + 0.09, label, ha='center', va='center', fontsize=10, fontweight='bold', color=INK, zorder=4)
    ax.text(px, py - 0.16, shp, ha='center', va='center', fontsize=8.5, color=mix(INK, IVORY, 0.7), zorder=4)
ax.text(-0.62, ymax - 0.12, 'y = ((x @ x.T).tanh() * 2 + x[:, :3].exp()).log_softmax(-1).sum()\n'
        'the graph backward() walks, read off Tensor._prev — one box per op call, arrows point forward',
        ha='left', va='top', fontsize=10.5, color=INK)
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
fig.savefig(os.path.join(OUT, 'autodidact-graph.png'), dpi=100)
plt.close(fig)

with open(os.path.join(OUT, 'autodidact-numbers.txt'), 'w') as f:
    f.write(f'spiral final loss {sp_loss[-1]:.4f} val acc {final_acc:.3f}\n')
    f.write(f'gpt params {n_params} final loss {g_loss[-1]:.3f} time {g_t[-1]:.1f}s chars {len(TEXT)} vocab {len(chars)}\n')
    f.write('sample:\n' + sample_txt + '\n')
    f.write(f'graph nodes {len(nodes)} edges {len(edges)}\n')
print('done ->', OUT)
