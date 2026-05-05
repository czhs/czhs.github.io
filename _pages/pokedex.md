---
layout: page
permalink: /pokedex/
title: pokedex
nav: true
nav_order: 9
---

Welcome to my pokedex!

<div class="row justify-content-sm-center">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/pokdex/catchem.webp" title="catchem" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    I'm going to be the best <del>pokemon</del> AI trainer!
</div>

<div class="row justify-content-sm-center">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/pokdex/fat_pikachu.png" title="fat pikachu" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Fat pikachu. He jamakes me crazy.
</div>

<style>
@keyframes pika-spin     { to { transform: rotate(360deg); } }
@keyframes pika-spin-rev { to { transform: rotate(-360deg); } }

.pika-jam {
  position: relative;
  height: 520px;
  margin: 2rem 0;
  padding: 0;
  border-radius: 12px;
  background: linear-gradient(135deg, #009b3a 0%, #fedd00 50%, #ce1126 100%);
  overflow: hidden;
}
.pika-jam .pika {
  position: absolute;
  width: 80px;
  height: 80px;
  will-change: transform;
}
.pika-jam .pika img {
  width: 100%;
  height: 100%;
  animation: pika-spin 2.4s linear infinite;
  filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3));
}
.pika-jam .pika:nth-child(2n) img { animation: pika-spin-rev 1.7s linear infinite; }
.pika-jam .pika:nth-child(3n) img { animation: pika-spin 3.3s linear infinite; }
.pika-jam .pika:nth-child(5n) img { animation: pika-spin-rev 1.1s linear infinite; }
.pika-jam .pika:nth-child(7n) img { animation: pika-spin 4.5s linear infinite; }

#reggae-toggle {
  display: inline-block;
  font-size: 1.1rem;
  padding: 0.6rem 1.4rem;
  background: linear-gradient(90deg, #009b3a, #fedd00, #ce1126);
  border: 2px solid #000;
  border-radius: 8px;
  color: #000;
  font-weight: 700;
  letter-spacing: 0.5px;
  cursor: pointer;
  margin: 1rem 0;
  box-shadow: 0 3px 0 #000;
}
#reggae-toggle:active { transform: translateY(2px); box-shadow: 0 1px 0 #000; }
</style>

<button id="reggae-toggle" type="button">▶ start the jam</button>

<div class="pika-jam" id="pika-jam">
{% for i in (1..36) %}<span class="pika"><img src="{{ '/assets/img/pokdex/fat_pikachu.png' | relative_url }}" alt="spinning fat pikachu" loading="lazy"></span>{% endfor %}
</div>

<script>
(() => {
  const jam = document.getElementById('pika-jam');
  if (!jam) return;
  const pikas = [...jam.querySelectorAll('.pika')];
  const state = pikas.map(() => ({ x: 0, y: 0 }));
  const SIZE = 80;

  function place() {
    const w = jam.clientWidth, h = jam.clientHeight;
    pikas.forEach((el, i) => {
      el.style.left = Math.random() * (w - SIZE) + 'px';
      el.style.top  = Math.random() * (h - SIZE) + 'px';
      state[i].x = 0; state[i].y = 0;
    });
  }
  place();
  window.addEventListener('resize', place);

  // Lévy flight: step length ~ Pareto (heavy tail), direction uniform.
  // Most frames small jitters; rare frames huge leaps.
  const ALPHA = 1.5, SCALE = 0.6, MAX_STEP = 80, BOUND = 240;
  function step() {
    pikas.forEach((el, i) => {
      const s = state[i];
      const u = Math.random() || 1e-9;
      let L = SCALE * Math.pow(u, -1 / ALPHA);
      if (L > MAX_STEP) L = MAX_STEP;
      const theta = Math.random() * Math.PI * 2;
      s.x += L * Math.cos(theta);
      s.y += L * Math.sin(theta);
      // soft bound: nudge back toward origin if drifted too far
      if (s.x >  BOUND) s.x -= (s.x - BOUND) * 0.08;
      if (s.x < -BOUND) s.x -= (s.x + BOUND) * 0.08;
      if (s.y >  BOUND) s.y -= (s.y - BOUND) * 0.08;
      if (s.y < -BOUND) s.y -= (s.y + BOUND) * 0.08;
      el.style.transform = `translate(${s.x}px, ${s.y}px)`;
    });
    requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
})();
</script>

<script>
(() => {
  const btn = document.getElementById('reggae-toggle');
  let ctx, master, timer, beat = 0, playing = false;
  const BPM = 75;
  const eighthMs = 60000 / BPM / 2;
  const eighthSec = eighthMs / 1000;

  // Cm-key reggae jam
  const bassPattern = [55.00, 55.00, 65.41, 73.42, 55.00, 65.41, 49.00, 73.42];
  const chord = [196.00, 233.08, 293.66]; // Cm: G3 Bb3 D4
  // Pentatonic melody over 2 measures (16 eighths). 0 = rest.
  const melody = [
    523.25, 0, 622.25, 0,    698.46, 0, 622.25, 0,
    523.25, 466.16, 392.00, 0,    466.16, 0, 0, 0,
  ];
  // Slam poem — each line gets its own pitch/rate for performance feel.
  const poem = [
    { text: "Listen.",                                     pitch: 1.0,  rate: 0.65 },
    { text: "Nineteen ninety-six.",                        pitch: 1.1,  rate: 0.85 },
    { text: "He came chubby. He came confident.",          pitch: 1.05, rate: 0.9  },
    { text: "And the world said... too much.",             pitch: 0.85, rate: 0.7  },
    { text: "So they made him lean.",                      pitch: 0.9,  rate: 0.85 },
    { text: "They made him lithe.",                        pitch: 0.9,  rate: 0.85 },
    { text: "But me?",                                     pitch: 1.2,  rate: 0.8  },
    { text: "I'm here for the round one.",                 pitch: 1.1,  rate: 0.85 },
    { text: "Big body. Big voltage. Big mood.",            pitch: 1.05, rate: 0.85 },
    { text: "Stay fat, Pikachu.",                          pitch: 0.95, rate: 0.7  },
    { text: "Stay. Fat.",                                  pitch: 0.85, rate: 0.55 },
  ];
  let poemIdx = 0, poemTimer = null, chosenVoice = null;

  function pickVoice() {
    if (!('speechSynthesis' in window)) return;
    const voices = speechSynthesis.getVoices();
    if (!voices.length) return;
    const preferred = ['Daniel', 'Samantha', 'Karen', 'Moira', 'Tessa',
                       'Rishi', 'Google UK English Male', 'Google US English'];
    for (const name of preferred) {
      const v = voices.find(v => v.name.includes(name));
      if (v) { chosenVoice = v; return; }
    }
    chosenVoice = voices.find(v => v.lang && v.lang.startsWith('en')) || voices[0];
  }
  if ('speechSynthesis' in window) {
    pickVoice();
    speechSynthesis.addEventListener('voiceschanged', pickVoice);
  }

  function envNote(freq, t, dur, type, peak) {
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.type = type;
    o.frequency.value = freq;
    g.gain.setValueAtTime(0, t);
    g.gain.linearRampToValueAtTime(peak, t + 0.005);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g).connect(master);
    o.start(t);
    o.stop(t + dur + 0.05);
  }

  function kick(t) {
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.frequency.setValueAtTime(140, t);
    o.frequency.exponentialRampToValueAtTime(38, t + 0.12);
    g.gain.setValueAtTime(0.6, t);
    g.gain.exponentialRampToValueAtTime(0.001, t + 0.25);
    o.connect(g).connect(master);
    o.start(t);
    o.stop(t + 0.3);
  }

  function hat(t) {
    const buf = ctx.createBuffer(1, ctx.sampleRate * 0.05, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / d.length);
    const s = ctx.createBufferSource();
    const g = ctx.createGain();
    const f = ctx.createBiquadFilter();
    f.type = 'highpass'; f.frequency.value = 7000;
    g.gain.value = 0.08;
    s.buffer = buf;
    s.connect(f).connect(g).connect(master);
    s.start(t);
  }

  function snare(t) {
    // bandpass-filtered noise for that "tsk" backbeat
    const buf = ctx.createBuffer(1, ctx.sampleRate * 0.18, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++) {
      d[i] = (Math.random() * 2 - 1) * Math.exp(-i / (ctx.sampleRate * 0.05));
    }
    const s = ctx.createBufferSource();
    const f = ctx.createBiquadFilter();
    f.type = 'bandpass'; f.frequency.value = 1800; f.Q.value = 0.6;
    const g = ctx.createGain();
    g.gain.value = 0.18;
    s.buffer = buf;
    s.connect(f).connect(g).connect(master);
    s.start(t);
  }

  function pad(t, dur) {
    // detuned sine "organ" pad sustained across the measure
    chord.forEach(f => {
      const o1 = ctx.createOscillator();
      const o2 = ctx.createOscillator();
      o1.type = 'sine'; o2.type = 'triangle';
      o1.frequency.value = f;
      o2.frequency.value = f * 1.006;
      const g = ctx.createGain();
      g.gain.setValueAtTime(0, t);
      g.gain.linearRampToValueAtTime(0.035, t + 0.4);
      g.gain.setValueAtTime(0.035, t + dur - 0.5);
      g.gain.linearRampToValueAtTime(0, t + dur);
      o1.connect(g); o2.connect(g);
      g.connect(master);
      o1.start(t); o2.start(t);
      o1.stop(t + dur + 0.05); o2.stop(t + dur + 0.05);
    });
  }

  function lead(freq, t, dur) {
    if (!freq) return;
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.type = 'triangle';
    o.frequency.value = freq;
    g.gain.setValueAtTime(0, t);
    g.gain.linearRampToValueAtTime(0.08, t + 0.01);
    g.gain.exponentialRampToValueAtTime(0.001, t + dur);
    o.connect(g).connect(master);
    o.start(t);
    o.stop(t + dur + 0.05);
  }

  function speakNextLine() {
    if (!playing || !('speechSynthesis' in window)) return;
    const line = poem[poemIdx % poem.length];
    const u = new SpeechSynthesisUtterance(line.text);
    u.pitch = line.pitch;
    u.rate  = line.rate;
    u.volume = 0.95;
    if (chosenVoice) u.voice = chosenVoice;
    // duck the music while a line speaks
    u.onstart = () => {
      if (master) master.gain.setTargetAtTime(0.10, ctx.currentTime, 0.08);
    };
    u.onend = () => {
      if (master) master.gain.setTargetAtTime(0.28, ctx.currentTime, 0.15);
      if (!playing) return;
      poemIdx++;
      // breath between lines — longer pause at the end of the poem
      const gap = (poemIdx % poem.length === 0) ? 1400 : 380;
      poemTimer = setTimeout(speakNextLine, gap);
    };
    speechSynthesis.speak(u);
  }

  function tick() {
    const t = ctx.currentTime + 0.04;
    const b = beat % 8;
    const tick16 = beat % 16;

    // bass — every eighth
    envNote(bassPattern[b], t, 0.28, 'sawtooth', 0.22);

    // skank chord stab + hi-hat on offbeats
    if (b % 2 === 1) {
      chord.forEach(f => envNote(f, t, 0.13, 'square', 0.045));
      hat(t);
    }

    // one-drop kick on beat 3
    if (b === 4) kick(t);

    // snare on the backbeat (beats 2 and 4)
    if (b === 2 || b === 6) snare(t);

    // organ pad sustained over each measure (4 beats = 8 eighths)
    if (b === 0) pad(t, eighthSec * 8);

    // pentatonic melody lead, looped over 2 measures
    lead(melody[tick16], t, eighthSec * 0.9);

    beat++;
  }

  btn.addEventListener('click', () => {
    if (!playing) {
      ctx = new (window.AudioContext || window.webkitAudioContext)();
      master = ctx.createGain();
      master.gain.value = 0.28;
      master.connect(ctx.destination);
      beat = 0; poemIdx = 0;
      playing = true;
      tick();
      timer = setInterval(tick, eighthMs);
      // kick off the slam poem after a short intro
      poemTimer = setTimeout(speakNextLine, 1600);
      btn.textContent = '⏸ stop the jam';
    } else {
      playing = false;
      clearInterval(timer);
      clearTimeout(poemTimer);
      if ('speechSynthesis' in window) speechSynthesis.cancel();
      ctx.close();
      btn.textContent = '▶ start the jam';
    }
  });
})();
</script>
