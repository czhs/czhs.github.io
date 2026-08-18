# Research notebook PDF -> /research blog post


When Chris uploads a notebook PDF (like "IH Engineering Notebook") and asks to post it,
follow this workflow. The first post
(`_research/ih-engineering-notebook-2026-08-15.md` + its payload) is the reference
implementation; commit `fd3181e` shows the final state.

### Invariants (non-negotiable)

1. **Chris's words are byte-exact.** Extract the text layer with
   `pdftotext -layout` — never retype. Preserve curly quotes, punctuation quirks,
   bold, bullet structure, and embedded screenshots (extract with `pdfimages -png`,
   place at their original positions).
2. **Insert only where the text directs it.** Chris marks insertion points with
   parentheses or brackets addressed at Claude — e.g. "(cite number here for me
   please)", "[please insert some of the graphs we made after here]". Notes to
   himself ("Haven't really examined", "I should be careful about this tomorrow")
   are NOT insertion points. A "(fact check me here please)" that checks out is
   simply removed, no insertion (his preference, 2026-08-15). **If any marker is
   ambiguous, ask before proceeding** — he expects the question. One standing
   exception to "only where the text directs it": when he names a paper or an
   author in passing ("It seems like I rediscovered ROME by Bau"), he wants the
   citation even with no marker asking for it — offer it, and verify title and
   author order against the source, never from memory (2026-08-17).
3. **Claude-inserted material must be unmissable**: orange, monospace, grey chip
   background — `.claude-insert` (inline) / `.claude-block` (block) classes, styled
   for both themes (`html[data-theme="dark"]` variants), plus a self-identifying
   legend line at the top of the post in the same style. Copy the style block from
   the reference post's master (see "masters" below).
4. **Show the design locally and get approval BEFORE publishing.**
   `bundle exec jekyll serve --config _config.yml,_config_local.yml`, review at
   `localhost:4000/research/<slug>/`.
5. **Plaintext NEVER touches the public repo — entries publish encrypted.**
   Not in the working tree, not in git history, and not in `_includes`/`assets`
   side files (figure SVGs and screenshots count as content). If plaintext ever
   gets committed, rewrite history before it lingers (that happened once;
   force-push with `--force-with-lease` fixed it within the hour).
6. **Never write the shared password anywhere in this repo** (it would defeat the
   encryption — the repo is public). Ask Chris for it at encrypt time.

### Chris's markup conventions in the notebook PDF

Read these off the PDF *pages* (`Read` the file with `pages:`), not just the text
layer — the text layer loses highlighting, bold/italic, and image placement.

- **Orange/amber highlight = Claude's material.** Everything highlighted in the
  notebook is text Claude produced; render it as `.claude-insert` (inline) or
  `.claude-block` (block). Unhighlighted prose is Chris's, verbatim.
- **Bracketed tags like `[Claude1]` are Chris's OWN cross-references**, not a
  Claude marker — the name is coincidental and it confused this workflow once.
  One site defines the tag (it prefixes the block being labelled), and any number
  of other lines reference it. Mark them up as:
  - definition: `<span class="xref xref-def">[Tag]</span>` on an element carrying
    `id="xref-<tag-lowercased>"`
  - reference: `<a class="xref xref-ref" href="#xref-<tag>">[Tag]</a>`

  `research_styles.liquid` then draws an arc through the field margin from each
  reference to its definition (grows on hover, arrowhead lands last, arc itself
  clickable, minimum scroll to reveal). Narrow screens get no arc — the tag just
  scrolls. **Expect more of these; ask if a tag's target is ambiguous.**

- **A leading `Aug NN description: …` line is the front matter, not body text.**
  Since 2026-08-17 he opens the notebook with e.g. "Aug 17 description: I
  reinvented ROME & pivot". That string becomes the post's `description:` and is
  dropped from the body — do not reproduce it as prose. It stays PUBLIC on the
  /research listing under the title (he confirmed that is what he wants; earlier
  entries used deliberately vague descriptions instead, so ask if a day's line
  looks like something he would not want in the clear).
- **An entry can carry no highlighting at all.** Check before assuming: render
  the pages and scan for non-grey pixels outside the image boxes rather than
  eyeballing it. When nothing is highlighted, the legend line still goes in, worded
  for what is actually there ("text in this style was inserted by Claude (one
  citation) — everything else is verbatim from the notebook").
- **Notes addressed to Claude are not always insertion points.** "*I need to dig
  into this carefully later Claude, remind me!*" is a note to self — leave it
  verbatim. A marker only earns an insertion when it asks for content
  ("cite number here for me please").

### kramdown will rewrite his punctuation

Smart typography turns `--` into an en-dash and straight quotes/apostrophes
curly, silently breaking the byte-exact rule — it mangled `stuff--`, `I've`,
`swarm's` and `top-1 = " February"` on the second entry. Write those spans as
HTML entities (`&#45;&#45;`, `&#39;`, `&quot;`).

**Always diff the rendered body against the PDF text layer before encrypting**
(normalise whitespace, split to words, `difflib.SequenceMatcher`); the target is
zero real differences once list bullets and italic markers are discounted.

### If an entry contains math

MathJax is no longer loaded site-wide (it was costing every page ~1 MB for
nothing). Other pages get it by content sniffing, but that cannot see inside an
encrypted payload — so a research entry with math must set `math: true` in the
**stub's** front matter, not just the plaintext master.

### The pipeline

1. Extract: `pdftotext -layout <pdf> body.txt` and `pdfimages -png <pdf> img`;
   clean zero-width chars from the text.
2. Draft the plaintext post at `_research/<slug>.md` (front matter:
   `layout: research_preview` for the local review build, title, date — never
   future-dated, description, `related_posts: false`), with the
   claude-insert style block, legend line, verbatim body, styled insertions,
   screenshots under `assets/img/research/`, and any generated figures as
   `{% include research/fig_*.svg %}` (figure generators live in the VPD repo:
   `code_pile/site_figs_build.py` pattern — recompute from raw results, never
   hand-type numbers).
3. Serve locally, review with Chris, iterate.
4. Encrypt: with the plaintext post still built in `_site`, run
   `python3 bin/research_lock.py <slug> <password>` — it extracts the rendered
   `<article class="post-content">` body, inlines all local images as data URIs,
   and writes AES-GCM ciphertext to `assets/enc/research-<slug>.json`
   (PBKDF2-SHA256, 300k iterations — same scheme as the poem page).
5. Swap in the locked stub: `_research/<slug>.md` becomes front matter only —
   `layout: research_locked`, title/date/description (these stay public on the
   `/research` listing), `enc_payload: /assets/enc/research-<slug>.json`.
6. Archive the plaintext masters OUTSIDE this repo:
   `/Users/hshi/Desktop/VPD-Copying/docs/research_src/` (post .md, screenshots,
   figure SVGs — see its README for the re-edit loop).
7. Delete plaintext copies from the repo (`git rm` the images/includes), verify in
   the browser that the gate serves zero plaintext and the password decrypts, then
   commit stub + payload and push.

### How the gate works (for debugging)

`_layouts/research_locked.html` renders a password form; WebCrypto derives the key
(PBKDF2 → AES-256-GCM) and injects the decrypted HTML. One shared password covers
all entries: success stores it in `sessionStorage` (`research_pw`), so sibling
entries auto-unlock for the tab session. Wrong password → "not it.". The listing
page `_pages/research.md` (orphan, `nav: false`) auto-lists every `_research` doc —
titles/descriptions/dates are public by design; bodies are not.

### Known pitfalls

- The `research` collection block is in `_config.yml` (ringworld pattern) —
  config changes need a serve restart; everything else hot-reloads.
- `bin/research_lock.py` needs the `cryptography` package (present in the system
  python on Chris's Mac).
- The extraction anchor is `<article class="post-content">` — if the post layout
  ever changes, update the encryptor.
- Titles in the encrypted payload still leak via the public listing/description —
  keep those lines generic if an entry is sensitive.
