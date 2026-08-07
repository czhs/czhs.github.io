---
# TEMPLATE — `published: false` keeps this out of the built site. To add a real
# post, copy this file to _ringworld/<slug>.md, delete the `published` line, and
# fill in the front matter. The URL comes from the filename: my-sae-viz.md
# becomes /ringworld/my-sae-viz/.
#
# GOTCHA: a post dated in the future is listed in the feed but its page is never
# written, so the card 404s. Jekyll's `future` defaults to false and applies to
# collection docs. Date posts today or earlier.
published: false

title: What I found poking at SAE features
# Who made it. Free text — however they want to be credited.
author: Jane Doe
# Optional link on the author's name: personal site, GitHub, wherever.
author_url: https://example.com
# The day they worked on it. Drives feed ordering. Must not be in the future.
date: 2026-08-30
# Optional: which session it came out of, matching `num` in _data/ringworld.yml.
session: 1
# One or two sentences. Shown on the feed card, and used as the page description.
description: Two hours of staring at feature 4207 and a plot that finally made sense.
# Optional cover, shown on the feed card and above the post. Pick one of the
# watercolours in assets/img/ringworld/posts/ — campus-lawn, craig-street-sunset,
# dish, green-roof, oculus — or add a new image to that folder. These are the
# post illustrations; the kawaii sprites belong to the sessions, not to writeups.
# A post with no cover just gets no thumbnail, which is fine.
cover: /assets/img/ringworld/posts/oculus.jpg
---

Write the post here in markdown. Headings, images, code, links — all normal.

Images live in `assets/img/ringworld/posts/` and go in the usual way:

![alt text](/assets/img/ringworld/posts/dish.jpg)
