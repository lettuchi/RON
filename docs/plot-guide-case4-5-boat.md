# Plot guide — Case 4.5 kobune (舟の帳)

**VN placement:** Post–Case 4 interlude (`case4_5_boat_interlude`) — after dock close, before Case Five stub.  
**Script:** `game/case4_5_boat.rpy`  
**Voice:** [toa-dialogue-style.md](toa-dialogue-style.md) (attachment, not love confession), [kaoru-dialogue-style.md](kaoru-dialogue-style.md) (commands, proprietary warmth).

---

## Thread metadata

| Field | Value |
|-------|--------|
| **Title** | Stress Reduction and Small Boats |
| **URL** | https://discord.com/channels/1057790980327231609/1451232878829768807 |
| **Channel** | `#teardrop-island` (parent `1141618624814129173`) |
| **Guild** | Ryoko Owari Nights `1057790980327231609` |
| **Date** | December 18–19, 2025 |
| **Participants** | **Kakita Toa** (Amanda) · **Kitsu Kaoru** (Jason) — duo-primary |
| **Transcript** | `docs/discord-threads-raw.md` § **Stress Reduction and Small Boats** — 48 IC posts (verbatim, 2026-06-03) |
| **VN adaptation** | Faithful spine: Teardrop Island **marina**, winter Scorpion crisis, **kobune**, shore find → throw **into hull** → fade-to-black on-boat intimacy → *I found you* / first **Kitsu Kaoru** → bath/kotatsu tease. **VN-only:** rigid-landing injury bad end when player fights the throw. |

---

## One-line premise

**IC:** Kaoru beaches a kobune at Teardrop Island, furious and freezing after winter Scorpion chaos; Toa finds him, breaks down over the city's suffering, and he demands she warm him — leading to a rocking-boat NSFW scene and post-coital *I found you* attachment beat.

**VN:** After Case Four, Toa investigates the island marina; she finds wet, furious Kaoru, complies or defies his warmth demand, is thrown **into the kobune**, then intimacy fades to black. Trust the hull or fight the throw → survive with bruises or **Game Over**.

---

## Eligibility — `case4_5_boat_interlude_eligible()`

- `all_romance_routes_complete()` (Cases 1–3 romance + Case 4 defend)
- `case4_closed`
- `case4_kaoru_defended`
- Not `case4_5_boat_interlude_seen`
- No prior bad ends: `case3_bad_end_injury`, `case4_toa_slain`, `case4_5_bad_end_boat_injury`

Case 3.5 date still runs **only** after Case 3 (`case3_post_case3_bridge`).

---

## Beat map (verbatim IC → VN)

| # | IC beat (Discord) | VN beat (`case4_5_boat.rpy`) |
|---|-------------------|------------------------------|
| 1 | Kaoru wet, kicking kobune ashore; Scorpion-winter frustration | Bridge: dock spill → island manifest; Teardrop marina establishing CG |
| 2 | Toa investigating; runs to soggy Magistrate + boat | Find Kaoru; *Can just ONE thing go right?!* |
| 3 | Concern; hot fingertips on cold cheeks | `case4_5_boat_duo_tense` |
| 4 | Hand up — stop talking; wringing; does not send her away | Narration + Toa sobs |
| 5 | *Bad day for you too?* — strips on shore | Tasteful skip; breakdown dialogue |
| 6 | Calamity / hunger / spooky / he could have died | Toa wail beat |
| 7 | *I'm fine. I'm just cold.* | Kaoru line |
| 8 | *why are you even in a boat?* / only way to Teardrop Island | Kaoru line |
| 9 | *yoriki, get to deal with it* — warm me up | `case4_5_boat_warm_menu` |
| 10 | Sleeve-hug warmth | `trust_warm` or `defy_cold` → hug |
| 11 | *Almost enough. But not.* → drags to boat | `case4_5_boat_drag_to_kobune` |
| 12 | Hopes for step-in; deck not tatami | Toa foreshadow |
| 13 | **Throw over side into boat** | `case4_5_boat_throw_splash` + `case4_5_boat_fall_menu` |
| 14 | Wet wood pain; disorienting rock | Survive path only |
| 15 | *You're on top today… work through your feelings* | Pre-fade Kaoru |
| 16–24 | Explicit on-boat (oral → mount → *good girl* / gunwales) | `case4_5_boat_lantern_implied` fade — no graphic prose |
| 25 | Hands on gunwales | Narration in fade beat |
| 26–28 | Climax; boat teeters | Implied |
| 29 | Cuddle; cold returns | Post-fade warmth |
| 30 | *I found you. Remember?* | Toa attachment line |
| 31 | First spoken **Kitsu Kaoru**; magistrate vs man | Toa line |
| 32 | *why more women can't be like you* | Kaoru |
| 33 | Bath + mikan + kotatsu | Compressed bridge |
| 34 | *bend you over the side of the bath* | Kaoru tease → Case 5 stub |

---

## VN beat map

| # | Beat | CG / label |
|---|------|------------|
| 1 | Office — island witness, no ledger | — |
| 2 | Teardrop marina winter, kobune | `case4_5_boat_canal_night` |
| 3 | Shore find — wet Kaoru, Toa runs in | `case4_5_boat_duo_tense` |
| 4 | Sob / strip / breakdown / yoriki demand | — |
| 5 | Menu: hug vs hold back | `case4_5_boat_warm_menu` |
| 6 | Drag → throw into hull | `case4_5_boat_throw_splash` |
| 7 | Fall menu (trust vs fight) | `case4_5_boat_fall_menu` |
| 8 | Fade intimacy on boat | `case4_5_boat_lantern_implied` |
| 9a | *I found you* / Kitsu Kaoru / bath tease | — |
| 9b | Bridge → Case 5 stub | `case4_5_boat_bridge` → `case5_stub_tease` |
| 10 | Bad end | `gameover_case4_5_boat` |

---

## Menus & flags

| Menu | Choice | Flag | Result |
|------|--------|------|--------|
| `case4_5_boat_warm_menu` | Step into him | `case4_5_boat_choice = trust_warm` | Hug → drag → throw |
| | Hold back | `defy_cold` | Verbal spar → hug anyway → throw |
| `case4_5_boat_fall_menu` | Go limp | `case4_5_boat_fall_choice = trust_fall` | Bruised knees; fade intimacy |
| | Fight the throw | `fight_fall` | `case4_5_bad_end_boat_injury` → Game Over |

---

## Bad end trigger

**Player choice:** *Fight the throw — land rigid on the thwart.* on `case4_5_boat_fall_menu` immediately after Kaoru throws her **into the kobune** (`case4_5_boat_throw_splash`).

**Flow:** `case4_5_boat_bad_end_warning` → `case4_5_bad_end_boat` → `gameover_case4_5_boat` → title.

**Title card:** Case Four Point Five — 「舟の果て」 — *The kobune deck took Kakita Toa.*

**IC note:** Discord throw is for warmth/sex; deck pain is real but not a branch. VN bad end is optional adaptation (fight vs limp), not verbatim IC.

---

## Key lines (VN uses)

| Speaker | Line |
|---------|------|
| Kaoru | *Can just ONE thing go right?!* |
| Kaoru | *yoriki, get to deal with it* |
| Kaoru | *Almost enough. But not.* / *Worse.* (re: tatami) |
| Kaoru | *You're on top today…* |
| Kaoru | *Good girl* / gunwales (fade narration) |
| Toa | *The deck of a boat was not a tatami mat.* |
| Toa | *I found you. Remember?* |
| Toa | *I found Kitsu Kaoru the man.* |
| Toa | *Bath. Mikan under the kotatsu.* |

---

## CG regen prompts (if art still shows canal skiff)

Use [cg-style-prompt-block.md](cg-style-prompt-block.md). Keep filenames; overwrite PNGs.

| Image file | Scene |
|------------|--------|
| `cg-case4_5-boat-canal-night.png` | Winter Teardrop Island marina: broken pilings, rubble, grey bay wind, small beached **kobune**, no magistrate skiff, no noble canal stone |
| `cg-case4_5-boat-duo-tense.png` | Shore: soaked Kaoru wringing robes, furious; Toa in dry black kosode approaching over wreckage; cold daylight |
| `cg-case4_5-boat-throw-splash.png` | Kaoru tossing Toa over **gunwale into kobune hull** (not into canal); boat rocking, wet deck |
| `cg-case4_5-boat-lantern-implied.png` | Kobune interior, low winter light, silhouettes, his hands on gunwales, implied closeness — no explicit anatomy |
| `cg-case4_5-bad-boat-injury.png` | Toa crumpled on thwart after rigid fall; marina winter; tragic, not gory |

---

## Playtest jump

Dev menu → **Case 4.5 — Teardrop kobune** (`case4_5_boat_interlude`).

Bad end only: Dev → Bad ends → **Case 4.5 — kobune injury game over**.

Full path: complete Case 4 with defend romance → `case4_post_case4_bridge`.

---

## Voice manifest

VO wired in `case4_5_boat.rpy` (2026-06-03): `toa_173`–`toa_191`, `kaoru_206`–`kaoru_224`, `narrator_174`–`narrator_182`. Run `sync_voice_performance_manifest.py` after script edits.
