# Prologue choice-outcome CGs, one image per distinct branch beat.
# Map: docs/cg-choice-map.md
# Script vars: stats.rpy (door_response, formality_tone, discipline_check,
#   permit_strategy, unless_branch) + performance_boldness / rebuke / physical_initiative.

# --- After door slam (prologue_door_menu → door_response) ---
image cg choice door leave = At("images/cg/cg-choice-door-leave.png", fit_cg)           # leave
image cg choice door knock again = At("images/cg/cg-choice-door-knock-again.png", fit_cg) # knock_again
image cg choice door wait quietly = At("images/cg/cg-choice-door-wait-quietly.png", fit_cg) # wait_quietly

# --- Formality (prologue_formality_menu → formality_tone) ---
image cg choice formality hyper formal = At("images/cg/cg-choice-formality-hyper-formal.png", fit_cg) # hyper_formal
image cg choice formality direct = At("images/cg/cg-choice-formality-direct.png", fit_cg)             # direct
image cg choice formality humorous = At("images/cg/cg-choice-formality-humorous.png", fit_cg)         # humorous

# --- Entering office (prologue_enter_office_menu → discipline_check) ---
image cg choice office comply = At("images/cg/cg-choice-office-comply.png", fit_cg)           # discipline_check == 0
image cg choice office peek shelves = At("images/cg/cg-choice-office-peek-shelves.png", fit_cg) # discipline_check == 1

# --- Expired permit (prologue_expired_menu → permit_strategy) ---
image cg choice permit academy trip = At("images/cg/cg-choice-permit-academy-trip.png", fit_cg) # academy_trip
image cg choice permit local fix = At("images/cg/cg-choice-permit-local-fix.png", fit_cg)     # local_fix
image cg choice permit plead = At("images/cg/cg-choice-permit-plead.png", fit_cg)               # plead

# --- Before dance (prologue_before_dance_menu) ---
image cg choice dance negotiate = At("images/cg/cg-choice-dance-negotiate.png", fit_cg)   # negotiate terms (insight++)
image cg choice dance immediate = At("images/cg/cg-choice-dance-immediate.png", fit_cg)   # perform immediately
image cg choice dance refuse = At("images/cg/cg-choice-dance-refuse.png", fit_cg)         # prologue_refused_dance

# --- Performance tone (prologue_performance_menu → performance_boldness) ---
image cg choice performance formal = At("images/cg/cg-choice-performance-formal.png", fit_cg)       # formal fan dance
image cg choice performance flirtatious = At("images/cg/cg-choice-performance-flirtatious.png", fit_cg) # flirtatious

# --- Escalation at grab (prologue_grab_menu → rebuke / physical_initiative) ---
image cg choice grab rebuke = At("images/cg/cg-choice-grab-rebuke.png", fit_cg)   # rebuke (+rebuke)
image cg choice grab lean_in = At("images/cg/cg-choice-grab-lean-in.png", fit_cg) # lean in (+physical_initiative)

# --- Final "unless?" (prologue_unless_menu → unless_branch) ---
image cg choice unless verbal = At("images/cg/cg-choice-unless-verbal.png", fit_cg)     # verbal
image cg choice unless physical = At("images/cg/cg-choice-unless-physical.png", fit_cg) # physical
image cg choice unless walk out = At("images/cg/cg-choice-unless-walk-out.png", fit_cg)   # walk_out
