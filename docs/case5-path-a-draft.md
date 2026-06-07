# Case 5 Path A — The Left Hand (御前の帳 / *Seal at the Hearing*)

**Status:** Draft only — **not** wired into `game/*.rpy`.  
**Scope:** Path A (canon public hearing + yoriki appointment + optional private confession route). Paths B/C dropped.  
**Spine:** [plot-guide-five-case-arc.md](plot-guide-five-case-arc.md) · **Voice:** [kaoru-dialogue-style.md](kaoru-dialogue-style.md), [toa-dialogue-style.md](toa-dialogue-style.md)  
**Replaces:** `case5_stub_tease` in `game/case4_5_boat.rpy` (pleasure-quarter seal one-liner tease).

**Canon emotional state (Case 5 entry):** Toa is habituated to live-in intimacy, enjoys sex with Kaoru, and has internalized *toy in the bedroom, something like wife everywhere else* — she will **not** say *wife* aloud yet. Kaoru still speaks in office props; love stays subtext until the optional private beat.

---

## Case 4 bridge changes

### Current flow (`game/case4_investigation.rpy`, `game/case4_5_boat.rpy`)

```
case4_milestone_end
  → case4_closed = True
  → jump case4_post_case4_bridge

label case4_post_case4_bridge:
    if case4_5_boat_interlude_eligible():
        jump case4_5_boat_interlude
    jump case5_stub_tease          # ← REPLACE

label case4_5_boat_bridge:
    …
    jump case5_stub_tease          # ← REPLACE
```

### Replace with

```renpy
label case4_post_case4_bridge:
    if case4_5_boat_interlude_eligible():
        jump case4_5_boat_interlude
    # Optional future slot (not in this draft):
    # if case4_5_cute_interlude_eligible():
    #     jump case4_5_cute_interlude
    jump case5_investigation_start
```

```renpy
label case4_5_boat_bridge:
    …
    jump case5_investigation_start   # not case5_stub_tease
```

**Delete or archive** `label case5_stub_tease` once `game/case5_investigation.rpy` ships; keep `bgm_case5_tease` as hearing-prelude BGM or retag to `bgm_case5_hearing`.

### Optional future — Case 4.5 “cute” interlude

Slot **after** `case4_5_boat_interlude` (or instead of boat when ineligible) and **before** `case5_investigation_start`: low-stakes domestic beat (kotatsu, permit doodle, mikan peel) with **no** new case number. Eligibility TBD — suggest `case4_closed` + `live_in_companion` + not `case4_5_cute_seen`, no bad ends. Exit: `jump case5_investigation_start`.

---

## Acts (Path A)

| Act | Label(s) | Summary |
|-----|----------|---------|
| **1** | `case5_investigation_start` → `case5_false_exit` | Dawn summons; Toa believes dismissal or punishment; pleasure-quarter seal hook as **bait**, not the case spine. |
| **2** | `case5_audition_callback` | Kaoru lists Cases 1–4 in concrete magistrate diction (audition reveal without saying “audition”). |
| **3** | `case5_public_hearing` | Open docket; quarter clerks, Crane envoy pressure, rival magistrate shadow. |
| **4** | `case5_scroll_presentation` | Scroll: **yoriki** appointment; Toa stammers Crane custom (honor guard, clan auditors), not marriage aloud. |
| **5** | `case5_yoriki_menu` | Accept → Path A canon; Refuse → brutal bad-end fork (`case5_bad_end_refusal_warning`). |
| **6** | `case5_private_extra` (optional) | Private chamber; confession cover story; intimacy fade; *toy / not-wife-yet* interiority. |
| **7** | `case5_epilogue_week_one` | Open-ended first week as sworn left hand — files, quarter walk, no “I love you” required. |

**Act count:** 7

---

## Suggested flags (`game/stats.rpy` — implement later)

| Flag | Set when |
|------|----------|
| `case5_started` | Enter `case5_investigation_start` |
| `case5_false_exit_seen` | Act 1 complete |
| `case5_hearing_attended` | Act 3 complete |
| `case5_yoriki_offered` | Scroll shown |
| `case5_yoriki_accepted` | Menu: accept oath |
| `case5_yoriki_refused` | Menu: refuse (bad-end router) |
| `case5_private_confession` | Extra route: admits cover + acceptance |
| `case5_private_intimacy` | Extra route: bedroom fade |
| `case5_closed` | Epilogue return / milestone |
| `seen_gameover_case5` | Refusal bad end viewed (mirror `seen_gameover_case4`) |

**Eligibility (Path A canon):** mirror Case 4.5 — `all_romance_routes_complete()`, `case4_closed`, `case4_kaoru_defended`, `live_in_companion`, `canon_first_scene`, no prior case bad ends. Non-canon / witness-only playthroughs get a shortened **witness discharge** ending (out of scope for this draft; stub label `case5_noncanon_discharge`).

---

## CG art pipeline — suggested filenames

| File | Ren'Py tag (proposed) | Use |
|------|------------------------|-----|
| `cg-case5-false-exit-office.png` | `case5_false_exit_office` | Act 1 — empty desk, seal cord, Toa in travel kosode |
| `cg-case5-hearing-hall.png` | `case5_hearing_hall` | Act 3 — wide dais, crowd, witness line |
| `cg-case5-hearing-kaoru-dais.png` | `case5_hearing_kaoru_dais` | Act 3 — Kaoru gold haori, Emerald seal |
| `cg-case5-scroll-desk.png` | `case5_scroll_desk` | Act 4 — scroll unfurled, hanko dish |
| `cg-case5-yoriki-oath.png` | `case5_yoriki_oath` | Act 5 accept — hands on scroll / witness stand |
| `cg-case5-private-talk.png` | `case5_private_talk` | Act 6 — shoji lit, two-shot, clothes on |
| `cg-case5-bedroom-toy.png` | `case5_bedroom_toy` | Act 6 — tasteful NSFW fade key (silhouette / sheets) |
| `cg-case5-epilogue-week.png` | `case5_epilogue_week` | Act 7 — corridor walk, file under arm |
| `cg-epilogue-romance-kotatsu-intimate.png` | `epilogue_romance_kotatsu_intimate` | Bonus epilogue — kotatsu room, tasteful intimate beat |
| `cg-case5-bad-chained.png` | `gameover_case5_chained` | Bad end: quarter chains (shipped) |
| `cg-case5-bad-quarter-cage.png` | `gameover_case5_quarter_cage` | Bad end: hall cage (shipped) |

**CG count (this draft):** 10 markers (8 canon Path A + 2 bad-end stubs)

---

## Full Ren'Py-style draft — Path A

*Voice IDs are placeholders (`kaoru_5xx`, `toa_5xx`, `narrator_5xx`). Wire manifest after script lock.*

```renpy
# game/case5_investigation.rpy  (DRAFT — do not paste until reviewed)
# Entry: case4_post_case4_bridge / case4_5_boat_bridge
# Path A only. case5_yoriki_refused → case5_bad_end_refusal_warning

label case5_investigation_start:

    $ case5_started = True

    scene bg magistrate_office with dissolve
    play music audio.bgm_case5_tease fadein 1.5 loop volume 0.45
    show kaoru commanding at left
    show toa determined at right

    voice "audio/voice/narrator_500.mp3"
    "Three mornings after the dock's steel went quiet, the runner does not bring breakfast. He brings a summons — ink still wet, pleasure-quarter seal copied twice as if the clerk feared forgery."

    show toa worried
    voice "audio/voice/toa_500.mp3"
    toa "Magistrate-sama — the runner would not meet my eyes. Is the witness line… finished?"

    show kaoru cold
    voice "audio/voice/kaoru_500.mp3"
    kaoru "Witness is a word for provisional paper. Case Five opens at the hour of the serpent. Dress for court, not for my corridor."

    show toa flustered
    voice "audio/voice/toa_501.mp3"
    toa "Court means dismissal. Or punishment. You said when the files closed we would discuss terms—"

    show kaoru smirk
    voice "audio/voice/kaoru_501.mp3"
    kaoru "We are discussing them. In a room that can hear you."

    jump case5_false_exit


label case5_false_exit:

    $ case5_false_exit_seen = True

    # [CG: case5_false_exit_office — dawn office, vacant cushion, Toa clutching witness notes, Kaoru silhouette at door]

    scene bg magistrate_office with dissolve
    show kaoru commanding at left
    show toa worried at right

    voice "audio/voice/narrator_501.mp3"
    "She packs Crane neatness into a travel kosode — the kind one wears when patronage ends and the gate guard asks for paper she no longer has."

    show kaoru cold
    voice "audio/voice/kaoru_502.mp3"
    kaoru "Leave the adjoining chamber at the gate. Today you are witness. The hall does not care what you call last night."

    show toa determined
    voice "audio/voice/toa_502.mp3"
    toa "Then I will attend as your witness one last time. The hall taught me how to stand where I am told."

    show kaoru charm
    voice "audio/voice/kaoru_503.mp3"
    kaoru "Good. The pleasure-quarter seal on this summons is bait for clerks who think Case Five is only Chrysanthemum politics. It is not. Stay in my line."

    scene black with fade
    pause 0.5

    jump case5_audition_callback


label case5_audition_callback:

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 2.0 loop volume 0.42
    show kaoru commanding at center
    show toa determined at left

    voice "audio/voice/kaoru_504.mp3"
    kaoru "Case One — you read a lie under pressure at the Lacquered Plum and did not run when the comb was Scorpion."

    voice "audio/voice/kaoru_505.mp3"
    kaoru "Case Two — you stood on the hill where the city could see you beside my file, and you did not hide behind Crane honor when the kiln ash choked the alley."

    voice "audio/voice/kaoru_506.mp3"
    kaoru "Case Three — you trusted the bolt room when the room tried to kill you. You let me pull you out instead of proving the Academy on splinters."

    if case4_kaoru_defended:
        voice "audio/voice/kaoru_507.mp3"
        kaoru "Case Four — you stayed behind my shoulder when steel wanted you alone. You did not compose poetry on my dock."

    show toa soft
    voice "audio/voice/toa_503.mp3"
    toa "You never said any of that was… an examination."

    show kaoru smirk
    voice "audio/voice/kaoru_508.mp3"
    kaoru "I said provisional attachment until the files close. The files did not close themselves, To-chan."

    show toa flustered
    voice "audio/voice/toa_504.mp3"
    toa "I thought you meant stipend. Permit. A room adjoining yours."

    show kaoru charm
    voice "audio/voice/kaoru_509.mp3"
    kaoru "I meant a left hand. The city requires a name on it. I chose yours before you knew the job title."

    scene black with fade
    pause 0.4

    jump case5_public_hearing


label case5_public_hearing:

    $ case5_hearing_attended = True

    # [CG: case5_hearing_hall — wide magistrate dais, crowd, incense, Toa in witness kosode, Kaoru gold haori at center]

    scene bg hearing_hall with dissolve
    play music audio.bgm_case5_hearing fadein 2.0 loop volume 0.48
    show kaoru commanding at center
    show toa determined at left

    voice "audio/voice/narrator_502.mp3"
    "Ryoko Owari's open docket hall smells of wet stone and copied petitions. Quarter clerks line the left wall; a Crane envoy's crest sits cold on the right. Someone in the back row wears another magistrate's colors without sitting in the seat."

    show kaoru cold
    voice "audio/voice/kaoru_510.mp3"
    kaoru "Kitsu Kaoru, Emerald Magistrate. Case Five: witness chains for the Chrysanthemum root, and appointment of sworn yoriki for ongoing docket."

    show toa worried
    voice "audio/voice/toa_505.mp3"
    toa "Yoriki is— that is police rank. That is… not a dancer's permit."

    # [CG: case5_hearing_kaoru_dais — Kaoru at dais, seal tray, crowd blur, Toa small at witness rostrum]

    show kaoru commanding
    voice "audio/voice/kaoru_511.mp3"
    kaoru "Witness is not enough in this city. You signed my corridor, my cushion, my release. The quarter whispers kept woman. The file will say office."

    voice "audio/voice/narrator_503.mp3"
    "The Crane envoy does not stand. His silence is its own letter to Shiro no Yogen."

    jump case5_scroll_presentation


label case5_scroll_presentation:

    $ case5_yoriki_offered = True

    # [CG: case5_scroll_desk — appointment scroll, Emerald wax, yoriki characters legible, hanko dish foreground]

    scene bg hearing_hall with dissolve
    show kaoru commanding at center
    show toa flustered at left

    play sound audio.paper_shuffle volume 0.5
    voice "audio/voice/kaoru_512.mp3"
    kaoru "Kakita Toa. Appointment as yoriki to the Emerald office of Ryoko Owari. Witness chains, quarter escort, left-hand signature on my docket."

    show toa determined
    voice "audio/voice/toa_506.mp3"
    toa "Magistrate-sama — Crane custom expects… marriage negotiation. Honor guard. Not— not a magistrate's toy at a public desk."

    show kaoru smirk
    voice "audio/voice/kaoru_513.mp3"
    kaoru "You already served the desk. You slept behind my screen. You argued well when I preferred competence within reach."

    show kaoru charm
    voice "audio/voice/kaoru_514.mp3"
    kaoru "This is office. I am not asking for poetry. I am asking for a name the city can cite when the seal walks."

    menu case5_yoriki_menu:
        "Accept the oath — left hand on the scroll.":
            $ case5_yoriki_accepted = True
            jump case5_yoriki_accept

        "Refuse — I am a Crane dancer, not your property.":
            $ case5_yoriki_refused = True
            jump case5_bad_end_refusal_warning


label case5_yoriki_accept:

    # [CG: case5_yoriki_oath — Toa's hand on scroll edge, Kaoru's hanko poised, crowd out of focus]

    scene bg hearing_hall with dissolve
    show kaoru satisfied at center
    show toa soft at left

    play sound audio.seal_stamp volume 0.6
    voice "audio/voice/toa_507.mp3"
    toa "I accept the appointment and its duties. You will have my discretion and my attendance."

    show kaoru charm
    voice "audio/voice/kaoru_515.mp3"
    kaoru "You passed every case I put in front of you. Do not make me say it twice in front of clerks who sell courage by the cup."

    show toa flustered
    voice "audio/voice/toa_508.mp3"
    toa "I will not embarrass your file."

    voice "audio/voice/narrator_504.mp3"
    "The envoy exhales once — calculation, not blessing. The rival magistrate's colors leave before the wax cools."

    menu case5_post_oath_menu:
        "Sign and follow him to the inner office tonight.":
            jump case5_private_extra

        "Sign and return to the witness chamber — boundaries until he sends for you.":
            jump case5_epilogue_week_one


label case5_private_extra:

    $ case5_private_confession = True

    scene bg magistrate_office with dissolve
    play music audio.bgm_office fadein 2.0 loop volume 0.38
    show kaoru charm at left
    show toa soft at right

    # [CG: case5_private_talk — shoji lit from corridor, two-shot seated, tea untouched, formal kosode still on]

    voice "audio/voice/narrator_505.mp3"
    "The inner office after public ink is smaller than the hearing hall. He locks the corridor himself — no runner, no cushion joke."

    show kaoru commanding
    voice "audio/voice/kaoru_516.mp3"
    kaoru "You may speak ...without the docket listening. One sentence you did not file. One sentence is missing from your testimony"

    show toa worried
    voice "audio/voice/toa_509.mp3"
    toa "Although I needed the permit to stay close, I chose to stay on purpose. I could have ran. And then you could have caught me."

    show kaoru smirk
    voice "audio/voice/kaoru_517.mp3"
    kaoru "...I know."

    show toa determined
    voice "audio/voice/toa_510.mp3"
    toa "You are not easy."

    show kaoru charm
    voice "audio/voice/kaoru_518.mp3"
    kaoru "Most try to rename me. You laid on your back and still came back to the desk."

    show toa flustered
    voice "audio/voice/toa_511.mp3"
    toa "In the bedroom I can be your toy. Out there— I want… I want to stand beside you."

    show kaoru satisfied
    voice "audio/voice/kaoru_519.mp3"
    kaoru "Then stand. The oath is public. The rest is mine to file when you stop stammering."

    menu case5_private_intimacy_menu:
        "Come to the screen — tonight is his, not the city's.":
            $ case5_private_intimacy = True
            jump case5_private_intimacy_fade

        "Bow at the threshold — oath enough for one day.":
            jump case5_epilogue_week_one


label case5_private_intimacy_fade:

    scene black with fade
    pause 0.6

    # [CG: case5_bedroom_toy — tasteful NSFW: silk screen silhouette, disordered futon, gold haori folded on chest, no graphic detail]

    voice "audio/voice/narrator_506.mp3"
    "She does not perform Crane purity behind his screen. She performs hunger honestly — the kind that does not ask him to be kinder, only present."

    voice "audio/voice/toa_512.mp3"
    toa "Magistrate-sama— still yours."

    voice "audio/voice/kaoru_520.mp3"
    kaoru "Still mine. That is the only title that matters tonight."

    scene black with fade
    pause 1.0

    jump case5_epilogue_week_one


label case5_epilogue_week_one:

    $ case5_closed = True

    # [CG: case5_epilogue_week — morning corridor, Toa with yoriki sash over kosode, file under arm, Kaoru ahead without looking back]

    scene bg magistrate_office with dissolve
    play music audio.bgm_street fadein 2.0 loop volume 0.4
    show kaoru commanding at left
    show toa determined at right

    voice "audio/voice/narrator_507.mp3"
    "Week one of the sworn left hand is not a montage of victory. It is runners, copied seals, a quarter walk where the okami nod at her sash instead of her obi."

    show kaoru cold
    voice "audio/voice/kaoru_521.mp3"
    kaoru "File the witness chain before noon. The Chrysanthemum root still has tendrils in the pleasure quarter."

    show toa soft
    voice "audio/voice/toa_513.mp3"
    toa "Yes, Magistrate-sama. The line is written — and I am still at your door."

    show kaoru charm
    voice "audio/voice/kaoru_522.mp3"
    kaoru "Good. Case Five is pinned, not closed. The city still lies."

    voice "audio/voice/narrator_508.mp3"
    "She does not say love. He does not offer it. Ryoko Owari has a name on his left hand — and a week that has only begun."

    return


# --- BAD END: refusal (shipped; see docs/case5-bad-end-brutal.md) ---

# Flow: case5_bad_end_refusal_warning → CW menu → case5_bad_end_refusal_choice
#   → case5_bad_end_refusal_chained | case5_bad_end_refusal_cage
#   → gameover_case5_chained | gameover_case5_quarter_cage (CG-held climax, pause 2.0 beats)
# Flags: case5_closed, case5_yoriki_refused, seen_gameover_case5
# Art: cg-case5-bad-chained.png, cg-case5-bad-quarter-cage.png (PNG TBD)
```

---

## Implementation notes (post-draft)

1. **New bg:** `bg hearing_hall` — use `cg-case5-hearing-hall.png` as establishing bg until dedicated tile exists (mirror Case 4 `dock_raid` pattern).
2. **Audio:** add `bgm_case5_hearing`, `audio.seal_stamp`; extend [elevenlabs-music-prompts.md](elevenlabs-music-prompts.md).
3. **Gallery:** Case 5 group + `gameover_case5_*` locked slots; bad ends content-warning pattern from `case4_bad_end_toa_slain_warning`.
4. **Dev jump:** `$ case4_closed = True` + `all_romance_routes_complete()` flags → `jump case5_investigation_start`.
5. **Noncanon:** `case5_noncanon_discharge` — witness thanked, no scroll (separate doc).

---

## Quick reference

| Item | Value |
|------|-------|
| **Doc path** | `docs/case5-path-a-draft.md` |
| **Acts** | 7 |
| **CG markers** | 10 (8 canon + 2 bad-end stubs) |
| **Primary flags** | `case5_yoriki_accepted`, `case5_private_confession`, `case5_private_intimacy`, `case5_closed` |
