#!/bin/bash
set -euo pipefail

proj="/Users/mr.adams/excel agent"
cd "$proj"

# Ensure scripts are executable
chmod +x scripts/*.sh || true

echo "==> Setting OpenAI key (you may be prompted)..."
./scripts/setup-openai-key.sh || true

echo "==> Checking OpenAI connectivity..."
./scripts/check-openai-connectivity.sh || true

echo "==> Creating virtualenv and installing if needed, then running a smoke test..."
./scripts/run-openai-agent.sh || true

echo "Setup complete. You can now proceed to step 2."
echo "Opening Data and Knowledge Base folders for convenience..."
open "/Users/mr.adams/excel agent/data" || true
open "/Users/mr.adams/excel agent/knowledge-base" || true
read -n 1 -s -r -p "Press any key to close"
