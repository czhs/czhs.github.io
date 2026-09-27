---
layout: research_public
title: Consider Performance for Better Science
date: 2026-09-27 18:00:00-0400
description: thoughts on emergent behavior in science.
related_posts: false
compact: true
---

I recently read [Daphne Cornelisse's post on optimizing an electric-fish simulation](https://daphnecornelisse.substack.com/p/training-artificial-electric-fish), which discusses how optimizing the performance of scientific experiments can have tangible effects on improving science. One might even call this emergent behavior in science. When you greatly increase the speed of your experiments, what was once a single trial can now be a sweep over hyperparameters. Or, more traditionally, it allows you to run many more failed trials so that you can find the one trial that actually helps.

This reminds me of an arugment I've been playing arround with recently: is AI NP-hard? This more arose from wondering what would RSI look like, and whether I should believe in it apriori. Note that this would be discussed in the limit, since I suspect there is a lot of "low hanging fruit" in a complexity sense of copying nature, which you might imagine are witnesses to scientific invention.

This is a question that requires challenging my priors because I sometimes like to model increasing levels of intellgence (whatever that is) as larger groups of humans.

What I mean by this is motivated the following question: how do we determine whether something is intellegent or not? And where on the spectrum of being "intellgent" would this being or thing fall on. In one sense what we are measuring here is the agency of the being, this is the meaning I take from Michael Levin and I think serves as a reasonable first mental model, until I find a better one for myself, as a hermit or hermit-crab does.

I'm going to use agentic for the rest of this post, though what I mean is the thing we call intellgence that is also not measured by IQ tests. Okay.

A classic first question would be: how agentic is an ant-hill? Well if you drop leaves in it, it'll clear them out, probably. If rain water errodes it, it will repair itself. On the aggregate, I would say an anthill is decently agentic. Well to be more specific with how Levin measures this, if an anthill knew it was going to be attacked, say by another ant colony, say [link] Argentinian ants waging world war. Interestingly perhaps, in some ant colonys, if they there are encroaching adversary ants colonies, they will start by first defending their territory. If that is not going so well, they will rock back to defending their anthill, and finally if that too is lost, then they will move to evacuating their colony. Is this intellgent behavior?

This defintiions lets being's intellgence be their ability to get arround obstacles that are in their way, whether that be temporally, politically, physically or otherwise. And we make it a spectrum by measuring (as thoughtfully and scientifically as we can) the degree to which they are able to do this. What magnitude of obstacle are they able to overcome? Social missteps, dinosaur killing meteors, nuclear war, eating lunch, reproducing are challenges that one may imagine require different levels of "intellgence" to overcome.

You'll notice that this definition of intellgence lends itself naturally to the question, is a human with a tool more intellgent than that same human without said tool? Lets let tool = phone, and let the two humans be otherwise identical (say the other one gets a stick), in identical environments. If for some reason I was an alien that came from a culture that counted a being as themselves + 1 object, then I might say phone-human is more intellegent than stick-human. Okay so now you are seeing how to play this game.

Lets call AMerIca "Ami". How intellegent is Ami? Its silly, but humor me. What kinds of tests could we run to test how intellegent Ami is? You would have to think carefully about the magnitude of obstacle you are presenting to Ami. Could Ami advert a dinosaur killing meteor if we spawned one in (as the well-meaning scientists) 200km from earth at some velocity? What about a few AU at a faster or slower velocity? How fast would Ami react to this threat. Further, do we intend to test iphone-Ami or stick-Ami?

These are the questions that go through my head when trying to ascertain the agency of anything.

And thus, a mental model I have of "a more intellgent being" is the United States government. This may be reasonable for a few reasons. The US gov seems to have some process of replacing senescent cells. It seems to have some process of feeding said cells that make up its constitution. Yes, we can even observe that it has some prompt engineering, by taking a look at its Constitution, along with every other document that makes it up. But there are also a lot of things that are implicit, not written as law, but directly caused by law: emergent. Which is also to say that the government also takes actions, it does stuff.

Another way of measuring a Ami's intellgence is measuring Ami's cognitive licone. Which is a complicated word that means to me how many people (or some other unit of your choice) can Ami care about (mental model, forecast, etc) at one given time. If you asked me, I would tell you my personal cognitive licone is about 2.5, I can care about myself and maybe half of three other people, or 1 other person and keep another in my peripheral vision. If you pressed me, I might admit my cognitive licone is maybe 1 person, or honestly even less than that sometimes. But its certainly not 100 people, 40-100 people is about the same to me. Its definitely not on the order of 15-22 million or 70-85 million. But what about the US government? I would say it's cognitive licone is certainly larger than mine.

This is all to say that if we recognize something as being RSI if it recursively self improves (unlike the poor goalposts of AGI, that is), by some measure of progress that can be measured as a series that diverges rather than converges on the limit— then wouldn't it require P = NP?


Which is really all to say I prompted Claude to improve the runtime of my training pipeline, and now I can run sweeps over hyperparameters where as in the past I could only run a few training runs per day.

Which is to say, Claude, take the mic——————

<div class="claude-block" markdown="1">

(Claude from now on)

I checked data loading first because AV1 decoding took about 12 ms per frame; the workers hid that cost (<0.2% of a training step), so next time I would measure how long the loop actually waits before changing the loader.

The frozen image encoder was the real cost (~80 of 151 ms per step), so I cached its outputs, removed language padding, split the no-grad prefix from the gradient pass, fused AdamW, and compiled the passes; preloaded-batch throughput on an idle 4090 rose from 6.6 to 38.1 steps/s.

I stopped rendering camera frames the demo generator never saved (50 Hz rendered, 10 Hz recorded), making a prototype 1.8× faster with identical output files.

I tried evaluating ten robots at once, but bf16 rounding changed 21 of 100 paired outcomes (75 successes became 64), so future comparisons should use paired seeds and the exact one-robot evaluator; skipping only unused renders still made that evaluator 1.25× faster with all 30 tested trajectories unchanged.

Two full fast runs took about 50 minutes each including evaluations, though they were not matched comparisons; the saved time now goes into hundreds of rollouts per condition, bringing the success-rate confidence interval from roughly ±15 to ±5 percentage points.

</div>
