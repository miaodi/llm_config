# Content Review — 2026-09-05

Reviewed every skill, agent, template, memory file, and repository document. Existing skill and
agent filenames remain stable; the cleanup retained 27 skills and 13 agents.
The subsequent addition of P4 Engineer brings the inventory to 14 agents, separating
Perforce operations and description generation from read-only defect review.

## Changes

- Added explicit triggers/exclusions and an [ownership map](skill-map.md). Removed duplicate
  priority/workflow/checklist/output sections where they restated the same rule.
- Reduced agents to outcome ownership, conditional skill selection, and completion evidence.
  Removed compulsory handoffs and blanket clarification/approval questions.
- Enabled execution for implementation and teaching roles so they can verify their own work.
  The P4 reviewer remains read-only in purpose and has no editor tool.
- Separated prose, markup, native page operations, report revision, figures, and TeX builds.
- Separated B2/CMake configuration from source diagnostics; removed speculative build-speed
  flags and syntax recipes that were not justified for a particular environment.
- Separated graph primitives from numerical methods. Corrected the confusion between BFS
  distance layers and dependency levels, SCC blocks and independent solves, and tree height
  and weighted schedule cost. Removed unsupported blanket parallel complexity claims.
- Replaced categorical sparse solver/format advice with assumptions, storage invariants,
  true-residual checks, breakdown handling, and total solve cost.
- Removed nonfunctional Nsight pseudocode and fixed comparison guidance to preserve launch
  identity, units, missing counters, and profiler replay effects.
- Removed blanket preferences for 1D GPU launches, shared memory, or new C++ features regardless
  of project support. Preserved useful ownership, compile-time, and host/device-boundary guidance.
- Added ML leakage/checkpoint checks and RL termination, truncation, budget, and evaluation distinctions.
- Kept the personal STARs convention in the message workflow; it no longer blocks code review.
- Replaced legacy Confluence macro assumptions with target-version/representation checks.

## Primary references checked

- [NetworkX topological generations](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.topological_generations.html)
- [PETSc CG assumptions](https://petsc.org/release/manualpages/KSP/KSPCG/)
- [Nsight Compute profiling guide](https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html)
- [B2 manual](https://www.bfgroup.xyz/b2/manual/release/index.html)

The cleanup removes brittle claims rather than treating a static skill as a replacement for
version-matched API documentation. Automated checks validate structure, references, and installation;
they do not prove model routing quality or every domain instruction's behavior in future sessions.

## Verification

- Nine automated checks cover all six targets, repeated installs, copy/link transitions,
  native metadata, references, instruction preservation, legacy migration, and source protection.
- Codex CLI 0.153.4 discovered all 27 revised skills with no parse errors or duplicate names.
- OpenCode 1.18.29 discovered all 27 skills after installing all three targets into one temporary
  project; its resolved P4 reviewer configuration disables editing/writing and retains skill access.
- Native Codex agent TOML is parsed by the test suite; no model-backed subagent task was run.
- Copilot formats/paths were checked against documentation; Copilot CLI was unavailable locally.
