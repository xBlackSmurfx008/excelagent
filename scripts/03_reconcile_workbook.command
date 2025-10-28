#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
chmod +x scripts/*.sh || true

echo "==> Reconciliation (end-to-end)"
read -rp "Workbook file under data/ (e.g., reconciliation.xlsx): " FILE
read -rp "Month (e.g., August): " MONTH
read -rp "Year (e.g., 2025): " YEAR

if [[ -z "$FILE" ]]; then
  echo "No file provided. Aborting."; read -n 1 -s -r -p "Press any key to close"; exit 1
fi

echo "Running reconcile_all..."
./scripts/agent.sh reconcile all --file "$FILE" --month "$MONTH" --year "$YEAR" || true

echo
echo "Opening workbook..."
open "data/$FILE" || true
echo "Done. Review the AutoSummary sheet."
read -n 1 -s -r -p "Press any key to close"

