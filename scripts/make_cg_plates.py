#!/usr/bin/env python3
"""Export 1536x1024 background plates for cg-build compositor into Cursor assets/."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "assets" / "cg-build"))

from compositor import fit_bg, GEN, W, H  # noqa: E402

PLATES = {
    "plate-prologue-office.png": ROOT / "game" / "images" / "bg" / "magistrate_office.png",
    "plate-case1-hall.png": ROOT / "game" / "images" / "bg" / "magistrate_office.png",
    "plate-case2-dawn.png": ROOT / "game" / "images" / "bg" / "magistrate_office.png",
}


def main() -> None:
    os.makedirs(GEN, exist_ok=True)
    for name, src in PLATES.items():
        if not src.is_file():
            raise FileNotFoundError(src)
        out = Path(GEN) / name
        fit_bg(str(src)).save(out)
        print(f"wrote {out} ({W}x{H})")


if __name__ == "__main__":
    main()
