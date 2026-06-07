# Ren'Py plugins & community modules — research for Ryoko Owari Nights

**Engine:** Ren'Py 8.5.3 · **Date:** 2026-06-03  
**Scope:** Research + selective installs (2026-06-03). Curated from [awesome-renpy](https://github.com/methanoliver/awesome-renpy), Ren'Py docs, itch.io, and GitHub.

### Installed in this repo

| # | Plugin | Location | Docs |
|---|--------|----------|------|
| 1 | RenPy Auto Highlight | `game/00auto-highlight.rpy`; wired in `game/images/characters.rpy` | [SoDaRa/Auto-Highlight](https://github.com/SoDaRa/Auto-Highlight) |
| 2 | setup-renpy CI | `.github/workflows/renpy-lint.yml` | [docs/ci.md](ci.md) |
| 4 | Lip Sync (scaffold) | `game/lip-sync-plugin/` | [docs/lip-sync-setup.md](lip-sync-setup.md) |
| 6 | ActionEditor 3 (dev) | `tools/ActionEditor3/` | [docs/actioneditor-dev.md](actioneditor-dev.md) |

---

## Project snapshot (what you already have)

| Area | Status |
|------|--------|
| **Voiced dialogue** | `config.has_voice = True`; ~287 manifest lines; `voice "audio/voice/…"` per line; ElevenLabs pipeline in `scripts/` |
| **Sprites** | `layeredimage` for Toa/Kaoru + Auto Highlight (`sprite_highlight`); expression only — no mouth layers |
| **CG gallery** | Custom `game/gallery.rpy` — unlock via `renpy.seen_image()`, grouped grid, full-screen viewer, music-montage replay slots |
| **Cinematics** | OP/ED + image songs with Ken Burns, vignette, color grade (`transforms_op_ed.rpy`, `opening.rpy`, `ed_sequence.rpy`, `*_image_song.rpy`) |
| **Branch stats** | Custom flags in `stats.rpy` (insight, honor, route axes) — not a packaged framework |
| **Screenshot QA** | Ren'Py built-in test framework (`test_screenshot*.rpy`, `test_all_turns.rpy`, review manifest) |
| **Android / CI** | `.github/workflows/renpy-lint.yml` (Ren'Py 8.5.3 lint on push/PR); see [docs/ci.md](ci.md) |
| **Libraries folder** | `game/libs/` empty; no `python-packages/` |

**Implication:** Recommendations below favor *polish on top of existing systems*, not wholesale replacements (especially the gallery).

---

## Top recommendations (ranked)

### 1. RenPy Auto Highlight

| | |
|---|---|
| **URL** | https://github.com/SoDaRa/Auto-Highlight · https://wattson.itch.io/renpy-auto-highlight |
| **What it does** | Dims/zooms non-speaking sprites automatically via a Character callback — no per-line ATL |
| **Install** | Copy `game/00auto-highlight.rpy` into `game/` |
| **License** | MIT |
| **Maintenance** | Active (GitHub push Aug 2025); widely used on Lemma Soft |
| **Why for Ryoko Owari** | Otome scenes with Toa + Kaoru on screen benefit immediately; your `layeredimage` defs only need `at sprite_highlight('…')` and `cb_name` on Character defs |

### 2. GitHub Actions — `setup-renpy` + Ren'Py CLI lint/test

| | |
|---|---|
| **URL** | https://github.com/remarkablegames/setup-renpy · [blog post](https://remarkablegames.org/posts/setup-renpy-cli-github-actions/) |
| **What it does** | Downloads Ren'Py 8.5.x in CI; runs `renpy-cli game lint` and screenshot test suites headless |
| **Install** | Add `.github/workflows/renpy.yml` (no game files copied) |
| **License** | MIT (action repo) |
| **Maintenance** | Active; supports `cli-version: 8.5.3` |
| **Why for Ryoko Owari** | You already invest heavily in screenshot regression (`test_all_turns`, review manifest) — CI catches script/image breakage on every push without manual `_run_screenshot_review.bat` |

**Example workflow snippet:**

```yaml
- uses: actions/checkout@v4
- uses: remarkablegames/setup-renpy@v1
  with:
    cli-version: "8.5.3"
- run: renpy-cli game lint
- run: renpy-cli game test screenshot_capture --overwrite-screenshots
  env:
    SDL_AUDIODRIVER: dummy
    SDL_VIDEODRIVER: dummy
```

Prefer this over older [renpy-lint-action](https://github.com/ProjectAliceDev/renpy-lint-action) (defaults to ancient SDK versions).

### 3. Achievements for Ren'Py (Feniks / shawna-p)

| | |
|---|---|
| **URL** | https://github.com/shawna-p/RenPy-Achievements · https://feniksdev.itch.io/achievements-for-renpy |
| **What it does** | Declarative achievement class, popups, progress bars, in-game gallery; wraps Ren'Py + Steam achievement backends |
| **Install** | Copy `achievement_backend.rpy` + `achievements.rpy` into `game/` |
| **License** | Check repo (Feniks releases are typically MIT-style; verify before ship) |
| **Maintenance** | Tested through Ren'Py 8.4; Feniks actively maintains itch releases |
| **Why for Ryoko Owari** | Natural hooks: canon ending, Case 1/2 romance CGs, bad ends, gallery 100%, image-song unlocks — otome replay value without rewriting your custom CG gallery |

### 4. RenPy Lip Sync Plugin (+ Rhubarb)

| | |
|---|---|
| **URL** | https://github.com/Wendy-Nam/RenPy-Lipsync-Plugin · https://seo-a-nam.itch.io/lipsync-plugin-for-renpy |
| **What it does** | Batch-generates mouth-shape timing from voice files via [Rhubarb Lip Sync](https://github.com/DanielSWolf/rhubarb-lip-sync); async playback with skip-safe termination |
| **Install** | Copy `lip-sync-plugin/` to project root; add Rhubarb executable; run `generate_lipsync_data.py`; extend `layeredimage` with mouth attribute group |
| **License** | MIT (plugin + Rhubarb) |
| **Maintenance** | Moderate (2025 itch/GitHub updates) |
| **Why for Ryoko Owari** | Highest immersion lift for a fully voiced otome — **but** requires new mouth sprite sheets per expression and prefers `.wav`/`.ogg` (you ship `.mp3` today). Plan as an art + audio pipeline milestone, not a drop-in |

### 5. Kinetic Text Tags

| | |
|---|---|
| **URL** | https://github.com/SoDaRa/Kinetic-Text-Tags · https://wattson.itch.io/kinetic-text-tags |
| **What it does** | Custom text tags: shake, wave, scatter, gradient, mouse-reactive text for emotional dialogue |
| **Install** | Copy `game/kinetic_text_tags.rpy` (+ optional `gradient_tags.rpy`) into `game/` |
| **License** | MIT |
| **Maintenance** | Active; author notes some effects overlap Ren'Py 8 `{bt}`/`{fi}` ATL text tags |
| **Why for Ryoko Owari** | `{sc}…{/sc}` scared text, trembling confession lines, rain-scene emphasis — minimal script changes, strong otome mood |

### 6. ActionEditor 3 *(dev-only, strip before release)*

| | |
|---|---|
| **URL** | https://github.com/kyouryuukunn/renpy-ActionEditor3 |
| **What it does** | In-engine director tool: camera moves, transforms, timing preview; exports ATL/script |
| **Install** | Copy ActionEditor package into `game/` during development |
| **License** | Check repo README (typically permissive for dev use) |
| **Maintenance** | Active (~184★; widely referenced on Lemma Soft) |
| **Why for Ryoko Owari** | Speeds tuning OP/ED/image-song montages you currently hand-code in `transforms_op_ed.rpy` — keep out of release builds |

### 7. Caption Tool for Ren'Py (npckc)

| | |
|---|---|
| **URL** | https://npckc.itch.io/caption-tool-for-renpy |
| **What it does** | Image + music/SFX captions for accessibility; first-run prompt; links to Ren'Py accessibility menu |
| **Install** | Copy `captiontool.rpy` into `game/`; add Preferences button |
| **License** | MIT |
| **Maintenance** | Updated for Ren'Py 8.3; should work on 8.5 |
| **Why for Ryoko Owari** | Many CGs and cinematic montages with no dialogue — captions help low-vision players and self-voicing mode |

### 8. Encyclopaedia Framework

| | |
|---|---|
| **URL** | https://github.com/jsfehler/renpy-encyclopaedia · https://renpy-encyclopaedia.readthedocs.io/ |
| **What it does** | Unlockable codex/glossary with sort, filter, sub-pages, persistent unlocks |
| **Install** | `pip install --no-compile --target game renpy-encyclopaedia` **or** copy release folder into `game/` |
| **License** | MIT |
| **Maintenance** | v3.6.0 (Dec 2024); CI on GitHub; Ren'Py 8.1+ |
| **Why for Ryoko Owari** | L5R setting (Clan terms, Ryoko Owari locations, NPC dossiers) fits otome “Extras → Codex” without building screens from scratch |

### 9. renpy-graphviz *(workflow tool, not in-game)*

| | |
|---|---|
| **URL** | https://github.com/EwenQuim/renpy-graphviz · https://ewenquim.github.io/renpy-graphviz/ |
| **What it does** | Flowchart of labels/jumps/menus from `.rpy` files |
| **Install** | Standalone Python tool / online version — not copied into `game/` |
| **License** | MIT |
| **Maintenance** | Active |
| **Why for Ryoko Owari** | Complements your manual `docs/prologue-choice-tree.svg` and `screenshot-turn-map.json` — auto-regenerate branch maps as Case 3+ grows |

### 10. Multi-Touch Zoom Gallery *(conditional — paid)*

| | |
|---|---|
| **URL** | https://feniksdev.itch.io/multi-touch-zoom-gallery-for-renpy ($15) |
| **What it does** | Pinch-zoom / rotate CG viewer; `ZoomGallery` API mirrors built-in `Gallery` |
| **Install** | Copy `multi_touch/` into `game/` |
| **License** | Paid asset (check itch license terms) |
| **Maintenance** | Feniks; Ren'Py 8.x tested |
| **Why for Ryoko Owari** | **Only if** you ship Android/touch — lets players inspect detailed romance CGs. Your custom gallery works well on desktop; migration cost is non-trivial |

---

## Built-in Ren'Py 8.5 features worth using (not third-party)

These are engine-native — listed because teams often duplicate them with plugins:

| Feature | Doc | Fit |
|---------|-----|-----|
| **`config.auto_voice`** | [Voice](https://www.renpy.org/doc/html/voice.html) | Auto-play `audio/voice/{id}.ogg` from dialogue identifiers — could reduce manual `voice` statements once filenames stabilize |
| **`voice_tag` / `SetVoiceMute`** | [Voice](https://www.renpy.org/doc/html/voice.html) | Per-character mute in Preferences (you partially use this for narrator) |
| **Built-in `achievement` module** | [Achievement](https://www.renpy.org/doc/html/achievement.html) | Steam/mobile backends — Feniks system wraps this with nicer UI |
| **Built-in `Gallery` class** | [Gallery](https://www.renpy.org/doc/html/gallery.html) | You already exceed this with custom grouping + music replay |
| **Ren'Py test / screenshot API** | [Testcases](https://www.renpy.org/doc/html/testcases.html) | Already in use — pair with CI (#2) |
| **ATL `{bt}` / `{fi}` text tags** | Ren'Py 8+ | Overlaps part of Kinetic Text Tags — use built-in first for simple bounce/fade |

---

## Maybe later

| Module | URL | When it might matter |
|--------|-----|----------------------|
| **DynamicSpriteManager** | https://github.com/alexkrob/dynamicsprites/ | If expression/outfit combinatorics explode beyond hand-maintained `layeredimage` |
| **GalleryPlus** | https://github.com/cheonbyeol/RenPy-GalleryPlus | If you refactor to built-in `Gallery` and need paging/looping |
| **Zoom Viewport** | https://feniksdev.itch.io/zoom-viewport-for-renpy | Investigation “evidence board” UI (Case files, ledger zoom) |
| **renpy-build-action** | https://github.com/ProjectAliceDev/renpy-build-action | Release builds for Win/Mac/Linux/Android in CI (after lint CI works) |
| **VS Code Ren'Py extension** | https://github.com/LuqueDaniel/vscode-language-renpy | Syntax, launch, lint from editor — quality-of-life, not player-facing |
| **Dating Sim Engine** | https://github.com/renpy/dse | Only if schedule/planner UI becomes a core mechanic (you have lighter custom stats) |
| **Phone / messenger frameworks** | [awesome-renpy § Device imitation](https://github.com/methanoliver/awesome-renpy#device-imitation) | Only if future cases use in-fiction texting |
| **renpyDialogToAudio** | https://github.com/lugia19/renpyDialogToAudio | Redundant — you already have ElevenLabs + manifest scripts |

---

## Skip / anti-recommendations

| Item | Why skip |
|------|----------|
| **BobCGallery** | [Reported broken on Ren'Py 8.3.7+](https://bobcgames.itch.io/bobcgallery); your custom gallery is more capable |
| **renpy-gallery-inject** | For patching *other* games without source changes — not your situation |
| **RenPy AutoScriptPlugin (ChatGPT)** | Procedural AI dialogue — wrong for a authored otome |
| **Autofocus** | Same niche as Auto Highlight (#1) — pick one |
| **RPY-VNBE** | Overlaps achievements + text effects piecemeal; less maintained than Feniks/SoDaRa pieces |
| **Old `renpy-lint-action` defaults** | Ships ancient SDK unless carefully configured — use `setup-renpy` instead |
| **Starter templates** (renpy-awesome-template, etc.) | For greenfield projects — you are mid-production |
| **RPG / card / minigame kits** | No combat or arcade gameplay in scope |
| **renpy-achievement (popup-only)** | No backend; Feniks system is strictly better |
| **Kinetic Text `{bt}`/`{fi}` tags** | Redundant with Ren'Py 8 ATL tags unless you need shake/gradient/scatter |
| **Lip sync without mouth art** | Plugin is useless until layeredimage mouth groups exist per character |

---

## Suggested adoption order

1. **Auto Highlight** — low risk, immediate otome polish  
2. **CI lint + screenshot smoke test** — protect existing QA investment  
3. **Achievements** — when route/endings stabilize  
4. **Kinetic Text Tags** — sprinkle on key emotional beats  
5. **Caption Tool** — before any public demo  
6. **Encyclopaedia** — when codex content is written  
7. **Lip sync** — only after mouth sprites + audio format decision  
8. **ActionEditor** — optional dev aid for montage timing  

---

## Reference index

- Curated list: https://github.com/methanoliver/awesome-renpy  
- Ren'Py 8.5.3 release: https://github.com/renpy/renpy/releases/tag/8.5.3.26051504  
- Feniks tool collection: https://itch.io/c/3491447/my-renpy-tools  
- Ren'Py modules / python-packages: https://www.renpy.org/doc/html/python_modules.html  

---

*Generated as research deliverable — no packages were installed in the project.*
