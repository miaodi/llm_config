#!/usr/bin/env bash
# Install llm-config agents and skills into VS Code user-level directories,
# a project's .github directory, or Codex user-level directories.
#
# User install:
#   Agents  → ~/.config/Code/User/agents/
#   Skills  → ~/.copilot/skills/
#
# Project install:
#   Agents  → <project>/.github/agents/
#   Skills  → <project>/.github/skills/
#   Instructions → <project>/.github/copilot-instructions.md
#
# Codex install:
#   Agent specs → ~/.codex/agents/  (reference files; not spawn_agent registrations)
#   Skills      → ~/.codex/skills/
#
# Usage:
#   ./setup.sh                          # symlink user-level install
#   ./setup.sh --copy                   # copy user-level install
#   ./setup.sh --project /path/to/repo  # symlink project install
#   ./setup.sh --project /path/to/repo --copy
#   ./setup.sh --codex                  # symlink Codex skills and reference agent specs

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MODE="symlink"
PROJECT_ROOT=""
TARGET="vscode"

usage() {
    cat <<EOF
Usage:
  ./setup.sh [--copy] [--project PATH|--codex]

Options:
  --copy           Copy files instead of symlinking them.
  --project PATH   Install into PATH/.github instead of user-level directories.
  --codex          Install Codex skills and reference agent specs into ~/.codex.
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
            if [[ "$TARGET" == "codex" ]]; then
                echo "error: --project and --codex cannot be used together" >&2
                usage >&2
                exit 1
            fi
            PROJECT_ROOT="$2"
            TARGET="project"
            shift 2
            ;;
        --codex)
            if [[ -n "$PROJECT_ROOT" ]]; then
                echo "error: --project and --codex cannot be used together" >&2
                usage >&2
                exit 1
            fi
            TARGET="codex"
            shift
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
COMMIT_MESSAGE_TEMPLATE_SRC="$SCRIPT_DIR/templates/commit-message/git-p4-commit-message-template.txt"
INSTALL_SKILLS=1

if [[ "$TARGET" == "project" ]]; then
    PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"
    GITHUB_DIR="$PROJECT_ROOT/.github"
    AGENT_DST="$GITHUB_DIR/agents"
    SKILL_DST="$GITHUB_DIR/skills"
    COMMIT_MESSAGE_TEMPLATE_DST="$GITHUB_DIR/templates/commit-message/git-p4-commit-message-template.txt"
    INSTRUCTIONS_DST="$GITHUB_DIR/copilot-instructions.md"
elif [[ "$TARGET" == "codex" ]]; then
    AGENT_DST="${HOME}/.codex/agents"
    SKILL_DST="${HOME}/.codex/skills"
    COMMIT_MESSAGE_TEMPLATE_DST="${HOME}/.codex/templates/commit-message/git-p4-commit-message-template.txt"
    INSTRUCTIONS_DST=""
else
    AGENT_DST="${HOME}/.config/Code/User/agents"
    SKILL_DST="${HOME}/.copilot/skills"
    COMMIT_MESSAGE_TEMPLATE_DST="${HOME}/.config/Code/User/templates/commit-message/git-p4-commit-message-template.txt"
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

if [[ "$INSTALL_SKILLS" -eq 1 ]]; then
    echo "Installing skills to $SKILL_DST ..."
    mkdir -p "$SKILL_DST"
    for d in "$SKILL_SRC"/*/; do
        [ -d "$d" ] || continue
        name="$(basename "$d")"
        install_dir "$d" "$SKILL_DST/$name"
        echo "  $name/"
    done
fi

if [[ -f "$COMMIT_MESSAGE_TEMPLATE_SRC" ]]; then
    echo "Installing commit message template to $COMMIT_MESSAGE_TEMPLATE_DST ..."
    install_file "$COMMIT_MESSAGE_TEMPLATE_SRC" "$COMMIT_MESSAGE_TEMPLATE_DST"
fi

if [[ -n "$INSTRUCTIONS_DST" ]]; then
    echo "Installing project instructions to $INSTRUCTIONS_DST ..."
    create_project_instructions "$INSTRUCTIONS_DST" "$(basename "$PROJECT_ROOT")"
fi

echo ""
echo "Done ($MODE mode)."
echo "Agents are in: $AGENT_DST"
if [[ "$INSTALL_SKILLS" -eq 1 ]]; then
    echo "Skills are in: $SKILL_DST"
fi
if [[ -f "$COMMIT_MESSAGE_TEMPLATE_SRC" ]]; then
    echo "Commit template is in: $COMMIT_MESSAGE_TEMPLATE_DST"
fi
if [[ -n "$INSTRUCTIONS_DST" ]]; then
    echo "Instructions are in: $INSTRUCTIONS_DST"
fi
echo ""
if [[ "$TARGET" == "codex" ]]; then
    echo "Restart Codex for skill changes to take effect."
    echo "Note: ~/.codex/agents/*.agent.md files are reference specs in this CLI; they do not register new spawn_agent types."
else
    echo "Restart VS Code or reload the window for changes to take effect."
fi
