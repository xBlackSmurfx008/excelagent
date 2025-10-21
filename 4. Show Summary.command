#!/bin/bash
set -euo pipefail

proj="/Users/mr.adams/excel agent"
cd "$proj"
chmod +x scripts/*.sh || true

echo "==> Last run summary"
./scripts/show-last-run.sh || true

echo
echo "You can re-run step 3 to refresh the summary."
read -n 1 -s -r -p "Press any key to close"

