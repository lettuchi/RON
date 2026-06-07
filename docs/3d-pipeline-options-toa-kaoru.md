# 3D Pipeline Options — Kakita Toa & Kitsu Kaoru

**Date:** 2026-06-04  
**Scope:** What Cursor/agents can use today vs. what requires new plugins, APIs, or human 3D work.  
**Related:** [`docs/3d-character-spec-toa-kaoru.md`](3d-character-spec-toa-kaoru.md), [`scripts/3d_model_request_template.md`](../scripts/3d_model_request_template.md), [`scripts/generate_3d_placeholders.py`](../scripts/generate_3d_placeholders.py)

---

## Executive summary (for agents)

- **Meshy MCP is configured in-repo** (`.cursor/mcp.json.example` → copy to `.cursor/mcp.json`, user adds `MESHY_API_KEY`). Project `mcps/` folder still lists only browser/app control until Cursor loads the meshy server.
- **Meshy REST script:** `scripts/meshy_image_to_3d.py` — setup in [`docs/meshy-setup.md`](meshy-setup.md).
- **In-repo today:** labeled **placeholder mannequins** (`assets/3d/*-placeholder.glb`) via `trimesh`, not production anime meshes.
- **`scripts/.env.example` includes `MESHY_API_KEY`** (placeholder). Add your `msy_…` key in gitignored `scripts/.env`; optionally mirror in `.cursor/mcp.json` for MCP.
- **Recommended path for this VN:** 2D reference locks → **Meshy image-to-3D** (or Tripo multi-view) → **Blender retopo/UV/rig** → **glTF to `assets/3d/`** — treat 3D as **reference / cinematics / experiments**, not Ren'Py sprite replacement.

---

## 1. MCP servers (this workspace)

**Location:** `C:\Users\Amanda\.cursor\projects\c-Users-Amanda-Developer-ryoko-owari\mcps\`

### Enabled servers and tools

| Server | Tools | 3D / mesh / Blender / glTF? |
|--------|-------|-----------------------------|
| **cursor-ide-browser** | `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_fill`, `browser_select_option`, `browser_scroll`, `browser_press_key`, `browser_drag`, `browser_lock`, `browser_take_screenshot`, `browser_cdp`, `browser_tabs`, `browser_highlight`, `browser_get_bounding_box`, `browser_mouse_click_xy` | **No** — web UI only (could drive Meshy/Tripo *websites* manually; fragile for downloads/auth) |
| **cursor-app-control** | `open_automation`, `rename_chat`, `create_project`, `move_agent_to_root`, `move_agent_to_cloned_root` | **No** |

### Clear statement

**There is no MCP for 3D modeling, Blender, mesh editing, or glTF in this project today.**

### Meshy MCP (configured in repo — user adds key)

| Service | MCP | Notes |
|---------|-----|--------|
| **Meshy** | `@meshy-ai/meshy-mcp-server` | **Configured:** [`.cursor/mcp.json.example`](../.cursor/mcp.json.example) → `.cursor/mcp.json`. Setup: [`docs/meshy-setup.md`](meshy-setup.md). Requires `MESHY_API_KEY` (`msy_…`). |

### Optional MCP not installed (external)

| Service | MCP | Notes |
|---------|-----|--------|
| **Tripo** | No official Cursor MCP found in project docs | Use REST API or browser; see [Tripo API](https://www.tripo3d.ai/api) |
| **Blender** | None standard | Use Shell + `blender --background` if Blender is on PATH |

Windows Cursor config (also in `.cursor/mcp.json.example`):

```json
"meshy": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@meshy-ai/meshy-mcp-server"],
  "env": { "MESHY_API_KEY": "msy_YOUR_KEY" }
}
```

---

## 2. Project tooling (in-repo)

| Asset / script | Role |
|----------------|------|
| `scripts/generate_3d_placeholders.py` | Builds **colored primitive mannequins** (cylinders/boxes) at correct heights/colors; exports `.glb` via **trimesh** |
| `docs/3d-character-spec-toa-kaoru.md` | Canonical heights, hex colors, outfit variants, glTF export settings, Ren'Py facing notes |
| `scripts/meshy_image_to_3d.py` | Meshy **image→3D** REST: `--check`, `--character`, `--image` → `assets/3d/raw/meshy-*/` |
| `scripts/3d_model_request_template.md` | Prompt packs + Tripo/Meshy/Blender checklist for **external** generation |
| `assets/3d/toa-placeholder.glb`, `kaoru-placeholder.glb` | Blocking silhouettes — **not** anime production meshes |

**Dependencies (documented, not in `requirements-voice.txt`):**

```bash
pip install trimesh numpy scipy
python scripts/generate_3d_placeholders.py
```

### API keys in `scripts/.env.example` (names only)

| Key name | Purpose |
|----------|---------|
| `ELEVENLABS_API_KEY` | Voice TTS |
| `ELEVENLABS_VOICE_V2_TOA`, `ELEVENLABS_VOICE_V2_KAORU`, `ELEVENLABS_VOICE_V2_NARRATOR` | Voice IDs |
| `ELEVENLABS_MODEL_ID` | TTS model |
| `NOVELAI_API_KEY` | 2D CG generation |
| `NOVELAI_ACCOUNT_ID` | Optional reference |
| `MESHY_API_KEY` | Meshy image→3D (`scripts/meshy_image_to_3d.py`) |

**Suggested additions** (user adds to `scripts/.env` when scripting exists):

| Key name | Service |
|----------|---------|
| `TRIPO_API_KEY` | Tripo image/multi-image→3D API (if/when a download script is added) |

---

## 3. Cursor / agent capabilities (multi-step, no new plugins)

| Capability | What it can do for Toa/Kaoru 3D | Limit |
|------------|----------------------------------|-------|
| **GenerateImage** | Strong **2D** reference sheets, ortho turnarounds, texture guides from locked sprites | **2D only** — not a mesh |
| **Shell** | Run `generate_3d_placeholders.py`; if Blender installed: `blender --background script.py` for batch import/export/validate | Blender **not verified** in agent sandbox this session; user must confirm `blender --version` locally |
| **Python (trimesh)** | Placeholders, simple mesh merge, format export to `.glb` | No anime topology, rig, or kimono cloth sim |
| **Python (pygltflib)** | Optional glTF validation/metadata — not in repo requirements yet | Install if adding validation scripts |
| **WebFetch** | Read Meshy/Tripo API docs | Cannot call paid APIs without keys in env |
| **meshy_image_to_3d.py** | Poll Meshy, download GLB to `assets/3d/raw/` | Requires `MESHY_API_KEY` in `scripts/.env` |
| **browser MCP** | Could upload refs on Meshy/Tripo web UI | Login, CAPTCHA, credit billing, inconsistent automation — **not recommended** as primary pipeline |
| **Read / edit repo** | Specs, prompts, Blender export checklists, folder layout under `assets/3d/` | Cannot judge final anime likeness without human review |

---

## 4. External services (comparison)

Ranked for **this project**: anime humanoids from **existing VN sprite PNGs**, export **glTF/GLB**, then Blender cleanup.

| Service | Reference image input | glTF / GLB export | API / automation | Typical cost model | Fit for Toa/Kaoru |
|---------|----------------------|-------------------|------------------|--------------------|-------------------|
| **Meshy** | Yes — `image-to-3d`, `multi-image-to-3d`; rigging + animation APIs | Yes — `model_urls.glb` (also FBX, OBJ, USDZ) | REST + **optional MCP**; async poll/webhook | Credits per task (e.g. image→3D **20–30 credits** with Meshy-6 + texture) | **Best API fit** for agent scripting once `MESHY_API_KEY` is set |
| **Tripo AI** | Yes — image + **multi-view** (front/side/top) | Yes — mesh conversion in post-processing (formats per plan) | REST platform; marketing emphasizes character/object | Credit/subscription (check [platform.tripo3d.ai](https://platform.tripo3d.ai)) | Strong for **multi-angle** if you generate side views from sprites |
| **Rodin / Hyper3D** | Yes (web product) | GLB/OBJ typical on download | Mostly **web UI**; docs page unstable for agents | Per-generation credits | Good one-off sculpts; **kimono/hair** need heavy cleanup |
| **Luma Genie** | Image/text (product evolves) | Often USDZ/GLB depending on tier | Web + some API tiers | Subscription | Better for objects/scenes than VN-grade anime rig |
| **CSM (Common Sense Machines)** | Image→3D | glTF common | API (docs intermittently unavailable) | Commercial | Worth trial; less documented in-repo than Meshy |
| **Blender + human** | Image planes from `game/images/sprites/…` | Native glTF 2.0 export | Fully local; agent can write `.py` for **batch** steps only if Blender on PATH | Free (artist time **40–120+ h** per spec doc) | **Required** for production rig, obi/sleeves, expression shape keys |

### Quality expectations (honest)

- **AI image→3D** on full-body anime sprites: usable **block-in** or **VRChat-adjacent** sculpts, not Hakuoki-quality game meshes without retopo.
- **Separate passes** needed: Toa `work` vs `date` furisode; Kaoru default vs festival gold haori (see `3d_model_request_template.md`).
- **Negatives matter:** Tripo/Meshy will often hallucinate furisode sleeves, masks, or photoreal skin unless prompts + negatives from the template are used.

### API vs manual export

| Approach | Pros | Cons |
|----------|------|------|
| **API (Meshy)** | Agent can poll, download GLB into `assets/3d/raw/` | Credits; assets expire (~**3 days** on Meshy non-Enterprise — download immediately) |
| **Manual web export** | Visual QA per character | Not repeatable; agent cannot run unattended |

---

## 5. Ren'Py integration angle

**Shipped game today:** **2D only** — `layeredimage` sprites in `game/images/characters.rpy`, bust crops in `game/ui_layout.rpy`, CG layering in `game/scene_layering.rpy`. No `Model()` or glTF displayables in game scripts.

| Use case | Realistic role for 3D |
|----------|------------------------|
| **VN runtime sprites** | **Not recommended** — 2D pipeline is mature; 3D would not match painterly CGs without custom shaders |
| **Reference sculpt / scale check** | Placeholders + eventual glTF in Blender with image planes at 180 cm / 173 cm |
| **Blender cinematics** | Pre-rendered video or image sequences for trailers/menus |
| **Live2D alternative** | Separate toolchain; 3D does not replace Live2D without new engine work |
| **Unity / Godot side project** | glTF export from spec doc is appropriate |
| **Future Ren'Py 3D experiment** | Community `Model` patterns; spec already notes yaw facing (Toa left, Kaoru right) |

**Conclusion:** 3D supports **pre-production, marketing, and optional gallery** — not replacing `toa-neutral.png` / `kaoru-smirk.png` without a major art-direction pivot.

---

## 6. Options table

| Option | Tools needed | Steps | Quality | Agent can automate? | User must do? |
|--------|--------------|-------|---------|---------------------|---------------|
| **A. In-repo placeholders** | Python, trimesh | Run `generate_3d_placeholders.py` | Blocking scale only | **Yes** fully | Nothing |
| **B. Meshy image→3D** | `MESHY_API_KEY`, REST or Meshy MCP | Upload sprite URL → poll → download GLB → commit to `assets/3d/raw/` | Medium sculpt; bad sleeves/hands | **Mostly** (script + key) | Credit purchase; art QA; kimono cleanup |
| **C. Tripo multi-image→3D** | Tripo API key, 2–3 ref views | Front sprite + synthetic side (or CG crop) → generate → GLB | Good geometry on v3; textures vary | **Partial** (needs script) | Multi-view prep; subscription |
| **D. Rodin / Hyper3D web** | Browser, account | Upload PNG → download → import Blender | Variable; often stylized | **Low** (browser MCP brittle) | Manual export each time |
| **E. Blender manual** | Blender, spec PNGs | Planes → sculpt/retopo → UV → texture → Rigify → glTF | **Highest** for VN parity | **Partial** (Python export scripts if Blender installed) | Sculpt, weight paint, expressions |
| **F. 2D → better 2D refs** | GenerateImage, NovelAI (`NOVELAI_API_KEY`) | Ortho turnaround sheets for 3D artist | N/A (feeds D/E) | **Yes** for 2D refs | Commission or run D/E |
| **G. Commissioned artist** | Brief + `3d_model_request_template.md` | Artist delivers `.blend` + `.glb` | Production | Agent drafts brief/checklist | Pay, review, integrate assets |

---

## 7. Recommended 3-step path (this project)

Aligned with existing docs and realistic agent + human split.

### Step 1 — Image → mesh (AI)

1. Attach locked PNGs from `scripts/3d_model_request_template.md` (`toa-neutral.png`, `kaoru-smirk.png`, optional date lock).
2. Call **Meshy** `POST /openapi/v1/image-to-3d` with `image_url` (host sprites on a temporary HTTPS URL or use Meshy upload flow), `should_texture: true`, `enable_pbr: true` where supported.
3. Download `model_urls.glb` immediately to:
   - `assets/3d/raw/toa-work-meshy.glb`
   - `assets/3d/raw/kaoru-meshy.glb`
4. **Second pass** for Toa date furisode using `case3_5-toa-date-lock.png` (cropped) — do not merge outfits in one generation.

*Alternative:* Tripo **multi-image** if you create a side-view render (GenerateImage ortho) for higher silhouette accuracy.

### Step 2 — Blender cleanup (human-led, agent-assisted)

1. Import GLB; scale to **1.80 m / 1.73 m** (see spec).
2. Retopo anime edge flow; fix hands, obi, hakama pleats / furisode sleeves.
3. UV + project paint from 2D sprites; optional cel-shade materials.
4. Rigify (or custom) + weight paint sleeves/obi; optional shape keys per `characters.rpy` names.

Agent can help: write Blender Python for import/export, validation, batch rename — **if** Blender is installed and path is known.

### Step 3 — Export to repo

1. Export **glTF 2.0 binary** per spec (+Y up, 2K textures, named meshes `Toa_Kosode`, etc.).
2. Place production files at:
   - `assets/3d/toa-work.glb` (and later `toa-date.glb`)
   - `assets/3d/kaoru.glb`
3. Validate in [glTF Viewer](https://gltf-viewer.donmccurdy.com/).
4. Keep `*-placeholder.glb` until production assets pass checklist in `3d_model_request_template.md`.

---

## 8. Install & keys for future agent runs

| Item | Action |
|------|--------|
| **Python** | `pip install trimesh numpy scipy` (placeholders); optional `pygltflib` for validation |
| **Blender 4.x** | Install locally; add to PATH; verify `blender --version` |
| **Meshy** | `MESHY_API_KEY` in `scripts/.env`; copy [`.cursor/mcp.json.example`](../.cursor/mcp.json.example) → `.cursor/mcp.json`; see [`docs/meshy-setup.md`](meshy-setup.md) |
| **Tripo** | Developer account + API key if automating Tripo instead of Meshy |
| **Repo script** | `python scripts/meshy_image_to_3d.py --check` then `--character toa` / `kaoru` |

**Do not** commit API keys or pretend AI output is final shipped anime art.

---

## 9. What agents still cannot do fully autonomously

1. **Produce production-quality, rigged anime characters** matching Hakuoki-style 2D from a single API call.
2. **Correct kimono topology** (witness kosode vs furisode, obi crane, hakama pleats) without human Blender work.
3. **Rig weight painting** and **expression shape keys** at VN quality without artist time.
4. **Replace Ren'Py layeredimage sprites** in the shipped game without engine/shader work and new art direction.
5. **Run Blender** without a local install and tested background scripts.
6. **Guarantee likeness** to locked sprites — requires human art direction and iteration.
7. **Use Meshy MCP in Cursor** until you copy `mcp.json`, add a funded `MESHY_API_KEY`, and enable the server in MCP settings.

---

## 10. Quick reference — canonical 2D locks

| Character | Primary path |
|-----------|----------------|
| Toa witness | `game/images/sprites/toa/toa-neutral.png` |
| Toa date | `game/images/reference/case3_5-toa-date-lock.png` |
| Kaoru | `game/images/sprites/kaoru/kaoru-smirk.png` |
| Duo lighting | `game/images/cg/cg-case2-festival-kiss.png` |

Full tables: [`docs/3d-character-spec-toa-kaoru.md`](3d-character-spec-toa-kaoru.md).
