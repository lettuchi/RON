# Case 3.5, "Is this a date?" (Teardrop Island; Discord #teardrop-island adaptation).
# Entry: case3_post_case3_bridge when romance_through_case3_complete().
# Exit: case4_post_case3_bridge → Case 4 dock raid.
# Save flag: case4_date_interlude_seen (legacy name; means Case 3.5 viewed).
# VOICED: Case 3.5 manifest pass (2026-06-03). toa_130-172, kaoru_162-205, narrator_144-173 (117 lines).

label case3_post_case3_bridge:

    if case3_5_date_interlude_eligible():
        jump case3_5_is_this_a_date_interlude

    jump case4_post_case3_bridge


label case3_5_is_this_a_date_interlude:

    $ case4_date_interlude_seen = True

    # ,  Act I: Invitation & crossing , 
    scene bg magistrate_office with fade
    play music audio.bgm_office fadein 2.0 loop volume 0.45
    show kaoru commanding at left
    show toa happy at right

    voice "audio/voice/narrator_144.mp3"
    "Case Three's saw kerf still smells of cedar dust when Kaoru sets down his brush. Not on a docket this time, but on a folded sheet of rice paper, sealed with wax that carries no office chop at all."

    voice "audio/voice/kaoru_162.mp3"
    kaoru "The clerk can run until dawn for all I care. You, on the other hand, have an appointment that is not on any ledger."

    show toa surprised
    voice "audio/voice/toa_130.mp3"
    toa "Magistrate-sama, Case Four is going to be steel at the dock. If I vanish in festival dress, the watch will file nothing but gossip about it."

    show kaoru smirk
    voice "audio/voice/kaoru_163.mp3"
    kaoru "The watch files what I sign. And tonight I am signing nothing except your attendance."

    voice "audio/voice/narrator_145.mp3"
    "He slides the paper across the desk. The hand is unmistakably his, blunt vertical strokes, not a breath of poetry in it."

    voice "audio/voice/kaoru_164.mp3"
    kaoru "Meet me on Teardrop Island. There is an inn on the north side, tucked between two geisha houses. Wear your best."

    show toa flustered
    voice "audio/voice/toa_131.mp3"
    toa "Wear my... That is not the address of a field inspection. That is..."

    show kaoru charm
    voice "audio/voice/kaoru_165.mp3"
    kaoru "Read the rest once you have remembered how to breathe."

    voice "audio/voice/narrator_146.mp3"
    "The second line is written smaller: *Performances available upon request from either neighboring house. Do not be late.*"

    show toa thinking
    voice "audio/voice/toa_132.mp3"
    toa "You bought a whole venue. You did not buy me a single reason why."

    show kaoru satisfied
    voice "audio/voice/kaoru_166.mp3"
    kaoru "You will have your reason when you arrive, and arrive hungry. Keep up, To-chan."

    scene black with fade
    pause 0.4

    voice "audio/voice/narrator_147.mp3"
    "She agonized over every last hairpin, dithered between obi brocades for hours, and finally flipped a coin just to settle on her shoes. Autumn's turning let her play with patterns the peak seasons would never allow."

    $ show_cg_scene("case3_5_date_silk_fabric", fade)
    $ set_toa_outfit("date")

    voice "audio/voice/narrator_148.mp3"
    "Black furisode, scattered with the turn of autumn: bush clover and chrysanthemum at the roots of a maple that climbs her sleeves, red leaves drifting all the way down her arms. Rose-gold obi brocade tied in a musubi that trails past her hips. Zori instead of clunky geta, and kanzashi bells that sing whenever she moves."

    voice "audio/voice/narrator_149.mp3"
    "Rouge on her lips and at her eyes. Deliberate grace tonight, instead of her usual exuberant freedom. At one-third of her normal stride, the walk to the ferry takes forever."

    $ show_cg_scene("case3_5_date_arrival", fade)
    play music audio.bgm_case3_5_date fadein 2.5 loop volume 0.48

    voice "audio/voice/narrator_150.mp3"
    "Teardrop Island at night is all lantern-gold on dark water, licensed-quarter elegance without a trace of the magistrate hall's ink. The geisha house eaves lean close over the canal like confidantes sharing a secret."

  # ,  Act II: Arrival & dress , 
    $ show_cg_scene("case3_5_date_inn_exterior", fade)

    voice "audio/voice/narrator_151.mp3"
    "The inn sits exactly where he said it would: north side, wedged between two houses whose signboards promise music. Not another guest on the walkway. Not a sound of chatter behind the main screen."

    show toa date surprised at center
    voice "audio/voice/toa_133.mp3"
    toa "The whole place?!"

    voice "audio/voice/narrator_152.mp3"
    "A servant offers a cup of crisp hojicha, the kind she will chase down again for weeks afterward. When she asks, they only bow: yes, Magistrate Kitsu has taken the entire venue. Performances on request, from either neighbor."

    voice "audio/voice/toa_134.mp3"
    toa "So... no one else is here at all."

    $ show_cg_scene("case3_5_date_tatami_lanterns", fade)

    voice "audio/voice/narrator_153.mp3"
    "Inside: tatami, paper lanterns, a low table set for two. Biwa music threads through from behind the wall, not a performance yet, just atmosphere."

    show kaoru charm at left
    show toa date happy at right

    voice "audio/voice/toa_135.mp3"
    toa "Good evening, Magistrate-sama!"

    voice "audio/voice/narrator_154.mp3"
    "She tries to bow the way she always does. The stiff fukuro obi grants her barely a hinge. She laughs to herself and straightens, catching his fragrance, the very same note as that first wrong door."

    voice "audio/voice/kaoru_167.mp3"
    kaoru "Good evening, Toa-san. The journey here was not too difficult, I hope?"

    show toa date flustered
    voice "audio/voice/toa_136.mp3"
    toa "No, only longer than I expected. I do hope you were not waiting too long."

    show toa date bashful
    voice "audio/voice/toa_137.mp3"
    toa "...You smell so nice."

    show kaoru amused
    voice "audio/voice/kaoru_168.mp3"
    kaoru "Hm."

    voice "audio/voice/kaoru_169.mp3"
    kaoru "Are you hungry? Thirsty?"

    show toa date thinking
    voice "audio/voice/toa_138.mp3"
    toa "Um..."

    voice "audio/voice/narrator_155.mp3"
    "She tips her face upward, checking in with her own body."

    show toa date happy
    voice "audio/voice/toa_139.mp3"
    toa "Both!"

  # ,  Act III: Private room & kaiseki , 
    show kaoru commanding
    voice "audio/voice/kaoru_170.mp3"
    kaoru "The menu has already been decided for you."

    voice "audio/voice/narrator_156.mp3"
    "A servant slips out without so much as a ledger. Kaoru angles himself toward her, not quite facing her, the way he sits when he wants the truth without an audience for it."

    show kaoru thinking
    voice "audio/voice/kaoru_171.mp3"
    kaoru "I wanted to show you some appreciation. For all the work you have done for me."

    voice "audio/voice/narrator_157.mp3"
    "Not *thank you*. He has said that word to her before, in his own particular way. It does not bother her at all that he skips it tonight."

    $ show_cg_scene("case3_5_date_kaiseki_duo", fade)

    voice "audio/voice/narrator_158.mp3"
    "Kaiseki trays arrive, autumn's turning laid out on porcelain. Matsutake with salted plum and preserved chrysanthemum. Skipjack with mustard greens, alliums, shiso flowers. White miso and chestnut."

    show toa date happy
    voice "audio/voice/toa_140.mp3"
    toa "Eeeee, matsutake! I'm so excited!"

    voice "audio/voice/kaoru_172.mp3"
    kaoru "Enjoy it."

    $ show_cg_scene("case3_5_date_sake_cup", fade)

    voice "audio/voice/narrator_159.mp3"
    "The sake is poured, and he does not throw it back. It is expensive enough to be savored."

    voice "audio/voice/kaoru_173.mp3"
    kaoru "I have arranged for more music, and dancers, should that suit your desires."

    show toa date twitterpated
    voice "audio/voice/toa_141.mp3"
    toa "I have not listened to music, or watched dancing, just for the joy of it in such a long time. This is really lovely, Magistrate-sama."

    show toa date happy
    voice "audio/voice/toa_142.mp3"
    toa "Kampai!"

    voice "audio/voice/kaoru_174.mp3"
    kaoru "Kampai."

    $ show_cg_scene("case3_5_date_candle_flame", fade)

    voice "audio/voice/narrator_160.mp3"
    "The warm courses follow: toro with uni rice porridge, cabbage and bamboo with shrimp, mushroom shabushabu simmering over a tealight, sesame noodles bright with watercress and radish."

    voice "audio/voice/narrator_161.mp3"
    "She whispers *itadakimasu*. Good food earns her silence, nothing but a soft hum the moment matsutake meets her tongue."

    $ show_cg_scene("case3_5_date_toa_lashes", fade)

    voice "audio/voice/narrator_162.mp3"
    "Between bites she watches him savor each flavor the way he savors a confession he has not filed yet, unhurried, proprietary, pleased without performing that pleasure for an audience."

    menu case3_5_date_meal_menu:
        "Eat in companionable quiet, and let the meal do the talking.":
            show toa date happy
            voice "audio/voice/toa_143.mp3"
            toa "When it is this good, the paperwork can wait."

            show kaoru smirk
            voice "audio/voice/kaoru_175.mp3"
            kaoru "Finally. A witness note I can eat without crossing out your adjectives."

        "Ask him what this evening really is, before the dancers arrive.":
            show toa date embarrassed
            voice "audio/voice/toa_144.mp3"
            toa "Magistrate-sama, you bought out an island inn. You put me in furisode. What do you call this, if not courtship?"

            show kaoru cold
            voice "audio/voice/kaoru_176.mp3"
            kaoru "I call it payment for bolt-room competence. Do not let the quarter file poetry about us before the dessert is even cleared."

            show toa date bashful
            voice "audio/voice/toa_145.mp3"
            toa "Then I will eat until the only thing the quarter can file is crumbs."

  # ,  Act IV: Dance & reading bodies , 
    voice "audio/voice/narrator_163.mp3"
    "When they have polished off two dishes apiece, more instruments come in beneath the biwa: strings, flute, a hand drum."

    $ show_cg_scene("case3_5_date_watch_dancers", fade)

    show toa date surprised
    voice "audio/voice/narrator_164.mp3"
    "At the first drumbeats she perks up, slate eyes half-transfixed and half-evaluating, an old authority settling back into her shoulders."

    show kaoru charm at left
    show toa date happy at right

    voice "audio/voice/kaoru_177.mp3"
    kaoru "If I ever turn up a dance crime, at least I will know exactly who to bring with me."

    voice "audio/voice/kaoru_178.mp3"
    kaoru "Relax. Enjoy the dance. Unless the watching is the fun of it. What could they be doing better?"

    menu case3_5_date_dance_menu:
        "Just watch in quiet delight, no lecture.":
            show toa date soft
            voice "audio/voice/toa_146.mp3"
            toa "They are beautiful. That is more than enough for one night."

            show kaoru satisfied
            voice "audio/voice/kaoru_179.mp3"
            kaoru "Witness approved."

        "Teach him how bodies tell the truth.":
            jump case3_5_date_dance_lecture

    jump case3_5_date_after_dance


label case3_5_date_dance_lecture:

    show toa date determined
    voice "audio/voice/toa_147.mp3"
    toa "I would never correct them mid-performance. Every dance is practice for the next one."

    voice "audio/voice/toa_148.mp3"
    toa "I am not hunting for mistakes. Movement tells you the dancer's mind. Pretense stumbles eventually, in the body or in the mind."

    voice "audio/voice/toa_149.mp3"
    toa "The body is a truthteller. And it remembers everything."

    show kaoru thinking
    voice "audio/voice/kaoru_180.mp3"
    kaoru "Much as a magistrate reads deceit."

    show toa date happy
    voice "audio/voice/toa_150.mp3"
    toa "Precisely, Magistrate-sama. Trust your intuition. Our bodies know far more than we give them credit for."

    $ show_cg_scene("case3_5_date_lesson", fade)

    show toa date thinking
    voice "audio/voice/toa_151.mp3"
    toa "Back left, called in at the last minute, knows the choreography but not today's spacing. Front right, junior, trembling whenever she holds still, you only put her in because the venue is empty. Back center is the teacher, an older style, staying behind to drive the rest of them. And front left is dancing pure obligation, eyes hunting for patrons instead of following the music."

    show kaoru amused
    voice "audio/voice/kaoru_181.mp3"
    kaoru "Well, then. It seems I have learned something new tonight."

    voice "audio/voice/kaoru_182.mp3"
    kaoru "And you do realize these observations of yours are not limited to dance?"

    show toa date soft
    voice "audio/voice/toa_152.mp3"
    toa "I use it every waking minute of my life, Magistrate-sama."

    jump case3_5_date_trust_overshare


label case3_5_date_after_dance:

    show toa date soft
    voice "audio/voice/toa_153.mp3"
    toa "The junior will be alright. She just should not shake like that twice."

    jump case3_5_date_trust_overshare


label case3_5_date_trust_overshare:

    $ show_cg_scene("case3_5_date_kaoru_hand_cup", fade)
    pause 1.2

    voice "audio/voice/narrator_307.mp3"
    "His thumb finds the collar cord instead of her palm. Gold brocade, rose obi edge, skin warming under linen that is not office kosode. Shallow focus, shallow mercy."

    $ show_cg_scene("case3_5_date_inn_collar_hands", fade)
    pause 2.0

    show toa date thinking at right
    show kaoru charm at left

    voice "audio/voice/toa_154.mp3"
    toa "People still ask me, at least once a week, whether I am alright. Whether you are hurting me. Whether I stay of my own free will."

    show toa date determined
    voice "audio/voice/toa_155.mp3"
    toa "I tell them I have never once felt unsafe with you. That you actually weigh what I say. That we see each other clearly, without lying..."

    voice "audio/voice/narrator_165.mp3"
    "She catches herself right on the edge of a word she will not let herself name until Case Five."

    show toa date embarrassed
    voice "audio/voice/toa_156.mp3"
    toa "So, um. The point is, bodies do not lie, and I have always trusted..."

    voice "audio/voice/narrator_166.mp3"
    "She turns to her plate instead. Then the sake. Then the air."

    show kaoru amused
    voice "audio/voice/kaoru_183.mp3"
    kaoru "I know. I file what your body says louder than your mouth."

    show kaoru commanding
    voice "audio/voice/kaoru_184.mp3"
    kaoru "Now tell me who has been saying these things. I insist. Gossip is inventory I did not authorize."

  # ,  Act V: Gossip sting & reassurance , 
    $ show_cg_scene("case3_5_date_gossip", fade)

    show toa date embarrassed
    voice "audio/voice/toa_157.mp3"
    toa "W-well, Hi-Hiromi-san. And Doji S-Sango-san..."

    show kaoru surprised
    voice "audio/voice/kaoru_185.mp3"
    kaoru "Doji Sango-san? Have the two of us even spoken?"

    voice "audio/voice/narrator_167.mp3"
    "He leans back, delighted, treating the rumor as intelligence, not as shame."

    voice "audio/voice/kaoru_186.mp3"
    kaoru "If it is only two names, then I clearly need to work on my image."

    show toa date worried
    voice "audio/voice/toa_158.mp3"
    toa "It is not only two. I simply cannot summon any more while my heart is sprinting like this."

    voice "audio/voice/kaoru_187.mp3"
    kaoru "And what else has this Doji Sango-san been saying?"

    show toa date embarrassed
    voice "audio/voice/toa_159.mp3"
    toa "Nothing beyond that one basket of topics. I do not know her well."

    voice "audio/voice/kaoru_188.mp3"
    kaoru "Oh. Now I am very interested."

    show toa date thinking
    voice "audio/voice/toa_160.mp3"
    toa "I think you may simply have to ask her directly, Magistrate-sama."

    voice "audio/voice/kaoru_189.mp3"
    kaoru "I would never do such a thing. That would be admitting defeat."

    show toa date surprised
    voice "audio/voice/toa_161.mp3"
    toa "Should I stop telling people that I stay freely? Did I do something wrong?"

    voice "audio/voice/kaoru_190.mp3"
    kaoru "No. Do not change a single thing. If servants are carrying it, she may as well be keeping watchers."

    show toa date worried
    voice "audio/voice/toa_162.mp3"
    toa "Alright..."

    voice "audio/voice/narrator_168.mp3"
    "She eats the sesame seeds one by one, then frowns as the question turns itself over."

    show toa date sad
    voice "audio/voice/toa_163.mp3"
    toa "Do you... hear bad things about me?"

    $ show_cg_scene("case3_5_date_reassurance", fade)

    show kaoru charm
    voice "audio/voice/kaoru_191.mp3"
    kaoru "Never once. You are very well loved in this city."

    show toa date happy
    voice "audio/voice/toa_164.mp3"
    toa "Well, that's good!"

    show kaoru smirk
    voice "audio/voice/kaoru_192.mp3"
    kaoru "Dessert?"

    show toa date happy
    voice "audio/voice/toa_165.mp3"
    toa "Of course! What's a fancy meal without it?"

    voice "audio/voice/narrator_169.mp3"
    "Bean paste with tea. Sweet enough to let them pretend there is no dock steel waiting for them at dawn."

  # ,  Act VI: Island path & date question , 
    scene black with fade
    pause 0.3

    $ show_cg_scene("case3_5_date_walk_duo", dissolve)
    play music audio.bgm_street fadein 2.0 loop volume 0.42

    voice "audio/voice/narrator_170.mp3"
    "They walk the lantern path down toward the ferry, her zori careful on the stone, his pace slowed to match her bells and her obi."

    show kaoru charm at left
    show toa date twitterpated at right

    voice "audio/voice/toa_166.mp3"
    toa "You bought the whole island. You fed me matsutake. You said that I am loved."

    show kaoru thinking
    voice "audio/voice/kaoru_193.mp3"
    kaoru "I said the city speaks well of my witness. Do not go inflating the file."

    show toa date embarrassed
    voice "audio/voice/toa_167.mp3"
    toa "Magistrate-sama, when you plan out an entire evening like tonight, what do you call it?"

    menu case3_5_date_walk_menu:
        "Let the lanterns answer for him, and swallow the question.":
            pass

        "Ask him outright: is this a date?":
            $ is_this_a_date_asked = True
            jump case3_5_date_asked_beat

    jump case3_5_date_after_walk


label case3_5_date_asked_beat:

    show toa date determined
    voice "audio/voice/toa_168.mp3"
    toa "Is this a date?"

    show kaoru amused
    voice "audio/voice/kaoru_194.mp3"
    kaoru "A date is a line in a permit book."

    pause 0.35

    show kaoru cold
    voice "audio/voice/kaoru_195.mp3"
    kaoru "This is appreciation. For witness competence. And food, so you do not faint on my desk tomorrow."

    show toa date angry
    voice "audio/voice/toa_169.mp3"
    toa "That is not an answer."

    show kaoru smirk
    voice "audio/voice/kaoru_196.mp3"
    kaoru "It is the answer the quarter deserves. You are patronage on paper, the woman who trusted me in the bolt room. Do not borrow festival vocabulary because the sake was expensive and your obi is too honest."

    show toa date soft
    voice "audio/voice/toa_170.mp3"
    toa "The festival was real. Your hand on that cup was real. Do not tell me to un-feel it just because the file would prefer silence."

    show kaoru cold
    voice "audio/voice/kaoru_197.mp3"
    kaoru "Feel whatever you like in private. In public, you are mine to position."

    pause 0.2

    show kaoru charm
    voice "audio/voice/kaoru_198.mp3"
    kaoru "...No."

    pause 0.4

    show kaoru thinking
    voice "audio/voice/kaoru_199.mp3"
    kaoru "It is the closest I come to calling this courtship, before I learn better."

    show kaoru cold
    voice "audio/voice/kaoru_200.mp3"
    kaoru "Forget the second sentence. The first one stands. Feel the rest in private."

    voice "audio/voice/narrator_171.mp3"
    "Crane training keeps her face pleasant. Inside, something unnamed aches, not love, not by name, only the quiet wish that he would stop stepping back after every step he takes forward."

    jump case3_5_date_after_walk


label case3_5_date_after_walk:

    $ show_cg_scene("case3_5_date_almost_hands", fade)

    voice "audio/voice/narrator_172.mp3"
    "His hand lifts. Not to take hers, but to straighten a lantern cord near her sleeve. His fingers pause a breath's width from her palm, close enough that she feels the heat he will not file. The almost-touch hurts worse than any no."

    if not is_this_a_date_asked:
        menu case3_5_date_late_ask_menu:
            "Let it go, and carry the ache quietly.":
                pass

            "Ask him anyway: is this a date?":
                $ is_this_a_date_asked = True
                show toa date embarrassed
                voice "audio/voice/toa_171.mp3"
                toa "Just one word, yes or no. Is this a date?"

                show kaoru amused
                voice "audio/voice/kaoru_201.mp3"
                kaoru "No."

                pause 0.35

                show kaoru charm
                voice "audio/voice/kaoru_202.mp3"
                kaoru "...It is the closest I come, before I learn better."

                show kaoru cold
                voice "audio/voice/kaoru_203.mp3"
                kaoru "Forget I said the second sentence. The first one stands."

  # ,  Act VII: Return & bridge to Case 4 , 
    scene bg magistrate_office with fade
    play music audio.bgm_office fadein 2.0 loop volume 0.48
    $ set_toa_outfit("work")
    show kaoru commanding at left
    show toa work soft at right

    voice "audio/voice/narrator_173.mp3"
    "The compound gate closes behind them. Cedar and ink take the place of hojicha and drum. She should sleep. Instead she lies there listening to his footsteps fade toward the inner hall, still not a date by his ledger, still not love by its name, still hers in every file he refuses to romanticize."

    voice "audio/voice/kaoru_204.mp3"
    kaoru "Tea. Then bed. The dock tomorrow will not smell of lanterns."

    voice "audio/voice/toa_172.mp3"
    toa "Yes, Magistrate-sama."

    show kaoru smirk
    voice "audio/voice/kaoru_205.mp3"
    kaoru "And, To-chan. Do not sulk in the witness log. Sulk in private where I can inventory it. I permit you that much."

    jump case4_post_case3_bridge
