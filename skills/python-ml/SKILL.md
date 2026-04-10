---
name: python-ml
description: "Use when writing Python for machine learning projects, experiment scaffolding, training loops, evaluation, hyperparameter management, and reproducible ML workflows."
---

# Python ML Skill

## Purpose
Write Python code for machine learning projects that is clear, modular, reproducible, and easy to experiment with.

## When To Use
Use for model implementation, experiment scaffolding, training loops, evaluation code, and result analysis in Python-based ML projects.

## Priorities
1. Preserve correctness and reproducibility.
2. Keep experiment structure simple and inspectable.
3. Make it easy to compare baselines and hyperparameters.
4. Prefer readable code over framework cleverness.

## Workflow
1. Define the experiment interface: config, data flow, model, training, evaluation, and logging.
2. Keep hyperparameters centralized and easy to modify.
3. Separate reusable components from assignment-specific glue code.
4. Add clear metrics collection and result persistence.
5. Make it straightforward to run baselines, ablations, and repeated seeds.

## Review Checklist
- Are configs centralized?
- Can experiments be reproduced with the same seed and settings?
- Are train/eval paths clearly separated?
- Are metrics, checkpoints, and logs easy to inspect?
- Is the code easy to adapt for ablations and sweeps?

## Constraints
- Do not hide key experiment settings in scattered constants.
- Do not optimize for clever abstractions over debugging clarity.
- Keep dependencies and project structure appropriate for a course project.

## Output
Provide:
- implementation plan
- code structure recommendations
- experiment hooks
- evaluation and logging guidance
