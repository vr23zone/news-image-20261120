#!/usr/bin/env python3
"""draw5.py — v5 BOLD of "One Day, One Orbit": Friday 20 November 2026.

Fifth iteration, built on the v3 CREAM version (draw3.py @ 0114383) —
the story data is EXACTLY v1/v2/v3/v4's 37 verified stories (imported
from draw.py via draw2.py: 13 drawn panels + 24 briefs, 8 continents)
— no fact, headline, detail or source changes, and the layout, stat
strip, COP31 panel, map pins and DATE CHECK box are v3's, unchanged.

What changes is ONLY the rendering, at Rohim's request ("buat warnanya
lebih tebal dan pekat" — make the colours thicker/bolder and deeper).
v4 SOFT (draw4.py) went pastel; v5 goes the OPPOSITE way, past v3:

- BOLD, DEEP PALETTE: every page colour is pushed richer — HLS
  saturation x1.35 and lightness pulled down (x0.93) for jewel-deep
  tones; ink is a strong near-black; the DATE CHECK / accent red is a
  deep strong crimson (166,14,32); the map sea is a deep navy and the
  land a rich golden sand.
- FULL YELLOW PAGE (Rohim's added instruction, 21 Nov 00:11 WIB:
  "background full nya warna kuning"): the whole canvas background
  is one flat bold deep yellow #F2B705 — no cream page, no gray —
  with panels in a pale yellow-cream #FEF4CD so the text stays
  readable while the page reads unmistakably YELLOW everywhere
  around and between the panels.
- BOLD SCENES: each of the 13 illustrations is post-processed as it is
  pasted in — saturation x1.32, contrast x1.07, brightness x0.99 — so
  the flat colour blocks read thick, saturated and punchy. NO blur,
  NO pastel wash: scenes stay flat and crisp like v3, only deeper.
- CRISP PANELS: square corners with a strong near-black frame, as v3.
- Text stays sharp strong ink: headlines bold, everything readable.

Deterministic: fixed layout, fixed fonts, seeded noise only (star/rain
fields). Rendered at 2x (2048x2048) and downscaled to 1024x1024. Run
twice -> identical bytes. Output: entry.png, 1024x1024, <= 1 MiB.

No recognisable face of a real person is drawn anywhere: every
illustration is a generic scene of places, weather, objects and
symbols, never a likeness.
"""

import colorsys
import math
import random

from PIL import Image, ImageDraw, ImageEnhance

# Reuse v2's proven helpers, palette, data and map so the story content
# and text metrics are identical; only scenes/stats/finish differ.
from draw import STORIES, WIRE  # noqa: F401  (v1 verified data, unchanged)
from draw2 import (
    CONTINENT_COLORS, FAINT, GOLD, INK, MUTED, NAVY, PANEL, PAPER, RED,
    SAND, SERIF, SERIF_B, SERIF_I, SANS, SANS_B, WHITE, BRIEFS, LAND,
    PINS, TBILISI, SS, W, H, X, block, chip_label, draw_map, fit_font,
    font, scene_canvas, stars, text_c, text_r, vgrad, wrap,
)
import draw2 as _draw2


# --- v5 bold palette ------------------------------------------------------
# One deterministic deepening rule for page colours: HLS saturation
# x1.35 (about a third MORE saturated) and lightness pulled down x0.93,
# which deepens mid/dark tones into rich, concentrated ink-like hues.
def _deepen(col):
    r, g, b = (v / 255 for v in col)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    s = min(1.0, s * 1.35)
    l = l * 0.93
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return tuple(round(v * 255) for v in (r, g, b))


PAPER = (242, 183, 5)    # #F2B705 — FULL bold deep yellow page
PANEL = (254, 244, 205)  # #FEF4CD — pale yellow-cream panels on the yellow
FAINT = (150, 118, 40)   # deep golden-brown divider rule (visible on yellow)
INK = (13, 14, 17)       # strong near-black ink
MUTED = _deepen(MUTED)   # deepened warm gray for captions/sources
RED = (166, 14, 32)      # deep strong crimson (DATE CHECK, stat bars)
GOLD = _deepen(GOLD)
NAVY = _deepen(NAVY)     # deep navy map sea
SAND = _deepen(SAND)     # rich golden-sand map land
WHITE = (255, 255, 255)  # pure white for maximum scene contrast
CONTINENT_COLORS = {name: _deepen(col) for name, col in CONTINENT_COLORS.items()}

# Helpers imported from draw2 (scene_canvas, draw_map) read the palette
# from draw2's own module globals — patch those too so scenes start on
# the yellow paper and the map/pins use the bold palette.
for _name, _val in (("PAPER", PAPER), ("PANEL", PANEL), ("FAINT", FAINT),
                    ("INK", INK), ("MUTED", MUTED), ("RED", RED),
                    ("GOLD", GOLD), ("NAVY", NAVY), ("SAND", SAND),
                    ("WHITE", WHITE), ("CONTINENT_COLORS", CONTINENT_COLORS)):
    setattr(_draw2, _name, _val)

OUT = "entry.png"


# --- v5 bold scene finish ---------------------------------------------------
def deepen_scene(sub):
    """Deepen one rendered scene sub-image (render scale, RGB).

    Saturation x1.32 and contrast x1.07 make the flat colour blocks
    thick, rich and punchy; brightness x0.99 keeps the depth. NO blur,
    NO wash, NO tint — scenes stay flat and crisp like v3, only deeper
    and more saturated. Deterministic.
    """
    img = sub.convert("RGB")
    img = ImageEnhance.Color(img).enhance(1.32)
    img = ImageEnhance.Contrast(img).enhance(1.07)
    img = ImageEnhance.Brightness(img).enhance(0.99)
    return img


def paste_scene(img, sub, x, y):
    """Paste a deepened scene with square corners, v3 style — the
    continent colour bar sits directly under it."""
    img.paste(deepen_scene(sub), (X(x), X(y)))



# ------------------------------------------------------------------ scenes
# Each scene draws into a sub-image of w x h (1024 units). Generic places,
# weather and objects only — never a person. v3: bigger motifs, fuller
# frames, bolder labels than v2.

def sc_cyclone(img, d, w, h):
    """Cyclone spiral over a Bay of Bengal coastline — v3: glow pass,
    delta rivers, Gopalpur marker, denser rain."""
    vgrad(img, (0, 0, X(w), X(h)), (13, 54, 92), (33, 102, 134))
    land = [(0, 0), (0.42 * w, 0), (0.34 * w, 0.18 * h), (0.40 * w, 0.38 * h),
            (0.30 * w, 0.58 * h), (0.36 * w, 0.80 * h), (0.28 * w, h),
            (0, h)]
    d.polygon([(X(a), X(b)) for a, b in land], fill=(219, 199, 150))
    d.line([(X(a), X(b)) for a, b in land[1:-1]], fill=(242, 230, 192), width=X(2))
    # Delta rivers on the landmass.
    for (rx, ry) in ((0.10, 0.30), (0.16, 0.52), (0.08, 0.72)):
        d.line([X(rx * w), X(ry * h), X((rx + 0.13) * w), X((ry + 0.05) * h),
                X((rx + 0.20) * w), X((ry + 0.16) * h)],
               fill=(110, 150, 170), width=X(1.3))
    # Spiral arms: soft glow pass under a bright core pass.
    cx, cy = 0.63 * w, 0.50 * h
    for arm in range(3):
        pts = []
        for t in range(0, 101):
            th = arm * (2 * math.pi / 3) + t * 0.055
            r = 3 + t * 0.66
            pts.append((X(cx + r * math.cos(th) * 1.28), X(cy + r * math.sin(th) * 0.80)))
        d.line(pts, fill=(200, 228, 240, 70), width=X(6.5))
        d.line(pts, fill=(243, 249, 251), width=X(3.0))
    d.ellipse([X(cx - 7.5), X(cy - 5.5), X(cx + 7.5), X(cy + 5.5)], fill=(13, 54, 92))
    d.ellipse([X(cx - 7.5), X(cy - 5.5), X(cx + 7.5), X(cy + 5.5)], outline=WHITE, width=X(1.8))
    # Wind streak arcs around the spiral.
    for rr, a0 in ((0.30, 200), (0.38, 20)):
        d.arc([X(cx - rr * w), X(cy - rr * h * 0.62), X(cx + rr * w), X(cy + rr * h * 0.62)],
              a0, a0 + 70, fill=(190, 220, 235), width=X(1.6))
    rng = random.Random(7)
    for _ in range(42):
        sx = rng.uniform(0.52 * w, w - 6)
        sy = rng.uniform(0.50 * h, h - 8)
        d.line([X(sx), X(sy), X(sx - 5), X(sy + 7)], fill=(190, 220, 235), width=X(1.2))
    d.text((X(10), X(8)), "ODISHA", font=font(SANS_B, 10), fill=(70, 60, 40))
    d.text((X(10), X(21)), "INDIA", font=font(SANS, 8.5), fill=(70, 60, 40))
    # Gopalpur landfall marker on the coast.
    gx, gy = 0.375 * w, 0.33 * h
    d.ellipse([X(gx - 3.4), X(gy - 3.4), X(gx + 3.4), X(gy + 3.4)], fill=RED, outline=WHITE, width=X(1.2))
    d.text((X(gx - 30), X(gy - 13)), "GOPALPUR", font=font(SANS_B, 7.5), fill=(70, 60, 40))
    text_r(d, w - 8, h - 15, "BAY OF BENGAL", font(SANS_B, 8.5), (200, 226, 238))
    chip_label(d, 8, h - 19, "LANDFALL · GUSTS 110 KM/H", RED)


def sc_kyiv(img, d, w, h):
    """Ballistic streaks, searchlights and a burning power plant — v3:
    more arcs, lit windows, smoke plume, second burst."""
    vgrad(img, (0, 0, X(w), X(h)), (6, 10, 30), (24, 32, 62))
    stars(d, (0, 0, X(w), X(h)), 60, 11)
    # Searchlight cones sweeping from the skyline.
    for (lx, tilt) in ((0.18, 0.16), (0.80, -0.14)):
        d.polygon([(X(lx * w), X(h)), (X((lx + tilt - 0.05) * w), X(0.06 * h)),
                   (X((lx + tilt + 0.05) * w), X(0.06 * h))],
                  fill=(220, 230, 255, 34))
    arcs = [((0.06, 0.06), (0.34, 0.52)), ((0.30, 0.02), (0.52, 0.58)),
            ((0.55, 0.05), (0.70, 0.60)), ((0.78, 0.03), (0.86, 0.55)),
            ((0.16, 0.16), (0.42, 0.60)), ((0.66, 0.14), (0.78, 0.58)),
            ((0.44, 0.10), (0.60, 0.62)), ((0.90, 0.12), (0.93, 0.50))]
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
    base = h
    blocks = [(0, 0.30), (0.07, 0.42), (0.13, 0.34), (0.20, 0.46), (0.27, 0.36),
              (0.33, 0.30), (0.72, 0.34), (0.79, 0.44), (0.86, 0.33), (0.93, 0.40)]
    rngw = random.Random(23)
    for bx, bh in blocks:
        d.rectangle([X(bx * w), X(base - bh * h), X(bx * w + 0.055 * w), X(base)],
                    fill=(5, 8, 18))
        for wy in range(3):
            for wx in range(2):
                if rngw.random() < 0.45:
                    d.rectangle([X(bx * w + 4 + wx * 7), X(base - bh * h + 5 + wy * 8),
                                 X(bx * w + 7 + wx * 7), X(base - bh * h + 9 + wy * 8)],
                                fill=(255, 205, 110))
    d.rectangle([X(0.44 * w), X(0.66 * h), X(0.66 * w), X(base)], fill=(5, 8, 18))
    for chx in (0.50, 0.585):
        d.rectangle([X(chx * w), X(0.34 * h), X(chx * w + 0.028 * w), X(0.68 * h)],
                    fill=(5, 8, 18))
        d.rectangle([X(chx * w - 0.004 * w), X(0.32 * h), X(chx * w + 0.032 * w), X(0.36 * h)],
                    fill=(5, 8, 18))
    # Smoke plume over the plant.
    for i in range(4):
        sx, sy = 0.545 * w + i * 7, 0.30 * h - i * 4
        d.ellipse([X(sx - 6 - i * 2), X(sy - 4), X(sx + 6 + i * 2), X(sy + 4)],
                  fill=(90, 92, 104, 120))
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
    """COP31 final day — v3 redesign: big globe with melting cap, a tall
    thermometer, and a delegates' table with flag poles along the bottom
    (the ~200 nations), filling the frame v2 left empty."""
    vgrad(img, (0, 0, X(w), X(h)), (10, 58, 78), (24, 110, 118))
    # Sun disc top-right corner, clear of the dateline text.
    d.ellipse([X(0.885 * w), X(-0.02 * h), X(1.03 * w), X(0.32 * h)], fill=(244, 178, 66))
    # Globe, larger and left of centre.
    gx, gy, gr = 0.33 * w, 0.45 * h, 0.35 * h
    d.ellipse([X(gx - gr), X(gy - gr), X(gx + gr), X(gy + gr)], fill=(52, 124, 186))
    for (ox, oy, rw, rh) in ((-0.38, -0.18, 0.30, 0.17), (0.28, -0.02, 0.26, 0.15),
                             (-0.12, 0.34, 0.30, 0.16), (0.40, 0.44, 0.20, 0.12),
                             (-0.48, 0.22, 0.20, 0.12)):
        d.ellipse([X(gx + (ox - rw) * gr), X(gy + (oy - rh) * gr),
                   X(gx + (ox + rw) * gr), X(gy + (oy + rh) * gr)], fill=(74, 160, 92))
    for oy in (-0.05, 0.38):
        d.arc([X(gx - gr), X(gy + oy * gr - 0.42 * gr), X(gx + gr), X(gy + oy * gr + 0.42 * gr)],
              20, 160, fill=(120, 180, 220), width=X(1.1))
    cap = []
    for a in range(180, 361, 12):
        cap.append((gx + gr * math.cos(math.radians(a)), gy + gr * math.sin(math.radians(a))))
    for i, a in enumerate(range(348, 179, -14)):
        rr = gr * (0.80 if i % 2 == 0 else 0.90)
        cap.append((gx + rr * math.cos(math.radians(a)), gy + rr * math.sin(math.radians(a))))
    d.polygon([(X(a), X(b)) for a, b in cap], fill=(238, 246, 250))
    for dx in (-0.42, 0.08, 0.48):
        d.polygon([(X(gx + dx * gr - 2), X(gy - gr * 0.80)), (X(gx + dx * gr + 2), X(gy - gr * 0.80)),
                   (X(gx + dx * gr), X(gy - gr * 0.56))], fill=(238, 246, 250))
    # Thermometer, tall and wide, right of centre.
    tx = 0.635 * w
    d.rounded_rectangle([X(tx), X(0.07 * h), X(tx + 0.052 * w), X(0.72 * h)],
                        radius=X(7), fill=(240, 244, 246), outline=(180, 190, 196), width=X(1))
    d.rectangle([X(tx + 0.016 * w), X(0.22 * h), X(tx + 0.036 * w), X(0.72 * h)], fill=RED)
    d.ellipse([X(tx - 0.018 * w), X(0.62 * h), X(tx + 0.070 * w), X(0.90 * h)], fill=RED)
    d.ellipse([X(tx - 0.018 * w), X(0.62 * h), X(tx + 0.070 * w), X(0.90 * h)],
              outline=(240, 244, 246), width=X(1.4))
    for i in range(5):
        ty = 0.15 * h + i * 0.11 * h
        d.line([X(tx + 0.058 * w), X(ty), X(tx + 0.082 * w), X(ty)], fill=WHITE, width=X(1.5))
    # Delegates' table band with a row of generic flag poles.
    d.rectangle([0, X(0.82 * h), X(w), X(h)], fill=(10, 40, 56))
    d.rectangle([0, X(0.82 * h), X(w), X(0.845 * h)], fill=(16, 66, 84))
    flag_cols = [(178, 32, 44), (36, 90, 166), (34, 139, 60), (212, 160, 32),
                 (104, 74, 160), (0, 130, 150), (176, 92, 20), (240, 240, 240)]
    for i in range(14):
        fx = 0.045 * w + i * 0.068 * w
        d.line([X(fx), X(0.845 * h), X(fx), X(0.955 * h)], fill=(200, 205, 210), width=X(1.1))
        d.rectangle([X(fx), X(0.845 * h), X(fx + 0.030 * w), X(0.885 * h)],
                    fill=flag_cols[i % len(flag_cols)])
    d.text((X(0.035 * w), X(0.055 * h)), "ANTALYA · NOV 20", font=font(SANS_B, 10), fill=WHITE)
    chip_label(d, 8, h - 19, "COP31 · FINAL DAY", RED)
    text_r(d, w - 8, h - 15, "TEXT DUE AT MIDNIGHT", font(SANS_B, 8.5), (216, 238, 240))


def sc_markets(img, d, w, h):
    """Falling chart with candlesticks and volume bars — v3: bolder."""
    d.rectangle([0, 0, X(w), X(h)], fill=(13, 17, 29))
    for gx in range(1, 8):
        d.line([X(gx * w / 8), 0, X(gx * w / 8), X(h)], fill=(36, 44, 64), width=1)
    for gy in range(1, 3):
        d.line([0, X(gy * h / 3), X(w), X(gy * h / 3)], fill=(36, 44, 64), width=1)
    pts = [(0.03, 0.40), (0.16, 0.46), (0.28, 0.42), (0.40, 0.54), (0.52, 0.51),
           (0.64, 0.64), (0.76, 0.70), (0.88, 0.80), (0.97, 0.86)]
    xy = [(X(a * w), X(b * h)) for a, b in pts]
    d.polygon(xy + [(X(w), X(h)), (0, X(h))], fill=(178, 32, 44, 80))
    # Candlesticks stepping down along the fall.
    for i in range(7):
        cx = (0.08 + i * 0.125) * w
        top = (0.30 + i * 0.075) * h
        bot = top + 0.20 * h
        d.line([X(cx), X(top - 4), X(cx), X(bot + 4)], fill=(255, 110, 110), width=X(1.2))
        d.rectangle([X(cx - 4.5), X(top), X(cx + 4.5), X(bot)], fill=(198, 44, 54))
    d.line(xy, fill=(255, 84, 84), width=X(2.4))
    ex, ey = xy[-1]
    d.polygon([(ex, ey), (ex - X(9), ey - X(2)), (ex - X(3), ey + X(7))], fill=(255, 84, 84))
    # Volume bars along the bottom.
    for i, vh in enumerate((0.10, 0.14, 0.09, 0.17, 0.13, 0.20, 0.16, 0.23)):
        bx = (0.04 + i * 0.12) * w
        d.rectangle([X(bx), X(h - vh * h), X(bx + 0.07 * w), X(h)], fill=(90, 40, 48))
    d.text((X(8), X(5)), "ASIA -7% WK", font=font(SANS_B, 9.5), fill=(255, 120, 120))
    text_r(d, w - 7, 5, "KOSPI -4.7%", font(SANS_B, 9.5), (255, 214, 120))


def sc_houthi(img, d, w, h):
    """Two missile arcs toward a tall tower at dusk — v3: fuller skyline."""
    vgrad(img, (0, 0, X(w), X(h)), (64, 40, 78), (198, 98, 62))
    # Crescent moon top-right, clear of the RIYADH label.
    d.ellipse([X(0.86 * w), X(0.05 * h), X(0.94 * w), X(0.33 * h)], fill=(250, 236, 190))
    d.ellipse([X(0.885 * w), X(0.02 * h), X(0.965 * w), X(0.30 * h)], fill=(84, 50, 79))
    tx = 0.60 * w
    d.polygon([(X(tx), X(h)), (X(tx + 3), X(0.22 * h)), (X(tx + 7), X(0.22 * h)),
               (X(tx + 10), X(h))], fill=(16, 14, 26))
    d.line([X(tx + 5), X(0.22 * h), X(tx + 5), X(0.05 * h)], fill=(16, 14, 26), width=X(1.6))
    d.rectangle([X(0.06 * w), X(0.72 * h), X(0.40 * w), X(h)], fill=(16, 14, 26))
    d.rectangle([X(0.80 * w), X(0.62 * h), X(0.97 * w), X(h)], fill=(16, 14, 26))
    d.rectangle([X(0.42 * w), X(0.80 * h), X(0.58 * w), X(h)], fill=(16, 14, 26))
    d.rectangle([X(0.68 * w), X(0.78 * h), X(0.79 * w), X(h)], fill=(16, 14, 26))
    for (a0, b0, a1, b1, sag) in ((0.05, 0.75, 0.60, 0.13, 0.30), (0.30, 0.92, 0.615, 0.42, 0.22)):
        pts = []
        for t in range(21):
            u = t / 20
            pts.append((X((a0 + (a1 - a0) * u) * w),
                        X((b0 + (b1 - b0) * u + sag * u * u) * h)))
        d.line(pts, fill=(255, 190, 90), width=X(2.4))
    bx, by = 0.615 * w, 0.30 * h
    for ang in range(0, 360, 45):
        d.line([X(bx), X(by), X(bx + 11 * math.cos(math.radians(ang))),
                X(by + 8 * math.sin(math.radians(ang)))], fill=(255, 170, 60), width=X(1.6))
    d.text((X(8), X(5)), "RIYADH", font=font(SANS_B, 9), fill=(255, 226, 190))


def sc_tanker(img, d, w, h):
    """Burning tanker with a second ship on the horizon — v3: bigger fire."""
    vgrad(img, (0, 0, X(w), X(h)), (30, 52, 84), (16, 40, 66))
    d.ellipse([X(0.86 * w), X(0.06 * h), X(0.94 * w), X(0.30 * h)], fill=(226, 232, 238))
    d.rectangle([0, X(0.66 * h), X(w), X(h)], fill=(10, 26, 44))
    # Distant second tanker, small on the left horizon.
    d.polygon([(X(0.03 * w), X(0.63 * h)), (X(0.20 * w), X(0.63 * h)),
               (X(0.18 * w), X(0.68 * h)), (X(0.05 * w), X(0.68 * h))], fill=(22, 34, 52))
    d.rectangle([X(0.15 * w), X(0.56 * h), X(0.19 * w), X(0.63 * h)], fill=(22, 34, 52))
    for i in range(5):
        y = 0.72 * h + i * 0.06 * h
        d.line([X(0.05 * w + (i % 2) * 14), X(y), X(0.35 * w + (i % 2) * 14), X(y)],
               fill=(52, 84, 116), width=X(1.2))
    d.polygon([(X(0.08 * w), X(0.66 * h)), (X(0.92 * w), X(0.66 * h)),
               (X(0.86 * w), X(0.80 * h)), (X(0.14 * w), X(0.80 * h))], fill=(8, 10, 16))
    d.rectangle([X(0.16 * w), X(0.56 * h), X(0.70 * w), X(0.66 * h)], fill=(8, 10, 16))
    d.rectangle([X(0.74 * w), X(0.44 * h), X(0.86 * w), X(0.66 * h)], fill=(8, 10, 16))
    fx, fy = 0.42 * w, 0.56 * h
    for (fw, fh, col) in ((14, 32, (255, 110, 30)), (9.5, 24, (255, 160, 40)), (5.5, 15, (255, 214, 92))):
        d.polygon([(X(fx - fw), X(fy)), (X(fx + fw), X(fy)), (X(fx + fw * 0.3), X(fy - fh * 0.6)),
                   (X(fx), X(fy - fh)), (X(fx - fw * 0.35), X(fy - fh * 0.55))], fill=col)
    for i in range(4):
        d.ellipse([X(fx + 6 + i * 10), X(fy - 38 - i * 3), X(fx + 24 + i * 11), X(fy - 24 - i * 3)],
                  fill=(120, 124, 132, 130))
    d.text((X(8), X(5)), "HORMUZ", font=font(SANS_B, 9), fill=(210, 226, 240))


def sc_genoa(img, d, w, h):
    """Airliner held on a runway, control tower, three drones — v3."""
    vgrad(img, (0, 0, X(w), X(h)), (96, 148, 196), (168, 200, 228))
    # Control tower + terminal block, right.
    d.rectangle([X(0.90 * w), X(0.30 * h), X(0.925 * w), X(0.78 * h)], fill=(30, 40, 56))
    d.rectangle([X(0.885 * w), X(0.22 * h), X(0.94 * w), X(0.32 * h)], fill=(30, 40, 56))
    d.rectangle([X(0.70 * w), X(0.58 * h), X(0.88 * w), X(0.78 * h)], fill=(52, 62, 78))
    for i in range(4):
        d.rectangle([X(0.715 * w + i * 0.04 * w), X(0.63 * h), X(0.735 * w + i * 0.04 * w), X(0.70 * h)],
                    fill=(255, 214, 120))
    d.rectangle([0, X(0.78 * h), X(w), X(h)], fill=(70, 76, 84))
    for i in range(6):
        d.line([X(0.06 * w + i * 0.17 * w), X(0.885 * h), X(0.12 * w + i * 0.17 * w), X(0.885 * h)],
               fill=(240, 240, 240), width=X(1.6))
    px, py = 0.08 * w, 0.60 * h
    d.polygon([(X(px), X(py)), (X(px + 0.34 * w), X(py - 0.02 * h)), (X(px + 0.40 * w), X(py + 0.05 * h)),
               (X(px + 0.40 * w), X(py + 0.11 * h)), (X(px + 0.03 * w), X(py + 0.10 * h))], fill=(24, 30, 40))
    d.polygon([(X(px + 0.02 * w), X(py - 0.01 * h)), (X(px - 0.03 * w), X(py - 0.16 * h)),
               (X(px + 0.05 * w), X(py - 0.15 * h)), (X(px + 0.07 * w), X(py))], fill=(24, 30, 40))
    d.polygon([(X(px + 0.16 * w), X(py + 0.06 * h)), (X(px + 0.24 * w), X(py + 0.20 * h)),
               (X(px + 0.29 * w), X(py + 0.20 * h)), (X(px + 0.22 * w), X(py + 0.05 * h))], fill=(24, 30, 40))
    for (dx, dy) in ((0.60, 0.14), (0.76, 0.30), (0.52, 0.34)):
        cx, cy = dx * w, dy * h
        d.line([X(cx - 9), X(cy - 5), X(cx + 9), X(cy + 5)], fill=(20, 24, 32), width=X(1.6))
        d.line([X(cx - 9), X(cy + 5), X(cx + 9), X(cy - 5)], fill=(20, 24, 32), width=X(1.6))
        d.ellipse([X(cx - 2.4), X(cy - 2.4), X(cx + 2.4), X(cy + 2.4)], fill=RED)
    d.text((X(8), X(5)), "GENOA · FLIGHTS HELD", font=font(SANS_B, 9), fill=(16, 30, 48))


def sc_trump(img, d, w, h):
    """No-call symbol, hourglass and a big 2027 calendar — v3: bolder."""
    d.rectangle([0, 0, X(w), X(h)], fill=(238, 230, 210))
    # Calendar page right, larger.
    cx = 0.56 * w
    d.rectangle([X(cx), X(0.06 * h), X(cx + 0.38 * w), X(0.94 * h)], fill=WHITE,
                outline=(150, 140, 120), width=X(1))
    d.rectangle([X(cx), X(0.06 * h), X(cx + 0.38 * w), X(0.34 * h)], fill=RED)
    text_c(d, cx + 0.19 * w, 0.095 * h, "2027", font(SERIF_B, 11), WHITE)
    text_c(d, cx + 0.19 * w, 0.40 * h, "JAN 1", font(SERIF_B, 17), INK)
    text_c(d, cx + 0.19 * w, 0.72 * h, "NO CALL", font(SANS_B, 9), MUTED)
    # Hourglass left, larger.
    hx, hy = 0.36 * w, 0.48 * h
    d.polygon([(X(hx - 15), X(hy - 19)), (X(hx + 15), X(hy - 19)), (X(hx), X(hy))], fill=(120, 96, 52))
    d.polygon([(X(hx - 15), X(hy + 19)), (X(hx + 15), X(hy + 19)), (X(hx), X(hy))], outline=(120, 96, 52), width=X(1.8))
    d.polygon([(X(hx - 5), X(hy + 18)), (X(hx + 5), X(hy + 18)), (X(hx), X(hy + 6))], fill=(212, 160, 32))
    d.line([X(hx - 18), X(hy - 21), X(hx + 18), X(hy - 21)], fill=(90, 72, 40), width=X(2.6))
    d.line([X(hx - 18), X(hy + 21), X(hx + 18), X(hy + 21)], fill=(90, 72, 40), width=X(2.6))
    # Phone handset (crescent) under a red prohibition sign, bottom-left.
    px, py = 0.15 * w, 0.72 * h
    d.ellipse([X(px - 13), X(py - 8), X(px + 13), X(py + 10)], fill=(30, 34, 40))
    d.ellipse([X(px - 8), X(py - 14), X(px + 18), X(py + 4)], fill=(238, 230, 210))
    d.ellipse([X(px - 13), X(py - 13), X(px + 13), X(py + 13)], outline=RED, width=X(2.2))
    d.line([X(px - 9.2), X(py + 9.2), X(px + 9.2), X(py - 9.2)], fill=RED, width=X(2.2))
    d.text((X(8), X(5)), "IRAN", font=font(SANS_B, 9), fill=(110, 60, 30))


def sc_tesla(img, d, w, h):
    """Bigger car before a Buenos Aires skyline on the flag bands — v3."""
    d.rectangle([0, 0, X(w), X(0.36 * h)], fill=(116, 172, 223))
    d.rectangle([0, X(0.36 * h), X(w), X(0.68 * h)], fill=(245, 246, 244))
    d.rectangle([0, X(0.68 * h), X(w), X(h)], fill=(116, 172, 223))
    # Sun with rays in the white band.
    sx, sy = 0.50 * w, 0.52 * h
    for ang in range(0, 360, 30):
        d.line([X(sx + 9 * math.cos(math.radians(ang))), X(sy + 9 * math.sin(math.radians(ang))),
                X(sx + 13 * math.cos(math.radians(ang))), X(sy + 13 * math.sin(math.radians(ang)))],
               fill=(250, 190, 60), width=X(1.6))
    d.ellipse([X(sx - 8), X(sy - 8), X(sx + 8), X(sy + 8)], fill=(250, 190, 60))
    # Skyline silhouette along the white band's lower edge (obelisk centre-left).
    sil = (70, 110, 160)
    for (bx, bw, bh) in ((0.02, 0.07, 0.16), (0.10, 0.05, 0.22), (0.16, 0.08, 0.13),
                         (0.70, 0.06, 0.19), (0.77, 0.08, 0.14), (0.86, 0.05, 0.23),
                         (0.92, 0.06, 0.15)):
        d.rectangle([X(bx * w), X(0.68 * h - bh * h), X((bx + bw) * w), X(0.68 * h)], fill=sil)
    d.polygon([(X(0.335 * w), X(0.68 * h)), (X(0.345 * w), X(0.40 * h)),
               (X(0.355 * w), X(0.40 * h)), (X(0.365 * w), X(0.68 * h))], fill=sil)
    # Road strip at the bottom with dashes.
    d.rectangle([0, X(0.86 * h), X(w), X(h)], fill=(40, 44, 52))
    for i in range(7):
        d.line([X(0.04 * w + i * 0.14 * w), X(0.93 * h), X(0.11 * w + i * 0.14 * w), X(0.93 * h)],
               fill=(240, 240, 240), width=X(1.6))
    # Car, larger, sitting on the road.
    cy = 0.62 * h
    d.polygon([(X(0.10 * w), X(cy + 9)), (X(0.15 * w), X(cy - 3)), (X(0.30 * w), X(cy - 5)),
               (X(0.42 * w), X(cy - 15)), (X(0.64 * w), X(cy - 15)), (X(0.78 * w), X(cy - 4)),
               (X(0.89 * w), X(cy + 2)), (X(0.90 * w), X(cy + 9))], fill=(18, 22, 30))
    d.rectangle([X(0.10 * w), X(cy + 8), X(0.90 * w), X(cy + 12)], fill=(18, 22, 30))
    for wx in (0.26, 0.74):
        d.ellipse([X(wx * w - 7), X(cy + 5), X(wx * w + 7), X(cy + 19)], fill=(10, 12, 16))
        d.ellipse([X(wx * w - 3), X(cy + 9.5), X(wx * w + 3), X(cy + 14.5)], fill=(150, 156, 164))
    d.polygon([(X(0.45 * w), X(cy - 13)), (X(0.61 * w), X(cy - 13)), (X(0.65 * w), X(cy - 5)),
               (X(0.44 * w), X(cy - 5))], fill=(168, 206, 232))
    d.text((X(8), X(4)), "BUENOS AIRES", font=font(SANS_B, 9), fill=(16, 40, 66))


def sc_turtle(img, d, w, h):
    """A big sea turtle over sand, coral and light rays — v3: fuller."""
    vgrad(img, (0, 0, X(w), X(h)), (150, 208, 200), (226, 214, 168))
    # Light rays from the surface.
    for (rx, rw) in ((0.18, 0.05), (0.44, 0.07), (0.72, 0.05)):
        d.polygon([(X(rx * w), 0), (X((rx + rw) * w), 0),
                   (X((rx + rw + 0.10) * w), X(h)), (X((rx + 0.10) * w), X(h))],
                  fill=(255, 255, 255, 26))
    # Sand band with ripple arcs.
    d.rectangle([0, X(0.84 * h), X(w), X(h)], fill=(232, 220, 178))
    for i in range(6):
        d.arc([X(0.05 * w + i * 0.16 * w), X(0.86 * h), X(0.16 * w + i * 0.16 * w), X(0.99 * h)],
              180, 330, fill=(200, 184, 140), width=X(1.1))
    # Coral fans bottom corners.
    for (cx, col) in ((0.06, (232, 120, 110)), (0.94, (240, 150, 90))):
        for ang in (-50, -25, 0, 25, 50):
            ex = cx * w + 12 * math.sin(math.radians(ang))
            ey = h - 11 * math.cos(math.radians(ang))
            d.line([X(cx * w), X(h), X(ex), X(ey)], fill=col, width=X(1.8))
            d.ellipse([X(ex - 1.8), X(ey - 1.8), X(ex + 1.8), X(ey + 1.8)], fill=col)
    # Turtle, ~1.6x v2's, centre.
    cx, cy = 0.47 * w, 0.50 * h
    for (fx, fy, ang) in ((0.315, 0.26, -30), (0.625, 0.26, 30), (0.32, 0.74, 30), (0.62, 0.74, -30)):
        d.ellipse([X(fx * w - 14), X(fy * h - 7), X(fx * w + 14), X(fy * h + 7)], fill=(52, 110, 84))
    d.ellipse([X(cx - 34), X(cy - 18), X(cx + 34), X(cy + 18)], fill=(64, 128, 92))
    d.ellipse([X(cx - 26), X(cy - 13), X(cx + 26), X(cy + 13)], outline=(34, 84, 58), width=X(1.8))
    d.ellipse([X(cx - 11), X(cy - 7), X(cx + 11), X(cy + 7)], outline=(34, 84, 58), width=X(1.3))
    d.ellipse([X(cx - 24), X(cy - 4), X(cx - 12), X(cy + 5)], outline=(34, 84, 58), width=X(1.1))
    d.ellipse([X(cx + 12), X(cy - 4), X(cx + 24), X(cy + 5)], outline=(34, 84, 58), width=X(1.1))
    d.ellipse([X(cx + 34), X(cy - 7), X(cx + 46), X(cy + 7)], fill=(64, 128, 92))
    d.ellipse([X(cx + 41.5), X(cy - 2.2), X(cx + 44), X(cy + 0.3)], fill=(16, 30, 22))
    # Small fish silhouettes, right.
    for (fx, fy, fs) in ((0.82, 0.30, 6), (0.88, 0.42, 4.6), (0.79, 0.55, 3.8)):
        d.polygon([(X(fx * w - fs), X(fy * h)), (X(fx * w + fs * 0.4), X(fy * h - fs * 0.45)),
                   (X(fx * w + fs * 0.4), X(fy * h + fs * 0.45))], fill=(44, 96, 120))
        d.polygon([(X(fx * w + fs * 0.4), X(fy * h)), (X(fx * w + fs), X(fy * h - fs * 0.5)),
                   (X(fx * w + fs), X(fy * h + fs * 0.5))], fill=(44, 96, 120))
    for i in range(5):  # sea grass, taller
        gx = 0.10 * w + i * 0.05 * w
        d.arc([X(gx), X(0.45 * h), X(gx + 13), X(1.02 * h)], 90, 200, fill=(44, 120, 80), width=X(1.7))
    for (bx, by, br) in ((0.70, 0.24, 2.6), (0.76, 0.15, 1.8), (0.66, 0.12, 1.4)):
        d.ellipse([X(bx * w - br), X(by * h - br), X(bx * w + br), X(by * h + br)],
                  outline=(255, 255, 255), width=X(1))
    d.text((X(8), X(4)), "PERTH", font=font(SANS_B, 9), fill=(24, 70, 60))


def sc_nz(img, d, w, h):
    """Hills with wind turbines above a drifting boat — v3: the carbon
    story gets its landscape; rudder loose, dashed drift path."""
    vgrad(img, (0, 0, X(w), X(h)), (146, 196, 224), (96, 146, 184))
    # Green hill band.
    hills = [(0, 0.52), (0.14, 0.38), (0.30, 0.46), (0.46, 0.34), (0.62, 0.44),
             (0.78, 0.36), (0.90, 0.44), (1.0, 0.40), (1.0, 0.56), (0, 0.56)]
    d.polygon([(X(a * w), X(b * h)) for a, b in hills], fill=(86, 148, 92))
    # Wind turbines on the ridge.
    for (tx, ty, s) in ((0.22, 0.415, 9), (0.52, 0.375, 11), (0.84, 0.40, 8)):
        d.line([X(tx * w), X(ty * h), X(tx * w), X((ty - 0.16) * h + 0)], fill=(240, 244, 246), width=X(1.6))
        cy2 = (ty - 0.16) * h
        for ang in (90, 210, 330):
            d.line([X(tx * w), X(cy2), X(tx * w + s * 0.55 * math.cos(math.radians(ang))),
                    X(cy2 + s * 0.55 * math.sin(math.radians(ang)))],
                   fill=(240, 244, 246), width=X(1.5))
    d.rectangle([0, X(0.56 * h), X(w), X(h)], fill=(40, 96, 140))
    for i in range(4):
        y = 0.66 * h + i * 0.08 * h
        d.arc([X(0.06 * w + i * 22), X(y - 4), X(0.30 * w + i * 22), X(y + 5)], 180, 330,
              fill=(150, 200, 230), width=X(1.2))
    bx, by = 0.38 * w, 0.60 * h
    d.polygon([(X(bx - 27), X(by)), (X(bx + 27), X(by)), (X(bx + 18), X(by + 8)), (X(bx - 18), X(by + 8))],
              fill=(120, 62, 30))
    d.line([X(bx), X(by), X(bx), X(by - 30)], fill=(60, 44, 30), width=X(2.2))
    d.polygon([(X(bx + 2), X(by - 30)), (X(bx + 2), X(by - 3)), (X(bx + 20), X(by - 3))], fill=(246, 244, 238))
    d.polygon([(X(bx - 2), X(by - 25)), (X(bx - 2), X(by - 3)), (X(bx - 15), X(by - 3))], fill=(226, 220, 204))
    d.polygon([(X(0.72 * w), X(0.56 * h)), (X(0.79 * w), X(0.58 * h)), (X(0.765 * w), X(0.76 * h)),
               (X(0.71 * w), X(0.72 * h))], fill=(178, 40, 40))
    for t in range(7):
        u = t / 6
        d.ellipse([X((0.50 + 0.17 * u) * w), X((0.47 + 0.07 * u) * h),
                   X((0.50 + 0.17 * u) * w + 2.6), X((0.47 + 0.07 * u) * h + 2.6)], fill=(240, 240, 230))
    d.text((X(8), X(4)), "CARBON MARKET ADRIFT", font=font(SANS_B, 9), fill=(18, 44, 66))


def sc_antarctica(img, d, w, h):
    """Bergs, a research station and two penguins — v3: fuller shelf."""
    vgrad(img, (0, 0, X(w), X(h)), (196, 224, 240), (232, 242, 248))
    d.ellipse([X(0.04 * w), X(0.05 * h), X(0.13 * w), X(0.30 * h)], fill=(250, 238, 190))
    d.rectangle([0, X(0.62 * h), X(w), X(h)], fill=(120, 178, 214))
    bergs = [(0.06, 0.30, 0.30, 0.62), (0.58, 0.22, 0.86, 0.62), (0.84, 0.38, 0.99, 0.62)]
    for (ax, ay, bx2, by2) in bergs:
        d.polygon([(X(ax * w), X(by2 * h)), (X(ax * w + 6), X(ay * h + 8)), (X((ax + bx2) / 2 * w), X(ay * h)),
                   (X(bx2 * w - 5), X(ay * h + 10)), (X(bx2 * w), X(by2 * h))], fill=(246, 250, 252))
        d.polygon([(X((ax + bx2) / 2 * w), X(ay * h)), (X(bx2 * w - 5), X(ay * h + 10)),
                   (X(bx2 * w), X(by2 * h)), (X((ax + bx2) / 2 * w + 6), X(by2 * h))], fill=(206, 228, 240))
    # Research station on the shelf, left: two red huts + mast.
    d.rectangle([0, X(0.80 * h), X(w), X(h)], fill=(240, 247, 250))
    d.rectangle([X(0.07 * w), X(0.70 * h), X(0.17 * w), X(0.82 * h)], fill=(178, 44, 44))
    d.polygon([(X(0.065 * w), X(0.70 * h)), (X(0.12 * w), X(0.645 * h)), (X(0.175 * w), X(0.70 * h))],
              fill=(240, 244, 246))
    d.rectangle([X(0.185 * w), X(0.735 * h), X(0.25 * w), X(0.82 * h)], fill=(198, 60, 50))
    d.line([X(0.30 * w), X(0.82 * h), X(0.30 * w), X(0.60 * h)], fill=(60, 66, 74), width=X(1.6))
    d.line([X(0.30 * w), X(0.60 * h), X(0.335 * w), X(0.60 * h)], fill=(60, 66, 74), width=X(1.6))
    d.rectangle([X(0.335 * w), X(0.585 * h), X(0.375 * w), X(0.625 * h)], fill=RED)
    crack = [(0, 0.88), (0.2, 0.85), (0.38, 0.90), (0.55, 0.86), (0.72, 0.91), (0.88, 0.87), (1.0, 0.90)]
    d.line([(X(a * w), X(b * h)) for a, b in crack], fill=(30, 90, 140), width=X(2.4))
    # Two penguins, right.
    for (px, py, s) in ((0.90, 0.70, 1.0), (0.845, 0.735, 0.62)):
        pxw, pyh = px * w, py * h
        d.ellipse([X(pxw - 4.5 * s), X(pyh - 9 * s), X(pxw + 4.5 * s), X(pyh + 9 * s)], fill=(18, 22, 28))
        d.ellipse([X(pxw - 2.4 * s), X(pyh - 2 * s), X(pxw + 2.4 * s), X(pyh + 7 * s)], fill=WHITE)
        d.polygon([(X(pxw + 4 * s), X(pyh - 6 * s)), (X(pxw + 7 * s), X(pyh - 4.6 * s)),
                   (X(pxw + 4 * s), X(pyh - 3.4 * s))], fill=(240, 150, 40))
    d.text((X(8), X(4)), "THE ICE SHEET", font=font(SANS_B, 9), fill=(30, 80, 120))


def sc_tbilisi(img, d, w, h):
    """Damaged block at night, two searchlights and a crane — v3."""
    vgrad(img, (0, 0, X(w), X(h)), (18, 22, 44), (44, 48, 78))
    stars(d, (0, 0, X(w), X(h)), 16, 5)
    d.polygon([(X(0.03 * w), X(0.96 * h)), (X(0.62 * w), X(0.30 * h)), (X(0.70 * w), X(0.52 * h))],
              fill=(255, 240, 180, 52))
    d.polygon([(X(0.99 * w), X(0.94 * h)), (X(0.60 * w), X(0.34 * h)), (X(0.52 * w), X(0.52 * h))],
              fill=(200, 220, 255, 36))
    # Crane silhouette top-left.
    d.line([X(0.06 * w), X(0.94 * h), X(0.06 * w), X(0.10 * h)], fill=(8, 10, 18), width=X(2.6))
    d.line([X(0.06 * w), X(0.10 * h), X(0.44 * w), X(0.10 * h)], fill=(8, 10, 18), width=X(2.2))
    d.line([X(0.40 * w), X(0.10 * h), X(0.40 * w), X(0.24 * h)], fill=(8, 10, 18), width=X(1.2))
    d.rectangle([X(0.375 * w), X(0.24 * h), X(0.425 * w), X(0.30 * h)], fill=(8, 10, 18))
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
    d.polygon([(X(0.30 * w), X(0.94 * h)), (X(0.48 * w), X(0.62 * h)), (X(0.66 * w), X(0.94 * h))],
              fill=(52, 54, 68))
    d.polygon([(X(0.40 * w), X(0.94 * h)), (X(0.52 * w), X(0.74 * h)), (X(0.62 * w), X(0.94 * h))],
              fill=(66, 68, 84))
    d.rectangle([X(0.02 * w), X(0.90 * h), X(0.10 * w), X(0.97 * h)], fill=(10, 12, 22))
    d.ellipse([X(0.035 * w), X(0.86 * h), X(0.085 * w), X(0.93 * h)], fill=(255, 240, 180))
    # Emergency light dots at the base.
    d.ellipse([X(0.13 * w), X(0.90 * h), X(0.16 * w), X(0.945 * h)], fill=(220, 50, 50))
    d.ellipse([X(0.175 * w), X(0.90 * h), X(0.205 * w), X(0.945 * h)], fill=(70, 120, 255))
    d.text((X(8), X(4)), "TBILISI · NIGHT RESCUE", font=font(SANS_B, 9), fill=(220, 226, 244))


# ------------------------------------------------------------------- data
# Same stories, same order, same datelines as v2 — only the scene
# functions and the stat strip change.
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

# v3 stat strip: the strongest numbers already inside the verified
# story data (panel 1's gusts, brief 15's debut value, panel 4's Kospi,
# panel 3's nations, panel 13's hours, brief 16's Dow points).
STATS = [
    ("110 km/h", "Akvan’s gusts at Odisha landfall"),
    ("$1.76tn", "Anthropic’s value on Nasdaq debut (*)"),
    ("−4.7%", "Kospi: Asia’s worst week since 2020"),
    ("~200", "nations at COP31’s final day"),
    ("8 hours", "a Tbilisi girl, 3, spent in rubble"),
    ("−1,101", "Dow points in Wall St’s fifth straight loss (*)"),
]


# ----------------------------------------------------------------- layout
# Geometry identical to draw2.py (proven to fit every text); only the
# scenes, stats and finish changed.
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
           font(SERIF_I, 14.5), (92, 87, 79))
    d.rectangle([X(M), X(117), X(W - M), X(120)], fill=INK)
    d.rectangle([X(M), X(122.5), X(W - M), X(123.5)], fill=INK)


def draw_stats(d):
    y = 131
    cw = CW / 6
    for i, (num, label) in enumerate(STATS):
        cx = M + i * cw
        d.rectangle([X(cx), X(y), X(cx + 2.5), X(y + 33)], fill=RED)
        nf = fit_font(d, num, SERIF_B, 23, cw - 16, min_size=15)
        d.text((X(cx + 9), X(y - 2)), num, font=nf, fill=INK)
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
    # v5 bold: square corners, strong near-black frame (v3 style).
    d.rectangle([X(x), X(y), X(x + w), X(y + h)], fill=PANEL)
    d.rectangle([X(x), X(y), X(x + w), X(y + h)], outline=(24, 24, 27), width=X(1))


def draw_lead(img, d, x, y, w, h, item):
    num, story, dateline, scenefn = item
    cont, _glyph, head, detail, src = story
    panel_base(d, x, y, w, h)
    sub, sd = scene_canvas(w, 110)
    scenefn(sub, sd, w, 110)
    paste_scene(img, sub, x, y)
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
          font(SERIF, 12), (74, 70, 64), 14.5)
    d.text((X(x + 10), X(y + h - 16)), f"({src})", font=font(SERIF_I, 9.5), fill=MUTED)


def draw_feature(img, d, x, y, w, h, item):
    num, story, dateline, scenefn = item
    cont, _glyph, head, detail, src = story
    panel_base(d, x, y, w, h)
    sub, sd = scene_canvas(w, 46)
    scenefn(sub, sd, w, 46)
    paste_scene(img, sub, x, y)
    d.rectangle([X(x), X(y + 46), X(x + w), X(y + 48.5)], fill=CONTINENT_COLORS[cont])
    d.text((X(x + 7), X(y + 52)), f"{num:02d} · {dateline}",
           font=font(SANS_B, 8), fill=(98, 94, 86))
    yy = block(d, x + 7, y + 63, wrap(d, head, font(SERIF_B, 12), X(w - 14)),
               font(SERIF_B, 12), INK, 14)
    block(d, x + 7, yy + 2.5, wrap(d, detail, font(SANS, 9), X(w - 14)),
          font(SANS, 9), (76, 72, 66), 11.5)
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
            d.text((x2 + d.textlength(ps, font=pf), X(yy)), text, font=tf, fill=INK)
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
          font(SANS, 9.5), (74, 70, 64), 12)
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
    # v5 bold: no paper grain — flat colour, deepened per-scene in
    # deepen_scene() and unified by the bold palette above.
    img = img.resize((W, H), Image.LANCZOS)
    img.save(OUT, optimize=True)
    import os
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}, {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
