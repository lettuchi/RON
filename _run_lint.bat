@echo off
del "C:\Users\Amanda\Developer\ryoko-owari\_lint_report.txt" 2>nul
del "C:\Users\Amanda\Developer\ryoko-owari\_lint_done.txt" 2>nul
"C:\Users\Amanda\Developer\renpy-sdk\renpy-8.5.3-sdk\renpy.exe" "C:\Users\Amanda\Developer\ryoko-owari" lint "C:\Users\Amanda\Developer\ryoko-owari\_lint_report.txt" --error-code < NUL
echo LINT_DONE_EXIT=%ERRORLEVEL%> "C:\Users\Amanda\Developer\ryoko-owari\_lint_done.txt"
