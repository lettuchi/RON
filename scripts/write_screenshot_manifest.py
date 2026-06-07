#!/usr/bin/env python3
"""Build screenshots/review-2026-06-02/manifest.md from captured PNGs."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW_DIR = os.path.join(ROOT, "screenshots", "review-2026-06-02")
MANIFEST_PATH = os.path.join(REVIEW_DIR, "manifest.md")

SKIP_NOTE = """
## Skipped (by design)

| Item | Reason |
|------|--------|
| Every internal `return` / helper label | Not player-visible |
| Full image-song sequences | First frame only in `cinematics/` (autoplay + long runtime) |
| Every prologue door branch permutation | CG catalog + canon-turn run cover representative beats |
| Case 2 full dialogue walkthrough | Case 2 opening + CG menus; extend `test_all_turns` for full Case 2 later |
| Non-canon full playthrough | `case1_noncanon_start` still captured; full verbal/walkout paths share many CGs |
| `test` / `after_menu_*` (Ren'Py template) | Dev-only sample script in `testcases.rpy` |
"""

CG_CATALOG_META = []
_meta_path = os.path.join(ROOT, "game", "test_screenshot_review.rpy")
if os.path.isfile(_meta_path):
    # Lightweight parse: ("path", "tag", "desc") tuples from REVIEW_CG_CATALOG
    import re

    block = open(_meta_path, encoding="utf-8").read()
    for m in re.finditer(
        r'\("([^"]+)",\s*"([^"]+)",\s*"([^"]+)"\)', block
    ):
        rel, tag, desc = m.groups()
        if rel.startswith("cg/"):
            CG_CATALOG_META.append((rel + ".png", tag, desc))


def collect_pngs(base: str) -> list[str]:
    out: list[str] = []
    if not os.path.isdir(base):
        return out
    for dirpath, _dirs, files in os.walk(base):
        for name in sorted(files):
            if name.lower().endswith(".png") and not name.endswith(".new.png"):
                rel = os.path.relpath(os.path.join(dirpath, name), base).replace("\\", "/")
                out.append(rel)
    return sorted(out)


def main() -> int:
    os.makedirs(REVIEW_DIR, exist_ok=True)
    pngs = collect_pngs(REVIEW_DIR)
    tag_by_file = {os.path.basename(p): (tag, desc) for p, tag, desc in ((m[0], m[1], m[2]) for m in CG_CATALOG_META)}

    reports: dict[str, object] = {}
    for name in ("cg-catalog-report.json", "canon-turns/run-report.json"):
        path = os.path.join(REVIEW_DIR, name.replace("/", os.sep))
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                reports[name] = json.load(f)

    lines = [
        "# Screenshot review manifest",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"Resolution: 1280×720 (project default via `gui.init(1280, 720)`)",
        f"Total PNGs: **{len(pngs)}**",
        "",
        "## Re-run capture",
        "",
        "```bat",
        "_run_screenshot_review.bat",
        "```",
        "",
        "Individual suites:",
        "",
        "```bat",
        "C:\\Users\\Amanda\\Developer\\renpy-sdk\\renpy-8.5.3-sdk\\renpy.exe ryoko-owari test screenshot_review_cg::review_cg_catalog_generated --overwrite-screenshots",
        "C:\\Users\\Amanda\\Developer\\renpy-sdk\\renpy-8.5.3-sdk\\renpy.exe ryoko-owari test screenshot_all_turns::canon_all_dialogue --overwrite-screenshots",
        "```",
        "",
        "## Output layout",
        "",
        "| Folder | Contents |",
        "|--------|----------|",
        "| `cg/` | All gallery-tagged CGs and choice moments (static poses) |",
        "| `story/` | Key label entry frames (prologue, cases, branches) |",
        "| `endings/` | Rain + case bad endings |",
        "| `cinematics/` | Opening / ED / image-song first frames |",
        "| `canon-turns/` | Full canon-path dialogue (`turn_NNN.png`, `_menu` at choices) |",
        "",
    ]

    if reports:
        lines.append("## Run reports")
        lines.append("")
        for name, data in reports.items():
            lines.append(f"### `{name}`")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(data, indent=2))
            lines.append("```")
            lines.append("")

    if CG_CATALOG_META:
        lines.append("## CG catalog (label → file)")
        lines.append("")
        lines.append("| File | CG tag | Description |")
        lines.append("|------|--------|-------------|")
        for rel, tag, desc in sorted(CG_CATALOG_META, key=lambda x: x[0]):
            lines.append(f"| `{rel}` | `{tag}` | {desc} |")
        lines.append("")

    lines.append("## All captured files")
    lines.append("")
    for rel in pngs:
        lines.append(f"- `{rel}`")
    lines.append(SKIP_NOTE)

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        if not lines[-1].endswith("\n"):
            f.write("\n")

    print(f"Wrote {MANIFEST_PATH} ({len(pngs)} PNGs indexed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
