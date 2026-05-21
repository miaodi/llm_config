#!/usr/bin/env bash
# Install llm-config agents and skills into Copilot, Codex, or OpenCode
# user-level directories, or into a project-local configuration directory.
#
# Copilot install:
#   Agents  → ~/.copilot/agents/
#   Skills  → ~/.copilot/skills/
#
# Copilot project install:
#   Agents  → <project>/.github/agents/
#   Skills  → <project>/.github/skills/
#   Instructions → <project>/.github/copilot-instructions.md
#
# Codex install:
#   Agents  → ~/.codex/agents/  (.agent.md files)
#   Skills  → ~/.codex/skills/
#
# Codex project install:
#   Agents  → <project>/.codex/agents/  (.agent.md files)
#   Skills  → <project>/.codex/skills/
#
# OpenCode install:
#   Agents  → ~/.config/opencode/agents/  (.md files)
#   Skills  → ~/.config/opencode/skills/
#
# OpenCode project install:
#   Agents  → <project>/.opencode/agents/  (.md files)
#   Skills  → <project>/.opencode/skills/
#
# Usage:
#   ./setup.sh --copilot                # symlink Copilot user-level install
#   ./setup.sh --copilot --copy         # copy Copilot user-level install
#   ./setup.sh --copilot-project /path/to/repo
#   ./setup.sh --copilot-project /path/to/repo --copy
#   ./setup.sh --codex                  # install Codex user-level agents and skills
#   ./setup.sh --codex-project /path/to/repo
#   ./setup.sh --opencode               # install OpenCode user-level agents and skills
#   ./setup.sh --opencode-project /path/to/repo

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MODE="symlink"
PROJECT_ROOT=""
TARGET=""

usage() {
    cat <<EOF
Usage:
./setup.sh --copilot [--copy]
./setup.sh --copilot-project PATH [--copy]
./setup.sh --codex [--copy]
./setup.sh --codex-project PATH [--copy]
./setup.sh --opencode [--copy]
./setup.sh --opencode-project PATH [--copy]

Options:
--copilot        Install Copilot agents and skills into user-level directories.
--copy           Copy files instead of symlinking them.
--copilot-project PATH
                 Install Copilot agents and skills into PATH/.github.
--project PATH   Alias for --copilot-project PATH.
--codex          Install Codex agents and skills into user-level directories.
--codex-project PATH
                 Install Codex agents and skills into PATH/.codex.
--opencode       Install OpenCode agents and skills into user-level directories.
--opencode-project PATH
                 Install OpenCode agents and skills into PATH/.opencode.
--help           Show this help text.
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --copy)
            MODE="copy"
            shift
            ;;
        --copilot)
            if [[ -n "$TARGET" ]]; then
                echo "error: choose only one install target" >&2
                usage >&2
                exit 1
            fi
            TARGET="copilot"
            shift
            ;;
        --copilot-project|--project)
            if [[ $# -lt 2 ]]; then
                echo "error: $1 requires a path" >&2
                usage >&2
                exit 1
            fi
            if [[ -n "$TARGET" ]]; then
                echo "error: choose only one install target" >&2
                usage >&2
                exit 1
            fi
            PROJECT_ROOT="$2"
            TARGET="copilot-project"
            shift 2
            ;;
        --codex-project)
            if [[ $# -lt 2 ]]; then
                echo "error: --codex-project requires a path" >&2
                usage >&2
                exit 1
            fi
            if [[ -n "$TARGET" ]]; then
                echo "error: choose only one install target" >&2
                usage >&2
                exit 1
            fi
            PROJECT_ROOT="$2"
            TARGET="codex-project"
            shift 2
            ;;
        --opencode-project)
            if [[ $# -lt 2 ]]; then
                echo "error: --opencode-project requires a path" >&2
                usage >&2
                exit 1
            fi
            if [[ -n "$TARGET" ]]; then
                echo "error: choose only one install target" >&2
                usage >&2
                exit 1
            fi
            PROJECT_ROOT="$2"
            TARGET="opencode-project"
            shift 2
            ;;
        --codex)
            if [[ -n "$TARGET" ]]; then
                echo "error: choose only one install target" >&2
                usage >&2
                exit 1
            fi
            TARGET="codex"
            shift
            ;;
        --opencode)
            if [[ -n "$TARGET" ]]; then
                echo "error: choose only one install target" >&2
                usage >&2
                exit 1
            fi
            TARGET="opencode"
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

if [[ -z "$TARGET" ]]; then
    echo "error: choose an install target: --copilot, --copilot-project PATH, --codex, --codex-project PATH, --opencode, or --opencode-project PATH" >&2
    usage >&2
    exit 1
fi

AGENT_SRC="$SCRIPT_DIR/agents"
SKILL_SRC="$SCRIPT_DIR/skills"
COMMIT_MESSAGE_TEMPLATE_SRC="$SCRIPT_DIR/templates/commit-message/git-p4-commit-message-template.txt"
INSTALL_SKILLS=1
AGENT_INSTALL_FORMAT="source"

resolve_vscode_user_dir() {
    if [[ -d "${HOME}/.vscode-server/data/User" ]]; then
        printf '%s\n' "${HOME}/.vscode-server/data/User"
    else
        printf '%s\n' "${HOME}/.config/Code/User"
    fi
}

if [[ "$TARGET" == "copilot-project" ]]; then
    PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"
    GITHUB_DIR="$PROJECT_ROOT/.github"
    AGENT_DST="$GITHUB_DIR/agents"
    SKILL_DST="$GITHUB_DIR/skills"
    COMMIT_MESSAGE_TEMPLATE_DST="$GITHUB_DIR/templates/commit-message/git-p4-commit-message-template.txt"
    INSTRUCTIONS_DST="$GITHUB_DIR/copilot-instructions.md"
elif [[ "$TARGET" == "codex" ]]; then
    CODEX_HOME="${CODEX_HOME:-${HOME}/.codex}"
    AGENT_DST="$CODEX_HOME/agents"
    SKILL_DST="$CODEX_HOME/skills"
    COMMIT_MESSAGE_TEMPLATE_DST="$CODEX_HOME/templates/commit-message/git-p4-commit-message-template.txt"
    INSTRUCTIONS_DST=""
elif [[ "$TARGET" == "codex-project" ]]; then
    PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"
    CODEX_DIR="$PROJECT_ROOT/.codex"
    AGENT_DST="$CODEX_DIR/agents"
    SKILL_DST="$CODEX_DIR/skills"
    COMMIT_MESSAGE_TEMPLATE_DST="$CODEX_DIR/templates/commit-message/git-p4-commit-message-template.txt"
    INSTRUCTIONS_DST=""
elif [[ "$TARGET" == "opencode" ]]; then
    OPENCODE_HOME="${OPENCODE_HOME:-${HOME}/.config/opencode}"
    AGENT_DST="$OPENCODE_HOME/agents"
    SKILL_DST="$OPENCODE_HOME/skills"
    COMMIT_MESSAGE_TEMPLATE_DST="$OPENCODE_HOME/templates/commit-message/git-p4-commit-message-template.txt"
    INSTRUCTIONS_DST=""
    AGENT_INSTALL_FORMAT="opencode"
elif [[ "$TARGET" == "opencode-project" ]]; then
    PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"
    OPENCODE_DIR="$PROJECT_ROOT/.opencode"
    AGENT_DST="$OPENCODE_DIR/agents"
    SKILL_DST="$OPENCODE_DIR/skills"
    COMMIT_MESSAGE_TEMPLATE_DST="$OPENCODE_DIR/templates/commit-message/git-p4-commit-message-template.txt"
    INSTRUCTIONS_DST=""
    AGENT_INSTALL_FORMAT="opencode"
elif [[ "$TARGET" == "copilot" ]]; then
    VSCODE_USER_DIR="$(resolve_vscode_user_dir)"
    AGENT_DST="${HOME}/.copilot/agents"
    SKILL_DST="${HOME}/.copilot/skills"
    COMMIT_MESSAGE_TEMPLATE_DST="$VSCODE_USER_DIR/templates/commit-message/git-p4-commit-message-template.txt"
    INSTRUCTIONS_DST=""
else
    echo "error: unsupported install target: $TARGET" >&2
    exit 1
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

install_opencode_agent_file() {
    local src="$1" dst="$2"
    mkdir -p "$(dirname "$dst")"
    awk -v src="$src" '
        NR == 1 && $0 == "---" {
            in_frontmatter = 1
            next
        }
        in_frontmatter && $0 == "---" {
            if (description == "") {
                print "error: missing description in " src > "/dev/stderr"
                exit 1
            }
            print "---"
            print description
            print "mode: subagent"
            print "---"
            in_frontmatter = 0
            next
        }
        in_frontmatter {
            if ($0 ~ /^description:[[:space:]]*/) {
                description = $0
            }
            next
        }
        {
            print
        }
    ' "$src" > "$dst"
}

ensure_dir() {
    local dst="$1"
    if [[ ! -d "$dst" ]]; then
        if [[ -e "$dst" || -L "$dst" ]]; then
            echo "error: $dst exists but is not a directory; remove it first:" >&2
            echo "  rm $dst" >&2
            exit 1
        fi
        local parent
        parent="$(dirname "$dst")"
        if [[ (-e "$parent" || -L "$parent") && ! -d "$parent" ]]; then
            echo "error: $parent exists but is not a directory; remove it first:" >&2
            echo "  rm $parent" >&2
            exit 1
        fi
        mkdir -p "$dst"
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

echo "Installing agents..."
echo "  Installing to $AGENT_DST ..."
mkdir -p "$AGENT_DST"
for f in "$AGENT_SRC"/*.agent.md; do
    [ -f "$f" ] || continue
    name="$(basename "$f")"
    if [[ "$AGENT_INSTALL_FORMAT" == "opencode" ]]; then
        name="${name%.agent.md}.md"
        install_opencode_agent_file "$f" "$AGENT_DST/$name"
    else
        install_file "$f" "$AGENT_DST/$name"
    fi
    echo "  $name"
done

if [[ "$INSTALL_SKILLS" -eq 1 ]]; then
    echo "Installing skills to $SKILL_DST ..."
    ensure_dir "$SKILL_DST"
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
if [[ "$TARGET" == "codex" || "$TARGET" == "codex-project" ]]; then
    echo "Restart Codex for changes to take effect."
elif [[ "$TARGET" == "opencode" || "$TARGET" == "opencode-project" ]]; then
    echo "Restart OpenCode for changes to take effect."
else
    echo "Restart VS Code or reload the window for changes to take effect."
fi
