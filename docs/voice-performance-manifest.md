# Voice performance manifest (parallel TTS dialog)

Ren'Py game scripts stay **untagged**. Expressive ElevenLabs v3 audio tags (`[laughs]`, `[whispers]`, `[pause]`, Ã¢â‚¬Â¦) live only in:

```
scripts/voice_performance_manifest.json
```

See [elevenlabs-audio-tags.md](elevenlabs-audio-tags.md) for tag vocabulary and [voice-metadata.md](voice-metadata.md) for the v2 MP3 pipeline.

## Fields (per line)

| Field | Purpose |
|-------|---------|
| `id` | Same as `toa_001`, `kaoru_002`, `narrator_042` in `voice_manifest.json` / `narrator_manifest.json` |
| `character` | `toa`, `kaoru`, or `narrator` |
| `source` | `file.rpy:line` hint when known |
| `game_text` | Verbatim display / manifest text (diff against game) |
| `tts_text` | Text sent to ElevenLabs (may include v3 tags) |
| `tags_notes` | Optional editor note (heuristic or manual) |
| `model_hint` | `eleven_v3` when tags matter; `eleven_multilingual_v2` when plain |

## Workflow

### After adding voiced lines to the game

1. Rebuild character manifest if needed: `python scripts/build_manifest.py`
2. Sync performance manifest (adds new ids, preserves your tags):

   ```bash
   python scripts/sync_voice_performance_manifest.py
   ```

3. Tag new lines in `voice_performance_manifest.json`, or re-run heuristics:

   ```bash
   python scripts/sync_voice_performance_manifest.py --apply-tags
   python scripts/sync_voice_performance_manifest.py --apply-tags --retag-all
   python scripts/enrich_manifest_delivery_tags.py --retag   # emotion + woven pauses/reactions
   ```

4. Check drift between game and stored `game_text`:

   ```bash
   python scripts/sync_voice_performance_manifest.py --diff
   ```

5. Drop ids removed from the game:

   ```bash
   python scripts/sync_voice_performance_manifest.py --prune-orphans
   ```

### Regenerate audio with tags

Bracket tags need **`eleven_v3`**. The default batch model (`eleven_multilingual_v2`) often speaks brackets literally.

In `scripts/.env`:

```env
ELEVENLABS_MODEL_ID=eleven_v3
```

Or per run:

```bash
python scripts/regenerate_voice_with_metadata.py --model eleven_v3 --ids toa_001,kaoru_002
```

By default, `regenerate_voice_with_metadata.py` loads `scripts/voice_performance_manifest.json` and uses `tts_text` when present.

| Flag | Effect |
|------|--------|
| `--performance-manifest PATH` | Alternate JSON path |
| `--no-performance` | Use manifest `text` only (game lines) |
| `--use-performance-text` | Explicit default when file exists |
| `--model eleven_v3` | Override `ELEVENLABS_MODEL_ID` |

Tagged lines log as `PERF {id}: tagged TTS` during generation. ID3 `renpy_line` stores the **TTS input**; `game_text` is in the embedded JSON comment blob when generated with the updated script.

## Line counts (June 2026)

| Set | Lines in performance manifest |
|-----|------------------------------:|
| Toa | 244 |
| Kaoru | 282 |
| Narrator | 246 |
| **Total** | **772** |

(772 = deduped toa/kaoru/narrator after Case 2 greenfield. Run `sync_voice_performance_manifest.py --prune-orphans` after manifest ID churn.)

### Case 2 — Academy packet + festival + morning tea

**VOICED 2026-06-03** (`case2_investigation.rpy`, `case2_festival.rpy`, `case2_romance_morning` in `case_endings.rpy`):

| Character | ID range | Count | Notes |
|-----------|----------|------:|-------|
| Toa | `toa_211`–`toa_245` | 35 | Investigation, alley/desk menus, festival kiss branches, morning tea |
| Kaoru | `kaoru_244`–`kaoru_282` | 39 | Briefing through festival bridge |
| Narrator | `narrator_229`–`narrator_246` | 18 | Ash/warehouse beats, hill/fireworks/kiss, shoji fade, dawn tea |
| **Case 2 total** | | **92** | |

Key festival beats tagged in `performance_tagging.py` `MANUAL_OVERRIDES` (`kaoru_269`, `narrator_240`–`241`, `kaoru_271`, `kaoru_274`, `narrator_242`, morning `kaoru_280` / `toa_243` / `kaoru_282`).

**92-line regen promoted 2026-06-03** (`eleven_v3`, `scripts/case2_voice_ids.txt`): v2 staging `game/audio/voice/v2/eve-donovan-2026-06-03/` → legacy `game/audio/voice/{id}.mp3`; rpy backups `game/versions/case2-voice-2026-06-03/*.rpy.bak`. Voices: Toa `Ylb1ch6nQEKvpaUivWj6`, Kaoru `zyxAdkuEJWvr177AyQPs`, Narrator `giAoKpl5weRTCJK7uB9b`. API failures: 0.

Per-file voice tags: `case2_investigation.rpy` 44, `case2_festival.rpy` 39, `case2_romance_morning` 9.


### Prologue â€” Kaoru (`kaoru_001`â€“`kaoru_080`, `prologue.rpy`)

**Kaoru 99-line regen promoted 2026-06-03** (`eleven_v3`, voice `zyxAdkuEJWvr177AyQPs`): legacy `game/audio/voice/{id}.mp3` for `kaoru_001`â€“`kaoru_080` and `kaoru_206`â€“`kaoru_224` (`scripts/kaoru_regen_ids.txt`); source `game/audio/voice/v2/eve-donovan-2026-06-03/`; prior legacy in `game/audio/voice/versions/kaoru-regen-legacy-backup-2026-06-03/`. Case 4.5 `kaoru_206`–`kaoru_224` promoted same date; prior legacy in `game/audio/voice/versions/kaoru-case45-legacy-backup-2026-06-03/`.

### Prologue + Case 4.5 — Toa & narrator (`scripts/toa_narrator_remaining_ids.txt`)

**94-line regen promoted 2026-06-03** (`eleven_v3`, performance manifest `tts_text` after `--apply-tags` + prologue Toa `MANUAL_OVERRIDES` in `performance_tagging.py`):

| Character | ID range | Count | Voice ID |
|-----------|----------|------:|----------|
| Toa | `toa_001`–`toa_066` (`prologue.rpy`, `prologue_canon_encounter.rpy`) | 66 | `Ylb1ch6nQEKvpaUivWj6` |
| Toa | `toa_173`–`toa_191` (Case 4.5) | 19 | same |
| Narrator | `narrator_174`–`narrator_182` (Case 4.5) | 9 | `giAoKpl5weRTCJK7uB9b` |

Source v2: `game/audio/voice/v2/eve-donovan-2026-06-03/`; prior legacy in `game/audio/voice/versions/toa-narrator-regen-backup-2026-06-03/`. Regen: `python scripts/regenerate_voice_with_metadata.py --model eleven_v3 --ids @scripts/toa_narrator_remaining_ids.txt --force --concurrency 4`. API failures: 0.


### Case 3.5 Ã¢â‚¬â€ "Is this a date?" (`case3_5_date_interlude.rpy`)

Wired 2026-06-03 (continues global ID sequences after Case 1 / epilogue):

| Character | ID range | Count |
|-----------|----------|------:|
| Toa | `toa_130`Ã¢â‚¬â€œ`toa_172` | 43 |
| Kaoru | `kaoru_162`Ã¢â‚¬â€œ`kaoru_205` | 44 |
| Narrator | `narrator_144`Ã¢â‚¬â€œ`narrator_173` | 30 |
| **Case 3.5 total** | | **117** |

Narrator ids follow **first-appearance** order in `narrator_manifest.json` (Case 3.5 blocks sit after epilogue rain lines, not at `narrator_116`). Key beats use `MANUAL_OVERRIDES` in `performance_tagging.py` (kaiseki gratitude `kaoru_171`, dance `kaoru_177`Ã¢â‚¬â€œ`178`, *very well loved* `kaoru_191`, date question / deflection `toa_168` / `kaoru_194`Ã¢â‚¬â€œ`196` / `kaoru_198`Ã¢â‚¬â€œ`199`, Toa ache `toa_170`, narrator ache `narrator_171`).

**352-line Case 1 + Case 3.5 regen promoted 2026-06-03** (`eleven_v3`, `scripts/case1_case35_voice_batch_ids.txt`): includes Case 3.5 ids above plus Case 1 companion/investigation; v2 staging `game/audio/voice/v2/eve-donovan-2026-06-03/`; legacy backup `game/audio/voice/versions/case1-case35-voice-backup-2026-06-03/`.

### Case 4.5 — Teardrop kobune (`case4_5_boat.rpy`)

**VOICED (2026-06-03):** `voice` lines wired; manifests synced via `build_manifest.py` + `narrator_manifest.json` append.

| Character | ID range | Count | Notes |
|-----------|----------|------:|-------|
| Toa | `toa_173`–`toa_191` | 19 | Breakdown, *I found you*, first **Kitsu Kaoru** |
| Kaoru | `kaoru_206`–`kaoru_224` | 19 | *yoriki*, throw, bath tease (Kaoru v3 regen batch) |
| Narrator | `narrator_174`–`narrator_182` | 9 | Marina / fade / domestic bridge |
| **Case 4.5 total** | | **47** | |

Kaoru prologue + Case 4.5: see Kaoru section above (99 lines). Toa + narrator Case 4.5 lines in 144-line batch above.

**Case 4.5 CGs (2026-06-03):** Regenerated marina/kobune set via GenerateImage; backups in `game/images/cg/versions/case4-5-cg-regen-2026-06-03/` (`cg-case4_5-boat-canal-night`, `duo-tense`, `throw-splash`, `lantern-implied`, `bad-boat-injury`).

### Tagging coverage (Eleven v3 `tts_text`, June 2026)

After `python scripts/enrich_manifest_delivery_tags.py --retag` (2026-06 delivery pass):

| Metric | Source |
|--------|--------|
| **Total entries** | `counts.total` in manifest JSON |
| **Lines with 2+ tags** | `counts.min_two_tags` |
| **Tagged vs plain** | `counts.tagged_tts` (`tts_text` ≠ `game_text`) |
| **Reaction/pause tags** | `counts.with_reaction_pause` (`[pause]`, `[sighs]`, `[chuckles]`, …) |
| **Mid-woven tags** | `counts.with_mid_woven` (delivery/reaction after lead emotion block) |
| Manual overrides | `MANUAL_OVERRIDES` in `performance_tagging.py` (punishment bridge, Case 3.5, Case 4.5, etc.) |

Re-count after every sync/enrich; koan `kaoru_139` is the only intentional sub-two-tag exception.

## Tagging policy (2026-06)

**Minimum density:** Every wired voice line in `voice_performance_manifest.json` should carry **at least two** Eleven v3 bracket tags from [elevenlabs-audio-tags.md](elevenlabs-audio-tags.md). More tags are fine when they track beats inside a long line (e.g. em-dash narration).

**Woven delivery (2026-06):** Beyond lead emotion tags, insert reaction/pause/delivery tags **inside** `tts_text` where the line earns it — `[short pause]` after stammers, `[sighs]` on breakdown, `[chuckles]` on snacks banter, `[exhales]` on realization, clause `[short pause]` on long narrator sentences. Not every line; `weave_delivery_tags()` in `performance_tagging.py` is scene-aware (Case 3.5 dinner, dock fight, Teardrop boat, punishment bridge). See [voice-performance-manifest-review.md](voice-performance-manifest-review.md).

**Scene + arc, not defaults:** Tags must reflect the **scene emotion** and **character arc** (Toa: bright nerve → defiant spine → intimate whispers; Kaoru: dry control → possessive warmth → public dismissive). Avoid blanket `[matter-of-fact]` unless the line is genuinely flat bureaucracy; prefer `[deadpan]`, `[dismissive]`, `[calm]`, `[warmly]` pairs.

**Review before regen:** After manifest edits, review `scripts/voice_performance_manifest.json` (or `docs/voice-performance-manifest-review.md` excerpt). **Do not** batch-regenerate MP3s until tags are approved. Regen uses `ELEVENLABS_MODEL_ID=eleven_v3` and `regenerate_voice_with_metadata.py` only after sign-off.

**Pipeline:**

```bash
python scripts/build_manifest.py
python scripts/sync_voice_performance_manifest.py --apply-tags --retag-all
python scripts/enrich_manifest_delivery_tags.py --retag    # full emotion + woven delivery pass
python scripts/enrich_manifest_delivery_tags.py --weave-only   # mid-line only, keep existing leads
python scripts/retag_performance_ids.py --ids @scripts/some_ids.txt   # optional targeted pass
```

**Exceptions:** Koan/aphorism Kaoru (`KAORU_KOAN_IDS`, e.g. `kaoru_139` *ask the river*) stay **untagged** (0 tags).

**Enforcement:** `MIN_TAGS_PER_LINE = 2` and `ensure_min_tags()` in `scripts/performance_tagging.py`; manifest `counts.min_two_tags` after sync.

## Tagging guidelines (character voice)

- **Toa:** `[cheerfully]` + `[nervously]` for magistrate-facing beats; `[defiant]` + `[cheerfully]` on refuse/punishment bravado; `[whispers]` + `[warmly]` on intimate lines; `[giggling]` only with a second lead tag.
- **Kaoru:** `[deadpan]` / `[dismissive]` + `[calm]` for dry control; `[warmly]` + `[calm]` on companion charm (`kaoru_321`); `[whispers]` + `[calm]` on intimate signing; **no tags** on koan lines only.
- **Narrator:** `[pause]` + `[dramatic]` on rain gameover, punishment escort (`narrator_269`), investigation/action; `[whispers]` + `[pause]` on implied-intimacy narration.
- Heuristics + `MANUAL_OVERRIDES` live in `scripts/performance_tagging.py`. Rain epilogue narrator ids are `narrator_108`–`narrator_115` (first-appearance order in `narrator_manifest.json`).

## Related files

| File | Role |
|------|------|
| `scripts/voice_performance_manifest.json` | Tagged TTS source |
| `scripts/sync_voice_performance_manifest.py` | Sync / diff / tag |
| `scripts/performance_tagging.py` | Heuristic tag pass + `weave_delivery_tags()` |
| `scripts/enrich_manifest_delivery_tags.py` | Batch rewrite `tts_text` with woven delivery tags |
| `scripts/voice_performance_lib.py` | Shared load/merge |
| `scripts/regenerate_voice_with_metadata.py` | Consumes `tts_text` |

## Changelog

- **2026-06-04** — Woven delivery tags: `weave_delivery_tags()`, `enrich_manifest_delivery_tags.py`, backup `scripts/versions/voice_performance_manifest-pre-delivery-tags-2026-06-03.json`. Result: **870/871** with 2+ tags; **398/871 (45.7%)** with reaction/pause tags; **272/871 (31.2%)** mid-woven. Review: [voice-performance-manifest-review.md](voice-performance-manifest-review.md). **No MP3 regen.**

- **2026-06-04** — Tagging policy (2+ tags, scene+arc): `performance_tagging.py` (`MIN_TAGS_PER_LINE`, `ensure_min_tags`, expanded `MANUAL_OVERRIDES` for `kaoru_321`, punishment bridge `toa_272`–`276` / `kaoru_322`–`327` / `narrator_269`). Pipeline: `build_manifest.py` → `sync_voice_performance_manifest.py --apply-tags --retag-all`. Result: **870/871** lines with 2+ tags; review excerpt in [voice-performance-manifest-review.md](voice-performance-manifest-review.md). **No MP3 regen.**

- **2026-06-04** - Staged regen promote: **886** lines from `game/audio/voice/v2/eve-donovan-2026-06-04/` to legacy `game/audio/voice/{id}.mp3`; prior legacy in `game/audio/voice/versions/staged-regen-legacy-backup-2026-06-04/` (**838** backed up). Log: `scripts/promote_v2_legacy_2026-06-04.log`. eleven_v3 stages 1-8 + 8b.

- **2026-06-03** - Case 3/4 investigation greenfield (`scripts/case34_investigation_voice_ids.txt`): **86** lines (toa 26, kaoru 38, narrator 22; ranges `toa_246`-`toa_271`, `kaoru_283`-`kaoru_320`, `narrator_247`-`narrator_268`). Pipeline: `wire_case34_investigation_voice.py`, `build_manifest.py`, `sync_voice_performance_manifest.py --apply-tags`, `regenerate_voice_with_metadata.py --model eleven_v3 --force --concurrency 4`; promoted from `game/audio/voice/v2/eve-donovan-2026-06-03/` to legacy `game/audio/voice/{id}.mp3`. API failures: 0.

- **2026-06-03** - Case 2 greenfield (`scripts/case2_voice_ids.txt`): **92** lines (toa 35, kaoru 39, narrator 18; ranges `toa_211`-`toa_245`, `kaoru_244`-`kaoru_282`, `narrator_229`-`narrator_246`). Pipeline: `wire_case2_voice.py`, `build_manifest.py`, `sync_voice_performance_manifest.py --apply-tags`, `regenerate_voice_with_metadata.py --model eleven_v3 --force --concurrency 4`; promoted from `game/audio/voice/v2/eve-donovan-2026-06-03/` to legacy `game/audio/voice/{id}.mp3`. API failures: 0.

- **2026-06-03** - Case 1 + Case 3.5 legacy v3 regen (`scripts/case1_case35_voice_batch_ids.txt`): **352** lines (toa 105, kaoru 125, narrator 122; ranges `toa_067`-`toa_172`, `kaoru_081`-`kaoru_205`, `narrator_052`-`narrator_173`). Pipeline: `sync_voice_performance_manifest.py --apply-tags`, `retag_performance_ids.py`, `regenerate_voice_with_metadata.py --model eleven_v3 --force --concurrency 4` (Toa `Ylb1ch6nQEKvpaUivWj6`, Kaoru `zyxAdkuEJWvr177AyQPs`, Narrator `giAoKpl5weRTCJK7uB9b`); promoted from `game/audio/voice/v2/eve-donovan-2026-06-03/` to legacy `game/audio/voice/{id}.mp3`; 228 prior legacy takes in `game/audio/voice/versions/case1-case35-voice-backup-2026-06-03/`. API failures: 0.

- **2026-06-03** — Courtesy-bow TTS disambiguation batch (`scripts/bow_disambig_ids.txt`): kaoru_007, kaoru_015, kaoru_092, kaoru_233, narrator_023, narrator_095, narrator_097, narrator_099, narrator_108, narrator_126, narrator_152, narrator_154, toa_197.

- **2026-06-03** - Bad ends VO batch (scripts/bad_end_voice_ids.txt): **99** lines (kaoru 23, toa 23, narrator 53) across prologue rain/brothel/Kaoru pursuit, Case 1 punishment + canal/2/3/4/4.5 game overs, injury/slayn warnings. Regen: eleven_v3 → game/audio/voice/v2/eve-donovan-2026-06-03/; promoted to legacy game/audio/voice/{id}.mp3 with prior takes in game/audio/voice/versions/bad-end-voice-backup-2026-06-03/. Wired 84 new oice lines via scripts/wire_bad_end_voice.py; API failures: 0.
