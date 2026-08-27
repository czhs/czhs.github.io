# /76265/ poem directory — adding a poem from an uploaded PDF

When Chris uploads a poem PDF and asks to put it up, this is the whole workflow.
Architecture (his call, 2026-08-27): the /76265/ index is **public** — titles and
dates show ungated — but each poem's **body is password-gated**, one payload per
poem, all poems currently sharing one password. Bodies must never exist tracked;
this repo is public.

### Pieces

- `_pages/76265.html` — orphan page (`nav: false`, `sitemap: false`, title stays
  "76265"). Liquid-renders the public index from `_data/poems_76265.yml`;
  hash-routes `#<slug>` to a poemlock gate (style lifted from /poem7-24-26/) that
  fetches `assets/enc/76265-<slug>.json` and decrypts with WebCrypto —
  PBKDF2-SHA256 300k → AES-256-GCM, the `bin/research_lock.py` scheme.
  `sessionStorage["poems76265_pw"]` auto-unlocks sibling poems and reloads, like
  the research gate.
- `_data/poems_76265.yml` — generated public manifest (slug, title, date).
- `local/poems/76265/` — **untracked** masters: the source PDFs, one
  `poems/NN-<slug>.html` per poem, and `build.py` (writes the manifest + all
  payloads).
- Passwords live in untracked `local/passwords.md`. Never write one anywhere
  tracked; if the file is missing, ask Chris.

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
4. `python3 local/poems/76265/build.py <password>`.
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

### Rules

- Titles and dates public by design; bodies only ever inside ciphertext — not in
  commits, alt text, docs, or this file.
- New poems are data-only changes (manifest + payload); the page doesn't change
  unless the design does.
- /poem7-24-26/ is separate (own page, own password, not in the directory).
