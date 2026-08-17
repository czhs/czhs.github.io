# chrisshi.com — DNS wiring and cutover

Registered at Cloudflare 2026-08-04. Currently serves a **coming-soon placeholder**,
NOT this site — czhs.github.io serves directly with no redirect.

Three moving parts:

1. **Cloudflare DNS** (zone `chrisshi.com`): 4 A records `@` → `185.199.108–111.153`,
   4 AAAA `@` → `2606:50c0:8000–8003::153`, CNAME `www` → `czhs.github.io`.
   **All records stay grey-cloud "DNS only"** — proxying breaks GitHub's Let's
   Encrypt challenge, and Cloudflare SSL "Flexible" causes an infinite redirect loop
   with Pages. DNS never changes when switching which repo serves the domain.
2. **`czhs/chrisshi-coming-soon`** (local: `~/Desktop/chrisshi-coming-soon`) — plain
   HTML, no Jekyll; its root `CNAME` currently claims the domain. It also doubles as
   the company page for Karst Biodefense (contact `research@chrisshi.com`) — don't
   take it down without a replacement at the domain.
3. **This repo** — has NO `CNAME` and `url: https://czhs.github.io` while the
   placeholder holds the domain.

**Cutover to chrisshi.com:** clear the domain on the placeholder first
(`gh api -X PUT repos/czhs/chrisshi-coming-soon/pages -f cname=""`) — two repos can't
claim one domain — then add a root `CNAME` containing `chrisshi.com` here and set
`url:` in `_config.yml`. Reverse symmetrically.

**Why `CNAME` must live in `main`, not just the Settings UI:** `deploy.yml` publishes
with `JamesIves/github-pages-deploy-action`, which wipes `gh-pages` every run — a
Settings-written CNAME gets deleted on the next push, silently unsetting the domain.
Jekyll copies a root `CNAME` into `_site` (not in `exclude:`), so keeping it in
`main` makes it survive. Note: once the user site has a custom domain,
`czhs.github.io/*` 301s to it, path preserved.
