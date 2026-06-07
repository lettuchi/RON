# Lightweight investigation stats for Milestone B.

default insight = 0
default composure = 0
default honor = 0

default kaoru_submission = 0
default kaoru_resistance = 0

# --- Prologue first-scene flags (see docs/first-scene-analysis.md) ---

# Kaoru route axes, incremented by prologue choices; gate future intimacy beats.
default compliance = 0           # Yielding to Kaoru's demands and prolongation
default performance_boldness = 0 # Flirtatious performance vs formal fan dance
default rebuke = 0               # Push back on physical escalation (grab)
default physical_initiative = 0  # Lean in / physical answer to "unless?"

# Prologue choice bookkeeping, string labels for branch routing in Case 0+.
default door_response = ""       # leave / knock_again / wait_quietly
default formality_tone = ""      # hyper_formal / direct / humorous
default discipline_check = 0       # +1 if peeked at shelves (Kaoru notices)
default permit_strategy = ""       # academy_trip / local_fix / plead
default performance_style = ""     # formal_dance / flirtatious
default negotiated_terms = False   # True if player bargained before the audition
default door_left_once = False     # True after first "leave" corridor wander
default unless_branch = ""         # verbal / physical / walk_out, cliffhanger route label

# Canon first-scene resolution (physical "unless?" → Case 1 true route)
default permit_signed = False
default permit_effective_days = 0    # 0 = unsigned; 3 = signature dated forward (canon)
default canon_first_scene = False

# --- Case 1 companion arrangement (canon path, three days after prologue) ---

default live_in_companion = False
default companion_accept_tone = ""   # graceful / negotiate / gush

# --- Case 1 investigation (canal body opening) ---

default case1_briefing_choice = ""   # detail / politics / professional
default case1_observation = ""       # Canal menu observation tag
default case1_physical_clue = ""     # scorpion_comb
default case1_victim_name = ""       # Filled when haori letter identifies the dead
default case1_clue_found = False     # True after scorpion comb secured
default case1_probe_response = ""    # eager / defer / pushback / defiance, Kaoru's canal test
default case1_punishment_entry = ""   # canal / registry / fail, bridge before punishment CG
default case1_milestone = ""         # Next beat gate (e.g. miya_guest_registry_next)

# --- Case 1 continuation (guest registry / licensed quarter, day two) ---

default case1_registry_approach = "" # credentials / quiet / kaoru_lead, how they enter the Plum
default case1_witness_name = ""       # Geisha witness who knew Jiro (Suzu)
default case1_forged_seal = False     # True once the false Emerald writ is found
default case1_ledger_choice = ""      # record / copy / trust, what to do with the forged writ

# --- Case 1 finale (high-tide barge) ---

default case1_barge_approach = ""       # stealth / official / split, boarding the Scorpion barge
default case1_manifest_seized = False # True once false rice/resin manifest secured
default case1_closed = False            # True after case1_barge_milestone_end

# --- Case 1 romance / bad end (case_endings.rpy) ---
default case1_kaoru_trust = 0           # Investigation-bond score; >= 4 unlocks trust route
default case1_sponsorship_flirt = False # Patronage-tension beat (companion prelude / boldness)
default case1_romance_route = ""        # trust / sponsorship / default, set at romance router

# --- Case 2 investigation (Academy packet / burned courier) ---

default case2_briefing_choice = ""      # route / politics / witnesses
default case2_confront_choice = ""      # accuse / trap / defer, outer-desk clerk
default case2_courier_name = ""         # Tsubaki
default case2_packet_found = False
default case2_milestone = ""            # case2_closed
default case2_closed = False

# --- Case 2 festival interlude (case2_festival.rpy) ---

default case2_festival_seen = False
default case2_festival_kiss_only = False
default case2_festival_intimate = False

# --- Case 3 investigation (kimono fabric shop / bolt-room accident) ---

default case3_started = False
default case3_briefing_choice = ""       # ledger / witness / scorpion_thread
default case3_clue_bolt = False          # mis-tagged Scorpion dye lot on bolt ends
default case3_clue_clerk = False         # clerk's second ledger under the counter
default case3_clue_shelf = False         # shelf brace scored, not age, fresh cut
default case3_accident_choice = ""       # trust_kaoru / dodge_alone
default case3_accident_avoided = False
default case3_kaoru_rescue = False
default case3_bad_end_injury = False
default case3_closed = False

# --- Case 4 investigation (dock raid / Kurogane swordfight) ---

default case4_started = False
default case4_investigation_choice = ""  # crate / watchman / stairs (dock raid)
default case4_briefing_choice = ""       # deprecated, supper arc (save compat)
default case4_table_choice = ""          # deprecated, supper arc (save compat)
default case4_suspect_named = False
default case4_suspect_name = ""          # Kurogane when named
default case4_toa_slain = False          # dock swordfight bad end
default case4_bad_end_abandoned = False  # deprecated, supper walk-out (save compat)
default case4_kaoru_defended = False     # dock swordfight romance beat
default case4_closed = False

# --- Case 4.5 interlude (canal boat / 舟の帳) ---

default case4_5_boat_interlude_seen = False
default case4_5_boat_choice = ""       # trust_warm / defy_cold
default case4_5_boat_fall_choice = ""  # trust_fall / fight_fall
default case4_5_boat_survived = False
default case4_5_bad_end_boat_injury = False

# --- Case 3.5 interlude ("Is this a date?"), legacy flag name ---

default case4_date_interlude_seen = False  # True when Case 3.5 interlude viewed
default is_this_a_date_asked = False

# --- Case 5 investigation (The Left Hand / yoriki hearing) ---

default case5_started = False
default case5_false_exit_seen = False
default case5_hearing_attended = False
default case5_yoriki_offered = False
default case5_yoriki_accepted = False
default case5_yoriki_refused = False
default case5_private_confession = False
default case5_private_intimacy = False
default case5_closed = False
default case5_romance_bonus_seen = False

# --- Case romance / bad endings (case_endings.rpy) ---
# seen_gameover_case4_5, seen_gameover_case5, defined in case_endings.rpy
# seen_gameover_case1, seen_gameover_case2, seen_gameover_case3, seen_gameover_case4
# case1_romance_seen, case2_romance_seen, defined in case_endings.rpy

# --- Modern AU Case 3: Permits & HR (au_modern_case3_permits_hr.rpy) ---
# Isolated bonus flags; do NOT gate canon. Wrong Floor / Case 1 / Case 2 declare
# their own AU defaults inline in their .rpy files; Case 3's live here per project
# convention so the new choices are read-not-dead (see signatory desk + reconcile reads).

default seen_au_modern_case3 = False
default au_modern_case3_statement = ""    # "" / public / quiet (Menu 1: viral-clip posture)
default au_modern_case3_disclosure = ""   # "" / procedural / personal (Menu 2: signatory conflict)

# --- Modern AU Epilogue: Effective Immediately (au_modern_epilogue.rpy) ---
# Final Modern AU episode. Isolated bonus flags; do NOT gate canon. Each choice flag
# below is read later in the same episode (no dead flags): waiting -> smile beat + closure
# narration; posture -> closure callback; audit -> branch + end-stinger card. The episode
# also reads existing AU flags (au_modern_case3_disclosure, au_modern_case2_night_audit)
# for continuity callbacks.

default seen_au_modern_epilogue = False
default au_modern_epilogue_waiting = ""    # "" / immediate / three_days (Menu 1: letterhead waiting period)
default au_modern_epilogue_posture = ""    # "" / witness / uncurled (Menu 2: harbor witness posture)
default au_modern_epilogue_audit = False   # Menu 3 consent gate: True = after-hours audit branch
