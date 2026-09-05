#!/usr/bin/env bash
# Install native Copilot, Codex, or OpenCode customizations; see --help.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/scripts/install.py" "$@"
