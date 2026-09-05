---
name: handoff-document
description: Use when the user requests a durable pause/resume note or context transfer for another session or person. Not for routine progress updates or final summaries.
---

# Handoff Document

## Scope

Own resumable task state, not general documentation or a transcript of the conversation.

## Method

- Use the requested path or existing handoff convention. Otherwise write
  `handoffs/YYYY-MM-DD-<topic>.md`; avoid overwriting an unrelated handoff.
- Refresh relevant state: workspace, branch/commit, uncommitted changes, active environment,
  artifacts, and running work. Record only details needed to resume.
- Preserve the user's goal, accepted constraints, decisions, completed work, and outstanding work.
- Separate confirmed results from hypotheses and proposed next steps.
- Record actual verification commands and outcomes, plus decisive failed approaches worth avoiding.
- Put the next action near the top, with enough path/command context to execute it.
- Exclude credentials, irrelevant logs, and transient details that do not affect resumption.

## Suggested structure

Goal and acceptance criteria; current state; changes and evidence; remaining work; next action.
Include environment and recovery notes only when needed. Omit empty sections. The handoff should
be understandable without earlier chat and should not claim that proposed commands already ran.
