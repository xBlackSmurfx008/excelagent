#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

chmod +x scripts/*.sh || true

echo "==> Launching Monitor Window..."
./scripts/monitor.sh

