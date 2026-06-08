# Restore the demo sandbox to its broken (RED) state so you can re-run the loop.
# Usage:  pwsh loops/E-demo-sandbox/reset.ps1   (or run from this folder)
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item -Force (Join-Path $here ".broken\calc.py") (Join-Path $here "sandbox\calc.py")
Write-Host "Demo sandbox reset to broken state. Run the tests to confirm RED:" -ForegroundColor Yellow
Write-Host "  cd `"$here\sandbox`"; python -m unittest test_calc -v"
