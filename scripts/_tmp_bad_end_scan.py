import re, pathlib

BAD_ROOTS = {
    "gameover_case1_canal", "gameover_case2_alley", "gameover_case3_injury",
    "gameover_case4_abandon", "gameover_case4_slayn", "gameover_case4_5_boat",
    "gameover_rain", "case1_bad_end_kaoru_punishment", "case3_bad_end_injury",
    "case3_bad_end_injury_warning", "case4_bad_end_toa_slain", "case4_bad_end_toa_slain_warning",
    "case4_5_bad_end_boat", "case4_5_boat_bad_end_warning", "prologue_bad_end_brothel",
    "prologue_bad_end_kaoru", "prologue_refuse_bad_end",
}

def label_blocks(text):
    parts = re.split(r"^label (\w+):", text, flags=re.M)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}

all_blocks = {}
for p in pathlib.Path("game").rglob("*.rpy"):
    for k, v in label_blocks(p.read_text(encoding="utf-8", errors="replace")).items():
        all_blocks[(str(p), k)] = v

voice_re = re.compile(r'voice\s+"audio/voice/([^"]+)"')
ids = set()
unvoiced = []
for name in sorted(BAD_ROOTS):
    found = False
    for (fp, lab), body in all_blocks.items():
        if lab != name:
            continue
        found = True
        for vid in voice_re.findall(body):
            ids.add(vid.replace(".mp3", ""))
        lines = body.splitlines()
        for i, line in enumerate(lines):
            m = re.match(r"^\s*(kaoru|toa)\s+\"", line)
            if m and i > 0 and "voice " not in lines[i - 1]:
                unvoiced.append((name, pathlib.Path(fp).name, line.strip()[:100]))
    if not found:
        print("MISSING LABEL:", name)

print("VOICE IDS", len(ids))
for x in sorted(ids):
    print(x)
print("--- unvoiced kaoru/toa in bad blocks ---")
for u in unvoiced:
    print(u[0], u[1], u[2])
print("count", len(unvoiced))
