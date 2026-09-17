#!/usr/bin/env python3
"""The /robotics/ portfolio's cover image — the picture that stands for the whole
portfolio wherever one image has to (the og:image link preview, 1200 x 630).

It is the site's own index page redrawn as one still: the zine sheet inside the
ink frame on the seafoam field, the sidebar's name block and mono index on the
left, and a ruled contact sheet of the projects' stills on the right with Robot
Jousting as the hero cell. Every literal (palette, faces, weights, rules) comes
from _includes/portfolio_styles.liquid; titles come from _data/robotics.yml.

    python3 bin/robotics_cover.py            # writes assets/img/robotics-portfolio-cover.jpg
    python3 bin/robotics_cover.py out.jpg    # elsewhere

Needs Pillow, PyYAML and fontTools (+ brotli) — the site's variable woff2 fonts
are instanced to static TTFs in a cache dir on first run. Stills are read from
the gitignored assets/img/robotics/ (local copies of the robotics-media release).
Renders and simulation frames are deliberately not used: on a cover nothing is
captioned, and the site's rule is that renders stay labelled as renders.
"""
import os
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / 'assets' / 'img' / 'robotics'
FONT_SRC = ROOT / 'assets' / 'fonts'
CACHE = Path(os.environ.get('ROBOTICS_COVER_FONTS', ROOT / 'bin' / '.fontcache'))
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'assets' / 'img' / 'robotics-portfolio-cover.jpg'

# zine seafoam, fixed — portfolio_styles.liquid literals
FIELD = (0x8F, 0xB2, 0xA4)
INK = (0x13, 0x26, 0x1F)
IVORY = (0xFF, 0xFC, 0xF2)
ACCENT = (0x0F, 0x60, 0x46)


def mix(c, bg, t):
    return tuple(round(t * a + (1 - t) * b) for a, b in zip(c, bg))


INK_SOFT = mix(INK, IVORY, 0.62)
RAIL = mix(INK, IVORY, 0.26)
NUM = mix(INK, IVORY, 0.40)

# The mosaic, in reading order. The first still is the hero (2 x 2 cells); the
# rest fill the remaining cells of a 4 x 3 grid. Card covers first, then the
# strongest real frames from the footage and one CAD view (the joust gripper's
# CAD carries a caption inside the image that a square crop cuts through).
STILLS = [
    'joust.jpg',
    'robot-dog-card.jpg',
    'duck-card.jpg',
    'pie-robot-card.jpg',
    'gantry.jpg',
    'dice-arms.jpg',
    'tartanimu.jpg',
    'pie-cream-poster.jpg',
    'gantry-cad-1.jpg',
]

# Render at 2x and downsample: text and 3px rules stay crisp in the JPEG.
S = 2
W, H = 1200 * S, 630 * S
SHM, FW, SHP = 14 * S, 8 * S, 26 * S       # field ring, ink frame, sheet padding
RULE = 3 * S


def font(name, size):
    """Static instance of one of the site's variable fonts, cached as TTF."""
    CACHE.mkdir(parents=True, exist_ok=True)
    src, axis = {
        'sans': ('plus-jakarta-sans-latin-var.woff2', 'wght'),
        'mono': ('jetbrains-mono-latin-var.woff2', 'wght'),
    }[name[0]]
    weight = name[1]
    ttf = CACHE / f'{src.split("-latin")[0]}-{weight}.ttf'
    if not ttf.exists():
        from fontTools.ttLib import TTFont
        from fontTools.varLib import instancer
        f = TTFont(FONT_SRC / src)
        f.flavor = None
        instancer.instantiateVariableFont(f, {axis: weight}).save(ttf)
    return ImageFont.truetype(str(ttf), int(size * S))


def text(draw, xy, s, f, fill, tracking=0.0):
    """Draw with letter-spacing (em units); Pillow has no tracking of its own."""
    x, y = xy
    if not tracking:
        draw.text((x, y), s, font=f, fill=fill)
        return f.getlength(s)
    t = tracking * f.size
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + t
    return x - xy[0]


def cover_fit(im, w, h):
    """object-fit: cover — scale to fill w x h, crop the excess about the centre."""
    im = im.convert('RGB')
    s = max(w / im.width, h / im.height)
    im = im.resize((max(w, round(im.width * s)), max(h, round(im.height * s))), Image.LANCZOS)
    left = (im.width - w) // 2
    top = (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))


def main():
    data = yaml.safe_load((ROOT / '_data' / 'robotics.yml').read_text())
    projects = data['projects']

    img = Image.new('RGB', (W, H), FIELD)
    d = ImageDraw.Draw(img)
    # the window: ink frame on the field, ivory sheet inside
    d.rectangle((SHM, SHM, W - SHM - 1, H - SHM - 1), fill=INK)
    d.rectangle((SHM + FW, SHM + FW, W - SHM - FW - 1, H - SHM - FW - 1), fill=IVORY)

    x0, y0 = SHM + FW + SHP, SHM + FW + SHP          # sheet content origin
    x1, y1 = W - SHM - FW - SHP, H - SHM - FW - SHP  # and far corner
    col_w = 318 * S                                    # the sidebar column
    gap = 34 * S

    # ── sidebar ────────────────────────────────────────────────────────────
    eyebrow = font(('mono', 700), 11)
    name_f = font(('sans', 800), 60)
    sub_f = font(('sans', 500), 16.5)
    idx_num = font(('mono', 400), 11)
    idx_title = font(('sans', 600), 16)
    idx_date = font(('mono', 400), 10)
    url_f = font(('mono', 700), 11.5)

    y = y0 + 2 * S
    text(d, (x0, y), data.get('site_label', 'Robotics').upper(), eyebrow, ACCENT, tracking=0.18)
    y += 26 * S
    # the name at display size, tight tracking, accent dot
    nm = data['name']
    xx = x0
    for i, ch in enumerate(nm):
        d.text((xx, y), ch, font=name_f, fill=INK)
        xx += name_f.getlength(ch) - 0.045 * name_f.size
        if i + 1 < len(nm) and nm[i + 1] == ' ':
            xx += 0.03 * name_f.size
    d.text((xx, y), '.', font=name_f, fill=ACCENT)
    y += 80 * S
    # subtitle, wrapped to the column
    words = data['subtitle'].split()
    lines, cur = [], ''
    for w_ in words:
        trial = (cur + ' ' + w_).strip()
        if sub_f.getlength(trial) <= col_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    lines.append(cur)
    for ln in lines:
        d.text((x0, y), ln, font=sub_f, fill=INK_SOFT)
        y += 24 * S

    # index: 3px rule, mono eyebrow, numbered rows with dates (the sidebar's manifest)
    y += 18 * S
    d.rectangle((x0, y, x0 + col_w, y + RULE - 1), fill=INK)
    y += 14 * S
    text(d, (x0, y), 'INDEX', font(('mono', 700), 9.5), INK_SOFT, tracking=0.16)
    y += 22 * S
    row_h = 32 * S
    for i, p in enumerate(projects, 1):
        d.text((x0, y + 3 * S), f'{i:02d}', font=idx_num, fill=NUM)
        d.text((x0 + 30 * S, y), p['title'], font=idx_title, fill=INK)
        date = (p.get('date') or '').upper()
        if date:
            wdt = idx_date.getlength(date)
            d.text((x0 + col_w - wdt, y + 4 * S), date, font=idx_date, fill=NUM)
        y += row_h
        if i < len(projects):
            d.rectangle((x0, y - 6 * S, x0 + col_w, y - 6 * S + max(1, S // 2) + S // 2), fill=RAIL)

    # the address, bottom-left, over its own rule
    ub = y1 - 14 * S
    d.rectangle((x0, ub - 12 * S, x0 + col_w, ub - 12 * S + RULE - 1), fill=INK)
    text(d, (x0, ub - 1 * S), 'CHRISSHI.COM/ROBOTICS/', url_f, INK, tracking=0.08)

    # ── contact sheet ──────────────────────────────────────────────────────
    gx0 = x0 + col_w + gap
    gx1, gy0, gy1 = x1, y0, y1
    cols, rows = 4, 3
    # cell geometry: outer 3px border, 3px rules between cells
    inner_w = gx1 - gx0 - 2 * RULE - (cols - 1) * RULE
    inner_h = gy1 - gy0 - 2 * RULE - (rows - 1) * RULE
    cw = inner_w // cols
    ch = inner_h // rows
    # snap the grid to whole cells so every rule is exactly 3px
    gx1 = gx0 + 2 * RULE + cols * cw + (cols - 1) * RULE
    gy1 = gy0 + 2 * RULE + rows * ch + (rows - 1) * RULE
    d.rectangle((gx0, gy0, gx1 - 1, gy1 - 1), fill=INK)

    def cell_box(c, r, span=1):
        x = gx0 + RULE + c * (cw + RULE)
        yy = gy0 + RULE + r * (ch + RULE)
        w = span * cw + (span - 1) * RULE
        h = span * ch + (span - 1) * RULE
        return x, yy, w, h

    # hero at (0,0) spanning 2x2; the remaining cells in reading order
    slots = [(0, 0, 2)]
    for r in range(rows):
        for c in range(cols):
            if r < 2 and c < 2:
                continue
            slots.append((c, r, 1))
    for (c, r, span), still in zip(slots, STILLS):
        x, yy, w, h = cell_box(c, r, span)
        src = IMG / still
        if not src.exists():
            sys.exit(f'missing still: {src} (pull the robotics-media release into assets/img/robotics/)')
        img.paste(cover_fit(Image.open(src), w, h), (x, yy))
    # a cell without a still stays the sheet's ivory (none with nine stills)
    for (c, r, span) in slots[len(STILLS):]:
        x, yy, w, h = cell_box(c, r, span)
        d.rectangle((x, yy, x + w - 1, yy + h - 1), fill=IVORY)

    out = img.resize((W // S, H // S), Image.LANCZOS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT, quality=90, optimize=True, progressive=True)
    print('wrote', OUT, out.size, f'{OUT.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
