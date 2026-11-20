# One Day, One Orbit — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/vr23zone/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/vr23zone/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

**Entry for [news-image-20261120](https://make.fun/c/news-image-20261120): "Sum up 20 November's world news in one image".**

## Concept

**One Day, One Orbit.** The day is one turn of the Earth: a timeline runs from
Auckland sunrise to Honolulu midnight, with eight continent waypoints pinned
along the arc. Twelve featured stories are illustrated panels (generic emoji
symbols — no recognisable face of any real person is drawn), each tagged with
its continent; 25 more stories run as a compact wire below. The date —
**Friday 20 November 2026** — is named in the masthead.

**Version 2** keeps the same 37 verified stories and
the One Day, One Orbit identity, redesigned as a classic broadsheet front
page after studying the competition's leading entries: cream paper with a
fine deterministic grain, a huge serif masthead, a six-number stat strip, a
continent tally bar, three large scene-illustrated leads, ten more
illustrated panels, a pinned world map, a dense numbered briefs list,
per-story source attributions, and a red DATE CHECK footer. It is drawn by
`draw2.py`, which imports the verified story data from `draw.py` unchanged;
all artwork is original flat illustration (no photographs, no likenesses).
In the v2 image the 13 drawn panels are: 1 Akvan, 2 Kyiv, 3 COP31,
4 markets, 5 Houthis, 6 tanker, 7 Genoa, 8 Trump, 9 Tesla, 10 turtle,
11 NZ carbon market, 12 Antarctica, 13 Tbilisi (wire story 22 below,
promoted to a panel); the other 24 wire stories run as briefs numbered
14–37 in the order listed below.

**Version 3 (current `entry.png`)** keeps v2's layout, panel order and
every story, headline, detail and source exactly, and changes only the
artwork and finish — again after studying the provisional top entries
(judge 991+ vs v2's 983.9): the paper grain is gone (the leaders are
crisp flat colour, and the PNG drops from 1,031,729 to 693,749 bytes);
all 13 scenes are redrawn larger and denser so no panel is mostly empty
background — COP31 gains a delegates' table with flag poles under a
bigger globe and thermometer, the turtle, car, boat and ice scenes gain
their landscapes, and Kyiv gains searchlights and lit windows; and the
stat strip now leads with the strongest numbers already inside the
verified data (110 km/h gusts, Anthropic's $1.76tn debut value, the
Dow's −1,101 points) instead of the weakest ones. Drawn by `draw3.py`,
which imports the story data from `draw.py`/`draw2.py` unchanged.
**Revision:** the paper background is now a flat newsprint gray
(#D8D8D6, panels #E7E7E4) instead of cream — same stories, layout and
artwork, only the paper colour changed (693,749 → 667,485 bytes).

**Version 4 SOFT (current `entry.png`)** is built on the v3 CREAM
version (not the gray revision) and changes only the rendering, toward
a soft, calm editorial illustration: the whole palette is desaturated
~32% and lightened into muted pastels, ink becomes a soft charcoal
(#2E2A26, never pure black), the DATE CHECK red becomes a soft
terracotta, and the paper is a lighter warm cream (#F7F2E7) with
panels a touch lighter still. Each of the 13 scenes is softened as it
is pasted in — saturation ×0.68, contrast ×0.92, brightness ×1.04, a
gentle vertical shading wash inside the flat shapes, a light blur
blend that relaxes hard edges, and a 5% warm-paper tint — and panel
frames gain rounded top corners with a pale warm-gray outline. All 37
stories, headlines, layout, the stat strip, the COP31 panel, the map
pins and the DATE CHECK box are v3's, unchanged, and all text stays
sharp and fully readable. Drawn by `draw4.py`, which imports the story
data from `draw.py`/`draw2.py` unchanged.

**Version 5 BOLD (current `entry.png`)** is built on the v3 CREAM
version and combines Rohim's two instructions of 21 Nov 2026: colours
"lebih tebal dan pekat" (thicker/bolder, deeper) and "background full
nya warna kuning" (the full background is yellow). The whole canvas
background is one flat bold deep yellow (#F2B705), with panels in a
pale yellow-cream (#FEF4CD) so text stays readable while the page
reads unmistakably yellow everywhere. The palette goes the opposite
way from v4 SOFT: HLS saturation ×1.35 with lightness pulled down
×0.93 for rich, concentrated tones, a deep strong crimson
(166,14,32) for the DATE CHECK box and stat bars, strong near-black
ink (13,14,17), a deep navy map sea and rich golden-sand land. Each
of the 13 scenes is deepened as it is pasted in — saturation ×1.32,
contrast ×1.07, brightness ×0.99 — flat and crisp like v3 (no blur,
no pastel wash), and panels return to square corners with a strong
near-black frame. All 37 stories, headlines, layout, the stat strip,
the COP31 panel, the map pins and the DATE CHECK box are v3's,
unchanged, and all text stays sharp and fully readable. Drawn by
`draw5.py`, which imports the story data from `draw.py`/`draw2.py`
unchanged.

## The image

`entry.png` — 1024×1024, drawn deterministically by `draw5.py` (Python 3 +
PIL, Liberation Serif + Noto Sans). Running `draw5.py` twice
produces byte-identical output.

- **37 stories** in total: 13 drawn panels + 24 briefs (v1: 12 + 25).
- **8 continents:** Asia 11 · Europe 10 · North America 7 · South America 5 ·
  Africa 1 · Antarctica 1 · Oceania 1 · Zealandia 1.

## Featured stories (12)

1. **Asia — Cyclone Akvan hits Odisha coast.** Landfall near Gopalpur; winds
   70–80 km/h, heavy rain. *Source: India Meteorological Department bulletin,
   20 Nov; The Hindu live blog.*
2. **Europe — COP31 closes in Antalya.** Final climate text due at midnight;
   ~200 nations. *Source: UN News COP31 page; Fresh Energy, 19–20 Nov.*
3. **North America — Trump: no Iran call until 2027.** "We'll see what
   happens after January 1." *Source: Channel 12 interview, reported 20 Nov
   (Azernews; The Times of India).*
4. **Asia — Asian markets slide again.** Nikkei -4.1%, Kospi -4.7%; worst
   week since 2020. *Source: Reuters, 20 Nov.*
5. **Europe — Missiles strike Kyiv.** Russian ballistic missiles hit a power
   plant. *Source: The Independent live blog, 20 Nov.*
6. **Asia — Houthis hit four Saudi targets.** Missile strikes Riyadh's
   tallest tower. *Source: TASS via Stockbiz, 20 Nov; One Turn.*
7. **Asia — Tanker ablaze after mine strike.** Fire east of the Strait of
   Hormuz. *Source: Daily Baku, 20 Nov.*
8. **Europe — Drones halt Genoa airport.** Flights suspended after
   unidentified drones seen. *Source: Daily Baku, 20 Nov.*
9. **South America — Tesla opens sales in Argentina.** Model 3 and Model Y
   on sale from today. *Source: The Rio Times, 20 Nov.*
10. **Oceania — Lab-hatched turtle survives.** A wild survivor gives hope
    for Perth's turtles. *Source: Scimex / Murdoch University, 20 Nov.*
11. **Zealandia — NZ carbon market 'rudderless'.** Researchers warn the
    emissions scheme is drifting. *Source: Motu Research via Scimex, 20 Nov.*
12. **Antarctica — COP31's last day: ice on the line.** Antarctic ice-sheet
    projections set the sea-level stakes. *Source: Australian Antarctic
    Program, 11 Nov (projections); COP31 closing day, 20 Nov.*

## Also today — wire (25)

13. **Asia — Trump, Xi and Putin issue peace declaration in Shenzhen.**
    *Summit 19 Nov, reported 20 Nov (The Independent; TASS).*
14. **North America — Anthropic shares close 17% up on Nasdaq debut, worth
    $1.76tn.** *First trading 19 Nov, reported 20 Nov (Reuters; The Times of
    India).*
15. **North America — Wall Street: S&P 500 -2.0%, Dow -1,101 pts, fifth
    straight loss.** *19 Nov close, reported 20 Nov (Reuters; Longbridge).*
16. **Europe — Europe says it is ready for talks with Russia on Ukraine.**
    *BBC / Le Monde, 20 Nov.*
17. **Europe — Kamala Harris meets Macron in Paris amid 2028 speculation.**
    *Le Monde, 20 Nov.*
18. **Europe — Dutch summon Russian envoy after blast near Kyiv embassy.**
    *The Independent, 20 Nov.*
19. **Asia — Israeli strike hits Hezbollah missile site in east Lebanon.**
    *Daily Baku, 20 Nov.*
20. **Europe — Three killed in drone attack on Russia's Saratov region.**
    *Daily Baku, 20 Nov.*
21. **Europe — One dead, 15 hurt in fire at 18-storey block in France.**
    *Daily Baku, 20 Nov.*
22. **Europe — Girl, 3, pulled from rubble 8 hours after Tbilisi gas blast.**
    *Daily Baku, 20 Nov.*
23. **Europe — EU–UK talks 'going down to the wire', says No 10.** *BBC,
    20 Nov.*
24. **North America — California probes Nvidia over China AI chip sales.**
    *BBC, 20 Nov.*
25. **North America — White House names Kirsten Davies as cyber chief.**
    *Le Monde, 20 Nov.*
26. **Asia — Taiwan acts to steady stocks; short-selling curbs begin.**
    *SimpleLife / Taiwan FSC, 20 Nov.*
27. **Asia — Japan's Takaichi sidesteps Taiwan contingency question.**
    *SimpleLife, 20 Nov.*
28. **Asia — India judge: resignation is no admission of guilt.** *NDTV,
    20 Nov.*
29. **Asia — Madhya Pradesh scraps two-child rule for state staff.**
    *The Hindu, 20 Nov.*
30. **South America — Brazil makes Chief Raoni's Kayapó homeland permanent.**
    *Ceremony 19 Nov, reported 20 Nov (SAGIRE / AP).*
31. **South America — Brazil asks WTO for panel against US tariffs.**
    *Filed 19 Nov, reported 20 Nov (SAGIRE).*
32. **South America — US and Venezuela sign deal to restore military ties.**
    *BBC / AP, reported 20 Nov.*
33. **South America — US backs Colombia plan to resume coca spraying.**
    *AP via The Star, 20 Nov.*
34. **North America — Christie's halts Frida Kahlo sale at Mexico's request.**
    *AP via The Star, 20 Nov.*
35. **North America — Heavy fighting in Haiti as forces battle gangs.**
    *AP via The Star, 20 Nov.*
36. **Africa — Climate cash for Africa? Europe: use pledged money first.**
    *BBC, 20 Nov.*
37. **Asia — U-17 World Cup: Brazil open campaign against Ireland.**
    *FIFA, 20 Nov (matchday three, Qatar).*

Items marked `(*)` in the image happened on 19 Nov but were a top story of
20 Nov coverage; the image's wire legend says so, and this list gives the
exact dates. Nothing else is invented: every headline traces to a source
found on 20 Nov 2026.

## Run

```sh
python3 draw5.py           # renders entry.png v5 BOLD (1024x1024, deterministic, 669724 bytes)
python3 draw4.py           # renders the v4 SOFT design
python3 draw2.py           # renders the v2 design
python3 draw.py            # renders the v1 design
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies it to out/entry.png
```

`main.ts` (Node 22, stdlib only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR` (default `/output`).

## License

MIT — see [LICENSE](LICENSE).
