---
layout: page
title: webring
permalink: /webring/
description:
nav: true
nav_icon: ring
---

<ul class="webring-list">
  <li><a href="https://isaac9000.github.io/">Isaac Sun</a></li>
  <li><a href="https://andersonchung.com/">Andy Chung</a></li>
  <li><a href="https://etashj.github.io/">Etash Jhanji</a></li>
  <li><a href="http://mmilunicmobile.github.io/">Matthew Milunic</a></li>
  <li><a href="https://srzhang.com/">Stephen Zhang</a></li>
  <li><a href="https://chirprush.github.io/">Rushil Surti</a></li>
  <li><a href="https://kritdass.github.io/">Krit Das</a></li>
  <li><a href="https://snowballsh.com/">Yinuo Huang</a></li>
  <li><a href="https://ghobrady.github.io/">Brady Gho</a></li>
  <li><a href="https://avnithvijayram.com/">Avnith Vijayram</a></li>
</ul>
<p style="font-size: 0.8rem; opacity: 0.45;">order is randomized upon reload</p>

<script>
  (() => {
    const list = document.querySelector('.webring-list');
    const items = Array.from(list.children);
    for (let i = items.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [items[i], items[j]] = [items[j], items[i]];
    }
    list.append(...items);
  })();
</script>
