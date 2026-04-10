#!/usr/bin/env bash
# Install llm-config agents and skills into VS Code user-level directories.
#
# Agents  → ~/.config/Code/User/prompts/  (roam across all workspaces)
# Skills  → ~/.copilot/skills/            (available in all workspaces)
#
# Usage:
#   ./setup.sh              # symlink (default, tracks repo changes)
#   ./setup.sh --copy       # copy instead of symlink

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MODE="symlink"
if [[ "${1:-}" == "--copy" ]]; then
    MODE="copy"
fi

AGENT_SRC="$SCRIPT_DIR/agents"
SKILL_SRC="$SCRIPT_DIR/skills"

AGENT_DST="${HOME}/.config/Code/User/prompts"
SKILL_DST="${HOME}/.copilot/skills"

install_file() {
    local src="$1" dst="$2"
    mkdir -p "$(dirname "$dst")"
    if [[ "$MODE" == "copy" ]]; then
        cp "$src" "$dst"
    else
        ln -sf "$src" "$dst"
    fi
}

install_dir() {
    local src="$1" dst="$2"
    mkdir -p "$(dirname "$dst")"
    if [[ "$MODE" == "copy" ]]; then
        cp -r "$src" "$dst"
    else
        ln -sfn "$src" "$dst"
    fi
}

echo "Installing agents to $AGENT_DST ..."
mkdir -p "$AGENT_DST"
for f in "$AGENT_SRC"/*.agent.md; do
    [ -f "$f" ] || continue
    name="$(basename "$f")"
    install_file "$f" "$AGENT_DST/$name"
    echo "  $name"
done

echo "Installing skills to $SKILL_DST ..."
mkdir -p "$SKILL_DST"
for d in "$SKILL_SRC"/*/; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"
    install_dir "$d" "$SKILL_DST/$name"
    echo "  $name/"
done

echo ""
echo "Done ($MODE mode)."
echo "Agents are in: $AGENT_DST"
echo "Skills are in: $SKILL_DST"
echo ""
echo "Restart VS Code or reload the window for changes to take effect."
