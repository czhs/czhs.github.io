---
layout: page
permalink: /pokedex/
title: pokedex
nav: true
nav_order: 9
---

*Under construction.*

A collection of tools and harnesses that I find useful, particularly for
autoresearch — collected from across the internet. None of these are mine. Feel free to reach out to me if you have anything to add!

<ul class="tool-list">
  <li class="tool">
    <a class="tool-name" href="https://github.com/ykdojo/safeclaw" target="_blank" rel="noopener">safeclaw</a>
    <p class="tool-blurb">Sandboxing layer for Claude Code — a useful starting point if you're hardening an agent harness against itself.</p>
  </li>
</ul>

<style>
.tool-list {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0 0;
}
.tool-list .tool {
  padding: 1rem 0 1.1rem;
  border-top: 1px solid var(--global-divider-color);
}
.tool-list .tool:last-child {
  border-bottom: 1px solid var(--global-divider-color);
}

.tool-name {
  font-weight: 600;
  font-size: 1.05rem;
  color: var(--global-theme-color);
}
.tool-name:hover {
  color: var(--global-hover-color);
}

.tool-blurb {
  margin: 0.4rem 0 0;
  font-size: 0.93rem;
  color: var(--global-text-color);
  opacity: 0.85;
}
</style>
