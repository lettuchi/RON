## GUI support, scale helper only.
##
## The original Ren'Py GUI generator block (gui7) only exists inside the
## Ren'Py SDK launcher and must NOT run when launching the game normally.
## It caused: ModuleNotFoundError: No module named 'gui7'
##
## Regenerate GUI assets from the Ren'Py Launcher if needed, not at game start.

init -100 python in gui:

    def scale(n):
        return int(n)
