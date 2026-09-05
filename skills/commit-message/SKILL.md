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

1. `.codex/llm-config/templates/commit-message/git-p4-commit-message-template.txt` in the repository root.
2. `${CODEX_HOME:-${HOME}/.codex}/llm-config/templates/commit-message/git-p4-commit-message-template.txt`.

### Copilot

1. `.github/llm-config/templates/commit-message/git-p4-commit-message-template.txt` in the repository root.
2. `${COPILOT_HOME:-${HOME}/.copilot}/llm-config/templates/commit-message/git-p4-commit-message-template.txt`.

### OpenCode

1. `.opencode/llm-config/templates/commit-message/git-p4-commit-message-template.txt` in the repository root.
2. `${OPENCODE_CONFIG_DIR:-${XDG_CONFIG_HOME:-${HOME}/.config}/opencode}/llm-config/templates/commit-message/git-p4-commit-message-template.txt`.

If the product cannot be determined from the active agent environment, ask the
user which product is invoking the skill instead of searching all product paths.

When working directly from this llm-config source checkout, the source template
at `templates/commit-message/git-p4-commit-message-template.txt` may be used as
the repository-local template.

Use that file as the single source of truth for message shape and allowed sections.

## Rules

- Follow the shared template for shape and allowed sections; omit unused optional sections.
- Base the summary on the actual change. Preserve identifiers supplied in context and distinguish
  observed validation from suggested commands.
- This personal P4 workflow requires an actual STARs ID in a final description. If missing,
  complete the review/draftable work and ask for the ID before finalizing the description.
  Never invent an ID. This is a personal convention, not a Perforce requirement.
- Drafting text does not stage, commit, publish, submit, or alter changelist membership.

Return the message ready to use, without template comments or fabricated validation.
