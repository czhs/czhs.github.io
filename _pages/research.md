---
layout: page
permalink: /research/
title: research
description: lab notebook — running notes and results from my interpretability research.
nav: false
---

<ul class="post-list" style="list-style:none;padding-left:0">
  {% assign docs = site.research | sort: "date" | reverse %}
  {% for post in docs %}
  <li style="margin-bottom:1.4rem">
    <h3 style="margin-bottom:0.15rem"><a class="post-title" href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    <p style="margin-bottom:0.2rem">{{ post.description }}</p>
    <p class="post-meta" style="font-size:0.85rem;color:var(--global-text-color-light)">{{ post.date | date: "%B %-d, %Y" }}</p>
  </li>
  {% endfor %}
</ul>
