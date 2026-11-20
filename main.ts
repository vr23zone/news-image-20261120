// main.ts — news-image-20261120 entry: "One Day, One Orbit".
//
// Copies the pre-rendered entry.png (drawn by draw3.py, PIL,
// deterministic; draw3.py imports the verified story data from draw.py
// unchanged, via draw2.py) to $MAKEFUN_OUTPUT_DIR (default /output).
// Node 22, stdlib only, no network.
//
// Final entry (v3 broadsheet): 37 stories from Friday 20 November 2026
// across 8 continents (Asia 11, Europe 10, North America 7, South America
// 5, Africa 1, Antarctica 1, Oceania 1, Zealandia 1) — 13 illustrated
// panels plus a 24-story briefs list and a pinned world map. V3 keeps
// v2's layout and stories but redraws every scene larger and denser,
// drops the paper grain for the crisp flat finish the leading entries
// use, and leads the stat strip with the day's strongest numbers from
// the same verified data. Revision: paper background changed from
// cream to flat newsprint gray (#D8D8D6). Render verified
// deterministic: draw3.py run twice gives byte-identical entry.png
// (1024x1024, 667485 bytes).
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
