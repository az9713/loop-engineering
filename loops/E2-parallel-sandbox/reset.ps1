# Restore the E2 sandbox to its broken (RED) state so you can re-run the loop.
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Get-ChildItem (Join-Path $here ".broken") -Filter *.py | ForEach-Object {
    Copy-Item -Force $_.FullName (Join-Path (Join-Path $here "sandbox") $_.Name)
}
Write-Host "E2 sandbox reset to broken state. Confirm RED:" -ForegroundColor Yellow
Write-Host "  cd `"$here\sandbox`"; python -m unittest discover -p test_*.py"
