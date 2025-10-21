#!/bin/bash
set -euo pipefail

proj="/Users/mr.adams/excel agent"
cd "$proj"

chmod +x scripts/*.sh || true

echo "==> Launching Monitor Window..."
./scripts/monitor.sh

