---
name: reinforcement-learning
description: Use for RL task formulation, algorithm/update correctness, environment termination semantics, sample budgets, and policy evaluation. Python project scaffolding belongs to python-ml.
---

# Reinforcement Learning

## Scope

Own RL methodology and interpretation. `python-ml` handles implementation structure and artifacts.

## Method

1. Characterize observations, actions, partial observability, reward, horizon, stochasticity,
   and reset/termination semantics. Match the method to these properties and the allowed budget.
2. Establish a suitable baseline; add complexity only when it addresses an observed limitation
   or a requested comparison. Do not add advanced algorithms merely to complete a template.
3. Check update semantics: on/off-policy data, bootstrap masks, target updates, advantage/return
   computation, exploration, clipping, and recurrent-state handling as applicable.
4. Distinguish true termination from time-limit truncation. Bootstrap according to the task's
   terminal definition and algorithm; verify the environment API actually provides the needed state.
5. Define held-out evaluation, training budget in environment steps and wall time, checkpoint
   selection, action stochasticity, and normalization behavior before comparing methods.
6. Compare repeated independent runs when making stability claims. Separate variation across
   training seeds from evaluation episodes; a single seed is a smoke test, not robust evidence.
7. Plot raw and, if useful, smoothed curves with smoothing disclosed. Report sample efficiency,
   final policy quality, failure rates, and uncertainty appropriate to available runs.

Tune a few parameters tied to the failure hypothesis. Keep evaluation data out of repeated
unreported selection, compare methods under stated budgets, and distinguish training reward
from evaluation performance. Never fabricate a convergence or success claim from incomplete runs.
