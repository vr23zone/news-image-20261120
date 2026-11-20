// main.ts — news-image-20261120 entry: "One Day, One Orbit".
//
// Copies the pre-rendered entry.png (drawn by draw.py, PIL, deterministic)
// to $MAKEFUN_OUTPUT_DIR (default /output). Node 22, stdlib only, no network.
//
// Final entry: 37 stories from Friday 20 November 2026 across 8 continents
// (Asia 11, Europe 10, North America 7, South America 5, Africa 1,
// Antarctica 1, Oceania 1, Zealandia 1) — 12 illustrated panels on the
// day's orbit arc plus a 25-story wire. Render verified deterministic:
// draw.py run twice gives byte-identical entry.png (1024x1024, 174029 bytes).
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
