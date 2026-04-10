# Reinforcement Learning Skill

## Purpose
Design, implement, evaluate, and analyze reinforcement learning experiments with clear baselines, sound metrics, and algorithm-appropriate hyperparameters.

## When To Use
Use for RL assignments, environment analysis, algorithm selection, training design, evaluation planning, hyperparameter tuning, and result interpretation.

## Priorities
1. Match the algorithm to the environment and project goal.
2. Establish baselines before tuning advanced methods.
3. Evaluate stability, sample efficiency, and variance across seeds.
4. Analyze why a method works or fails, not just whether reward increased.

## Workflow
1. Characterize the task: environment type, action space, observability, reward structure, horizon, and stochasticity.
2. Choose reasonable baselines and one or two advanced algorithms that fit the setting.
3. Define training budget, evaluation protocol, and success metrics before running experiments.
4. Select algorithm-specific hyperparameters to tune rather than using a generic sweep blindly.
5. Run repeated seeds and compare convergence speed, stability, and final performance.
6. Suggest plots that reveal behavior, not just final scores.
7. Analyze output in terms of variance, convergence, sample efficiency, brittleness, and failure modes.

## Suggested Plots
- reward versus environment steps
- reward versus wall-clock time
- mean and variance across seeds
- ablation plots for key design choices
- sensitivity plots for critical hyperparameters
- success rate or episode length where relevant
- policy/value diagnostics when they explain behavior

## Hyperparameter Guidance
- Tune algorithm-specific parameters first: learning rate, target-update cadence, entropy coefficient, clipping parameter, discount factor, lambda, rollout length, batch size, replay size, exploration schedule, and network size.
- Prefer small targeted sweeps guided by algorithm behavior.
- Track both best setting and sensitivity, not only the maximum score.

## Constraints
- Do not recommend advanced RL algorithms without explaining why they fit the environment.
- Do not trust a single seed.
- Do not present unstable reward curves without discussing variance and failure modes.
- Distinguish training reward from evaluation performance.

## Output
Provide:
- algorithm recommendation
- baseline plan
- hyperparameters to try
- plots to generate
- output analysis and interpretation guidance
