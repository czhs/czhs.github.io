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
  <figcaption class="rbx-shot-cap">The CAD assembly. Two servos per leg sit inside the body, the Raspberry Pi and the RPLIDAR A1 ride on the top plate.</figcaption>
</figure>

A printed quadruped. All structural parts are self-designed and 3D printed. Each
leg is driven by two servos mounted in the body, through pushrod linkages, from a
PCA9685 servo controller on a Raspberry Pi. On the bench it stands and runs an
authored dance routine on all four legs, powered over a tether.

The sensing is designed but not brought up. The RPLIDAR A1 on the top plate and
the RealSense depth camera behind the front panel are in the CAD, with mounting
and power budgeted. Nothing autonomous ran.

## CAD

Every part was modelled before printing: body shells, top plate, leg links, servo
pockets, standoffs for the lidar. The model carries the real constraints: servo
mounting geometry, link lengths, and wiring paths.

No servo is mounted on a leg. Both actuators for each leg sit in the body and
drive the lower link through a pushrod, so what swings is printed plastic and
bearings. Moment of inertia scales with the square of distance from the joint, so
a servo at the knee costs several times what the same mass costs at the hip.
Hobby servos have a fixed torque budget, and leg inertia sets how fast a leg can
move before it stops tracking its commands.

The tradeoff is an indirect drive. Joint angle is a nonlinear function of servo
angle, set by the linkage geometry, and the mapping has to be computed from the
CAD and applied in software. Each pin joint adds slop, and slop at the hip is
multiplied by leg length at the foot.

## Prototyping

One leg was built and tested before the other three: a single leg bolted to a
vertical extrusion on a plywood stand, driven from a breadboard with a dev board
and a bench power module.

On the rig a leg is one degree of freedom with the frame holding everything else
still, so a failure has one cause. On an assembled robot, a linkage that binds
and a servo that browns out look the same from the outside.

The rig answered three questions: whether the linkage moves through its full
range without self-interference, whether the printed pin joints survive repeated
load, and what the servo delivers against the real leg rather than the datasheet.

## Servo controllers

The servos run off a PCA9685, a 16-channel PWM controller on the I2C bus.

Hardware PWM matters for servos. A hobby servo reads position from pulse width,
about 1000 to 2000 microseconds in a 20 millisecond frame, so a 10 microsecond
error is about one degree. The Pi has few hardware PWM channels, and software PWM
on Linux jitters with the scheduler. A servo fed jittery pulses buzzes and runs
hot. The PCA9685 generates every channel in hardware from its own oscillator, so
pulse widths hold regardless of what the Pi is doing.

Effective resolution: the counter is 12-bit across the frame. At 50 Hz one count
is about 4.9 microseconds, and the 1000 microsecond servo band spans about 205
counts, just under one degree per count over 180 degrees of travel. Enough for
gaits, but not the 4096 steps the datasheet implies.

Two more constraints. The prescaler is shared, so all 16 channels run at one
frame rate. And the chain is open loop: the board reports its last command, the
servo reports nothing, and the robot's estimate of its own pose is the last
command sent.

## Power delivery

Power is split into two rails from one LiPo pack.

The servo rail is high current and spiky. A loaded servo draws several times its
idle current, a stalled one draws stall current, and every leg can load the rail
on the same beat of a gait. A buck converter sized for that load steps the pack
down to the servo rail.

The logic rail has to stay clean. A Raspberry Pi that dips below its undervoltage
threshold resets and takes the robot down with it. The Pi is fed separately from
the servo rail, and the two rails share a ground so the PCA9685's logic side and
the servos agree on zero volts.

Bench testing ran off a current-limited supply instead of the pack. The current
readout shows the standing draw, the cost of a pose transition, and the spike
when a leg hits a limit. The current limit also acts as a fuse: a stalled servo
stops moving instead of burning.

## Robot animation

The dance is authored motion: a sequence of poses with interpolation between
them, not a learned or planned gait.

Every joint takes a position command and nothing else. No velocity, no torque, no
feedback. The motion is defined entirely by the pose list and the timing between
poses.

Three limits constrain the authoring:

- **Slew rate.** A servo has a maximum speed. Commanding a large angle in a short
  time gets a leg that arrives late and out of phase with the others.
- **Ground contact.** A quadruped on the floor is a closed kinematic chain. Feet
  in contact cannot move independently of the body, and motion that ignores this
  makes the servos fight the ground.
- **Loop closure.** A looping routine has to end on its first pose in every
  joint, or the seam shows on every repeat.

The MuJoCo renders on the Open Duck Mini page are the same problem in simulation.

## Depth camera and 2D lidar

The design carries two sensors, both in CAD only: an RPLIDAR A1 on the top plate
and a RealSense depth camera behind the front panel.

The lidar measures range in one horizontal plane through 360 degrees. It sits on
standoffs above the top plate because anything in its plane blocks it
permanently, and on a quadruped that would be the body and the legs. Raised
clear, it returns walls in every direction, in the dark, at ranges a camera does
not match. That is the measurement 2D localisation and mapping want.

A single slice at body height cannot see a step, a gap, or a cable on the floor,
and those decide where a foot can go. The depth camera covers that: stereo depth
returns a dense surface in front of the robot, which is the measurement foot
placement needs. The costs are a narrow field of view, range in metres rather
than tens of metres, USB 3 bandwidth, a real share of the 5 volt budget, and poor
returns on untextured surfaces.

Both sensors mount to a body that pitches and rolls with every step. A depth
frame is only useful in world coordinates together with the body's attitude at
capture time, so a camera on a walking robot requires state estimation as well.

## What I learned

- **CAD to hardware.** Designing every structural part around servo geometry and
  wiring paths, printing it, and correcting the model where it was wrong.
- **Designing for inertia.** Actuators in the body, legs driven through linkages,
  and the nonlinear joint mapping and pin slop that come with that choice.
- **Prototyping one unknown at a time.** A single leg on a rig before four on a
  body that can fall over.
- **Servo control.** Hardware PWM over I2C instead of software PWM, the real
  resolution arithmetic, and what open loop means for knowing the robot's pose.
- **Power delivery.** Separate servo and logic rails, buck converter sizing
  against stall current, a shared ground, and a current-limited supply used as
  both instrument and fuse.
- **Robot animation.** Authoring pose sequences under slew limits, ground contact
  constraints, and loop closure.
- **Sensor selection.** What a 2D lidar measures and what it cannot, why a depth
  camera covers the gap, and what a moving mount costs both.
