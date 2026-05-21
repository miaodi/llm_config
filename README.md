# llm-config

Central repository for LLM and agent configuration, reusable skills, prompts, and operating conventions.

## Installation

Run the setup script to install agents and skills into Copilot, Codex, or OpenCode user-level directories, or into a project-local configuration directory. Choose one explicit install target; bare `./setup.sh` does not perform an install.

```bash
./setup.sh --copilot                # symlink Copilot user-level install
./setup.sh --copilot --copy         # copy Copilot user-level install
./setup.sh --copilot-project /path/to/repo
./setup.sh --copilot-project /path/to/repo --copy
./setup.sh --codex                  # symlink Codex skills and agent specs
./setup.sh --codex --copy           # copy Codex skills and agent specs
./setup.sh --opencode               # install OpenCode skills and agents
./setup.sh --opencode --copy        # copy OpenCode skills and agents
./setup.sh --opencode-project /path/to/repo
```

Copilot install targets:
- **Agents** → `~/.copilot/agents/*.agent.md`
- **Skills** → `~/.copilot/skills/<name>/SKILL.md`

Copilot project install targets:
- **Agents** → `<project>/.github/agents/*.agent.md`
- **Agents (Claude format)** → `<project>/.claude/agents/*.agent.md`
- **Skills** → `<project>/.github/skills/<name>/SKILL.md`
- **Instructions** → `<project>/.github/copilot-instructions.md` (generated as a normal file, not a symlink)

Agent frontmatter uses `name` and `target: vscode` for Copilot/VS Code discovery. Codex installs the same Markdown agent specs under `~/.codex/agents/`; Claude-format agents under `.claude/agents/` may need separate Claude-specific metadata, so do not rely on `target: vscode` as a portable Codex or Claude registration field.

Codex install targets:
- **Agent specs** → `~/.codex/agents/*.agent.md`
- **Skills** → `~/.codex/skills/<name>/SKILL.md`

OpenCode install targets:
- **Agents** → `~/.config/opencode/agents/*.md`
- **Skills** → `~/.config/opencode/skills/<name>/SKILL.md`

OpenCode project install targets:
- **Agents** → `<project>/.opencode/agents/*.md`
- **Skills** → `<project>/.opencode/skills/<name>/SKILL.md`

OpenCode also discovers skills from Claude-compatible `.claude/skills/<name>/SKILL.md` and agent-compatible `.agents/skills/<name>/SKILL.md` paths, but Markdown agent definitions belong in `~/.config/opencode/agents/` globally or `.opencode/agents/` per project. The installer writes OpenCode agents as native `*.md` files with OpenCode frontmatter; the filename becomes the OpenCode agent name.

Restart VS Code or reload the window after running VS Code installs. Restart Codex after running a Codex install. Restart OpenCode after running an OpenCode install.

### Per-project usage

To install into a single project with the script:

```bash
./setup.sh --copilot-project /path/to/your-project
```

The installer creates `.github/copilot-instructions.md` if it does not already exist, and preserves an existing file so you can keep project-specific guidance there.

### Codex Usage

To install system-level Codex skills and agent specs:

```bash
./setup.sh --codex
```

The Codex install places this repository's agents under `~/.codex/agents/` and skills under `~/.codex/skills/`. By default, these are symlinked back to this repository so edits here are visible after restarting Codex.

With `child_agents_md` enabled in Codex, the Markdown agent specs in `~/.codex/agents/` can be used as child-agent guidance. Keep reusable methods in skills and focused role definitions in agents.

### OpenCode Usage

To install system-level OpenCode skills and agents:

```bash
./setup.sh --opencode
```

The OpenCode install places this repository's skills under `~/.config/opencode/skills/` and agents under `~/.config/opencode/agents/`. For a project-local install, use `./setup.sh --opencode-project /path/to/repo`.

## Structure

- `agents/` — agent definitions (`*.agent.md` with YAML frontmatter)
- `skills/` — reusable task skills (`SKILL.md` with YAML frontmatter, one per directory)
- `templates/` — starter templates for new configs
- `memory/` — long-lived preferences and conventions
- `docs/` — documentation for contributors

## Agents

| Agent | Description |
|-------|-------------|
| `agent-creator` | Custom agent and skill design for this repository |
| `cpp-engineer` | Modern C++ design, type safety, ownership, compile-time computation |
| `document-writer` | Markdown, Confluence, LaTeX, and report editing |
| `p4-reviewer` | Perforce changelist review, submission readiness, changelist comments |
| `performance-engineer` | Runtime performance, profiling, bottleneck analysis, C++/CUDA tuning |
| `course-project-worker` | Course projects end-to-end: spec extraction, Python ML, RL, LaTeX reports |
| `build-engineer` | Boost.Build (b2/bjam), gcc/clang/nvcc error diagnosis, template errors, compilation speed |
| `cmake-project-builder` | Modern CMake projects, CMakePresets, C++/CUDA build errors, custom CMake functions |
| `git-integrator` | Git branch integration: merge/rebase strategy, conflict resolution, branch sync, and safe recovery |
| `git-publisher` | Git commit and push workflow: status, diff review, staging, commit messages, and publishing |

## Skills (23)

| Skill | Domain |
|-------|--------|
| `agent-customization` | Custom agent and skill scope, tools, and delegation wording |
| `coding` | General implementation, debugging, refactoring |
| `git-workflow` | Git branch workflows, merge/rebase decisions, conflict resolution, history cleanup, and recovery |
| `shell` | Bash, zsh, csh/tcsh scripting, terminal automation, pipelines, portability, and shell debugging |
| `boost-build` | Boost.Build (b2/bjam), Jamfiles, toolsets, compiler error decoding, compile-time optimization |
| `modern-cmake` | Modern CMake, target usage requirements, presets, toolchains, C++/CUDA/nvcc build diagnosis |
| `cpp-elegance` | Modern C++ clarity, RAII, concepts, API design |
| `cpp-performance` | C++ hot-path optimization, cache, vectorization |
| `cuda-performance` | GPU kernel tuning, shared memory, coalescing |
| `ncu-analysis` | Nsight Compute profiling, report extraction, and CUDA bottleneck diagnosis |
| `sparse-linear-algebra` | Sparse matrices, iterative solvers, preconditioners, reorderings, graph sparsity |
| `handoff-document` | Session handoff files for pausing, resuming, and transferring agent context |
| `p4-review` | Perforce code review and changelist comments |
| `p4-workflow` | Perforce changelist and shelf management |
| `research` | Technical investigation and synthesis |
| `writing` | Editing, summarization, style normalization |
| `markdown-editing` | Markdown documentation, tables, links, and GitHub formatting |
| `confluence-editing` | Confluence pages, team wiki structure, and macro-aware editing |
| `latex-tikz` | LaTeX documents and TikZ/PGFPlots figures |
| `pdf-requirements-review` | PDF spec extraction and project planning |
| `python-ml` | Python ML experiment scaffolding |
| `reinforcement-learning` | RL experiment design and analysis |
| `report-iteration-overleaf` | Report iteration and Overleaf workflows |

## Conventions

- Keep skills small and composable.
- Prefer one responsibility per file.
- Use Markdown unless a tool requires another format.
- Version changes with clear commit messages.

## Adding New Content

1. Copy `templates/skill-template.md` when creating a new skill.
2. Copy `templates/agent-template.md` when creating a new agent definition.
3. Document shared assumptions in `memory/`.
4. Re-run `./setup.sh` to pick up new files.
