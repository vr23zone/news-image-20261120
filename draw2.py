#!/usr/bin/env python3
"""draw2.py — v2 of "One Day, One Orbit": Friday 20 November 2026 in one image.

Redesign of draw.py (v1) as a classic broadsheet front page, after studying
the provisional top entries of news-image-20261120: a serif masthead, a stat
strip, a continent tally bar, three large illustrated lead stories, ten
smaller illustrated features, a pinned world map and a dense numbered briefs
column — while keeping v1's exact 37 verified stories (imported from
draw.py: 12 featured + 25 wire; the Tbilisi wire story is promoted to drawn
feature 13, leaving 24 briefs). 8 continents: Africa, Antarctica, Asia,
Europe, North America, Oceania, South America, Zealandia.

Deterministic: fixed layout, fixed fonts, seeded noise only. Rendered at
2x (2048x2048) and downscaled to 1024x1024. Run twice -> identical bytes.
Output: entry.png, 1024x1024, <= 1 MiB.

No recognisable face of a real person is drawn anywhere: every illustration
is a generic scene of places, weather, objects and symbols, never a likeness.
"""

import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from draw import STORIES, WIRE  # v1's verified story data, unchanged

SS = 2  # supersampling factor
W, H = 1024, 1024
OUT = "entry.png"

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"

PAPER = (246, 241, 231)
PANEL = (253, 251, 245)
INK = (22, 24, 28)
MUTED = (96, 94, 88)
FAINT = (203, 196, 178)
RED = (178, 32, 44)
NAVY = (13, 34, 64)
SAND = (224, 207, 165)
GOLD = (190, 142, 40)
WHITE = (255, 255, 255)

CONTINENT_COLORS = {
    "AFRICA": (176, 92, 20),
    "ANTARCTICA": (46, 134, 193),
    "ASIA": (178, 34, 52),
    "EUROPE": (36, 90, 166),
    "NORTH AMERICA": (20, 120, 90),
    "OCEANIA": (0, 130, 150),
    "SOUTH AMERICA": (34, 139, 60),
    "ZEALANDIA": (104, 74, 160),
}
# v1 story tuples use "NORTH AMERICA" etc. as keys already.


def X(v):
    """Scale a 1024-space coordinate to render space."""
    return int(round(v * SS))


def font(path, size):
    return ImageFont.truetype(path, max(4, X(size)))


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_font(d, text, path, start_size, max_w, min_size=8):
    """Largest font size <= start_size whose text fits max_w (1024 units)."""
    size = start_size
    while size > min_size and d.textlength(text, font=font(path, size)) > X(max_w):
        size -= 0.5
    return font(path, size)


def text_c(d, cx, y, text, fnt, fill):
    """Draw text centred on cx (1024 units)."""
    w = d.textlength(text, font=fnt)
    d.text((X(cx) - w / 2, X(y)), text, font=fnt, fill=fill)


def text_r(d, rx, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text((X(rx) - w, X(y)), text, font=fnt, fill=fill)


def block(d, x, y, lines, fnt, fill, leading):
    for line in lines:
        d.text((X(x), X(y)), line, font=fnt, fill=fill)
        y += leading
    return y


def vgrad(img, box, top, bottom):
    """Vertical gradient fill of box (render px) on img."""
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    d = ImageDraw.Draw(img)
    for i in range(h):
        t = i / h
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        d.line([x0, y0 + i, x1, y0 + i], fill=col)


def scene_canvas(w, h):
    """A fresh RGB sub-image of w x h (1024 units) plus its draw object."""
    img = Image.new("RGB", (X(w), X(h)), PAPER)
    return img, ImageDraw.Draw(img, "RGBA")


def stars(d, box, n, seed, ymax_frac=0.7):
    """Deterministic star field inside box (render px)."""
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    for _ in range(n):
        sx = rng.uniform(x0, x1)
        sy = rng.uniform(y0, y0 + (y1 - y0) * ymax_frac)
        r = rng.uniform(0.8, 1.9)
        a = rng.randint(90, 220)
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 246, 214, a))


def chip_label(d, x, y, text, fill, tcol=WHITE, size=9.5):
    """Small filled label chip with bold sans text, top-left at x, y."""
    f = font(SANS_B, size)
    tw = d.textlength(text, font=f)
    d.rectangle([X(x), X(y), X(x) + tw + X(10), X(y + 15)],
                fill=fill)
    d.text((X(x) + X(5), X(y + 2.2)), text, font=f, fill=tcol)
    return x + (tw / SS) + 10


# ------------------------------------------------------------------ scenes
# Each scene draws into a sub-image of w x h (1024 units). Generic places,
# weather and objects only — never a person.

def sc_cyclone(img, d, w, h):
    """Cyclone spiral over a Bay of Bengal coastline."""
    vgrad(img, (0, 0, X(w), X(h)), (16, 62, 96), (38, 108, 138))
    # Coastline: sand landmass on the left, curving bay.
    land = [(0, 0), (0.42 * w, 0), (0.34 * w, 0.18 * h), (0.40 * w, 0.38 * h),
            (0.30 * w, 0.58 * h), (0.36 * w, 0.80 * h), (0.28 * w, h),
            (0, h)]
    d.polygon([(X(a), X(b)) for a, b in land], fill=(216, 196, 148))
    d.line([(X(a), X(b)) for a, b in land[1:-1]], fill=(240, 228, 190), width=X(2))
    # Spiral: logarithmic spiral arms around the eye.
    cx, cy = 0.62 * w, 0.52 * h
    for arm in range(3):
        pts = []
        for t in range(0, 101):
            th = arm * (2 * math.pi / 3) + t * 0.055
            r = 3 + t * 0.62
            pts.append((X(cx + r * math.cos(th) * 1.25), X(cy + r * math.sin(th) * 0.78)))
        d.line(pts, fill=(240, 248, 250), width=X(3.2))
    d.ellipse([X(cx - 7), X(cy - 5), X(cx + 7), X(cy + 5)], fill=(16, 62, 96))
    d.ellipse([X(cx - 7), X(cy - 5), X(cx + 7), X(cy + 5)], outline=WHITE, width=X(1.6))
    # Rain streaks bottom right.
    rng = random.Random(7)
    for _ in range(26):
        sx = rng.uniform(0.55 * w, w - 6)
        sy = rng.uniform(0.55 * h, h - 8)
        d.line([X(sx), X(sy), X(sx - 5), X(sy + 7)], fill=(190, 220, 235), width=X(1.2))
    d.text((X(10), X(8)), "ODISHA", font=font(SANS_B, 10), fill=(70, 60, 40))
    d.text((X(10), X(21)), "INDIA", font=font(SANS, 8.5), fill=(70, 60, 40))
    text_r(d, w - 8, h - 15, "BAY OF BENGAL", font(SANS_B, 8.5), (200, 226, 238))
    chip_label(d, 8, h - 19, "LANDFALL · GUSTS 110 KM/H", RED)


def sc_kyiv(img, d, w, h):
    """Ballistic missile streaks over a night skyline and power plant."""
    vgrad(img, (0, 0, X(w), X(h)), (7, 12, 34), (26, 34, 66))
    stars(d, (0, 0, X(w), X(h)), 46, 11)
    # Missile arcs: bright cores with soft glow.
    arcs = [((0.06, 0.06), (0.34, 0.52)), ((0.30, 0.02), (0.52, 0.58)),
            ((0.55, 0.05), (0.70, 0.60)), ((0.78, 0.03), (0.86, 0.55)),
            ((0.16, 0.16), (0.42, 0.60)), ((0.66, 0.14), (0.78, 0.58))]
    for (ax, ay), (bx, by) in arcs:
        pts = []
        for t in range(21):
            u = t / 20
            px = (1 - u) * ax * w + u * bx * w
            py = (1 - u) * ay * h + u * by * h - math.sin(u * math.pi) * 0.10 * h
            pts.append((X(px), X(py)))
        d.line(pts, fill=(255, 120, 40, 90), width=X(4.5))
        d.line(pts, fill=(255, 196, 92), width=X(1.8))
        ex, ey = pts[-1]
        d.ellipse([ex - X(2.6), ey - X(2.6), ex + X(2.6), ey + X(2.6)], fill=(255, 224, 150))
    # Skyline silhouette.
    base = h
    blocks = [(0, 0.30), (0.07, 0.42), (0.13, 0.34), (0.20, 0.46), (0.27, 0.36),
              (0.33, 0.30), (0.72, 0.34), (0.79, 0.44), (0.86, 0.33), (0.93, 0.40)]
    for bx, bh in blocks:
        d.rectangle([X(bx * w), X(base - bh * h), X(bx * w + 0.055 * w), X(base)],
                    fill=(5, 8, 18))
    # Power plant: block + two chimneys centre-right of skyline.
    d.rectangle([X(0.44 * w), X(0.66 * h), X(0.66 * w), X(base)], fill=(5, 8, 18))
    for chx in (0.50, 0.585):
        d.rectangle([X(chx * w), X(0.34 * h), X(chx * w + 0.028 * w), X(0.68 * h)],
                    fill=(5, 8, 18))
        d.rectangle([X(chx * w - 0.004 * w), X(0.32 * h), X(chx * w + 0.032 * w), X(0.36 * h)],
                    fill=(5, 8, 18))
    # Fire glow at plant base + burst.
    for r, a in ((16, 60), (10, 110), (5.5, 180)):
        d.ellipse([X(0.55 * w - r), X(0.97 * h - r), X(0.55 * w + r), X(0.97 * h + r)],
                  fill=(255, 130, 40, a))
    bx, by = 0.55 * w, 0.60 * h
    for ang in range(0, 360, 30):
        ex = bx + 11 * math.cos(math.radians(ang))
        ey = by + 8 * math.sin(math.radians(ang))
        d.line([X(bx), X(by), X(ex), X(ey)], fill=(255, 170, 60), width=X(1.6))
    chip_label(d, 8, 8, "BALLISTIC STRIKES · OVERNIGHT", RED)
    text_r(d, w - 8, h - 15, "POWER PLANT HIT", font(SANS_B, 8.5), (214, 222, 240))


def sc_cop31(img, d, w, h):
    """Globe with melting ice cap and a rising thermometer: COP31 final day."""
    vgrad(img, (0, 0, X(w), X(h)), (18, 84, 92), (30, 122, 128))
    # Sun disc top-right behind thermometer.
    d.ellipse([X(0.80 * w), X(0.06 * h), X(0.97 * w), X(0.55 * h)], fill=(244, 178, 66))
    # Globe.
    gx, gy, gr = 0.36 * w, 0.58 * h, 0.37 * h
    d.ellipse([X(gx - gr), X(gy - gr), X(gx + gr), X(gy + gr)], fill=(58, 130, 190))
    # Land blobs, kept inside the disc (offsets in globe radii).
    for (ox, oy, rw, rh) in ((-0.38, -0.18, 0.30, 0.17), (0.28, -0.02, 0.26, 0.15),
                             (-0.12, 0.34, 0.30, 0.16), (0.40, 0.44, 0.20, 0.12),
                             (-0.48, 0.22, 0.20, 0.12)):
        d.ellipse([X(gx + (ox - rw) * gr), X(gy + (oy - rh) * gr),
                   X(gx + (ox + rw) * gr), X(gy + (oy + rh) * gr)], fill=(74, 160, 92))
    # Latitude arcs.
    for oy in (-0.05, 0.38):
        d.arc([X(gx - gr), X(gy + oy * gr - 0.42 * gr), X(gx + gr), X(gy + oy * gr + 0.42 * gr)],
              20, 160, fill=(120, 180, 220), width=X(1.1))
    # Ice cap: top arc of the disc with a jagged melting lower edge.
    cap = []
    for a in range(180, 361, 12):
        cap.append((gx + gr * math.cos(math.radians(a)), gy + gr * math.sin(math.radians(a))))
    for i, a in enumerate(range(348, 179, -14)):
        rr = gr * (0.80 if i % 2 == 0 else 0.90)
        cap.append((gx + rr * math.cos(math.radians(a)), gy + rr * math.sin(math.radians(a))))
    d.polygon([(X(a), X(b)) for a, b in cap], fill=(238, 246, 250))
    # Drips below the cap edge.
    for dx in (-0.42, 0.08, 0.48):
        d.polygon([(X(gx + dx * gr - 2), X(gy - gr * 0.80)), (X(gx + dx * gr + 2), X(gy - gr * 0.80)),
                   (X(gx + dx * gr), X(gy - gr * 0.58))], fill=(238, 246, 250))
    # Thermometer.
    tx = 0.665 * w
    d.rounded_rectangle([X(tx), X(0.14 * h), X(tx + 0.045 * w), X(0.78 * h)],
                        radius=X(6), fill=(240, 244, 246), outline=(180, 190, 196), width=X(1))
    d.rectangle([X(tx + 0.014 * w), X(0.30 * h), X(tx + 0.031 * w), X(0.78 * h)], fill=RED)
    d.ellipse([X(tx - 0.016 * w), X(0.70 * h), X(tx + 0.061 * w), X(0.94 * h)], fill=RED)
    for i in range(4):
        ty = 0.24 * h + i * 0.12 * h
        d.line([X(tx + 0.05 * w), X(ty), X(tx + 0.075 * w), X(ty)], fill=WHITE, width=X(1.4))
    d.text((X(0.10 * w), X(0.08 * h)), "ANTALYA · NOV 20", font=font(SANS_B, 9.5), fill=WHITE)
    chip_label(d, 8, h - 19, "COP31 · FINAL DAY", RED)
    text_r(d, w - 8, h - 15, "TEXT DUE AT MIDNIGHT", font(SANS_B, 8.5), (216, 238, 240))


def sc_markets(img, d, w, h):
    """Falling red chart on a dark exchange screen."""
    d.rectangle([0, 0, X(w), X(h)], fill=(14, 18, 30))
    for gx in range(1, 8):
        d.line([X(gx * w / 8), 0, X(gx * w / 8), X(h)], fill=(38, 46, 66), width=1)
    for gy in range(1, 3):
        d.line([0, X(gy * h / 3), X(w), X(gy * h / 3)], fill=(38, 46, 66), width=1)
    pts = [(0.03, 0.44), (0.16, 0.49), (0.28, 0.45), (0.40, 0.56), (0.52, 0.53),
           (0.64, 0.66), (0.76, 0.72), (0.88, 0.83), (0.97, 0.90)]
    xy = [(X(a * w), X(b * h)) for a, b in pts]
    d.polygon(xy + [(X(w), X(h)), (0, X(h))], fill=(178, 32, 44, 70))
    d.line(xy, fill=(255, 84, 84), width=X(2.4))
    ex, ey = xy[-1]
    d.polygon([(ex, ey), (ex - X(9), ey - X(2)), (ex - X(3), ey + X(7))], fill=(255, 84, 84))
    d.text((X(8), X(5)), "ASIA -7% WK", font=font(SANS_B, 9), fill=(255, 120, 120))
    text_r(d, w - 7, 5, "NIKKEI -4.1%", font(SANS_B, 9), (240, 240, 240))


def sc_houthi(img, d, w, h):
    """Missile arc toward a tall tower at dusk."""
    vgrad(img, (0, 0, X(w), X(h)), (64, 40, 78), (196, 96, 62))
    # Tower silhouette (tapered, with spire) right of centre.
    tx = 0.60 * w
    d.polygon([(X(tx), X(h)), (X(tx + 3), X(0.22 * h)), (X(tx + 7), X(0.22 * h)),
               (X(tx + 10), X(h))], fill=(16, 14, 26))
    d.line([X(tx + 5), X(0.22 * h), X(tx + 5), X(0.05 * h)], fill=(16, 14, 26), width=X(1.6))
    d.rectangle([X(0.06 * w), X(0.72 * h), X(0.40 * w), X(h)], fill=(16, 14, 26))
    d.rectangle([X(0.80 * w), X(0.62 * h), X(0.97 * w), X(h)], fill=(16, 14, 26))
    # Missile arc + burst at tower.
    pts = []
    for t in range(21):
        u = t / 20
        pts.append((X((0.05 + 0.55 * u) * w), X((0.75 - 0.62 * u + 0.30 * u * u) * h)))
    d.line(pts, fill=(255, 190, 90), width=X(2.6))
    bx, by = 0.615 * w, 0.30 * h
    for ang in range(0, 360, 45):
        d.line([X(bx), X(by), X(bx + 11 * math.cos(math.radians(ang))),
                X(by + 8 * math.sin(math.radians(ang)))], fill=(255, 170, 60), width=X(1.6))
    d.text((X(8), X(5)), "RIYADH", font=font(SANS_B, 9), fill=(255, 226, 190))


def sc_tanker(img, d, w, h):
    """Tanker silhouette with a flame plume, Strait of Hormuz."""
    vgrad(img, (0, 0, X(w), X(h)), (30, 52, 84), (16, 40, 66))
    d.rectangle([0, X(0.66 * h), X(w), X(h)], fill=(10, 26, 44))
    for i in range(5):
        y = 0.72 * h + i * 0.06 * h
        d.line([X(0.05 * w + (i % 2) * 14), X(y), X(0.35 * w + (i % 2) * 14), X(y)],
               fill=(52, 84, 116), width=X(1.2))
    # Hull + deck + superstructure.
    d.polygon([(X(0.08 * w), X(0.66 * h)), (X(0.92 * w), X(0.66 * h)),
               (X(0.86 * w), X(0.80 * h)), (X(0.14 * w), X(0.80 * h))], fill=(8, 10, 16))
    d.rectangle([X(0.16 * w), X(0.56 * h), X(0.70 * w), X(0.66 * h)], fill=(8, 10, 16))
    d.rectangle([X(0.74 * w), X(0.44 * h), X(0.86 * w), X(0.66 * h)], fill=(8, 10, 16))
    # Flame plume amidships.
    fx, fy = 0.42 * w, 0.56 * h
    for (fw, fh, col) in ((11, 26, (255, 110, 30)), (7.5, 19, (255, 160, 40)), (4.5, 12, (255, 214, 92))):
        d.polygon([(X(fx - fw), X(fy)), (X(fx + fw), X(fy)), (X(fx + fw * 0.3), X(fy - fh * 0.6)),
                   (X(fx), X(fy - fh)), (X(fx - fw * 0.35), X(fy - fh * 0.55))], fill=col)
    for i in range(3):  # smoke
        d.ellipse([X(fx + 6 + i * 9), X(fy - 34 - i * 3), X(fx + 20 + i * 10), X(fy - 22 - i * 3)],
                  fill=(120, 124, 132, 130))
    d.text((X(8), X(5)), "HORMUZ", font=font(SANS_B, 9), fill=(210, 226, 240))


def sc_genoa(img, d, w, h):
    """Airliner held on a runway while drones cross the sky."""
    vgrad(img, (0, 0, X(w), X(h)), (96, 148, 196), (168, 200, 228))
    d.rectangle([0, X(0.78 * h), X(w), X(h)], fill=(70, 76, 84))
    for i in range(6):
        d.line([X(0.06 * w + i * 0.17 * w), X(0.885 * h), X(0.12 * w + i * 0.17 * w), X(0.885 * h)],
               fill=(240, 240, 240), width=X(1.6))
    # Plane silhouette, side view, centre-left.
    px, py = 0.10 * w, 0.60 * h
    d.polygon([(X(px), X(py)), (X(px + 0.34 * w), X(py - 0.02 * h)), (X(px + 0.40 * w), X(py + 0.05 * h)),
               (X(px + 0.40 * w), X(py + 0.11 * h)), (X(px + 0.03 * w), X(py + 0.10 * h))], fill=(24, 30, 40))
    d.polygon([(X(px + 0.02 * w), X(py - 0.01 * h)), (X(px - 0.03 * w), X(py - 0.16 * h)),
               (X(px + 0.05 * w), X(py - 0.15 * h)), (X(px + 0.07 * w), X(py))], fill=(24, 30, 40))
    d.polygon([(X(px + 0.16 * w), X(py + 0.06 * h)), (X(px + 0.24 * w), X(py + 0.20 * h)),
               (X(px + 0.29 * w), X(py + 0.20 * h)), (X(px + 0.22 * w), X(py + 0.05 * h))], fill=(24, 30, 40))
    # Two drones with blinking lights.
    for (dx, dy) in ((0.66, 0.16), (0.82, 0.30)):
        cx, cy = dx * w, dy * h
        d.line([X(cx - 9), X(cy - 5), X(cx + 9), X(cy + 5)], fill=(20, 24, 32), width=X(1.6))
        d.line([X(cx - 9), X(cy + 5), X(cx + 9), X(cy - 5)], fill=(20, 24, 32), width=X(1.6))
        d.ellipse([X(cx - 2.4), X(cy - 2.4), X(cx + 2.4), X(cy + 2.4)], fill=RED)
    d.text((X(8), X(5)), "GENOA · FLIGHTS HELD", font=font(SANS_B, 9), fill=(16, 30, 48))


def sc_trump(img, d, w, h):
    """Hourglass beside a 2027 calendar page — no call until 2027."""
    d.rectangle([0, 0, X(w), X(h)], fill=(238, 230, 210))
    # Calendar page right.
    cx = 0.60 * w
    d.rectangle([X(cx), X(0.14 * h), X(cx + 0.34 * w), X(0.90 * h)], fill=WHITE,
                outline=(150, 140, 120), width=X(1))
    d.rectangle([X(cx), X(0.14 * h), X(cx + 0.34 * w), X(0.32 * h)], fill=RED)
    text_c(d, cx + 0.17 * w, 0.40 * h, "2027", font(SERIF_B, 15), INK)
    d.text((X(cx + 0.05 * w), X(0.66 * h)), "JAN 1", font=font(SANS_B, 8.5), fill=MUTED)
    # Hourglass left.
    hx, hy = 0.30 * w, 0.50 * h
    d.polygon([(X(hx - 13), X(hy - 17)), (X(hx + 13), X(hy - 17)), (X(hx), X(hy))], fill=(120, 96, 52))
    d.polygon([(X(hx - 13), X(hy + 17)), (X(hx + 13), X(hy + 17)), (X(hx), X(hy))], outline=(120, 96, 52), width=X(1.6))
    d.polygon([(X(hx - 4), X(hy + 16)), (X(hx + 4), X(hy + 16)), (X(hx), X(hy + 5))], fill=(212, 160, 32))
    d.line([X(hx - 16), X(hy - 19), X(hx + 16), X(hy - 19)], fill=(90, 72, 40), width=X(2.4))
    d.line([X(hx - 16), X(hy + 19), X(hx + 16), X(hy + 19)], fill=(90, 72, 40), width=X(2.4))
    d.text((X(8), X(5)), "IRAN", font=font(SANS_B, 9), fill=(110, 60, 30))


def sc_tesla(img, d, w, h):
    """Electric car in profile over Argentina's sky-blue bands."""
    d.rectangle([0, 0, X(w), X(0.36 * h)], fill=(116, 172, 223))
    d.rectangle([0, X(0.36 * h), X(w), X(0.66 * h)], fill=(245, 246, 244))
    d.rectangle([0, X(0.66 * h), X(w), X(h)], fill=(116, 172, 223))
    d.ellipse([X(0.465 * w), X(0.40 * h), X(0.535 * w), X(0.62 * h)], fill=(250, 190, 60))
    # Car silhouette.
    cy = 0.60 * h
    d.polygon([(X(0.16 * w), X(cy + 8)), (X(0.20 * w), X(cy - 2)), (X(0.34 * w), X(cy - 4)),
               (X(0.44 * w), X(cy - 13)), (X(0.62 * w), X(cy - 13)), (X(0.74 * w), X(cy - 3)),
               (X(0.84 * w), X(cy + 1)), (X(0.85 * w), X(cy + 8))], fill=(18, 22, 30))
    d.rectangle([X(0.16 * w), X(cy + 7), X(0.85 * w), X(cy + 11)], fill=(18, 22, 30))
    for wx in (0.30, 0.70):
        d.ellipse([X(wx * w - 7), X(cy + 6), X(wx * w + 7), X(cy + 20)], fill=(10, 12, 16))
        d.ellipse([X(wx * w - 3), X(cy + 10), X(wx * w + 3), X(cy + 16)], fill=(150, 156, 164))
    d.polygon([(X(0.47 * w), X(cy - 11)), (X(0.60 * w), X(cy - 11)), (X(0.63 * w), X(cy - 4)),
               (X(0.46 * w), X(cy - 4))], fill=(168, 206, 232))
    d.text((X(8), X(4)), "BUENOS AIRES", font=font(SANS_B, 9), fill=(16, 40, 66))


def sc_turtle(img, d, w, h):
    """A small sea turtle over sand and shallows."""
    vgrad(img, (0, 0, X(w), X(h)), (168, 216, 208), (226, 214, 168))
    cx, cy = 0.46 * w, 0.52 * h
    for (fx, fy, ang) in ((0.30, 0.30, -30), (0.62, 0.30, 30), (0.31, 0.74, 30), (0.61, 0.74, -30)):
        d.ellipse([X(fx * w - 10), X(fy * h - 5), X(fx * w + 10), X(fy * h + 5)], fill=(52, 110, 84))
    d.ellipse([X(cx - 24), X(cy - 13), X(cx + 24), X(cy + 13)], fill=(64, 128, 92))
    d.ellipse([X(cx - 18), X(cy - 9), X(cx + 18), X(cy + 9)], outline=(34, 84, 58), width=X(1.6))
    d.ellipse([X(cx - 7), X(cy - 5), X(cx + 7), X(cy + 5)], outline=(34, 84, 58), width=X(1.2))
    d.ellipse([X(cx + 24), X(cy - 5), X(cx + 33), X(cy + 5)], fill=(64, 128, 92))
    d.ellipse([X(cx + 29.5), X(cy - 1.6), X(cx + 31.5), X(cy + 0.4)], fill=(16, 30, 22))
    for i in range(4):  # sea grass
        gx = 0.08 * w + i * 0.055 * w
        d.arc([X(gx), X(0.55 * h), X(gx + 12), X(1.05 * h)], 90, 200, fill=(44, 120, 80), width=X(1.6))
    for (bx, by, br) in ((0.78, 0.30, 2.6), (0.84, 0.20, 1.8), (0.74, 0.16, 1.4)):
        d.ellipse([X(bx * w - br), X(by * h - br), X(bx * w + br), X(by * h + br)],
                  outline=(255, 255, 255), width=X(1))
    d.text((X(8), X(4)), "PERTH", font=font(SANS_B, 9), fill=(24, 70, 60))


def sc_nz(img, d, w, h):
    """A sailboat adrift, its rudder floating loose beside it."""
    vgrad(img, (0, 0, X(w), X(h)), (140, 190, 220), (90, 140, 180))
    d.rectangle([0, X(0.68 * h), X(w), X(h)], fill=(40, 96, 140))
    for i in range(4):
        y = 0.76 * h + i * 0.07 * h
        d.arc([X(0.06 * w + i * 22), X(y - 4), X(0.30 * w + i * 22), X(y + 5)], 180, 330,
              fill=(150, 200, 230), width=X(1.2))
    bx, by = 0.40 * w, 0.66 * h
    d.polygon([(X(bx - 22), X(by)), (X(bx + 22), X(by)), (X(bx + 15), X(by + 7)), (X(bx - 15), X(by + 7))],
              fill=(120, 62, 30))
    d.line([X(bx), X(by), X(bx), X(by - 26)], fill=(60, 44, 30), width=X(2))
    d.polygon([(X(bx + 2), X(by - 26)), (X(bx + 2), X(by - 3)), (X(bx + 17), X(by - 3))], fill=(246, 244, 238))
    d.polygon([(X(bx - 2), X(by - 22)), (X(bx - 2), X(by - 3)), (X(bx - 13), X(by - 3))], fill=(226, 220, 204))
    # Loose rudder + dashed drift path.
    d.polygon([(X(0.70 * w), X(0.60 * h)), (X(0.76 * w), X(0.62 * h)), (X(0.74 * w), X(0.78 * h)),
               (X(0.69 * w), X(0.74 * h))], fill=(150, 40, 40))
    for t in range(6):
        u = t / 5
        d.ellipse([X((0.52 + 0.15 * u) * w), X((0.52 + 0.06 * u) * h),
                   X((0.52 + 0.15 * u) * w + 2.4), X((0.52 + 0.06 * u) * h + 2.4)], fill=(240, 240, 230))
    d.text((X(8), X(4)), "CARBON MARKET ADRIFT", font=font(SANS_B, 9), fill=(18, 44, 66))


def sc_antarctica(img, d, w, h):
    """Icebergs and a crack across the sea ice."""
    vgrad(img, (0, 0, X(w), X(h)), (196, 224, 240), (232, 242, 248))
    d.rectangle([0, X(0.62 * h), X(w), X(h)], fill=(120, 178, 214))
    bergs = [(0.06, 0.30, 0.30, 0.62), (0.58, 0.22, 0.86, 0.62), (0.84, 0.38, 0.99, 0.62)]
    for (ax, ay, bx2, by2) in bergs:
        d.polygon([(X(ax * w), X(by2 * h)), (X(ax * w + 6), X(ay * h + 8)), (X((ax + bx2) / 2 * w), X(ay * h)),
                   (X(bx2 * w - 5), X(ay * h + 10)), (X(bx2 * w), X(by2 * h))], fill=(246, 250, 252))
        d.polygon([(X((ax + bx2) / 2 * w), X(ay * h)), (X(bx2 * w - 5), X(ay * h + 10)),
                   (X(bx2 * w), X(by2 * h)), (X((ax + bx2) / 2 * w + 6), X(by2 * h))], fill=(206, 228, 240))
    # Crack across the ice shelf foreground.
    d.rectangle([0, X(0.80 * h), X(w), X(h)], fill=(240, 247, 250))
    crack = [(0, 0.88), (0.2, 0.85), (0.38, 0.90), (0.55, 0.86), (0.72, 0.91), (0.88, 0.87), (1.0, 0.90)]
    d.line([(X(a * w), X(b * h)) for a, b in crack], fill=(30, 90, 140), width=X(2))
    # Penguin silhouette.
    px, py = 0.90 * w, 0.70 * h
    d.ellipse([X(px - 4.5), X(py - 9), X(px + 4.5), X(py + 9)], fill=(18, 22, 28))
    d.ellipse([X(px - 2.4), X(py - 2), X(px + 2.4), X(py + 7)], fill=WHITE)
    d.polygon([(X(px + 4), X(py - 6)), (X(px + 7), X(py - 4.6)), (X(px + 4), X(py - 3.4))], fill=(240, 150, 40))
    d.text((X(8), X(4)), "THE ICE SHEET", font=font(SANS_B, 9), fill=(30, 80, 120))


def sc_tbilisi(img, d, w, h):
    """Damaged block at night, a rescue light sweeping the rubble."""
    vgrad(img, (0, 0, X(w), X(h)), (18, 22, 44), (44, 48, 78))
    stars(d, (0, 0, X(w), X(h)), 16, 5)
    # Searchlight cone from left.
    d.polygon([(X(0.03 * w), X(0.96 * h)), (X(0.62 * w), X(0.30 * h)), (X(0.70 * w), X(0.52 * h))],
              fill=(255, 240, 180, 52))
    # Damaged building right: tilted top corner, cracked wall.
    bx = 0.60 * w
    d.rectangle([X(bx), X(0.24 * h), X(0.97 * w), X(0.92 * h)], fill=(10, 12, 22))
    d.polygon([(X(bx), X(0.24 * h)), (X(0.97 * w), X(0.24 * h)), (X(0.90 * w), X(0.40 * h)),
               (X(bx), X(0.44 * h))], fill=(24, 28, 46))
    for r in range(3):
        for c in range(3):
            if (r * 3 + c) % 3 != 2:
                d.rectangle([X(bx + 6 + c * 0.115 * w), X(0.34 * h + r * 0.17 * h),
                             X(bx + 15 + c * 0.115 * w), X(0.44 * h + r * 0.17 * h)],
                            fill=(255, 196, 92))
    d.line([X(bx + 4), X(0.46 * h), X(bx + 14), X(0.62 * h), X(bx + 7), X(0.78 * h)],
           fill=(120, 130, 160), width=X(1.2))
    # Rubble pile.
    d.polygon([(X(0.30 * w), X(0.94 * h)), (X(0.48 * w), X(0.62 * h)), (X(0.66 * w), X(0.94 * h))],
              fill=(52, 54, 68))
    d.polygon([(X(0.40 * w), X(0.94 * h)), (X(0.52 * w), X(0.74 * h)), (X(0.62 * w), X(0.94 * h))],
              fill=(66, 68, 84))
    d.rectangle([X(0.02 * w), X(0.90 * h), X(0.10 * w), X(0.97 * h)], fill=(10, 12, 22))
    d.ellipse([X(0.035 * w), X(0.86 * h), X(0.085 * w), X(0.93 * h)], fill=(255, 240, 180))
    d.text((X(8), X(4)), "TBILISI · NIGHT RESCUE", font=font(SANS_B, 9), fill=(220, 226, 244))


# ------------------------------------------------------------------- data
# Story tuples from draw.py: (continent, glyph, headline, detail, source).
TBILISI = ("EUROPE", "", "Girl, 3, pulled from rubble 8 hours after Tbilisi gas blast",
           "Pulled out alive, eight hours after a gas blast.", "Daily Baku")

LEADS = [
    (1, STORIES[0], "GOPALPUR, INDIA · CYCLONE", sc_cyclone),
    (2, STORIES[4], "KYIV, UKRAINE · WAR", sc_kyiv),
    (3, STORIES[1], "ANTALYA, TÜRKİYE · CLIMATE", sc_cop31),
]
FEATURES = [
    (4, STORIES[3], "TOKYO–SEOUL · MARKETS", sc_markets),
    (5, STORIES[5], "RIYADH · MISSILES", sc_houthi),
    (6, STORIES[6], "STRAIT OF HORMUZ · ENERGY", sc_tanker),
    (7, STORIES[7], "GENOA · AVIATION", sc_genoa),
    (8, STORIES[2], "WASHINGTON · POLITICS", sc_trump),
    (9, STORIES[8], "ARGENTINA · BUSINESS", sc_tesla),
    (10, STORIES[9], "PERTH · NATURE", sc_turtle),
    (11, STORIES[10], "NEW ZEALAND · CLIMATE", sc_nz),
    (12, STORIES[11], "ANTARCTICA · SCIENCE", sc_antarctica),
    (13, TBILISI, "TBILISI · RESCUE", sc_tbilisi),
]

# Briefs: the 24 remaining wire stories (Tbilisi promoted to feature 13),
# in v1 wire order, numbered 14-37. Place lead-ins added; facts unchanged.
BRIEFS = [
    (14, "SHENZHEN", "Trump, Xi and Putin issue peace declaration (*)"),
    (15, "NEW YORK", "Anthropic closes 17% up on Nasdaq debut, $1.76tn (*)"),
    (16, "NEW YORK", "Wall St: S&P -2.0%, Dow -1,101, fifth straight loss (*)"),
    (17, "BRUSSELS", "Europe says it is ready for talks with Russia"),
    (18, "PARIS", "Kamala Harris meets Macron amid 2028 speculation"),
    (19, "THE HAGUE", "Dutch summon envoy after blast near Kyiv embassy"),
    (20, "LEBANON", "Israeli strike hits Hezbollah missile site in east"),
    (21, "RUSSIA", "Three killed in drone attack on Saratov region"),
    (22, "FRANCE", "One dead, 15 hurt in fire at 18-storey block"),
    (23, "LONDON", "EU–UK talks ‘going down to the wire’, says No 10"),
    (24, "CALIFORNIA", "State probes Nvidia over China AI chip sales"),
    (25, "WASHINGTON", "White House names Kirsten Davies as cyber chief"),
    (26, "TAIPEI", "Taiwan acts to steady stocks; short-selling curbs"),
    (27, "TOKYO", "Takaichi sidesteps Taiwan contingency question"),
    (28, "INDIA", "Judge: resignation is no admission of guilt"),
    (29, "BHOPAL", "Madhya Pradesh scraps two-child rule for staff"),
    (30, "BRASILIA", "Chief Raoni’s Kayapo homeland made permanent (*)"),
    (31, "GENEVA", "Brazil asks WTO for panel against US tariffs (*)"),
    (32, "CARACAS", "US and Venezuela sign deal to restore military ties"),
    (33, "BOGOTA", "US backs Colombia plan to resume coca spraying"),
    (34, "MEXICO CITY", "Christie’s halts Frida Kahlo sale at govt request"),
    (35, "HAITI", "Heavy fighting as forces battle gangs"),
    (36, "AFRICA", "Climate cash? Europe: use pledged money first"),
    (37, "FOOTBALL", "U-17 World Cup: Brazil open against Ireland"),
]

STATS = [
    ("70–80 km/h", "Akvan’s winds at Odisha landfall"),
    ("−4.7%", "Kospi: Asia’s worst week since 2020"),
    ("~200", "nations at COP31’s final day"),
    ("4", "Saudi targets hit by Houthis"),
    ("8 hours", "a Tbilisi girl, 3, spent in rubble"),
    ("15 hurt", "1 dead in France 18-storey fire"),
]

# ------------------------------------------------------------- world map
# Rough equirectangular continent outlines (lon, lat), drawn small.
LAND = [
    [(-165, 68), (-140, 70), (-130, 71), (-115, 72), (-100, 73), (-90, 79), (-85, 76),
     (-82, 70), (-78, 62), (-70, 62), (-60, 55), (-55, 52), (-60, 46), (-66, 45),
     (-70, 42), (-74, 40), (-76, 36), (-79, 33), (-80, 30), (-81, 25), (-84, 28),
     (-87, 21), (-90, 20), (-94, 17), (-97, 16), (-100, 18), (-105, 22), (-108, 25),
     (-112, 29), (-117, 33), (-121, 35), (-124, 42), (-124, 47), (-130, 53),
     (-135, 57), (-150, 59), (-158, 56), (-165, 60)],
    [(-46, 60), (-38, 62), (-30, 66), (-22, 70), (-20, 74), (-25, 78), (-35, 80),
     (-52, 77), (-56, 70), (-54, 63)],
    [(-78, 7), (-76, 10), (-72, 12), (-66, 11), (-61, 9), (-55, 6), (-51, 3),
     (-50, 0), (-44, -3), (-37, -6), (-35, -8), (-37, -11), (-39, -14), (-40, -20),
     (-42, -23), (-46, -25), (-50, -30), (-54, -34), (-58, -38), (-60, -40),
     (-63, -42), (-65, -46), (-66, -50), (-68, -53), (-69, -55), (-71, -54),
     (-72, -50), (-73, -44), (-74, -38), (-73, -32), (-71, -27), (-70, -20),
     (-70, -18), (-73, -16), (-76, -14), (-79, -8), (-80, -5), (-81, -2), (-80, 2)],
    [(-9, 37), (-9, 44), (-2, 44), (-1, 46), (-5, 48), (-2, 50), (0, 51), (3, 53),
     (6, 54), (8, 55), (8, 57), (10, 58), (18, 56), (20, 55), (23, 56), (21, 60),
     (23, 63), (25, 66), (28, 69), (35, 68), (45, 67), (55, 68), (66, 70), (75, 72),
     (88, 73), (103, 77), (115, 76), (128, 73), (142, 72), (155, 71), (169, 70),
     (178, 67), (178, 65), (172, 62), (162, 59), (157, 52), (150, 50), (142, 49),
     (141, 44), (138, 36), (135, 34), (130, 32), (124, 30), (121, 26), (119, 24),
     (112, 22), (109, 19), (108, 13), (107, 9), (104, 6), (101, 6), (99, 8),
     (98, 11), (97, 15), (95, 16), (93, 18), (91, 22), (89, 22), (87, 21), (85, 20),
     (82, 16), (80, 13), (78, 9), (76, 10), (73, 16), (72, 20), (70, 21), (67, 24),
     (63, 25), (59, 25), (56, 26), (53, 26), (51, 28), (49, 29), (48, 30), (50, 28),
     (52, 26), (55, 25), (57, 24), (59, 23), (58, 21), (55, 17), (52, 15), (48, 13),
     (44, 12), (43, 12), (41, 15), (39, 20), (36, 24), (35, 28), (34, 29), (36, 31),
     (36, 36), (33, 36), (30, 36), (27, 37), (24, 38), (22, 37), (19, 40), (16, 39),
     (14, 41), (12, 44), (10, 44), (8, 44), (6, 43), (3, 42), (0, 39), (-2, 37)],
    [(-6, 35), (-9, 32), (-10, 29), (-14, 24), (-17, 20), (-17, 15), (-16, 12),
     (-13, 9), (-8, 5), (-4, 5), (2, 6), (6, 4), (9, 4), (9, -1), (12, -6),
     (13, -12), (13, -17), (14, -22), (16, -27), (18, -32), (19, -34), (25, -34),
     (28, -33), (31, -29), (33, -26), (35, -23), (36, -19), (37, -15), (39, -10),
     (40, -5), (41, 0), (46, 4), (51, 10), (48, 11), (44, 11), (42, 13), (40, 15),
     (38, 20), (37, 24), (35, 28), (33, 30), (32, 31), (27, 31), (22, 33), (18, 33),
     (13, 33), (10, 34), (10, 37), (5, 37), (0, 36)],
    [(95, 5), (100, 0), (104, -3), (107, -6), (104, -4), (100, 1), (96, 4)],
    [(109, 1), (113, 3), (117, 5), (119, 2), (118, -2), (114, -3), (110, -1)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (146, -8), (140, -6), (135, -3)],
    [(130, 31), (133, 34), (137, 35), (139, 36), (140, 38), (141, 40), (141, 42),
     (142, 44), (143, 45), (141, 44), (140, 41), (139, 38), (137, 35), (134, 34), (131, 32)],
    [(-5, 50), (-3, 53), (-2, 55), (-3, 57), (-5, 58), (-7, 57), (-8, 54), (-6, 52)],
    [(114, -22), (113, -26), (115, -31), (115, -34), (118, -35), (122, -34),
     (126, -32), (130, -32), (132, -31), (134, -33), (136, -35), (138, -35),
     (139, -37), (141, -38), (145, -38), (147, -38), (150, -37), (152, -33),
     (153, -29), (153, -25), (151, -22), (148, -19), (145, -17), (143, -14),
     (142, -11), (141, -13), (141, -16), (140, -18), (137, -16), (136, -15),
     (136, -12), (134, -11), (132, -11), (130, -12), (127, -13), (125, -15),
     (122, -17), (119, -19), (116, -20)],
    [(173, -35), (176, -37), (178, -38), (176, -40), (174, -41), (173, -39), (172, -37)],
    [(167, -45), (169, -46), (171, -44), (173, -42), (170, -43), (168, -46)],
    [(-180, -64), (-150, -68), (-110, -66), (-70, -70), (-30, -68), (10, -69),
     (50, -66), (90, -68), (130, -66), (180, -69), (180, -90), (-180, -90)],
]

# Pins: (number, lon, lat, continent, dx, dy) — dx/dy in 1024 units.
PINS = [
    (1, 84.9, 19.3, "ASIA", 0, 0),
    (2, 30.5, 50.4, "EUROPE", -2, -3),
    (3, 30.7, 36.9, "EUROPE", -5, 5),
    (4, 139.7, 35.7, "ASIA", 2, 0),
    (5, 46.7, 24.6, "ASIA", -5, 1),
    (6, 56.3, 26.5, "ASIA", 6, 4),
    (7, 8.9, 44.4, "EUROPE", -3, -2),
    (8, -77.0, 38.9, "NORTH AMERICA", 0, 0),
    (9, -58.4, -34.6, "SOUTH AMERICA", 0, 0),
    (10, 115.9, -31.9, "OCEANIA", 0, 0),
    (11, 174.8, -41.3, "ZEALANDIA", 1, 0),
    (12, 40.0, -64.5, "ANTARCTICA", 0, 1),
    (13, 44.8, 41.7, "EUROPE", 6, -4),
]


def draw_map(d, x, y, w, h):
    """Navy sea, sand land, numbered continent-coloured pins."""
    d.rounded_rectangle([X(x), X(y), X(x + w), X(y + h)], radius=X(4), fill=NAVY)
    mx, my, mw, mh = x + 6, y + 6, w - 12, h - 12

    def proj(lon, lat):
        return (mx + (lon + 180) / 360 * mw, my + (86 - lat) / 156 * mh)

    for lon in range(-150, 180, 30):  # graticule
        gx, _ = proj(lon, 0)
        d.line([X(gx), X(my), X(gx), X(my + mh)], fill=(28, 54, 92), width=1)
    for lat in (-60, -30, 0, 30, 60):
        _, gy = proj(0, lat)
        d.line([X(mx), X(gy), X(mx + mw), X(gy)], fill=(28, 54, 92), width=1)
    for poly in LAND:
        d.polygon([(X(a), X(b)) for a, b in (proj(lon, lat) for lon, lat in poly)], fill=SAND)
    f_pin = font(SANS_B, 7.5)
    for num, lon, lat, cont, dx, dy in PINS:
        px, py = proj(lon, lat)
        px, py = px + dx, py + dy
        col = CONTINENT_COLORS[cont]
        r = 6.4
        d.ellipse([X(px - r), X(py - r), X(px + r), X(py + r)], fill=col, outline=WHITE, width=X(1.2))
        label = str(num)
        tw = d.textlength(label, font=f_pin)
        d.text((X(px) - tw / 2, X(py) - X(3.9)), label, font=f_pin, fill=WHITE)


# ----------------------------------------------------------------- layout
M = 14
CW = W - 2 * M  # 996


def draw_header(d):
    d.text((X(M), X(10)), "ONE DAY, ONE ORBIT — THE WORLD IN ONE DAY",
           font=font(SANS_B, 10), fill=INK)
    text_r(d, W - M, 10, "37 STORIES · 8 CONTINENTS · EVERY TIME ZONE",
           font(SANS_B, 10), INK)
    d.rectangle([X(M), X(27), X(W - M), X(29.5)], fill=INK)
    f = fit_font(d, "Friday 20 November 2026", SERIF_B, 63, CW)
    text_c(d, W / 2, 34, "Friday 20 November 2026", f, INK)
    text_c(d, W / 2, 95,
           "Cyclone Akvan hits Odisha · COP31 closes in Antalya · Missiles strike Kyiv · Asia’s markets slide again",
           font(SERIF_I, 14.5), (60, 58, 52))
    d.rectangle([X(M), X(117), X(W - M), X(120)], fill=INK)
    d.rectangle([X(M), X(122.5), X(W - M), X(123.5)], fill=INK)


def draw_stats(d):
    y = 131
    cw = CW / 6
    for i, (num, label) in enumerate(STATS):
        cx = M + i * cw
        d.rectangle([X(cx), X(y), X(cx + 2.5), X(y + 33)], fill=RED)
        d.text((X(cx + 9), X(y - 2)), num, font=font(SERIF_B, 23), fill=INK)
        lf = fit_font(d, label, SANS, 8.8, cw - 13, min_size=7.5)
        d.text((X(cx + 9), X(y + 26)), label, font=lf, fill=MUTED)
    d.rectangle([X(M), X(172), X(W - M), X(173)], fill=FAINT)


def draw_tally(d):
    y = 180
    order = ["ASIA", "EUROPE", "NORTH AMERICA", "SOUTH AMERICA",
             "AFRICA", "OCEANIA", "ZEALANDIA", "ANTARCTICA"]
    counts = {"ASIA": 11, "EUROPE": 10, "NORTH AMERICA": 7, "SOUTH AMERICA": 5,
              "AFRICA": 1, "OCEANIA": 1, "ZEALANDIA": 1, "ANTARCTICA": 1}
    x = M
    for name in order:
        wseg = CW * counts[name] / 37
        d.rectangle([X(x), X(y), X(x + wseg), X(y + 15)], fill=CONTINENT_COLORS[name])
        if counts[name] >= 5:
            text_c(d, x + wseg / 2, y + 2.6, f"{name} {counts[name]}",
                   font(SANS_B, 9), WHITE)
        x += wseg
    d.text((X(M), X(199)),
           "AFRICA 1 · OCEANIA 1 · ZEALANDIA 1 · ANTARCTICA 1",
           font=font(SANS, 9), fill=MUTED)
    text_r(d, W - M, 199, "EVERY CONTINENT ON EARTH — IN ONE DAY",
           font(SANS_B, 9), INK)


def panel_base(d, x, y, w, h):
    d.rectangle([X(x), X(y), X(x + w), X(y + h)], fill=PANEL)
    d.rectangle([X(x), X(y), X(x + w), X(y + h)], outline=(38, 38, 38), width=X(1))


def draw_lead(img, d, x, y, w, h, item):
    num, story, dateline, scenefn = item
    cont, _glyph, head, detail, src = story
    panel_base(d, x, y, w, h)
    sub, sd = scene_canvas(w, 110)
    scenefn(sub, sd, w, 110)
    img.paste(sub, (X(x), X(y)))
    d.rectangle([X(x), X(y + 110), X(x + w), X(y + 113)], fill=CONTINENT_COLORS[cont])
    d.rectangle([X(x + 10), X(y + 120), X(x + 27), X(y + 137)], fill=RED)
    nf = font(SANS_B, 11)
    tw = d.textlength(str(num), font=nf)
    d.text((X(x + 18.5) - tw / 2, X(y + 122.5)), str(num), font=nf, fill=WHITE)
    d.text((X(x + 34), X(y + 121.5)), dateline, font=font(SANS_B, 9.8), fill=INK)
    text_r(d, x + w - 10, y + 121.5, cont, font(SANS_B, 9), CONTINENT_COLORS[cont])
    yy = block(d, x + 10, y + 142, wrap(d, head, font(SERIF_B, 18.5), X(w - 20)),
               font(SERIF_B, 18.5), INK, 21.5)
    block(d, x + 10, yy + 3, wrap(d, detail, font(SERIF, 12), X(w - 20)),
          font(SERIF, 12), (52, 52, 50), 14.5)
    d.text((X(x + 10), X(y + h - 16)), f"({src})", font=font(SERIF_I, 9.5), fill=MUTED)


def draw_feature(img, d, x, y, w, h, item):
    num, story, dateline, scenefn = item
    cont, _glyph, head, detail, src = story
    panel_base(d, x, y, w, h)
    sub, sd = scene_canvas(w, 46)
    scenefn(sub, sd, w, 46)
    img.paste(sub, (X(x), X(y)))
    d.rectangle([X(x), X(y + 46), X(x + w), X(y + 48.5)], fill=CONTINENT_COLORS[cont])
    d.text((X(x + 7), X(y + 52)), f"{num:02d} · {dateline}",
           font=font(SANS_B, 8), fill=(74, 72, 66))
    yy = block(d, x + 7, y + 63, wrap(d, head, font(SERIF_B, 12), X(w - 14)),
               font(SERIF_B, 12), INK, 14)
    block(d, x + 7, yy + 2.5, wrap(d, detail, font(SANS, 9), X(w - 14)),
          font(SANS, 9), (56, 56, 54), 11.5)
    sf = fit_font(d, f"({src})", SERIF_I, 8, w - 14, min_size=6)
    d.text((X(x + 7), X(y + h - 13)), f"({src})", font=sf, fill=MUTED)


def draw_bottom(d):
    y = 744
    d.text((X(M), X(y)), "WHERE IT HAPPENED", font=font(SANS_B, 11.5), fill=INK)
    draw_map(d, M, y + 20, 302, 168)
    block(d, M, y + 194, wrap(d, "Pins 1–13 mark the drawn stories, coloured by "
                              "continent — the day ran Auckland to Honolulu.",
                          font(SANS, 8.5), X(302)),
          font(SANS, 8.5), MUTED, 11)
    bx = 328
    d.text((X(bx), X(y)), "ALSO ON FRIDAY — 24 MORE STORIES",
           font=font(SANS_B, 12.5), fill=INK)
    d.rectangle([X(bx), X(y + 19), X(W - M), X(y + 21)], fill=GOLD)
    cols = [(bx, BRIEFS[:12]), (bx + 344, BRIEFS[12:])]
    for cx, items in cols:
        yy = y + 30
        for num, place, text in items:
            nf, pf = font(SANS_B, 9.5), font(SANS_B, 9.5)
            ns = f"{num} "
            ps = place + "  "
            total = (d.textlength(ns, font=nf) + d.textlength(ps, font=pf)
                     + d.textlength(text, font=font(SANS, 9.5)))
            tf = font(SANS, 9.5 if total <= X(330) else 8.8)
            d.text((X(cx), X(yy)), ns, font=nf, fill=RED)
            x2 = X(cx) + d.textlength(ns, font=nf)
            d.text((x2, X(yy)), ps, font=pf, fill=INK)
            d.text((x2 + d.textlength(ps, font=pf), X(yy)), text, font=tf, fill=(40, 40, 40))
            yy += 15.2


def draw_footer(d):
    y = 962
    d.rectangle([X(M), X(y), X(W - M), X(y + 32)], outline=RED, width=X(1.2))
    d.text((X(M + 10), X(y + 6)), "DATE\nCHECK", font=font(SANS_B, 9), fill=RED)
    text = ("Five stories broke late on Thursday 19 November and led Friday’s coverage — "
            "marked (*): the Shenzhen peace declaration, Anthropic’s Nasdaq debut, Wall "
            "Street’s fifth straight loss, the Kayapo homeland ruling and Brazil’s WTO "
            "request. All 32 other stories happened, or were first reported, on Friday "
            "20 November 2026 in at least one time zone.")
    block(d, M + 52, y + 5, wrap(d, text, font(SANS, 9.5), X(CW - 66)),
          font(SANS, 9.5), (52, 50, 48), 12)
    text_c(d, W / 2, 1001,
           "Every story attributed — sources: Reuters · BBC · AP · The Independent · IMD · "
           "UN News · Daily Baku · Rio Times · Scimex · FIFA — full list in README.md · "
           "Original drawings, no photographs, no likenesses",
           font(SANS, 8.5), MUTED)


def main():
    assert len(STORIES) == 12 and len(WIRE) == 25, "v1 story data changed"
    assert len(LEADS) + len(FEATURES) == 13 and len(BRIEFS) == 24
    img = Image.new("RGB", (X(W), X(H)), PAPER)
    d = ImageDraw.Draw(img, "RGBA")
    draw_header(d)
    draw_stats(d)
    draw_tally(d)
    pw = (CW - 20) / 3
    for i, item in enumerate(LEADS):
        draw_lead(img, d, M + i * (pw + 10), 216, pw, 232, item)
    fw = (CW - 32) / 5
    for i, item in enumerate(FEATURES):
        r, c = divmod(i, 5)
        draw_feature(img, d, M + c * (fw + 8), 456 + r * 144, fw, 136, item)
    draw_bottom(d)
    draw_footer(d)
    # Deterministic paper grain at render scale (softened by the downscale).
    rng = np.random.default_rng(20261120)
    arr = np.asarray(img).astype(np.int16)
    noise = rng.normal(0, 0.55, arr.shape[:2])[:, :, None]
    img = Image.fromarray(np.clip(arr + noise, 0, 255).astype(np.uint8))
    img = img.resize((W, H), Image.LANCZOS)
    img.save(OUT, optimize=True)
    import os
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}, {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
