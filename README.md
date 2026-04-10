# llm-config

Central repository for LLM and agent configuration, reusable skills, prompts, and operating conventions.

## Structure

- `skills/` reusable task-specific instructions
- `agents/` role definitions and agent personas
- `templates/` starter templates for new configs
- `memory/` long-lived preferences and conventions
- `docs/` documentation for contributors

## Conventions

- Keep skills small and composable.
- Prefer one responsibility per file.
- Use Markdown unless a tool requires another format.
- Version changes with clear commit messages.

## Getting Started

1. Copy `templates/skill-template.md` when creating a new skill.
2. Copy `templates/agent-template.md` when creating a new agent definition.
3. Document shared assumptions in `memory/`.
4. Keep repo-wide guidance in `docs/`.
