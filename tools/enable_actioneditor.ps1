# Copy ActionEditor 3 into game/dev_actioneditor for a dev session. See docs/actioneditor-dev.md.
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$src = Join-Path $root "tools\ActionEditor3"
$dst = Join-Path $root "game\dev_actioneditor"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item (Join-Path $src "*.rpy") $dst -Force
if (Test-Path (Join-Path $dst "tl")) { Remove-Item (Join-Path $dst "tl") -Recurse -Force }
Copy-Item (Join-Path $src "tl") $dst -Recurse -Force
Write-Host "ActionEditor enabled at game/dev_actioneditor — use Shift+P in-game (config.developer must be True)."
