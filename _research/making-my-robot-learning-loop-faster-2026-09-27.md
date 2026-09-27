---
layout: research_public
title: Making my robot learning loop faster
date: 2026-09-27 18:00:00-0400
description: Profiling a SmolVLA pipeline, finding its real bottleneck, and keeping the speedups that survived an accuracy check.
related_posts: false
authorship_note: Optimizations by a performance agent; post drafted with Codex from its report.
---

I wanted to learn more about optimization, partly after reading [Daphne Cornelisse's post about making an electric-fish simulation fast](https://daphnecornelisse.substack.com/p/training-artificial-electric-fish). I had a smaller problem close at hand: my SO-101 simulation pipeline generates robot demonstrations, fine-tunes SmolVLA to pick up a red cube, and evaluates the policy in closed loop. I asked a performance agent to find out where the time went and which shortcuts preserved the experiment.

The training profile ruled out a plausible suspect. The dataset is stored as AV1, and every batch reads frames, so video decoding might have been expensive. Instead, the data loader occupied less than 0.2% of a step on the RTX 4090. The expensive part was the *frozen* image encoder and connector: about 80 of the original 151 milliseconds per step. Over a 50,000-step run, the same 110,479 frames passed through that frozen computation roughly 14 times.

That changed the question from “how do I load images faster?” to “why compute the same image features again?” The agent cached the features once, then worked through the remaining step: it removed language-padding tokens from a no-gradient prefix, limited the gradient pass to the state and action tokens, used fused AdamW, and compiled the two passes. The cache took 6.7 minutes to build on the 4090 and occupies 13.6 GB, so it is a time-for-storage trade. Caching the entire transformer prefix looked like a further step, but would have needed about 174 GB to save at most another 7 milliseconds per training step.

On an idle 4090 with batches preloaded, the training step went from **6.6 to 38.1 steps per second**. That 5.8× figure is a step benchmark, not the speed of a whole experiment. In full runs, the new trainer reached about **27–29 steps per second** when it had the GPU to itself. Two 50,000-step runs, with checkpoint evaluations and some GPU sharing, finished in **49.8 and 52.0 minutes**. The older training run took about 2.3 hours, plus its evaluations.

The other stages produced a more interesting lesson than “faster is better.” During demonstration generation, the expert does not look at the camera images. Rendering at the 50 Hz control rate meant discarding four out of five frames; rendering only the recorded frames and streaming them to the video encoder made a short parallel benchmark **1.8× faster**, with identical dataset files. Those changes are still a prototype rather than part of the dataset builder.

Evaluation had a tempting shortcut: run ten simulated robots together so the policy can process their observations in a batch. On 30 quick episodes, success was 16/30 both ways, and the batched version was about 4.5× faster. On the larger set of 100 paired seeds, though, the batched version succeeded **64 times versus 75** for the original evaluator, losing 16 episodes and gaining five. Small numerical changes in batched inference changed individual trajectories. The agent kept the exact evaluation changes—render only frames the policy reads and skip the unused wrist camera—but set the standard evaluator back to one environment at a time. That path reproduced all 30 tested trajectories and gave a more modest **1.25×** speedup on the loaded RTX 3060.

I like that the fastest evaluation configuration didn't become the default. The training changes passed numerical checks against the original step and a 2,000-step same-seed loss-curve comparison; the ten-environment evaluator failed its larger outcome comparison. A faster loop matters because it lets me test more ideas, but only if I can still tell whether a changed result came from the idea or from the loop itself.
