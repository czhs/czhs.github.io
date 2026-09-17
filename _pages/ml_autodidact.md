---
layout: portfolio_post
portfolio: ml
permalink: /ml/autodidact/
project: autodidact
standalone_title: "autodidact — Chris Shi"
nav: false
---

<!-- The write-up is the repository's README, verbatim (the H1 dropped: the
     layout renders the title). Edit it upstream and re-copy rather than here. -->

<p class="rbx-post-src">From the repository README</p>

A reverse-mode autodiff engine and a small neural-network library, written from
scratch on top of numpy. No torch, no jax, nothing but `numpy`. The name is the
pun: auto-diff, self-taught. I wrote it to stop treating `backward()` as magic.

What's in here:

- `autodidact/tensor.py` - the `Tensor` class, `no_grad`, and `backward()` (topo sort + grad accumulation)
- `autodidact/ops.py` - every op's forward and backward rule, one function each
- `autodidact/nn/` - `Module` with automatic parameter registration, `Linear`, `Embedding`, `LayerNorm`, `Dropout`,
  `Sequential`, `ModuleList`, a functional module (`cross_entropy`, `mse_loss`, `dropout`, activations), and a
  GPT-2 style transformer (`CausalSelfAttention`, `Block`, `GPT` with tied embeddings and `generate`)
- `autodidact/optim.py` - `SGD` (momentum, nesterov), `Adam`, `AdamW`, a cosine-with-warmup schedule, `StepLR`
- `autodidact/data.py` - a batch iterator, a train/val split, random next-token windows
- `tests/` - numerical gradient checks for every op and layer in float64, plus small end-to-end training tests
- `examples/train_gpt.py` - char-level GPT on a built-in text snippet (`--text file.txt` for something real)
- `examples/spiral.py` - a 2-layer MLP on the 3-arm spiral toy dataset

## usage

```python
import numpy as np
import autodidact as ad
from autodidact import nn, optim

data = np.random.randint(0, 65, 10000)           # your tokens go here
model = nn.GPT(vocab=65, block_size=32, n_layer=2, n_head=4, n_embd=64)
opt = optim.AdamW(model.parameters(), lr=3e-3, weight_decay=0.1)
for step in range(500):
    x, y = ad.data.windows(data, 32, bs=16)
    logits, loss = model(x, y)
    opt.zero_grad(); loss.backward(); opt.step()
model.eval()
print(model.generate(x[:1, :8], 50, temperature=0.8, top_k=10))
```

The tensor side looks like you'd expect:

```python
x = ad.randn(3, 4, requires_grad=True)
y = ((x @ x.T).tanh() * 2 + x[:, :3].exp()).log_softmax(-1).sum()
y.backward()
x.grad  # numpy array
```

## running things

```
python3 -m pytest -q            # ~5s
python3 examples/spiral.py      # well under a second
python3 examples/train_gpt.py   # 300 steps, under ten seconds here
```

Nothing needs installing; the examples put the repo root on `sys.path`. `pip install -e .` works too if you'd
rather import it from elsewhere.

## notes on the bits that bit me

- **unbroadcast.** Forward broadcasting is free in numpy, but the gradient of a `[3,1]` tensor that got
  broadcast to `[3,4]` has to be summed back over the broadcast axes, and leading axes that were added
  have to be summed away entirely. Every binary op's backward goes through one `unbroadcast(g, shape)`
  helper and it's the single most load-bearing function in the repo.
- **batched matmul.** `(..., n, k) @ (..., k, m)` with broadcasting batch dims is the same problem in
  disguise. `dA = g @ B^T`, `dB = A^T @ g`, then unbroadcast both to the original shapes. I got the
  reduction wrong twice before writing the `[2,3,4] @ [4,5]` test.
- **log_softmax stability.** `log(sum(exp(x)))` overflows around x=700 in float64 and x=89 in float32.
  Subtract the max first. `cross_entropy` is `log_softmax` plus a gather, never `log(softmax(x))`.
- **gather backward.** `grad[idx] += g` silently drops repeated indices. `np.add.at` doesn't. This is
  what makes `Embedding` work when the same token shows up twice in a batch, which is always.
- **the topo sort.** Reverse-mode needs every node's gradient to be complete before it's pushed to its
  parents, so `backward()` does a post-order DFS from the root and walks the result backwards. It's
  iterative because a recursive one dies at the default recursion limit on a chain of a few thousand ops,
  which a training loop that reuses tensors across steps can produce by accident. The graph is freed after
  the walk unless `retain_graph=True`.
- **max.** The gradient goes to the argmax only; ties aren't split. Same as torch, and the gradchecks
  avoid ties by using random inputs.
- **weight tying.** The GPT's output projection is `x @ wte.w.T`, no separate head. `parameters()` dedupes
  by identity so a tied tensor gets one optimizer slot even when it's registered under two names.

## limitations

- numpy only, CPU only, no GPU, and slow. The examples are sized so they finish quickly, not so they
  learn anything impressive; the built-in text for `train_gpt.py` is a few hundred characters and the
  samples are babble with roughly the right letter statistics.
- At these tiny matrix sizes BLAS threading is pure overhead: `train_gpt.py` pins numpy to one thread
  because a step went from roughly 60ms to 20ms on my machine when I did. If you scale the model up,
  unset `OMP_NUM_THREADS` and measure again.
- Every op materializes its output and its backward closure holds references to whatever it needs, so
  memory scales with graph size. There's no in-place anything and no checkpointing.
- `max` only takes a single int axis (or `None`). `where`, `cat`, `stack` are functions, not methods.
- Gradchecks run in float64. float32 is what you actually train in, and the only thing checking that
  path is the training tests actually converging.
- No conv, no rnn, no attention KV cache, no mixed precision. It's an autodiff engine with enough on top to
  train a small GPT, and that's the scope.
