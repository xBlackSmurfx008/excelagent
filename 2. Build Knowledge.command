#!/bin/bash
set -euo pipefail

proj="/Users/mr.adams/excel agent"
cd "$proj"
chmod +x scripts/*.sh || true

echo "==> Building knowledge indexes (Markdown + Excel)..."
./scripts/agent.sh index || true

echo "Indexes built. Proceed to step 3 to reconcile."
read -n 1 -s -r -p "Press any key to close"

