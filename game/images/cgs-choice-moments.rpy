# Pre-choice moment CGs, one image shown immediately before each menu: statement.
# Map: docs/cg-pre-choice-map.md
# Reuses existing beat/choice art where the beat matches; dedicated files otherwise.

# --- Prologue door (reuse corridor beat CG) ---
image cg moment prologue_door_choices = At("images/cg/cg-first-scene-corridor-lost.png", fit_cg)
image cg moment prologue_door_second_chance = At("images/cg/cg-first-scene-corridor-lost.png", fit_cg)

# --- Prologue formality / office entry ---
image cg moment prologue_formality_menu = At("images/cg/cg-choice-moment-prologue_formality_menu.png", fit_cg)
image cg moment prologue_enter_office_menu = At("images/cg/cg-choice-office-comply.png", fit_cg)

# --- Prologue permit / dance (reuse beat CGs, wired in script before these menus) ---
image cg moment prologue_expired_menu = At("images/cg/cg-first-scene-permit-desk.png", fit_cg)
image cg moment prologue_before_dance_menu = At("images/cg/cg-choice-moment-prologue_before_dance_menu.png", fit_cg)
image cg moment prologue_refuse_retry_menu = At("images/cg/cg-choice-dance-refuse.png", fit_cg)
image cg moment prologue_performance_menu = At("images/cg/cg-first-scene-office-dance.png", fit_cg)

# --- Prologue escalation / unless ---
image cg moment prologue_grab_menu = At("images/cg/cg-choice-grab-rebuke.png", fit_cg)
image cg moment prologue_unless_menu = At("images/cg/cg-first-scene-chair-tension.png", fit_cg)

# --- Case 1 companion ---
image cg moment case1_companion_accept_menu = At("images/cg/cg-first-scene-permit-desk.png", fit_cg)
image cg moment case1_first_duty_menu = At("images/cg/cg-choice-moment-case1_first_duty_menu.png", fit_cg)

# --- Case 1 investigation ---
image cg moment case1_briefing_menu = At("images/cg/cg-choice-moment-case1_briefing_menu.png", fit_cg)
image cg moment case1_canal_menu = At("images/cg/cg-case1-canal-body.png", fit_cg)
image cg moment case1_kaoru_probe_menu = At("images/cg/cg-case1-canal-body.png", fit_cg)

# --- Case 1 continuation (guest registry / licensed quarter) ---
# Dedicated CGs generated per docs/case1-investigation-scene.md (prompts retained below for regen).
image cg moment case1_registry_menu = At("images/cg/cg-case1-licensed-quarter.png", fit_cg)
image cg moment case1_witness_menu = At("images/cg/cg-case1-guesthouse-suzu.png", fit_cg)
image cg moment case1_ledger_menu = At("images/cg/cg-case1-registry-ledger.png", fit_cg)

# --- Case 1 finale (barge) ---
image cg moment case1_barge_menu = At("images/cg/cg-case1-high-tide-barge.png", fit_cg)

# --- Case 2 investigation (Academy packet) ---
image cg moment case2_briefing_menu = At("images/cg/cg-case2-academy-desk.png", fit_cg)
image cg moment case2_alley_menu = At("images/cg/cg-case2-alley-courier.png", fit_cg)
image cg moment case2_desk_menu = At("images/cg/cg-case2-warehouse-ash.png", fit_cg)

# --- Case 3 investigation (fabric shop) ---
image cg moment case3_briefing_menu = At("images/cg/cg-case3-fabric-shop.png", fit_cg)
image cg moment case3_investigation_menu = At("images/cg/cg-case3-fabric-shop.png", fit_cg)
image cg moment case3_accident_menu = At("images/cg/cg-case3-accident-moment.png", fit_cg)

# --- Case 4 investigation (dock raid) ---
image cg moment case4_investigation_menu = At("images/cg/cg-case4-gritty-establishing.png", fit_cg)
image cg moment case4_swordfight_crisis_menu = At("images/cg/cg-case4-fight-wide.png", fit_cg)

# --- Case 4.5 Teardrop kobune ---
image cg moment case4_5_boat_crisis_menu = At("images/cg/cg-case4_5-boat-duo-tense.png", fit_cg)
# Deprecated supper moments (save compat / gallery refs if any):
image cg moment case4_briefing_menu = At("images/cg/cg-case2-academy-desk.png", fit_cg)
image cg moment case4_table_menu = At("images/cg/cg-case1-licensed-quarter.png", fit_cg)

# Generation prompts (Hakuoki shoujo, painterly, no text):
#   cg-case1-licensed-quarter.png: Rainy night in a Legend of the Five Rings canal pleasure
#     district, Hakuoki shoujo visual-novel CG. Wine-red paper lanterns reflected in black canal water, a
#     two-story cedar guest house ("the Lacquered Plum") on stilts over the water, a painted three-eyed crow
#     sign on the gable, soft rain, moody teal-and-gold palette, no characters, 16:9.
#   cg-case1-guesthouse-suzu.png: Hakuoki shoujo CG, lamplit tatami room. A frightened young
#     geisha (Suzu, ~19, white makeup cried through at the edges) kneeling and holding a black lacquer comb
#     inlaid with a red Scorpion mon; Kakita Toa (cheerful Crane woman in white hakama) kneeling at her level;
#     Kitsu Kaoru (cold mid-30s Emerald Magistrate in gold-trimmed robes) looming in the doorway. Warm/cold
#     light contrast, rain at the window, 16:9.
#   cg-case1-registry-ledger.png: Hakuoki shoujo CG close-up of an open guest-registry book on
#     a low desk, a forged Emerald Magistrate wax seal (chrysanthemum mon, too many petals) beside a brush
#     entry, a Scorpion lacquer comb in a lacquer evidence tray, lamplight, foreign silver coin, 16:9.
