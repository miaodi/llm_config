# Contribution Guide

## Ownership

- Skills own reusable methods; agents own outcomes and select methods.
- `memory/` owns personal defaults. Project instructions own repository-specific requirements.
- Descriptions are routing rules: give a concrete trigger and distinguish the nearest neighbor.
- Prefer extending the existing owner over adding another file with the same responsibility.
- Boundaries do not force handoffs. Load another skill only when its decision is needed.

## Review

1. Check the new trigger and a neighboring non-trigger against `docs/skill-map.md`.
2. Keep domain-specific invariants and useful examples; remove duplicated checklists and slogans.
3. Verify technical claims with primary/version-matched sources. Avoid universal performance
   claims, default algorithm lists, and examples that silently do nothing.
4. Keep instructions executable with the role's tool set. Do not forbid the validation needed
   to finish implementation or require approval already granted in the task.
5. Validate frontmatter, local references, native installer output, and repeat-install behavior
   with `python3 -m unittest discover -s tests -v`.
6. Update the skill map and README for scope, inventory, or installation changes.
