# P4 Workflow Skill

## Purpose
Work effectively in a Perforce-based codebase with explicit awareness of changelists, shelves, depot state, and review workflow.

## When To Use
Use when inspecting pending work, managing changelists, reviewing shelves, comparing revisions, or preparing code for submission in a P4 environment.

## Priorities
1. Preserve the intended changelist scope.
2. Understand depot state before making assumptions about local changes.
3. Treat shelves and pending changelists as first-class review units.
4. Avoid mixing unrelated work into the same changelist.
5. Be explicit about what is local, shelved, pending, or submitted.

## Workflow
1. Identify the relevant changelist, shelf, stream, and depot path before reviewing or editing.
2. Inspect pending files, shelved files, and file actions before reasoning about the change.
3. Distinguish local workspace state from depot history and submitted revisions.
4. Compare the changelist against the correct base revision or stream.
5. Keep edits scoped to the intended changelist and avoid folding unrelated files into it.
6. Call out integration, resolve, and branch history concerns when they affect correctness.
7. Summarize findings in terms of files, changelist scope, and submission risk.

## Review Checklist
- What changelist or shelf is under review?
- Are the files in the changelist actually related?
- Are there adds, deletes, moves, integrates, or resolves that change the risk profile?
- Is the comparison being made against the correct depot revision or stream?
- Is any relevant context still only shelved and not yet submitted?
- Could workspace state be hiding missing files or stale assumptions?
- Is the changelist too broad to review confidently?

## Constraints
- Do not assume Git-style workflows or terminology when the codebase uses Perforce.
- Do not treat a pending changelist as equivalent to submitted history.
- Do not ignore shelves, integrates, or resolves when they affect the meaning of the change.
- Do not mix unrelated fixes into an existing changelist without stating it clearly.

## Output
Provide:
- the changelist or shelf being discussed
- the effective scope of the work
- any depot-history or integration concerns
- the review or implementation recommendation
- any follow-up needed before submission
