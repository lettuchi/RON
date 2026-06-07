# Voice coverage audit (2026-06-04)

## Executive summary

| Metric | Count |
|--------|------:|
| Executable `voice "audio/voice/…"` lines (`.rpy`) | 981 |
| Unique wired voice IDs (excludes `#` comments) | 967 |
| Legacy `game/audio/voice/{id}.mp3` missing for wired IDs | **0** |
| Case Zero + Case 1 unwired regen | **Done** (see evening pass below) |
| ElevenLabs `--check` | OK (creator tier) |

**Wired dialogue:** Every executable voice statement has a legacy MP3 on disk.

**Not fully voiced in script:** Menu **choice labels** are not voiced (Ren'Py default). **Case 1 companion/investigation menu branches** are wired (0 unvoiced branch lines remaining in those files) (audio may exist in the library for other paths; these branch lines are unwired).

**Stub comments (outdated):** `case1_5_romance_interlude.rpy` header still says "stub manifest only" but lines are wired and MP3s exist (except unused manifest slot `toa_312`). `case5` / `epilogue_romance_bonus` headers say "regen batch TBD" but wired lines in those files have MP3s.

---

## Scan methodology

1. Recursed `game/**/*.rpy` for `voice "audio/voice/{id}.mp3"` (ignored `#` comment lines).
2. Verified `game/audio/voice/{id}.mp3` for each wired ID.
3. Cross-checked `scripts/voice_manifest.json`, `narrator_manifest.json`, `voice_performance_manifest.json`.
4. Stub ID ranges from comments and case headers.
5. Menu analysis: choice strings vs post-choice dialogue voicing.

---

## Manifest vs wiring

| Manifest | Entries | No legacy MP3 | In manifest, not wired in `.rpy` |
|----------|--------:|--------------:|-----------------------------------:|
| `voice_manifest.json` | 929 | 0 | 2 (`kaoru_224`, `toa_191`) |
| `narrator_manifest.json` | 311 | 0 | 41 |
| `voice_performance_manifest.json` | 1012 | 0 | 0 (superset IDs) |

Narrator lines are generated on disk; **runtime mute** via `MUTE_NARRATOR_VOICE = True` in `game/mute_narrator.rpy` (does not remove files or `voice` statements).

**False positive:** `narrator_NNN` appears only in a **comment** in `mute_narrator.rpy`, not in executable code.

---

## Stub / ID range checks

| Range | Missing MP3 | Notes |
|-------|------------:|-------|
| `narrator_297`–`303` (case1_5 header) | 0 | Wired in `case1_5_romance_interlude.rpy` |
| `kaoru_374`–`383` | 0 | Wired |
| `toa_308`–`317` | 1 | **`toa_312`**: manifest gap only — script jumps `toa_311` → `toa_313` (no `voice` line) |
| `kaoru_335+` / `toa_281+` / `narrator_272+` (case5 header) | 14 kaoru, 4 toa in high band | IDs **not wired** in `.rpy` (report only); wired case5/epilogue lines all have MP3s |
| `case5_investigation.rpy` wired set | 0 missing | 62 voice lines in file |
| `epilogue_romance_bonus.rpy` wired set | 0 missing | 14 voice lines in file |

Promote path checked: `game/audio/voice/v2/eve-donovan-2026-06-04/` (901 MP3s); nothing to promote for wired gaps.

Legacy library: **1013** MP3s under `game/audio/voice/*.mp3`.

---

## Menus and choices

- **`menu:` blocks:** 4 files (`prologue.rpy` ×3, `epilogue_rain_gameover.rpy`, `testcases.rpy`).
- **Choice entries (~155):** Choice **text** is never preceded by `voice` (expected).
- **After choice:** Most prologue menus voice the **first spoken line** in the branch, not the menu label.
- **Gaps:** 15 player-facing branches in `case1_companion.rpy` / `case1_investigation.rpy` (+ test menu) have **multiple dialogue lines without `voice`** before rejoining voiced script. Fixing requires adding `voice` lines + manifest IDs, not MP3 generation alone.

---

## Generation commands (this run)

```text
python scripts/regenerate_voice_with_metadata.py --check
# OK — no quota/blockers

# Not run (no wired missing IDs):
# python scripts/regenerate_voice_with_metadata.py --model eleven_v3 --ids @scripts/voice_coverage_missing_ids.txt
```

**ID list:** `scripts/voice_coverage_missing_ids.txt` (empty / comment only).

**Log:** No batch regen log produced this session; `--check` output only (console).

---

## Recommendations

1. Update stale `VOICED: stub` / `TBD` headers on `case1_5`, `case5`, `epilogue_romance_bonus`.
2. Wire + voice-tag the 17 menu-branch dialogue blocks in Case 1 companion/investigation (or accept silent branches).
3. Optional: add `toa_312` line in script or drop ID from manifest; optional generate MP3 for manifest-only high IDs if future wiring planned.

---

## Case 1 menu branches wired (2026-06-04)

- Wired **44** post-choice / merge-path lines in `case1_companion.rpy` and `case1_investigation.rpy` (menu branches + merge path at investigation witness exit).
- New IDs: `toa_319`-`toa_338`, `kaoru_426`-`kaoru_449` (see `scripts/case1_unwired_voice_ids.txt`).
- Regenerated with eleven_v3; log: scripts/case1_unwired_voice_regen_2026-06-04.log.
- Menu-branch scan: **0** remaining unwired lines inside choice blocks.
- `game/kaoru_pro_prologue.rpy`: **93/93** Case Zero voice statements present; legacy MP3s on disk.

---

## Case Zero + Case 1 unwired pass (2026-06-04 evening)

| Item | Result |
|------|--------|
| Case Zero voice IDs (`narrator_312`-`365`, `kaoru_387`-`425`) | **93/93** legacy MP3s on disk |
| Case Zero regen (this session) | **6** newly synthesized in v2; **87** already in v2; **93** promoted to legacy |
| Case 1 menu-branch + merge-path wiring | **52** unique `toa_319+` / `kaoru_426+` IDs wired in `case1_companion.rpy` + `case1_investigation.rpy` |
| Case 1 regen (this session) | **2** newly synthesized (`toa_338`, `kaoru_449`); **42** reused existing v2; **44** promoted to legacy |
| Executable `voice` lines (`.rpy`, recount) | **1117** |
| Case 1 menu branches with unvoiced dialogue (companion + investigation) | **0** |

Logs: `scripts/case_zero_voice_regen_2026-06-04.log`, `scripts/case1_unwired_voice_regen_2026-06-04.log`.

Case Zero CGs: `cg-case-zero-redacted-docket.png`, `cg-case-zero-rain-alley-door.png` (NovelAI 1536x1024; GenerateImage unavailable in automation — NovelAI fallback).

