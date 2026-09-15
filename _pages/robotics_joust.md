---
layout: portfolio_post
portfolio: robotics
permalink: /robotics/joust/
project: joust
standalone_title: "Robot Jousting — Chris Shi"
nav: false
---

<!-- Every paragraph below is verbatim from the write-up at /robo-jousting/
     (_pages/robo-jousting.md). Trim to real phrases if it has to shrink; do not
     reword. The hero, the path, the galleries and the prev/next links all come
     from _data/robotics.yml. -->

## Driving the arms live

At the start of a match the game prepares the hardware: home the rails, move apart, both
arms to rest. It drives the carriages together for the charge and apart for the return,
plays each beat on both arms, and waits on the arms' own busy flags rather than on
timers. The screen beat is stretched to the real motion — an overhead chop is 4.5 s of
arm time, not the 1.4 s the screen would take on its own.

A mock daemon carrying the real motion timings lets the whole thing be rehearsed with no
hardware attached. In rehearsal the screen never released before the arms, with a worst
margin of +23 ms.

Players choose their own openers and finishing flourishes. The En garde opener runs
before the first beat; the Samurai finish runs after the knockout, with the winner
raining blows while the loser collapses. Both stream the rail carriages in time with the
arm motions.

The arms sit on stepper rails and charge in to 19.5 inches of each other.

## Calibration, by hand

The arms' servo calibrations live in the repo, in `calib/`. We calibrated the SO-100 by
holding it at the zero pose and sweeping every joint to its stops, then checked the zero
points against physical references — the arm leaning fully back on its board, the
upright square pose, the blade sitting on top of the gripper — before we trusted the
taught moves on the real arm.
