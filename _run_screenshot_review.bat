@echo off
setlocal
set RENPY=C:\Users\Amanda\Developer\renpy-sdk\renpy-8.5.3-sdk\renpy.exe
set PROJ=C:\Users\Amanda\Developer\ryoko-owari
cd /d "%PROJ%"

if not exist "%RENPY%" (
    echo ERROR: Ren'Py SDK not found at %RENPY%
    exit /b 1
)

echo [review] Generating CG testcase...
python "%PROJ%\scripts\gen_review_cg_testcase.py"
if errorlevel 1 goto failed

echo [review] CG catalog...
"%RENPY%" "%PROJ%" test screenshot_review_cg::review_cg_catalog_generated --overwrite-screenshots
if errorlevel 1 goto failed

echo [review] Story beats...
"%RENPY%" "%PROJ%" test screenshot_review::review_story_beats --overwrite-screenshots
if errorlevel 1 goto failed

echo [review] Bad endings...
"%RENPY%" "%PROJ%" test screenshot_review::review_bad_endings --overwrite-screenshots
if errorlevel 1 goto failed

echo [review] Cinematics first frame...
"%RENPY%" "%PROJ%" test screenshot_review::review_cinematics_first_frame --overwrite-screenshots
if errorlevel 1 goto failed

echo [review] Canon playthrough all dialogue turns (may take several minutes)...
"%RENPY%" "%PROJ%" test screenshot_all_turns::canon_all_dialogue --overwrite-screenshots
if errorlevel 1 goto failed

echo [review] Writing manifest...
python "%PROJ%\scripts\write_screenshot_manifest.py"
if errorlevel 1 goto failed

echo [review] Done. See screenshots\review-2026-06-02\manifest.md
exit /b 0

:failed
echo [review] FAILED — see log.txt / traceback.txt in project root
exit /b 1
