# Skill and Agent Ownership

Select by the decision being made, not file extension or keywords alone. A task can need
several skills in sequence; boundaries do not require delegation or stopping work.

| Skill | Owns | Use the neighbor for |
| --- | --- | --- |
| coding | Defect investigation, behavior changes, verification | Language design, build configuration, Git operations |
| cpp-elegance | C++ ownership, lifetimes, interfaces, generic design | cpp-performance for measured CPU costs |
| cpp-performance | CPU runtime measurement and optimization | cuda-performance for GPU kernels/pipelines |
| cuda-performance | GPU implementation and pipeline optimization | ncu-analysis for report mechanics |
| ncu-analysis | Nsight Compute capture, extraction, matched comparisons | cuda-performance for optimization; timelines for host overlap |
| boost-build | B2/Jam requirements and generated commands | modern-cmake for CMake; cpp-elegance for source type issues |
| modern-cmake | CMake target graph, presets, exports, toolchains | Source defects and runtime performance |
| shell | Shell semantics, quoting, processes, startup, script reliability | The invoked command's domain semantics |
| sparse-linear-algebra | Numerical methods, storage, convergence, matrix dependencies | graph-algorithms for generic graph primitives |
| graph-algorithms | Traversal, graph invariants, dependency scheduling | Sparse numerical interpretation and hardware tuning |
| computational-learning-notes | A runnable concept demonstration and explanation | Production performance optimization |
| python-ml | Experiment implementation, data integrity, checkpoints | reinforcement-learning for RL methodology |
| reinforcement-learning | RL updates, task formulation, evaluation | python-ml for project scaffolding |
| paper-review | A single paper’s contribution, results, proof roadmap, and critical assessment | research for broad literature synthesis; writing for prose editing |
| research | External evidence gathering and synthesis | coding for ordinary local source inspection |
| writing | Prose, argument, meaning, tone | markdown-editing for markup; research for new evidence |
| markdown-editing | Markdown rendering, fences, tables, links | writing for prose even in a Markdown file |
| confluence-editing | Native page representation and version-aware changes | writing for prose and argument |
| latex-tikz | TikZ/PGFPlots figure source and layout | latex-project-build for document compilation |
| latex-project-build | Root/engine detection and TeX build pipeline | Figure design and report revision |
| report-iteration-overleaf | Prior-report revision and Overleaf source packaging | Standalone prose, figures, or build repairs |
| pdf-requirements-review | PDF requirements and acceptance traceability | Arbitrary PDF summary or whole-project execution |
| handoff-document | Durable state for resuming a task | Routine progress updates or final answers |
| git-workflow | Branch integration, conflicts, history recovery | Git Publisher for routine commits/pushes |
| p4-workflow | Perforce state and authorized mutations | p4-review for findings |
| p4-review | Read-only changelist/shelf review | p4-workflow for mutations; commit-message for descriptions |
| commit-message | Shared Git/P4 message template | Staging, publishing, and changelist operations |
| agent-customization | Reusable role/skill boundaries and formats | AGENTS.md Writer for project-local working instructions |

## Agents

Agents own outcomes and select the skills above. They do not repeat the method:

- **C++ Engineer:** correct C++ implementation through validation.
- **Boost.Build Engineer / CMake Project Builder:** build-system-specific repairs or configuration.
- **Performance Engineer:** measured CPU/GPU application improvement.
- **Sparse Parallel Engineer:** numerical method and dependency design.
- **Computational Learning Coach:** a runnable lesson.
- **Course Project Worker:** multi-stage assignment completion and requirement coverage.
- **Document Writer:** technical document authorship.
- **Paper Reviewer:** source-grounded individual paper review and accessible proof explanation.
- **AGENTS.md Writer:** evidence-based repository operating instructions.
- **Agent Creator:** reusable customization design.
- **Git Integrator / Git Publisher:** integration versus routine publication.
- **P4 Reviewer:** read-only defect review.
- **P4 Engineer:** authorized Perforce operations and description generation/updates,
  using `p4-workflow` and, when needed, `commit-message`.

Shared personal preferences remain in `memory/`. Project-specific facts belong in the target
repository's instructions. Platform discovery and format conversion belong in the installer.

## Conditional coverage

All 28 skills are referenced by at least one agent, either in its skill list or conditional
completion guidance. These references select methods only when needed:

- **Document Writer:** `handoff-document` for requested pause/resume notes, and `research`
  for external evidence. Web access supports that research work.
- **Course Project Worker:** `research` for evidence gathering or literature comparison.
- **Build and Git/P4 agents:** `shell` for script semantics or command composition, not routine
  command invocation. P4 Reviewer uses it only within read-only review/inspection.

These conditional capabilities do not introduce new agents or expand authorization for the task.
