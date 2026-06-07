# Romance bonus epilogue: kotatsu afternoon after Case 5 Path A canon.
# Unlock: epilogue_romance_bonus_eligible() after case5_epilogue_week_one.
# VOICED: kaoru_361+, toa_297+, narrator_282+ (legacy MP3s on disk).

label epilogue_romance_bonus:

    $ case5_romance_bonus_seen = True
    $ cg_active = False
    $ hide_stage_sprites()

    scene op_kotatsu with fade
    play music audio.bgm_canon_intimate fadein 2.0 loop volume 0.42
    show kaoru charm at left
    show toa happy at right

    voice "audio/voice/narrator_282.mp3"
    "Afternoon off the ledger: no case number, no runner, only steam under the kotatsu and mikan peel curling on the tray."

    show toa soft
    voice "audio/voice/toa_297.mp3"
    toa "Yoriki paperwork says I must initial every quarter escort in triplicate. Your clerks invented a fourth copy while I bathed."

    show kaoru cold
    voice "audio/voice/kaoru_361.mp3"
    kaoru "Clerks sell courage by the cup. You sell me indignation by the segment."

    show toa flustered
    voice "audio/voice/toa_298.mp3"
    toa "I am teasing. You may almost smile if you try."

    show kaoru smirk
    voice "audio/voice/kaoru_362.mp3"
    kaoru "Almost is the only concession this office allows before sunset."

    voice "audio/voice/narrator_285.mp3"
    "The corner of his mouth twitches. Not quite a smile."

    pause 0.35

    show toa happy
    voice "audio/voice/toa_299.mp3"
    toa "Good. I will file that under victories too small for the docket."

    show kaoru charm
    voice "audio/voice/kaoru_363.mp3"
    kaoru "Eat your mikan. Drip on the yoriki sash and I will make you copy the stain into the record twice. I still take what I am owed."

    voice "audio/voice/narrator_283.mp3"
    "She passes him a segment anyway. He takes it without looking, as if hunger were a secret he refused to file, and her fingers on the peel a form he meant to seal later."

    show toa soft
    voice "audio/voice/toa_300.mp3"
    toa "No new case tonight. No seal stolen before dawn. Just this room."

    show kaoru satisfied at left
    voice "audio/voice/kaoru_364.mp3"
    kaoru "Just this room is still mine to share when the city is not listening. Do not make me say it twice."

    voice "audio/voice/toa_301.mp3"
    toa "Then I will stay where the ledger cannot count."

    voice "audio/voice/narrator_311.mp3"
    "Under the quilt edge, bare ankles and shared heat, wool and skin and the shallow depth of a room that keeps no ledger. Tactile warmth, not performance."

    $ show_cg_scene("epilogue_kotatsu_warmth", fade)
    pause 2.0

    $ show_cg_scene("epilogue_romance_kotatsu_intimate", fade)
    pause 2.5

    voice "audio/voice/narrator_284.mp3"
    "Rain ticks the eaves. The kotatsu holds their warmth and the peel and the almost-smile he will deny tomorrow. Ryoko Owari lies elsewhere. Here, for once, it does not matter who holds the key."

    pause 2.0
    scene black with fade
    pause 0.8

    # Canon capstone: roll the ED credits ("The Liar's String") as the emotional close
    # of the fully-romanced route, then the completion card.
    call ed_sequence from _ed_after_bonus_epilogue

    centered "{size=+4}Bonus epilogue complete{/size}\n{size=-4}Off the ledger.{/size}"

    menu epilogue_romance_bonus_exit:
        "Return to title.":
            stop music fadeout 2.0
            return

        "Main menu.":
            stop music fadeout 2.0
            $ renpy.full_restart()
