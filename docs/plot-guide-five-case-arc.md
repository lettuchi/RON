# Plot guide — five-case arc

**Spine doc:** [story-so-far.md](story-so-far.md) · **Kaoru voice:** [kaoru-dialogue-style.md](kaoru-dialogue-style.md) · **Toa arc:** [toa-dialogue-style.md](toa-dialogue-style.md)

---

## Premise

> An itinerant Crane dancer earns Emerald Magistrate Kitsu Kaoru's companion permit, and follows him through five corrupt cases believing she is only his witness, and discovers in the end he was auditioning his yoriki the whole time.

---

## Why five cases

Ryoko Owari does not run on one crime; it runs on **layers**. One case closes a symptom; the next reveals who paid for the symptom. Five beats work when each case is a **different face of the same root** (Chrysanthemum / pleasure-quarter / magistrate politics), not five unrelated mysteries.

| Case | What the city thinks it's about | What Kaoru is actually doing |
|------|----------------------------------|------------------------------|
| **1** | Smuggling / barge / factor | Tests whether Toa can **read a lie under pressure** and stay in his line |
| **2** | Festival / public face | Tests whether she can be **seen with him** without flinching or claiming Crane honor over his file |
| **3** | Trade / fabric / bolt room | Tests **trust** when the room tries to kill her (rescue beat) |
| **3.5** | (No case number — off ledger) | Tests whether she can accept **gift without a name** (date without "date") |
| **4** | Dock / steel | Tests whether she will **stay behind him** when it costs her pride |
| **4.5** | (Interlude) | Tests **body obedience** off the record — not filed, but he files her anyway in his head |
| **5** | Hearing / seal / quarter politics | **Closes the audition** — yoriki appointment is the prize she didn't know she was competing for |

OOC, five is also clean for an otome: **one case ≈ one emotional gear shift** (competence → visibility → trust → desire → commitment).

---

## Audition framing — prologue → Case 1

**Prologue:** Dance-for-ink, *unless?*, forward-dated permit — first competence test disguised as renewal. Toa thinks she earned paper; Kaoru thinks she earned a seat in his corridor.

**Permit → Case 1 gap (three days):** Companion offer in `game/case1_companion.rpy` frames the next weeks **without saying yoriki**:

| Kaoru's cover | What Toa hears |
|---------------|----------------|
| Extended witness bond | Ride along until the first root is cut |
| Provisional attachment | Survive Case One, then discuss permanence (= salary / room) |
| Political insulation | "The Crane is watching" — cover that happens to be true |
| He likes her (subtext) | *You argued well. I prefer competence within reach.* |

**What Toa believes:** Proving the permit was worth it — earning the room, stipend, protection.  
**What the player learns:** Every case is a **competency trial**; romantic pressure is the unspoken scoring rubric.

**Case 1 hook:** Immediately after companion close (`case1_investigation_hook`), Kaoru **springs the week** — five matters on his slate, witness docket duty, Case One through Five — without saying yoriki. Toa thought the deal was dance, patronage, adjoining room; cases read as bait-and-switch. Archive run for Case One ledger, then desk callback (`case1_investigation_assign`) before the canal body briefing. Non-canon (`case1_noncanon_start`) gets the same count with witness-only framing and no live-in seal.

**Scene docs:** [case1-companion-scene.md](case1-companion-scene.md) · [case1-investigation-scene.md](case1-investigation-scene.md)

---

## Case 5 — yoriki surprise

Toa's surprise lands if, for the whole game, she believes she holds a **different job title**:

- **What she thinks:** witness, companion, permit artist, Magistrate-sama's useful Crane who sleeps behind his screen.
- **What Kaoru never says:** "I am evaluating you for yoriki."
- **What the city whispers:** sponsorship, kept woman, influence — not **office**.

**Case 5 is the administrative climax**, not just another puzzle:

- Cases 1–4 conspiracy demands a **public magistrate act** (hearing, seal, rival, Crane envoy).
- Kaoru needs a **sworn yoriki** to sign witness chains and stand beside him in the quarter.
- Toa assumed goodbye after the last blade stopped. Instead: **appointment** scroll across the desk.

**Reveal beat structure:**

1. She thinks the meeting is punishment or goodbye.
2. He lists what she did in Cases 1–4 (concrete, not poetic).
3. The scroll says **yoriki**.
4. She stammers about Crane custom / marriage / honor.
5. He shuts it down: *This is office. You already served it.*
6. Optional soft button: she accepts without saying love; he doesn't either.

**Kaoru line (in character):** not "I love you" — *You passed every case I put in front of you. The city requires a name on my left hand. I chose yours.*

**Current stub:** `case5_stub_tease` in `game/case4_5_boat.rpy` (pleasure-quarter seal tease).

---

## Recurring dual-meaning phrases

Magistrate vocabulary that means two things — seed in dialogue, pay off in Case 5:

| Kaoru says | Toa hears | Player (later) hears |
|------------|-----------|----------------------|
| "Stay in my line." | Don't embarrass me | Yoriki discipline |
| "The file requires a left hand." | Clerk work | Second seat / yoriki |
| "You are still on trial." | Harsh boss | Audition |
| "When Case X closes, we discuss terms." | Pay / permit renewal | Appointment |
| "Witness is not enough in this city." | Insult | You need rank |
| "Provisional attachment until the files close." | Bureaucratic hedge | Audition never ended |

**In-world tagline (Kaoru, not marketing):** *Provisional attachment until the files close.*

---

## Case plot guides (existing)

| Chapter | Doc |
|---------|-----|
| Case 1 companion | [case1-companion-scene.md](case1-companion-scene.md) |
| Case 1 investigation | [case1-investigation-scene.md](case1-investigation-scene.md) |
| Case 2 investigation | [case2-investigation-scene.md](case2-investigation-scene.md) |
| Case 3 investigation | [case3-investigation-scene.md](case3-investigation-scene.md) |
| Case 3.5 date interlude | [plot-guide-is-this-a-date.md](plot-guide-is-this-a-date.md) · [case3.5-date-interlude-design.md](case3.5-date-interlude-design.md) |
| Case 4 investigation | [case4-investigation-scene.md](case4-investigation-scene.md) |
| Case 4.5 kobune | [plot-guide-case4-5-boat.md](plot-guide-case4-5-boat.md) |

Case 5 script not yet built — expand from `case5_stub_tease` into roster / hearing scene per sections above.
