---
name: agent-customization
description: "Use when creating, refining, or reviewing a custom agent (.agent.md), choosing its scope and tools, improving delegation keywords, or deciding whether guidance belongs in a reusable skill instead."
---

# Agent Customization Skill

## Purpose
Create focused custom agents that match a real workflow, use the minimum necessary tools, and stay aligned with this repository's templates and conventions.

## When To Use
Use when drafting a new `.agent.md`, tightening an existing agent's scope, choosing tools, improving discovery wording, or separating reusable guidance into a companion skill.

## Priorities
1. Keep the agent single-purpose and easy to delegate to.
2. Choose the minimum tool set that supports the job.
3. Make the description concrete enough for subagent discovery.
4. Distinguish clearly between agent responsibilities and skill guidance before drafting either file.
5. Follow this repository's templates, naming patterns, and contribution guidance.

## Agent Vs Skill
- Create an agent when the problem is a role: a job with a clear owner, operating boundaries, tool choices, and delegation triggers.
- Create a skill when the problem is reusable guidance: a method, checklist, style rule set, or domain playbook that more than one agent could follow.
- Prefer an agent when the file needs to answer "when should this specialist be chosen over the default agent?"
- Prefer a skill when the file needs to answer "how should work in this domain be done well every time?"
- If the request mixes both, keep the agent thin and move the reusable procedure into a skill that the agent names in its body.

## Workflow
1. Identify the real job: what the agent owns, when it should be chosen, and what it should not do.
2. Decide explicitly whether the primary artifact should be an agent, a skill, or a paired agent-plus-skill design.
3. Read `templates/agent-template.md`, `docs/contribution-guide.md`, and nearby `agents/*.agent.md` or `skills/*/SKILL.md` files before drafting.
4. Pick the smallest tool set that still lets the agent do its job safely and effectively.
5. Write a keyword-rich description, clear role, concrete goals, explicit non-goals, and practical heuristics.
6. Move reusable methods, checklists, and domain rules into a new or existing skill instead of the agent body.
7. Save the draft, then identify the most ambiguous design choice and ask only the follow-up questions that materially improve the result.

## Review Checklist
- Is the agent solving one clear job rather than several loosely related ones?
- Is this actually an agent problem, or would a skill be the more meaningful artifact?
- Does the description contain trigger phrases a parent agent could actually match on?
- Are the tools minimal, and are any powerful tools justified?
- Do the goals and non-goals make the boundary obvious?
- Would some of the body be better as a reusable skill?
- Does the file match the repo template and nearby style?
- Is the agent name aligned with its real responsibility?

## Constraints
- Do not create swiss-army agents with vague, overlapping responsibilities.
- Do not add `execute` or `web` unless there is a concrete reason.
- Do not duplicate large blocks of reusable guidance across multiple agents.
- Do not leave delegation wording generic when concrete trigger phrases are available.
- Do not rewrite unrelated agents just to normalize style.

## Output
Provide:
- the drafted or revised `.agent.md`, `SKILL.md`, or paired design
- the reason this should be an agent, a skill, or both
- the intended use case and trigger conditions
- the chosen tools and why they are sufficient
- any open questions that would materially improve the design
- any recommended companion skill or follow-up customization