---
name: handoff-document
description: "Use when documenting current work so another agent or future session can resume seamlessly: writing session handoff docs, pause/resume notes, context-transfer files, transition plans, extended debugging summaries, implementation status reports, or when the user says they need to take a break, start a new session, continue later, or onboard the next agent."
---

# Handoff Document Skill

## Purpose
Create a self-contained Markdown handoff file that lets a future agent resume work without relying on prior chat history.

## When To Use
Use when the user asks to pause, start a new session, transfer context to another agent, summarize current progress, or preserve the state of a long-running implementation, debugging, research, review, or build task.

## Priorities
1. Continuity: the next agent should know the goal, current state, and exact next step.
2. Accuracy: distinguish confirmed facts from assumptions, hypotheses, and unknowns.
3. Traceability: name files, commands, errors, decisions, and artifacts precisely.
4. Actionability: include a prioritized resume checklist, not just a narrative summary.
5. Brevity with completeness: preserve important context without dumping full logs or chat transcripts.

## File Placement
- Use the path requested by the user.
- Otherwise, follow any existing project convention such as `handoffs/`, `docs/handoffs/`, or `notes/handoffs/`.
- If no convention exists, create `handoffs/YYYY-MM-DD-<short-topic>.md` at the workspace root.
- Do not overwrite an existing handoff unless the user asks; add a timestamp or numeric suffix instead.

## Workflow
1. Refresh the local state before writing:
   - Record the current workspace, branch, short commit, and dirty worktree state.
   - Check `git status --short`, relevant diffs, and touched files when available.
   - Capture the current date, timezone, and any active environment, build preset, virtualenv, container, or hardware assumptions that matter.
2. Reconstruct the goal:
   - State the user's original objective and any acceptance criteria.
   - List constraints, preferences, deadlines, or non-goals that shaped the work.
3. Document what changed:
   - Summarize implemented changes by file or module.
   - Include why each important change was made.
   - Link or name generated artifacts, reports, logs, benchmark outputs, screenshots, or test data.
4. Document what was tried:
   - Record failed attempts, rejected approaches, errors encountered, and the reason each path was abandoned.
   - Include short error excerpts only when they help the next agent recognize the issue.
5. Document verification:
   - List commands that were run and their outcomes.
   - State clearly when tests, builds, profilers, or manual checks were not run.
   - Note what is working, what is partially working, and what remains unverified.
6. Write the handoff file using the template below.
7. Review the file from the next agent's perspective:
   - Can they identify the first command to run?
   - Can they tell which files are safe to edit next?
   - Can they avoid repeating known dead ends?
   - Can they see every blocker, open question, and risk?

## Handoff Template
````markdown
# Handoff: <short task title>

Date: <YYYY-MM-DD HH:MM timezone>
Workspace: `<absolute or repo-relative path>`
Branch: `<branch>`
Commit: `<short commit or unknown>`
Status: <in progress | blocked | ready for review | verification needed>

## Goal
<What we are trying to accomplish and what "done" means.>

## Current State
<One-screen summary of where the work stands now. Include the most important fact first.>

## Implemented
- `<path>`: <what changed and why>
- `<path>`: <what changed and why>

## Working
- <Behavior, command, test, build, or workflow that currently works.>

## Not Working / Blocked
- <Failure, blocker, or missing dependency. Include concise error excerpts if useful.>

## Tried Already
- <Attempt>: <result and why not to repeat it>

## Verification
- `<command>`: <passed | failed | not run | partial> - <short outcome>

## Important Files And Artifacts
- `<path>`: <why it matters>

## Open Questions
- <Question or decision the next agent/user must resolve.>

## Next Steps
1. <Highest-priority next action, including exact command or file to inspect.>
2. <Second action.>
3. <Third action.>

## Resume Commands
```bash
<commands that recreate the useful local context>
```

## Notes For The Next Agent
<Risks, assumptions, user preferences, or context that does not fit elsewhere.>
````

## Review Checklist
- Is the handoff self-contained without the prior conversation?
- Are implemented changes separated from attempted but abandoned work?
- Are passing, failing, partial, and unrun checks labeled honestly?
- Are file paths, commands, branches, commits, and artifacts specific?
- Are next steps ordered by priority?
- Are secrets, credentials, private tokens, and irrelevant log dumps excluded?

## Constraints
- Do not claim a test, build, benchmark, profiler, or manual check passed unless it was actually run and observed.
- Do not hide uncertainty; write `unknown`, `not checked`, or `not verified` where appropriate.
- Do not include secrets or credentials. Redact sensitive values while preserving enough context to debug.
- Do not turn the handoff into a full transcript. Summarize decisions and outcomes.
- Do not modify unrelated project files while creating the handoff.

## Output
Create or update the handoff Markdown file, then report:
- the file path
- the most important resume point
- any verification gaps the next agent should know immediately
