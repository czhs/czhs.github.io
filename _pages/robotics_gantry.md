---
layout: portfolio_post
portfolio: robotics
permalink: /robotics/gantry/
project: gantry
standalone_title: "Hack 100 Gantry — Chris Shi"
nav: false
---

<!-- Media lead. The shared portfolio_post layout now builds its hero from a `run:`
     block, and this project has no run, so the hero clip had nowhere to render.
     This block puts it back at the top of the page. If the layout regains a hero
     stage for run-less projects, delete this and let the data file drive it again;
     the gallery below the write-up is still coming from _data/robotics.yml. -->

{% assign rbxd = site.data[page.portfolio] %}
{% if jekyll.environment == 'production' and rbxd.media_base %}{% assign mb = rbxd.media_base %}{% else %}{% assign mb = '' %}{% endif %}

<figure class="rbx-shot" style="margin: 0 0 2rem">
  <video class="rbx-shot-media" controls autoplay muted loop playsinline preload="metadata" poster="{% include portfolio_src.liquid path='assets/img/robotics/gantry-poster.jpg' base=mb %}">
    <source src="{% include portfolio_src.liquid path='assets/video/robotics/gantry.mp4' base=mb %}" type="video/mp4">
  </video>
  <figcaption class="rbx-shot-cap">The finished machine, 1 May — the steppers are playing Ode to Joy.</figcaption>
</figure>

A three-axis Cartesian gantry, about 1.2 m on a side, standing free on its own legs
over a taped-out floor grid, built to reach any point in that grid, drop a tool head
onto it, pick something up and put it somewhere else.

It was built in a week. 18-100 runs an optional hackathon in the week before spring
finals — build anything you want — and rather than something that fits on a desk we
went after a machine we could not comfortably finish. The single-axis bench test
further down this page is dated 26 April and the assembled gantry running is 1 May.
Everything here happened in the five days between them, off a 19-line bill of
materials totalling $352.50, with no kit and nothing bought pre-assembled. It won
$50, which did not cover the extrusion, and on the last evening we taught the
steppers to play Ode to Joy.

That week is the real design constraint and most of what follows is downstream of
it. A gantry this size is not a hard machine to design if you can buy linear rails
and a motion controller and wait for them to ship. It becomes an interesting one when
every axis has to be made out of extrusion, printed plastic and $15 worth of stepper
drivers on a breadboard, and be moving by Friday.

## The steppers play Ode to Joy

That is what the clip above is: the machine playing the melody, with no speaker
anywhere on it. A stepper is a loudspeaker if you drive its step pin at an audio
frequency — pitch is step rate, so a note is a delay and a tune is a table of them,
and the windings you were using to move an axis are the thing making the sound.

It is a party trick, and it is also the clearest possible proof that step generation
timing is under control to the microsecond — which is the same property that makes
two axes arrive at a corner together.

## The frame

Everything structural is 2020 V-slot aluminium extrusion: eight 1220 mm lengths and
four 400 mm. Four of the long pieces make the square deck, one becomes the moving
gantry beam, and the rest come down as legs, with the short pieces flat on the floor
as feet so the machine stands on its own instead of being clamped to a table.

V-slot rather than box tube or plate is the load-bearing decision in the whole
design. The slot is both the structure and the bearing surface, so a linear axis
costs three wheels and a plate instead of a rail and block set that would have eaten
the entire budget. Carriages ride on V-wheels — thirteen of them, three per carriage
plus spares. One wheel on each plate sits on an eccentric spacer: rotate it and the
wheel is driven into the opposite slot wall until the plate has no rock left and
still rolls freely. That eccentric is the only thing standing between a carriage that
is sloppy and one that binds, and on a machine this long it gets re-set by hand every
time the frame is squared.

Nothing is drilled or welded. A 100-piece T-nut and bolt kit holds the whole frame
together, which means every joint slides — the frame gets squared _after_ it is
assembled, not by being right the first time. On a 1.2 m span built in a room with a
concrete floor, that is the difference between a machine and a pile of extrusion.

## X and Y

The gantry beam carries a NEMA 17 on a bracket at one end and an idler pulley at the
other, with a GT2 timing belt spanning the beam and the tool carriage clamped to it.
The idler sits on a flat arm bolted through a slot, so belt tension is a screw
adjustment rather than a rebuild — visible in the second CAD view, at the far end
from the motor.

The numbers fall out of the belt. GT2 is a 2 mm tooth pitch; on a 20-tooth pulley the
carriage moves 40 mm per motor revolution. A 1.8° stepper is 200 full steps per
revolution, so a full step is 0.2 mm, and the DRV8825's 1/32 microstepping puts the
nominal resolution at about 6 µm.

That number is honest arithmetic and dishonest engineering, and knowing the
difference was most of what this axis taught me. Microstep torque falls off steeply
past 1/8, and on a belt drive the real repeatability is set by belt stretch, wheel
preload and how square the frame is — not by the driver. Microstepping bought
smoothness and quiet, and the accuracy came from tension and squaring.

## Z, and why it is a rack and pinion

The Z axis is a printed gear rack driven by a printed pinion on a fourth NEMA 17,
with the motor bolted to the carriage through two vertical slots. Sliding the motor
in those slots sets how deep the pinion sits in the rack, which is a direct trade
between backlash and binding — too shallow and the head has play, too deep and the
axis stalls at the top of its travel.

A leadscrew would have been more precise and was the wrong choice. Over this much
travel a screw whips at speed and forces slow feeds, and the head only has to be
repeatable at two heights — clear, and down on the target — not everywhere in
between. Rack and pinion gave a fast Z out of two printed parts and a motor.

The cost is that it does not self-lock. Nothing holds the head up but motor current,
so cutting power drops the tool head. That is a design consequence you have to accept
deliberately and then handle in firmware.

## The tool head

Three DS3225 digital servos — 25 kg·cm, metal gear — do the close work: one rotates
the wrist, the others drive the claw. Two electromagnets sit at the pick point.

Splitting capture from holding is the idea worth defending. An electromagnet needs no
closing force and almost no alignment: it grabs a ferrous target that is roughly
under it, which is exactly the tolerance a dead-reckoned gantry can promise. The claw
then orients and secures what the magnet caught. Release is instant and
deterministic, with none of the "did the gripper actually open" ambiguity — at the
price of only working on ferrous parts, and of residual magnetism you have to plan
around rather than hope away.

## Electronics

Everything runs off an Arduino-class microcontroller and a row of DRV8825 StepSticks
on a single full-size breadboard, mounted to a printed bracket clamped to the frame
so the whole control stack travels with the machine.

The bill has five steppers and five drivers for three driven axes. On a one-week
clock that is not over-ordering, it is the whole risk plan: a driver that lets go on
day four with nothing open and no time to reorder ends the project, and a spare
costs $3.

Current limiting is per-driver, set with the trimpot on each StepStick. The DRV8825
sets its chopping current from the reference voltage — with the usual 0.1 Ω sense
resistors, a 2 A motor wants about 1.0 V — and with bare drivers and no airflow you
set it well under that and give up torque you were not going to use. Getting that
one turn of a trimpot right is the difference between a warm driver and a thermal
shutdown mid-move.

The rest of the electrical work is the part that does not photograph well and decides
whether the machine finishes:

- **Twenty lever microswitches**, for homing and hard limits at both ends of every
  axis. With open-loop steppers and no encoders, the switch _is_ the position
  reference — you home once and everything after that is dead reckoning off the step
  count, which is also why a missed step is silent and cumulative.
- **DIP sockets**, thirty-four of them, so a dead chip comes out with fingers instead
  of a soldering iron.
- **JST-XH extension leads** on every motor, so the cable running out to the moving
  beam is connectorised. A snagged cable then unplugs instead of tearing the leads
  out of a motor.
- **60 ft of 18 AWG** for motor power, kept off the jumper wire entirely — three
  motors at up to 2 A each is not a breadboard rail's job.
- **50 ft of braided sleeving** and a ferrite on the supply lead. The cable run flexes
  on every single move of the machine, and on a gantry that is the thing that
  eventually fails.
- **Per-channel indicator LEDs** and hand-written flag labels taped to every wire in
  the loom, which is what made a breadboard that dense debuggable at all.

## Bringing it up

The limit switch clip is one rail on a bench — a single carriage, one motor, one
switch — and it is dated five days before the machine ran. That order was the whole
method, and on a week-long build it was the only affordable one. Every unknown in the
machine — does the carriage bind, does the belt slip under acceleration, does the
switch trigger repeatably at speed, does the driver stay cool — got paid for one at a
time on a bench, so that assembling the full gantry was assembly and not discovery.
There was no schedule in which to debug three axes at once for the first time.

## What I took from it

- **Designing to a bill of materials.** Every dimension in this machine is a
  consequence of 1220 mm stock, a 100-piece hardware kit and $352.50. Choosing V-slot
  so the structure doubles as the bearing, and rack-and-pinion so Z is two printed
  parts, are budget decisions before they are mechanical ones.
- **CAD through to a machine that exists.** Modelling the frame, the carriage plates,
  the rack, the pinion and the tool head, then printing and assembling them and
  finding out where the model was optimistic.
- **Open-loop motion control end to end.** Step/direction generation, microstepping
  and where its resolution stops being real, acceleration limits, homing to a switch,
  and living with dead reckoning.
- **Motor drive electronics.** Sizing and current-limiting stepper drivers, thermal
  derating, keeping motor power and logic apart, and reading a datasheet for a number
  you have to set by hand.
- **Cable management as a design problem, not cleanup.** Sleeving, strain relief,
  connectorised motor leads and a labelled loom on a machine where every wire moves.
- **Isolating unknowns.** Bench-testing a single axis until it is boring before
  scaling it up, so that assembly is assembly and not debugging.
- **Owning procurement under a hard deadline.** Nineteen line items and 211 parts
  sourced to a budget in a week where a wrong order could not be corrected, with
  spares held on exactly the components most likely to die.
