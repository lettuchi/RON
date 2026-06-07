from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(r"C:/Users/Amanda/Developer/ryoko-owari")
V2 = ROOT / "game/audio/voice/v2/eve-donovan-2026-06-04"
LEG = ROOT / "game/audio/voice"
BACKUP = ROOT / "game/audio/voice/_backup_promote_2026-06-04_case1_menu"
ids = (ROOT / "scripts/case1_unwired_voice_ids.txt").read_text(encoding="utf-8").split()
BACKUP.mkdir(parents=True, exist_ok=True)
promoted = 0
backed = 0
for vid in ids:
    vid = vid.strip()
    if not vid:
        continue
    src = V2 / f"{vid}.mp3"
    dst = LEG / f"{vid}.mp3"
    if not src.is_file():
        print("MISSING v2", vid)
        continue
    if dst.is_file():
        shutil.copy2(dst, BACKUP / f"{vid}.mp3")
        backed += 1
    shutil.copy2(src, dst)
    promoted += 1
print(f"promoted={promoted} backed_up={backed} backup_dir={BACKUP}")
