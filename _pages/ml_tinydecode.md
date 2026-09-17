---
layout: portfolio_post
portfolio: ml
permalink: /ml/tinydecode/
project: tinydecode
standalone_title: "tinydecode — Chris Shi"
nav: false
---

<!-- The write-up is the repository's README, verbatim (the H1 dropped: the
     layout renders the title). Edit it upstream and re-copy rather than here. -->

<p class="rbx-post-src">From the repository README</p>

A small llama-style inference runtime I wrote to understand where the time
actually goes in single-stream decoding. It's not a serving system. One
request at a time (batching works but isn't the point), static shapes
everywhere, and the decode step is as close to "one graph replay per token"
as I could get it.

What's in here:

- a plain llama/tinyllama/llama-3 model in `model.py` with three attention
  paths: `prefill` (causal over the prompt), `decode` (one token against the
  cache) and `chunk` (a few tokens on top of existing context, used to verify
  speculative drafts)
- a static, preallocated kv cache (`kv_cache.py`). `seq_lens` lives on the
  device so the decode step never touches the host
- fused cuda kernels in `csrc/`: rmsnorm and residual-add + rmsnorm, in-place
  rope, silu*up, and a split-kv single-query attention kernel for decode
  (flash-decoding style: chunks of the cache in parallel, then a log-sum-exp
  merge). Every kernel has a plain torch twin in `ops/ref.py` that it's tested
  against, and everything falls back to torch on cpu or with
  `TINYDECODE_NO_EXT=1`
- cuda graph capture of the whole decode step (`graphs.py`), and of the
  fixed-size verify pass when spec decoding
- speculative decoding (`speculative.py`) with either a smaller draft model or
  free n-gram prompt lookup, with the proper rejection-sampling scheme so
  sampling at temperature > 0 still matches the target distribution exactly
- latency instrumentation that costs nothing: cuda events per decode step,
  synced once at the end. `Stats` gives ttft, itl p50/p99, tok/s, acceptance rate

## using it

```
pip install -e ".[hf]"
python scripts/generate.py path/to/TinyLlama-1.1B-Chat-v1.0 -p "The capital of France is" -n 64
python scripts/generate.py path/to/Llama-3.2-3B --draft path/to/Llama-3.2-1B -k 5
python scripts/generate.py path/to/Llama-3.2-3B --ngram -p "$(cat some_file.py)"
```

Models are loaded straight from a huggingface llama-format directory
(`config.json` + safetensors + `tokenizer.json`). The cuda extension is
jit-built the first time a cuda tensor hits an op; give it a minute on the
first run, or `python setup.py install` once.

From python:

```python
from tinydecode import Engine, load_hf, Tokenizer, graphs, speculative

model = load_hf("path/to/model", device="cuda", dtype=torch.bfloat16)
tok = Tokenizer("path/to/model")
eng = graphs.enable(Engine(model, max_seq_len=4096))

ids, stats = eng.generate(tok.encode("hello"), max_new_tokens=100, temperature=0.7, top_p=0.9)
print(tok.decode(ids))
print(stats.summary())

# same thing with a draft model
draft = graphs.enable(Engine(load_hf("path/to/small-model", device="cuda", dtype=torch.bfloat16)))
ids, stats = speculative.generate(eng, speculative.ModelDrafter(draft), tok.encode("hello"), k=5)
print(stats.acceptance_rate)
```

## how the decode step is put together

Per token, eager torch on a small model spends most of its time launching
kernels, not running them. So the shape of the whole thing is: make every
step identical, then replay it.

- The engine feeds `step(tokens)` exactly one `[B, 1]` tensor. Positions come
  from `cache.seq_lens`, the kv write is an `index_put_` at those positions,
  attention masks by `j < seq_len`. No shape depends on how far along we are.
- `graphs.GraphedStep` warms up on a side stream (jit build, cublas
  workspaces, allocator pools), captures one `_eager_step`, and afterwards
  `step` is a `copy_` into the token buffer and a `replay()`.
- The residual stream is handled by `add_rmsnorm`, so each block is: attn ->
  fused (add + norm) -> mlp -> fused (add + norm), and the next block's input
  norm is already done when we get there.
- The only sync per token is the `.tolist()` to feed the sampled id back
  and check for eos. It's the same sync everyone has.

The decode attention kernel is the interesting one. Grid is `(batch, q_head,
split)`, each block takes a 256-key chunk of the cache, does scores ->
softmax stats -> `p @ V` for its chunk with the query in shared memory, and
writes `(m, l, acc)`. A second tiny kernel merges the splits. That keeps the
sm's busy at batch 1 where "one block per head" would leave most of the gpu
idle at long context. GQA is handled by mapping q head -> kv head in the
index math, no `repeat_interleave` copies.

## speculative decoding

`speculative.generate` runs draft -> verify -> accept rounds. The verify pass
is the `chunk` attention path over `k+1` tokens, and since `k` is fixed it
gets its own cuda graph. That path folds the q-head group into the sequence
axis before calling sdpa, so the cache is read once per layer instead of
being copied once per group. Acceptance is the usual `min(1, p_t/p_d)` per
token, vectorized with one sync for the accept count, and the extra token
comes from the residual `(p_t - p_d)+` at the first rejection (or the bonus
row if everything went through). At temperature 0 this collapses to
"accept while argmax matches", which is what the tests check against plain
greedy decoding.

Rollback is trivial with a static cache: `seq_lens.fill_(n)`. The stale
entries past that are never read.

The n-gram drafter needs no second model: it looks for the last few tokens
earlier in the sequence and proposes what followed. Useless on prose, great
on code and anything that quotes its input.

## numbers

I don't want to paste numbers that go stale, so:

```
python bench/latency.py path/to/model --new 128      # eager/graphs x torch/fused, prints a markdown table
python bench/spec.py path/to/model --draft path/to/small -k 3 5 8
python bench/spec.py path/to/model --ngram
```

Both accept `--tiny` to run on random weights as a smoke test (also works
on cpu, which is how the test suite runs on my laptop).

## tests

```
pip install -e ".[dev]"
pytest
```

Everything runs on cpu through the torch fallbacks. The cuda tests
(kernels vs reference in fp32/fp16/bf16, graph capture, graphed vs eager
generation) skip themselves without a gpu.

## not done / known gaps

- no paged attention, no continuous batching, no quantization. Batch > 1
  works (right-padded prefill, per-row lengths) but nothing is tuned for it
- prefill uses `scaled_dot_product_attention`, which is fine; the custom
  kernel is decode-only
- only the llama3 flavour of rope scaling; qwen-style qkv biases aren't loaded
- the n-gram lookup is a python loop over the token list. Fine for a few
  thousand tokens, would want a hash map past that
- mps is untested, cpu is only for correctness
