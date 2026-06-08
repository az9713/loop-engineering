#!/usr/bin/env bash
# Restore the demo sandbox to its broken (RED) state so you can re-run the loop.
# Usage:  bash loops/E-demo-sandbox/reset.sh
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -f "$here/.broken/calc.py" "$here/sandbox/calc.py"
echo "Demo sandbox reset to broken state. Run the tests to confirm RED:"
echo "  cd \"$here/sandbox\" && python -m unittest test_calc -v"
