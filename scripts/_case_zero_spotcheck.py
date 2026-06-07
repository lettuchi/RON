import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "game/kaoru_pro_prologue.rpy").read_text(encoding="utf-8")
wired = set(re.findall(r'voice "audio/voice/(\w+)\.mp3"', text))
ids = []
for line in (ROOT / "scripts/case_zero_voice_ids.txt").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#"):
        ids.append(line)
legacy_missing = [i for i in ids if not (ROOT / "game/audio/voice" / f"{i}.mp3").exists()]
print("case_zero ids file:", len(ids))
print("wired in rpy:", len(wired))
print("legacy mp3 missing:", len(legacy_missing))
if legacy_missing:
    print("missing:", legacy_missing)
