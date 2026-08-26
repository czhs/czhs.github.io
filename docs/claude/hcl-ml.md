# /HCL-ML — the Sensor Context Encoder Challenge page

An orphan, password-gated page (`nav: false`, not in the /research listing) built
for the HCL ML challenge. Same at-rest scheme as /research but its **own**
password and `sessionStorage` key (`hcl_pw`) — the password is recorded only in
the private master archive (see Publishing), never in this repo. The challenge
brief is `~/Desktop/HCL Project/ML Challenge.pdf`; the work lives on the 4090
(`~/HCL-Project/HCL-ML`).

## One unified document

Since 2026-08-26 the body is a single unified technical write-up (the earlier
two-version report/notebook picker was removed). The plaintext master is
`_pages/hcl-ml.md` locally (a `.hcl-doc` div of raw HTML blocks); the published
stub carries only front matter plus `enc_payload`. Chrome is
`_includes/hcl_tab_chrome.liquid` (scroll-spy contents rail, built from the DOM
after unlock so no heading ships in the clear) and `_includes/hcl_ends.liquid`
(the robotics-portfolio end card). Figure includes under
`_includes/research/hcl/` are local-only and gitignored — the built body embeds
them before encryption, so committing them would leak the content.

**This page is the one allowed link to `/robotics/`** (Chris, 2026-08-21). The
never-link rule in [robotics-ml-portfolio](robotics-ml-portfolio.md) protects the
public personal site; /HCL-ML is gated and shared with the same audience.

## Inline co-drafting (local only)

The preview layout includes `_includes/hcl_editor.liquid`; the published layout
(`hcl_locked`) does not, so none of it ships. With both servers up —

- `jekyll` (launch.json) — the watching serve; a `--detach`ed serve does **not**
  regenerate, so kill that first if one is around.
- `hcl-edit` (launch.json) — `python3 local/hcl_edit.py 4031`.

— every prose block on `localhost:4000/HCL-ML/` is `contenteditable`. Leaving a
block POSTs it to the server, which rewrites that element **in place in
`_pages/hcl-ml.md`**, so the next `Read` of the file sees Chris's edit. Blocks are
matched by tag + normalised text in document order; a figure include inside a
block round-trips as a `[[HCL_INCLUDE]]` token. Enter splits a paragraph,
Backspace in an empty one deletes it, Esc leaves. The first write of a run drops
a backup at `local/hcl-ml.<stamp>.bak.md`; the server's stdout is the op log.

To co-draft after publication, restore the plaintext master from the archive
into `_pages/hcl-ml.md` (layout `hcl_preview`), edit, then re-run Publishing.

## Publishing

Same pipeline as [research-posts](research-posts.md) with the page's own
password: restore/keep the plaintext master, build so `_site/HCL-ML/index.html`
has real content, then

    python3 bin/research_lock.py hcl-ml <pw> _site/HCL-ML/index.html assets/enc/hcl-ml.json

swap the page to the stub (`layout: hcl_locked` + `enc_payload:
/assets/enc/hcl-ml.json`, no body), archive the plaintext master at
`/Users/hshi/Desktop/VPD-Copying/docs/research_src/` (password noted in its
README), rebuild, and verify the gate serves zero plaintext before committing.
First published 2026-08-26.
