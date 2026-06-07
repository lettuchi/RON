"""Heuristic Eleven v3 tags for Ryoko Owari voice lines (scene + arc aware)."""
from __future__ import annotations

import re

# Policy (2026-06): at least two v3 tags per wired line unless koan exception.
MIN_TAGS_PER_LINE = 2

# Curated tts_text for key beats (full string or tag-prefixed line).
MANUAL_OVERRIDES: dict[str, str] = {
    # --- Prologue door / first meeting ---
    "kaoru_001": "[deadpan] Done complaining?",
    "kaoru_002": "[matter-of-fact] Wrong door. Again.",
    "toa_003": "[nervously] I wasn't— [short pause] That is, I apologize for the disturbance, sochira-no-kata!",
    "narrator_004": "[pause] The door shuts with finality. Toa's ears ring.",
    "toa_010": "[nervously] Honored sochira-no-kata, this unworthy petitioner begs a moment regarding her performer's permit renewal.",
    "toa_014": "[whispers] Forgive me — Emerald Magistrate.",
    "kaoru_012": "[calm] Emerald Magistrate Kitsu Kaoru. You will use my title if you wish to leave with a seal.",
    # --- Bad-end / refuse arc ---
    "toa_037": "[defiant] I'm a petitioner, not your evening entertainment.",
    "toa_038": "[defiant] Justice isn't a private show for magistrates with bored eyes.",
    "toa_039": "[defiant] I'll find another seal. Or another city.",
    "toa_053": "[defiant] That isn't justice. It's just cruelty, and you know it.",
    "toa_060": "[defiant] Guest room previews and forward-dated seals can wait. I still have pride.",
    "kaoru_049": "[matter-of-fact] Justice is what I write on the page you didn't earn.",
    "kaoru_070": "[dismissive] Justice arrives when you stop treating my office like a stage you can exit on your terms.",
    # --- Unless? / canon intimate ---
    "kaoru_064": "[whispers] [short pause] Unless?",
    "kaoru_066": "[whispers] Unless you mean to finish what you started.",
    "kaoru_061": "[calm] Defiance suits you. Cheap seals don't.",
    "toa_047": "[whispers] Magistrate-sama. That is not in any permit renewal I read.",
    "toa_049": "[whispers] If you're going to hold me, hold me like you mean the audition.",
    "kaoru_075": "[whispers] You earned more than noise tonight.",
    "kaoru_077": "[calm] There. Signed.",
    "kaoru_080": "[whispers] Thirtieth. You'll knock on the right door — I'll leave it unlatched.",

    # toa_001_prologue_flat --- Prologue Toa (flat heuristic fallbacks) ---
    "toa_001": "[nervously] I was sure the clerk said third hall, fourth door on the left. Or was it the right?",
    "toa_007": "[defiant] I've come too far to be scared off by a reputation.",
    "toa_008": "[cheerfully] Every sign points back to this door. Of course it does.",
    "toa_012": "[cheerfully] I promise I'm only lost geographically, not legally. May I present my renewal request?",
    "toa_013": "[cheerfully] Crane training says brave. Unicorn roads say stupid is survivable.",
    "toa_016": "[nervously] Post GEM-puku, traveling from Unicorn lands. I mean to establish residence and perform legally.",
    "toa_017": "[cheerfully] The roads taught me flexibility. The Crane taught me posture.",
    "toa_020": "[nervously] They should be current. I checked before leaving\u2014",
    "toa_021": "[nervously] If I cannot renew locally, they'll send me back to the Academy. I can't\u2014 not yet.",
    "toa_023": "[calm] The Crane taught me to know when a battle isn't worth the obi.",
    "toa_025": "[cheerfully] Almost is a start. I dance for a living \u2014 I know how to build toward a finale.",
    "toa_026": "[nervously] I have no patrons here. No standing. If you turn me out, I sleep in the canal district.",
    "toa_027": "[cheerfully] My pony needs shoes. The innkeeper tolerates me because I fold linens without complaint.",
    "toa_028": "[defiant] I'm still here. That counts for something.",
    "toa_030": "[nervously] It's March twenty-sixth. By tomorrow I need proof I belong here.",
    "toa_032": "[nervously] I have training. I have\u2014",
    "toa_033": "[defiant] You want a performance.",
    "toa_034": "[defiant] If I perform, you sign. No delays, no new conditions after.",
    "toa_040": "[defiant] Fine. One dance. One seal. Then I never perform for you again.",
    "toa_042": "[cheerfully] The maiden waits at the gate. The road is long. She walks anyway.",
    "toa_044": "[defiant] That earns your seal. You said impress you \u2014 I did.",
    "toa_045": "[defiant] We had terms. No delays.",
    "toa_046": "[nervously] Pending?",
    "toa_050": "[whispers] Unless you sign before dawn. Unless Ryoko Owari becomes mine to dance in \u2014 legally.",
    "toa_051": "[defiant] Unless I find a magistrate who reads dates instead of moods. Good evening.",
    "toa_054": "[defiant] I gave you the performance. I named my price. What more\u2014",
    "toa_055": "[cheerfully] I'll be back. With a better argument and dry obijime.",
    "toa_058": "[defiant] I came for a seal, not a lesson in your appetite.",
    "toa_064": "[defiant] You dated it forward on purpose.",
    "toa_065": "[cheerfully] [chuckles] Fine. I'll bring rice crackers and a better fan dance.",
    "toa_066": "[defiant] Guest room preview, forward-dated paperwork, and you call it negotiable.",
    "toa_184": "[nervously] O-oh, alright.",
    "narrator_174": "[pause] Case Four's ink is still wet. Winter Scorpion raids have the harbor clerks lying about grain \u2014 and Toa has learned to read fear in filing dates.",
    "narrator_176": "[pause] She peers from behind a split mooring post, witness notes tucked in her sleeve. Then a familiar voice \u2014 wrong register, wrong weather.",
    "narrator_177": "[pause] The Emerald Magistrate, soggy and furious, and a boat \u2014 in this freezing cold?",
    "narrator_179": "[pause] Knees, hips, shoulder \u2014 wet wood. Pain and surprise in one breath. The rock of the boat is wrong, almost intimate.",
    "narrator_181": "[pause] When the rhythm ends, they are a knot of warmth and borrowed robes. Bay cold waits outside the strake.",
    "narrator_182": "[pause] They ferry back before the watch invents a drowning. Steam and citrus in the magistrate wing \u2014 bath, kotatsu, treaty without ledger line.",
    "toa_062": "[nervously] Then sign. Before I lose my nerve and my obi in the same breath.",
    # --- Rain gameover narration (IDs from narrator_manifest first-appearance order) ---
    "narrator_108": "[pause] Behind her the magistrate's gate slides home — lacquer and iron, final as a verdict she didn't get to read.",
    "narrator_113": "[pause] She slows where the lamplight gives out. Past it the city is only rain and the shape of rain.",
    "narrator_114": "[dramatic] She kept her pride. She picked it up off the magistrate's desk, whole, and carried it out under her arm. Tonight it is the only thing she owns in Ryoko Owari.",
    "narrator_115": "[dramatic] Somewhere behind her an expired permit waits for a smirk that will never bother to chase her down. It doesn't have to. The city does that for him.",
    # --- Case 1 companion / investigation beats ---
    "kaoru_081": "[matter-of-fact] Early is still obedience. Sit before you spill something on my docket.",
    "toa_068": "[cheerfully] Snacks after paperwork. That's still the order of operations.",
    "toa_072": "[defiant] The permit still expires. Some of us read dates.",
    "toa_077": "[cheerfully] Fine. But I'm billing you for snacks.",
    "kaoru_139": "Ask the river when you're qualified. Until then — observe.",
    # --- Case 3.5 "Is this a date?" (Tear Drop kaiseki / dance / deflection) ---
    "kaoru_171": "[calm] I wanted to show you my appreciation for the work you have done for me.",
    "toa_141": "[cheerfully] [warmly] I haven't listened to music or seen dancing just for fun in a really long time. [short pause] This is really lovely, Magistrate-sama.",
    "kaoru_177": "[deadpan] [chuckles] If I ever find any dance crimes I know who I need to bring with me.",
    "kaoru_178": "[matter-of-fact] Relax. Enjoy the dance. Unless watching is the fun — what could they do better?",
    "kaoru_191": "[calm] Never once. You are very well loved in this city.",
    "toa_168": "[defiant] [short pause] Is this a date?",
    "kaoru_194": "[deadpan] A date is a line on a permit book.",
    "kaoru_195": "[matter-of-fact] This is appreciation. Witness competence. Food so you do not faint on my desk tomorrow.",
    "kaoru_196": "[dismissive] It is the answer the quarter deserves. You are patronage artist, woman who trusted me in the bolt room — do not borrow festival vocabulary because the sake was expensive.",
    "toa_170": "[defiant] The festival was real. Your hand on the cup was real. Do not tell me to un-feel it because the file prefers silence.",
    "kaoru_198": "[pause] [exhales] ...No.",
    "kaoru_199": "[whispers] It is the closest I come before I learn better.",
    "narrator_171": "[pause] Crane training keeps her face pleasant. Inside, something unnamed aches — not love by name, only the wish he would stop stepping back after every forward step.",
    # --- Case 4.5 Teardrop kobune ---
    "toa_173": "[cheerfully] Magistrate-sama — I can take the island manifest before dawn. The ferry masters file late when they are frightened.",
    "toa_174": "[defiant] That is not how permits work.",
    "toa_175": "[excited] Magistrate-sama!",
    "toa_176": "[nervously] Are you alright? What in the world happened to you?",
    "toa_177": "[sad] Bad day? Yes — yes, it's been a bad day!",
    "toa_178": "[crying] [nervously] Calamity and hunger and suffering, spooky nonsense in the wards — [sighs] and now you — almost sunk a boat, [short pause] and it's so cold, and you could have died—",
    "toa_179": "[sad] ....why are you even in a boat?",
    "toa_180": "[whispers] Yes, Magistrate-sama.",
    "toa_181": "[defiant] I am not cargo on your bad night.",
    "toa_182": "[defiant] Then ask — not order — when you need me.",
    "toa_185": "[whispers] ...You didn't. You didn't find me.",
    "toa_186": "[defiant] I found you. Remember?",
    "toa_187": "[whispers] I was looking for a magistrate for my paperwork. But I found Kitsu Kaoru the man.",
    "toa_188": "[cheerfully] Your color is back. Can we go home now?",
    "toa_189": "[cheerfully] Bath. Mikan under the kotatsu. That is the treaty.",
    "toa_191": "[cheerfully] The file line is written. I am still at your door.",
    "narrator_175": "[pause] Teardrop Island marina — not the licensed quarter's polished stone, but winter ribs and broken pilings. Bay wind cuts through rubble. A small kobune rocks at the tide line, paint scarred from someone else's war.",
    "narrator_178": "[pause] A sniffle. [short pause] A whimper. Tears on wind-reddened cheeks — concern he will not let her offer, and she does not yet know if he is whole.",
    "narrator_180": "[whispers] Rocking hull. Gunwales under his palms when the boat threatens to tip. *Good girl* breathed against her hair — implied, never filed, hunger without ledger line.",
    # --- Case 2 festival / morning tea ---
    "narrator_238": "[pause] Fireworks climb over the canal — chrysanthemum bursts, then falling embers that die in the water wrong-green and beautiful. Toa flinches at the first crack; Kaoru's hand finds her wrist, steady, proprietary.",
    "kaoru_269": "[whispers] Let them watch the sky. I am watching you remember you are still alive after ash.",
    "narrator_240": "[pause] He kisses her on the bench — not performance, not ink — mouth warm against hers while fireworks stutter overhead and the city pretends it is innocent.",
    "narrator_241": "[pause] Her smile stays where he can see it. Underneath, something dull settles — not heartbreak, not yet a name for it — only the ache of wanting his nod to mean more than patronage.",
    "kaoru_271": "[dismissive] A festival kiss is paper confetti — pretty, public, worthless in the morning docket. You will not read my mouth like a charter.",
    "kaoru_274": "[whispers] Then you choose a door I already hold. Guest room on the descent — one screen, one lock, my corridor.",
    "narrator_242": "[whispers] Shoji breath and lantern grain. Clothed silhouettes, then fabric whisper — implied, never filed, satisfaction without ledger line.",
    "narrator_245": "[pause] Dawn through cedar shutters. Duplicate charter cooling on the desk; tea steaming; the outer clerk already transferred to a cell.",
    "kaoru_280": "[whispers] The Academy thinks you're still respectable. I think you're still mine to complicate.",
    "toa_243": "[nervously] Don't make me used to mornings that don't hurt.",
    "kaoru_282": "[whispers] Too late. Case Three will hurt worse. I'll be beside you when it does — if you keep choosing me over the door.",
    # --- Case 3 / 4 investigation (bolt room / dock raid) ---
    "narrator_254": "[dramatic] [pause] The shelf goes. Silk hammers air; dust becomes snow. [short pause] Toa has one breath and two bad choices — call the man at the door, or prove Crane training still wins alone.",
    "narrator_264": "[dramatic] Three blades in rain — Kaoru's katana a clean arc, Toa's dance-line wakizashi, Kurogane's Scorpion cut trying to split them. Crate wood splinters. Footing is blood-slick tar.",
    "narrator_266": "[pause] She drops back — one step, not cowardice. Kaoru crosses her line without looking; his coat takes the foreman's edge where her obi would have torn.",
    "narrator_267": "[whispers] Steel screams once. Kurogane stumbles — custody rope, not mercy. Kaoru's sleeve is dark with rain or worse; his free hand still finds her wrist, pinning her behind his shoulder.",
    "kaoru_315": "[whispers] Breathe. Count. You are still mine to file.",
    "toa_268": "[whispers] You — you took the cut meant for me.",
    # --- Case 1 companion charm ---
    "kaoru_321": "[warmly] [calm] I like you. So much so that I want to keep you around.",
    # --- Case 1 punishment bridge (canal witness / desk threat) ---
    "toa_272": "[defiant] [cheerfully] Then punish me, Magistrate-sama. You've threatened it since I touched the wrong door.",
    "toa_273": "[nervously] [short pause] I didn't— I meant you wouldn't—",
    "toa_274": "[whispers] [defiant] ...Wouldn't dare. Keep guessing.",
    "toa_275": "[whispers] [calm] Behind closed screens. You heard me the first time.",
    "toa_276": "[nervously] [cheerfully] Magistrate-sama— one more pass at the canal—",
    "kaoru_322": "[dismissive] [calm] You ask for my desk in front of a drowning clerk and a Miya witness. Stupid, To-chan. Mine.",
    "kaoru_323": "[dismissive] [calm] Office. My corridor. We're not finished when you decide we're finished.",
    "kaoru_324": "[whispers] [calm] You asked for closed screens twice in one night. You will have them.",
    "kaoru_325": "[dismissive] [calm] Desk. Now. Before you mistake appetite for permission again.",
    "kaoru_326": "[matter-of-fact] [dismissive] Empty witness note. Blank collar line. You do not get another hour.",
    "kaoru_327": "[dismissive] [calm] Desk. You will learn what my hall costs when you arrive with nothing to sign.",
    "narrator_269": "[pause] [dramatic] Rain beads on the canal rope. The clerk studies his wax tablet. Kaoru's hand closes on her elbow — escort, not comfort — and the compound swallows them.",
    # --- Bow disambiguation (courtesy bow / bending, not ribbon or archery) ---
    "kaoru_007": "[matter-of-fact] At least your courtesy bow didn't wobble. Continue — briefly.",
    "kaoru_015": "[matter-of-fact] Posture on the cushion. We'll see if your feet match your courtesy bow.",
    "kaoru_092": "[matter-of-fact] After. And stop your courtesy bowing at every clause. My neck aches from watching.",
    "kaoru_233": "[matter-of-fact] You bow when the floor meets your knees — bend at the waist, courtesy bow. Less talk.",
    "narrator_023": "The fan closes on the final beat [pause] not a courtesy bow, but a held breath.",
    "narrator_095": "But Toa has already slipped past the desk — the kitchen way, the servant's courtesy bow, the easy warmth of a woman who has carried tea in worse rooms. A young geisha looks up from folding a dead man's spare haori.",
    "narrator_097": "The geisha rises. She is perhaps nineteen, her white makeup cried through at the edges. She bows too low in courtesy, the way frightened people do when they have already decided to be brave.",
    "narrator_099": "She has already decided Toa is safe. The kitchen courtesy bow bought what no seal could. Her words come in a rush, like water finding the crack it wanted.",
    "narrator_108": "[pause] The factor weighs the room, the spoken record, the unmoving magistrate. Then he bows — a deliberate courtesy bow at the waist — the exact depth that insults without inviting a blade, and withdraws into the rain.",
    "narrator_126": "The lamplight ends. What is left is rain on white hair and a courtesy bow that will not hold.",
    "narrator_152": "A servant offers crisp hojicha — she will hunt that tea again for weeks. When she asks, they bow in courtesy: yes, Magistrate Kitsu has taken the venue. Performances upon request from either neighbor.",
    "narrator_154": "She tries to bow as she always does — a shallow courtesy bow at the waist. The stiff fukuro obi allows barely a hinge. She laughs inwardly and straightens, catching his fragrance — the same note as the first wrong door.",
    "toa_197": "[defiant] I won't bow low — not a courtesy bow — to your appetite.",
}

# Kaoru aphorism / koan lines: delivery stays flat; do not tag.
KAORU_KOAN_IDS = frozenset({"kaoru_139"})
KAORU_KOAN_PHRASES = (
    "ask the river",
    "until then — observe",
    "until then - observe",
)


def _has_tag(text: str) -> bool:
    return bool(re.search(r"\[[^\]]+\]", text))


def _tag_count(text: str) -> int:
    return len(re.findall(r"\[[^\]]+\]", text))


def _strip_leading_tags(text: str) -> str:
    return re.sub(r"^(?:\[[^\]]+\]\s*)+", "", text).lstrip()


def _secondary_tag(primary: str, character: str, game_text: str) -> str:
    """Complement an existing lead tag (avoid doubling matter-of-fact)."""
    p = primary.strip("[]").lower()
    low = game_text.lower()
    if p in ("nervously", "nervous"):
        return "[short pause]" if "..." in game_text or "—" in game_text else "[cheerfully]"
    if p in ("cheerfully", "cheerful", "excited", "excitedly"):
        return "[nervously]" if "?" in game_text or "magistrate" in low else "[short pause]"
    if p in ("defiant",):
        return "[whispers]" if "magistrate" in low else "[calm]"
    if p in ("whispers", "whisper", "whispering"):
        return "[warmly]" if character == "toa" else "[calm]"
    if p in ("sad", "crying"):
        return "[nervously]"
    if p in ("deadpan",):
        return "[dismissive]"
    if p in ("dismissive",):
        return "[calm]"
    if p in ("calm",):
        return "[deadpan]" if character == "kaoru" else "[pause]"
    if p in ("matter-of-fact",):
        return "[dismissive]" if character == "kaoru" else "[pause]"
    if p in ("pause", "short pause"):
        return "[dramatic]" if len(game_text) > 60 else "[whispers]"
    if p in ("dramatic", "dramatically"):
        return "[pause]"
    if p in ("giggling", "chuckles", "laughs"):
        return "[cheerfully]"
    pairs = {
        "toa": "[cheerfully]",
        "kaoru": "[calm]",
        "narrator": "[pause]",
    }
    return pairs.get(character, "[pause]")


def _default_pair(character: str, game_text: str) -> tuple[str, str]:
    low = game_text.lower()
    if character == "toa":
        if re.search(r"\b(defiant|won't|isn't justice|cruelty|punish)\b", low):
            return "[defiant]", "[cheerfully]"
        if "magistrate" in low:
            return "[nervously]", "[cheerfully]"
        return "[cheerfully]", "[nervously]"
    if character == "kaoru":
        if re.search(r"\b(desk|witness|mine\.|stupid)\b", low):
            return "[dismissive]", "[calm]"
        return "[calm]", "[deadpan]"
    if re.search(r"\b(rain|gate|verdict|game over|swallows)\b", low):
        return "[pause]", "[dramatic]"
    if "—" in game_text:
        return "[pause]", "[dramatic]"
    return "[pause]", "[calm]"


def ensure_min_tags(
    tts: str, character: str, line_id: str, game_text: str
) -> str:
    if _is_kaoru_koan(game_text, line_id):
        return tts
    n = _tag_count(tts)
    if n >= MIN_TAGS_PER_LINE:
        return tts
    if n == 1:
        tags = re.findall(r"\[[^\]]+\]", tts)
        sec = _secondary_tag(tags[0], character, game_text)
        body = _strip_leading_tags(tts)
        return f"{tags[0]} {sec} {body}"
    t1, t2 = _default_pair(character, game_text)
    return f"{t1} {t2} {tts}"


def _lead(text: str, tag: str) -> str:
    if _tag_count(text) >= MIN_TAGS_PER_LINE:
        return text
    if _tag_count(text) == 1:
        return text
    return f"{tag} {text}"


def _dual_lead(text: str, tag1: str, tag2: str) -> str:
    if _tag_count(text) >= MIN_TAGS_PER_LINE:
        return text
    if _tag_count(text) == 1:
        tags = re.findall(r"\[[^\]]+\]", text)
        return f"{tags[0]} {tag2} {_strip_leading_tags(text)}"
    return f"{tag1} {tag2} {text}"


def _suffix(text: str, tag: str) -> str:
    if _tag_count(text) >= MIN_TAGS_PER_LINE:
        return text
    if _tag_count(text) == 0:
        return f"{text} {tag}"
    return text


def _insert_before_clause(text: str, clause: str, tag: str) -> str:
    if _tag_count(text) >= MIN_TAGS_PER_LINE:
        return text
    idx = text.lower().find(clause.lower())
    if idx <= 0:
        return _lead(text, tag)
    return f"{text[:idx].rstrip()} {tag} {text[idx:].lstrip()}"


def _is_kaoru_koan(text: str, line_id: str = "") -> bool:
    if line_id in KAORU_KOAN_IDS:
        return True
    low = text.lower()
    return any(p in low for p in KAORU_KOAN_PHRASES)


# Mid-line delivery: reactions, pauses, laughs (docs/elevenlabs-audio-tags.md).
REACTION_PAUSE_TAGS = frozenset({
    "pause", "short pause", "long pause", "pauses",
    "pause, then normally",
    "sighs", "sigh", "exhales", "exhales sharply", "inhales deeply",
    "frustrated sigh",
    "laughs", "laughing", "laughs harder", "starts laughing", "wheezing",
    "laughing hysterically", "chuckles", "giggles", "giggling", "snorts",
    "with genuine belly laugh", "stifling laughter", "cracking up",
    "gulps", "swallows", "happy gasp", "gasp", "groaning", "clears throat",
    "stammers", "starting to speak", "jumping in", "overlapping",
    "interrupting, then stopping abruptly",
})

DELIVERY_WOVEN_TAGS = frozenset({
    "whispers", "whisper", "whispering", "shouts", "shout", "shouting",
    "quietly", "loudly", "slow", "slowly", "rushed",
})

MAX_MID_WOVEN_PER_LINE = 2


def _tag_body(raw: str) -> str:
    return raw.strip().lower()


def is_reaction_pause_tag(tag: str) -> bool:
    t = _tag_body(tag)
    if t in REACTION_PAUSE_TAGS:
        return True
    return t.endswith(" pause") or t.startswith("pause ")


def is_woven_delivery_tag(tag: str) -> bool:
    t = _tag_body(tag)
    return t in REACTION_PAUSE_TAGS or t in DELIVERY_WOVEN_TAGS


def count_reaction_pause_tags(text: str) -> int:
    return sum(
        1 for m in re.finditer(r"\[([^\]]+)\]", text) if is_reaction_pause_tag(m.group(1))
    )


def has_mid_woven_tag(text: str) -> bool:
    """True if a reaction/pause/delivery tag appears after the lead tag block."""
    body = _strip_leading_tags(text)
    for m in re.finditer(r"\[([^\]]+)\]", body):
        if is_woven_delivery_tag(m.group(1)):
            return True
    return False


def _scene_from_source(source: str) -> str:
    s = (source or "").lower()
    if "case3_5" in s or "date_interlude" in s:
        return "case35_dinner"
    if "case34" in s or "case3_4" in s or "investigation" in s and "case" in s:
        return "dock_fight"
    if "case4_5" in s or "boat" in s:
        return "teardrop_boat"
    if "punishment" in s or "case_endings" in s:
        return "punishment"
    if "festival" in s or "case2" in s:
        return "festival"
    if "prologue" in s:
        return "prologue"
    if "rain" in s or "gameover" in s or "game_over" in s:
        return "rain_end"
    return "general"


def _nearby_has_tag(text: str, idx: int, tag: str, window: int = 28) -> bool:
    lo = max(0, idx - window)
    hi = min(len(text), idx + window)
    return tag.lower() in text[lo:hi].lower()


def _insert_before(text: str, needle: str, tag: str) -> str:
    idx = text.find(needle)
    if idx <= 0 or _nearby_has_tag(text, idx, tag):
        return text
    return f"{text[:idx].rstrip()} {tag} {text[idx:].lstrip()}"


def _insert_after(text: str, needle: str, tag: str) -> str:
    idx = text.find(needle)
    if idx < 0:
        return text
    end = idx + len(needle)
    if _nearby_has_tag(text, end, tag):
        return text
    return f"{text[:end].rstrip()} {tag} {text[end:].lstrip()}"


def _insert_after_nth_comma(text: str, n: int, tag: str) -> str:
    count = 0
    for i, ch in enumerate(text):
        if ch != ",":
            continue
        count += 1
        if count == n:
            return _insert_after(text, text[: i + 1], tag)
    return text


def _mid_woven_count(text: str) -> int:
    body = _strip_leading_tags(text)
    return sum(
        1 for m in re.finditer(r"\[([^\]]+)\]", body) if is_woven_delivery_tag(m.group(1))
    )


def weave_delivery_tags(
    tts: str,
    character: str,
    game_text: str,
    line_id: str = "",
    source: str = "",
) -> tuple[str, str]:
    """Weave reaction/pause/delivery tags into tts_text (often mid-sentence)."""
    if _is_kaoru_koan(game_text, line_id):
        return tts, ""
    if line_id in MANUAL_OVERRIDES and _mid_woven_count(tts) >= 1:
        return tts, ""

    scene = _scene_from_source(source)
    low = game_text.lower()
    out = tts
    notes: list[str] = []

    def add(note: str, fn) -> None:
        nonlocal out
        if _mid_woven_count(out) >= MAX_MID_WOVEN_PER_LINE:
            return
        prev = out
        out = fn()
        if out != prev:
            notes.append(note)

    # Ellipsis / trailing beat
    if "..." in game_text and "[pause]" not in out.lower() and "[short pause]" not in out.lower():
        if "..." in out:
            add("ellipsis beat", lambda: _insert_before(out, "...", "[short pause]"))

    # Stammer / cut-off em dash (dialogue)
    if re.search(r"\w+—\s", game_text) or "— I" in game_text or "didn't—" in game_text:
        for needle in ("— I", "didn't—", "wouldn't—", "wasn't—"):
            if needle in out and "[short pause]" not in out[max(0, out.find(needle) - 20) : out.find(needle) + 20]:
                add("stammer", lambda n=needle: _insert_before(out, n, "[short pause]"))
                break

    # Humor / playful
    if re.search(r"\b(ha\b|teehee|giggle|snacks|billing|rice cracker|fan dance)\b", low):
        if "[chuckles]" not in out.lower() and "[giggling]" not in out.lower():
            body = _strip_leading_tags(out)
            if character == "kaoru" and re.search(r"\b(crime|dance crime|cheeky)\b", low):
                if "." in body:
                    first_sent = body.split(".")[0] + "."
                    add("dry laugh", lambda fs=first_sent: _insert_after(out, fs, "[chuckles]"))
            elif character == "toa" and "." in body:
                first_sent = body.split(".")[0] + "."
                add("playful laugh", lambda fs=first_sent: _insert_after(out, fs, "[chuckles]"))

    # Distress / breakdown
    if re.search(r"\b(bad day|could have died|calamity|almost sunk|crying|so cold)\b", low):
        if "and now you" in out.lower() and "[sighs]" not in out.lower():
            add("distress sigh", lambda: _insert_before(out, "and now you", "[sighs]"))
        elif "[sighs]" not in out.lower() and len(game_text) > 55:
            add("distress sigh", lambda: _insert_after_nth_comma(out, 2, "[sighs]"))

    # Realization / exhale
    if re.search(r"\b(remember\?|found you|why are you|lose my nerve)\b", low):
        if "[exhales]" not in out.lower():
            body = _strip_leading_tags(out)
            first_word = body.split()[0] if body else ""
            if first_word and first_word[0].isupper():
                add("realization", lambda: _insert_after(out, first_word, "[exhales]"))

    # Fear / gulp
    if re.search(r"\b(lose my nerve|terrified|gulps|could have died)\b", low) and character == "toa":
        if "[gulps]" not in out.lower() and "?" in game_text:
            add("fear gulp", lambda: _insert_before(out, "?", "[gulps]"))

    # Long lines: clause pause after first comma (not every line)
    body = _strip_leading_tags(out)
    if len(game_text) > 72 and "," in body and not has_mid_woven_tag(out):
        add("clause pause", lambda: _insert_after_nth_comma(out, 1, "[short pause]"))

    # Semicolon narration beats
    if character == "narrator" and ";" in game_text and len(game_text) > 65:
        semi = game_text.find(";")
        frag = game_text[: semi + 1]
        if frag in out and "[short pause]" not in out.lower():
            add("semi beat", lambda: _insert_after(out, frag, "[short pause]"))

    # Scene: Case 3.5 dinner — warm pauses on gratitude / deflection
    if scene == "case35_dinner":
        if character == "toa" and re.search(r"\b(lovely|long time|festival was real)\b", low):
            if "Magistrate" in out and "[short pause]" not in out.lower():
                add("dinner warmth", lambda: _insert_before(out, "Magistrate", "[short pause]"))
        if character == "kaoru" and re.search(r"\b(appreciation|witness competence|festival vocabulary)\b", low):
            if len(game_text) > 50 and "," in out:
                add("dinner measured", lambda: _insert_after_nth_comma(out, 1, "[short pause]"))

    # Scene: dock fight — breath before action pivot
    if scene == "dock_fight":
        if character == "narrator" and re.search(r"\b(blade|sword|crate|footing|rain)\b", low):
            if "—" in out and "[exhales sharply]" not in out.lower():
                parts = re.split(r"\s[—–]\s", _strip_leading_tags(out), maxsplit=1)
                if len(parts) == 2:
                    add("fight breath", lambda: _insert_before(out, "—", "[exhales sharply]"))
        if character == "toa" and re.search(r"\b(took the cut|breathe|count)\b", low):
            if "[exhales]" not in out.lower():
                add("aftermath breath", lambda: _insert_after(out, "You", "[exhales]"))

    # Scene: teardrop boat — sniffle / cold
    if scene == "teardrop_boat":
        if character == "narrator" and "sniffle" in low:
            add("sniffle beat", lambda: _insert_after(out, "sniffle.", "[short pause]"))
        if character == "toa" and "cold" in low and "[shivering]" not in out.lower():
            if "[short pause]" not in out.lower() and "so cold" in out.lower():
                add("cold beat", lambda: _insert_before(out, "so cold", "[short pause]"))

    # Scene: punishment bridge — possessive whisper mid
    if scene == "punishment":
        if character == "kaoru" and re.search(r"\b(desk|corridor|screens|mine\.)\b", low):
            if "To-chan" in out and "[whispers]" not in out.lower() and len(game_text) < 90:
                add("punishment hush", lambda: _insert_before(out, "To-chan", "[whispers]"))
        if character == "toa" and re.search(r"\b(wouldn't|dare|guessing)\b", low):
            if "—" in out and "[short pause]" not in out:
                add("punishment stumble", lambda: _insert_before(out, "—", "[short pause]"))

    # Scene: festival — fireworks pause
    if scene == "festival" and character == "narrator" and "fireworks" in low:
        if ";" in out or "," in out:
            add("festival hush", lambda: _insert_after_nth_comma(out, 1, "[pause]"))

    # Scene: rain gameover — long dramatic pause mid
    if scene == "rain_end" and character == "narrator" and len(game_text) > 70:
        if "—" in out and count_reaction_pause_tags(out) < 2:
            add("rain cadence", lambda: _insert_before(out, "—", "[long pause]"))

    # Unless? intimate — already manual for kaoru_064
    if re.search(r"\bunless\?\b", low) and "[short pause]" not in out.lower():
        add("unless beat", lambda: _insert_before(out, "Unless", "[short pause]"))

    return out, "; ".join(notes)


def tag_toa(text: str) -> tuple[str, str]:
    low = text.lower()

    # Defiant / bad-end energy (before generic magistrate rules)
    if re.search(
        r"\b(not your evening|isn't justice|isn't a private|another seal|another city|"
        r"cruelty|still have pride|petitioner, not|won't make it a habit)\b",
        low,
    ):
        return _dual_lead(text, "[defiant]", "[cheerfully]"), "defiant pushback"
    if re.search(r"\b(punish me|threatened it since)\b", low):
        return _dual_lead(text, "[defiant]", "[cheerfully]"), "punishment bravado"
    if re.search(r"\b(i'm here for a seal, not|not a leash|leash)\b", low):
        return _dual_lead(text, "[defiant]", "[calm]"), "defiant"

    # Flustered apology / disturbance
    if "apolog" in low or "disturb" in low or "wasn't—" in text or "wasn't-" in text:
        return _dual_lead(text, "[nervously]", "[short pause]"), "flustered apology"
    if re.search(r"\b(forgive me|sochira-no-kata|unworthy petitioner)\b", low):
        return _dual_lead(text, "[nervously]", "[cheerfully]"), "formal fluster"

    # Case 4.5 breakdown / pier beats (before generic magistrate-sama)
    if re.search(r"\b(bad day|could have died|almost sunk|calamity and hunger)\b", low):
        return _dual_lead(text, "[sad]", "[nervously]"), "distress"
    if re.search(r"\b(found you|not cargo|ask — not order)\b", low):
        return _dual_lead(text, "[defiant]", "[warmly]"), "spine"
    if re.search(r"\b(deck of a boat|tatami mat)\b", low):
        return _dual_lead(text, "[nervously]", "[whispers]"), "muttered beat"

    # Intimate / quiet magistrate-sama — default bright, not blanket whisper
    if "magistrate-sama" in low or (
        re.search(r"\bemerald magistrate\b", low) and len(text) < 85
    ):
        if re.search(
            r"\b(hold me|not in any permit|yes, magistrate|th-thank|lose my nerve)\b",
            low,
        ):
            return _dual_lead(text, "[whispers]", "[warmly]"), "intimate deferential"
        if re.search(r"\b(forgive|begs? a moment|apolog)\b", low):
            return _dual_lead(text, "[nervously]", "[cheerfully]"), "deferential nervous"
        if "!" in text or re.search(r"\b(before dawn|manifest|written|still at your)\b", low):
            return _dual_lead(text, "[cheerfully]", "[excited]"), "bright deferential"
        if "?" in text:
            return _dual_lead(text, "[nervously]", "[cheerfully]"), "deferential question"
        return _dual_lead(text, "[cheerfully]", "[nervously]"), "magistrate-sama"

    if re.search(r"\bmagistrate\b", low) and len(text) < 70:
        if "?" in text or re.search(r"\b(hopefully|charm)\b", low):
            return _dual_lead(text, "[cheerfully]", "[nervously]"), "hopeful"
        return _dual_lead(text, "[nervously]", "[cheerfully]"), "magistrate-facing"

    if re.search(r"\b(afraid|terrified|panic|lose my nerve)\b", low):
        return _dual_lead(text, "[nervously]", "[short pause]"), "fear"
    if re.search(r"\bscared\b", low) and "scared off" not in low:
        return _dual_lead(text, "[nervously]", "[calm]"), "fear"

    # Bright / earnest (short)
    if re.search(r"\b(thank|wonderful|perfect|excellent|glad|nicely)\b", low) and len(text) < 90:
        return _dual_lead(text, "[cheerfully]", "[excited]"), "bright"
    if re.search(r"\b(snacks|curry|rice cracker|billing)\b", low) and len(text) < 95:
        return _dual_lead(text, "[cheerfully]", "[nervously]"), "playful earnest"
    if re.search(r"\b(one more corridor|hopefully both|round two)\b", low):
        return _dual_lead(text, "[cheerfully]", "[defiant]"), "determined bright"

    # Performance / dance energy
    if re.search(r"\b(audience of one|watch closely|regret looking|dance until)\b", low):
        return _dual_lead(text, "[cheerfully]", "[excited]"), "performance"
    if text.count("!") >= 2 or re.search(r"\b(justice|operations)\b", low) and "!" in text:
        return _dual_lead(text, "[excited]", "[cheerfully]"), "playful energy"

    if "..." in text and len(text) > 45:
        return _insert_before_clause(text, "...", "[short pause]"), "beat"

    if re.search(r"\b(ha|giggle|teehee)\b", low):
        return _dual_lead(text, "[cheerfully]", "[giggling]"), "light laugh"

    if re.search(r"\b(kakita toa|dancer of the kakita)\b", low):
        return _dual_lead(text, "[cheerfully]", "[nervously]"), "introduction"

    return text, ""


def tag_kaoru(text: str, line_id: str = "") -> tuple[str, str]:
    if _is_kaoru_koan(text, line_id):
        return text, ""

    low = text.lower()

    # Intimate / low register (before dry defaults)
    if re.search(
        r"\b(unless\?|unless you mean|earned more than noise|leave it unlatched|"
        r"finish what you started|pending\.|signature\.\.\.)\b",
        low,
    ):
        return _dual_lead(text, "[whispers]", "[calm]"), "intimate"
    if re.search(r"\b(whisper|come closer|listen closely)\b", low):
        return _dual_lead(text, "[whispers]", "[warmly]"), "intimate"
    if re.search(r"\b(i like you|keep you around)\b", low):
        return _dual_lead(text, "[warmly]", "[calm]"), "companion charm"
    if re.search(r"\b(stupid, to-chan|my corridor|closed screens|mistake appetite)\b", low):
        return _dual_lead(text, "[dismissive]", "[calm]"), "punishment possessive"
    if re.search(r"\b(drowning clerk|miya witness|witness note|blank collar)\b", low):
        return _dual_lead(text, "[dismissive]", "[matter-of-fact]"), "public desk threat"

    # Terse one-liners
    if len(text) < 28 and text.rstrip().endswith((".", "?")):
        if re.search(r"\b(done|wrong|still there|tedious|knock|enter|stand|may have)\b", low):
            return _dual_lead(text, "[deadpan]", "[dismissive]"), "dry beat"
        if text.rstrip().endswith("?"):
            return _dual_lead(text, "[deadpan]", "[calm]"), "dry question"

    if re.search(r"\b(it does\. door\.|better\. most|these dates\.|may have\.)\b", low):
        return _dual_lead(text, "[deadpan]", "[calm]"), "terse"

    if re.search(r"\b(tedious|waste|boring|enough|leave before|charge you)\b", low):
        return _dual_lead(text, "[dismissive]", "[calm]"), "curt"

    if re.search(r"\b(sit\. not catalog|said sit|cushion\. floor)\b", low):
        return _dual_lead(text, "[dismissive]", "[calm]"), "command"

    if re.search(r"\b(useful|well done|good performance|almost earns|defiance suits)\b", low):
        return _dual_lead(text, "[calm]", "[warmly]"), "measured approval"

    if re.search(r"\b(enter|follow instructions|companion duties|state your business)\b", low):
        return _dual_lead(text, "[calm]", "[dismissive]"), "controlled"

    if re.search(r"\b(justice is what|justice arrives|gate closes|canal district)\b", low):
        return _dual_lead(text, "[dismissive]", "[calm]"), "warning"

    if "?" in text and len(text) < 55 and not re.search(r"\b(permit expired|wrong clan)\b", low):
        return _dual_lead(text, "[deadpan]", "[dismissive]"), "dry question"

    if re.search(r"\b(again|of course|naturally|cheeky)\b", low) and len(text) < 50:
        return _dual_lead(text, "[deadpan]", "[chuckles]"), "dry amusement"

    if re.search(r"\b(crane hair|unicorn permit|flexibility\. good)\b", low):
        return _dual_lead(text, "[calm]", "[deadpan]"), "appraising"

    if "..." in text and len(text) > 40:
        return _insert_before_clause(text, "...", "[pause]"), "beat"

    return text, ""


def tag_narrator(text: str) -> tuple[str, str]:
    low = text.lower()

    # Case Five / epilogue romance (untagged batch 2026-06)
    if re.search(r"\b(runner skips breakfast|summons instead|pleasure-quarter seal)\b", low):
        return _dual_lead(text, "[dramatic]", "[pause]"), "case5 summons"
    if re.search(r"\b(travel kosode|patronage runs out|gate guard asks)\b", low):
        return _dual_lead(text, "[tender]", "[pause]"), "case5 packing"
    if re.search(r"\b(open docket hall|wet stone and copied petitions)\b", low):
        return _dual_lead(text, "[dramatic]", "[pause]"), "case5 hall"
    if re.search(r"\b(crane envoy does not stand|letter home to the crane)\b", low):
        return _dual_lead(text, "[pause]", "[dramatic]"), "case5 envoy"
    if re.search(r"\b(envoy exhales once|rival magistrate's colors)\b", low):
        return _dual_lead(text, "[grim]", "[pause]"), "case5 envoy exit"
    if re.search(r"\b(inner office after public ink|locks the corridor)\b", low):
        return _dual_lead(text, "[pause]", "[dramatic]"), "case5 private office"
    if re.search(r"\b(crane purity behind his screen|without asking him to be kinder)\b", low):
        return _dual_lead(text, "[tender]", "[whispers]"), "case5 intimacy"
    if re.search(r"\b(sworn left hand is not a montage|okami nod at her sash)\b", low):
        return _dual_lead(text, "[dramatic]", "[pause]"), "case5 first week"
    if re.search(r"\b(does not say love|does not offer it|week that has only begun)\b", low):
        return _dual_lead(text, "[tender]", "[pause]"), "case5 closing"
    if re.search(r"\b(witness-only paper|discharge instead of appointment)\b", low):
        return _dual_lead(text, "[grim]", "[pause]"), "case5 bad branch"
    if re.search(r"\b(afternoon off the ledger|steam under the kotatsu|mikan peel)\b", low):
        return _dual_lead(text, "[tender]", "[warmly]"), "epilogue kotatsu"
    if re.search(r"\b(passes him a segment|hunger were also classified)\b", low):
        return _dual_lead(text, "[warmly]", "[amused]"), "epilogue mikan"
    if re.search(r"\b(rain ticks the eaves|kotatsu holds their warmth)\b", low):
        return _dual_lead(text, "[tender]", "[pause]"), "epilogue rain"
    if re.search(r"\b(corner of his mouth twitches|not quite a smile)\b", low):
        return _dual_lead(text, "[warmly]", "[amused]"), "epilogue almost-smile"

    if re.search(
        r"\b(teardrop island marina|broken pilings|kobune rocks|bay wind cuts)\b",
        low,
    ):
        return _dual_lead(text, "[pause]", "[dramatic]"), "marina establish"
    if re.search(r"\b(sniffle|whimper|wind-reddened cheeks)\b", low):
        return _dual_lead(text, "[pause]", "[sympathetic]"), "emotional beat"
    if re.search(r"\b(rocking hull|gunwales under his palms|good girl)\b", low):
        return _dual_lead(text, "[whispers]", "[pause]"), "intimate narration"
    if re.search(r"\b(door shuts with finality|ears ring|slows where the lamplight)\b", low):
        return _dual_lead(text, "[pause]", "[dramatic]"), "sharp beat"
    if re.search(r"\b(rain beads on the canal|escort, not comfort|compound swallows)\b", low):
        return _dual_lead(text, "[pause]", "[dramatic]"), "punishment escort"
    if re.search(
        r"\b(carried it out|kept her pride|expired permit waits|lanterns bleed orange)\b",
        low,
    ):
        return _dual_lead(text, "[dramatic]", "[pause]"), "closing beat"
    if re.search(r"\b(folds her hands\. no muttering|magistrate's gate slides)\b", low):
        return _dual_lead(text, "[pause]", "[calm]"), "gentle beat"
    if re.search(r"\b(fireworks|kiss|shoji|blade|custody|saw kerf)\b", low):
        return _dual_lead(text, "[pause]", "[dramatic]"), "investigation beat"
    if "—" in text and len(text) < 95 and len(text) > 30:
        parts = re.split(r"\s[—–]\s", text, maxsplit=1)
        if len(parts) == 2 and not _has_tag(text):
            return f"[pause] {parts[0]} [dramatic] {parts[1]}", "em dash beat"

    return text, ""


def tag_line(
    character: str,
    game_text: str,
    line_id: str = "",
    source: str = "",
) -> tuple[str, str, str]:
    """Return (tts_text, tags_notes, model_hint)."""
    if line_id in MANUAL_OVERRIDES:
        tts = MANUAL_OVERRIDES[line_id]
        notes = "manual override"
    elif character == "toa":
        tts, notes = tag_toa(game_text)
    elif character == "kaoru":
        tts, notes = tag_kaoru(game_text, line_id)
    elif character == "narrator":
        tts, notes = tag_narrator(game_text)
    else:
        tts, notes = game_text, ""

    tts = ensure_min_tags(tts, character, line_id, game_text)
    tts, weave_notes = weave_delivery_tags(tts, character, game_text, line_id, source)
    if weave_notes:
        notes = f"{notes}; {weave_notes}" if notes else weave_notes
    model = "eleven_v3" if _tag_count(tts) > 0 else "eleven_multilingual_v2"
    return tts, notes, model


def count_tags(tts_text: str) -> int:
    return len(re.findall(r"\[[^\]]+\]", tts_text))
