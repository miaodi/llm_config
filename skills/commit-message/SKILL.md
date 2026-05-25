---
name: commit-message
description: "Use when drafting, reviewing, or normalizing Git commit messages or Perforce changelist descriptions from the shared Git/P4 commit message template."
---

# Commit Message Skill

## Purpose
Draft concise, reviewable commit messages and P4 changelist descriptions from the shared template.

## Shared Template
Before drafting a message, identify which product is running this skill:

- Codex: use the Codex paths only.
- Copilot: use the Copilot paths only.
- OpenCode: use the OpenCode paths only.

Do not search every product's install location. Product-specific lookup keeps the
template selection predictable and avoids unnecessary filesystem scans.

After identifying the product, read the first available template path for that
product:

### Codex
1. `.codex/templates/commit-message/git-p4-commit-message-template.txt` in the current repository root.
2. `${CODEX_HOME:-${HOME}/.codex}/templates/commit-message/git-p4-commit-message-template.txt`.

### Copilot
1. `.github/templates/commit-message/git-p4-commit-message-template.txt` in the current repository root.
2. `${HOME}/.vscode-server/data/User/templates/commit-message/git-p4-commit-message-template.txt` when that VS Code server user directory exists.
3. `${HOME}/.config/Code/User/templates/commit-message/git-p4-commit-message-template.txt`.

### OpenCode
1. `.opencode/templates/commit-message/git-p4-commit-message-template.txt` in the current repository root.
2. `${OPENCODE_HOME:-${HOME}/.config/opencode}/templates/commit-message/git-p4-commit-message-template.txt`.

If the product cannot be determined from the active agent environment, ask the
user which product is invoking the skill instead of searching all product paths.

When working directly from this llm-config source checkout, the source template
at `templates/commit-message/git-p4-commit-message-template.txt` may be used as
the repository-local template.

Use that file as the single source of truth for message shape and allowed sections.

## Rules
- For Git, produce the final message without template comments or placeholder text.
- For P4, require an actual STARs ID. If the user did not provide one and it cannot be found in the change context, ask for it before producing the final changelist description.
- For P4, produce the final changelist description without template comments, placeholder text, or synthetic separator lines, and append `STARs: <id>` as the final line.
- Use `type(scope): summary` when there is a clear scope; use `type: summary` when there is not.
- Prefer concise summaries under 72 characters.
- Include a body only when it adds useful context beyond the summary.
- Include validation only when the user provides it or the workflow explicitly needs it; do not add placeholder validation.
- Preserve issue IDs, review IDs, STARs IDs, or breaking-change footers when provided by the user or discovered in the change context.

## Output
Provide the commit message or changelist description ready to paste or submit.
