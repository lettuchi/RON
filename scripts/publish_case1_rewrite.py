#!/usr/bin/env python3
"""Publish case1 conversational rewrite: sidecar + .rpy from baseline + overrides."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "docs" / "script-rewrite-2026-06-04" / "_case1-baseline.json"
SIDECAR = ROOT / "docs" / "script-rewrite-2026-06-04" / "case1-updates.json"
PERF = ROOT / "scripts" / "voice_performance_manifest.json"

# Hand-polished lines (id -> game_text). Merged over baseline polish.
OVERRIDES: dict[str, str] = {
    "narrator_060": "The stair behind the inner screen swallows every footfall. Dust has crept into Toa's hakama, and the ledger under her arm smells of river damp and ink old enough to flake.",
    "toa_102": "Case One. No bells on me, obijime still dry, and I never let go of the ledger. Small victories, for once.",
    "narrator_061": "Lantern light finds her at the top step. The noble quarter corridor seems to narrow the moment she sees a magistrate standing in it, already waiting.",
    "kaoru_118": "You took long enough. Set the docket on my desk and try not to breathe on the wax seals.",
    "toa_103": "You said archive dust was acceptable. I assume my breathing counts too.",
    "narrator_271": "She climbs back from the archive with the canal docket hugged to her chest. No adjoining chamber waits beside his office, only four more files stacked behind Case One, and one week to prove she belongs to any of them.",
    "toa_104": "Docket retrieved. Still breathing.",
    "kaoru_333": "Still insolent. Desk. Case One first. The other four will find you if you don't flee to the curry shops first.",
    "narrator_063": "Kaoru breaks the outer seal. Inside: watch reports, a charcoal sketch of the recovery site, and a name line left blank until someone puts a face to the dead.",
    "toa_278": "I unpacked for patronage. You're handing me a corpse.",
    "kaoru_330": "Patronage keeps you in my corridor. Case One opens on my desk, first of five you'll witness before this week ends.",
    "toa_280": "Witness attachment. Five files. You never led with that number.",
    "kaoru_334": "You wanted the hall. Case One opens first. Four more follow if you don't bore me or bolt for the curry shops.",
    "kaoru_120": "Case One. A body in the canal at first light. Noble quarter, where the water runs clean enough to mirror gold leaf.",
    "kaoru_121": "The watch writes drowning whenever the name line stays empty. You'll learn which boxes they'll sign, and which they won't.",
    "toa_105": "Clean water, dirty ledger. Who pulled him out?",
    "kaoru_122": "Night watch. Fishermen who swore they saw nothing. And the Scorpion quarter upstream pretends the current runs backward.",
    "narrator_064": "He taps the sketch: a narrow cut between warehouses, rope marks scored into the stone, no blood in the water worth mentioning.",
    "kaoru_123": "The victim wears Miya colors under a borrowed haori. Retainer's knot. Someone wanted him found. Someone else wanted him lost.",
    "toa_106": "Miya means Crane politics. Crane politics means you, Magistrate-sama.",
    "kaoru_124": "Which is exactly why you sleep in the room beside my office. Discretion isn't decoration.",
    "toa_107": "Escort to the canal. Written terms. I'm here to collect.",
    "kaoru_125": "You'll collect at the waterline. First.",
    "kaoru_126": "Which is why you're not sleeping in my hall yet. Prove you can witness a thing without selling it to the curry shops.",
    "toa_108": "I came back. That has to count for something.",
    "kaoru_127": "It counts toward the canal. It does not count toward trust.",
    "narrator_065": "A bag of rice crackers sits on the desk corner. Her indulgence, his allowance.",
    "toa_109": "Snacks after paperwork. Even for corpses nobody's going to bury.",
    "kaoru_128": "Eat one now. You'll lose your appetite before we reach the water.",
    "toa_110": "Retainer's knot, tied left-handed. Haori two sizes too wide, borrowed. No wallet, no letter case.",
    "kaoru_129": "Good. The watch wrote drowning and missed half of what you just said.",
    "narrator_066": "In the margin, a clerk noted the fingernails: scrubbed clean the night before. Labor without the honest dirt that should come with it.",
    "toa_111": "So who profits when a Crane thread snaps in Scorpion current?",
    "kaoru_130": "Opium ledgers. Marriage contracts. Anyone in this city who sells silence by the barrel.",
    "kaoru_131": "You will not say any of that aloud at the canal. Watch faces instead.",
    "toa_112": "Witness notes only: recovery time, position, clothing, visible wounds. Theories can wait.",
    "kaoru_132": "Good. Notes I can file without crossing out half your adjectives.",
    "kaoru_133": "Try keeping that posture once the smell reaches you.",
    "narrator_067": "They leave through the inner hall, not the public corridor where Toa once wandered lost. Guards nod to Kaoru. They look straight through Toa, like furniture that learned to walk.",
    "toa_113": "Furniture with legs still memorizes the route.",
    "kaoru_134": "See that you do. Night calls won't wait for someone to light the lanterns.",
    "narrator_068": "Ryoko Owari wakes around them: cart wheels, a shamisen somewhere distant, sweet smoke from a vial house two alleys over. The canal cut is still half a district off.",
    "kaoru_135": "Watch the eaves. Thieves in the noble quarter work for employers, not hunger.",
    "toa_114": "And the wrongness in the air? Thin, like someone peeled a ward off the wall and left bare paper behind.",
    "kaoru_136": "Wrong-colored water usually means a clerk poured something upstream. Check the eaves before you blame charms.",
    "narrator_069": "A crow watches from a warehouse sign, three painted eyes that aren't quite Imperial and aren't quite Scorpion. It takes wing the instant Kaoru glances up.",
    "narrator_070": "The canal runs black-green under morning cloud, greener than honest water, as if someone dissolved a charm and tipped the dregs downstream. Rope burns scar the stone where watchmen hauled the body up.",
    "narrator_071": "No crowd. Only a clerk with a wax tablet, and a Miya envoy pretending to read the warehouse sign so he won't have to look at the pallet.",
    "kaoru_137": "To-chan. Stand where I point you, and don't touch the water.",
    "toa_115": "Point, then. I'll witness.",
    "narrator_072": "The covered pallet lies at the canal's lip, cloth still damp. When the clerk folds back the sheet, a young man's face shows, peaceful in entirely the wrong way, as if his sleep had been negotiated rather than earned.",
    "toa_116": "He looks borrowed, even now.",
    "kaoru_138": "Identification first. Gossip a distant second. Mourning never.",
    "toa_117": "Haori upstream, body down here. Current, or carriage?",
    "kaoru_139": "Ask the river once you're qualified to. Until then, observe.",
    "toa_118": "Palms soft until yesterday, ink on the index finger. Ledger work. Sleeve hem eaten by canal slime from upstream, not from here.",
    "kaoru_140": "Which means he died somewhere else, then was dressed for display.",
    "toa_119": "Magistrate-sama, the bruising on his throat is shaped like fingers, not water.",
    "kaoru_141": "Because drowning keeps the taxes calm. You'll learn when to write only what the city can swallow.",
    "kaoru_142": "And when to make me swallow the harder truth instead. Not today.",
    "toa_120": "Witness note: recovery at canal mark three, noble quarter. Clothing as listed. Cause of death pending magistrate review.",
    "kaoru_143": "Boring. Useful. The clerk can sign that without fainting.",
    "kaoru_151": "Summarize it. One sentence. If I say your words back to the Crane envoy, does he flinch or laugh?",
    "toa_124": "Dressed for display after he died. Borrowed haori, wrong water. A message meant for Crane eyes.",
    "kaoru_152": "Good. You sound like you belong in my hall, the moment you stop performing for corpses.",
    "kaoru_153": "Bold. Don't mistake my attention for approval.",
    "toa_125": "Recovery at mark three. Clothing as listed. Cause of death pending your review, Magistrate-sama.",
    "kaoru_154": "Safe. The envoy won't laugh. He won't fear you either.",
    "toa_126": "You asked me to observe. I did. If you wanted theater, you should have left the bells on me in the archive.",
    "kaoru_155": "There she is. Keep that spine when the Miya registry clerks start smiling at you.",
    "kaoru_156": "A witness without a seal is gossip. Learn faster.",
    "narrator_073": "Near the rope post, something lacquered catches lantern glare, wedged in the seam where oil and wrong-colored water meet.",
    "toa_121": "A comb. Scorpion mon inlaid. Not Miya.",
    "kaoru_144": "Don't touch it with bare hands.",
    "narrator_074": "He wraps it in wax cloth himself, eyes never leaving the eaves, and hands it to Toa only long enough for her seal on the chain-of-custody line.",
    "kaoru_145": "Scorpion comb in Crane water. Bag it for custody. Don't compose metaphors over my desk.",
    "kaoru_146": "Borrowed haori, foreign comb. Someone staged a message for Crane eyes. Put a name on that blank line.",
    "kaoru_147": "The comb goes to the office. The name goes on the line. You walk beside me, not a step ahead.",
    "narrator_075": "The clerk lifts the separate haori from a dry crate. Wax inside the lining has melted, but the inner fold still holds a courier's chit, half legible under river stain.",
    "toa_127": "Miya Jiro. Guest-house ledger clerk. Deliver before third bell. That's a name now, not rumor.",
    "kaoru_157": "Jiro handled Crane correspondence for the noble-quarter guest house. Someone killed the clerk and still kept the appointment.",
    "kaoru_158": "You wanted a theory. Now you've got a face to hang it on. Don't gloat at the envoy.",
    "kaoru_159": "Still standing. Still useful. Copy the chit before the ink flakes.",
    "kaoru_160": "Write it clean. The watch will keep signing drowning until I stop letting them.",
    "narrator_076": "The Miya envoy finally looks up from the warehouse sign. He sees the chit in Kaoru's hand and suddenly remembers urgent business elsewhere.",
    "narrator_077": "Back among cedar and ink, the Scorpion comb sits in a lacquer tray like a poisonous jewel. Beside it, Kaoru inks {i}Miya Jiro{/i} onto the line the watch left blank.",
    "kaoru_148": "Tomorrow we cross the Miya guest registry against Scorpion shipping rolls. One of them flinches the moment Jiro's name is said aloud.",
    "toa_122": "Guest-house clerk, Crane thread, Scorpion comb. Someone staged a whole poem and forgot it would have an audience.",
    "toa_128": "We've got a name now, and a sender vain enough to leave his comb behind. That's a thread worth pulling.",
    "kaoru_149": "Eat. Then copy the watch testimony twice: once for the Empire, once for what I actually believe happened.",
    "kaoru_150": "Eat, if you must. Then copy testimony until your hand cramps. Then we'll discuss whether you've earned another week here.",
    "toa_123": "Case One has a face now. Jiro. I won't forget him.",
    "narrator_078": "Morning again, and the docket has grown teeth overnight. Beside Jiro's name Kaoru pinned a second sheet: the Miya guest house, the Lacquered Plum, where a dead clerk once kept other men's appointments.",
    "narrator_079": "Rain reaches the licensed quarter first. It beads on paper lanterns the color of old wine and runs the canal black between teahouses that sell forgetting by the hour.",
    "narrator_080": "The Lacquered Plum leans over the water on cedar stilts. A three-eyed crow, the same painted sign or a cousin of it, watches from the gable. This time it does not fly.",
    "narrator_081": "Inside: lamplight and face powder. The okami kneels behind a low desk stacked with appointment books, smile fixed hard as lacquer, eyes already tallying the cost of a magistrate's boots on her tatami.",
    "narrator_082": "Kaoru sets the wax-wrapped comb on the desk and folds the cloth back. The okami's painted calm cracks, just a hairline.",
    "narrator_083": "But Toa has already slipped past the desk the kitchen way: servant's bow, easy warmth of a woman who carried tea in worse rooms. A young geisha looks up from folding a dead man's spare haori.",
    "narrator_084": "The okami's smile finally fails. In the corner a girl, a geisha, young, eyes red-rimmed, flinches under the weight of his voice.",
    "narrator_085": "The geisha rises. Perhaps nineteen, white makeup cried through at the edges. She bows too low, the way frightened people do once they've already decided to be brave.",
    "narrator_086": "Kaoru tilts the wrapped comb toward the lamp. Suzu goes the color of her own face powder.",
    "narrator_087": "She's already decided Toa is safe. The kitchen bow bought what no seal could. Her words come in a rush, like water finding the crack it wanted.",
    "narrator_088": "She watches Toa's hands, not her face. Slowly, fear loosens its knot.",
    "narrator_089": "The girl's hand flies to her own throat. The gesture answers before her voice can.",
    "narrator_090": "Kaoru says nothing. He simply waits, and the room shrinks around his stillness until the okami's powder runs and Suzu's resolve breaks, all under a magistrate who hasn't yet bothered to threaten her.",
    "narrator_091": "The okami surrenders the high-tide registry the way a gambler gives up a marked card: slowly, watching the door the whole time. Kaoru turns to the night Jiro died.",
    "narrator_092": "The booking is authorized in red: a private-room writ, the kind the licensed quarter demands of the magistracy to seal a room against the watch. The wax bears the Emerald mon.",
    "narrator_093": "The screen slides open without a knock. A man in Scorpion grey steps in from the rain, trade factor by his ink-stained cuffs and the easy menace of someone used to buying magistrates by the dozen.",
    "narrator_094": "The factor's hand drifts toward his sleeve. Kaoru doesn't move at all, and somehow that's worse than if he had.",
    "narrator_095": "The factor's composure thins. A spoken record, in a house full of witnesses, is much harder to drown than a single clerk.",
    "narrator_096": "The factor weighs it all: the room, the spoken record, the unmoving magistrate. Then he bows to the exact depth that insults without inviting a blade, and withdraws into the rain.",
    "narrator_097": "The screen slides shut. Suzu lets out a breath she's held since he entered. The okami has already started deciding which version of tonight she'll sell, and to whom.",
    "narrator_098": "Back among cedar and ink, the case finally has a shape. On the lacquer tray: the Scorpion comb, Suzu's name, and, depending on the night, a forged Emerald writ or its careful copy.",
    "narrator_099": "He crosses the office and stops too close: practiced proximity of a man who has decided the distance between you is his to set.",
    "narrator_052": "Morning in the noble quarter tastes of ink and cedar. The thirtieth is still the date on her permit, but Toa is already at the threshold with tea and a borrowed case file.",
    "toa_067": "The permit says I'm legal on the thirtieth. I'm early with tea and a case file.",
    "kaoru_081": "Early is still obedience. Sit before you spill something on my docket.",
    "narrator_053": "He gestures to the cushion on the tatami in front of the desk, the same spot where he made her sit for her audition.",
    "toa_068": "Snacks after paperwork. That's still the order of operations, isn't it?",
    "kaoru_082": "We'll see if your appetite survives what I'm about to read you aloud.",
    "kaoru_083": "Bring that audience-of-one energy to the docket. Cases bore me less when you perform.",
    "toa_070": "Then I'll save the bells for evidence review.",
    "kaoru_091": "You danced like a maiden at a shrine. Try not to curtsey at a corpse.",
    "toa_078": "I'll manage, Magistrate-sama. I know the difference.",
    "toa_079": "Honored Magistrate-sama, shall I pour the tea before the terms you mentioned on the thirtieth, or after?",
    "kaoru_092": "After. And stop bowing at every clause. My neck aches just from watching you.",
    "toa_080": "You said we'd discuss residency. So I'm listening.",
    "kaoru_093": "Good. Plain speech spares us both another fan dance.",
    "kaoru_321": "I like you. Enough that I want to keep you around.",
    "narrator_054": "He slides a stack across the desk. Not her permit book this time, but office stationery stamped with the Emerald crest.",
    "kaoru_094": "You may keep the guest room until the date takes effect. That was courtesy, not a loophole.",
    "toa_081": "A guest room. A preview. You really do enjoy making people come back, don't you.",
    "kaoru_161": "The signature was always going to bring you back. I merely wrote out the appointment you'd earned.",
    "narrator_055": "The top sheet is titled {i}Appointment of Live-In Companion (Patronage of Artistic Residence){/i}. Her name is already inked there, in his hand.",
    "toa_082": "Live-in companion. That's not a guest room preview. That's a contract.",
    "kaoru_095": "Companion duties: attend the magistrate, carry messages, witness interviews, keep discretion, remain on the premises unless I release you. Your art is why the treasury pays. Not the excuse.",
    "kaoru_096": "You'll take meals in the inner hall. You'll sleep in the chamber adjoining my office. You'll answer when I call, day or night.",
    "toa_083": "Day or night. You ask a great deal, Magistrate-sama.",
    "kaoru_097": "It sounds like law because it is. Ryoko Owari doesn't grant interclan residence to dancers who vanish after sunset.",
    "narrator_056": "He taps a second page: stipend figures, duty rotations, and a line for her seal beside his.",
    "toa_084": "And the stipend?",
    "kaoru_098": "Three koku monthly, plus board. Official gifts to support your expression. The treasury won't call you a kept performer so long as the ledger says patronage.",
    "toa_085": "Three koku is more than the curry shop ever paid me to smile at tourists.",
    "kaoru_099": "Then you understand the bargain. Sign it, or go back to Unicorn roads and expired paper.",
    "kaoru_100": "You already proved you can close a proposition in this room. Don't pretend shock suits you.",
    "toa_086": "Shock and delight, both at once. You do that to me.",
    "toa_087": "Magistrate-sama, I accept the appointment and its duties. You'll have my discretion and my attendance.",
    "kaoru_101": "Better. You almost sound like you belong behind my desk, instead of on it.",
    "toa_088": "I'll sign once we've defined release, and settled which nights are mine for Academy correspondence.",
    "kaoru_102": "Bold, for someone who still smells of my cedar shelves.",
    "kaoru_103": "Academy letters wait on the outer desk. You don't leave this compound without escort until Case One closes. Those are the terms.",
    "toa_089": "Escort, not a leash. I can live with that.",
    "kaoru_104": "You'll work with what I give you. Now sign.",
    "toa_090": "Three koku. Fine. Wonderful, I'll frame the ledger. But Magistrate-sama, I want the room. I want the hall. I want to be here.",
    "toa_091": "That came out louder than was professional.",
    "kaoru_105": "Honest, at last. The treasury pays you regardless. Try not to grin at the clerk.",
    "narrator_057": "She takes up the brush. Her seal meets his: waxless, official, irrevocable until he says otherwise.",
    "kaoru_106": "Effective on the thirtieth, as written. Until then, you're mine to schedule, starting with Case One.",
    "toa_092": "Case One it is. Files, witnesses, and snacks for the road.",
    "kaoru_107": "You'll fetch the docket from the inner archive. Then you'll learn how this city buries its dead without funerals.",
    "toa_093": "I'll fetch it. I'll learn it. Just... thank you. For the room next to yours.",
    "kaoru_108": "Thank me with a dry ledger, not with your mouth. Archive stairs. Now.",
    "toa_094": "Archive. Escort. Written terms. I'm holding you to all three.",
    "kaoru_109": "Hold the lantern instead. You'll want both hands free on those steps.",
    "toa_095": "Understood. I'll be back with the docket and a dry obijime.",
    "kaoru_110": "Leave the bells behind. This case is not a stage.",
    "toa_096": "Point me to the chamber. I'd rather unpack before the archive swallows me whole.",
    "kaoru_111": "Past the inner screen, down the left corridor. Don't rearrange my shelves.",
    "toa_097": "I only peeked the once. And you noticed.",
    "kaoru_112": "I notice everything. Unpack after the docket, not before.",
    "toa_098": "Archive first. You'll know I'm serious when I come back covered in dust.",
    "kaoru_113": "Left stair, behind the screen. Archive dust on your hakama is acceptable. Just don't drop the ledger.",
    "toa_099": "Case One, the archive, and look, your cup's already empty. Companion duty starts now.",
    "kaoru_114": "Refill it. Then the archive. Then unpack. In that order, or I'll date your next permit forward again.",
    "toa_100": "Cruel. And fair. The cup first, then.",
    "kaoru_328": "Five matters on my slate this week. Companion ink puts you on my witness docket for all of it, Case One through Five. Survive all five, or the quarter eats your stipend.",
    "toa_277": "The permit was for dance. Patronage. A room behind your screen, not five corpses in rotation.",
    "kaoru_329": "Dance bought you the corridor. Cases buy your keep. Competence within reach, that's what I want. Archive stairs, Case One ledger, before the watch blanks the line.",
    "narrator_270": "He files witness attachment the way clerks file tax. Her whole week is already columned on his desk, and he never once said yoriki.",
    "narrator_058": "The inner screen slides open. Beyond it, the stairs smell of old paper and river damp: the archive, where Case One waits.",
    "kaoru_115": "When you come back, we open the file on the canal body. No audience. No bells. Only answers.",
    "toa_101": "Snacks after paperwork. The rule still holds, even for corpses without funerals.",
    "kaoru_116": "Bring rice crackers. I'll allow one indulgence before the city disappoints you.",
    "toa_071": "Case file, tea, and, if I've been very good, a rice cracker. Ready when you are.",
    "kaoru_331": "Correction: five matters on my slate this week. Witness attachment only. Case One through Five. No companion seal on this timeline.",
    "toa_279": "You sold me a permit renewal. Not a whole magistrate's season.",
    "kaoru_332": "Seasons are what I assign. Fetch Case One from the archive. Survive the week, and then we'll discuss whether you sleep in my hall.",
    "kaoru_085": "You came back. I noted that.",
    "toa_072": "The permit still expires. Some of us actually read the dates.",
    "kaoru_086": "You still flinch when I reach for the cup. Don't, next time.",
    "toa_073": "Progress would be signing without all the games.",
    "kaoru_087": "You negotiated once. We'll see if you learned anything.",
    "toa_074": "I learned that you drink water when you're impressed.",
    "toa_075": "I also learned your terms shift. So Case One gets its terms in writing.",
    "kaoru_088": "Ambitious. Now fetch the file.",
    "kaoru_089": "You asked me for remedies once. Case One is your audition for belonging here.",
    "toa_076": "Then watch closely. Audience of one.",
    "kaoru_090": "No curry shop tonight. Just work.",
    "toa_077": "Fine. But I'm billing you for the snacks.",
    "narrator_059": "A live-in companion appointment waits in draft on his desk: unsigned, unoffered on this timeline. Case One opens without the patronage seal.",
    "kaoru_117": "Fetch the canal docket from the archive. We'll discuss residency once you've survived the week.",
}


def load_tts_helper():
    spec = importlib.util.spec_from_file_location(
        "gen", ROOT / "scripts" / "generate_case1_sidecar.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.make_tts


def main() -> int:
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    baseline_by_id = {r["id"]: r for r in baseline}
    perf_by_id = {
        e["id"]: e
        for e in json.loads(PERF.read_text(encoding="utf-8"))["entries"]
    }
    make_tts = load_tts_helper()
    rows_out = []
    for vid, new in sorted(OVERRIDES.items()):
        row = baseline_by_id.get(vid)
        if not row:
            continue
        char = row["character"]
        old_rpy = row["game_text"]
        old_manifest = perf_by_id.get(vid, {}).get("game_text", "")
        if new == old_rpy and new == old_manifest:
            continue
        rows_out.append(
            {
                "id": vid,
                "character": char,
                "game_text": new,
                "tts_text": make_tts(char, vid, new),
            }
        )
    SIDECAR.write_text(json.dumps(rows_out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(rows_out)} rows to {SIDECAR}")

    by_id = dict(OVERRIDES)
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from apply_case1_rpy_from_sidecar import FILES, patch_file

    for path in FILES:
        n, _ = patch_file(path, by_id)
        print(f"patched {path.name}: {n} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
