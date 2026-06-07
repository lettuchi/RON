"""Promote v2 MP3s to legacy for given IDs."""
from __future__ import annotations
import argparse
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "game" / "audio" / "voice" / "v2" / "eve-donovan-2026-06-04"
LEGACY = ROOT / "game" / "audio" / "voice"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids-file", required=True)
    ap.add_argument("--log", required=True)
    args = ap.parse_args()
    ids = [ln.strip() for ln in Path(args.ids_file).read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")]
    log_lines = [f"Promote v2 -> legacy started {datetime.now()}", f"v2 source: {V2}", f"legacy: {LEGACY}"]
    promoted = skipped = errors = 0
    for vid in ids:
        src = V2 / f"{vid}.mp3"
        dst = LEGACY / f"{vid}.mp3"
        if not src.exists():
            log_lines.append(f"SKIP missing v2 {vid}")
            skipped += 1
            continue
        try:
            shutil.copy2(src, dst)
            log_lines.append(f"PROMOTED {vid}")
            promoted += 1
        except OSError as e:
            log_lines.append(f"ERROR {vid}: {e}")
            errors += 1
    log_lines.append(f"Promoted count: {promoted}")
    log_lines.append(f"Skipped (no v2): {skipped}")
    log_lines.append(f"Errors: {errors}")
    Path(args.log).write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print("\n".join(log_lines[-5:]))
    return 0 if errors == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
