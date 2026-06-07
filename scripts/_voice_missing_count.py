import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
wired = set()
for p in (ROOT / "game").rglob("*.rpy"):
    for m in re.finditer(r'^\s*voice "audio/voice/(\w+)\.mp3"', p.read_text(encoding="utf-8"), re.M):
        line_start = m.start()
        line = p.read_text(encoding="utf-8")[:line_start].split("\n")[-1]
        if line.lstrip().startswith("#"):
            continue
        wired.add(m.group(1))
missing = sorted(i for i in wired if not (ROOT / "game/audio/voice" / f"{i}.mp3").exists())
print("wired_ids", len(wired))
print("missing_legacy_mp3", len(missing))
if missing:
    print("first_missing", missing[:20])
