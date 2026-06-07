# Voice performance manifest — review excerpt (2026-06-04)

**Source of truth:** `scripts/voice_performance_manifest.json` (871 entries).

**Delivery pass:** `python scripts/enrich_manifest_delivery_tags.py --retag` after expanding `weave_delivery_tags()` in `performance_tagging.py`. Backup: `scripts/versions/voice_performance_manifest-pre-delivery-tags-2026-06-03.json`. **No MP3 regeneration.**

| Metric | Value |
|--------|------:|
| Total entries | 871 |
| Lines with **2+ tags** | 870 (**99.9%**) |
| Lines with **reaction/pause** tag (`[pause]`, `[sighs]`, `[chuckles]`, …) | 398 (**45.7%**) |
| Lines with **mid-woven** tag (after lead block) | 272 (**31.2%**) |
| `tts_text` ≠ `game_text` | 870 |
| Sub-two-tag exception | `kaoru_139` (koan — intentional) |

Open the JSON for full review. Below: **8 before/after** pairs (pre-delivery backup → current), then **~40 woven samples** across scenes.

---

## Before / after — mid-line placement (8)

| id | Before `tts_text` | After `tts_text` |
|----|-------------------|------------------|
| `toa_003` | `[nervously] [short pause] I wasn't— That is, I apologize…` | `[nervously] I wasn't— [short pause] That is, I apologize…` |
| `toa_168` | `[defiant] [calm] Is this a date?` | `[defiant] [short pause] Is this a date?` |
| `toa_178` | `[crying] [nervously] …wards, and now you — almost sunk…` | `[crying] [nervously] …wards — [sighs] and now you — almost sunk a boat, [short pause] and it's so cold…` |
| `kaoru_177` | `[deadpan] [dismissive] If I ever find any dance crimes…` | `[deadpan] [chuckles] If I ever find any dance crimes…` |
| `kaoru_198` | `[pause] [whispers] ...No.` | `[pause] [exhales] ...No.` |
| `narrator_254` | `[dramatic] [pause] The shelf goes… snow. Toa has one breath…` | `[dramatic] [pause] The shelf goes… snow. [short pause] Toa has one breath…` |
| `narrator_178` | `[pause] [dramatic] A sniffle. A whimper. Tears…` | `[pause] A sniffle. [short pause] A whimper. Tears…` |
| `narrator_269` | `…on her elbow — escort, not comfort — and…` | `…on her elbow — escort, [short pause] not comfort — and…` |

---

## Woven samples — prologue

| id | `tts_text` (abridged) |
|----|------------------------|
| `toa_003` | `[nervously] I wasn't— [short pause] That is, I apologize for the disturbance, sochira-no-kata!` |
| `kaoru_014` | `[calm] [deadpan] Crane hair, [short pause] Unicorn permit dates. Wrong clan for this desk…` |
| `kaoru_056` | `[dismissive] [calm] Merit enough. Signature [short pause] ... pending.` |
| `kaoru_080` | `[whispers] [calm] Thirtieth. You'll knock on the right door [short pause] — I'll leave it unlatched.` |
| `narrator_002` | `[pause] [calm] Toa clutches her permit book… [short pause] turning in a corridor that refuses to end.` |
| `narrator_023` | `The fan closes on the final beat [pause] not a courtesy bow, but a held breath.` |

---

## Woven samples — Case 3.5 dinner (“date?”)

| id | `tts_text` (abridged) |
|----|------------------------|
| `toa_141` | `[cheerfully] [warmly] …really long time. [short pause] This is really lovely, Magistrate-sama.` |
| `toa_168` | `[defiant] [short pause] Is this a date?` |
| `kaoru_177` | `[deadpan] [chuckles] If I ever find any dance crimes I know who I need to bring with me.` |
| `kaoru_196` | `[dismissive] [calm] …patronage artist, [short pause] woman who trusted me in the bolt room — do not borrow festival vocabulary…` |
| `kaoru_198` | `[pause] [exhales] ...No.` |
| `kaoru_199` | `[whispers] It is the closest I come before I learn better.` |
| `narrator_144` | `[pause] [dramatic] Case Three's saw kerf… [short pause] but on a folded sheet of rice paper…` |
| `narrator_171` | `[pause] Crane training keeps her face pleasant. Inside, something unnamed aches…` |

---

## Woven samples — Case 4.5 Teardrop boat

| id | `tts_text` (abridged) |
|----|------------------------|
| `toa_176` | `[nervously] [cheerfully] Magistrate-sama!` |
| `toa_178` | `[crying] [nervously] …wards — [sighs] and now you — almost sunk a boat, [short pause] and it's so cold…` |
| `toa_187` | `[whispers] I was looking for a magistrate for my paperwork. But I found Kitsu Kaoru the man.` |
| `kaoru_212` | `[calm] [deadpan] …bad day, [sighs] and you, yoriki, get to deal with it.` |
| `narrator_175` | `[pause] [dramatic] Teardrop Island marina — … [short pause] but winter ribs and broken pilings…` |
| `narrator_178` | `[pause] A sniffle. [short pause] A whimper. Tears on wind-reddened cheeks…` |
| `narrator_180` | `[whispers] [pause] Rocking hull. Gunwales under his palms…` |

---

## Woven samples — Case 3/4 dock fight

| id | `tts_text` (abridged) |
|----|------------------------|
| `narrator_254` | `[dramatic] [pause] The shelf goes… snow. [short pause] Toa has one breath and two bad choices —` |
| `narrator_264` | `[dramatic] [pause] Three blades in rain — Kaoru's katana a clean arc…` |
| `narrator_266` | `[pause] She drops back — one step, not cowardice…` |
| `kaoru_315` | `[whispers] Breathe. Count. You are still mine to file.` |
| `toa_268` | `[whispers] You — you took the cut meant for me.` |

---

## Woven samples — punishment bridge + Case 1 companion

| id | `tts_text` (abridged) |
|----|------------------------|
| `toa_272` | `[defiant] [cheerfully] Then punish me, Magistrate-sama…` |
| `toa_273` | `[nervously] [short pause] I didn't— I meant you wouldn't—` |
| `toa_274` | `[whispers] [defiant] ...Wouldn't dare. Keep guessing.` |
| `kaoru_322` | `[dismissive] [calm] …Stupid, [short pause] To-chan. Mine.` |
| `kaoru_324` | `[whispers] [calm] You asked for closed screens twice in one night. You will have them.` |
| `narrator_269` | `[pause] [dramatic] Rain beads on the canal rope… escort, [short pause] not comfort — and the compound swallows them.` |
| `toa_068` | `[cheerfully] [short pause] Snacks after paperwork. [chuckles] That's still the order of operations.` |
| `toa_077` | `[cheerfully] [short pause] Fine. [chuckles] But I'm billing you for snacks.` |
| `kaoru_321` | `[warmly] [calm] I like you. So much so that I want to keep you around.` |

---

## Woven samples — Case 2 festival + rain gameover

| id | `tts_text` (abridged) |
|----|------------------------|
| `kaoru_269` | `[whispers] Let them watch the sky. I am watching you remember you are still alive after ash.` |
| `narrator_240` | `[pause] He kisses her on the bench — not performance, not ink —` |
| `kaoru_271` | `[dismissive] [calm] A festival kiss is paper confetti — pretty, [short pause] public, worthless in the morning docket.` |
| `kaoru_274` | `[whispers] [calm] …Guest room on the descent — one screen, [short pause] one lock, my corridor.` |
| `toa_243` | `[nervously] Don't make me used to mornings that don't hurt.` |
| `narrator_125` | `[dramatic] [pause] She kept her pride… [short pause] whole, and carried it out under her arm.` |
| `narrator_127` | `[pause] [dramatic] On stage she could make grief look graceful. Here there is no audience [long pause] — only the canal breathing back her own shaking.` |

---

## Changelog note

- **280** `tts_text` rows changed vs pre-delivery backup; **107** lines newly gained a reaction/pause tag; **268** newly gained a mid-woven tag.
- Helpers: `weave_delivery_tags()`, `is_reaction_pause_tag()`, scene buckets (`case35_dinner`, `dock_fight`, `teardrop_boat`, `punishment`, …).
- Approve tags here before `regenerate_voice_with_metadata.py --model eleven_v3`.
