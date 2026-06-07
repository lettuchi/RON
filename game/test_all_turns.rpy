# Screenshot every dialogue turn on the canon playthrough path.
#
# Re-run (from repo root):
#   /path/to/renpy-8.5.3-sdk/renpy.sh ryoko-owari test screenshot_all_turns::canon_all_dialogue --overwrite-screenshots
#
# Regenerate static turn inventory (all branches in source):
#   python3 scripts/build_screenshot_turn_map.py
#
# Output: screenshots/review-2026-06-02/canon-turns/turn_NNN.png (+ _menu at choices)
# Legacy path docs/test-screenshots/turns/, superseded by review folder (Jun 2026).
# Branch policy: docs/screenshot-turn-map.json → canon_screenshot_branch

init python:
    import json
    import os

    _SCREENSHOT_OUTPUT_DIR = os.path.join(renpy.config.basedir, "screenshots/review-2026-06-02/canon-turns")
    os.makedirs(_SCREENSHOT_OUTPUT_DIR, exist_ok=True)

    _screenshot_turn_n = 0
    _screenshot_menu_count = 0
    _screenshot_menu_caption = ""
    _screenshot_reached_milestone_end = False
    _screenshot_tail_steps = 0
    _screenshot_max_steps = 450
    _screenshot_skipped = []
    _SCREENSHOT_UNLESS_MENU_ORDINAL = 8  # 0-based: 9th menu → physical (index 1)

    _turn_map_path = os.path.join(renpy.config.basedir, "docs/screenshot-turn-map.json")
    if os.path.isfile(_turn_map_path):
        with open(_turn_map_path, encoding="utf-8") as f:
            _turn_map_data = json.load(f)
        _screenshot_max_steps = int(_turn_map_data.get("turn_count", 369)) + 90

    def _screenshot_reset_run_state():
        global _screenshot_turn_n, _screenshot_menu_count, _screenshot_menu_caption
        global _screenshot_reached_milestone_end, _screenshot_tail_steps
        _screenshot_turn_n = 0
        _screenshot_menu_count = 0
        _screenshot_menu_caption = ""
        _screenshot_reached_milestone_end = False
        _screenshot_tail_steps = 0

    def _screenshot_turn_path(suffix=""):
        global _screenshot_turn_n
        _screenshot_turn_n += 1
        base = "screenshots/review-2026-06-02/canon-turns/turn_{:03d}".format(_screenshot_turn_n)
        if suffix:
            base += suffix
        return base

    def _screenshot_save_png(rel_base):
        filename = os.path.join(renpy.config.basedir, rel_base + ".png")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        img = renpy.display.draw.screenshot(renpy.game.interface.surftree)
        renpy.display.scale.image_save_unscaled(img, filename)
        del img

    def _screenshot_menu_choice_index():
        global _screenshot_menu_count
        idx = 1 if _screenshot_menu_count == _SCREENSHOT_UNLESS_MENU_ORDINAL else 0
        _screenshot_menu_count += 1
        return idx

    def _screenshot_click_menu():
        global _screenshot_menu_caption
        screen = renpy.get_screen("choice")
        if screen is None:
            _screenshot_menu_caption = ""
            _screenshot_skipped.append("menu_screen_missing")
            return
        items = screen.scope.get("items", [])
        if not items:
            _screenshot_menu_caption = ""
            _screenshot_skipped.append("menu_items_empty")
            return
        choice_idx = _screenshot_menu_choice_index()
        choice_idx = min(choice_idx, len(items) - 1)
        item = items[choice_idx]
        _screenshot_menu_caption = item.caption
        renpy.run(item.action)

    def _screenshot_label_callback(name, abnormal):
        if name == "case1_investigation_milestone_end":
            global _screenshot_reached_milestone_end, _screenshot_tail_steps
            _screenshot_reached_milestone_end = True
            _screenshot_tail_steps = 30

    def _screenshot_should_stop():
        if _screenshot_turn_n >= _screenshot_max_steps:
            return True
        if _screenshot_reached_milestone_end and _screenshot_tail_steps <= 0:
            return True
        ctx = renpy.game.context()
        if _screenshot_turn_n > 8 and ctx.current is None and not renpy.get_screen("choice") and not renpy.get_screen("say"):
            return True
        return False

    def _screenshot_tick_tail():
        global _screenshot_tail_steps
        if _screenshot_reached_milestone_end and _screenshot_tail_steps > 0:
            _screenshot_tail_steps -= 1

    def _screenshot_drive_ready():
        """Until-condition: True when the advance-until loop should stop."""
        if _screenshot_should_stop():
            return True
        if renpy.get_screen("choice"):
            _screenshot_save_png(_screenshot_turn_path("_menu"))
            _screenshot_click_menu()
            _screenshot_tick_tail()
            return False
        if renpy.get_screen("say") or renpy.get_screen("nvl"):
            _screenshot_save_png(_screenshot_turn_path())
        _screenshot_tick_tail()
        return False

    if _screenshot_label_callback not in renpy.config.label_callbacks:
        renpy.config.label_callbacks.append(_screenshot_label_callback)

    def _screenshot_write_run_report():
        report_path = os.path.join(renpy.config.basedir, "screenshots/review-2026-06-02/canon-turns/run-report.json")
        payload = {
            "screenshots_captured": _screenshot_turn_n,
            "menus_handled": _screenshot_menu_count,
            "canon_branch": "canon_first_choice_physical_unless",
            "output_dir": "screenshots/review-2026-06-02/canon-turns",
            "skipped": list(_screenshot_skipped),
            "reached_milestone_end": _screenshot_reached_milestone_end,
        }
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
            f.write("\n")


testsuite screenshot_all_turns:
    description "Canon-path dialogue screenshots for every turn"

    setup:
        $ _test.screenshot_directory = ""
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 3600.0
        $ preferences.text_cps = 0
        $ preferences.afm_enable = True
        $ preferences.afm_time = 0
        $ _screenshot_reset_run_state()

    testcase canon_all_dialogue:
        run Jump("start")
        advance repeat 3
        advance until eval _screenshot_drive_ready()
        python:
            _screenshot_write_run_report()
        exit
