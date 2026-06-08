---
name: novelai-image-gen
description: >-
  Generates Ryoko Owari romance and canon-ending CGs via NovelAI Image API
  (scripts/generate_novelai_image.py, novelai_prompts.json). Use when the user
  asks for NovelAI, external CG generation, romance CG regen, prologue embrace
  art, case1 lantern, case2 morning, or NSFW-tasteful otome CGs for Toa/Kaoru.
---

# NovelAI Image Generation — Ryoko Owari

Complements [vn-art-pipeline](../vn-art-pipeline/SKILL.md) (Cursor `GenerateImage` for placeholders). **NovelAI** is for higher-control romance/CG production when the user has a subscription and API token.

## Prerequisites

| Item | Location |
|------|----------|
| API token | `NOVELAI_API_KEY` in `scripts/.env` (copy from `scripts/.env.example`) |
| Presets | `scripts/novelai_prompts.json` |
| CLI | `scripts/generate_novelai_image.py` |
| Doc | `docs/novelai-image-pipeline.md` |

**Never** commit `scripts/.env` or paste real keys into chat/commits.

If `NOVELAI_API_KEY` is missing: explain setup, run `--dry-run` only, do **not** call the live API.

## When to use

- User wants NovelAI-generated CGs for canon romance beats
- Regenerating `cg-canon-*` or case romance PNGs with danbooru-style tags + project anchors
- Comparing mild vs full presets before overwriting `game/images/cg/`

**Prefer `GenerateImage`** for quick placeholders, sprites, and mood boards (see vn-art-pipeline).

## API summary (current)

| | |
|--|--|
| Base | `https://image.novelai.net` |
| Generate | `POST /ai/generate-image` |
| Auth | `Authorization: Bearer <NOVELAI_API_KEY>` |
| Body | `{ "input": "<prompt>", "model": "<id>", "action": "generate", "parameters": { ... } }` |
| Response | ZIP containing one or more PNGs (script extracts first PNG) |

**Models (project default):** `nai-diffusion-4-5-full` — also documented: `nai-diffusion-4-full`, `nai-diffusion-3`. Prefer V4.5 for new CGs unless user specifies otherwise.

**Resolution:** Wallpaper landscape `1920×1088` (NovelAI max wallpaper; within 2048×1536 cap). Do not assume arbitrary 1920×1080 unless API accepts it; script defaults to 1920×1088.

**Parameters used:** `width`, `height`, `steps`, `scale` (CFG), `sampler` (`k_euler_ancestral`), `negative_prompt`, `n_samples: 1`, `qualityToggle: true`. **SMEA off** in this CLI (`sm: false`, `sm_dyn: false`) — NovelAI’s web UI can auto-enable SMEA above 1024×1024; our 1536×1024 runs use standard sampling unless you change the script.

**Character Precise Reference defaults:** `ref_strength` / `ref_fidelity` = **1.0** (max; `director_reference_strength_values` and `1 - fidelity` → secondary 0.0). Style refs use `_meta.style_ref_strength` / `style_ref_fidelity` separately.

**Style tags:** `_meta.style_tags` / `style_negative` prepended to all presets — painterly dark otome look, anti-chibi/cartoon. See [docs/novelai-image-pipeline.md](../../docs/novelai-image-pipeline.md#painterly-style-anti-cartoon).

**Precise Reference (V4.5):** `director_reference_images`, `director_reference_descriptions`, `director_reference_strength_values`, `director_reference_secondary_strength_values` (fidelity = `1 - secondary`), `director_reference_information_extracted`. Types per reference: `character`, `style`, `character&style`. Character + style refs can mix in one request. **Not compatible with Vibe Transfer** in the same request. Docs: https://docs.novelai.net/en/image/precisereference/

## Limitations and errors

| Code | Meaning | Agent action |
|------|---------|--------------|
| 401 | Invalid/expired token | User renews Persistent API token |
| 402 | No Anlas / subscription | User tops up at novelai.net |
| 429 | Rate limit | Wait, retry |
| 400/422 | Bad size/model/prompt | Check dimensions, model id, prompt length |
| Policy in body | Content moderation | Use `*_mild` preset; reduce explicit tags |

Script uses **stdlib only** (`urllib`, `zipfile`) — same `.env` loader pattern as `generate_duet_song.py`.

## Content boundaries (project + ToS)

Follow [canon-encounter-beats.md](../../docs/canon-encounter-beats.md) and NovelAI Terms:

- **R-rated sensual**, tasteful implied intimacy — otome/L5R power dynamic
- **No** genitalia, pornographic close-ups, or explicit intercourse on-screen
- Fade-to-black beats stay **off-CG** (embrace is max heat for prologue)
- Kaoru: **no oni mask**, no Kitsu spirit imagery on sprites/CGs
- Toa: black **kosode** (not furisode), **gold crane obi**, white eyelashes

Generate **mild** alternates (`prologue_embrace_mild`, `case1_lantern_mild`) into `assets/cg/` before overwriting canon files.

## Romance CG presets (7 + mild backups)

| Preset | Output file | Ren'Py tag |
|--------|-------------|------------|
| `prologue_proposition` | `game/images/cg/cg-canon-proposition.png` | `canon_proposition` |
| `prologue_pull_close` | `cg-canon-pull-close.png` | `canon_pull_close` |
| `prologue_undressing` | `cg-canon-undressing.png` | `canon_undressing` |
| `prologue_embrace` | `cg-canon-embrace.png` | `canon_embrace` |
| `prologue_afterglow` | `cg-canon-afterglow.png` | `canon_afterglow` |
| `case1_lantern` | `cg-case1-romance-lantern.png` | `case1_romance_lantern` |
| `case2_morning` | `cg-case2-romance-morning.png` | `case2_romance_morning` |

Signing / three-days canon CGs are **non-romance** — use inline `--prompt` or extend `novelai_prompts.json` if needed.

Character tag anchors live in `novelai_prompts.json` → `character_tags` (`toa_tags`, `kaoru_tags`). Keep aligned with vn-art-pipeline specs.

## Workflow

```
1. Confirm NOVELAI_API_KEY (or guide user through .env setup)
2. --dry-run --preset <name>  → review prompt/size
3. Generate → writes preset output path
4. User reviews PNG in game/images/cg/ or assets/
5. Promote: backup old PNG if replacing production art
6. Launch Ren'Py — gallery unlocks via existing show_cg_scene paths (no.rpy change if filename unchanged)
```

**Gallery:** `game/gallery.rpy` already references the `cg-canon-*` and romance paths above. New filenames require gallery + `cgs-*.rpy` updates.

**Wiring files:**

- `game/images/cgs-canon-ending.rpy` — prologue canon CGs
- `game/case_endings.rpy` — `case1_romance_lantern`, `case2_romance_morning`
- `game/prologue_canon_encounter.rpy` — beat sequence

## CLI examples

```bash
python scripts/generate_novelai_image.py --list-presets
python scripts/generate_novelai_image.py --dry-run --preset prologue_embrace
python scripts/generate_novelai_image.py --preset case1_lantern
python scripts/generate_novelai_image.py --preset prologue_embrace_mild
python scripts/generate_novelai_image.py --prompt "..." --negative "lowres" --output assets/cg/test.png --seed 42
```

Override generation: `--width`, `--height`, `--steps`, `--scale`, `--sampler`, `--model`, `--seed`.

**Character Precise Reference (canonical PNGs):**

| Character | Path | Size |
|-----------|------|------|
| Toa (work) | `game/images/reference/toa-precise-reference.png` | 1536×1024 |
| Toa (date) | `game/images/reference/toa-date-precise-reference.png` | 1536×1024 |
| Kaoru (ponytail) | `game/images/reference/kaoru-precise-reference.png` | 1536×1024 |
| Kaoru (hair-down) | `game/images/reference/kaoru-hair-down-precise-reference.png` | 1536×1024 |
| Toa (Modern AU tracksuit) | `docs/art-references/au-modern/toa-au-modern-tracksuit-turnaround-reference.png` | 1536×1024 |
| Kaoru (Modern AU suit) | `docs/art-references/au-modern/kaoru-au-modern-suit-turnaround-reference.png` | 1536×1024 |

All Precise Reference sheets use a **2×2 turnaround** (front / back / side / face) on plain grey — see `vn-art-pipeline` skill.

`_meta.char_ref_sprites` in `novelai_prompts.json` points here (not neutral sprites). Regenerate when sprites/outfits change — see [docs/novelai-image-pipeline.md](../../docs/novelai-image-pipeline.md#character-precise-reference-files-canonical).

**Regen via Cursor:** `GenerateImage` + sprite/CG anchors — turnaround model sheet, plain background, Hakuoki style.

**Regen via NovelAI:**

```bash
python scripts/generate_novelai_image.py --dry-run --preset toa_ref
python scripts/generate_novelai_image.py --preset toa_ref
python scripts/generate_novelai_image.py --dry-run --preset toa_date_ref
python scripts/generate_novelai_image.py --preset toa_date_ref
python scripts/generate_novelai_image.py --dry-run --preset kaoru_ref
python scripts/generate_novelai_image.py --preset kaoru_ref
python scripts/generate_novelai_image.py --dry-run --preset kaoru_hair_down_ref
python scripts/generate_novelai_image.py --preset kaoru_hair_down_ref
python scripts/generate_novelai_image.py --dry-run --preset toa_au_ref
python scripts/generate_novelai_image.py --preset toa_au_ref
python scripts/generate_novelai_image.py --dry-run --preset kaoru_au_ref
python scripts/generate_novelai_image.py --preset kaoru_au_ref

# Romance CGs: both precise refs by default (see _meta.char_ref_sprites)
python scripts/generate_novelai_image.py --dry-run --preset prologue_embrace
python scripts/generate_novelai_image.py --preset prologue_embrace --no-char-ref --toa-ref
python scripts/generate_novelai_image.py --char-ref game/images/reference/toa-precise-reference.png --ref-strength 1.0 --ref-fidelity 1.0 --ref-type character

# Painterly style: tags auto-prepended; optional style Precise Reference (mixes with char refs)
python scripts/generate_novelai_image.py --preset test_festival
python scripts/generate_novelai_image.py --preset prologue_embrace --style-ref
python scripts/generate_novelai_image.py --no-char-ref --no-style-ref --vibe
```

Preset JSON keys: boolean `toa_ref` / `kaoru_ref` / `style_ref` on romance presets; dedicated presets `toa_ref` / `toa_date_ref` / `toa_au_ref` / `kaoru_ref` / `kaoru_hair_down_ref` / `kaoru_au_ref` / `test_festival`. Hair-down Kaoru CGs: pass `--char-ref game/images/reference/kaoru-hair-down-precise-reference.png` or use `{kaoru_hair_down_tags}` in custom prompts. Modern AU uses `_meta.au_modern_char_refs`, not `char_ref_sprites`. Also: `char_refs`, `ref_strength`, `ref_fidelity`, `style_ref_strength`, `style_ref_fidelity`, `ref_type`. Style sheet: `_meta.style_ref_sprite` → `game/images/reference/style-painterly-reference.png`. Vibe mood board: `assets/reference/yone-style-vibe-source.png` (use with `--no-char-ref --vibe` only).

## Editing prompts

1. Open `scripts/novelai_prompts.json`
2. Edit preset `prompt` / `negative_extra` / `scene`
3. Use `{toa_tags}`, `{kaoru_tags}`, and `{style_tags}` placeholders — do not duplicate full character or style blocks inline
4. Tune `_meta.style_tags` / `style_negative` for painterly vs cartoony balance
5. Dry-run before live generation

## Agent checklist

- [ ] Read vn-art-pipeline for Hakuoki + L5R anchors
- [ ] Check key present; else setup instructions + dry-run only
- [ ] Dry-run before spending Anlas
- [ ] Backup existing `game/images/cg/` PNG if overwriting
- [ ] Offer mild preset if policy error or user wants safer gallery art
- [ ] Do not commit secrets or `scripts/.env`

## Additional resources

- Pipeline doc: [docs/novelai-image-pipeline.md](../../docs/novelai-image-pipeline.md)
- Canon beats: [docs/canon-encounter-beats.md](../../docs/canon-encounter-beats.md)
- NovelAI Image API: https://image.novelai.net/docs/index.html
