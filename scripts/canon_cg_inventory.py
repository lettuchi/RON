#!/usr/bin/env python3
"""Enumerate canon CG tags, PNGs, and wired gameplay usage."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
IMAGES = GAME / "images"
CG_DIR = IMAGES / "cg"

EXCLUDE_REGISTRY_PREFIXES = ("cgs-au-modern", "cgs-practice-room")


def parse_registries() -> dict[str, str]:
    tag_to_png: dict[str, str] = {}
    for rf in sorted(IMAGES.glob("cgs-*.rpy")):
        if any(rf.name.startswith(p) for p in EXCLUDE_REGISTRY_PREFIXES):
            continue
        if "au-modern" in rf.name:
            continue
        text = rf.read_text(encoding="utf-8")
        for m in re.finditer(r'image cg (\S+) = At\("images/cg/([^"]+)"', text):
            tag, png = m.group(1), m.group(2)
            if "au_modern" in tag or "au-modern" in png:
                continue
            tag_to_png[tag] = png
    return tag_to_png


def parse_wired() -> set[str]:
    wired: set[str] = set()
    for rpy in GAME.glob("*.rpy"):
        if "au_modern" in rpy.name:
            continue
        text = rpy.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r'show_cg_scene\(\s*["\']([^"\']+)["\']', text):
            tag = m.group(1).strip()
            if tag.startswith("au_modern"):
                continue
            wired.add(tag)
    return wired


def list_canon_pngs_on_disk() -> list[Path]:
    patterns = (
        "cg-case*.png",
        "cg-prologue*.png",
        "cg-badend*.png",
        "cg-ending*.png",
        "cg-first*.png",
        "cg-canon*.png",
        "cg-choice*.png",
        "cg-gameover*.png",
        "cg-epilogue*.png",
    )
    found: set[Path] = set()
    for pat in patterns:
        found.update(CG_DIR.glob(pat))
    # exclude AU
    return sorted(p for p in found if "au-modern" not in p.name and "practice-room" not in p.name)


def main() -> None:
    tag_to_png = parse_registries()
    wired = parse_wired()
    disk = list_canon_pngs_on_disk()
    registry_pngs = set(tag_to_png.values())

    missing_registry = sorted(wired - set(tag_to_png.keys()))
    orphan_tags = sorted(set(tag_to_png.keys()) - wired)
    disk_not_registry = sorted(
        p.name for p in disk if f"images/cg/{p.name}" not in registry_pngs
    )

    wired_pngs = sorted(
        {tag_to_png[t] for t in wired if t in tag_to_png}
    )

    out = ROOT / "docs" / "_canon_cg_inventory.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"registry_tags={len(tag_to_png)}",
        f"unique_registry_pngs={len(registry_pngs)}",
        f"wired_tags={len(wired)}",
        f"wired_unique_pngs={len(wired_pngs)}",
        f"disk_canon_pattern_pngs={len(disk)}",
        f"wired_not_in_registry={len(missing_registry)}",
        f"orphan_registry_tags={len(orphan_tags)}",
        "",
        "=== WIRED ===",
    ]
    for t in sorted(wired):
        lines.append(f"{t}\t{tag_to_png.get(t, 'MISSING')}")
    lines += ["", "=== ORPHAN REGISTRY ==="]
    for t in orphan_tags:
        lines.append(f"{t}\t{tag_to_png[t]}")
    if missing_registry:
        lines += ["", "=== WIRED MISSING REGISTRY ==="]
        for t in missing_registry:
            lines.append(t)
    if disk_not_registry:
        lines += ["", "=== DISK NOT IN REGISTRY (sample) ==="]
        for n in disk_not_registry[:40]:
            lines.append(n)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(out.read_text(encoding="utf-8")[:4000])


if __name__ == "__main__":
    main()
