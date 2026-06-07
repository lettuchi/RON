from pathlib import Path
import re
p = Path(r"C:\Users\Amanda\Developer\ryoko-owari\scripts\generate_music.py")
t = p.read_text(encoding="utf-8")

SAFE = {
    "corridor": (
        "Instrumental Japanese cinematic ambient bed for a feudal-Japan visual novel corridor scene. "
        "Endless magistrate-quarter hallway at night: distant paper lanterns, hushed nobility, ink and cedar in the air. "
        "Sparse koto harmonics and a soft breathy sho-like pad, occasional single woodblock or wind-chime color, "
        "very slow harmonic motion around 80 BPM or almost pulseless. Mysterious but not scary, quiet anticipation. "
        "No vocals, no lyrics, no modern drums, no synth EDM, no battle percussion. Seamless loop-friendly: steady "
        "texture, no big ending crash, last bar flows back to the first. Traditional Japanese aesthetics."
    ),
    "street": (
        "Instrumental Japanese cinematic street theme for a canal city at night. Warm shamisen or biwa riff over light "
        "hand percussion and soft taiko on beats 1 and 3, distant lantern ambience. Tempo around 88 to 92 BPM, walking "
        "pace, worldly and slightly tense but not battle. Textures suggesting fish, copper, and rain on stone in the mix, "
        "not literal sound effects. No vocals, no lyrics, no EDM four-on-the-floor, no heroic fanfare. Loop-friendly: "
        "repeating 8-bar street motif, steady energy, ending connects to opening motif."
    ),
    "canon_intimate": (
        "Instrumental Japanese cinematic romantic aftermath bed inspired by feudal Japan visual novels. Warm, tender, "
        "gentle closeness without explicit sensuality: slow koto melody and soft string pads in D major or gentle modal "
        "major, 70 to 72 BPM, breathing room like paper screens and shared tea. Bittersweet undercurrent, two people "
        "choosing trust despite doubt. No vocals, no lyrics, no heavy percussion, no modern pop ballad cliches. "
        "Loop-friendly: soft continuous arc, loop point on a sustained chord, no dramatic stop."
    ),
    "case2_festival": (
        "Instrumental Japanese festival night theme inspired by a feudal canal-city matsuri. Lively but refined taiko "
        "festival rhythms softened for dialogue, shamisen and fue motifs, warm paper-lantern harmonies. 95 BPM feel "
        "without overwhelming voice acting, subtle tension suggesting hidden intrigue. No vocals, no lyrics, no EDM "
        "drops, no arcade chiptune. Loop-friendly with a repeating festival hook every 8 bars and steady energy."
    ),
    "case3_5_date": (
        "Instrumental Japanese cinematic date-night bed for a private inn with hidden biwa music through shoji, feudal "
        "Japan otome atmosphere. Intimate and slightly nervous: soft koto, distant biwa phrase like music through a "
        "wall, warm shakuhachi echo, gentle hand percussion like tea service, 68 to 74 BPM. Romance with stakes, quiet "
        "evening not public festival. No vocals, no lyrics, no club beats, no comedic slapstick. Loop-friendly, tender "
        "continuous mood."
    ),
    "case4_dock": (
        "Instrumental Japanese cinematic action-tension bed for a rainy lower dock and imminent duel tension. Driving "
        "shamisen and low taiko in restrained pulses for dialogue and choice menus, not a full anime battle track. "
        "Harmonic minor scale, 100 to 108 BPM feel, rain-heavy atmosphere in the mix. No vocals, no lyrics, no "
        "Hollywood trailer horns, no EDM. Loop-friendly for investigation."
    ),
    "bad_end_punishment": (
        "Instrumental Japanese cinematic dread bed for a sealed official office at night. Low cello ostinato, single taiko "
        "heartbeats, sparse biwa, 65 BPM, claustrophobic solemn mood. No vocals, no lyrics, no screaming, no impact "
        "sound effects. Loop-friendly under long narration."
    ),
}

for tid, prompt in SAFE.items():
    pat = rf'("{tid}": \{{\s*"filename":[^"]+"[^"]+",\s*"length_ms": \d+,\s*"prompt": \(\s*)(.*?)(\s*\),\s*\}},)'
    m = re.search(pat, t, re.DOTALL)
    if not m:
        raise SystemExit(f"track {tid} not found")
    escaped = prompt.replace("\\", "\\\\").replace('"', '\\"')
    inner = "\n            \"" + "\"\n            \"".join(prompt.split(". ")) + "\""
    # simpler: single line join
    lines = [ln.strip() for ln in prompt.split(". ") if ln.strip()]
    inner = "\n            ".join(f'"{ln}."' if not ln.endswith(".") else f'"{ln}"' for ln in lines)
    # fix double dots
    inner = re.sub(r'\.\"', '. "', inner)
    new_block = m.group(1) + inner + m.group(3)
    t = t[:m.start()] + new_block + t[m.end():]

p.write_text(t, encoding="utf-8")
print("updated", list(SAFE))
