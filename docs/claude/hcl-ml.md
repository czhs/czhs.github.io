# /research/hcl-ml/ — the Sensor Context Encoder Challenge write-up

The unified technical write-up for the HCL ML challenge (brief:
`~/Desktop/HCL Project/ML Challenge.pdf`; the work lives on the 4090,
`~/HCL-Project/HCL-ML`; code at github.com/czhs/HCL-ML).

**Public since 2026-10-31.** Chris moved it into the research journal with no
password: `_research/hcl-ml.html`, `layout: research_public`, cover
`art-relic-of-progenitus.jpg` (Scryfall art crop, EMA #231, sized like the
other covers). `/HCL-ML/` (`_pages/hcl-ml.md`) is now a `layout: redirect`
stub so the old shared link still lands.

What changed in the move:

- The body is the decrypted former payload (figures already inlined), wrapped
  in `{% raw %}`. The two closing paragraphs addressed to the hiring team (the
  home-robotics paragraph and the "Postscript") were cut at Chris's request —
  don't restore them on a public page.
- The robotics end card (`hcl_ends.liquid`) is gone: the page is now on the
  public personal site, so the never-link-to-`/robotics/` rule in
  [robotics-ml-portfolio](robotics-ml-portfolio.md) applies to it.
- Removed with the gate: `hcl_locked`, `hcl_preview`, `hcl_editor.liquid`,
  `assets/enc/hcl-ml.json`. The inline co-drafting editor (`local/hcl_edit.py`)
  targeted the old `_pages/hcl-ml.md` master and is dormant; restore from git
  history (`f9f0807e`) if it is wanted again.
- Kept: `hcl_tab_chrome.liquid` (scroll-spy contents rail + the repo card
  styles), included from the entry body.

Edit the write-up directly in `_research/hcl-ml.html`.

Title and description are verbatim from the repo README (its heading and
opening sentence), not new copy — keep them sourced that way.
