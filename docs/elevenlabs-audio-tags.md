# ElevenLabs Eleven v3 — audio tag reference

**Model:** `eleven_v3` only (Voice Design Text to Preview, Text to Speech, Text to Dialogue, Eleven v3 Conversational agents). Bracket tags are **not** reliable on `eleven_multilingual_v2` / Turbo / Flash.

**Format:** Square brackets, natural-language instructions — e.g. `[laughs]`, `[whispers]`, `[strong French accent]`. Place at the point delivery should change (usually immediately before or after the affected words).

## Not a fixed enum

Official docs state repeatedly that audio tags are **natural-language instructions, not an enum parameter**. Lists below are **documented examples**, not a complete closed set. You can use contextually similar tags (e.g. `[nervously]`, `[frustrated sigh]`, `[leaves rustling]`). Effectiveness depends on voice training and tag/voice match.

- [Help: How do audio tags work with Eleven v3?](https://help.elevenlabs.io/hc/en-us/articles/35869142561297)
- [TTS best practices — Prompting Eleven v3](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices) (primary tag list + Enhance prompt)
- [Text to Dialogue — Emotional deliveries with audio tags](https://elevenlabs.io/docs/overview/capabilities/text-to-dialogue)
- [Expressive mode (agents)](https://elevenlabs.io/docs/eleven-agents/customization/voice/expressive-mode)
- [Blog: Character performance](https://elevenlabs.io/blog/eleven-v3-character-direction) · [Blog: Situational awareness](https://elevenlabs.io/blog/eleven-v3-situational-awareness)

**Case:** Tags are **case-insensitive** (`[HAPPY]` = `[happy]`).

**Scope (Enhance UI rules):** Tags must describe something **auditory** (voice delivery or hearable reaction). Do **not** use visual-only tags such as `[standing]`, `[grinning]`, `[pacing]`, or `[music]`.

**Agents:** With Eleven v3 Conversational, a tag typically affects roughly the **next 4–5 words**, then delivery returns to baseline.

**Pauses:** v3 does **not** use SSML `<break>`. Use tags like `[short pause]` / `[pause]`, ellipses `...`, dashes, or punctuation.

---

## Emotions & mood


| Tag |
| --- |



|                                 | Source                                         |
| ------------------------------- | ---------------------------------------------- |
| `[happy]`                       | Best practices (Enhance)                       |
| `[sad]`                         | Help, Text to Dialogue, Enhance                |
| `[excited]`                     | Help, Best practices, Expressive mode, Enhance |
| `[angry]`                       | Help (“What is Eleven v3?”), Enhance           |
| `[curious]`                     | Help, Best practices                           |
| `[crying]`                      | Help, Best practices                           |
| `[mischievously]`               | Help, Best practices                           |
| `[sarcastic]`                   | Best practices                                 |
| `[happily]`                     | Help (“What is Eleven v3?”)                    |
| `[calm]`                        | Kore.ai integration table (citing v3)          |
| `[dramatic]` / `[dramatically]` | Kore.ai table; Best practices examples         |
| `[eager]`                       | Kore.ai table                                  |
| `[annoyed]`                     | Enhance prompt                                 |
| `[appalled]`                    | Enhance prompt                                 |
| `[thoughtful]`                  | Enhance prompt                                 |
| `[surprised]`                   | Enhance prompt                                 |
| `[nervous]` / `[nervously]`     | Blog (situational)                             |
| `[frustrated]`                  | Blog (situational)                             |
| `[tired]`                       | Blog (situational)                             |
| `[elated]`                      | Text to Dialogue                               |
| `[indecisive]`                  | Text to Dialogue                               |
| `[quizzically]`                 | Text to Dialogue                               |
| `[delighted]`                   | Best practices examples                        |
| `[amazed]`                      | Best practices examples                        |
| `[impressed]`                   | Best practices examples                        |
| `[alarmed]`                     | Best practices examples                        |
| `[frustrated]`                  | Best practices examples                        |
| `[desperately]`                 | Best practices examples                        |
| `[panicking]`                   | Best practices examples                        |
| `[cautiously]`                  | Text to Dialogue; Best practices examples      |
| `[cheerfully]`                  | Text to Dialogue                               |
| `[warmly]`                      | Best practices examples; Kore.ai example       |
| `[sympathetic]`                 | Best practices examples                        |
| `[reassuring]`                  | Best practices examples                        |
| `[professional]`                | Best practices examples                        |
| `[dismissive]`                  | Best practices; character blog                 |
| `[cute]`                        | Best practices examples                        |
| `[sheepishly]`                  | Best practices examples                        |
| `[deadpan]`                     | Best practices examples                        |
| `[sternly]`                     | Enhance prompt; community v3                   |
| `[bitterly]`                    | Enhance prompt                                 |
| `[mockingly]`                   | Character blog; Enhance                        |
| `[menacingly]`                  | Text to Dialogue; situational blog             |
| `[pleading]`                    | Best practices examples                        |
| `[breathless]`                  | Best practices examples                        |
| `[resigned]`                    | Best practices examples                        |
| `[seductive]`                   | Best practices examples                        |
| `[teasing]`                     | Best practices examples                        |
| `[flirtatious]`                 | Best practices examples                        |
| `[trembling]`                   | Best practices examples                        |
| `[sobbing]`                     | Best practices examples                        |
| `[firmly]`                      | Enhance prompt                                 |
| `[scoffs]`                      | Enhance prompt                                 |
| `[coldly]`                      | Project regen (Kaoru flat warmth)              |
| `[bureaucratic]`                | Project regen (hall / cage VO)                 |
| `[satisfied]`                   | Project regen (curry beat)                     |
| `[tender]`                      | Project regen (intimate narrator)            |
| `[grim]`                        | Project regen (bad branch narrator)            |


---

## Delivery direction (volume, energy, manner)


| Tag                | Source                                                  |
| ------------------ | ------------------------------------------------------- |
| `[whispers]`       | Help, Best practices, Expressive mode                   |
| `[whisper]`        | Enhance prompt (singular)                               |
| `[whispering]`     | Text to Dialogue; Best practices (voice selection note) |
| `[shouts]`         | Help                                                    |
| `[shout]`          | Best practices (voice-related note)                     |
| `[shouting]`       | Blog (situational)                                      |
| `[quietly]`        | Blog (situational)                                      |
| `[loudly]`         | Blog (situational)                                      |
| `[slow]`           | Expressive mode                                         |
| `[slowly]`         | Kore.ai table                                           |
| `[rushed]`         | Kore.ai table; Blog (situational)                       |
| `[sarcastically]`  | Character blog                                          |
| `[matter-of-fact]` | Character blog                                          |
| `[whiny]`          | Character blog                                          |
| `[excitedly]`      | Best practices examples                                 |
| `[curiously]`      | Best practices examples                                 |
| `[questioning]`    | Best practices examples                                 |
| `[dramatic]`       | Character blog; examples                                |
| `[sternly]`        | Enhance prompt                                          |
| `[firmly]`         | Enhance prompt                                          |
| `[mockingly]`      | Character blog                                          |
| `[menacingly]`     | Text to Dialogue                                        |
| `[bitterly]`       | Enhance prompt                                          |
| `[pleading]`       | Best practices examples                               |
| `[breathless]`     | Best practices examples                               |
| `[resigned]`       | Best practices examples                               |
| `[seductive]`      | Best practices examples                               |
| `[teasing]`        | Best practices examples                               |
| `[flirtatious]`    | Best practices examples                               |
| `[trembling]`      | Best practices examples                               |


---

## Laughter & vocal reactions


| Tag                          | Source                                                  |
| ---------------------------- | ------------------------------------------------------- |
| `[laughs]`                   | Help, Best practices, Expressive mode, Text to Dialogue |
| `[laughing]`                 | Text to Dialogue; Enhance; Best practices examples      |
| `[laughs harder]`            | Best practices (voice-related)                          |
| `[starts laughing]`          | Best practices (voice-related)                          |
| `[wheezing]`                 | Best practices (voice-related)                          |
| `[laughing hysterically]`    | Best practices examples                                 |
| `[chuckles]`                 | Enhance prompt                                          |
| `[giggles]` / `[giggling]`   | Best practices; Text to Dialogue                        |
| `[snorts]`                   | Best practices (voice-related)                          |
| `[with genuine belly laugh]` | Best practices examples                                 |
| `[stifling laughter]`        | Best practices examples                                 |
| `[cracking up]`              | Best practices examples                                 |


---

## Sighs, breaths, throat & mouth sounds


| Tag                 | Source                                               |
| ------------------- | ---------------------------------------------------- |
| `[sighs]`           | Help, Best practices, Expressive mode, Enhance       |
| `[sigh]`            | Text to Dialogue; Best practices punctuation example |
| `[exhales]`         | Best practices (voice-related)                       |
| `[exhales sharply]` | Enhance prompt                                       |
| `[inhales deeply]`  | Enhance prompt                                       |
| `[frustrated sigh]` | Best practices examples                              |
| `[clears throat]`   | Help, Enhance                                        |
| `[gulps]`           | Best practices (sound effects); Kore.ai; Blog        |
| `[swallows]`        | Best practices (sound effects)                       |
| `[happy gasp]`      | Best practices examples                              |
| `[gasp]`            | Blog (situational) — also implied by “gasp” family   |
| `[groaning]`        | Text to Dialogue                                     |
| `[scoffs]`          | Enhance prompt                                       |
| `[sobbing]`         | Best practices examples                              |


---

## Pauses, pacing & timing


| Tag                                      | Source                                            |
| ---------------------------------------- | ------------------------------------------------- |
| `[short pause]`                          | Enhance prompt                                    |
| `[long pause]`                           | Enhance prompt                                    |
| `[pause]`                                | Best practices dialogue examples; Kore.ai example |
| `[pauses]`                               | Best practices examples; Blog (situational)       |
| `[pause, then normally]`                 | Best practices examples                           |
| `[stammers]`                             | Blog (situational)                                |
| `[singing quickly]`                      | Best practices examples (compound delivery)       |
| `[muttering]`                            | Enhance example                                   |
| `[starting to speak]`                    | Best practices examples                           |
| `[jumping in]`                           | Text to Dialogue; Best practices examples         |
| `[overlapping]`                          | Best practices examples                           |
| `[interrupting, then stopping abruptly]` | Best practices examples                           |


Ellipses `...` and capitalization are also documented pacing/emphasis tools (not bracket tags).

---

## Character, accent & performance style


| Tag                                                             | Source                                                                                |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `[strong X accent]`                                             | Best practices — replace X (e.g. `[strong French accent]`, `[strong Russian accent]`) |
| `[French accent]` / `[American accent]` / `[Australian accent]` | Character blog                                                                        |
| `[British accent]` / `[Southern US accent]`                     | Character blog; Kore.ai table                                                         |
| `[pirate voice]`                                                | Character blog                                                                        |
| `[evil scientist voice]`                                        | Character blog                                                                        |
| `[childlike tone]`                                              | Character blog                                                                        |
| `[robotic voice]`                                               | Best practices examples                                                               |
| `[binary beeping]`                                              | Best practices examples                                                               |
| `[fantasy narrator]`                                            | Character blog                                                                        |
| `[sci-fi AI voice]`                                             | Character blog                                                                        |
| `[classic film noir]`                                           | Character blog                                                                        |
| `[sings]` / `[singing]`                                         | Best practices (unique); Enhance example                                              |
| `[woo]`                                                         | Best practices (experimental)                                                         |
| `[fart]`                                                        | Best practices (experimental)                                                         |


---

## Sound effects & environmental audio


| Tag                  | Source                           |
| -------------------- | -------------------------------- |
| `[gunshot]`          | Best practices                   |
| `[applause]`         | Best practices; Text to Dialogue |
| `[clapping]`         | Best practices                   |
| `[explosion]`        | Best practices                   |
| `[leaves rustling]`  | Text to Dialogue                 |
| `[gentle footsteps]` | Text to Dialogue                 |


Blog and community examples also mention tags like `[door creaks]` and `[bird chirping]` as **illustrative** environmental cues; treat as open-ended like other audio-event tags.

---

## Scene / overall direction (non-verbal context)

Documented as **overall direction** tags — scene or performance mode, not a single word emotion:


| Tag                 | Source           |
| ------------------- | ---------------- |
| `[football]`        | Text to Dialogue |
| `[wrestling match]` | Text to Dialogue |
| `[auctioneer]`      | Text to Dialogue |


---

## Tags explicitly discouraged (Enhance / UI)

Not valid audio tags for v3 Enhance:

- `[standing]`, `[grinning]`, `[pacing]`, `[music]`

Enhance also says: do not use tags for non-voice elements when the goal is dialogue enhancement only.

---

## Quick matrix (help center + best practices “voice-related”)


| Category  | Examples                                                                             |
| --------- | ------------------------------------------------------------------------------------ |
| Emotions  | `[curious]` `[crying]` `[mischievously]` `[sad]` `[angry]` `[excited]` `[sarcastic]` |
| Delivery  | `[whispers]` `[shouts]` `[shout]` `[slow]` `[rushed]` `[slowly]`                     |
| Reactions | `[laughs]` `[clears throat]` `[sighs]` `[exhales]` `[snorts]` `[gulps]`              |
| SFX       | `[gunshot]` `[applause]` `[clapping]` `[explosion]` `[swallows]`                     |
| Special   | `[strong X accent]` `[sings]` `[woo]` `[fart]`                                       |


---

## Ryoko Owari pipeline note

Ship new and re-tagged lines with **`eleven_v3`** (`ELEVENLABS_MODEL_ID=eleven_v3` or `scripts/regenerate_voice_with_metadata.py --model eleven_v3`). Legacy batches may still list `eleven_multilingual_v2` in `voice_performance_manifest.json` until regen; bracket tags are unreliable on v2. See [voice-design-prompts.md](voice-design-prompts.md) § Expressive tags for Voice Design (v3 preview) vs shipped regen (v2).

**Manifest workflow:** `game_text` mirrors Ren'Py display lines (plain prose in `game/*.rpy`). **`tts_text` lives only** in `scripts/voice_performance_manifest.json`. After script rewrites, merge sidecars with `scripts/merge_script_rewrite_sidecars.py`, then audit tags with `scripts/audit_tts_tags.py` and enrich with `scripts/apply_tts_tag_enrichment.py`.

---

## Ryoko Owari project palette (Eleven v3)

Curated tags used in regen and `scripts/performance_tagging.py` heuristics. Combine **1–2 lead tags** + optional **mid-line** `[short pause]` / `[long pause]` / reaction tags. Not every line needs every bucket — pick the beat.

### Kaoru (Kitsu Kaoru)

| Energy | Tags |
| --- | --- |
| Cold / deadpan | `[deadpan]`, `[matter-of-fact]`, `[calm]`, `[dismissive]`, `[coldly]` |
| Charm / proprietary | `[warmly]`, `[teasing]`, `[amused]`, `[satisfied]` |
| Cruel / hall power | `[dismissive]`, `[sternly]`, `[firmly]`, `[menacingly]`, `[bureaucratic]` |
| Intimate / low register | `[whispers]`, `[calm]`, `[seductive]` (sparingly) |
| Smirk / dry amusement | `[deadpan]`, `[chuckles]`, `[mockingly]`, `[teasing]` |

**Example lead pairs:** `[deadpan] [dismissive]`, `[calm] [deadpan]`, `[dismissive] [calm]`, `[whispers] [calm]`, `[warmly] [teasing]`.

### Toa (Kakita Toa)

| Energy | Tags |
| --- | --- |
| Cheerful / proud | `[cheerfully]`, `[excited]`, `[delighted]`, `[warmly]` |
| Flustered / formal fraying | `[nervously]`, `[short pause]`, `[sheepishly]` |
| Earnest / bright deferential | `[cheerfully]`, `[nervously]` (magistrate-facing) |
| Defiant / spine | `[defiant]`, `[firmly]`, `[calm]` |
| Soft / intimate | `[whispers]`, `[warmly]`, `[tender]` |
| Determined | `[defiant]`, `[cheerfully]`, `[excited]` |

**Example lead pairs:** `[cheerfully] [nervously]`, `[nervously] [short pause]`, `[defiant] [cheerfully]`, `[whispers] [warmly]`.

### Narrator

| Energy | Tags |
| --- | --- |
| Dramatic / investigation | `[dramatic]`, `[pause]`, `[alarmed]` |
| Tender / romance | `[tender]`, `[warmly]`, `[sympathetic]`, `[whispers]` |
| Grim / bad branch | `[grim]`, `[pause]`, `[resigned]` |
| Sensory / place | `[pause]`, `[dramatic]`, `[cautiously]` |
| Pause rhythm | `[pause]`, `[short pause]`, `[long pause]` mid-clause |

**Example lead pairs:** `[pause] [dramatic]`, `[dramatic] [pause]`, `[tender] [pause]`, `[grim] [pause]`.

### Bad ends (narrator + VO)

| Energy | Tags |
| --- | --- |
| Menacing | `[menacingly]`, `[dramatic]`, `[pause]` |
| Pleading (Toa) | `[pleading]`, `[nervously]`, `[breathless]` |
| Breathless / panic | `[breathless]`, `[panicking]`, `[gulps]` |
| Resigned close | `[resigned]`, `[dramatic]`, `[long pause]` |

Rain gameover and refusal arcs lean on `[pause]` + `[dramatic]`; cage / discharge branches use `[grim]` and `[bureaucratic]` on Kaoru.

---

## Authoring rules (this project)

1. **Lead with 1–2 emotion tags** at the start of `tts_text` (e.g. `[deadpan] [dismissive]`). On emotional peaks use **2–4** tags total (lead + mid-line reaction/pause). Neutral exposition: **1–2** tags only.
2. **Mid-line beats:** insert `[short pause]` or `[long pause]` where the actor would breathe or let a clause land — after names, before reversals, between list items (Case Five recitation, hall procedure).
3. **Never tag visual-only actions** (`[standing]`, `[grinning]`, `[pacing]`). Tags must be **auditory** (delivery, sigh, laugh, pause).
4. **`game_text` stays plain** in manifests and `game/*.rpy`. **Tags only in `tts_text`** in `voice_performance_manifest.json`. Spoken words in `tts_text` must match `game_text` (tags are extra bracket tokens only).
5. **Script rewrites:** conversational copy lands via `docs/script-rewrite-2026-06-04/case*-updates.json` and `scripts/merge_script_rewrite_sidecars.py`. After merge, run `scripts/audit_tts_tags.py` and `scripts/apply_tts_tag_enrichment.py` (or commit a `tts-tag-enrichment.json` sidecar and apply with `--from-sidecar`).
6. **Do not over-tag:** if `[calm] [deadpan]` already fits a cold Kaoru line, add `[short pause]` only where the line has a natural beat — not on every sentence.

**Audit / enrich commands:**

```bash
python scripts/audit_tts_tags.py --ids
python scripts/apply_tts_tag_enrichment.py --dry-run
python scripts/apply_tts_tag_enrichment.py
```