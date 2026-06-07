# NovelAI image pipeline

External CG generation for **Ryoko Owari** romance and canon-ending art via the NovelAI Image API.

## Quick links

| Resource | Path |
|----------|------|
| Agent skill | [.cursor/skills/novelai-image-gen/SKILL.md](../.cursor/skills/novelai-image-gen/SKILL.md) |
| CLI | [scripts/generate_novelai_image.py](../scripts/generate_novelai_image.py) |
| Presets | [scripts/novelai_prompts.json](../scripts/novelai_prompts.json) |
| Art direction (shared) | [.cursor/skills/vn-art-pipeline/SKILL.md](../.cursor/skills/vn-art-pipeline/SKILL.md) |

## Setup

1. Copy `scripts/.env.example` → `scripts/.env`
2. Add `NOVELAI_API_KEY=` with your [Persistent API token](https://novelai.net/) (User Settings)
3. Active NovelAI subscription with Anlas for image generations
4. Python 3.10+ (stdlib only — no extra packages)

## Usage

```bash
# List romance presets
python scripts/generate_novelai_image.py --list-presets

# Preview request without spending Anlas
python scripts/generate_novelai_image.py --dry-run --preset prologue_embrace

# Generate into game/images/cg/ (overwrites target — back up first)
python scripts/generate_novelai_image.py --preset prologue_embrace

# V4.5 Precise Reference (Character Reference) — uses director_reference_* API fields
python scripts/generate_novelai_image.py --preset prologue_embrace --toa-ref --ref-strength 0.75 --ref-fidelity 0.35
python scripts/generate_novelai_image.py --preset prologue_embrace --no-char-ref   # tags only, no sprite refs

# Character + Style Precise Reference (same request; per-ref type in director_reference_descriptions)
python scripts/generate_novelai_image.py --preset test_festival
python scripts/generate_novelai_image.py --preset prologue_embrace --style-ref

# Vibe-only pass (no Precise Reference — incompatible in same request)
python scripts/generate_novelai_image.py --preset test_festival --no-char-ref --no-style-ref --vibe

# Custom prompt
python scripts/generate_novelai_image.py --prompt "..." --negative "extra tags" --output assets/test.png
```

After promoting art, verify in Ren'Py: `game/images/cgs-canon-ending.rpy`, `game/case_endings.rpy`, `game/gallery.rpy`.

## Official API

- Image API docs: https://image.novelai.net/docs/index.html
- Precise Reference (UI): https://docs.novelai.net/en/image/precisereference/
- Endpoint: `POST https://image.novelai.net/ai/generate-image`
- Auth: `Authorization: Bearer <NOVELAI_API_KEY>`
- Terms: https://novelai.net/terms — follow NovelAI and project content boundaries

### Precise Reference (V4.5 only)

Maps to `parameters` on the generate request (reverse-engineered from NovelAI’s web client; see [novelai-bridge](https://github.com/RhNu/novelai-bridge)):

| UI / concept | API field | Notes |
|--------------|-----------|--------|
| Reference image(s) | `director_reference_images` | Base64 PNG per image |
| Character / Style / both | `director_reference_descriptions[].caption.base_caption` | `"character"`, `"style"`, or `"character&style"` |
| Strength | `director_reference_strength_values` | 0–1 per reference |
| Fidelity | `director_reference_secondary_strength_values` | `1 - fidelity` per reference |
| (fixed) | `director_reference_information_extracted` | `[1.0, …]` per reference |

**Incompatible with Vibe Transfer** (`reference_image_multiple`, etc.) in the same request. The CLI omits vibe fields when Precise Reference is active.

Romance presets auto-attach Toa + Kaoru **Precise Reference** sheets from `novelai_prompts.json` → `_meta.char_ref_sprites` unless `--no-char-ref`. Per-preset overrides: `toa_ref`, `kaoru_ref`, `char_refs`, `ref_strength`, `ref_fidelity`, `ref_type`.

**Character + Style in one request:** attach character refs with `type=character` and a style mood sheet with `type=style` in the same `director_reference_*` arrays (NovelAI allows mixing reference types). Enable via preset `style_ref: true`, `--style-ref`, or `_meta.romance_presets_style_ref`. Default style sheet: `game/images/reference/style-painterly-reference.png`.

Extra Anlas cost applies per NovelAI docs (+5 per reference).

## Painterly style (anti-cartoon)

NovelAI defaults can skew **cartoony / chibi / flat cel-shading**. The project prepends `_meta.style_tags` to every preset prompt and adds `_meta.style_negative` to the shared negative.

| Field | Purpose |
|-------|---------|
| `_meta.style_tags` | Painterly dark otome illustration tags (semi-realistic, mature features, dramatic lighting, etc.) |
| `_meta.style_negative` | Blocks chibi, cartoon, flat cel shading, moe proportions |
| `_meta.style_ref_sprite` | Style Precise Reference PNG (no characters) — painterly mood board |
| `assets/reference/yone-style-vibe-source.png` | Vibe Transfer source when `--no-char-ref --vibe` |

Phrasing is **painterly dark otome illustration** — not named-artist mimicry. Regenerate the style sheet when you want a different palette or brush texture.

**Workflows**

| Goal | Command |
|------|---------|
| Tags + char + style refs | `--preset test_festival` (or `--style-ref` on any romance preset) |
| Tags + vibe only (no char refs) | `--no-char-ref --no-style-ref --vibe` |
| Tags only | `--no-char-ref --no-style-ref` |

Compare outputs in `assets/cg/` before promoting to `game/images/cg/`.

### Character Precise Reference files (canonical)

| Character | Path | Size | Role |
|-----------|------|------|------|
| Kakita Toa | `game/images/reference/toa-precise-reference.png` | 1536×1024 | NovelAI V4.5 `director_reference_*` default for Toa |
| Kitsu Kaoru | `game/images/reference/kaoru-precise-reference.png` | 1536×1024 | Same for Kaoru |
| Style (painterly) | `game/images/reference/style-painterly-reference.png` | 1536×1024 | `type=style` Precise Reference — no characters |

**Best practices (NovelAI):** full-body or upper-body standing, neutral pose, plain/simple background, character large on canvas, clean Hakuoki otome illustration. Landscape **1536×1024** matches existing `game/images/cg/*.png`. Style reference should be a **scenic mood board** (canals, lanterns, painterly texture) with no people.

**When to regenerate**

- Canonical **sprites** change (`toa-neutral.png`, `kaoru-smirk.png`) — outfit, hair, or face drift
- Outfit anchors change (Toa: black kosode + gold crane obi; Kaoru: emerald/crimson magistrate robes, no mask)
- Romance/CG generations show consistent wrong face or costume despite tags

**How to regenerate**

1. **Cursor (free, no Anlas):** Agent uses `GenerateImage` with sprite paths in `reference_image_paths`, saves to the table paths above, verifies 1536×1024 (resize with Pillow if needed).
2. **NovelAI (optional):** `python scripts/generate_novelai_image.py --preset toa_ref` or `--preset kaoru_ref` — presets anchor on sprites via `char_refs`, output overwrites the precise-reference PNGs. Dry-run first.

After regen, `_meta.char_ref_sprites` should already point at these files; no preset edits required unless paths change.
