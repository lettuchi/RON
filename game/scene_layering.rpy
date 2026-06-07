# Scene layering: bg / CG / sprite conventions (see docs/scene-layering.md).
#
# CG scenes: small full-body sprites (cg_left / cg_right) flank the illustration.
# Bust portraits (side toa / side kaoru) still appear in the say screen.

default cg_active = False
default toa_outfit = "work"

init python:
    STAGE_CHAR_TAGS = ("toa", "kaoru")
    STAGE_LAYERS = ("master",)
    _SHOW_KEYWORDS = frozenset(("at", "with", "as"))
    _DEFAULT_EXPRESSION = {"kaoru": "smirk", "toa": "neutral"}
    _TOA_OUTFIT_ATTRS = frozenset(("work", "date", "outfit_work", "outfit_date"))
    _TOA_EXPRESSION_ATTRS = frozenset((
        "neutral", "happy", "sad", "angry", "surprised", "flustered",
        "worried", "thinking", "determined", "soft",
        "bashful", "embarrassed", "twitterpated",
    ))
    _entering_cg_scene = False

    def _master_is_cg():
        if renpy.store.cg_active:
            return True
        try:
            return "cg" in renpy.get_showing_tags("master")
        except Exception:
            return False

    def hide_stage_sprites():
        """Hide full-body character sprites on all stage layers; busts in textbox are unaffected."""
        for layer in STAGE_LAYERS:
            for tag in STAGE_CHAR_TAGS:
                renpy.hide(tag, layer=layer)

    def _normalize_toa_outfit_name(outfit):
        if outfit in ("outfit_work", "work"):
            return "work"
        if outfit in ("outfit_date", "date"):
            return "date"
        return outfit

    def _outfit_from_attrs(attrs):
        if not attrs:
            return renpy.store.toa_outfit
        for a in attrs:
            if a in _TOA_OUTFIT_ATTRS:
                return _normalize_toa_outfit_name(a)
        return renpy.store.toa_outfit

    def _expression_from_attrs(char_tag, attrs, explicit=None):
        if explicit and explicit not in _SHOW_KEYWORDS:
            return explicit
        if char_tag == "toa" and attrs:
            for a in attrs:
                if a in _TOA_EXPRESSION_ATTRS:
                    return a
        elif attrs:
            return attrs[0]
        return _DEFAULT_EXPRESSION.get(char_tag, "neutral")

    def _format_toa_show(expression, outfit=None):
        if outfit is None:
            outfit = renpy.store.toa_outfit
        outfit = _normalize_toa_outfit_name(outfit)
        renpy.store.toa_outfit = outfit
        if outfit == "date":
            return "toa date {}".format(expression)
        if outfit == "work":
            return "toa work {}".format(expression)
        return "toa {}".format(expression)

    def set_toa_outfit(outfit="work"):
        """Remember Toa outfit for CG busts and implicit show lines (work | date)."""
        renpy.store.toa_outfit = _normalize_toa_outfit_name(outfit)

    def _resolve_expression(char_tag, expression):
        attrs = renpy.get_attributes(char_tag, layer="master")
        return _expression_from_attrs(char_tag, attrs, expression)

    def set_expression(char_tag, expression=None):
        """Update bust expression with sprite offstage (bust-only during CG)."""
        expr = _resolve_expression(char_tag, expression)
        if char_tag == "toa":
            name = _format_toa_show(expr)
        else:
            name = "{} {}".format(char_tag, expr)
        _original_renpy_show(
            name,
            at_list=[renpy.store.offstage],
            layer="master",
        )

    def _cg_stage_transform(char_tag):
        if char_tag == "kaoru":
            return renpy.store.cg_left
        if char_tag == "toa":
            return renpy.store.cg_right
        return None

    def _map_at_list_for_cg(char_tag, at_list):
        if _at_list_is_offstage(at_list):
            return at_list
        left = renpy.store.left
        right = renpy.store.right
        cg_left = renpy.store.cg_left
        cg_right = renpy.store.cg_right
        mapped = []
        for item in at_list or ():
            if item is left:
                mapped.append(cg_left)
            elif item is right:
                mapped.append(cg_right)
            else:
                mapped.append(item)
        if not mapped:
            default = _cg_stage_transform(char_tag)
            if default is not None:
                mapped = [default]
        return mapped

    def show_cg_sprite(char_tag, expression=None, at_list=()):
        """Show a character on a CG scene with cg_left / cg_right sizing."""
        expr = _resolve_expression(char_tag, expression)
        if char_tag == "toa":
            name = _format_toa_show(expr)
        else:
            name = "{} {}".format(char_tag, expr)
        mapped_at = _map_at_list_for_cg(char_tag, at_list)
        return _original_renpy_show(name, at_list=mapped_at, layer="master")

    def _parse_character_show(name):
        """Extract (char_tag, expression, outfit) from show names for toa/kaoru."""
        outfit = None
        if isinstance(name, tuple):
            if len(name) >= 1 and name[0] in STAGE_CHAR_TAGS:
                char_tag = name[0]
                expression = None
                for part in name[1:]:
                    if part in _SHOW_KEYWORDS:
                        break
                    if char_tag == "toa" and part in _TOA_OUTFIT_ATTRS:
                        outfit = _normalize_toa_outfit_name(part)
                    elif expression is None and part not in _TOA_OUTFIT_ATTRS:
                        expression = part
                return char_tag, expression, outfit
            return None, None, None
        if isinstance(name, str):
            parts = name.split()
            if not parts or parts[0] not in STAGE_CHAR_TAGS:
                return None, None, None
            char_tag = parts[0]
            expression = None
            for part in parts[1:]:
                if part in _SHOW_KEYWORDS:
                    break
                if char_tag == "toa" and part in _TOA_OUTFIT_ATTRS:
                    outfit = _normalize_toa_outfit_name(part)
                elif expression is None and part not in _TOA_OUTFIT_ATTRS:
                    expression = part
            return char_tag, expression, outfit
        return None, None, None

    def _at_list_is_offstage(at_list):
        if not at_list:
            return False
        offstage = renpy.store.offstage
        for item in at_list:
            if item is offstage:
                return True
        return False

    def show_cg_scene(cg_tag, transition=None):
        """Show a full-screen CG; stage sprites reappear on next show/dialogue at CG size."""
        global _entering_cg_scene
        if transition is None:
            transition = renpy.store.dissolve
        hide_stage_sprites()
        _entering_cg_scene = True
        renpy.scene()
        _entering_cg_scene = False
        _original_renpy_show("_cg_letterbox", layer="master", tag="_cg_letterbox")
        _original_renpy_show("cg " + cg_tag, layer="master")
        renpy.store.cg_active = True
        renpy.with_statement(transition)

    def restore_location_sprites(bg_tag, kaoru_expression="smirk", toa_expression="neutral", transition=None, toa_outfit=None):
        """Return from a CG beat to a location background with both stage sprites."""
        if transition is None:
            transition = renpy.store.dissolve
        hide_stage_sprites()
        renpy.scene()
        _original_renpy_show("bg " + bg_tag, layer="master")
        renpy.with_statement(transition)
        renpy.store.cg_active = False
        _original_renpy_show("kaoru {} at left".format(kaoru_expression), layer="master")
        if toa_outfit is None:
            toa_outfit = renpy.store.toa_outfit
        _original_renpy_show(
            "{} at right".format(_format_toa_show(toa_expression, toa_outfit)),
            layer="master",
        )

    def _cg_scene_callback(layer):
        if layer != "master":
            return
        if _entering_cg_scene:
            return
        # Leaving a CG beat (scene bg/black/etc.), only clear when CG tag is gone.
        try:
            if "cg" not in renpy.get_showing_tags("master"):
                renpy.store.cg_active = False
        except Exception:
            renpy.store.cg_active = False

    _original_renpy_show = renpy.show

    def cg_safe_show(name, at_list=(), layer="master", what=None, zorder=0, tag=None, behind=None, atl=None, **kwargs):
        if layer == "master" and _master_is_cg():
            char_tag, expression, outfit = _parse_character_show(name)
            if char_tag is not None:
                if char_tag == "toa" and outfit is not None:
                    renpy.store.toa_outfit = outfit
                if _at_list_is_offstage(at_list):
                    show_kwargs = dict(
                        layer=layer,
                        what=what,
                        zorder=zorder,
                        tag=tag,
                        behind=behind,
                        atl=atl,
                        **kwargs,
                    )
                    if at_list:
                        show_kwargs["at_list"] = at_list
                    if char_tag == "toa":
                        expr = _resolve_expression(char_tag, expression)
                        name = _format_toa_show(expr, outfit or renpy.store.toa_outfit)
                    return _original_renpy_show(name, **show_kwargs)
                return show_cg_sprite(char_tag, expression, at_list)
        show_kwargs = dict(
            layer=layer,
            what=what,
            zorder=zorder,
            tag=tag,
            behind=behind,
            atl=atl,
            **kwargs,
        )
        if at_list:
            show_kwargs["at_list"] = at_list
        char_tag, expression, outfit = _parse_character_show(name)
        if char_tag == "toa":
            if outfit is not None:
                renpy.store.toa_outfit = outfit
            elif expression is not None:
                name = _format_toa_show(expression, renpy.store.toa_outfit)
        return _original_renpy_show(name, **show_kwargs)

    renpy.show = cg_safe_show

    def _install_cg_character_callbacks():
        for char_name in STAGE_CHAR_TAGS:
            char = getattr(renpy.store, char_name, None)
            if char is None:
                continue
            old_cb = getattr(char, "callback", None)

            def make_wrapped(old_callback, tag=char_name):
                def wrapped(event, interact=True, **kwargs):
                    if _master_is_cg() and event == "show":
                        show_cg_sprite(tag, None)
                    if old_callback is not None:
                        old_callback(event, interact=interact, **kwargs)
                return wrapped

            char.callback = make_wrapped(old_cb)

    config.scene_callbacks.append(_cg_scene_callback)

init 999 python:
    # Ren'Py `show` statements call config.show, not only renpy.show.
    config.show = cg_safe_show
    _install_cg_character_callbacks()
