# ActionEditor 3 (dev-only)

**Upstream:** [renpy-ActionEditor3](https://github.com/kyouryuukunn/renpy-ActionEditor3)  
**Installed copy:** `tools/ActionEditor3/` (not loaded during normal play — files are **outside** `game/`).

Use this to tune camera/transform timing for OP/ED montages (`game/transforms_op_ed.rpy`, `game/opening.rpy`, image-song scripts), then paste generated ATL from the clipboard.

## Enable for a dev session

Copy editor scripts into the game tree (Ren'Py only loads `.rpy` under `game/`):

```powershell
# From repo root
$src = "tools\ActionEditor3"
$dst = "game\dev_actioneditor"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item "$src\*.rpy" $dst -Force
Copy-Item "$src\tl" $dst -Recurse -Force
```

Ensure **developer mode** is on (Ren'Py launcher: preferences, or `define config.developer = True` in a local-only overlay).

Launch the project, open a label with the visuals you want to edit (e.g. `opening` / OP test), then:

| Shortcut | Action |
|----------|--------|
| **Shift+P** | Open Action Editor |
| **Shift+U** | Image Viewer |
| **Shift+S** | Sound Viewer |

Adjust transforms on the timeline → copy generated script from the editor → paste into `transforms_op_ed.rpy` or the relevant cinematic `.rpy`.

## Disable before release

```powershell
Remove-Item -Recurse -Force "game\dev_actioneditor"
```

Release builds should not ship ActionEditor. If you used camera blur or generated warpers in shipped ATL, upstream notes you may need to keep `ActionEditor.rpy` / `00warper.rpy` / `ATL_functions.rpy` — this project’s OP/ED code is hand-written today, so removal is usually safe.

## Target files

- `game/transforms_op_ed.rpy` — Ken Burns, vignette, color grade transforms  
- `game/opening.rpy` — OP sequence  
- `game/ed_sequence.rpy`, `game/*_image_song.rpy` — ED / image songs  
