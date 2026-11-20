#!/usr/bin/env python3
"""draw.py — "One Day, One Orbit": Friday 20 November 2026 world news in one image.

Concept: the day as one orbit of the Earth. A timeline runs from Auckland
sunrise to Honolulu midnight; 12 featured stories are pinned along the day's
arc as illustrated panels, each tagged with its continent, and 25 more stories
run as a compact wire below. 37 stories, 8 continents (Africa, Antarctica,
Asia, Europe, North America, Oceania, South America, Zealandia).

Deterministic: fixed layout, fixed fonts, fixed emoji tiles rendered from the
system Noto Color Emoji strike (size 109) and downscaled. Run twice and the
bytes are identical. Output: entry.png, 1024x1024, <= 1 MiB.

No recognisable face of a real person is drawn anywhere: every panel uses a
generic emoji symbol or a drawn shape, never a likeness.

Story sources are listed per story in STORIES / WIRE below and in README.md.
Dates: every story happened on, or was first reported on, 20 November 2026,
except where the README notes a 19 Nov event whose coverage dominated 20 Nov.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

# Palette — deep night-sky header, warm paper body, high-contrast ink text.
NAVY = (11, 31, 58)
NAVY2 = (16, 46, 84)
PAPER = (247, 243, 232)
CARD = (255, 255, 255)
INK = (18, 24, 34)
MUTED = (74, 84, 100)
GOLD = (212, 160, 32)
WHITE = (255, 255, 255)
LINE = (203, 210, 220)

CONTINENT_COLORS = {
    "AFRICA": (176, 92, 20),       # ochre
    "ANTARCTICA": (46, 134, 193),  # ice blue
    "ASIA": (178, 34, 52),         # crimson
    "EUROPE": (36, 90, 166),       # royal blue
    "NORTH AMERICA": (20, 120, 90),  # teal
    "OCEANIA": (0, 130, 150),      # ocean
    "SOUTH AMERICA": (34, 139, 60),  # green
    "ZEALANDIA": (104, 74, 160),   # violet
}


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(SANS_B, 44)
F_DATE = font(SANS_B, 25)
F_SUB = font(SANS, 16)
F_TAG = font(SANS_B, 11)
F_HEAD = font(SANS_B, 16)
F_BODY = font(SANS, 13)
F_WIRE = font(SANS, 12)
F_WIRE_B = font(SANS_B, 12)
F_FOOT = font(SANS, 12)
F_STRIP = font(SANS_B, 12)

_emoji_cache = {}


def emoji_tile(glyph, size):
    """Render one colour-emoji glyph at the font's bitmap strike (109) and
    downscale it to `size` px. Cached, deterministic."""
    key = (glyph, size)
    if key in _emoji_cache:
        return _emoji_cache[key]
    big = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    f = ImageFont.truetype(EMOJI, 109)
    d.text((5, 5), glyph, font=f, embedded_color=True)
    tile = big.resize((size, size), Image.LANCZOS)
    _emoji_cache[key] = tile
    return tile


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_header(d):
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    # Small orbit glyph: sun arc over a globe dot row.
    d.ellipse([24, 26, 78, 80], outline=GOLD, width=3)
    d.arc([30, 32, 72, 74], 200, 340, fill=GOLD, width=3)
    d.ellipse([44, 46, 58, 60], fill=GOLD)
    d.text((96, 20), "ONE DAY, ONE ORBIT", font=F_TITLE, fill=WHITE)
    d.text((98, 72), "FRIDAY  20  NOVEMBER  2026", font=F_DATE, fill=(255, 214, 90))
    d.text((98, 96), "The world in one turn — from Auckland sunrise to Honolulu midnight  •  37 stories  •  8 continents",
           font=font(SANS, 15), fill=(205, 216, 232))


def draw_orbit_strip(d):
    """The day's arc: 8 continent waypoints, west to east, on one orbit line."""
    d.rectangle([0, 122, W, 164], fill=(233, 226, 208))
    stops = [
        ("AUCKLAND", "OCEANIA"), ("SYDNEY", "OCEANIA"), ("TOKYO", "ASIA"),
        ("DELHI", "ASIA"), ("ANTALYA", "EUROPE"), ("PARIS", "EUROPE"),
        ("NEW YORK", "NORTH AMERICA"), ("HONOLULU", "NORTH AMERICA"),
    ]
    d.arc([60, 118, 964, 210], 180, 360, fill=(150, 158, 172), width=3)
    step = (W - 120) / (len(stops) - 1)
    for i, (place, cont) in enumerate(stops):
        x = 60 + int(i * step)
        col = CONTINENT_COLORS[cont]
        d.ellipse([x - 7, 128, x + 7, 142], fill=col, outline=WHITE, width=2)
        label = place
        tw = d.textlength(label, font=F_TAG)
        d.text((x - tw / 2, 146), label, font=F_TAG, fill=INK)


def draw_panel(img, d, x, y, w, h, story):
    """One featured panel: continent colour bar, emoji scene, tag, headline,
    one-line detail. story = (continent, glyph, headline, detail, source)."""
    cont, glyph, head, detail, _src = story
    col = CONTINENT_COLORS[cont]
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                        outline=LINE, width=1)
    d.rounded_rectangle([x, y, x + w, y + 6], radius=3, fill=col)
    d.rounded_rectangle([x, y + 3, x + w, y + 6], fill=col)
    # Emoji scene in a soft tinted square.
    tint = tuple(min(255, c + 165) for c in col)
    d.rounded_rectangle([x + 10, y + 16, x + 58, y + 64], radius=8, fill=tint)
    tile = emoji_tile(glyph, 40)
    img.paste(tile, (x + 13, y + 19), tile)
    d.text((x + 68, y + 17), cont, font=F_TAG, fill=col)
    tx = x + 68
    tw = w - 78
    lines = wrap(d, head, F_HEAD, tw)[:3]
    text_block(d, tx, y + 33, lines, F_HEAD, INK, 19)
    dlines = wrap(d, detail, F_BODY, w - 20)[:2]
    text_block(d, x + 10, y + h - 12 - 15 * len(dlines), dlines, F_BODY, MUTED, 15)


def draw_wire(d, y0):
    """Compact wire: 25 one-line stories in two columns (13 + 12)."""
    d.text((16, y0), "ALSO TODAY — 25 MORE STORIES    (*) 19 Nov event, a top story on 20 Nov", font=F_STRIP, fill=NAVY)
    d.line([16, y0 + 20, W - 16, y0 + 20], fill=GOLD, width=2)
    col_w = (W - 32 - 24) // 2
    for col_i, items in enumerate((WIRE[:13], WIRE[13:])):
        x = 16 + col_i * (col_w + 24)
        y = y0 + 28
        for cont, head in items:
            col = CONTINENT_COLORS[cont]
            d.ellipse([x, y + 4, x + 7, y + 11], fill=col)
            d.text((x + 12, y), head, font=F_WIRE, fill=INK)
            y += 14
    return y0 + 28 + 13 * 14


def draw_footer(d, y):
    d.rectangle([0, y, W, H], fill=NAVY)
    d.text((16, y + 8),
           "37 stories from Friday 20 November 2026 — sources: Reuters, BBC, AP, The Independent, IMD, UN News, FIFA, Scimex. Full list in README.md",
           font=F_FOOT, fill=(205, 216, 232))


# ---------------------------------------------------------------- stories
# Featured panels: (continent, emoji glyph, headline, detail, source).
# All 12 happened on 20 Nov 2026. Glyphs are generic symbols, never a face.
STORIES = [
    ("ASIA", "\U0001F300", "Cyclone Akvan hits Odisha coast",
     "Landfall near Gopalpur; winds 70–80 km/h, heavy rain.",
     "IMD bulletin 20 Nov; The Hindu live blog"),
    ("EUROPE", "\U0001F30D", "COP31 closes in Antalya",
     "Final climate text due at midnight; ~200 nations.",
     "UN News COP31 page; Fresh Energy, 19–20 Nov"),
    ("NORTH AMERICA", "\u23F3", "Trump: no Iran call until 2027",
     "\u201cWe\u2019ll see what happens after January 1,\u201d he says.",
     "Channel 12 interview, reported 20 Nov (Azernews)"),
    ("ASIA", "\U0001F4C9", "Asian markets slide again",
     "Nikkei -4.1%, Kospi -4.7%; worst week since 2020.",
     "Reuters, 20 Nov"),
    ("EUROPE", "\U0001F4A5", "Missiles strike Kyiv",
     "Russian ballistic missiles hit a power plant.",
     "The Independent live blog, 20 Nov"),
    ("ASIA", "\U0001F680", "Houthis hit four Saudi targets",
     "Missile strikes Riyadh\u2019s tallest tower.",
     "TASS via Stockbiz, 20 Nov"),
    ("ASIA", "\U0001F6E2\uFE0F", "Tanker ablaze after mine strike",
     "Fire east of the Strait of Hormuz.",
     "Daily Baku, 20 Nov 01:27"),
    ("EUROPE", "\u2708\uFE0F", "Drones halt Genoa airport",
     "Flights suspended after unidentified drones seen.",
     "Daily Baku, 20 Nov 04:22"),
    ("SOUTH AMERICA", "\U0001F697", "Tesla opens sales in Argentina",
     "Model 3 and Model Y on sale from today.",
     "Rio Times, 20 Nov"),
    ("OCEANIA", "\U0001F422", "Lab-hatched turtle survives",
     "A wild survivor gives hope for Perth\u2019s turtles.",
     "Scimex / Murdoch University, 20 Nov"),
    ("ZEALANDIA", "\U0001F343", "NZ carbon market \u2018rudderless\u2019",
     "Researchers warn the emissions scheme is drifting.",
     "Motu Research via Scimex, 20 Nov"),
    ("ANTARCTICA", "\U0001F9CA", "COP31\u2019s last day: ice on the line",
     "Antarctic ice-sheet projections set the sea-level stakes.",
     "Australian Antarctic Program, 11 Nov; COP31 close 20 Nov"),
]

# Wire: (continent, one-line headline). Each <= 70 chars, one line at 12 pt.
# Items marked (*) happened 19 Nov but dominated 20 Nov coverage; see README.
WIRE = [
    ("ASIA", "Trump, Xi and Putin issue peace declaration in Shenzhen (*)"),
    ("NORTH AMERICA", "Anthropic shares close 17% up on Nasdaq debut, worth $1.76tn (*)"),
    ("NORTH AMERICA", "Wall Street: S&P 500 -2.0%, Dow -1,101 pts, fifth straight loss (*)"),
    ("EUROPE", "Europe says it is ready for talks with Russia on Ukraine"),
    ("EUROPE", "Kamala Harris meets Macron in Paris amid 2028 speculation"),
    ("EUROPE", "Dutch summon Russian envoy after blast near Kyiv embassy"),
    ("ASIA", "Israeli strike hits Hezbollah missile site in east Lebanon"),
    ("EUROPE", "Three killed in drone attack on Russia's Saratov region"),
    ("EUROPE", "One dead, 15 hurt in fire at 18-storey block in France"),
    ("EUROPE", "Girl, 3, pulled from rubble 8 hours after Tbilisi gas blast"),
    ("EUROPE", "EU\u2013UK talks 'going down to the wire', says No 10"),
    ("NORTH AMERICA", "California probes Nvidia over China AI chip sales"),
    ("NORTH AMERICA", "White House names Kirsten Davies as cyber chief"),
    ("ASIA", "Taiwan acts to steady stocks; short-selling curbs begin"),
    ("ASIA", "Japan's Takaichi sidesteps Taiwan contingency question"),
    ("ASIA", "India judge: resignation is no admission of guilt"),
    ("ASIA", "Madhya Pradesh scraps two-child rule for state staff"),
    ("SOUTH AMERICA", "Brazil makes Chief Raoni's Kayapo homeland permanent (*)"),
    ("SOUTH AMERICA", "Brazil asks WTO for panel against US tariffs (*)"),
    ("SOUTH AMERICA", "US and Venezuela sign deal to restore military ties"),
    ("SOUTH AMERICA", "US backs Colombia plan to resume coca spraying"),
    ("NORTH AMERICA", "Christie's halts Frida Kahlo sale at Mexico's request"),
    ("NORTH AMERICA", "Heavy fighting in Haiti as forces battle gangs"),
    ("AFRICA", "Climate cash for Africa? Europe: use pledged money first"),
    ("ASIA", "U-17 World Cup: Brazil open campaign against Ireland"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    draw_orbit_strip(d)
    # 12 featured panels: 3 columns x 4 rows.
    pw = (W - 32 - 20) // 3
    ph, gap = 142, 8
    y0, x0 = 172, 16
    for i, story in enumerate(STORIES):
        r, c = divmod(i, 3)
        draw_panel(img, d, x0 + c * (pw + 10), y0 + r * (ph + gap),
                   pw, ph, story)
    wire_end = draw_wire(d, y0 + 4 * ph + 3 * gap + 8)
    draw_footer(d, 990)
    assert len(STORIES) == 12 and len(WIRE) == 25, "story count must be 37"
    assert wire_end <= 990, f"wire overruns footer: {wire_end}"
    img.save(OUT, optimize=True)
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
