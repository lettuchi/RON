# Voice design prompts — Kakita Toa & Kitsu Kaoru

**Formatted for [ElevenLabs Voice Design](https://elevenlabs.io/docs/eleven-creative/voices/voice-design#prompting-guide)** per the official prompting guide (structured prompt + Text to Preview + Guidance Scale).

Project: *Ryoko Owari Nights* (L5R otome VN, English dialogue with occasional Japanese honorifics).  
See [voice-setup.md](voice-setup.md) and [voice-metadata.md](voice-metadata.md) for TTS integration and voice IDs.

---

## Prompting rules (ElevenLabs)

Use this structure for every Voice Design prompt:

```
Native <Language>. <Gender>, <Age range>. <Quality level>.
Persona: <2–5 words>. Emotion: <2–3 adjectives>.
<1–2 sentences about timbre, pacing, delivery>
```

| Do | Don't |
|----|-------|
| Specify language and regional variant in the **first sentence** | Use "accent" when you mean **intonation** or emphasis |
| Use quality descriptors (`Good quality`, `Excellent quality`, etc.) | Use FX words (`reverb`, `echo`, `phone`, `tape`) |
| Match **Text to Preview** to the voice's personality and pace | Contradict the prompt with mismatched preview text (e.g. angry preview for a calm voice) |
| Prefer **longer preview text** (full sentences or short paragraph) for stable auditions | Rely on one-word previews for subtle tone tests |

**Guidance Scale:** Higher = stricter prompt adherence (accent/tone accuracy); lower = more creative, sometimes smoother audio. Suggested ranges below are starting points — adjust if output is too flat or too niche.

---

## Kakita Toa

### Voice Design prompt (copy-paste)

```
Native English, neutral international (no strong regional dialect). Female, young adult in her mid-20s. Good quality. Persona: Crane clan dancer. Emotion: bright, deferential, playful. Medium-high alto with warm, forward timbre and musical lift on questions; trained diction without shrill or childish pitch. Moderately quick when excited, slightly softer when pleading; honors "Magistrate-sama" with genuine respect and affection, never sarcasm.
```

### One-liner alternate (simple / neutral voices)

Young adult woman, bright warm alto, eager and deferential, playful Crane dancer energy — not childish.

### Text to Preview (primary audition)

Use this in the **Text to preview** box when generating. Longer text stabilizes tone and pacing.

```
I was sure the clerk said third hall, fourth door on the left. Or was it the right? I apologize for the disturbance, sochira-no-kata! Kakita Toa, dancer of the Kakita family — new to Ryoko Owari. Yes, Magistrate-sama. I promise I'm only lost geographically, not legally. May I present my renewal request?
```

### Text to Preview (intimate / flustered range)

```
Magistrate-sama — his throat bruises like fingers, not water. I'll manage, Magistrate-sama. I know the difference. Th-thank you, Magistrate-sama.
```

### Guidance Scale

**30–35%** — balance prompt accuracy with expressive VN delivery.

### Pitfalls to avoid

- Child, teen, or loli vocal quality; soprano chipmunk or mature contralto
- Monotone, bored, sullen, or whisper-only baseline
- Aggressive, sarcastic, or dominatrix delivery (Kaoru's lane)
- Thick regional dialects (Southern, Cockney, caricature accents)
- Constant vocal fry, ASMR breathiness, or shrill anime squeal on every line
- Male or androgynous timbre; robotic news-anchor flatness

### After save — TTS settings (ElevenLabs)

| Setting | Suggestion |
|--------|------------|
| **Model** | `eleven_multilingual_v2` (mixed EN + honorifics) |
| **Stability** | ~50–65% (allow expression; avoid mush) |
| **Similarity / clarity** | Medium-high once cloned |
| **Style / exaggeration** | Slightly elevated for dance/flirt beats; pull back for investigation |

**Library references:** Carla (legacy), Jessica alternate — see [voice-setup.md](voice-setup.md).

---

## Kitsu Kaoru

### Voice Design prompt (copy-paste)

```
Native English, neutral international with subtle mid-Atlantic polish (no cowboy, surfer, or heavy villain British). Male, adult in his mid-30s. Excellent quality. Persona: Emerald Magistrate. Emotion: controlled, dominant, amused. Low baritone with rich chest resonance and crisp consonants; smirk audible in delivery, short satisfied laughter never bubbly. Deliberate measured pacing, rarely raised volume; dangerous warmth underneath — possessive and proprietary in intimacy, magistrate-cold in investigation, composure always intact.
```

### One-liner alternate (simple / neutral voices)

Adult man, low controlled baritone, dangerous charm — dominant magistrate, warm only when he chooses.

### Text to Preview (primary audition)

```
Done complaining? Wrong door. Again. Emerald Magistrate Kitsu Kaoru. You will use my title if you wish to leave with a seal. Plain speech. You waste less of my evening than most. Flexibility. Good. You'll need it — this city bends people until they snap or shine.
```

### Text to Preview (intimate / possessive range)

```
Enter. Since you can follow instructions when motivated. That is why I'm keeping you, To-chan. I am drafting sponsorship, not a courtesan's contract. I know what I am paying for.
```

### Guidance Scale

**35–40%** — accent and tone accuracy matter for consistent magistrate presence.

### Pitfalls to avoid

- Young, soft, or softboy timbre; high-pitched, nasal, or wheezy delivery
- Constant shouting, snarling, or moustache-twirling villain
- Friendly neighbor or customer-service warmth as default
- Stiff robotic bureaucracy with zero charisma
- Drunk-slurred or overly breathy baseline (reserve for specific lines)
- Female or ambiguous gender presentation; comic relief goofiness
- Thick regional accents that read modern-Western out of setting

### After save — TTS settings (ElevenLabs)

| Setting | Suggestion |
|--------|------------|
| **Model** | `eleven_multilingual_v2` (mixed EN + honorifics) |
| **Stability** | ~65–80% (consistent magistrate; higher than Toa) |
| **Similarity / clarity** | High — every clipped line must read in VN |
| **Style / exaggeration** | Low–medium default; raise only for intimate or triumphant beats |

**Library references:** Jax Meridian (legacy), Josh or Arnold alternates — see [voice-setup.md](voice-setup.md).

---

## Alternate prompts (under 1000 characters)

Second Voice Design wording for the same canon — use when the primary prompt above yields voices that are close but not quite right. Same structured format; different emphasis (court-trained lyric vs. musical deferential; proprietary heat vs. smirk-and-baritone). Character counts verified for ElevenLabs copy-paste limits.

### Kakita Toa — alternate Voice Design prompt

**Character count: 448**

```
Native English, international neutral delivery (no caricature regional drawl). Female, young adult, mid-twenties. Very good quality. Persona: Kakita court dancer. Emotion: radiant, respectful, spirited. Warm medium alto with clear Crane-trained enunciation; lyric lift without squeal, pitch firmly adult never juvenile. Flows brisk when flustered, gentles on apology; "Magistrate-sama" spoken with sincere devotion and light sparkle, never mockery.
```

### Kitsu Kaoru — alternate Voice Design prompt

**Character count: 475**

```
Native English, polished neutral intonation (not cowboy, surfer, or sneering villain British). Male, adult, mid-thirties. Very good quality. Persona: Emerald Magistrate lord. Emotion: restrained, authoritative, sardonic. Deep baritone, velvety chest tone, knife-clean consonants; amusement lives in timing, never goofy laugh. Unhurried cadence, volume stays composed; intimacy blooms as proprietary heat, duty stays glacial — warmth always feels chosen and slightly perilous.
```

Use the same **Text to Preview** and **Guidance Scale** ranges as the primary prompts in each character section above.

---

## Workflow

1. **Voices → My Voices → Add a new voice → Voice Design** in ElevenLabs (or API).
2. Paste the **Voice Design prompt**, set **Guidance Scale**, paste **Text to Preview**, generate (three options per run).
3. Save the best voice; paste **voice IDs** into `.env` (`ELEVENLABS_VOICE_V2_TOA`, `ELEVENLABS_VOICE_V2_KAORU`).
4. Batch TTS: `scripts/regenerate_voice_with_metadata.py --sample 5` using game lines from the manifest.
5. Canon tone reference: [discord-threads-raw.md](discord-threads-raw.md) (Magistrate office thread), [story-so-far.md](story-so-far.md).

**Do not commit** API keys or `.env`.

---

## Expressive tags ([laughs], etc.)

**Voice Design (UI):** With **Eleven v3** Voice Design, put bracket **audio tags** in **Text to Preview** — e.g. `[laughs]`, `[giggling]`, `[whispers]`, `[sighs]`, `[excited]`. Tags are natural-language cues in square brackets, not SSML. See [Eleven v3 audio tags](https://help.elevenlabs.io/hc/en-us/articles/35869142561297) and [TTS best practices (v3)](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices). You can also describe delivery in the **Voice Design prompt** (e.g. “short satisfied laughter never bubbly”) without brackets.

**Saved-voice TTS (this project):** Batch scripts default to **`eleven_multilingual_v2`** (`ELEVENLABS_MODEL_ID` in `scripts/.env`). **Bracket audio tags only work reliably on `eleven_v3`**, not on multilingual v2 / Turbo / Flash. The regen script sends manifest `text` unchanged (no stripping); on v2, `[laughs]` is often read aloud or ignored.

| Where | Model | Tags |
|-------|--------|------|
| Voice Design → Text to Preview | Eleven v3 | Supported |
| `regenerate_voice_with_metadata.py` / `generate_voice.py` | Default `eleven_multilingual_v2` | Not supported — use v3 only if you accept tradeoffs (latency, consistency, EN/JP honorifics) |
| Text to Dialogue API | `eleven_v3` only | Supported (multi-speaker) |

**Common v3 tags (not exhaustive):** emotions — `[sad]`, `[angry]`, `[excited]`, `[curious]`, `[sarcastic]`; delivery — `[whispers]`, `[shouts]`, `[slowly]`; reactions — `[laughs]`, `[chuckles]`, `[giggling]`, `[sighs]`, `[clears throat]`; pauses — `[short pause]`, ellipses `...` (v3 does not use SSML `<break>`). Stack at most ~2 compatible tags; avoid `[whispers]` + `[excited]` together.

### Tag reference (official examples)

ElevenLabs does **not** publish a closed enum; tags are open-ended natural-language cues. For the fullest categorized list compiled from official docs (help center, best practices, Text to Dialogue, Expressive mode, v3 blogs), see **[elevenlabs-audio-tags.md](elevenlabs-audio-tags.md)**.

**If tags are not an option (recommended for Ryoko Owari batch):** write the laugh in words (`Ha!` / `he laughs`), use punctuation and pacing (`...`, `—`), shape tone in the Voice Design prompt, or regenerate one line with `ELEVENLABS_MODEL_ID=eleven_v3` for auditions only. Do not put bracket tags in shipped Ren'Py dialogue unless you switch the whole pipeline to v3.
