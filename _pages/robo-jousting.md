---
layout: page
permalink: /robo-jousting/
title: "The Tilt of Tiltford: robot jousting"
description: Two real robot arms with 3D-printed swords fence each other on stepper rails while a crowd plays from their phones. Built at HackCMU 2026.
standalone_title: "The Tilt of Tiltford — robot jousting"
nav: false
---

<figure class="rj-hero" style="margin: 0 0 2rem">
  <video
    controls
    playsinline
    preload="metadata"
    width="100%"
    style="width: 100%; height: auto; border-radius: 6px"
    poster="{{ '/assets/img/robo-jousting/tilt_trailer_poster.jpg' | relative_url }}"
  >
    <source src="{{ '/assets/img/robo-jousting/tilt_trailer.mp4' | relative_url }}" type="video/mp4">
    Your browser does not support the video tag.
  </video>
  <figcaption class="caption">
    The Tilt of Tiltford — trailer.
    Also on <a href="https://youtu.be/A5sqve7kuhc">YouTube</a>.
  </figcaption>
</figure>

## What it is

Two real SO-100/SO-101 robot arms, each holding a 3D-printed sword, fence each other
on stepper rails at a medieval festival. Players fight from their phones. A crowd
watches. It is an HRI experiment in whether a machine can make a room of people
cheer.

We built it at HackCMU 2026, on 12 September 2026.

{% include figure.liquid
   path="assets/img/robo-jousting/sim_orbit_engarde_hero.webp"
   alt="Two robot arms facing each other on rails, swords raised en garde"
   caption="En garde. Both arms on their rails, blades up, before the first beat."
   zoomable=true
%}

{% include figure.liquid
   path="assets/img/robo-jousting/screencap_01_title.webp"
   alt="The Tilt of Tiltford title screen, a medieval festival scene"
   caption="The big screen the crowd watches."
   zoomable=true
%}

## Two phones, one arena

Two players scan QR codes, name their knight, tune a deck, and plan three moves in
secret. The big screen holds the rules, so nobody can cheat: phones send intents to a
long-polled mailbox server and the host resolves them.

The host is resumable, seats can be reissued, and the plan timer auto-locks a player
who has wandered off — all the things that go wrong when the arena is a festival and
the players are strangers.

There is also a single-player campaign against three AI knights: Bluebell the squire,
Sir Percival, and the Iron Champion.

{% include figure.liquid
   path="assets/img/robo-jousting/06_lobby_qr.webp"
   alt="Lobby screen showing two QR codes, one for the red knight and one for the blue knight"
   caption="The lobby: two codes, two knights."
   zoomable=true
%}

{% include figure.liquid
   path="assets/img/robo-jousting/07_phone.webp"
   alt="The phone controller showing a hand of cards"
   caption="What a player holds: a hand of cards and three slots to fill in secret."
   zoomable=true
%}

## The game

Attacks land on a high line or a low line. Guards cover a line; feints sell a line you
are not using. Voltage loads with feints and pays out later.

Rush charges down the rail and beats any swing — but a guard stops it cold. Two rushes
in a row make a Full Tilt, which goes through any guard. Counter throws a blow back at
the knight who sent it, and is spent once used. Hands persist at five cards, so what
you spent last round is what you are missing this round.

Marla the tavern keeper coaches from the side of the screen, and a herald calls the
tilt. The festival score is synthesised live — no samples — and the arms have a knight
foley of their own.

{% include figure.liquid
   path="assets/img/robo-jousting/screencap_04_planning_voltage.webp"
   alt="The planning phase, showing three move slots and a voltage meter"
   caption="Planning: three moves, chosen in secret, with voltage loaded from feints."
   zoomable=true
%}

{% include figure.liquid
   path="assets/img/robo-jousting/screencap_06_counter_hover_preview.webp"
   alt="Hovering the Counter card shows a preview of what it would do"
   caption="Counter throws a blow back at whoever sent it, and is spent once used."
   zoomable=true
%}

{% include figure.liquid
   path="assets/img/robo-jousting/screencap_05_exchange_fx.webp"
   alt="The exchange resolving on screen with impact effects"
   caption="The exchange resolves."
   zoomable=true
%}

{% include figure.liquid
   path="assets/img/robo-jousting/screencap_03_versus_poses.webp"
   alt="The two knights in their versus poses before a bout"
   caption="Versus."
   zoomable=true
%}

## The robots

Every move was designed in MuJoCo, then tuned on the real arms, and the moves are
chained together by a transition library so one motion can run into the next. The game
waits on the real motions — the screen does not resolve an exchange until the arms have
actually fought it.

### The real arms

The arms fenced for real. Three exchanges were filmed, and they are in the trailer: an
overhead chop stopped by the high bar, an overhead chop landing against a low guard,
and a low slash from the left stopped by the right-hand guard.

{% include figure.liquid
   path="assets/img/robo-jousting/real_robot_exchange_blockhigh.webp"
   alt="Two real robot arms mid-exchange: an overhead chop caught on the high bar"
   caption="An overhead chop, stopped by the high bar."
   zoomable=true
%}

{% include figure.liquid
   path="assets/img/robo-jousting/real_robot_exchange_blockmid.webp"
   alt="Two real robot arms mid-exchange: an overhead chop coming down against a low guard"
   caption="An overhead chop, landing against a low guard."
   zoomable=true
%}

<div class="row justify-content-sm-center" style="margin-bottom: 1.5rem">
  <div class="col-sm-6 mt-3 mt-md-0">
    {% include figure.liquid
       path="assets/img/robo-jousting/real_robot_exchange_attackleft_blockright.webp"
       alt="Two real robot arms: a low slash from the left stopped by the right-hand guard"
       caption="A low slash from the left, stopped by the right-hand guard."
       zoomable=true
    %}
  </div>
  <div class="col-sm-6 mt-3 mt-md-0">
    {% include figure.liquid
       path="assets/img/robo-jousting/sim_attackleft_blockright.webp"
       alt="The same low slash and right-hand guard, rendered in MuJoCo simulation"
       caption="The same exchange designed in MuJoCo, blades meeting 3 mm from the guard."
       zoomable=true
    %}
  </div>
</div>

### Calibration, by hand

The arms' servo calibrations live in the repo, in `calib/`. We calibrated the SO-100 by
holding it at the zero pose and sweeping every joint to its stops, then checked the zero
points against physical references — the arm leaning fully back on its board, the
upright square pose, the blade sitting on top of the gripper — before we trusted the
taught moves on the real arm.

{% include figure.liquid
   path="assets/img/robo-jousting/real_robot_bts_calibration.webp"
   alt="Behind the scenes: a hand holding the arm at a reference pose during calibration"
   caption="Calibration, by hand."
   zoomable=true
%}

### Driving the arms live

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

<div class="row justify-content-sm-center" style="margin-bottom: 1.5rem">
  <div class="col-sm-6 mt-3 mt-md-0">
    <figure>
      <video autoplay loop muted playsinline preload="metadata" width="100%" style="width:100%;height:auto;border-radius:4px"
             poster="{{ '/assets/img/robo-jousting/en_garde_opener_poster.webp' | relative_url }}">
        <source src="{{ '/assets/img/robo-jousting/en_garde_opener.mp4' | relative_url }}" type="video/mp4">
      </video>
      <figcaption class="caption">En garde opener.</figcaption>
    </figure>
  </div>
  <div class="col-sm-6 mt-3 mt-md-0">
    <figure>
      <video autoplay loop muted playsinline preload="metadata" width="100%" style="width:100%;height:auto;border-radius:4px"
             poster="{{ '/assets/img/robo-jousting/samurai_finish_poster.webp' | relative_url }}">
        <source src="{{ '/assets/img/robo-jousting/samurai_finish.mp4' | relative_url }}" type="video/mp4">
      </video>
      <figcaption class="caption">Samurai finish — the winner rains blows while the loser collapses.</figcaption>
    </figure>
  </div>
</div>

{% include figure.liquid
   path="assets/img/robo-jousting/sim_clash_impact.webp"
   alt="Two swords meeting at the moment of impact in simulation"
   caption="The moment two blades meet."
   zoomable=true
%}

{% include figure.liquid
   path="assets/img/robo-jousting/sim_pipeline_still.webp"
   alt="The move pipeline from MuJoCo simulation through to the real arms"
   caption="From MuJoCo to the arms."
   zoomable=true
%}

## The hardware

We printed a fencing gripper for the arms: a sword holder that takes swappable 6 and 8
inch blades in five styles — fang, katana, rapier, falchion and crystal — plus a shield,
a gauntlet and a sword-breaker talon for the wrist.

For the tilt itself we printed a plate with one of each 8 inch blade, plus the gauntlet
and talon wrists.

{% include figure.liquid
   path="assets/img/robo-jousting/full_arm_8in_fang.webp"
   alt="CAD render of a full arm holding an 8 inch fang blade"
   caption="A full arm with the 8 inch fang blade."
   zoomable=true
%}

{% include figure.liquid
   path="assets/img/robo-jousting/cad_blades_turntable.webp"
   alt="Turntable render of the five blade styles: fang, katana, rapier, falchion, crystal"
   caption="Five blades: fang, katana, rapier, falchion, crystal — at 6 and 8 inches."
   zoomable=true
%}

{% include figure.liquid
   path="assets/img/robo-jousting/cad_wrists.webp"
   alt="CAD render of the shield, gauntlet and sword-breaker talon wrists"
   caption="Shield, gauntlet, and the sword-breaker talon."
   zoomable=true
%}

## The Arm Studio

To make all of that, we built our own animation platform. The Arm Studio holds the move
library with its MuJoCo clips; the Theatre, where foley is locked to a clip; the
interactions matrix of every card against every card; and the Playhouse, where two arms
play a scene together.

{% include figure.liquid
   path="assets/img/robo-jousting/09_armstudio.webp"
   alt="The Arm Studio interface with the move library and clip timeline"
   caption="The Arm Studio: move library, Theatre, interactions matrix, Playhouse."
   zoomable=true
%}

## Team and links

Team: [names]

Code: [github.com/avnithv/robot-jousting](https://github.com/avnithv/robot-jousting)
