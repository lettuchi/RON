from pathlib import Path
doc = Path(r"C:\Users\Amanda\Developer\ryoko-owari\docs\elevenlabs-music-prompts.md")
text = doc.read_text(encoding="utf-8")
old = "**Status (repo, Jun 2026):** `game/audio/music.rpy` references `.ogg` / `.mp3` under `game/audio/bgm/`. On disk, `game/audio/bgm/` currently holds only GarageBand `.band` projects (`toa_theme.band`, `kaoru_theme.band`, `Project.band`) — no shipped loop files in-tree. Procedural placeholders are described in `docs/audio-setup.md` / `docs/garageband-bgm-guide.md`."
files = sorted([
    "bad_end_brothel.mp3", "bad_end_punishment.mp3", "bad_end_rain.mp3", "bad_ending.mp3",
    "canon_intimate.mp3", "canon_intimate.ogg", "case1_barge.mp3", "case2_festival.mp3",
    "case3_5_date.mp3", "case3_fabric.mp3", "case4_5_kobune.mp3", "case4_dock.mp3",
    "case5_tease.mp3", "corridor.mp3", "corridor.ogg", "kaoru_theme_new.mp3",
    "office.mp3", "street.mp3", "street.ogg", "toa_theme_new.mp3",
])
new = (
    "**Status (generated 2026-06-04 via `scripts/generate_music.py`, log `scripts/music_generation_2026-06-03.log`):** "
    "Eleven Music **creator** tier; probe OK; no 402/403. Seven prompts initially hit ToS (`bad_prompt`); "
    "retried with sanitized prompts (no L5R/Hakuoki/corrupt/coercive wording). "
    "`game/audio/music.rpy`: `bgm_office` now points at `office.mp3` (legacy `office.ogg` was file-locked). "
    "Shipped instrumental files under `game/audio/bgm/`:\n\n"
    + "\n".join(f"- `{f}`" for f in files)
    + "\n\n"
    "Proposed case/optional beds (not yet wired in `music.rpy`): "
    "`case1_barge.mp3`, `case2_festival.mp3`, `case3_fabric.mp3`, `case3_5_date.mp3`, "
    "`case4_dock.mp3`, `case4_5_kobune.mp3`, `case5_tease.mp3`, "
    "`bad_end_rain.mp3`, `bad_end_brothel.mp3`, `bad_end_punishment.mp3`. "
    "Duplicate `kaoru_theme_new_regen.mp3` can be deleted after verifying `kaoru_theme_new.mp3`."
)
if old not in text:
    raise SystemExit("status block not found")
doc.write_text(text.replace(old, new, 1), encoding="utf-8")
print("doc updated")
