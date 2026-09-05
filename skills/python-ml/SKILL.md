---
name: python-ml
description: Use for Python ML data pipelines, training/evaluation code, experiment configuration, checkpoints, and reproducibility. Reinforcement-learning method and evaluation choices belong to reinforcement-learning.
---

# Python ML Engineering

## Scope

Own experiment implementation and artifact integrity. `reinforcement-learning` owns RL-specific
algorithm/evaluation decisions; `research` owns literature comparison.

## Method

- Follow the existing framework and environment. Keep configuration explicit and persist the
  resolved settings, code revision, dependency versions, seeds, and dataset identity with results.
- Separate data preparation, training, evaluation, and logging without adding a framework for
  a small experiment. Prevent split leakage and fitting preprocessing on held-out data.
- Check shapes, dtypes, device placement, batching, loss reduction, and optimizer/gradient behavior.
- Use the framework's training/evaluation and gradient modes deliberately; they are not synonymous.
- Start with a small smoke run and sanity baseline before spending the full compute budget.
- Save enough state for the intended resume semantics: weights, optimizer/scheduler, counters,
  and RNG/data-loader state when exact continuation is required.
- Record raw metrics and failures; do not overwrite runs silently or report only favorable seeds.
- Seed relevant generators, but do not promise bitwise reproducibility across hardware and kernels.

Verify a small end-to-end run and the relevant checkpoint/evaluation path. Report measured
results separately from planned experiments; do not train indefinitely to satisfy an imagined target.
