#!/usr/bin/env python3
"""Cut the ringworld character sprites out of the source sticker sheets.

The sheets in assets/img/ringworld/source/ are watercolour characters on flat
white. This thresholds to an ink mask, dilates enough that a character merges
with its own sparkles but not with its neighbours, labels the blobs, and writes
each one to assets/img/ringworld/sprites/ with the white knocked out to alpha.

Sprites are named by hand in NAMES below, keyed by sheet position (reading
order, left to right in bands). Re-run after editing a sheet:

    python3 _scripts/cut_ringworld_sprites.py

Requires pillow, numpy, scipy. Output is committed, so this only needs running
when the source art changes.
"""

import os

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets/img/ringworld/source")
OUT = os.path.join(ROOT, "assets/img/ringworld/sprites")

SHEETS = {"a": "sprite-sheet-1.png", "b": "sprite-sheet-2.png"}

NAMES = {
    "a01": "saturn-peach",   "a02": "ringworld",     "a03": "star-big",
    "a04": "star-trail",     "a05": "rocket",        "a06": "ufo-blue",
    "a07": "astronaut",      "a08": "crystal",       "a09": "cloud-mint",
    "a10": "frog",           "a11": "star-folded",   "a12": "cloud-blue",
    "a13": "rock-grey",      "a14": "blob-peach",    "a15": "blob-lilac",
    "b01": "saturn-purple",  "b02": "saturn-orange", "b03": "moon",
    "b04": "stars-twin",     "b05": "ufo-alien",     "b06": "comet-peach",
    "b07": "star-ringed",    "b08": "constellation", "b09": "ufo-eye",
    "b10": "blob-blue",      "b11": "jellyfish",     "b12": "blob-green",
    "b13": "comet",          "b14": "ufo-bear",      "b15": "alien-green",
    "b16": "cloud-purple",
}

DILATE = 13      # px: bridges a character to its sparkles, not to its neighbour
MIN_AREA = 2600  # drop lone specks
PAD = 6
MAX_EDGE = 220   # exported sprites are decorative; 220px covers 2x at any use


def cut(tag, path):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im).astype(np.int16)
    rgb, alpha = a[..., :3], a[..., 3]

    # ink = anything meaningfully darker or more saturated than the white ground
    lum = rgb.mean(axis=2)
    sat = rgb.max(axis=2) - rgb.min(axis=2)
    ink = ((lum < 244) | (sat > 12)) & (alpha > 20)

    lab, _ = ndimage.label(ndimage.binary_dilation(ink, np.ones((DILATE, DILATE), bool)))

    boxes = []
    for i, sl in enumerate(ndimage.find_objects(lab), start=1):
        if sl is None:
            continue
        blob = (lab[sl] == i) & ink[sl]
        if blob.sum() < MIN_AREA:
            continue
        ys, xs = np.nonzero(blob)
        y0, x0 = max(0, sl[0].start + ys.min() - PAD), max(0, sl[1].start + xs.min() - PAD)
        y1 = min(a.shape[0], sl[0].start + ys.max() + 1 + PAD)
        x1 = min(a.shape[1], sl[1].start + xs.max() + 1 + PAD)
        boxes.append((y0, x0, y1, x1))

    boxes.sort(key=lambda b: (b[0] // 140, b[1]))  # reading order, in bands

    written = []
    for idx, (y0, x0, y1, x1) in enumerate(boxes, start=1):
        key = f"{tag}{idx:02d}"
        name = NAMES.get(key, key)
        crop = np.asarray(im.crop((x0, y0, x1, y1))).astype(np.int16).copy()
        c_lum = crop[..., :3].mean(axis=2)
        c_sat = crop[..., :3].max(axis=2) - crop[..., :3].min(axis=2)
        # ramp white out rather than cutting it, so watercolour edges stay soft
        soft = np.maximum(
            np.clip((250 - c_lum) * 8, 0, 255),
            np.clip((c_sat - 6) * 14, 0, 255),
        )
        crop[..., 3] = np.minimum(crop[..., 3], soft)

        out = Image.fromarray(crop.astype(np.uint8))
        out.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
        out.quantize(colors=128, method=Image.FASTOCTREE).save(
            os.path.join(OUT, f"{name}.png"), optimize=True
        )
        written.append((key, name, out.size))
    return written


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for tag, fname in SHEETS.items():
        for key, name, size in cut(tag, os.path.join(SRC, fname)):
            print(f"{key} -> {name:16s} {size[0]}x{size[1]}")
