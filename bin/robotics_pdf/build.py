#!/usr/bin/env python3
"""Build the /robotics/ portfolio PDF: a cover with a table of contents, then
one landscape page per project, in the site's zine skin.

  python3 bin/robotics_pdf/build.py            # out/robotics-portfolio.pdf
  python3 bin/robotics_pdf/build.py --png      # + out/png/<page>.png previews
  python3 bin/robotics_pdf/build.py --only duck --png   # one page, into out/only-duck/

Inputs: _data/robotics.yml (order, titles, dates, captions, links) and one
fragment per project in pages/<slug>.html — the *body* of that page only; the
masthead and footer are written here so every page matches. Images come from
assets/img/robotics/ (served as img/<basename>) or frames/ (stills cut from the
clips with ffmpeg, served as frames/<name>). See CONTRACT.md.

The build refuses to finish quietly when a page overflows: after layout it
measures every element against its sheet and lists anything that runs past the
edge, is clipped, failed to load, or is an image the project may not use.
"""
import argparse
import datetime as dt
import html
import os
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
DATA = REPO / "_data" / "robotics.yml"
IMG = REPO / "assets" / "img" / "robotics"
FONTS = REPO / "assets" / "fonts"
FRAMES = HERE / "frames"
PAGES = HERE / "pages"
SITE = "https://chrisshi.com"
PW, PH = 1056, 816
PDF_NAME = "robotics-portfolio.pdf"

# Lead figures that the page stubs (_pages/robotics_<slug>.md) place themselves,
# so they are not in the data file's media lists but are part of the project.
STUB_IMAGES = {
    "robot-dog": ["robot-dog-poster.jpg"],
    "gantry": ["gantry-poster.jpg"],
    "tartanimu": ["tartanimu-traj.jpg"],
}
# Image-name prefixes a project's frames/ stills must carry.
PREFIX = {
    "joust": ("joust",),
    "robot-dog": ("robot-dog",),
    "duck": ("duck",),
    "pie-robot": ("pie",),
    "gantry": ("gantry",),
    "tartanimu": ("tartanimu",),
    "dice-arms": ("dice-arms",),
}
# Never in the PDF: the pie-robot b-roll is password-gated on the site.
FORBIDDEN = re.compile(r"^pie-robot-broll")
# Cover-sheet cells that should not use the site's card cover (slug -> src).
# Empty since 2026-09-16: the duck card is now the leg-free cutout itself.
COVER_STILL = {}


def esc(s):
    return html.escape("" if s is None else str(s), quote=True)


def load():
    return yaml.safe_load(DATA.read_text())


def allowed_images(p):
    """Every still the data file (plus the page stub) attaches to a project."""
    names = set()

    def add(path):
        if path:
            names.add(Path(path).name)

    add(p.get("cover"))
    add(p.get("poster"))
    for s in p.get("run") or []:
        add(s.get("poster"))
        add(s.get("image"))
    for m in p.get("media") or []:
        add(m.get("poster"))
        add(m.get("image"))
    for sec in p.get("sections") or []:
        for m in sec.get("media") or []:
            add(m.get("poster"))
            add(m.get("image"))
    names.update(STUB_IMAGES.get(p["slug"], []))
    return {n for n in names if not FORBIDDEN.match(n)}


def abs_url(url):
    if url.startswith("/"):
        return SITE + url
    return url


def show_url(url):
    return re.sub(r"^(https?://|mailto:)(www\.)?", "", url).rstrip("/") + ("/" if url.endswith("/") else "")


def cover_html(d, projects, total):
    rows = []
    for i, p in enumerate(projects, 1):
        rows.append(
            f'<a class="toc-row" href="#p-{esc(p["slug"])}">'
            f'<span class="toc-num">{i:02d}</span>'
            f'<span class="toc-main"><span class="toc-title">{esc(p["title"])}</span>'
            f'<span class="toc-date">{esc(p.get("date"))}</span></span>'
            f'<span class="toc-page">{i + 1:02d}</span></a>'
        )
    links = []
    for l in d.get("links") or []:
        url = abs_url(l["url"])
        if url.lower().endswith(".pdf"):
            continue  # the sidebar's link to this very file
        links.append(f'<a href="{esc(url)}"><span>{esc(l["label"])}</span><span class="url">{esc(show_url(url))}</span></a>')
    cells = []
    for i, p in enumerate(projects, 1):
        cover = Path(p.get("cover") or p.get("poster") or "").name
        src = COVER_STILL.get(p["slug"]) or (f"img/{cover}" if cover else "")
        img = f'<img src="{esc(src)}" alt="">' if src else ""
        cells.append(
            f'<a class="cell" href="#p-{esc(p["slug"])}">{img}'
            f'<span class="cell-cap"><span class="cell-head"><span class="cell-num">{i:02d}</span>'
            f'<span class="cell-title">{esc(p["title"])}</span><span class="cell-date">{esc(p.get("date"))}</span></span>'
            f'<span class="cell-blurb">{esc(p.get("blurb"))}</span></span></a>'
        )
    month = dt.date.today().strftime("%B %Y")
    cells.append(
        '<div class="cell colophon" style="grid-column: span 2">'
        f'<strong><a href="{SITE}/robotics/">chrisshi.com/robotics/</a></strong>'
        f'Portfolio · {esc(month)}<br>{esc(d["name"])} · chrisshi@andrew.cmu.edu</div>'
    )
    return (
        '<section class="page" id="cover"><div class="sheet"><div class="cover">'
        '<aside class="cv-side">'
        f'<p class="eyebrow">{esc(d.get("site_label", "Robotics"))}</p>'
        f'<h1 class="cv-name">{esc(d["name"])}<span class="dot">.</span></h1>'
        f'<p class="cv-sub">{esc(d.get("subtitle"))}</p>'
        f'<nav class="toc"><p class="toc-h">Index</p>{"".join(rows)}</nav>'
        f'<nav class="cv-links">{"".join(links)}</nav>'
        "</aside>"
        f'<div class="contact cv-contact" style="--cols:3; --rows:3">{"".join(cells)}</div>'
        "</div></div></section>"
    )


def project_html(p, num, pageno, total, body):
    url = f"{SITE}/robotics/{p['slug']}/"
    return (
        f'<section class="page" id="p-{esc(p["slug"])}"><div class="sheet">'
        f'<header class="mast"><span class="mast-num">{num:02d}</span>'
        f'<h1 class="mast-title">{esc(p["title"])}</h1>'
        f'<span class="mast-date">{esc(p.get("date"))}</span></header>'
        f'<div class="body">{body}</div>'
        f'<footer class="foot"><a href="{esc(url)}">{esc(show_url(url))}</a>'
        f'<span class="foot-mid">Chris Shi · Robotics</span>'
        f'<span>{pageno:02d} / {total:02d}</span></footer>'
        "</div></section>"
    )


def fragment(slug):
    f = PAGES / f"{slug}.html"
    if f.exists():
        return f.read_text()
    return f'<div class="todo">pages/{esc(slug)}.html — not written yet</div>'


def document(pages):
    css = (HERE / "style.css").read_text()
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        "<title>Chris Shi — Robotics</title>"
        f"<style>{css}</style></head><body>{''.join(pages)}</body></html>"
    )


CHECK_JS = r"""
(allowed) => {
  const issues = [];
  const describe = (el) => {
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    if (el.className && typeof el.className === 'string') s += '.' + el.className.trim().split(/\s+/).join('.');
    const t = (el.textContent || '').trim().replace(/\s+/g, ' ');
    if (t) s += ' "' + t.slice(0, 40) + (t.length > 40 ? '…' : '') + '"';
    if (el.tagName === 'IMG') s += ' [' + el.getAttribute('src') + ']';
    return s;
  };
  document.querySelectorAll('.page').forEach((pg) => {
    const sheet = pg.querySelector('.sheet');
    const cs = getComputedStyle(sheet);
    const r = sheet.getBoundingClientRect();
    const box = {
      left: r.left + parseFloat(cs.borderLeftWidth) + parseFloat(cs.paddingLeft),
      right: r.right - parseFloat(cs.borderRightWidth) - parseFloat(cs.paddingRight),
      top: r.top + parseFloat(cs.borderTopWidth) + parseFloat(cs.paddingTop),
      bottom: r.bottom - parseFloat(cs.borderBottomWidth) - parseFloat(cs.paddingBottom),
    };
    // A project page's fragment must also stay inside .body — the band between
    // masthead and footer. Overflow smaller than the footer's margin would
    // otherwise pass the sheet check and quietly sit on the footer rule.
    const body = pg.querySelector('.body');
    const bodyBox = body ? body.getBoundingClientRect() : null;
    const seen = new Set();
    sheet.querySelectorAll('*').forEach((el) => {
      const b = el.getBoundingClientRect();
      if (!b.width && !b.height) return;
      const over = [];
      const lim = (body && body.contains(el)) ? bodyBox : box;
      const what = (lim === bodyBox) ? 'the body (masthead-to-footer band)' : 'the sheet';
      if (b.bottom > lim.bottom + 0.6) over.push('bottom by ' + (b.bottom - lim.bottom).toFixed(1) + 'px');
      if (b.right > lim.right + 0.6) over.push('right by ' + (b.right - lim.right).toFixed(1) + 'px');
      if (b.top < lim.top - 0.6) over.push('top by ' + (lim.top - b.top).toFixed(1) + 'px');
      if (b.left < lim.left - 0.6) over.push('left by ' + (lim.left - b.left).toFixed(1) + 'px');
      if (over.length) {
        // report the outermost offender only once per branch
        let anc = el.parentElement, dup = false;
        while (anc && anc !== sheet) { if (seen.has(anc)) { dup = true; break; } anc = anc.parentElement; }
        if (!dup) { seen.add(el); issues.push(pg.id + ': ' + describe(el) + ' runs past ' + what + ' (' + over.join(', ') + ')'); }
      }
      const st = getComputedStyle(el);
      const hides = /hidden|clip/.test(st.overflowY) || /hidden|clip/.test(st.overflowX);
      if (hides && el.tagName !== 'IMG') {
        if (el.scrollHeight > el.clientHeight + 1.5) issues.push(pg.id + ': ' + describe(el) + ' clips its content vertically (' + (el.scrollHeight - el.clientHeight).toFixed(0) + 'px hidden)');
        if (el.scrollWidth > el.clientWidth + 1.5 && st.textOverflow !== 'ellipsis') issues.push(pg.id + ': ' + describe(el) + ' clips its content horizontally (' + (el.scrollWidth - el.clientWidth).toFixed(0) + 'px hidden)');
      }
      if (el.tagName === 'IMG') {
        const src = el.getAttribute('src') || '';
        if (!el.complete || !el.naturalWidth) issues.push(pg.id + ': image failed to load [' + src + ']');
        const slug = pg.id.replace(/^p-/, '');
        if (pg.id !== 'cover' && allowed[slug]) {
          const name = src.split('/').pop();
          const ok = src.startsWith('img/') ? allowed[slug].img.includes(name)
                   : src.startsWith('frames/') ? allowed[slug].prefix.some((px) => name.startsWith(px)) && !/^pie-robot-broll/.test(name)
                   : false;
          if (!ok) issues.push(pg.id + ': image not in this project\'s media set [' + src + ']');
        }
        if (b.width < 40 || b.height < 40) issues.push(pg.id + ': tiny image (' + b.width.toFixed(0) + 'x' + b.height.toFixed(0) + ') [' + src + ']');
      }
    });
  });
  return issues;
}
"""


def ensure_links(out):
    out.mkdir(parents=True, exist_ok=True)
    for name, target in (("img", IMG), ("fonts", FONTS), ("frames", FRAMES)):
        target.mkdir(parents=True, exist_ok=True)
        link = out / name
        if link.is_symlink() or link.exists():
            if link.is_symlink() and os.readlink(link) == str(target):
                continue
            link.unlink()
        link.symlink_to(target)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="render one page: a project slug, or 'cover'")
    ap.add_argument("--png", action="store_true", help="also write out/png/<page>.png previews")
    ap.add_argument("--out", help="output directory (default out/, or out/only-<slug>/)")
    args = ap.parse_args()

    d = load()
    projects = d["projects"]
    total = len(projects) + 1
    allowed = {p["slug"]: {"img": sorted(allowed_images(p)), "prefix": list(PREFIX.get(p["slug"], (p["slug"],)))} for p in projects}

    pages = []
    if not args.only or args.only == "cover":
        pages.append(cover_html(d, projects, total))
    for i, p in enumerate(projects, 1):
        if args.only and args.only != p["slug"]:
            continue
        pages.append(project_html(p, i, i + 1, total, fragment(p["slug"])))
    if not pages:
        sys.exit(f"no page called {args.only!r}; slugs: {[p['slug'] for p in projects]}")

    out = Path(args.out) if args.out else (HERE / "out" / (f"only-{args.only}" if args.only else ""))
    ensure_links(out)
    html_path = out / "index.html"
    html_path.write_text(document(pages))

    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": PW, "height": PH}, device_scale_factor=1.5)
        page = ctx.new_page()
        page.goto(html_path.as_uri(), wait_until="load")
        page.evaluate("() => document.fonts.ready")
        page.evaluate(
            "() => Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => { i.onload = r; i.onerror = r; })))"
        )
        page.wait_for_timeout(150)
        issues = page.evaluate(CHECK_JS, allowed)
        n = page.locator(".page").count()
        if args.png:
            png_dir = out / "png"
            png_dir.mkdir(exist_ok=True)
            for i in range(n):
                loc = page.locator(".page").nth(i)
                pid = loc.get_attribute("id")
                loc.screenshot(path=str(png_dir / f"{pid}.png"))
            print(f"png previews: {png_dir}")
        pdf_path = out / PDF_NAME
        page.pdf(path=str(pdf_path), prefer_css_page_size=True, print_background=True,
                 margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        browser.close()

    from pypdf import PdfReader, PdfWriter

    # Chromium stamps itself as creator; give the file its own name and author.
    reader = PdfReader(str(pdf_path))
    npages = len(reader.pages)
    writer = PdfWriter(clone_from=reader)
    writer.add_metadata({
        "/Title": f"{d['name']} — Robotics Portfolio",
        "/Author": d["name"],
        "/Subject": f"{d.get('site_label', 'Robotics')} portfolio, {dt.date.today().strftime('%B %Y')} — {SITE}/robotics/",
        "/Creator": "bin/robotics_pdf/build.py",
    })
    with open(pdf_path, "wb") as fh:
        writer.write(fh)
    size_mb = pdf_path.stat().st_size / 1e6
    print(f"pdf: {pdf_path} — {npages} pages, {size_mb:.1f} MB")
    if npages != n:
        issues.append(f"PDF has {npages} pages but the document has {n} .page sections — something spilled onto an extra page")
    if issues:
        print(f"\n{len(issues)} LAYOUT ISSUE(S):")
        for s in issues:
            print("  - " + s)
        sys.exit(2)
    print("layout: OK — nothing runs past its sheet, nothing clipped, every image loaded")


if __name__ == "__main__":
    main()
