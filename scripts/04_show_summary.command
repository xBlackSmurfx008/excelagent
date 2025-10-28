#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
chmod +x scripts/*.sh || true

echo "==> Last run summary"
./scripts/show-last-run.sh || true

echo
echo "You can re-run step 3 to refresh the summary."
read -n 1 -s -r -p "Press any key to close"

