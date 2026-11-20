// main.ts — news-image-20261120 entry: "One Day, One Orbit".
//
// Copies the pre-rendered entry.png (drawn by draw2.py, PIL + numpy,
// deterministic; draw2.py imports the verified story data from draw.py,
// the v1 design) to $MAKEFUN_OUTPUT_DIR (default /output). Node 22,
// stdlib only, no network.
//
// Final entry (v2 broadsheet): 37 stories from Friday 20 November 2026
// across 8 continents (Asia 11, Europe 10, North America 7, South America
// 5, Africa 1, Antarctica 1, Oceania 1, Zealandia 1) — 13 illustrated
// panels plus a 24-story briefs list and a pinned world map. Render
// verified deterministic: draw2.py run twice gives byte-identical
// entry.png (1024x1024, 1031729 bytes).
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
