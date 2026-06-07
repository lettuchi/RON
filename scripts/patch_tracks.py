from pathlib import Path

NEW = r'''
    "corridor": {
        "filename": "corridor.mp3",
        "length_ms": 75000,
        "prompt": (
            "Instrumental Japanese cinematic ambient bed for a feudal-Japan visual novel corridor scene, "
            "Hakuoki / Legend of the Five Rings Ryoko Owari aesthetic. Endless magistrate-quarter hallway at night: "
            "distant paper lanterns, hushed nobility, ink and cedar in the air. Sparse koto harmonics and a soft "
            "breathy sho-like pad, occasional single woodblock or wind-chime color, very slow harmonic motion "
            "around 80 BPM or almost pulseless. Mysterious but not scary — anticipation before power meets the "
            "dancer. No vocals, no lyrics, no modern drums, no synth EDM, no battle percussion. Seamless loop-friendly: "
            "steady texture, no big ending crash, last bar flows back to the first."
        ),
    },
    "office": {
        "filename": "office.mp3",
        "length_ms": 80000,
        "prompt": (
            "Instrumental Japanese cinematic tension bed for an Emerald Magistrate's office in a corrupt canal city, "
            "Hakuoki / Legend of the Five Rings visual novel. Low string drone in a minor modal color, subtle felt "
            "taiko heartbeat far in the mix, sparse biwa or koto single-note accents like a seal waiting to fall. "
            "Mood: ink, cedar, stacked permits, lamplight on lacquer — authority and paperwork, not combat. Tempo "
            "around 75 BPM, restrained and elegant. No vocals, no lyrics, no busy melody, no horror clusters, no modern "
            "kit. Loop-friendly: continuous unease, gentle crossfade at loop point, no fade-to-silence ending."
        ),
    },
    "street": {
        "filename": "street.mp3",
        "length_ms": 85000,
        "prompt": (
            "Instrumental Japanese cinematic street theme for a corrupt canal city at night, Hakuoki / Legend of the "
            "Five Rings Ryoko Owari. Warm shamisen or biwa riff over light hand percussion and soft taiko on 1 and 3, "
            "distant lantern ambience, 88–92 BPM — walking pace, worldly and slightly dangerous but not battle. Scorpion "
            "trade-city honesty: fish, copper, rain on stone implied in the mix texture, not literal sound effects. "
            "No vocals, no lyrics, no EDM four-on-the-floor, no heroic fanfare. Loop-friendly: repeating 8-bar street "
            "motif, steady energy, ending connects to opening motif."
        ),
    },
    "canon_intimate": {
        "filename": "canon_intimate.mp3",
        "length_ms": 75000,
        "prompt": (
            "Instrumental Japanese cinematic romantic aftermath bed for a feudal-Japan otome visual novel, Hakuoki / "
            "Legend of the Five Rings. Warm, tender, implied intimacy without explicit sensuality: slow koto melody and "
            "soft string pads in D major or gentle modal major, 70–72 BPM, breathing room like paper screens and shared "
            "tea. Bittersweet undercurrent — two people who should not trust each other still choosing closeness. No "
            "vocals, no lyrics, no heavy percussion, no erotic R&B, no modern piano pop ballad clichés. Loop-friendly: "
            "soft continuous arc, loop point on a sustained chord, no dramatic stop."
        ),
    },
    "case1_barge": {
        "filename": "case1_barge.mp3",
        "length_ms": 80000,
        "prompt": (
            "Instrumental Japanese cinematic noir investigation theme for a smuggler's canal and river barge at night, "
            "Legend of the Five Rings Ryoko Owari corrupt trade city. Low pulsing strings, muted shamisen ostinato, "
            "occasional wooden boat creak texture very subtle in the mix, rain-ready harmonic minor color. Mood: manifest "
            "lines, Scorpion paint, witness pride before the water — suspense not combat. 82 BPM, loop-friendly, no "
            "vocals, no lyrics, no modern synth bass, no battle taiko rolls. Seamless loop for visual novel investigation "
            "dialogue."
        ),
    },
    "case2_festival": {
        "filename": "case2_festival.mp3",
        "length_ms": 85000,
        "prompt": (
            "Instrumental Japanese festival night theme for a feudal canal-city matsuri, Hakuoki otome visual novel, "
            "Legend of the Five Rings Ryoko Owari. Lively but refined: taiko festival pulse softened for dialogue, "
            "shamisen and fue motifs, paper-lantern warmth in the harmony, 95 BPM feel without overwhelming voice acting. "
            "Undercurrent of danger — celebration as cover for Scorpion business. No vocals, no lyrics, no EDM drop, no "
            "arcade chiptune. Loop-friendly: repeating festival hook every 8 bars, steady energy."
        ),
    },
    "case3_fabric": {
        "filename": "case3_fabric.mp3",
        "length_ms": 80000,
        "prompt": (
            "Instrumental Japanese cinematic suspense for a cramped fabric shop and bolt room in a corrupt city, Hakuoki / "
            "L5R visual novel. Close-in texture: plucked koto in tight repeating pattern, low cello pedal, rare sharp biwa "
            "accents like scissors — claustrophobic, witness-in-danger, not slasher horror. 78 BPM, minor key, loop-friendly "
            "for long dialogue under threat. No vocals, no lyrics, no screaming strings, no modern thriller pulses."
        ),
    },
    "case3_5_date": {
        "filename": "case3_5_date.mp3",
        "length_ms": 75000,
        "prompt": (
            "Instrumental Japanese cinematic date-night bed for a private inn with hidden biwa music through shoji, "
            "feudal-Japan otome visual novel, Ryoko Owari. Intimate and slightly nervous: soft koto, distant biwa phrase "
            "like music through a wall, warm shakuhachi echo, gentle hand percussion like tea service, 68–74 BPM. Romance "
            "with stakes — magistrate and witness alone, not public festival. No vocals, no lyrics, no club beats, no "
            "comedic slapstick. Loop-friendly, tender continuous mood."
        ),
    },
    "case4_dock": {
        "filename": "case4_dock.mp3",
        "length_ms": 70000,
        "prompt": (
            "Instrumental Japanese cinematic action-tension bed for a rainy lower dock and imminent sword confrontation, "
            "Legend of the Five Rings Ryoko Owari, Hakuoki-style visual novel. Driving shamisen and low taiko in restrained "
            "pulses — tension for dialogue and choice menus, not a full anime battle track. Harmonic minor, 100–108 BPM "
            "feel, rain-heavy atmosphere in the mix. No vocals, no lyrics, no Hollywood trailer horns, no EDM. Loop-friendly "
            "for investigation."
        ),
    },
    "case4_5_kobune": {
        "filename": "case4_5_kobune.mp3",
        "length_ms": 75000,
        "prompt": (
            "Instrumental Japanese cinematic bed for a small kobune fishing boat at night on a canal, feudal-Japan otome "
            "visual novel. Gentle hull-rocking pulse in low strings, water-like koto harmonics, intimate warmth mixed with "
            "danger — two people alone on water, magistrate and witness. 72 BPM, minor-to-modal color shift, not horror. "
            "No vocals, no lyrics, no heavy battle taiko, no modern boat engine SFX dominating. Loop-friendly for long boat "
            "scenes."
        ),
    },
    "bad_end_rain": {
        "filename": "bad_end_rain.mp3",
        "length_ms": 28000,
        "prompt": (
            "Instrumental short Japanese cinematic cue: heavy rain on stone and canal water, lonely runner in a corrupt "
            "city at night, Hakuoki tragedy. Sparse piano drops like rain, cold string pad, no percussion grid, 55 BPM, "
            "20–30 seconds of emotional collapse that can loop quietly under narration. No vocals, no lyrics, no thunder "
            "cliché hits, no horror screams."
        ),
    },
    "bad_end_brothel": {
        "filename": "bad_end_brothel.mp3",
        "length_ms": 25000,
        "prompt": (
            "Instrumental Japanese cinematic tragedy stinger for an implied off-screen fate, feudal visual novel bad end, "
            "extremely restrained horror-tragedy without gore. Single descending piano phrase, detuned koto harmonic, airless "
            "string cluster resolving to emptiness, 50 BPM, 25 seconds, no vocals, no lyrics, no scream sound effects, no "
            "modern horror jump sting. Suitable for fade-to-black narration."
        ),
    },
    "bad_end_punishment": {
        "filename": "bad_end_punishment.mp3",
        "length_ms": 60000,
        "prompt": (
            "Instrumental Japanese cinematic dread bed for a sealed magistrate office, power imbalance bad end, Hakuoki / "
            "L5R otome — coercive authority, not slasher gore. Low cello ostinato, single taiko heartbeats, sparse biwa, "
            "65 BPM, claustrophobic. No vocals, no lyrics, no screaming, no explicit impact SFX. Loop-friendly under long CG "
            "narration."
        ),
    },
    "case5_tease": {
        "filename": "case5_tease.mp3",
        "length_ms": 70000,
        "prompt": (
            "Instrumental Japanese cinematic mystery hook for an unfinished investigation — missing pleasure-quarter seal, "
            "feudal magistrate visual novel, Ryoko Owari corrupt city. Office tension meets distant shamisen from the quarter: "
            "low strings, ink-and-incense mood, a single ascending koto question motif like a file line not yet written, 76 BPM. "
            "Hope and danger balanced — sequel tease, not resolution. No vocals, no lyrics. Loop-friendly."
        ),
    },
'''

path = Path(__file__).resolve().parents[1] / "scripts" / "generate_music.py"
text = path.read_text(encoding="utf-8")
needle = "    },\n}\n\n# ---------------------------------------------------------------------------\n# Main-menu opening"
if needle not in text:
    raise SystemExit("needle not found")
text = text.replace(needle, "    }," + NEW + "}\n\n# ---------------------------------------------------------------------------\n# Main-menu opening", 1)
path.write_text(text, encoding="utf-8")
print("patched", path)
