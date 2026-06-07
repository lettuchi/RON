# Voice remaining audit — Ryoko Owari Nights

**Date:** 2026-06-03  
**Scope:** `game/*.rpy` (excluding `game/versions/`), manifests, v2 metadata. **Audit only** — no regen performed.  
**Convention (voiced routes):** prologue, cases, bad ends, romance interludes (Case 3.5 / 4.5). OP/ED, dev, tests, image songs excluded.

---

## Executive summary

| Metric | Count |
|--------|------:|
| `voice "audio/voice/…"` tags in story `.rpy` | **~650** occurrences |
| Unique wired IDs (`voice_manifest.json` + narrator) | **~640** character manifest + **182** narrator manifest rows |
| `voice_performance_manifest.json` entries | **680** (209 toa / 243 kaoru / 228 narrator) |
| Eleven v3 regen tracked in `voice_v2_metadata_manifest.json` | **340** |
| **Wired but not yet v3-regen’d** (est., manifest − v2) | **~340** |
| **Never wired** (no `voice` tag, no manifest ID) | **~0** in scoped routes (Case 3/4 done) |
| Performance manifest missing `tts_text` | **0** |
| Performance manifest orphans vs game | **0** |

**Bottom line:** Prologue, canon encounter, Case 2, Case 4.5, rain/bad-end blocks, Case 1 + Case 3.5 v3 batch, and June v3 promotion batches are in good shape. Remaining greenfield: **none** in voiced routes (Case 3/4 investigation wired 2026-06-03).

---

## 1. Wired inventory (by chapter)

Voice tags per story file (grep `game/*.rpy`, excludes `versions/`):

| Chapter / file | Voice tags | Notes |
|----------------|------------|--------|
| `prologue.rpy` | 207 | Fully wired |
| `prologue_canon_encounter.rpy` | 23 | Fully wired |
| `case1_companion.rpy` | 80 | Wired |
| `case1_investigation.rpy` | 110 | Wired |
| `case3_5_date_interlude.rpy` | 117 | Wired 2026-06-03 |
| `case4_5_boat.rpy` | 47 | Wired 2026-06-03 |
| `case_endings.rpy` | 35 | Bad-end narration |
| `epilogue_rain_gameover.rpy` | 27 | Rain / refuse paths |
| `case3_investigation.rpy` | **47** | **VOICED 2026-06-03** (+ `narrator_227` injury warning) |
| `case4_investigation.rpy` | **43** | **VOICED 2026-06-03** (+ `narrator_228` slayn warning) |
| `case2_investigation.rpy` | **44** | **VOICED 2026-06-03** |
| `case2_festival.rpy` | **39** | **VOICED 2026-06-03** (+ `case2_romance_morning` 9 lines in `case_endings.rpy`) |
| `case4_date_interlude.rpy` | 0 | Alias → Case 3.5 (no unique lines) |
| `script.rpy` | 1 | `toa_129` hook line |
| **OP/ED / dev / tests** | 0 | Intentionally excluded |

`build_manifest.py` parses the same wired file list as above (includes `case3_investigation.rpy` / `case4_investigation.rpy`).

---

## 2. Never wired (greenfield)

Routes with **speakable dialogue but no `voice` tag** and **no manifest entry**. Approximate line counts from script scan (character `toa`/`kaoru` + narrator `"…"` strings; excludes menus once inside `menu:` blocks).

| Chapter | Files | Est. lines | Next ID allocation (suggested) |
|---------|-------|------------|--------------------------------|
| **Case 2** — Academy packet | `case2_investigation.rpy`, `case2_festival.rpy`, `case2_romance_morning` | ~~**~97**~~ **92 DONE** | `toa_211`–`toa_245`, `kaoru_244`–`kaoru_282`, `narrator_229`–`narrator_246` |
| **Case 3** — investigation body | `case3_investigation.rpy` | ~~**~57**~~ **46 DONE** (34 character, 24 narrator; 1 already wired) | continue after Case 2 |
| **Case 4** — investigation body | `case4_investigation.rpy` | ~~**~52**~~ **40 DONE** (33 character, 20 narrator; 1 already wired) | continue after Case 3 |
| **Total greenfield** | | **0** (Case 2–4 investigation done) | |

**Workflow for greenfield:** write `voice` lines → extend `SCRIPT_FILES` in `build_manifest.py` + `narrator_manifest` rebuild → `sync_voice_performance_manifest.py --apply-tags` → `regenerate_voice_with_metadata.py --model eleven_v3`.

**Already wired stubs (not greenfield):** `narrator_227` / `narrator_228` on Case 3/4 injury-warning labels only (predates Batch C; investigation bodies wired 2026-06-03).

---

## 3. Wired but not v3-regen’d (`legacy_not_v3_regen`)

These IDs have `voice "audio/voice/{id}.mp3"` in game and entries in `voice_performance_manifest.json`, but **do not appear** in `voice_v2_metadata_manifest.json` (June 2026 v3 pass). They likely still play **legacy `eleven_multilingual_v2`** MP3s under `game/audio/voice/{id}.mp3` if promoted earlier; **Case 3.5 has no v3 rows at all** (grep: no `toa_130`, `kaoru_162`, `narrator_144` in v2 manifest).

### 3.1 Case 1 + Case 3.5 block (priority regen batch)

| Speaker | ID range | Count (est.) | Source files |
|---------|----------|-------------:|----------------|
| Toa | `toa_067`–`toa_172` | **106** | `case1_companion.rpy`, `case1_investigation.rpy`, `case3_5_date_interlude.rpy` |
| Kaoru | `kaoru_081`–`kaoru_091` (except `kaoru_092` in v2) | **10** | Case 1 openers |
| Kaoru | `kaoru_093`–`kaoru_205` | **113** | Case 1 + Case 3.5 |
| Narrator | `narrator_052`–`narrator_173` minus sparse v2 hits | **~112** | Case 1 + Case 3.5 |
| **Subtotal** | | **~341** | |

Sparse narrator IDs in the Case 1–3.5 band that **are** already in v2 metadata: `narrator_095`, `097`, `099`, `103`–`106`, `108`, `126`, `152`, `154` (rain/bad-end overlap elsewhere in v2).

### 3.2 Already v3-regen’d (reference)

Present in `voice_v2_metadata_manifest.json` (340 entries), including:

| Block | ID ranges |
|-------|-----------|
| Prologue Toa | `toa_001`–`toa_066` |
| Prologue Kaoru | `kaoru_001`–`kaoru_080` (+ `kaoru_092`) |
| Prologue narrator | `narrator_001`–`narrator_051` |
| Case 4.5 | `toa_173`–`toa_191`, `kaoru_206`–`kaoru_224`, `narrator_174`–`narrator_182` |
| Rain / bad ends / epilogue | `toa_192`–`toa_210`, `kaoru_225`–`kaoru_243`, `narrator_183`–`narrator_228` (+ selected mid-manifest narrator lines) |

Recent promotion logs: `scripts/remaining_voice_regen_2026-06-03.log` (144 lines), `kaoru_regen_ids.txt` (99), `toa_narrator_remaining_ids.txt` (94).

---

## 4. Manifest & performance JSON health

| Check | Result |
|-------|--------|
| IDs in game without performance entry | **0** orphans (`_meta.counts.orphans`) |
| Performance entry with empty `tts_text` | **0** |
| `model_hint: eleven_multilingual_v2` | **379** entries (many regen’d lines still marked v2; safe to treat as “needs v3 regen or metadata refresh”) |
| Tagged `tts_text` (bracket tags) | **291** (`_meta.counts.tagged_tts`) |
| `game_text` drift (`--diff`) | Not run this audit — run before next regen batch |

---

## 5. MP3 on disk (not verified this session)

This audit could not enumerate `game/audio/voice/*.mp3` from the sandbox (assets often gitignored). Use locally:

```powershell
# Legacy folder — missing or zero-byte
Get-ChildItem game\audio\voice\*.mp3 | Where-Object { $_.Length -eq 0 }
# Compare wired ID list to files
```

**Expected layout:**

- **Legacy play path:** `game/audio/voice/{id}.mp3` (what Ren'Py references today).
- **v3 staging:** `game/audio/voice/v2/eve-donovan-2026-06-03/{id}.mp3` — promote to legacy after QC.

**Gap types:**

| Type | Meaning |
|------|---------|
| `never_wired` | No tag, no MP3, no manifest row |
| `wired_no_mp3` | Tag + manifest, file missing/0 bytes |
| `v2_only_not_promoted` | v3 file in `v2/…` only, legacy path missing |
| `legacy_not_v3_regen` | Legacy MP3 may exist (v2 batch) but not in v2 metadata / not v3 |

---

## 6. Intentionally unvoiced (excluded from gaps)

| Category | Examples |
|----------|----------|
| Centered cards | Prologue bad-end warnings, Case 3/4 injury `{size=-2}…` cards |
| Menus | All `menu:` choice strings |
| OOC / dev | `dev_chapter_pick.rpy`, `test_*.rpy`, `testcases.rpy` |
| OP/ED | `opening.rpy`, `ed_sequence.rpy`, `transforms_op_ed.rpy` |
| Image songs | `toa_image_song.rpy`, `kaoru_image_song.rpy`, `duet_song.rpy` |
| Mute toggles | `mute_narrator.rpy`, `mute_audio.rpy` |
| UI / assets | `screens.rpy`, `gallery.rpy`, `images/*.rpy`, `gui.rpy` |

---

## 7. Summary table by gap type

| Type | Chapter focus | Toa | Kaoru | Narrator | Total (est.) |
|------|---------------|-----|-------|----------|-------------:|
| **Never wired** | — | 0 | 0 | 0 | **0** |
| **Legacy not v3** | Case 1, Case 3.5 | 106 | 123 | 112 | **~341** |
| **v3 done** | Prologue, 4.5, bad ends, rain | 85+ | 99+ | 117+ | **340** (v2 manifest) |

---

## 8. Recommended regen order (ID ranges)

Do **not** run until manifests and wiring are updated for greenfield. Suggested batches:

### Batch A — Case 1 + Case 3.5 v3 (wired, highest ROI)

```
toa_067–toa_172
kaoru_081–kaoru_091, kaoru_093–kaoru_205
narrator_052–narrator_173   # minus ids already in voice_v2_metadata_manifest.json
```

```bash
python scripts/sync_voice_performance_manifest.py --apply-tags
python scripts/regenerate_voice_with_metadata.py --model eleven_v3 --ids @scripts/case1_case35_v3_ids.txt --force
# Promote v2/eve-donovan-2026-06-03/*.mp3 → game/audio/voice/
```

### Batch B — Case 2 greenfield ✅ DONE 2026-06-03

Wired **92** lines (`scripts/wire_case2_voice.py`); regen `scripts/case2_voice_ids.txt`; promoted to legacy `game/audio/voice/{id}.mp3`. Rpy backups: `game/versions/case2-voice-2026-06-03/*.rpy.bak`.

| Character | ID range | Count | Files |
|-----------|----------|------:|-------|
| Toa | `toa_211`–`toa_245` | 35 | investigation 19, festival 12, morning 4 |
| Kaoru | `kaoru_244`–`kaoru_282` | 39 | investigation 19, festival 17, morning 3 |
| Narrator | `narrator_229`–`narrator_246` | 18 | investigation 6, festival 10, morning 2 |
| **Total** | | **92** | |

```bash
python scripts/build_manifest.py
python scripts/sync_voice_performance_manifest.py --apply-tags
python scripts/regenerate_voice_with_metadata.py --model eleven_v3 --ids @scripts/case2_voice_ids.txt --force --concurrency 4
# Promote v2/eve-donovan-2026-06-03/*.mp3 → game/audio/voice/
```

API failures: 0. Prior legacy backup folder reserved at `game/audio/voice/versions/case2-voice-backup-2026-06-03/` (no prior legacy files existed for new ids).

### Batch C — Case 3 / 4 investigation ✅ DONE 2026-06-03

Wired **86** lines (`scripts/wire_case34_investigation_voice.py`); regen `scripts/case34_investigation_voice_ids.txt`; promoted to legacy `game/audio/voice/{id}.mp3`. Rpy backups: `game/versions/case34-investigation-voice-2026-06-03/*.rpy.bak`. Prior legacy backup folder: `game/audio/voice/versions/case34-investigation-voice-backup-2026-06-03/` (0 prior files for new ids).

| Character | ID range | Count | Files |
|-----------|----------|------:|-------|
| Toa | `toa_246`–`toa_271` | 26 | `case3_investigation.rpy`, `case4_investigation.rpy` |
| Kaoru | `kaoru_283`–`kaoru_320` | 38 | same |
| Narrator | `narrator_247`–`narrator_268` | 22 | same |
| **Total** | | **86** | |

```bash
python scripts/build_manifest.py
python scripts/sync_voice_performance_manifest.py --apply-tags
python scripts/regenerate_voice_with_metadata.py --model eleven_v3 --ids @scripts/case34_investigation_voice_ids.txt --force --concurrency 4
# Promote v2/eve-donovan-2026-06-03/*.mp3 → game/audio/voice/
```

API failures: 0. Skipped (already wired): `narrator_227` / `narrator_228` injury/slayn warning cards; empty bad-end jump labels.

### Batch D — Tag/metadata cleanup

- Refresh `model_hint` to `eleven_v3` for regen’d rows.
- Run `sync_voice_performance_manifest.py --diff` after any script edits.

---

## 9. Related files

| File | Role |
|------|------|
| `scripts/voice_manifest.json` | Wired toa/kaoru/narrator text |
| `scripts/narrator_manifest.json` | Narrator-only rows (`narrator_001`–`182`) |
| `scripts/voice_performance_manifest.json` | `tts_text` for Eleven v3 |
| `scripts/voice_v2_metadata_manifest.json` | v3 regen audit trail (340 lines) |
| `scripts/build_manifest.py` | Regenerates voice manifest from wired `.rpy` |
| `docs/voice-performance-manifest.md` | Workflow + prior batch notes |

---

*Updated 2026-06-03 — Case 3/4 investigation voice pipeline complete (86 lines, eleven_v3). Greenfield wiring exhausted for investigation bodies.*
