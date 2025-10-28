#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

chmod +x scripts/*.sh || true

echo "==> Verifying SSH access to GitHub (ssh -T git@github.com) ..."
ssh -T git@github.com || true

echo
echo "==> Pushing to git@github.com:xBlackSmurfx008/excelagent.git ..."
./scripts/publish-github-ssh.sh xBlackSmurfx008/excelagent main || true

echo
echo "If push failed:"
echo "  1) Ensure your SSH key is added to GitHub (https://github.com/settings/keys)"
echo "  2) Test: ssh -T git@github.com (should show a success greeting)"
echo "  3) Retry this button"

read -n 1 -s -r -p "Press any key to close"

