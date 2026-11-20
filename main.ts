// main.ts — news-image-20261120 entry: "One Day, One Orbit".
//
// Copies the pre-rendered entry.png (drawn by draw5.py, PIL,
// deterministic; draw5.py imports the verified story data from draw.py
// unchanged, via draw2.py) to $MAKEFUN_OUTPUT_DIR (default /output).
// Node 22, stdlib only, no network.
//
// Final entry (v5 BOLD broadsheet): 37 stories from Friday 20 November 2026
// across 8 continents (Asia 11, Europe 10, North America 7, South America
// 5, Africa 1, Antarctica 1, Oceania 1, Zealandia 1) — 13 illustrated
// panels plus a 24-story briefs list and a pinned world map. V5 is built
// on the v3 cream version and keeps its layout and stories exactly, but
// renders it bold and deep on a FULL yellow page: flat deep yellow
// background (#F2B705) everywhere, pale yellow-cream panels (#FEF4CD),
// a saturated deep palette (HLS saturation x1.35, lightness x0.93),
// deep crimson accents (166,14,32), strong near-black ink (13,14,17),
// per-scene deepening (saturation x1.32, contrast x1.07), and square
// panels with a strong near-black frame — all text sharp and readable.
// Render verified deterministic: draw5.py run twice gives
// byte-identical entry.png (1024x1024, 669724 bytes).
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
