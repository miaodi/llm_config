#!/usr/bin/env bash
# Install llm-config agents and skills into either VS Code user-level directories
# or a project's .github directory.
#
# User install:
#   Agents  → ~/.config/Code/User/prompts/
#   Skills  → ~/.copilot/skills/
#
# Project install:
#   Agents  → <project>/.github/agents/
#   Skills  → <project>/.github/skills/
#   Instructions → <project>/.github/copilot-instructions.md
#
# Usage:
#   ./setup.sh                          # symlink user-level install
#   ./setup.sh --copy                   # copy user-level install
#   ./setup.sh --project /path/to/repo  # symlink project install
#   ./setup.sh --project /path/to/repo --copy

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MODE="symlink"
PROJECT_ROOT=""

usage() {
    cat <<EOF
Usage:
  ./setup.sh [--copy] [--project PATH]

Options:
  --copy           Copy files instead of symlinking them.
  --project PATH   Install into PATH/.github instead of user-level directories.
  --help           Show this help text.
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --copy)
            MODE="copy"
            shift
            ;;
        --project)
            if [[ $# -lt 2 ]]; then
                echo "error: --project requires a path" >&2
                usage >&2
                exit 1
            fi
            PROJECT_ROOT="$2"
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            echo "error: unknown option: $1" >&2
            usage >&2
            exit 1
            ;;
    esac
done

AGENT_SRC="$SCRIPT_DIR/agents"
SKILL_SRC="$SCRIPT_DIR/skills"

if [[ -n "$PROJECT_ROOT" ]]; then
    PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"
    GITHUB_DIR="$PROJECT_ROOT/.github"
    AGENT_DST="$GITHUB_DIR/agents"
    SKILL_DST="$GITHUB_DIR/skills"
    INSTRUCTIONS_DST="$GITHUB_DIR/copilot-instructions.md"
else
    AGENT_DST="${HOME}/.config/Code/User/prompts"
    SKILL_DST="${HOME}/.copilot/skills"
    INSTRUCTIONS_DST=""
fi

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

create_project_instructions() {
    local dst="$1"
    local project_name="$2"

    mkdir -p "$(dirname "$dst")"
    if [[ -e "$dst" ]]; then
        echo "  copilot-instructions.md (kept existing file)"
        return
    fi

    cat > "$dst" <<EOF
# Copilot Instructions

This project uses repo-local Copilot customizations installed from llm-config.

## Project Customizations
- Custom agents are stored in .github/agents/.
- Custom skills are stored in .github/skills/.

## Usage Guidance
- Prefer project-local agents and skills before falling back to user-level customizations.
- Keep project-specific conventions, workflows, and terminology in this file.
- Update this file directly for ${project_name}-specific guidance. It is intentionally a normal file, not a symlink.
EOF

    echo "  copilot-instructions.md"
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

if [[ -n "$INSTRUCTIONS_DST" ]]; then
    echo "Installing project instructions to $INSTRUCTIONS_DST ..."
    create_project_instructions "$INSTRUCTIONS_DST" "$(basename "$PROJECT_ROOT")"
fi

echo ""
echo "Done ($MODE mode)."
echo "Agents are in: $AGENT_DST"
echo "Skills are in: $SKILL_DST"
if [[ -n "$INSTRUCTIONS_DST" ]]; then
    echo "Instructions are in: $INSTRUCTIONS_DST"
fi
echo ""
echo "Restart VS Code or reload the window for changes to take effect."
