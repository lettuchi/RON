# Canon ending encounter, physical "Unless?" branch (tame implied romance).

label prologue_canon_ending:

    play music audio.bgm_canon_intimate fadein 2.5 loop volume 0.55

    play sound audio.sliding_door_close volume 0.65
    voice "audio/voice/narrator_040.mp3"
    "The latch catches. Lamplight thins to amber behind the desk."

    show kaoru hungry
    kaoru "Chair wasn't enough. Good. Come here."

    show toa flustered
    toa "You asked unless. I answered with my body."

    show kaoru charm
    kaoru "Then don't stop at the arm of the chair."

    jump prologue_canon_tame

label prologue_canon_tame:

    $ show_cg_scene("canon_pull_close", fade)
    play sound audio.cushion_slide volume 0.45

    voice "audio/voice/narrator_041.mp3"
    "His hand finds her wrist. Not to restrain her, to invite. He draws her off the chair, into the space between desk and lantern."

    show toa soft
    toa "Magistrate-sama..."

    show kaoru satisfied
    kaoru "Magistrate-sama stays on your tongue. For what comes next."

    voice "audio/voice/narrator_042.mp3"
    "Negotiation dissolves into breath. Her fingers find his collar; his thumb traces the line of her jaw."

    show toa happy
    toa "Sign later. Touch now."

    show kaoru hungry
    kaoru "Bold for someone who knocked on the wrong door."

    show toa flustered
    toa "You're the one who made me dance for ink."

    $ show_cg_scene("canon_undressing", fade)
    play sound audio.cushion_slide volume 0.5

    voice "audio/voice/narrator_043.mp3"
    "She loosens the gold outer robe, magistrate formality giving way to skin at throat and collarbone. He lets her. Control, yielded by degrees."

    show kaoru charm
    kaoru "Gold cord first. Slow. I've watched you long enough to know you won't rush."

    show toa soft
    toa "I undress men who watch too long. You watched longest."

    voice "audio/voice/narrator_044.mp3"
    "Maroon silk slips from one shoulder. Her obi loosens; his hakama stays untouched. She offers; he allows."

    $ show_cg_scene("canon_embrace", fade)

    voice "audio/voice/narrator_045.mp3"
    "They fold onto the cushion already on the tatami. Lamplight paints them in gold and shadow, breath shared, his hands in white hair, her mouth at his collar until words fail."

    show toa flustered
    toa "Don't make me beg twice tonight."

    show kaoru satisfied
    kaoru "Then don't perform. Mean it."

    voice "audio/voice/narrator_443.mp3"
    "For one breath the magistrate is gone, and something almost like a smile sits where the ledger usually does, the kind he will deny by morning."

    show kaoru charm
    kaoru "...I have wanted you quiet against me since you knocked on the wrong door. Do not make me file that anywhere. Just stay."

    voice "audio/voice/narrator_046.mp3"
    "She means it. He answers without words, hands in white hair, silk between them, heat where law used to sit."

    scene black with fade
    pause 0.8

    voice "audio/voice/narrator_047.mp3"
    "What followed stayed between petitioner and magistrate; implied, never entered in any clerk's ledger."

    pause 0.6

    voice "audio/voice/narrator_048.mp3"
    "When breath and silk found order again, robes still loose and cheeks flushed, the office smelled of ink and cedar, not scandal."

    $ show_cg_scene("canon_afterglow")
    jump prologue_canon_signing

label prologue_canon_signing:

    voice "audio/voice/kaoru_075.mp3"
    kaoru "You earned more than noise tonight."

    voice "audio/voice/toa_062.mp3"
    toa "Then sign. Before I lose my nerve and my obi in the same breath."

    voice "audio/voice/kaoru_076.mp3"
    kaoru "Patience."

    $ show_cg_scene("canon_signing")

    play sound audio.paper_shuffle volume 0.5
    voice "audio/voice/narrator_049.mp3"
    "He draws the renewal from her permit book. The hanko rises, law made weight in red wax."

    play sound audio.hanko_stamp
    voice "audio/voice/narrator_050.mp3"
    "Stamp. One crisp press against the page."

    $ permit_signed = True
    $ canon_first_scene = True
    $ permit_effective_days = 3
    $ kaoru_submission += 2

    voice "audio/voice/kaoru_077.mp3"
    kaoru "There. Signed."

    voice "audio/voice/toa_063.mp3"
    toa "Thank you... wait. This date."

    $ show_cg_scene("canon_three_days")

    voice "audio/voice/narrator_051.mp3"
    "She holds the paper to the lamp. His hand wrote three days hence, not tonight's mark."

    voice "audio/voice/toa_064.mp3"
    toa "You dated it forward on purpose."

    voice "audio/voice/kaoru_078.mp3"
    kaoru "Effective when I say. Return on the thirtieth. We'll discuss your residency then."

    voice "audio/voice/toa_065.mp3"
    toa "Fine. I'll bring rice crackers and a better fan dance."

    voice "audio/voice/kaoru_079.mp3"
    kaoru "Bring yourself, on time. We will negotiate the rest across my desk."

    voice "audio/voice/toa_066.mp3"
    toa "Guest room preview, forward-dated paperwork, and you call it negotiable."

    voice "audio/voice/kaoru_080.mp3"
    kaoru "Thirtieth. You'll knock on the right door; I'll leave it unlatched."

    jump prologue_case1_hook
