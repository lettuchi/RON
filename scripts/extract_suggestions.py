import re
from pathlib import Path
log = Path(r"C:\Users\Amanda\Developer\ryoko-owari\scripts\music_generation_2026-06-03.log").read_text(encoding="utf-8", errors="replace")
for m in re.finditer(r'prompt_suggestion":"((?:\\.|[^"\\])*)"', log):
    s = m.group(1).encode().decode("unicode_escape") if "\\" in m.group(1) else m.group(1)
    print(s[:300])
    print("---")
