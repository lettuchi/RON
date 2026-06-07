#!/usr/bin/env python3
"""Copy composited ED stills from assets/cg-build/out/ to game/images/ed/.

Backs up any existing target PNG to game/images/ed/versions/<timestamp>/.
"""
from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "cg-build" / "out"
ED = ROOT / "game" / "images" / "ed"
VERSIONS = ED / "versions"

ED_FILES = [
    "ed-kaoru-canal-pursuit.png",
    "ed-kaoru-watches-return.png",
    "ed-kaoru-bridge-red-bind.png",
    "ed-hands-second-knot.png",
    "ed-toa-bridge-run-mid-chorus.png",
    "ed-canal-twilight-ink.png",
    "ed-kaoru-canal-night-lantern.png",
    "ed-office-name-retrace.png",
    "ed-toa-bridge-instrumental.png",
    "ed-toa-bridge-final-chorus.png",
    "ed-toa-bridge-hesitant.png",
    "ed-office-sleep-red-thread.png",
]


def main() -> None:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = VERSIONS / stamp
    backup_dir.mkdir(parents=True, exist_ok=True)
    installed = 0
    missing = []
    for name in ED_FILES:
        src = OUT / name
        dst = ED / name
        if not src.is_file():
            missing.append(name)
            continue
        if dst.is_file():
            shutil.copy2(dst, backup_dir / name)
        shutil.copy2(src, dst)
        installed += 1
        print(f"installed {dst.relative_to(ROOT)}")
    print(f"\nbackup: {backup_dir.relative_to(ROOT)} ({len(list(backup_dir.glob('*.png')))} files)")
    print(f"installed: {installed}/{len(ED_FILES)}")
    if missing:
        print("missing from out/:", ", ".join(missing))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
