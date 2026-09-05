---
name: agent-customization
description: Use to design reusable custom-agent roles or skills and decide their boundaries, triggers, tools, and native product format. Repository-specific AGENTS.md instructions are a separate artifact.
---

# Agent and Skill Design

## Scope

Own reusable role/skill design. An agent defines responsibility and completion; a skill provides
one reusable method; project `AGENTS.md` records repository-specific working instructions.
Do not create an agent merely because a skill exists.

## Method

1. Identify the requested outcome and its nearest existing owner. Extend that owner if the new
   behavior fits; create a new artifact only for a distinct responsibility or reusable procedure.
2. Read `templates/agent-template.md`, `templates/skill-template.md`, and
   `docs/contribution-guide.md` through the installed resource map or source checkout.
3. Give the description a concrete trigger and exclusion. Avoid broad keyword lists that cause
   several skills to claim the same task.
4. Keep agents thin: responsibility, selected skills, boundaries, and completion evidence. Keep
   detailed algorithms/checklists in skills and shared personal preferences in `memory/`.
5. Select tools needed to finish the job, including validation. Do not create an implementation
   role that is forbidden to run its tests unless the user specifically wants advisory-only work.
6. Follow the target product's current schema/discovery rules. YAML agent files are not portable
   registrations for every product; use the installer adapters and validate their outputs.
7. Check a representative trigger, a neighboring non-trigger, referenced resources, and overlap
   with existing files. Scope boundaries guide skill selection, not mandatory handoffs.

Resolve routine choices from context. Do not add boilerplate permission questions, compulsory
delegation, or requests to reapprove already authorized work.
