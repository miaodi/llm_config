---
name: coding
description: Use for implementing, debugging, or reviewing software behavior. Owns defect investigation and verification; add a language or build skill only for its specific decisions.
---

# Coding

## Scope

Own the path from observed behavior to a justified change or review finding. Language design,
build configuration, version control, and performance measurement belong to their named skills.

## Workflow

1. Read applicable project instructions and the relevant implementation, callers, and tests.
2. Establish expected behavior and reproduce the failure when practical. Distinguish source
   defects from environment, configuration, and input problems.
3. Trace the cause before editing. Preserve public contracts and unrelated work; change the
   smallest coherent unit that addresses the request.
4. Run checks that exercise the changed behavior. Add regression coverage for meaningful
   failure modes, not tests that merely reproduce the implementation.
5. Review the final diff for unintended changes and report actual verification results.

## Review mode

Findings need a concrete trigger, impact, and file location. Prioritize correctness and
regressions; distinguish confirmed defects from questions. Do not edit during a review-only
request. No findings is valid, but does not establish that untested behavior is correct.

## Completion

Complete authorized implementation and validation rather than returning only a plan.
Summarize the resulting behavior, evidence, and material limitations without a mandatory report template.
