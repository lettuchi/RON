# Intimate closeup CG pass (2026-06-04)

Artful macro closeups supplementing full-scene CGs. Six new Ren'Py tags; five generated via Cursor `GenerateImage`, one stub pending NovelAI regen.

## Modern AU

Canon closeup refs below are **L5R period**. For **Wrong Floor / AU Case 1** CGs, attach AU outfit refs from [au-modern-character-references.md](au-modern-character-references.md) (`docs/art-references/au-modern/*-reference.png`; waist-up variants for bust shots). Canon sprites = face/hair only. Tags: `scripts/au_modern_cg_prompt_block.txt`.

## Generated (in `game/images/cg/`)

| Tag | File | Status |
|-----|------|--------|
| `case1_5_shoji_wrist` | `cg-case1_5-shoji-wrist-closeup.png` | Generated |
| `case1_5_shoji_tear` | `cg-case1_5-shoji-tear-closeup.png` | Generated |
| `case3_5_date_inn_collar_hands` | `cg-case3_5-date-inn-collar-hands.png` | Generated |
| `case4_5_boat_lash_rain` | `cg-case4_5-boat-lash-rain-closeup.png` | Generated |
| `case4_5_boat_hands_gunwale` | `cg-case4_5-boat-hands-gunwale-closeup.png` | Generated |
| `case5_oath_seal_hand` | `cg-case5-oath-seal-hand-closeup.png` | Generated |

## Stub / regen (NovelAI)

| Tag | File | Status |
|-----|------|--------|
| `epilogue_kotatsu_warmth` | `cg-epilogue-kotatsu-warmth-closeup.png` | **Stub** (copy of `cg-epilogue-romance-kotatsu-intimate.png`). GenerateImage blocked on skin-contact prompts. |

### NovelAI prompt: `epilogue_kotatsu_warmth`

Use `_meta.style_tags` from `scripts/novelai_prompts.json` (anime painterly, not semi-realistic verbatim in GenerateImage).

```
macro closeup under kotatsu, wool quilt hem only, two pairs of socked feet and hakama hems touching, mikan peel on low tray, rain on shoji bokeh, shallow depth of field, warm afternoon, Hakuoki otome, Ryoko Owari, suggestive domestic warmth, no nudity, no bare thighs, clothed, 1536x1024 landscape
```

Reference: `docs/art-references/ref-closeup-wrist.png` (composition only), `game/images/cg/cg-epilogue-romance-kotatsu-intimate.png` (palette).

## Style block

Always prepend/append [docs/cg-style-prompt-block.md](cg-style-prompt-block.md). Composition refs: `docs/art-references/ref-closeup-wrist.png`, `ref-closeup-lash-rain.png`, `ref-closeup-wet-manuscript-hands.png`.

## Modern AU closeups

For AU Wrong Floor / Case 1 intimate or bust shots: use **AU waist-up outfit refs** (not canon sprites alone) — see [au-modern-character-references.md](au-modern-character-references.md). Tags: `scripts/au_modern_cg_prompt_block.txt`.

## Hand QA (optional)

```bash
python scripts/check_cg_hands.py --path game/images/cg/cg-case1_5-shoji-wrist-closeup.png
```

## Audio regen

New voice IDs: `kaoru_384`–`386`, `toa_318`, `narrator_304`–`311`.

Changed lines (re-record): `kaoru_374`–`378`, `380`, `382`–`383`, `175`–`176`, `183`–`184`, `196`, `199`–`200`, `205`, `212`, `217`, `221`, `351`, `353`–`355`, `363`–`364`; `narrator_300`, `162`, `172`, `180`–`181`, `277`–`278`, `283`–`284`.

Run Eleven v3 regen for touched `tts_text` in `scripts/voice_performance_manifest.json` (batch TBD). Optional: `python scripts/apply_tts_tag_enrichment.py` on changed Kaoru lines for richer tags than the one-off patch `[calm]` prefix.
