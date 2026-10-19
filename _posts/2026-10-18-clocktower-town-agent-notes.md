---
layout: post
title: Clocktower Town agent notes
date: 2026-10-18 21:00:00-0700
description: the patterns, prompts and sources that worked when directing coding agents to build a multiplayer game in 4 days
tags: agents games
categories:
related_posts: false
published: true
---

*Compiled by Claude (Opus 5.5) analysis agents from the project's Claude Code transcripts and checked by separate fact-checking agents. Prompts in quotes were typed by Chris: spelling is corrected, wording is unchanged, and "…" marks a trim. Quotes marked as an agent's words are the agent's.*

**Project:** [Clocktower Town](https://clocktower.chrisshi.com), a browser social-deduction game (Blood on the Clocktower rules, human Storyteller, proximity voice). Built 2026-10-14 → 10-18 almost entirely by Claude Code agents, directed by one person across two accounts.

| | |
|---|---|
| Span | 4.2 days, ~21 h of human attention, ~70 h of agent activity |
| Subagents | 736 (124 spawned directly, 612 inside 32 multi-agent workflows), all Opus |
| Output tokens | 31.9 M, 92% written by subagents |
| Shipped | v1 at +18 h, v2 at +27 h, six v3 releases on day 5; 206 commits, 2,174 tests passing |
| Effort | 3D pixel-art pipeline: 24% of prompts, 57% of tokens. Testing: 1% of prompts, 10% of source lines |

## Patterns that worked

**1. Separate judging agents.** Builders never graded their own work; a different agent did.

| Judge | What it caught |
|---|---|
| Rules auditor (writes failing tests from the official rules) | 10 engine bugs (2 high severity) after the builder's 89 tests had passed; fixed within the hour |
| Secrecy auditor | 3 information leaks around night phases, e.g. the Storyteller still visible after night |
| Hostile-client harness (33 message types, 50 Storyteller commands) | Arrival time of night info leaked roles in automatic games |
| Art critics | Self-scores ran ~3 points high. The lead reported "25 of 31 characters are now at 19 or above" (agent's words); the critic found 0 of 31 at its ship bar of 19/24 |
| Live-build playtest critics | Missing portraits on the live site; vote marks on the wrong player in 4 of 15 seats |
| Design reviewers (feasibility, risk) | Revised the v3 integration contract before any build agent ran |

The judges were non-editing. The lead agent's prompt to one critic (agent's words):

> "Do NOT edit project files. … LOOK at every screenshot you cite. … Butler test: could a Butler watching ONE chosen master tell in real time when the master slaps, withdraws and locks? … Score 0-2 per criterion, /16, ship bar 13. For each issue give P1/P2/P3, exact repro, the screenshot path, and a concrete fix (file/function)."

**2. A main chat that manages agents and sends frequent images.**

> "while the agents are running, your job is to send me frequent image/video updates"

> "your job is to send me frequent images and videos of the animations progress, while the foundation agent works"

- The main sessions acted as managers: 112 agent spawns, 19 file edits.
- A watcher sent new renders every 4–5 min: about 230 images and clips over the project, 95 in one character session.
- Several errors were caught from these images rather than by agents:
  - a character's face in the wrong place;
  - a hidden door, then an unenterable house;
  - sliding cobblestones;
  - a debug view (stray pixels marked magenta) that the lead had been sending, and misreading as real defects, for ~21 h.

**3. A live demo maintained while it was being built.**

> "send agents to release what you have as you go, while also continuing to send me the visual updates"

- More than a dozen versioned builds went out from 10-16 to 10-18. The first interim build was live 4 min after the prompt, followed by a 30-min release loop.
- Later publishes checked for 60 fps, 0 security-policy violations and no missing files. Content-hashed paths stopped the CDN from serving stale builds.
- Collaborators could test the real thing, and playtest critics judged the live build rather than a local copy.
- The same habit shipped the game itself: v1 went to production with the art it had, instead of waiting for the art overhaul.

## Most valuable prompts

**A principle with its reason**

> "… the gamestate should be easily malleable by the storyteller, almost like props so the storyteller can adjust around bugs in the game/adapt to what is happening live"

- Saved to memory within a minute; it drove the v2 Storyteller panel (force seats and phases, teleport, edit any state).

> "we don't need to worry too much about game cheating behavior, security was mostly to make sure my own computer and my home stays safe while hosting the server"

- It re-weighted two running security agents and became a standing priority rule: isolate the host first, never trade voice UX for anti-cheat.

**A policy instead of a fix**

> "bugs should be fixed as they arise, or during the pipeline upgrade phase"

- It became a module-fix step after every wave of agents. That step fixed the shared bug that made every character glide instead of walk.

> "also there are some overlapping of emojis and tags and other indicators, those need to be addressed as well— all the possible stuff that can float on the head of a character"

- One stacking system for every overhead element, instead of a patch per overlap.

**Questions an asset designer can check**

> "each agent should also think about what is unique to their character. do extra things have to be animated? should it walk in a different way? how should expressions adapt to the new artstyle? will the animation look good at game speed? (same speed from v2's art, relatively speaking)"

- It became a required "unique to me" section in every character sheet, enforced by critics.
- Game speed was measured from the game code (≈4 body-heights/s).
- The 31 characters got distinct gaits (hop, waddle, glide) and signature emotes.

> "make sure to also get the storyteller, since it's a character as well. the storyteller should be visually distinct from all the other characters"

- The lead, summarising the critic: "the most distinctive member of the cast, even at quarter size" (agent's words).

**Art direction anchored to something that exists, with the gameplay reason**

> "The book should be a 3d sprite like the hand"

- 44 characters; fixed in one round.

> "… perhaps they slap the seal onto the ground in front of the character— that would be a very clear vote. this is important so that butler can be played properly"

- The Butler criterion became the test every later critic round ran (see the judge prompt above).

**Asking for measurement and independent checks**

> "is this process bottlenecked by anything? would improving performance right now improve the speed of the pipeline for the agents"

- The agent measured instead of guessing: 86% of agent time was model time, so halving render time would gain about 5%. The real bottleneck was the usage limit.

> "is the art demo up? send an agent to make sure it has all the new stuff you've worked on"

- A separate read-only audit found the new UI was not live and an unfinished character was still shipping publicly. Both were fixed within 45 min.

**Scope cuts, priorities, handoffs**

> "can we deploy a finished v1 of the game with whatever assets we have, not the overhaul?"

- v1.0.0 was live 18 min later, separate from the stalled art work.

> "I only care about perf of v3 now, v2 is fine"

- The running performance workflow was relaunched v3-only within a minute; the rule was saved to memory.

> "wind down for handoff, give me the prompt for the next session"

- The agent wrote a 3,007-character continuation brief (read-first list, ordered steps, resource and deploy rules). The next session launched its swarm 3 min after the paste.

## Sources given to the agents

Everything Chris supplied that informed the agents' work, beyond typed instructions.

**Specs and pre-written briefs (pasted)**

- **`CLOCKTOWER_TOWN_SPEC.md`**, the authoritative implementation spec attached to the first prompt: decision summary, stack, UX, secrecy model.
  - Its named inspirations were the physical staging of Minecraft Blood on the Clocktower and the lobby experience of Town of Salem.
- **A kickoff brief.** It set up a lead integrator plus 5 owner-per-path agents, contracts before parallel work, and "Don't fabricate verification or silently drop requirements."
  - Result: skeleton in 14 min, 5 modules in 55 min, a public URL at 1 h 20 m.
- **Readiness, security and sound briefs.**
  - The readiness brief said "don't assume something works because its implementation exists or because a test passes". It brought in the rules and secrecy auditors above.
  - The sound brief limited sources to CC0: Kenney audio packs, Freesound filtered to CC0, and OpenGameArt. It produced 35 sounds (1.03 MB) with a credits file.

**Rendering and animation research (the pixel3d pipeline)**

- David Holland, [3D Pixel Art Rendering](https://www.davidhol.land/articles/3d-pixel-art-rendering/).
  - It started a research swarm: 4 researchers, a synthesized techniques doc, then 10- and 21-agent build runs.
- t3ssel8r videos: [1FrIBkuq0ZI](https://www.youtube.com/watch?v=1FrIBkuq0ZI), [KPoeNZZ6H4s](https://www.youtube.com/watch?v=KPoeNZZ6H4s) (procedural animation with second-order dynamics), [erQ8PvxIjS8](https://www.youtube.com/watch?v=erQ8PvxIjS8), [cCUCMBmc9yQ](https://www.youtube.com/watch?v=cCUCMBmc9yQ).
  - They came with a ChatGPT-compiled list of implementations, passed on as "suggestions by chatgpt, you may use whatever you find helpful":
    - t3ssel8r's [Pixel Animation Importer](https://gist.github.com/t3ssel8r/aba0b33369ea620a63917f4ac21fd585)
    - [godot-3d-pixel-art](https://github.com/Robert-K/godot-3d-pixel-art)
    - [DynamicsStudy](https://github.com/iggigabriel/DynamicsStudy) and a [SecondOrderDynamics gist](https://gist.github.com/Andicraft/ab605dda924a0321e755abf8f573ebd7)
    - Kody King's [three.js 3D pixel-art shader](https://github.com/KodyJKing/hello-threejs)
    - Roystan's [outline](https://roystan.net/articles/outline-shader/), [toon](https://roystan.net/articles/toon-shader/) and [water](https://roystan.net/articles/toon-water/) shaders
    - [WiseFrame's Godot pixel-art shader series](https://wiseframe.dev/godot-pixel-art-shaders-pipeline-and-quantization)
    - a [Unity isometric pixel pipeline](https://github.com/bababuyyy/unity-isometric-pixel-pipeline)
    - an [outline + highlight shader](https://godotshaders.com/shader/3d-pixel-art-outline-highlight-post-processing-shader/)
    - t3ssel8r's Patreon notes
    - Catlike Coding's [custom render pipeline](https://catlikecoding.com/unity/tutorials/custom-srp/)
  - These produced the character pipeline's contract, playbook, 12-point rubric and learnings log, followed by an 11-agent build.
  - Reference frames served only as references for critics and authors; all shipped art is procedural code.

**Visual references**

- **Concept art and screenshots** attached in chat: about 28 prompts carried images, mostly the target look or a UI screenshot.
- **Town of Salem**, for the town layout: "clocktower should be at the top, houses arranged around like in the town of salem".
- **The game's own earlier art**, as an anchor: v1's procedural pixel art (kept as the v2 style), v2 sprite speed and scale, and "like the hand".

**Content sources**

- CMU course mascots, supplied by Chris, plus [r/cmu](https://www.reddit.com/r/cmu/) and the [CMU Readme](https://cmureadme.com/) archive for student humor. These fed 20 in-town easter eggs.

## Pitfalls

- **Art target not locked.** An image-model art track toward an HD-2D look ran 16–19 h before the project went back to v1's procedural pixel art.
  - *Do instead:* fix a target image and an in-game mock before scaling art agents, and prefer art written as code.
- **Unchecked self-grading.** See the art-critic row above; 29 of 31 fix rounds were never re-scored.
  - *Do instead:* only a separate critic's score counts, including after every fix.
- **Usage limits.** Unattended runs lost about 9 h on each of two nights. On the first, the resume timer lived inside the rate-limited session. Changing parallelism mid-run made a resume replay 2–3 h of finished work.
  - *Do instead:* fix workflow settings for the whole run, continue from the journal of finished items, and keep a dated handoff doc.
- **Permissions.** Approval given in chat does not override Claude Code's safety checks, and glob `rm` commands stalled unattended agents on prompts.
  - *Do instead:* set allow rules and a safe cleanup script before going unattended.
- **Performance proxies.** An agent claimed "Any normal GPU, including laptop integrated graphics, draws this kind of scene in milliseconds" (agent's words). A real laptop later showed a 12.8 s first load, after release.
  - *Do instead:* put the target device in the loop from the first 3D build.

## Rules worth copying

- Hidden-role games:
  - The server is authoritative, and each client receives only its own projection of the state.
  - Test it with a hostile-client harness that covers position, timing and voice side channels, not just message payloads.
- Every delegation prompt names the owned files, the exact verification commands, and a report with copied output. One owner per path, including across forked sessions.
- Write every tracked file as if the repo were public from commit 1; secret-scan on pre-push.
- Keep agent load off the production machine, or cap it from the first run.
- Pin the model and settings on every machine that runs agents.

*Not covered: a remote orchestrator that ran the day-5 v3 releases from another machine; its transcripts weren't collected.*
