#!/bin/bash
# Legacy launcher wrapper - forwards to unified launcher

echo "🔁 Forwarding to Unified Dashboard Launcher..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

chmod +x Launch_Unified_Dashboard.command || true
"$SCRIPT_DIR/Launch_Unified_Dashboard.command"
