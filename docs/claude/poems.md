# /76265/ poem directory — adding a poem from an uploaded PDF or image

When Chris uploads a poem (a PDF, or images for an erasure poem) and asks to put
it up, this is the whole workflow. Architecture (his call, 2026-08-27): the
/76265/ index is **public** — titles and dates show ungated — but each poem's
**body is password-gated**, one payload per poem. Passwords are **per poem**
(since 2026-09-15; the first poem uses the build's default, later ones may set
their own). Bodies must never exist tracked; this repo is public.

### Pieces

- `_pages/76265.html` — orphan page (`nav: false`, `sitemap: false`, title stays
  "76265"). Liquid-renders the public index from `_data/poems_76265.yml`;
  hash-routes `#<slug>` to a poemlock gate (style lifted from /poem7-24-26/) that
  fetches `assets/enc/76265-<slug>.json` and decrypts with WebCrypto —
  PBKDF2-SHA256 300k → AES-256-GCM, the `bin/research_lock.py` scheme.
  `sessionStorage["poems76265_pw"]` (a JSON list of every password entered this
  session, most recent first) auto-unlocks sibling poems and reloads, trying each
  in turn. The page also owns the `.poem-flip-card` CSS/JS (click-to-flip image
  poems, see below) — poem HTML is injected with `innerHTML`, so its scripts
  would never run.
- `_data/poems_76265.yml` — generated public manifest (slug, title, date).
- `local/poems/76265/` — **untracked** masters: the source PDFs/images, one
  `poems/NN-<slug>.html` per poem (image poems keep their web-sized copies in
  `poems/NN-<slug>/`), and `build.py` (writes the manifest + all payloads;
  inlines relative `src="…"` images as data URIs so they ship only encrypted).
- Passwords live in untracked `local/passwords.md`. A poem master may carry
  `<!-- password: word -->` to override the build's default; comments are
  stripped before encryption. Never write a password anywhere tracked; if the
  file is missing, ask Chris.

### Adding a poem

1. Copy the PDF into `local/poems/76265/`.
2. Extract the text layer (`pdftotext -layout`) **and** render/Read the PDF
   pages — the text layer can't show which words are italic.
3. Write `local/poems/76265/poems/NN-<slug>.html` (NN = next number; filename
   order is index order): first line `<!-- date: M-D-YY -->` (site poem date
   format, e.g. 8-27-26 — the date it goes up unless Chris gives one), then
   `<h1 class="poem-title">Title</h1>`, then one `<p>` per stanza with `<br>`
   line breaks exactly as the PDF shows them. Verbatim per
   [content-rules](content-rules.md): curly quotes/apostrophes and em-dashes as
   typed, `<em>` where the PDF is italic. This HTML never meets kramdown, so no
   entity-escaping games are needed.
4. `python3 local/poems/76265/build.py <default-password> [site-dir]` — pass a
   `main` worktree as `site-dir` when the checkout is on another branch (the
   page lives on `main`).
5. Verify before pushing: word-diff the decrypted payload against the PDF text
   layer (zero real diffs; `<em>`-boundary tokenization artifacts are fine),
   then serve locally and click through index → gate → wrong password ("not
   it.") → unlock in the browser.
6. Commit exactly what the build regenerated — `_data/poems_76265.yml` +
   `assets/enc/76265-*.json` (payloads get fresh salts each run) — plus
   `_pages/76265.html` only if the page itself changed. Titles/dates are public
   so they may appear in commit messages; body lines may not.
7. Push = deploy (normal repo rules — Chris says push/put it up). Verify live on
   chrisshi.com per [site-basics](site-basics.md), grepping the live page for
   the new title and confirming body words are absent.

### Image / erasure poems (flip card)

The 2026-09-15 pattern, for a poem that is a picture with a source underneath:

- Web-sized copies (JPEG q85, full phone/iPad resolution is fine — hundreds of
  KB) go in `local/poems/76265/poems/NN-<slug>/`; originals one dir up.
- Master body after the `<h1>`:
  `<figure class="poem-flip"><button class="poem-flip-card" type="button"
  aria-pressed="false" style="aspect-ratio: W / H"><span class="poem-flip-inner">
  <img class="poem-flip-front" src="NN-<slug>/poem.jpg" …><img
  class="poem-flip-back" src="NN-<slug>/page.jpg" …></span></button>
  <figcaption>…instructions…</figcaption></figure>` — front is the poem, back
  is what it was cut from; the inline aspect-ratio is the front image's.
- Don't lazy-load the back image (a lazy image on a rotated backface never
  loads — see site-basics). The build inlines both as data URIs.
- Per-poem password: `<!-- password: word -->` at the top of the master.

### Rules

- Titles and dates public by design; bodies only ever inside ciphertext — not in
  commits, alt text, docs, or this file.
- New poems are data-only changes (manifest + payload); the page doesn't change
  unless the design does.
- /poem7-24-26/ is separate (own page, own password, not in the directory).
