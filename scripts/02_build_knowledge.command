#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
chmod +x scripts/*.sh || true

echo "==> Building knowledge indexes (Markdown + Excel)..."
./scripts/agent.sh index || true

echo "Indexes built. Proceed to step 3 to reconcile."
read -n 1 -s -r -p "Press any key to close"

