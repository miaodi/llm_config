---
name: p4-review
description: "Use when reviewing Perforce changelists, shelves, diffs, or generating changelist comments. Covers code review, pre-submit inspection, submission risk, and STARs ID tracking."
---

# P4 Review Skill

## Purpose
Review Perforce changelists and shelves for correctness, regressions, scope control, and submission risk, and generate concise changelist comments when requested.

## When To Use
Use for code review, pre-submit inspection, shelf review, changelist triage, or changelist comment generation in a Perforce workflow.

## Priorities
1. Find correctness issues and regressions first.
2. Review the actual changelist scope, not an imagined Git-style diff.
3. Check whether the changelist is reviewable as a unit.
4. Distinguish submitted, pending, and shelved context clearly.
5. Call out missing tests, risky integrations, or unresolved files.
6. Generate concise, meaningful changelist comments that describe the actual change clearly.

## Workflow
1. Identify the changelist or shelf under review and confirm whether it is pending, shelved, or submitted.
2. If changelist ID is missing or ambiguous, stop and ask for the exact changelist; do not assume `default`.
3. If a project STARs ID is required for the changelist comment and none has been provided, stop and ask for it explicitly.
4. Inspect the file list and file actions before reading individual diffs.
5. Review the diff against the correct base revision or stream.
6. Look for correctness bugs, behavioral regressions, missing validation, and risky assumptions.
7. Check whether integrates, resolves, or file moves make the review incomplete without more context.
8. Check whether the changelist is too broad or mixes unrelated concerns.
9. When requested to write a changelist comment, summarize the intent, scope, and impact in concise language grounded in the actual diff.
10. For description updates, keep the operation metadata-only and preserve the existing file membership unchanged.
11. Summarize findings by severity with file references and submission risk.

## Review Checklist
- Is the changelist internally coherent?
- Are the most important files actually in the review set?
- Are there unresolved merges, integrates, or branch-specific assumptions?
- Does the changelist depend on other pending or shelved work?
- Are tests or validation steps missing for risky changes?
- Is the shelf or changelist safe to submit as-is?
- Has the required STARs ID been provided?
- Does the changelist comment accurately describe what changed and why?
- Is the changelist comment concise enough to scan quickly?

## Constraints
- Findings come before summary.
- Focus on bugs, regressions, risky assumptions, and missing tests.
- Do not downgrade review rigor because the work is only shelved.
- Do not assume missing context is harmless; call it out explicitly.
- Do not assume or use the `default` changelist unless the user explicitly requests it.
- Do not run `p4` commands that can move files between changelists (for example `p4 reopen -c`, `p4 change -i` with altered file sections) when the request is review or description writing.
- If a STARs ID is required and missing, ask for it instead of inventing or omitting it.
- Do not generate vague changelist comments such as "misc fixes" or "updates".
- Keep changelist comments concise, specific, and tied to the real scope of the diff.

## Output
Provide:
- prioritized findings
- open questions or missing context
- submission readiness
- validation gaps
- changelist comment text when requested
