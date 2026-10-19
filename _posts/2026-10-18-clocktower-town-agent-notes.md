---
layout: post
title: Clocktower Town agent notes
date: 2026-10-18 21:00:00-0700
description: project statistics and the sources given to the coding agents that built a multiplayer game in 4 days
tags: agents games
categories:
related_posts: false
published: true
_styles: >
  #markdown-content table tbody tr:hover,
  #markdown-content table tbody tr:hover td,
  #markdown-content table tbody tr:hover th {
    color: inherit !important;
    background-color: transparent !important;
  }
---

*Compiled by Claude (Opus 5.5) from the project's Claude Code transcripts.*

**Project:** [Clocktower Town](https://clocktower.chrisshi.com), a browser social-deduction game (Blood on the Clocktower rules, human Storyteller, proximity voice). Built 2026-10-14 → 10-18 almost entirely by Claude Code agents, across two accounts.

| | |
|---|---|
| Span | 4.2 days, ~21 h of human attention, ~70 h of agent activity |
| Subagents | 736 (124 spawned directly, 612 inside 32 multi-agent workflows), all Opus |
| Output tokens | 31.9 M, 92% written by subagents |
| Shipped | v1 at +18 h, v2 at +27 h, six v3 releases on day 5; 206 commits, 2,174 tests passing |
| Effort | 3D pixel-art pipeline: 24% of prompts, 57% of tokens. Testing: 1% of prompts, 10% of source lines |

## Sources given to the agents

**Rendering and animation research (the pixel3d pipeline)**

- David Holland, [3D Pixel Art Rendering](https://www.davidhol.land/articles/3d-pixel-art-rendering/)
- t3ssel8r videos:
  - [Making an Animation for my 3D Pixel Art Game](https://www.youtube.com/watch?v=1FrIBkuq0ZI)
  - [Giving Personality to Procedural Animations using Math](https://www.youtube.com/watch?v=KPoeNZZ6H4s)
  - [Procedural Pixel Art Fire](https://www.youtube.com/watch?v=erQ8PvxIjS8)
  - [Parallax Effect for 3D Pixel Art Engine](https://www.youtube.com/watch?v=cCUCMBmc9yQ)
- t3ssel8r's [Pixel Animation Importer](https://gist.github.com/t3ssel8r/aba0b33369ea620a63917f4ac21fd585) and Patreon notes
- [godot-3d-pixel-art](https://github.com/Robert-K/godot-3d-pixel-art)
- [DynamicsStudy](https://github.com/iggigabriel/DynamicsStudy) and a [SecondOrderDynamics gist](https://gist.github.com/Andicraft/ab605dda924a0321e755abf8f573ebd7)
- Kody King's [three.js 3D pixel-art shader](https://github.com/KodyJKing/hello-threejs)
- Roystan's [outline](https://roystan.net/articles/outline-shader/), [toon](https://roystan.net/articles/toon-shader/) and [water](https://roystan.net/articles/toon-water/) shaders
- [WiseFrame's Godot pixel-art shader series](https://wiseframe.dev/godot-pixel-art-shaders-pipeline-and-quantization)
- a [Unity isometric pixel pipeline](https://github.com/bababuyyy/unity-isometric-pixel-pipeline)
- an [outline + highlight shader](https://godotshaders.com/shader/3d-pixel-art-outline-highlight-post-processing-shader/)
- Catlike Coding's [custom render pipeline](https://catlikecoding.com/unity/tutorials/custom-srp/)

These became a research swarm. Its output was a techniques doc, the character pipeline's contract, playbook, 12-point rubric and learnings log, and then the build runs. Reference frames were used only for critique; all shipped art is procedural code.

**Visual references**

- Concept art and screenshots attached in chat (about 28 prompts carried images)
- Town of Salem, for the town layout: clocktower at the top, houses in a ring
- The game's own v1 procedural pixel art, kept as the v2 style and used as the speed and scale anchor for v3

**Content**

- CMU course mascots, [r/cmu](https://www.reddit.com/r/cmu/) and the [CMU Readme](https://cmureadme.com/) archive, used for student humor; they became 20 in-town easter eggs.
