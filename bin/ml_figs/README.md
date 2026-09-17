# bin/ml_figs — figures for the /ml/ portfolio

The card covers and gallery figures of the two DLSys projects on `/ml/` are real
output of the repos' own code, drawn in the site palette (literals from
`_includes/portfolio_styles.liquid`) with the site's JetBrains Mono. Nothing is
drawn by hand. Jekyll-excluded like the rest of `bin/`.

    # autodidact: runs examples/spiral.py's setup + examples/train_gpt.py's loop
    # verbatim (seed 0) and walks Tensor._prev for the graph; ~15 s on a laptop
    git clone https://github.com/czhs/autodidact /tmp/autodidact
    python3 bin/ml_figs/fig_autodidact.py /tmp/autodidact assets/img/ml

    # tinydecode: reads the bench output kept in bench/ (no GPU needed to redraw)
    python3 bin/ml_figs/fig_tinydecode.py bin/ml_figs/bench assets/img/ml

`bench/` is the stdout + JSON of one run of the repo's own benchmarks on the
RTX 4090 box (2026-09-17; details and the exact commands in
`docs/claude/robotics-ml-portfolio.md`). To re-measure, re-run `bench/latency.py`
(`--json`) and `bench/spec.py` there and replace these files.

Both scripts want `numpy`, `matplotlib` and, for the font, `fonttools` + `brotli`
(they decompress `assets/fonts/jetbrains-mono-latin-var.woff2` into `fonts/` once;
without them the figures fall back to Menlo). Outputs land in the (gitignored)
`assets/img/ml/`; publish with `gh release upload ml-media <files> --clobber`.
