#!/usr/bin/env bash
# Restore the E2 sandbox to its broken (RED) state so you can re-run the loop.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -f "$here/.broken/"*.py "$here/sandbox/"
echo "E2 sandbox reset to broken state. Confirm RED:"
echo "  cd \"$here/sandbox\" && python -m unittest discover -p test_*.py"
