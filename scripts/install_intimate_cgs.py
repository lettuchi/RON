#!/usr/bin/env python3
"""Install PG-13 composited CGs from assets/cg-build/out/ into game/images/cg/."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "cg-build" / "out"
CG = ROOT / "game" / "images" / "cg"
ARCHIVE = CG / "versions" / "r18-archived-2026-06-02"

CG_FILES = [
    "cg-prologue-dance-disrobe.png",
    "cg-prologue-butt-wiggle-grab.png",
    "cg-prologue-bent-over-desk.png",
    "cg-canon-steamy-undress-toa.png",
    "cg-canon-steamy-intimacy.png",
    "cg-canon-steamy-afterglow.png",
    "cg-case1-r18-undress.png",
    "cg-case1-r18-intimacy.png",
    "cg-case2-r18-morning.png",
    "cg-case2-r18-afterglow.png",
]


def main() -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    backed = 0
    for name in CG_FILES:
        dst = CG / name
        if dst.is_file():
            shutil.copy2(dst, ARCHIVE / name)
            backed += 1
    installed = 0
    missing = []
    for name in CG_FILES:
        src = OUT / name
        dst = CG / name
        if not src.is_file():
            missing.append(name)
            continue
        shutil.copy2(src, dst)
        installed += 1
        print(f"installed {dst.relative_to(ROOT)}")
    print(f"\narchive: {ARCHIVE.relative_to(ROOT)} ({backed} backed up)")
    print(f"installed: {installed}/{len(CG_FILES)}")
    if missing:
        print("missing from out/:", ", ".join(missing))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
