import re, pathlib

# labels reachable from bad-end jumps (include intermediate)
SEEDS = {
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

file_labels = {}
for p in pathlib.Path("game").rglob("*.rpy"):
    lbs = label_blocks(p.read_text(encoding="utf-8", errors="replace"))
    file_labels[str(p)] = lbs

# also add labels that contain 'bad_end' or start with gameover
for fp, lbs in file_labels.items():
    for lab in lbs:
        if "bad_end" in lab or lab.startswith("gameover_"):
            SEEDS.add(lab)

voice_re = re.compile(r'voice\s+"audio/voice/([^"]+)"')
ids = set()
for name in sorted(SEEDS):
    for fp, lbs in file_labels.items():
        body = lbs.get(name)
        if not body:
            continue
        for vid in voice_re.findall(body):
            ids.add(vid.replace(".mp3", ""))

print("expanded seeds", len(SEEDS))
print("voice ids", len(ids))
for x in sorted(ids):
    print(x)
