# Modern AU: Wrong Floor (main-menu bonus + dev chapter pick).
#
# Play: Main menu → "Bonus: Wrong Floor (Modern AU)"; or dev chapter pick → "AU: Wrong Floor (Modern)".
# Optional new-game gate (default OFF): persistent.play_au_modern_wrong_floor in script.rpy.
# Exit: au_modern_wrong_floor_end → dev menu or main menu.
# VOICED: narrator_366-385, 420-424; toa_365-382; kaoru_487-510, 548 (manifest wired; regen via scripts/au_modern_voice_ids.txt).
# Does not set canon case/permit flags.

default seen_au_modern_wrong_floor = False
default au_modern_door_response = ""
default au_modern_contract_choice = ""
default au_modern_unless_taken = False

label au_modern_wrong_floor_start:

    ## Launched in the rollback-enabled game (root) context, from the Modern AU hub
    ## (au_modern_hub_menu) or the dev chapter pick. Because this is the normal game
    ## context (not a call_in_new_context child of the menu), Back/rollback, mid-episode
    ## saving, character + narrator voices, and the quick/game menu all work without any
    ## menu-state fix-ups. Mark the AU episode active so the story-music mute callback
    ## keeps story BGM audible (incl. after loading a mid-episode save).
    $ au_episode_active = True
    $ enable_cinematic_music()

    $ seen_au_modern_wrong_floor = True
    $ au_modern_door_response = ""
    $ au_modern_contract_choice = ""
    $ au_modern_unless_taken = False

    scene black with fade
    play music audio.bgm_office fadein 2.5 loop volume 0.32

    centered "{font=fonts/YujiSyuku-Regular.ttf}{size=+6}Wrong Floor{/size}{/font}\n{size=-4}Modern AU · Ryoko Port · dev bonus{/size}"

    pause 1.0

    $ show_cg_scene("au_modern_tower_establishing", fade)
    pause 1.5

    voice "audio/voice/narrator_366.mp3"
    "Rain needles the harbor glass. Under the municipal licensing tower, the parking structure is a cathedral of dripping concrete, fluorescents buzzing while ferries cough diesel into the channel below. This is where Kakita Toa starts the morning she means to spend fixing her papers, and where Ryoko Port quietly decides it will not be that simple."

    voice "audio/voice/narrator_367.mp3"
    "Ryoko Port keeps its appointments under fluorescent mercy and never apologizes for the weather. The municipal tower hums like a printer that learned to judge people. Floor fourteen B belongs to the Ryoko Port Arts Council, the board that decides which artists the port will license at all, and renewing the sponsorship she had let lapse was supposed to be the easy part of her morning."

    voice "audio/voice/narrator_472.mp3"
    "The Arts Council is the body that decides who gets to make art in this port and who only gets to watch it from the cheap seats. It funds the performing-arts sponsorships, licenses the venues and storefronts, and streams its hearings straight onto the public record. A sponsorship is the Council's permission slip: with one, a transfer dancer may legally rehearse, perform, be paid, and stay. Without one she is a tourist with good posture and a packet six weeks expired."

    $ show_cg_scene("au_modern_rain_parking", fade)
    pause 1.5

    voice "audio/voice/toa_365.mp3"
    toa "The elevator map said fourteen B. The packet said fast track. Those two facts have not shaken hands yet."

    voice "audio/voice/narrator_368.mp3"
    "Toa clutches a tablet sleeve, expired sponsorship packet, and the personal stamp she was told to bring to every bureaucratic threshold. Crane logo on her rehearsal jacket, not costume. Ballet flats soaked through anyway."

    voice "audio/voice/narrator_469.mp3"
    "The public elevator lets her out on floor fourteen B, and on the wrong half of it. Intake, the counter where applicants take a number and wait their turn, is one wing over. Toa turns the other way, toward a glass door with a badge reader, and opens it without reading the plate."

    jump au_modern_wrong_door


label au_modern_wrong_door:

    if au_modern_door_response == "leave":
        voice "audio/voice/narrator_420.mp3"
        "She found the Office of Arts and Licensing again anyway, the deputy directors' wing where intake's mistakes came to be signed or denied. The plate still read Deputy Director. The hearing still glowed on his monitor, unmuted, as if the building had saved her seat."

    $ show_cg_scene("au_modern_wrong_floor", fade)
    pause 2.0

    voice "audio/voice/kaoru_487.mp3"
    kaoru "Wrong conference room. Again."

    voice "audio/voice/toa_366.mp3"
    toa "I wasn't... that is, I'm looking for Arts Council sponsorship intake?"

    voice "audio/voice/kaoru_488.mp3"
    kaoru "You opened the door to the Office of Arts and Licensing without reading the plate. Intake is the other wing, where applicants wait their turn. This wing is where I decide whether intake wasted its morning. Reading the wrong door is a skill, not an excuse."

    voice "audio/voice/narrator_369.mp3"
    "On the deputy director's monitor, an Arts Council board member freezes mid-objection. The hearing is live, unmuted, gallery view tiled with councilors and clerks who have never danced for a living. The chat scrolls before she has finished apologizing."

    voice "audio/voice/narrator_473.mp3"
    "It is a live Arts Council licensing hearing, the kind Ryoko Port streams straight onto the public record. The board votes on contested permits in full view of anyone bored enough to watch. Whatever the gallery types becomes minutes. Whatever the camera catches becomes, eventually, a clip."

    menu au_modern_door_menu:

        "Leave and find Arts Council on fourteen B.":
            $ au_modern_door_response = "leave"
            voice "audio/voice/toa_367.mp3"
            toa "Fine. I'll find a deputy with better signage."

            $ show_cg_scene("au_modern_intake_counter", fade)
            pause 2.0

            voice "audio/voice/narrator_370.mp3"
            "At the Arts Council intake counter two wings over, a junior clerk squints at her packet, circles the expiration date a second time in the same red, and points her back the way she came. Intake takes the form. Intake does not sign it."

            voice "audio/voice/toa_368.mp3"
            toa "Kitsu Kaoru, Deputy Director? That glass door with the badge reader?"

            jump au_modern_wrong_door

        "Knock again, properly this time.":
            $ au_modern_door_response = "knock"
            voice "audio/voice/toa_369.mp3"
            toa "Third time's the charm. Or the deputy director. Hopefully both."

            jump au_modern_permit_crisis

        "Wait quietly until invited.":
            $ au_modern_door_response = "wait"
            $ show_cg_scene("au_modern_wrong_floor_wait", fade)
            pause 2.0

            voice "audio/voice/narrator_371.mp3"
            "Toa straightens her rehearsal jacket, breathes, and tries not to look like a dancer lost in a tax form. Pride and panic share a spine."

            voice "audio/voice/kaoru_489.mp3"
            kaoru "Still there? Knock if you want something other than a live Council hearing to fail on the public record."

            jump au_modern_permit_crisis


label au_modern_permit_crisis:

    scene black with dissolve
    pause 0.4

    $ show_cg_scene("au_modern_zoom_hearing", fade)
    pause 2.0

    voice "audio/voice/narrator_421.mp3"
    "Kitsu Kaoru let her in the way a gate let in weather: as fact, not favor. Cold mug. Files tied with string the stapler could not be trusted to hold."

    voice "audio/voice/narrator_372.mp3"
    "He does not look up from two monitors until she sits in the chair beside the screen, not the one facing him. Witness posture lives there, he says later. Stage posture dies in the chat."

    voice "audio/voice/kaoru_490.mp3"
    kaoru "Crane Conservatory transfer packet. Expired six weeks ago. You walked into my live hearing like a pop-up ad."

    voice "audio/voice/toa_370.mp3"
    toa "The transfer letter said Ryoko Port had a fast track for performing arts sponsorship."

    voice "audio/voice/kaoru_491.mp3"
    kaoru "Ryoko Port has a queue. You are in it now, whether you intended to be or not."

    voice "audio/voice/kaoru_593.mp3"
    kaoru "The fast track your letter promised is not a faster queue. It is a signature. A Council sponsorship is only valid once a deputy director signs for the applicant. I am the deputy director on this floor. That is the line your transfer letter left out."

    voice "audio/voice/toa_465.mp3"
    toa "So the fast track is a person. And I opened his door by accident, on camera."

    voice "audio/voice/narrator_422.mp3"
    "The board member on screen clears his throat with performative patience. The chat lit up in order: *Unprofessional* from a ward tile. *Who is she* from someone who filed complaints for sport. *Hair like a press release* from a thread that used emoji in the official minutes."

    voice "audio/voice/narrator_373.mp3"
    "Toa kept her hands on her knees and her eyes on the edge of his monitor, where rain smeared the window. Every syllable landed on her spine like a sticker she could not peel off."

    voice "audio/voice/toa_371.mp3"
    toa "Can I at least not be the reason your Zoom looks unprofessional?"

    voice "audio/voice/kaoru_492.mp3"
    kaoru "You already are. Sit. Witness posture. Not performance posture. I will audit both."

    voice "audio/voice/narrator_423.mp3"
    "Deputy Director, the board member said, your applicant is blocking the agenda."

    voice "audio/voice/kaoru_548.mp3"
    kaoru "My applicant is seated where I placed her. If the agenda cannot tolerate a witness, revise the agenda."

    $ show_cg_scene("au_modern_postit_witness", fade)
    pause 1.5

    voice "audio/voice/narrator_374.mp3"
    "Yellow paper slides across the desk edge in block letters. Do not speak unless prompted. Dates and names only. A second note repeats the difference: witness posture, not performance posture. Someone laughed in a tile and muted themselves. Kaoru unmuted no one."

    voice "audio/voice/narrator_424.mp3"
    "He mutes the gallery with two keystrokes, not apology, and types one line without looking at her: witness only, do not engage."

    voice "audio/voice/kaoru_493.mp3"
    kaoru "Applicant present for sponsorship review. Packet error is mine to remediate. Continue your agenda item."

    voice "audio/voice/narrator_375.mp3"
    "When the board member asks whether Arts Council intake sent her, Kaoru says intake sent her to the wrong floor, so he is intake now. That is not comfort. It is jurisdiction, and she discovers she prefers jurisdiction to kindness, because kindness in this port always arrives with an expiration date and a clerk who is not present to be argued with."

    jump au_modern_studio_audition


label au_modern_studio_audition:

    scene black with fade
    pause 0.5

    $ show_cg_scene("au_modern_studio_audition", fade)
    pause 2.0

    voice "audio/voice/narrator_376.mp3"
    "When the hearing ends without praise, he hands her a studio key and a hallway that smells of floor wax and rain. The city rents the rehearsal room by the hour to applicants who need to prove, in a mirror, that they are more than a packet error. Prove it, and the deputy signs. That is the only fast track Ryoko Port actually keeps."

    # Novel beat: ryoko-owari-au-modern-wrong-floor.md (mirror, barre, witness counting).
    $ show_cg_scene("toa_ballet_practice_room", fade)
    pause 2.0

    voice "audio/voice/toa_372.mp3"
    toa "You want me to audition for a permit extension?"

    voice "audio/voice/kaoru_494.mp3"
    kaoru "I want proof you can follow choreography that is not flirting with clerks. Run the phrase."

    voice "audio/voice/narrator_377.mp3"
    "Mirror wall. Barre. Rain ticking the glass like a clerk tapping a stamp. She runs the phrase once. Apology still lives in her shoulders. He counts under his breath like a man checking witness notes, not applause."

    voice "audio/voice/kaoru_495.mp3"
    kaoru "Again. Less apology in the port de bras."

    voice "audio/voice/toa_373.mp3"
    toa "That one was clean. You counted out loud."

    voice "audio/voice/kaoru_496.mp3"
    kaoru "Counting is witness work. Stop expecting applause from a licensing officer."

    voice "audio/voice/kaoru_594.mp3"
    kaoru "If I sign your sponsorship, I swear to the Council that you are an artist and not a story about fraud waiting to happen. The board takes my word because I do not give it cheaply. So give me an artist to swear to."

    voice "audio/voice/toa_466.mp3"
    toa "And here I thought I was auditioning for a permit. I am auditioning for your signature."

    jump au_modern_contract_menu


label au_modern_contract_menu:

    $ show_cg_scene("au_modern_contract_desk", fade)
    pause 1.5

    voice "audio/voice/narrator_470.mp3"
    "Back in the licensing office, the audition behind her, the sponsorship draft waits on his desk. His signature is ready. The only thing still hers to decide is which rider hangs off it."

    voice "audio/voice/kaoru_497.mp3"
    kaoru "Two riders on the sponsorship draft I am prepared to sign. Pick one before I file you under *disruptive applicant* and let the queue keep you."

    voice "audio/voice/narrator_474.mp3"
    "The sponsorship itself is plain enough once someone explains the boxes. The Arts Council authorizes her to work as a performing artist in the port, and the deputy director's signature on the form vouches to the Council that she will not embarrass the seal that backs her. The riders do not change that. They only decide how close the deputy who signed it has to stand while his name is the one on the line for her. Both riders carry the same fine print, the witness clause: a fast-tracked artist must attend the deputy's inspections and document them, living proof for the Council that he does not hand permits to dancers he happens to favor. She does not learn what that costs until later. Today it is only a line she initials."

    menu au_modern_contract_choices:

        "Standard performance rider (professional terms).":
            $ au_modern_contract_choice = "standard"
            voice "audio/voice/toa_374.mp3"
            toa "Standard rider. Discretion, attendance, and no social posts that tag municipal accounts."

            $ show_cg_scene("au_modern_standard_rider", fade)
            pause 2.0

            voice "audio/voice/kaoru_498.mp3"
            kaoru "Correct. Boring is enforceable. I can work with boring."

            jump au_modern_curry_breakroom

        "Exclusive rehearsal sponsor (after-hours access).":
            $ au_modern_contract_choice = "exclusive"
            voice "audio/voice/toa_375.mp3"
            toa "Exclusive rehearsal sponsor. After-hours studio access and direct deputy review."

            voice "audio/voice/kaoru_499.mp3"
            kaoru "You understand that clause includes my calendar, not romance on letterhead."

            voice "audio/voice/toa_467.mp3"
            toa "I understand paperwork. I am very good at paperwork when someone explains the boxes. *Direct deputy review.* I read that line three times, and my pulse did something unprofessional each time."

            $ show_cg_scene("au_modern_phone_date", fade)
            pause 1.5

            jump au_modern_elevator_unless


label au_modern_elevator_unless:

    voice "audio/voice/narrator_378.mp3"
    "Building hour passes six. The official business is filed, the contract floor goes dark, and the public elevators sigh into standby one by one. Only the service lift still answers when he badges it, a dull metal box that does not appear on the map tourists photograph."

    voice "audio/voice/kaoru_500.mp3"
    kaoru "Unless?"

    voice "audio/voice/toa_376.mp3"
    toa "That is not a municipal form."

    voice "audio/voice/kaoru_501.mp3"
    kaoru "The contract floor is closed. This floor is not on your calendar. Get in."

    $ show_cg_scene("au_modern_elevator", fade)
    pause 2.0

    voice "audio/voice/narrator_379.mp3"
    "Rain stripes the glass on the way down. The car shudders once, as if the building cleared its throat. His badge taps the reader on a floor that does not appear on the public map."

    $ show_cg_scene("au_modern_unless_lift_kiss", dissolve)
    pause 2.0

    voice "audio/voice/narrator_380.mp3"
    "She does not pretend, afterward, that nothing happened. Whatever the service lift was, every form that matters will still file it as sponsorship: after-hours rehearsal access, logged under the exclusive rider she signed with her eyes open. The seal stays professional on paper. The rest stays off the public record, which is exactly what that rider is for."

    $ au_modern_unless_taken = True

    voice "audio/voice/kaoru_502.mp3"
    kaoru "Quiet. You wanted exclusive rehearsal. I audit deliverables."

    voice "audio/voice/toa_377.mp3"
    toa "Then audit quietly, Deputy Director-sama. The building still has ears."

    scene black with fade
    pause 0.5

    jump au_modern_curry_breakroom


label au_modern_curry_breakroom:

    scene black with dissolve
    play music audio.bgm_office fadein 2.0 loop volume 0.38

    voice "audio/voice/narrator_381.mp3"
    "The next midday she comes back to the tower, not as a lost applicant this time but as a woman cooking thank-you curry in the municipal break room, which smells of roux and a little guilt. Fluorescents hum. Rain keeps filing itself against the window. Somewhere upstairs a printer jams and someone swears with the tenderness of a prayer."

    voice "audio/voice/toa_378.mp3"
    toa "They don't give case numbers upstairs. So today I am cooking thank-you curry, not filing a report about it."

    voice "audio/voice/kaoru_503.mp3"
    kaoru "The break room is not a courtroom. Neither is the lid of that pot."

    voice "audio/voice/toa_379.mp3"
    toa "I brought the stamp. A proper hanko makes everything official, does it not?"

    $ show_cg_scene("au_modern_curry_breakroom", fade)
    pause 2.0

    voice "audio/voice/kaoru_504.mp3"
    kaoru "Official lentils are still lentils. Put my chop on paper, not on your paper plate."

    $ show_cg_scene("au_modern_breakroom_sink", dissolve)
    pause 2.0

    voice "audio/voice/narrator_382.mp3"
    "He eats without praise and without flinching, as though his jurisdiction now extends to broth. Toa watches his chopsticks and tries not to hope too visibly."

    jump au_modern_signing


label au_modern_signing:

    scene black with fade
    pause 0.4

    $ show_cg_scene("au_modern_contract_desk", dissolve)
    pause 1.0

    voice "audio/voice/narrator_383.mp3"
    "The sponsorship contract returns to her tablet sleeve with a fresh effective date. Three business days. Not a love letter. Still binding. She reads the effective line twice because numbers are safer than whatever lives in her chest when he stands too close in an elevator."

    voice "audio/voice/kaoru_505.mp3"
    kaoru "Three business days effective. Do not perform gratitude on municipal letterhead."

    voice "audio/voice/toa_380.mp3"
    toa "Filed. And I promise I will not stamp disposable tableware again."

    voice "audio/voice/kaoru_506.mp3"
    kaoru "See that you don't. The queue remembers applicants who treat stamps like confetti."

    if au_modern_contract_choice == "exclusive" and au_modern_unless_taken:
        voice "audio/voice/narrator_384.mp3"
        "After hours, his office couch accepts two people who still call it sponsorship on every form that matters. Harbor lights smear across the window."

        $ show_cg_scene("au_modern_office_intimate", fade)
        pause 2.0

        voice "audio/voice/kaoru_507.mp3"
        kaoru "Blanket is a loan against your noise. Snore, and I reassign you to the public waiting area."

        voice "audio/voice/toa_381.mp3"
        toa "Then I'll file my breathing under acceptable noise. Good night, Deputy Director-sama."

    jump au_modern_stinger_couch


label au_modern_stinger_couch:

    scene black with fade
    pause 0.5

    $ show_cg_scene("au_modern_couch_stinger", fade)
    pause 2.0

    voice "audio/voice/narrator_385.mp3"
    "Clementines on the armrest, bright as small suns he will deny noticing. Shared blanket. Almost-smile inventory: denied, pending, denied again."

    voice "audio/voice/kaoru_508.mp3"
    kaoru "Peel one. Domestic filing. I will deny that too until the port stops selling what I intend to keep."

    voice "audio/voice/toa_382.mp3"
    toa "You almost smiled when I said thank-you curry, didn't you?"

    voice "audio/voice/kaoru_509.mp3"
    kaoru "Motion denied. Good night, To-chan."

    voice "audio/voice/kaoru_510.mp3"
    kaoru "Floor fourteen B is still the wrong door tomorrow. Try reading the plate first."

    pause 1.5

    jump au_modern_wrong_floor_end


label au_modern_wrong_floor_end:

    scene black with fade
    stop music fadeout 2.0

    centered "{size=+2}Wrong Floor (Modern AU){/size}\n{size=-4}Dev bonus complete.{/size}"

    pause 1.0

    menu au_modern_continue_case1_menu:

        "Continue to Case 1: Wellness Compliance?":
            jump au_modern_case1_start

        "Return to menu.":
            pass

    if dev_chapter_pick_enabled:
        jump dev_chapter_pick_menu

    ## Back to the Modern AU hub (rollback-enabled game context). The hub clears
    ## au_episode_active and restores the menu theme.
    jump au_modern_hub_menu
