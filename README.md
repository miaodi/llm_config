# llm-config

Central repository for LLM and agent configuration, reusable skills, prompts, and operating conventions.

## Installation

Run the setup script to install agents and skills into VS Code user-level directories, a project's `.github` directory, or Codex user-level directories.

```bash
./setup.sh                          # symlink user-level install (default)
./setup.sh --copy                   # copy user-level install
./setup.sh --project /path/to/repo  # symlink project install into .github/
./setup.sh --project /path/to/repo --copy
./setup.sh --codex                  # symlink Codex skills and reference agent specs
./setup.sh --codex --copy           # copy Codex skills and reference agent specs
```

User install targets:
- **Agents** → `~/.config/Code/User/agents/*.agent.md`
- **Skills** → `~/.copilot/skills/<name>/SKILL.md`

Project install targets:
- **Agents** → `<project>/.github/agents/*.agent.md`
- **Skills** → `<project>/.github/skills/<name>/SKILL.md`
- **Instructions** → `<project>/.github/copilot-instructions.md` (generated as a normal file, not a symlink)

Codex install targets:
- **Agent specs** → `~/.codex/agents/*.agent.md` (reference files; not currently registered as new `spawn_agent` types)
- **Skills** → `~/.codex/skills/<name>/SKILL.md`

Restart VS Code or reload the window after running VS Code installs. Restart Codex after running a Codex install.

### Per-project usage

To install into a single project with the script:

```bash
./setup.sh --project /path/to/your-project
```

The installer creates `.github/copilot-instructions.md` if it does not already exist, and preserves an existing file so you can keep project-specific guidance there.

### Codex Usage

To install system-level Codex skills and reference agent specs:

```bash
./setup.sh --codex
```

The Codex install places this repository's skills under `~/.codex/skills/` so they can be surfaced as reusable runtime guidance.

The current local Codex CLI runtime exposes spawnable sub-agent types through its tool schema. In this install, that schema is limited to `default`, `explorer`, and `worker`; placing `.agent.md` files under `~/.codex/agents/` does not register additional `spawn_agent` types. Keep Codex-facing reusable behavior in skills, and treat `~/.codex/agents/*.agent.md` as role/spec files unless the runtime adds a custom-agent registration mechanism.

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

## Skills (20)

| Skill | Domain |
|-------|--------|
| `agent-customization` | Custom agent and skill scope, tools, and delegation wording |
| `coding` | General implementation, debugging, refactoring |
| `shell` | Bash, zsh, csh/tcsh scripting, terminal automation, pipelines, portability, and shell debugging |
| `boost-build` | Boost.Build (b2/bjam), Jamfiles, toolsets, compiler error decoding, compile-time optimization |
| `modern-cmake` | Modern CMake, target usage requirements, presets, toolchains, C++/CUDA/nvcc build diagnosis |
| `cpp-elegance` | Modern C++ clarity, RAII, concepts, API design |
| `cpp-performance` | C++ hot-path optimization, cache, vectorization |
| `cuda-performance` | GPU kernel tuning, shared memory, coalescing |
| `sparse-linear-algebra` | Sparse matrices, iterative solvers, preconditioners, reorderings, graph sparsity |
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
