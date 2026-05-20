---
name: commit-message
description: "Use when drafting, reviewing, or normalizing Git commit messages or Perforce changelist descriptions from the shared Git/P4 commit message template."
---

# Commit Message Skill

## Purpose
Draft concise, reviewable commit messages and P4 changelist descriptions from the shared template.

## Shared Template
Before drafting a message, read the first available template path:

1. `templates/commit-message/git-p4-commit-message-template.txt` in the current repository root.
2. `../../templates/commit-message/git-p4-commit-message-template.txt` relative to this skill directory.
3. `${HOME}/.codex/templates/commit-message/git-p4-commit-message-template.txt` for Codex user installs.
4. `.github/templates/commit-message/git-p4-commit-message-template.txt` for project installs.
5. `${HOME}/.config/Code/User/templates/commit-message/git-p4-commit-message-template.txt` for VS Code user installs.

Use that file as the single source of truth for message shape and allowed sections.

## Rules
- For Git, produce the final message without template comments or placeholder text.
- For P4, require an actual STARs ID. If the user did not provide one and it cannot be found in the change context, ask for it before producing the final changelist description.
- For P4, produce the final changelist description without template comments, placeholder text, or synthetic separator lines, and append `STARs: <id>` as the final line.
- Use `type(scope): summary` when there is a clear scope; use `type: summary` when there is not.
- Prefer concise summaries under 72 characters.
- Include a body only when it adds useful context beyond the summary.
- Include validation when known; otherwise write `Validation: Not run` only if useful for the workflow.
- Preserve issue IDs, review IDs, STARs IDs, or breaking-change footers when provided by the user or discovered in the change context.

## Output
Provide the commit message or changelist description ready to paste or submit.
