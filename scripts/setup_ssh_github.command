#!/bin/bash
set -euo pipefail

proj="/Users/mr.adams/excel agent"
cd "$proj"
chmod +x scripts/*.sh || true

./scripts/setup-ssh-github.sh

read -n 1 -s -r -p "Press any key to close"

