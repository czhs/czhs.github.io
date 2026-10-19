---
layout: post
title: Clocktower Town agent notes
date: 2026-10-18 21:00:00-0700
description: biggest wins and pitfalls from directing coding agents to build a multiplayer game in 4 days
tags: agents games
categories:
related_posts: false
published: true
---

*Compiled by Claude (Opus 5.5) analysis agents from the project's Claude Code transcripts. Prompts in quotes are Chris's, verbatim, typos included.*

**Project:** [Clocktower Town](https://clocktower.chrisshi.com), a browser social-deduction game (Blood on the Clocktower rules, human Storyteller, proximity voice). Built 2026-10-14 → 10-18 almost entirely by Claude Code agents, directed by one person across two accounts.

| | |
|---|---|
| Span | 4.2 days, ~20 h of human attention, ~70 h of agent activity |
| Human prompts | 391, median 67 characters; 81 typed while an agent was mid-turn |
| Subagents | 736 (124 spawned directly, 612 inside 32 multi-agent workflows), all Opus |
| Output tokens | 31.9 M, 92% written by subagents (the main session mostly coordinated) |
| Shipped | v1 at +18 h, v2 at +27 h, six v3 releases on day 5; 206 commits, 2,174 tests passing |

**Where the effort went**

- **3D pixel-art pipeline:** 24% of prompts, 57% of output tokens. 0 of 31 characters reached the critic's ship bar.
- **Orchestration** (status checks, usage limits, handoffs, which machine runs what): 14% of prompts. This is about the agents, not the game.
- **Testing:** 1% of prompts, but 10% of source lines; the agents wrote tests without being asked.

## Biggest wins

**1. Contracts and boundaries before parallel work, and no faked verification.** The kickoff prompt:

> "You are the lead engineer and integrator, not a planning-only assistant. Start building now. … Establish message schemas, authoritative room/lobby lifecycles, per-client secret projection, and teammate file boundaries before parallel changes. … Don't fabricate verification or silently drop requirements."

- Skeleton in 14 min; 5 owner-per-path agents committed in 55 min; public URL at 1 h 20 m.
- The secrecy model (each client gets only its own view) held: no payload leak was found in 5 days.
- "Never claim a test passed that you did not run" went into the agent guide and later into most delegation prompts.

**2. Demanding evidence instead of "done."**

> "don't assume something works because its implementation exists or because a test passes."

- This brought in adversarial auditors that write failing tests from the official rules.
- After 89 green builder tests, they found 10 rules bugs (2 high severity) and three night-time information leaks.
- The builder's own tests had encoded the builder's misreading of the rules.

**3. A principle with its reason, not a list of features.**

> "the gamestate should be easily maleable by the storyteller, almost like props so the storyteller can adjust around bugs in the game/adapt to what is happening live"

- The agent saved it to memory 36 seconds later.
- It then settled design questions in later versions without being restated: Storyteller teleport tools instead of auto-teleports, and every game state editable.

**4. Policies beat instance fixes.**

> "bugs should be fixed as they arise, or during the pipeline upgrade phase"

- It became a module-fix step after every wave, which fixed the bug that made every character glide.

> "also there are some overlapping of emojis and tags and other indicators, those need to be addressed as well— all the possible stuff that can float on the head of a characeter"

- That produced one stacking system for every overhead element, instead of a patch per overlap.

**5. Anchoring to something that already exists, and giving the gameplay reason.**

> "The book should be a 3d sprite like the hand"

- 44 characters, fixed in one round.

> "will the animation look good at game speed? (same speed from v2's art, relatively speaking)"

- The agent measured the anchor from game code (≈4 body-heights/s) and turned it into a readability check.

> "perhaps they slap the seal onto the ground infront of the character— that would be a very clear vote. this is important so that butler can be played properly"

- After 14 prompts of vote-legibility feedback without a criterion, this one had a testable criterion: the Butler player must be able to see their master's vote. Later critic rounds tested exactly that.

**6. Cutting scope, and asking for measurement.**

> "can we deploy a finished v1 of the game with whatever assets we have, not hte overhaul?"

- v1.0.0 was live 18 min later, separate from the stalled art work.

> "is this process bottlenecked by antyhing? would improving performance right now improve the speed of the pipeline for the agents"

- The agent measured instead of guessing: 86% of agent time was model time, so halving render time would save about 5%. The real bottleneck was the usage limit.

**7. Letting the agent write the next brief.**

> "wind down for handoff, give me the prompt for the next session"

- The agent wrote a 3,007-character continuation prompt (read-first list, ordered steps, resource and deploy rules). The new session launched its swarm 3 minutes after the paste.
- Together with "your job is to send me frequent image/video updates", this is how most visual bugs were caught.

## Pitfalls

**1. An art goal no one could measure, pursued with a mandated tool.**

> "the art should be stunning, even though it is pixel sprites"

- That goal, plus a 12.8 KB brief requiring an image model, opened a ~19 h art track: ~60 prompts and ~150 image runs.
- It ended at "I actually really like the pixel art in the v1— just polish the map."
- **Instead:** lock a target image and an in-game mock first. Prefer art the agents write as code, so they can iterate on it deterministically.

**2. Agents grading their own work.**

- During the character run, the lead agent reported "25 of 31 characters are now at 19 or above".
- The independent critic's final review found 0 of 31 at the bar (mean 15.7/24). Self-scores ran about 3 points high, and 29 of 31 fix rounds were never re-checked.
- **Instead:** only scores from a separate, non-editing critic count, and every fix round gets re-scored.

**3. Usage limits treated as an edge case.**

> "make sure the pipeline and swarm runs automatically without you, you just send updates to the channel, so if your monitor fails, the night isn't wasted"

- The resume timer lived inside the same rate-limited session, so about 9 h of that night were lost anyway.

> "you may run at 8 parallel characters going forward"

- Changing parallelism mid-run altered the agent order, and the resume replayed 2–3 h of finished work.
- **Instead:**
  - Fix workflow settings for the whole run.
  - On a stop, launch a continuation that runs only the unfinished items in the journal.
  - Keep a dated handoff doc current at every checkpoint.

**4. Granting permission in chat.**

> "You have all permissions"

- Claude Code's safety check refused five times in a row, moments before a flight. Approval given in chat does not override it; only settings rules do.
- **Instead:** add the allow rules (or choose the permission mode) before going unattended, and ban commands that trigger prompts (glob `rm`), which had also stalled overnight runs.

**5. Verbs that can be read two ways.**

> "commit everything to a branch now, there have been changes to remote"

- The agent began staging; the reply came 12 seconds later: "oh i didn't mean commit now".

> "manage session limit to make sure you don't get stopped by it"

- Pasted into two sessions, both read it as "ration usage". Both needed "the point is that you can continue between session boundaries."
- **Instead:** state the outcome, not the verb.

**6. Performance proxies.**

> "Any normal GPU, including laptop integrated graphics, draws this kind of scene in milliseconds."

- That was the agent's claim. A draw-call cut of 17–19% made frames slower.
- A 12.8 s first load surfaced only when a real laptop was tested, after the release was in production.
- **Instead:** put the target device in the loop from the first 3D build, and require every budget to state its exact measurement command.

**7. Nine requests in one message.**

- A 1,009-character prompt bundled hosting, layout, interiors, performance, the intro and the roster. It needed about 12 follow-ups.
- Short prompts tied to one thing almost always landed.

## Rules worth copying

- One owner per path, including across forked sessions. A fork once overwrote the main session's file beyond recovery.
- Every delegation prompt names the owned files, the exact verification commands, and a report format with copied output.
- Critics and auditors never edit; builders never grade themselves.
- Ask "is it done?" and expect a verified/unverified split.
- Write every tracked file as if the repo were public from commit 1. Keep host details in gitignored local files, and secret-scan on pre-push.
- Keep agent load off the production machine, or cap it from the first run.
- Pin the model and settings on every machine that runs agents.

*Not covered: a remote orchestrator that ran the day-5 v3 releases from another machine; its transcripts weren't collected.*
