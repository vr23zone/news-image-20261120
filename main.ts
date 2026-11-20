// main.ts — news-image-20261120 entry: "One Day, One Orbit".
//
// Copies the pre-rendered entry.png (drawn by draw4.py, PIL,
// deterministic; draw4.py imports the verified story data from draw.py
// unchanged, via draw2.py) to $MAKEFUN_OUTPUT_DIR (default /output).
// Node 22, stdlib only, no network.
//
// Final entry (v4 SOFT broadsheet): 37 stories from Friday 20 November 2026
// across 8 continents (Asia 11, Europe 10, North America 7, South America
// 5, Africa 1, Antarctica 1, Oceania 1, Zealandia 1) — 13 illustrated
// panels plus a 24-story briefs list and a pinned world map. V4 is built
// on the v3 cream version and keeps its layout and stories exactly, but
// softens the rendering throughout: a muted pastel palette (saturation
// x0.68, lightened), soft charcoal ink instead of black, soft warm
// cream paper (#F7F2E7), per-scene softening (gentle shading wash,
// light blur blend, warm tint), rounded panel corners, and a soft
// terracotta DATE CHECK box — while all text stays sharp and readable.
// Render verified deterministic: draw4.py run twice gives
// byte-identical entry.png (1024x1024, 676653 bytes).
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
