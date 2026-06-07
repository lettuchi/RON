# Prologue — Alternative Long Draft (dialog only)

**Status:** Review draft · **not wired** into `script.rpy` or shipped prologue  
**Target implementation label prefix:** `alt_prologue_*` (gate behind menu later; see § Fork)  
**Bad endings:** Unchanged — still `jump prologue_refuse_bad_end`, `jump prologue_walkout_ending`, `jump gameover_rain` from shipped `game/prologue.rpy`

---

## Design note (sources)

**From “Lost in the Magistrate's Office”** (screenshots / `docs/first-scene-analysis.md`, IC 03/26–03/27): corridor disorientation, *Done complaining?*, formal knock and *sochira-no-kata*, expired permit and Unicorn failure, social vacuum (inn, pony, curry), cushion and water cup, *Impress me* / office dance with obijime bells, withheld signature, wrist grab, slow clap, chair cliffhanger **Unless?** — structure and choice beats match `game/prologue.rpy`.

**From “Very much not lost in the Magistrate's Office”** (`docs/discord-threads-raw.md`, IC continuation Apr 2025): enthusiastic submissive Toa (*Magistrate-sama*, smiles through rough play), Kaoru’s possessive voice (*To-chan*, *good girl*, command and praise), escalation past the chair, aftercare (water cup, *too cute to splash*), curiosity about his day, **sponsorship-not-danna** framing (*art donor to artist*, *I know what I am paying for*), twice-weekly palace suite — tone and relationship beats, **not** verbatim explicit RP in the VN script.

**Versus current tame canon** (`game/prologue_canon_encounter.rpy`): single fade-to-black, signing and +3-day date only; sponsorship speech deferred to `case1_companion_offer`. This alt draft **extends the canon night** with Discord aftercare and contract foreshadowing, then **still** ends on forward-dated permit and `prologue_case1_hook` → Case 1 (companion scene carries full live-in paperwork).

**Content note:** R-rated sensual dialogue and stage direction; fade before graphic detail (otome/L5R). Bracketed `[DISCORD]` comments flag beats to tune when implementing CGs.

---

## Fork (future implementation)

```renpy
# TODO (script.rpy or prologue_start): menu once art/voice ready
# menu:
#     "Standard prologue (shipped)":
#         jump prologue_start
#     "Extended prologue (alt draft)":
#         jump alt_prologue_start
```

Shipped bad-end and non-canon branches: **re-use existing labels** from `prologue.rpy` (no rewrite in this draft).

---

# ACT I — Lost in the noble quarter

### `alt_prologue_start`  
**Scene:** `bg corridor` · BGM corridor · SFX footsteps

**Narrator:** Lantern light pools on polished floorboards. Every sliding door looks the same — same cedar smell, same hush, same illusion that the magistrate’s complex was designed by someone who hated dancers.

**Narrator:** Toa clutches her permit book and hanko case. She has turned three corners that should not connect and found herself facing a wall with a Lion mon she does not recognize.

**Toa:** I was sure the clerk said third hall, fourth door on the left. Or was it the right?

**Narrator:** Post-gempukku, Unicorn roads still live in her legs — but Crane paperwork lives in her nightmares. Somewhere behind these walls, someone holds the seal she needs before the gate guards decide she is a rumor.

**Toa:** One more corridor. Then I ask nicely. Very nicely.

**Narrator:** She passes a junior clerk carrying a stack of bound reports. He does not look up. Ryoko Owari teaches everyone to mind their own scrolls.

**Toa:** *(quietly)* Snacks first was the plan. Justice second. I may have reversed them before I found this building.

---

### `alt_prologue_wrong_door`  
**Scene:** door opens · Kaoru sprite cruel · BGM Kaoru theme

**Kaoru:** Done complaining?

**Toa:** I wasn’t— That is, I apologize for the disturbance, sochira-no-kata!

**Kaoru:** Wrong door. Again.

**Narrator:** The door shuts with finality. Toa’s ears ring. Somewhere inside, paper rustles — someone who does not suffer fools or lost Crane.

**[CHOICE — reuse `prologue_door_menu` in shipped file]**

---

### `alt_prologue_formal_knock`  
**Scene:** `bg magistrate_office` · sliding door · office BGM

**Narrator:** *(if waited quietly)* Toa kneels at the threshold and strikes the frame once — crisp, patient.

**Kaoru:** *(if waited)* Enter. You can knock when you want something. Try standing still next.

**Narrator:** *(else)* Toa kneels and strikes twice — measured, Crane-trained.

**[CHOICE — reuse `prologue_formality_menu`]**

**Kaoru:** Emerald Magistrate Kitsu Kaoru. You will use my title if you wish to leave with a seal.

**Toa:** Forgive me — Emerald Magistrate.

**Kaoru:** State your business. Briefly.

**Toa:** Kakita Toa, dancer of the Kakita family. New to Ryoko Owari.

**Toa:** Post-gempukku, traveling from Unicorn lands. I mean to establish residence and perform legally.

**Kaoru:** Crane hair, Unicorn permit dates. Wrong clan for this desk — wrong week to fix it.

**Toa:** The roads taught me flexibility. The Crane taught me posture.

**Kaoru:** Posture on the cushion. We'll see if your feet match your bow.

**Narrator:** On the wall behind him, an Emerald chrysanthemum hangs where a Crane mon might have been — jurisdiction made decoration.

---

# ACT II — Gates, expired ink, vacuum

### `alt_prologue_interclan_gate`

**Kaoru:** Interclan residence requires Emerald approval. You knew that.

**Toa:** I was told a private meeting with the local magistrate would suffice.

**Kaoru:** It does. Door.

**Narrator:** He gestures. The door closes behind her. The latch sounds like a verdict that has not yet been written.

**[CHOICE — reuse `prologue_enter_office_menu`]**

**Kaoru:** Cushion. Floor. You stand too much for someone begging favors.

**Narrator:** A cushion already waits on the tatami at his knee. He taps it once with one finger. A tall cup of water on the desk waits like a witness who has seen this play before.

**Toa:** *(if peeked at shelves)* Yes, Magistrate.

**Kaoru:** *(if peeked)* Since you admire my shelves, admire my seal from a distance when — if — you earn it.

---

### `alt_prologue_expired_permit`  
**CG note (future):** `permit_desk`

**Kaoru:** These dates.

**Toa:** They should be current. I checked before leaving—

**Kaoru:** They are not. Your permit expired. Unicorn bureaucracy failed to mention it?

**Toa:** If I cannot renew locally, they'll send me back to the Academy. I can't— not yet.

**[CHOICE — reuse `prologue_expired_menu`]**

---

### `alt_prologue_social_vacuum`

**Kaoru:** No local patrons. No endorsements.

**Toa:** Only the inn, a pony that needs shoes, and a curry shop where the owner tolerates me because I fold linens without complaint.

**Kaoru:** High society.

**Toa:** It's March twenty-sixth. By tomorrow I need proof I belong here.

**Kaoru:** Tut.

**Narrator:** Once. She has heard he can manage five before dawn.

**Toa:** I stopped at the curry house on the way. He asked if I was lost. I said I was finding the magistrate. He laughed and gave me extra rice.

**Kaoru:** Bribery by carbohydrates. The quarter’s finest diplomat.

**Toa:** I may have listed dance as my primary art. On the renewal form.

**Kaoru:** May have.

**Kaoru:** Dance listed. Venue missing. Patron column blank. Do the math.

**Toa:** I have training. I have stamina. I have a fan that cost more than my pony’s shoes.

**Kaoru:** Stand.

**Narrator:** The cushion at her feet does not move. The water cup on the desk does not move. It never does.

---

# ACT III — Audition (longer performance)

### `alt_prologue_audition_offer`

**Kaoru:** Proposed remedy?

**Toa:** You want a performance.

**Kaoru:** Impress me.

**[CHOICE — reuse `prologue_before_dance_menu`]**

---

### `alt_prologue_office_dance`  
**CG note (future):** `office_dance` · BGM Toa theme

**Narrator:** Lamplight shrinks the room. Toa loosens her obi — not indecent, but deliberate — and lets the silk breathe.

**[CHOICE — reuse `prologue_performance_menu`]**

**Narrator:** *(formal path)* She unfolds her fan. Steps trace courtship, hesitation, resolve — obijime bells whispering at each turn.

**Toa:** The maiden waits at the gate. The road is long. She walks anyway.

**Kaoru:** Better. Keep going. I haven't touched the hanko yet.

**Narrator:** *(flirtatious path)* She plays to one viewer. Hips sway where the kata allows; smile promises more than the room receives.

**Toa:** One person in the room. Might as well make him regret looking away.

**Kaoru:** Cheeky.

**Narrator:** Obijime bells laugh once — invitation and challenge in the same sound. The cup sets down softly. His eyes do not blink.

**Narrator:** *(extended)* She turns a slow circle inside the space between desk and shelf, hakama whispering, white hair catching lamplight like another obi.

**Kaoru:** You're dancing for the seal, not the shelves. Good. Don't stop.

**Toa:** Tomorrow is why I'm here. Tonight is why you're still watching.

---

### `alt_prologue_withheld_signature`

**Toa:** That earns your seal. You said impress me — I did.

**Kaoru:** Merit enough. Signature... pending.

**Toa:** Pending?

**Kaoru:** Continue.

**Narrator:** She continues — bells softer, gaze sharper, every turn aimed at the desk and the seal he still withholds.

**Kaoru:** A good performance.

**Kaoru:** *(if flirtatious)* Better when you stop pretending the room is empty.

**Toa:** The room was never empty. You were in it.

**Kaoru:** Flattery. Continue.

**Narrator:** A second passage — softer bells, sharper gaze. She ends on stillness, not a bow: breath held, fan closed, waiting.

**Kaoru:** A lesser magistrate would stamp your page and send you to the canal.

**Toa:** And for you?

**Kaoru:** I'm not done looking. Continue.

---

# ACT IV — Unless? (escalation)

### `alt_prologue_grab_moment`  
**[CHOICE — reuse `prologue_grab_menu`]**

**Narrator:** His hand finds her wrist — not painful, not gentle. Entitlement dressed as appraisal.

**Kaoru:** Unless?

**Narrator:** The chair creaks. Hakama folds. Power imbalance made visible — two figures, one question hanging.

**[CHOICE — reuse `prologue_unless_menu`]**

---

### Branch pointers (unchanged implementation)

| Menu choice | Jump (shipped) |
|-------------|----------------|
| Verbal | `prologue_verbal_ending` → `prologue_case1_hook` |
| Walk out | `prologue_walkout_ending` → `gameover_rain` |
| Refuse dance (earlier) | `prologue_refuse_bad_end` |
| **Physical (canon alt continues below)** | `alt_prologue_canon_night` |

---

# ACT V — Very much not lost (canon physical, extended night)

### `alt_prologue_canon_night`  
**Scene:** latch closes · BGM canon intimate · **no new CGs in draft**

**Narrator:** The latch catches. Lamplight thins to amber behind the desk.

**Kaoru:** Chair wasn't enough. Good. Come here.

**Toa:** You asked unless. I answered with my body.

**Kaoru:** Then don't stop at the arm of the chair.

**Narrator:** His hand finds her wrist — invitation, not restraint. He draws her off the chair into the space between desk and lantern.

**Toa:** Magistrate-sama—

**Kaoru:** Magistrate-sama stays on your tongue. For what comes next.

**Toa:** Sign later. Touch now.

**Kaoru:** Bold for someone who knocked on the wrong door twice.

**Toa:** You're the one who made me dance for ink.

**Kaoru:** You're why my permit book is still open and my hanko is cold. Don't fix that yet.

**Narrator:** Negotiation dissolves into breath. Her fingers find his collar; his thumb traces the line of her jaw.

**[CG future: canon_pull_close]**

**Kaoru:** Gold cord first. Slow. I've watched you long enough to know you won't rush.

**Toa:** I undress men who watch too long. You watched longest.

**Narrator:** Maroon silk slips from one shoulder. Her obi loosens; his hakama stays untouched — hers the offering, his the permission.

**[CG future: canon_undressing]**

**Toa:** If you mean to keep me, say it plainly. Not in court language.

**Kaoru:** I'm keeping you, To-chan. Latch is shut. The corridor can wait.

**[DISCORD tone — possessive praise, not graphic:]**  
**Kaoru:** That's my very good girl. Stay with me — don't perform for the shelves.

**Toa:** Yes, Magistrate-sama.

**Narrator:** **[FADE — implied intimacy on tatami/cushion; match shipped fade policy]**

**[CG future: canon_embrace → black → canon_afterglow]**

---

### `alt_prologue_canon_afterglow`

**Narrator:** When breath and silk find order again, robes loose and cheeks flushed, the office smells of ink and cedar, not scandal.

**Kaoru:** Are you passing out? You cannot sleep here. This is an office.

**Toa:** Mmngh… give me a minute…

**Narrator:** He considers splashing the cup of water over her. Decides she is too cute. This time.

**Kaoru:** Drink. Before you drip on my permit book.

**Toa:** *(reaches for cup)* Th-thank you, Magistrate-sama.

**Toa:** Is the rest of your day very busy, Magistrate-sama?

**Kaoru:** There's always more paperwork, To-chan. Why do you ask?

**Toa:** I was wondering what your average day is like. Oh — do you need me to sign anything?

**Kaoru:** I will spend today drafting the terms of your sponsorship. Our legal relationship will read art donor to artist — it would insult your lord and yourself if I acted like your danna.

**Kaoru:** The contract entitles you to gifts of a financial nature to support your artistic expression. Interpret that liberally.

**Kaoru:** I know what I am paying for.

**Toa:** Well… I don't, not quite yet. How often do you want to see me? When, where—

**Kaoru:** Twice a week, here at the palace. I will host you in my suite — when the permit allows. Until then, consider tonight a preview of attendance.

**Toa:** Oh. Alright. I'll do my best!

**Kaoru:** You already did. Drink your water before you drip on my desk.

**Toa:** Patience is Crane. Impatience is me asking again before dawn.

**Kaoru:** Then ask after I sign.

---

# ACT VI — Seal, forward date, Case 1 hook

### `alt_prologue_canon_signing`  
**[CG future: canon_signing, canon_three_days]**

**Kaoru:** You earned more than a stamp tonight. Sit still while I find the ink.

**Toa:** Then sign. Before I lose my nerve and my obi in the same breath.

**Kaoru:** Patience.

**Narrator:** He draws the renewal from her permit book. The hanko rises — law made weight in red wax. Stamp. One crisp press.

**Flags (same as shipped):** `permit_signed = True`, `canon_first_scene = True`, `permit_effective_days = 3`, `kaoru_submission += 2`

**Toa:** Thank you— wait. This date.

**Narrator:** She holds the paper to the lamp. His hand wrote three days hence — not tonight's mark.

**Toa:** You dated it forward on purpose.

**Kaoru:** Effective when I say. Return on the thirtieth. We'll discuss residency — and the sponsorship — then.

**Toa:** Guest room preview, forward-dated paperwork, and you call it negotiable.

**Kaoru:** Thirtieth. You'll knock on the right door — I'll leave it unlatched.

**Toa:** Twice a week, you said. Suite. Donor, not danna. I'll hold you to all three.

**Kaoru:** Hold me to twice a week and the suite. The rest we negotiate at my desk.

---

### `alt_prologue_case1_hook`  
**Jump (shipped):** `prologue_case1_hook`

**Narrator:** *(black)* Three days later…

**Implementation:** `jump case1_companion_offer` when `canon_first_scene` — Case 1 scene already contains full live-in companion contract; alt prologue **foreshadows** it so companion dialogue can be trimmed later if desired.

---

## Beat map (acts)

| Act | Label | Source thread | Notes |
|-----|--------|---------------|--------|
| I | `alt_prologue_start` … `formal_knock` | Lost | Longer corridor / curry / clerk flavor |
| II | `interclan_gate` … `social_vacuum` | Lost | Extra tut / pony / curry beats |
| III | `audition` … `withheld_signature` | Lost | Extended dance + withheld hanko |
| IV | `grab_moment` → menu | Lost | Reuse shipped menus & bad ends |
| V | `canon_night` … `afterglow` | Very much not lost | To-chan, water, sponsorship tease |
| VI | `canon_signing` → hook | Both + shipped | Same flags → Case 1 |

---

## What stays on shipped `prologue.rpy`

- All menus and flag math through `prologue_unless_menu`
- `prologue_refuse_bad_end`, `prologue_verbal_ending`, `prologue_walkout_ending`, `gameover_rain`
- `prologue_canon_encounter.rpy` tame CG path **or** replace with `alt_prologue_canon_*` once CGs exist

---

## Review checklist

- [ ] Tone: Discord heat vs otome M/R — adjust lines marked `[DISCORD]` / fades  
- [ ] Duplicate sponsorship in Case 1 — trim `case1_companion_offer` if alt prologue ships  
- [ ] Voice lines: new alt-only lines need IDs if implemented  
- [ ] Menu gate: add `prologue_mode` when ready  
- [ ] CG list: reuse canon_* tags + any new afterglow/water beats
