---
layout: portfolio_post
portfolio: robotics
permalink: /robotics/robot-dog/
project: robot-dog
standalone_title: "Robot Dog — Chris Shi"
nav: false
---

<!-- Media lead. The shared portfolio_post layout builds its hero from a `run:`
     block and this project has no run, so the hero clip has nowhere to render.
     Same fix as the gantry page: this block puts it back at the top. The gallery
     below the write-up still comes from _data/robotics.yml. -->

{% assign rbxd = site.data[page.portfolio] %}
{% if jekyll.environment == 'production' and rbxd.media_base %}{% assign mb = rbxd.media_base %}{% else %}{% assign mb = '' %}{% endif %}

<figure class="rbx-shot" style="margin: 0 0 2rem">
  <video class="rbx-shot-media" controls autoplay muted loop playsinline preload="metadata" poster="{% include portfolio_src.liquid path='assets/img/robotics/robot-dog-poster.jpg' base=mb %}">
    <source src="{% include portfolio_src.liquid path='assets/video/robotics/robot-dog.mp4' base=mb %}" type="video/mp4">
  </video>
  <figcaption class="rbx-shot-cap">The CAD assembly. The leg servos sit inside the body, and the Raspberry Pi and the RPLIDAR A1 ride on the top plate.</figcaption>
</figure>

A printed quadruped. Every structural part is self-designed and printed, the legs are
linkage-driven off servos held in the body, and a PCA9685 on the Pi's I2C bus drives
them. It got as far as standing on the bench and dancing on all four legs, on a
tether.

The sensing is designed and not brought up. The RPLIDAR A1 on the top plate and the
RealSense depth camera behind the front panel are in the CAD and in the power and
mounting budget; nothing autonomous ran. That split is worth stating up front,
because most of what this build taught me sits on either side of it: the mechanical
and electrical half is finished hardware, and the perception half is a set of
decisions made before parts get bought.

## CAD, and where the mass goes

The whole machine was modelled before anything was printed: body shells, top plate,
leg links, servo pockets, standoffs for the lidar. Printing is what makes that
worthwhile. A printed part is nearly free to redesign and expensive to redesign
badly, so the model has to carry the real constraints, which on this robot means
servo mounting geometry, link lengths and where the wiring runs.

The load-bearing decision is that no servo lives on the leg. Both actuators for a leg
sit in the body, and the lower link is driven through a pushrod, so what swings is
printed plastic and a couple of bearings.

That is a decision about inertia rather than packaging. A leg is a lever swung at the
hip, and the moment of inertia of anything on it scales with the square of its
distance from the joint, so a servo hung at the knee costs several times what the
same mass costs at the hip. On position-controlled hobby servos, which
have a fixed torque budget and no way to be told about the load, that difference
shows up directly as how fast a leg can be commanded to move before it stops tracking.

The cost is that a pushrod linkage is not a direct drive. Joint angle is no longer
proportional to servo angle, it is whatever the linkage geometry makes it, and the
mapping has to be worked out from the CAD and applied in software. The linkage also
adds slop at every pin, and slop at the hip is multiplied by the length of the leg by
the time it reaches the foot.

## One leg before four

The single leg test came first: one leg, one servo, bolted to a vertical extrusion on
a plywood stand, driven from a breadboard with a dev board and a bench power module.

Doing it that way was the right call for the same reason it always is. On the bench a
leg is one degree of freedom with the frame holding everything else still, so
anything that goes wrong has one cause. Once four legs are on a body that can fall
over, a leg that binds at the top of its stroke and a leg whose servo is browning out
look identical from the outside.

What that rig answered before four of them existed: whether the linkage moved through
its full range without hitting itself, whether the printed pin joints held under
repeated load, and what the servo could actually do against the weight of the leg
rather than against the datasheet.

## Servo controllers

The servos run off a PCA9685, a 16-channel PWM generator on the I2C bus, which covers
the leg channels with room left over.

The reason to use one instead of driving pins from the Pi is timing. A hobby servo
reads position from pulse width, roughly 1000 to 2000 microseconds inside a 20
millisecond frame, so a 10 microsecond error is about one degree of commanded
position. The Pi has very few hardware PWM channels, and anything generated in
software on a Linux box is at the mercy of the scheduler. A servo fed jittery pulses
jitters, buzzes, and heats up holding a position that keeps moving underneath it. The
PCA9685 has its own oscillator and its own PWM hardware on every channel, so the
pulse widths hold whatever they were last set to and the Pi is free to be late.

The arithmetic is worth knowing before trusting the resolution. The counter is 12 bit
across the whole frame, so at a 50 Hz frame rate one count is about 4.9 microseconds,
and the 1000 microsecond band a servo actually uses is only about 205 counts wide.
For 180 degrees of travel that is a little under one degree per count. It is plenty
for walking gaits and it is not the 4096 steps the datasheet number suggests, and the
difference is the sort of thing that is much cheaper to notice in arithmetic than in
a motion that will not smooth out.

Two other properties of the part shape the design. The prescaler is shared, so all
sixteen channels run at one frame rate and there is no mixing servos that want
different ones. And there is no feedback anywhere in this chain: the board reports
what it was told to output, the servo reports nothing at all, and the robot's idea of
its own pose is entirely the last command it sent.

## Power delivery

Power is two problems that happen to share a battery, and treating it as one is the
mistake.

The servo rail is a high-current, ugly, spiky load. A servo under load draws several
times its idle current, a stalled one draws its full stall current until something
gives, and every leg can reach for it at the same moment on the same beat of a
gait. The logic rail is small and needs to be clean: a Raspberry Pi that dips below
its undervoltage threshold does not degrade, it resets, and it takes the whole robot
down with it.

So the pack feeds a buck converter sized for the servo rail, the Pi is fed
separately, and the two share a ground so the PCA9685's logic side and the servos it
commands agree on what zero volts means. The value of separating them is that the
worst thing the legs can do, which is all pull at once, is contained on the rail that
expects it.

The bench supply in the dance footage is doing more than powering the robot. A supply
with a current readout is an instrument: it shows what the machine draws standing
still, what a pose transition costs, and what it pulls at the moment a leg hits its
limit. A current limit set on the supply is also the cheapest fuse there is, and it
turns a stalled servo from a smoke event into a motion that simply stops.

## Animating it

The dance is authored motion, not a learned or planned gait. That makes it a specific
kind of engineering problem, and the constraints come from what the actuators can
actually accept.

Every joint on this robot takes a position and nothing else. There is no velocity
command, no torque command, and no feedback coming back. So motion has to be written
as a sequence of poses and then as the interpolation between them, and the
interpolation is the part that matters. The pose list is what the robot looks like;
the timing between poses is what it looks like it is doing.

Three limits govern all of it. A servo has a maximum slew rate, and asking it to
cross a large angle in a small time does not produce a fast move, it produces a
command the servo ignores and a leg that arrives late and out of phase with the
others. A quadruped on the ground is a closed chain, so the feet in contact cannot be
moved independently of the body without the floor pushing back, and any authored
motion that forgets this is asking the servos to fight the ground. And a routine that
loops has to close: the last pose has to be the first pose, in every joint, or the
loop shows a seam every time it repeats.

Building expression under those limits is the same problem as the Duck renders, with
the additional constraint that hardware cannot be talked out of physics.

## The lidar and the depth camera

Both sensors were chosen and packaged before anything was mounted, and choosing them
was most of the exercise.

The RPLIDAR A1 is a spinning 2D lidar and it goes on standoffs above the top plate
for a physical reason: it measures one horizontal plane through 360 degrees, so
anything in that plane blocks it permanently. On a quadruped the body and the legs
are exactly what that plane would otherwise be full of. Raised clear, it gives range
to walls all the way around, in the dark, at a rate and accuracy a camera does not
match, which is what localisation in a room wants.

It is also blind to the entire problem a legged robot has. One horizontal slice at
body height says nothing about a step, a gap, a kerb, or a cable on the floor, and
those are precisely the things that decide where a foot can go.

That is what the RealSense is for, facing forward through the front panel. A stereo
depth camera returns a dense surface in front of the robot rather than a single
plane, which is the measurement foot placement needs. It costs a narrow field of
view, a working range measured in metres rather than tens of metres, USB 3 bandwidth
and a real share of the 5 volt budget, and it degrades on blank untextured surfaces
where stereo has nothing to match.

Neither sensor replaces the other, which is why the design carries both. There is a
third cost that the CAD makes obvious and a spec sheet does not: on a legged robot,
both sensors are bolted to a body that pitches and rolls with every step. A depth
frame is only useful in world terms if you know the body's attitude at the instant it
was captured, so mounting a camera on a walking robot commits you to knowing the
robot's own state as well.

## What I learned

- **CAD through to printed, assembled hardware.** Designing every structural part
  around real servo geometry and wiring paths, printing it, and finding out where
  the model was optimistic.
- **Designing for inertia, not just for fit.** Keeping the actuators in the body and
  driving the leg through a linkage, and accepting the nonlinear joint mapping and
  the pin slop that come with it.
- **Prototyping in the order that isolates causes.** One leg on a rig until it was
  boring, so that assembling four was assembly rather than four simultaneous
  unknowns.
- **Getting servo timing off the CPU.** Why an outboard PWM generator on I2C beats
  software PWM on Linux, what the 12 bit counter is actually worth across a servo's
  usable band, and what open loop means for knowing where the robot is.
- **Power delivery as two separate rails.** Sizing a buck converter for stall
  current, keeping logic away from the load that browns it out, sharing a ground on
  purpose, and using a current-limited bench supply as both an instrument and a fuse.
- **Authoring motion for position-controlled actuators.** Poses and interpolation
  under a slew rate limit, a closed kinematic chain against the floor, and loops that
  have to close in every joint.
- **Choosing sensors before mounting them.** What a 2D lidar measures and what it
  structurally cannot, why a depth camera covers the gap, and what a moving mount
  costs both of them.
- **Being clear about what exists.** The mechanics, the drive electronics and the
  motion are built and running; the perception is designed. Saying which is which is
  part of the work.
