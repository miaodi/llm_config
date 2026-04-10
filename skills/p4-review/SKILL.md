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
2. If a project STARs ID is required for the changelist comment and none has been provided, stop and ask for it explicitly.
3. Inspect the file list and file actions before reading individual diffs.
4. Review the diff against the correct base revision or stream.
5. Look for correctness bugs, behavioral regressions, missing validation, and risky assumptions.
6. Check whether integrates, resolves, or file moves make the review incomplete without more context.
7. Check whether the changelist is too broad or mixes unrelated concerns.
8. When requested to write a changelist comment, summarize the intent, scope, and impact in concise language grounded in the actual diff.
9. Summarize findings by severity with file references and submission risk.

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
