# /robotics/ and /ml/ — portfolio micro-sites (published shells)

Standalone portfolio micro-sites Chris shares directly with employers. Published as
**under-construction placeholder shells** since 2026-07-20 (`under_construction:
true`, all `cover`/`video` blanked); the MEDIA stays local-only
([site-basics.md](site-basics.md)).

**Hard constraint: the personal site must NEVER link to `/robotics/`** — not navbar,
homepage, or pokedex. All robotics pages carry `nav: false`. The link is one-way:
robotics links back to `/` ("Personal Website" in its sidebar). This is the inverse
of MLn's one-way rule.

Architecture (mirrors MLn's data-driven pattern, shared across both sites since the
`portfolio*` refactor): `_data/robotics.yml` + `_data/ml.yml` (`name`, `subtitle`,
`under_construction`, `links:`, `projects:` — `slug, title, date, cover`; order =
grid order); shared layouts `_layouts/portfolio*.liquid` +
`_includes/portfolio_styles.liquid`; pages `_pages/{robotics,ml}.html` +
`_pages/{robotics,ml}_<slug>.md` (thin: `layout, permalink, project`, heading
skeleton marked *Under construction*).

Projects (robotics, 6): Pie Robot, Gantry, Robot Dog, Duck, Dice Arms, TartanIMU.
Bodies/dates/covers intentionally empty for Chris to fill — do NOT fabricate
write-ups or specs ([content-rules.md](content-rules.md)). Real images go in
`assets/img/robotics/` (gitignored until a project goes public), never
`robotics_media/`.

To add a project: append to `projects:` in the data file + add the
`_pages/<site>_<slug>.md` stub. To publish a project: point its `cover`/`video` back
at the media paths (wired in the data-file comments) and commit those specific
assets.
