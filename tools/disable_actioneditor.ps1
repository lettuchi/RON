# Remove dev ActionEditor from game/. See docs/actioneditor-dev.md.
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$dst = Join-Path $root "game\dev_actioneditor"
if (Test-Path $dst) {
    Remove-Item $dst -Recurse -Force
    Write-Host "Removed game/dev_actioneditor."
} else {
    Write-Host "game/dev_actioneditor not present."
}
