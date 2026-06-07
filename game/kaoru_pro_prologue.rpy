# Case Zero · Kaoru pro-prologue (pre-Toa).
#
# Play: Dev menu → "Pro-prologue, Case Zero (Kaoru)" (dev_chapter_pick.rpy).
# Optional new-game gate (default OFF): set persistent.play_case_zero = True in
# console or prefs, then in script.rpy before `jump prologue_start`:
#     if getattr(persistent, "play_case_zero", False):
#         call kaoru_pro_prologue from _call_kaoru_case_zero
#
# Exit: jump prologue_start (Toa's wrong door).
# VOICED: kaoru_387-425, narrator_312-365 (legacy MP3s on disk).

default seen_case_zero = False
default case_zero_smile_choice = ""
default case_zero_puppet_choice = ""

label kaoru_pro_prologue:

    $ seen_case_zero = True
    scene black with fade
    play music audio.bgm_office fadein 3.0 loop volume 0.28

    centered "{font=fonts/YujiSyuku-Regular.ttf}{size=+6}Case Zero{/size}{/font}\n{size=-4}Emerald Magistrate docket · summary only{/size}"

    pause 1.0

    $ show_cg_scene("case_zero_redacted_docket", fade)

    voice "audio/voice/narrator_312.mp3"
    "SUMMARY ONLY. Witness names redacted per magistrate seal."

    voice "audio/voice/narrator_313.mp3"
    "Matter: administrative. No body. No numbered case file after closure."

    voice "audio/voice/narrator_314.mp3"
    "Subject: Kitsu Kaoru, Emerald Magistrate, Ryoko Owari quarter. Period: three mornings prior to interclan renewal spike."

    voice "audio/voice/narrator_315.mp3"
    "Witness A ████████ (tea clerk): left cups at the inner desk. Subject did not drink."

    voice "audio/voice/narrator_316.mp3"
    "Witness B ████████ (runner, age twelve): delivered three summonses across the Hour of the Tiger, each a few breaths apart. Subject signed without looking up."

    voice "audio/voice/narrator_317.mp3"
    "Witness C ████████ (puppeteer, street): performed villain motive incorrectly. Subject corrected from window. No arrest."

    voice "audio/voice/narrator_318.mp3"
    "Witness D ████████ (Ronin-adjacent): escorted per House of Falling Lanterns arithmetic. Subject ordered door closed."

    voice "audio/voice/narrator_319.mp3"
    "Finding: subject maintained ledger discipline. Emotional display: none recorded."

    voice "audio/voice/narrator_320.mp3"
    "Recommendation: file under patronage appetite, spendable witnesses, proprietary corridor. Open next docket when renewal petition arrives."

    scene bg magistrate_office with dissolve
    show kaoru cold at left

    voice "audio/voice/narrator_321.mp3"
    "First morning. Rain on the eaves like a clerk tapping a stamp."

    voice "audio/voice/narrator_322.mp3"
    "One cup at the desk corner. Steam gone. The magistrate reads a drowning report and does not touch it."

    play sound audio.paper_shuffle volume 0.4
    show kaoru commanding
    voice "audio/voice/kaoru_387.mp3"
    kaoru "Tea is witness work when someone wants a favor. File the cup. I did not ask."

    voice "audio/voice/narrator_347.mp3"
    "The tea clerk waits one breath too long, hoping he will sip and soften. He signs her overtime chit instead and sends her back to the kitchen."

    voice "audio/voice/kaoru_412.mp3"
    kaoru "Gratitude in liquid form is still a bid. I do not accept bids before breakfast."

    voice "audio/voice/narrator_323.mp3"
    "Second morning. Heavier rain. Two cups, both empty, lined up like failed petitions."

    voice "audio/voice/narrator_348.mp3"
    "Water streaks the window until the canal road is only lantern smears and the shape of a city that charges rent on visibility."

    voice "audio/voice/kaoru_388.mp3"
    kaoru "You may leave the second if it saves you a walk. I still will not drink gratitude."

    voice "audio/voice/kaoru_413.mp3"
    kaoru "If you want to please me, bring dry copies and leave the sugar on someone else's tray."

    voice "audio/voice/narrator_324.mp3"
    "Third morning. The canal smells wrong-green through the palace eaves. Three cups. The ledger line for interclan renewal stays blank one more day."

    voice "audio/voice/narrator_349.mp3"
    "On the outer desk a renewal spike notice waits unopened. Somewhere in the noble quarter a Crane without local ink is still on the road. He knows the type before the knock."

    show kaoru smirk
    voice "audio/voice/kaoru_389.mp3"
    kaoru "Three mornings, three cups, zero admissions. When the dancer arrives with tea she will learn the same arithmetic."

    voice "audio/voice/kaoru_414.mp3"
    kaoru "Mikan comes later. Peel on a tray. Domestic filing. I will deny that too until the quarter stops selling what I intend to keep."

    voice "audio/voice/narrator_325.mp3"
    "He almost smiled at that. His mouth considered it and filed the motion under denied."

    jump case_zero_almost_smile


label case_zero_almost_smile:

    voice "audio/voice/narrator_326.mp3"
    "Almost-smile inventory, magistrate wing, prior week. All entries denied."

    show kaoru cold
    voice "audio/voice/kaoru_390.mp3"
    kaoru "When the archive boy brought mikan peel on a tray. Denied."

    voice "audio/voice/kaoru_391.mp3"
    kaoru "When Witness ████ cried thank-you on the stairs and bowed too low. Denied."

    voice "audio/voice/kaoru_392.mp3"
    kaoru "When the puppet villain on the canal road got the children to clap. Denied."

    voice "audio/voice/kaoru_393.mp3"
    kaoru "When the rain stopped for six breaths and the office went quiet enough to pretend this city was kind. Denied."

    voice "audio/voice/kaoru_415.mp3"
    kaoru "When the night clerk laughed at my stamp and called me handsome in a voice that wanted a corridor pass. Denied."

    voice "audio/voice/kaoru_416.mp3"
    kaoru "When the okami's runner bowed with coin already counted and called me merciful. Denied. Merciful is a word witnesses use before they learn the price."

    voice "audio/voice/kaoru_417.mp3"
    kaoru "When I thought of a kotatsu and wool and citrus and a mouth that might ask me to almost smile on purpose. Denied twice. Denied in advance."

    voice "audio/voice/narrator_327.mp3"
    "He sets the inventory on the desk beside the unused cups. Somewhere under wool and citrus, a future afternoon will ask for an almost-smile again. He intends to deny it until the ledger stops counting."

    voice "audio/voice/narrator_350.mp3"
    "Proprietary hunger is not romance. It is the appetite to own a corridor, a witness schedule, a body that signs where he points. He writes the distinction on a scrap and tucks it with the seal."

    menu case_zero_smile_menu:
        "Close the inventory and work.":
            $ case_zero_smile_choice = "work"
            voice "audio/voice/kaoru_394.mp3"
            kaoru "Paper first. Mouth later. If later ever comes."

        "Watch the rain another minute.":
            $ case_zero_smile_choice = "rain"
            voice "audio/voice/kaoru_395.mp3"
            kaoru "Watching is free. Smiling is a debt I have not agreed to owe."

    jump case_zero_runner_pov


label case_zero_runner_pov:

    scene bg corridor with dissolve
    hide kaoru
    play sound audio.footsteps_corridor volume 0.45

    voice "audio/voice/narrator_328.mp3"
    "The runner is twelve and paid per stair. His name is not for this file."

    voice "audio/voice/narrator_329.mp3"
    "First bell of the Tiger. Summons packet, third copy, wax still warm from the night clerk. Magistrate wing, inner screen, do not knock like a petitioner who wants theater."

    voice "audio/voice/narrator_330.mp3"
    "He kneels at the threshold and slides the paper under the gap. Through the crack he sees legs crossed on tatami, maroon hem, ink-stained fingers holding a seal."

    voice "audio/voice/narrator_331.mp3"
    "Grey eyes lift once. Not to the boy. To the docket line where the signature belongs."

    play sound audio.sliding_door_open volume 0.4
    play sound audio.hanko_stamp volume 0.55
    voice "audio/voice/narrator_332.mp3"
    "The inner screen opens two fingers wide. A hand takes the summons. Stamp. The hand does not pat his head or say thank you."

    voice "audio/voice/narrator_333.mp3"
    "From inside, a voice the boy will not quote to friends because friends disappear in this quarter:"

    voice "audio/voice/kaoru_396.mp3"
    kaoru "Next stair. Do not wait for praise."

    play sound audio.sliding_door_close volume 0.45
    voice "audio/voice/narrator_351.mp3"
    "Second bell of the Tiger. Second packet. Same crack. Same eyes on the line. Same stamp like a heartbeat the boy learns to fear and need."

    voice "audio/voice/kaoru_418.mp3"
    kaoru "If you linger I will deduct a coin for theater."

    voice "audio/voice/narrator_352.mp3"
    "A third bell, late in the Hour of the Tiger. Third packet. The boy's knees hurt. Through the gap he sees the magistrate pour a cup of water and leave it untouched beside three tea cups that were never his."

    voice "audio/voice/narrator_353.mp3"
    "The boy understands, without words, that the man inside drinks nothing offered and takes everything that signs."

    voice "audio/voice/kaoru_419.mp3"
    kaoru "Run."

    voice "audio/voice/narrator_334.mp3"
    "The screen shuts. The boy runs down the archive stairs counting coin he already earned. The magistrate never spoke to the corridor. He never speaks to you."

    jump case_zero_puppet_show


label case_zero_puppet_show:

    scene bg magistrate_office with dissolve
    show kaoru commanding at left

    voice "audio/voice/narrator_335.mp3"
    "Midday. Rain thins to mist. From the magistrate window the canal road is a stage the city forgot to charge admission for."

    voice "audio/voice/narrator_336.mp3"
    "A puppet show: villain in Scorpion purple, merchant in Crane white, a love plot the puppeteer sells with extra flourishes."

    voice "audio/voice/narrator_337.mp3"
    "The villain confesses greed. The children boo on cue. Kaoru watches from the sill with a cup he still will not drink."

    show kaoru smirk
    voice "audio/voice/kaoru_397.mp3"
    kaoru "Wrong motive. He killed for debt schedule, not passion. Ledger line due on the fifteenth. Wife already sold the comb."

    voice "audio/voice/kaoru_398.mp3"
    kaoru "Puppeteer, your villain emotes well and files poorly. Fear is cheaper than love in this quarter. Write that on your crate."

    voice "audio/voice/narrator_338.mp3"
    "Down on the stones the puppeteer bows to the empty window, not knowing who corrected him. Kaoru does not applaud."

    voice "audio/voice/kaoru_399.mp3"
    kaoru "Dancers make the same mistake. Pretty feet, wrong reason. I will know the difference when one knocks."

    voice "audio/voice/narrator_354.mp3"
    "Patronage appetite sits in his chest like a second seal. He watches the puppet merchant die for love and knows the city sells a prettier lie because pretty lies keep the quarter spending."

    voice "audio/voice/kaoru_420.mp3"
    kaoru "Sponsorship is not kindness. It is a calendar and a corridor and a body I intend to read like a docket."

    voice "audio/voice/kaoru_421.mp3"
    kaoru "When the renewal petition comes I will not be the villain in purple. I will be the stamp. That is scarier and more honest."

    menu case_zero_puppet_menu:
        "Let the show end without arrest.":
            $ case_zero_puppet_choice = "watch"
            voice "audio/voice/kaoru_400.mp3"
            kaoru "Street theater is not my docket unless it blocks my corridor."

        "Send a clerk to cite the crate for obstruction.":
            $ case_zero_puppet_choice = "cite"
            voice "audio/voice/kaoru_401.mp3"
            kaoru "Citation keeps the puppeteer honest and the children moving. File it."

    jump case_zero_bad_end_mirror


label case_zero_bad_end_mirror:

    scene bg street_exterior with fade
    hide kaoru
    play music audio.bgm_bad_end_rain fadein 2.0 loop volume 0.42

    voice "audio/voice/narrator_339.mp3"
    "Night. Same rain geometry the quarter uses when it sells what the ledger will not keep."

    voice "audio/voice/narrator_340.mp3"
    "Side alley between two shuttered tea houses. Dry enough to stand. Narrow enough to trap. The canal breathes wrong-green at the mouth."

    $ show_cg_scene("case_zero_rain_alley_door", fade)

    voice "audio/voice/narrator_341.mp3"
    "A woman without a chop. Not a petitioner for this story. A witness he could escort to the watch, or sign temporary custody, or pretend he did not see."

    voice "audio/voice/narrator_355.mp3"
    "She testified last week on a forgery line. Useful mouth. Spendable now that the factor paid the other side."

    voice "audio/voice/narrator_342.mp3"
    "Ronin arithmetic gathers at the alley lip. House of Falling Lanterns coin. Pretty hair. Wet obi. No magistrate escort."

    voice "audio/voice/narrator_356.mp3"
    "The same geometry a soaked Crane girl will meet if she walks out without his seal. Kaoru knows the map because he helped draw the lines."

    show kaoru cold at center with dissolve

    voice "audio/voice/kaoru_402.mp3"
    kaoru "Wrong quarter to be visible without my seal."

    voice "audio/voice/narrator_343.mp3"
    "She reaches for his sleeve. He steps back into the rain where ink belongs."

    voice "audio/voice/kaoru_403.mp3"
    kaoru "I could open the watch door. I could write you a corridor pass until dawn."

    voice "audio/voice/kaoru_404.mp3"
    kaoru "Instead I will close the other door."

    voice "audio/voice/narrator_344.mp3"
    "He signs a chit the ronin expect. Not her name. A fee line. The okami's arithmetic completes without him watching the cart."

    voice "audio/voice/kaoru_422.mp3"
    kaoru "You wanted my corridor. This is what my corridor costs when I do not lend it."

    play sound audio.door_slam volume 0.65

    voice "audio/voice/narrator_345.mp3"
    "The alley door shuts on someone else's fate. Harsh mercy: the ledger stays clean, the magistrate keeps his hands dry, Ryoko Owari keeps chewing what it cannot classify."

    voice "audio/voice/narrator_357.mp3"
    "From the cart lane he hears nothing he is required to record. Aftercare of power is a dry sleeve and a walk back to cedar where the cups wait, untouched."

    hide kaoru with dissolve
    voice "audio/voice/kaoru_405.mp3"
    kaoru "Witness spendable when the quarter pays better. Patronage is appetite with a stamp. I know what I am buying."

    voice "audio/voice/kaoru_423.mp3"
    kaoru "I could have opened the watch door. I chose the fee line. Do not call that romance. Call it jurisdiction."

    voice "audio/voice/narrator_346.mp3"
    "He walks back through rain that does not distinguish brothel geography from magistrate corridors. Dread is a clerk who already stamped tomorrow."

    voice "audio/voice/narrator_358.mp3"
    "Tomorrow someone will knock the wrong door and he will call it scheduling. Tonight he lets the dread sit in his gut like cold tea."

    scene bg magistrate_office with fade
    show kaoru commanding at left
    stop sound fadeout 1.5
    play music audio.bgm_office fadein 2.0 loop volume 0.35

    voice "audio/voice/narrator_359.mp3"
    "He washes his hands. The basin reflects a magistrate, not a man. Good. Men soften. Magistrates stamp."

    voice "audio/voice/kaoru_406.mp3"
    kaoru "Case Zero closes. Next petition lands when some Crane gets lost in my hall."

    voice "audio/voice/kaoru_407.mp3"
    kaoru "Renewal season. Wrong door season. I will drink none of the tea and take all of the witness."

    voice "audio/voice/kaoru_424.mp3"
    kaoru "Companion means my corridor, my hanko, my release. I wrote that line before she existed. I intend to fill the blank."

    voice "audio/voice/kaoru_408.mp3"
    kaoru "Almost-smile stays denied. The corridor stays mine."

    voice "audio/voice/narrator_360.mp3"
    "On the tray he aligns the unused cups with the water he poured for himself. Four vessels. Zero admissions. The docket is ready."

    play sound audio.footsteps_corridor volume 0.5

    voice "audio/voice/narrator_361.mp3"
    "Footsteps in the noble quarter. Lost. Crisp. A permit book clicking like obi bells."

    voice "audio/voice/kaoru_409.mp3"
    kaoru "Corridor's awake. Renewal season."

    voice "audio/voice/narrator_362.mp3"
    "He does not rise. Petitioners come to his desk or they do not come at all."

    voice "audio/voice/kaoru_410.mp3"
    kaoru "She will knock wrong first. They always do."

    voice "audio/voice/narrator_363.mp3"
    "The knock is too eager. Too Crane. He almost smiles. Denied."

    voice "audio/voice/kaoru_411.mp3"
    kaoru "Come back when you learn my corridor. You will."

    voice "audio/voice/kaoru_425.mp3"
    kaoru "Wrong door season. I will drink none of the tea."

    voice "audio/voice/narrator_364.mp3"
    "Case Zero ends where Case One begins: a door, a seal, a hunger dressed as law."

    voice "audio/voice/narrator_365.mp3"
    "The docket opens on the other side of the screen."

    scene black with fade
    pause 0.8

    centered "{size=-4}Case Zero filed.\nThe wrong door opens next.{/size}"

    jump prologue_start
