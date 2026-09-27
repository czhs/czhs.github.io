---
layout: research_public
title: Speeding up the SO-101 experiment loop
date: 2026-09-27 18:00:00-0400
description: Faster SmolVLA training, an evaluation shortcut that failed, and more room for careful measurement.
related_posts: false
---

A 50,000-step SmolVLA run on my simulated SO-101 pick-and-place task used to take about 2.3 hours to train, plus checkpoint evaluations. With a new pipeline, two full runs took **49.8 and 52 minutes**, evaluations included. After reading [Daphne Cornelisse's electric-fish optimization post](https://daphnecornelisse.substack.com/p/training-artificial-electric-fish), I had a performance agent profile this loop and find out which parts could be made faster.

## The bottleneck wasn't video

The demonstrations are stored as AV1 video, so decoding seemed like a reasonable place to look. The profiler disagreed: waiting for data took less than 0.2% of a training step on the RTX 4090. Nearly half the step was spent running the frozen image encoder and connector. Over 50,000 steps, the model recomputed features for the same 110,479 frames about 14 times.

The fix was to cache those features once. The cache takes 6.7 minutes to build and uses 13.6 GB. The agent then removed unused language-padding tokens from the no-gradient prefix, restricted the gradient pass to the state and action tokens, switched to fused AdamW, and compiled both passes. On an idle 4090 with batches already loaded, the step went from **6.6 to 38.1 steps/s**. End-to-end training throughput was lower, around 27–29 steps/s. The two full runs above used different camera setups and shared the GPU for part of their runtime, so they aren't matched end-to-end benchmarks.

There were smaller wins elsewhere. The demonstration generator was rendering camera frames at 50 Hz even though it only recorded them at 10 Hz. Rendering only the recorded frames and streaming them to the encoder made a short parallel benchmark **1.8× faster**, with identical output files. That change is still a prototype, not yet in the dataset builder.

## The shortcut that failed

Evaluation looked like an easy place to go faster: batch ten simulated robots into each policy call. In a 30-episode test, one batched version went from 2.42 to 0.98 seconds per episode, with success at 16/30 in both versions. Synchronizing the batch brought it down to 0.54 seconds, but success fell to 14/30. Then the agent tried 100 paired seeds: the batched evaluator succeeded on **64**, while the original succeeded on **75**. Small changes in batched numerical computation were enough to flip trajectories, and the losses were not balanced by gains.

So the default evaluator still runs one environment at a time. It skips camera renders the policy never reads, which reproduced all 30 tested trajectories and was about **1.25× faster** on the loaded RTX 3060. The more dramatic batching number isn't a usable speedup for the comparisons I care about.

The time saved on training goes into more evaluation rollouts: hundreds per condition instead of a few dozen. This has brought the confidence interval on success rate from roughly **±15 percentage points down to about ±5**.
