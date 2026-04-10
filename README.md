# llm-config

Central repository for LLM and agent configuration, reusable skills, prompts, and operating conventions — in VS Code Copilot's native format.

## Installation

Run the setup script to symlink agents and skills into your VS Code user-level directories so they work across all workspaces:

```bash
./setup.sh            # symlink (default — tracks repo changes automatically)
./setup.sh --copy     # copy instead of symlink
```

This installs:
- **Agents** → `~/.config/Code/User/prompts/*.agent.md`
- **Skills** → `~/.copilot/skills/<name>/SKILL.md`

Restart VS Code or reload the window after running.

### Per-project usage

To use in a single project instead, symlink or copy into that project's `.github/` directory:

```bash
ln -s /path/to/llm-config/agents/*.agent.md  your-project/.github/agents/
ln -s /path/to/llm-config/skills/*           your-project/.github/skills/
```

## Structure

- `agents/` — agent definitions (`*.agent.md` with YAML frontmatter)
- `skills/` — reusable task skills (`SKILL.md` with YAML frontmatter, one per directory)
- `templates/` — starter templates for new configs
- `memory/` — long-lived preferences and conventions
- `docs/` — documentation for contributors

## Agents

| Agent | Description |
|-------|-------------|
| `cpp-engineer` | Modern C++ design, type safety, ownership, compile-time computation |
| `p4-reviewer` | Perforce changelist review, submission readiness, changelist comments |
| `performance-engineer` | Runtime performance, profiling, bottleneck analysis, C++/CUDA tuning |
| `course-project-worker` | Course projects end-to-end: spec extraction, Python ML, RL, LaTeX reports |
| `build-engineer` | Boost.Build (b2/bjam), gcc/clang/nvcc error diagnosis, template errors, compilation speed |

## Skills (14)

| Skill | Domain |
|-------|--------|
| `coding` | General implementation, debugging, refactoring |
| `boost-build` | Boost.Build (b2/bjam), Jamfiles, toolsets, compiler error decoding, compile-time optimization |
| `cpp-elegance` | Modern C++ clarity, RAII, concepts, API design |
| `cpp-performance` | C++ hot-path optimization, cache, vectorization |
| `cuda-performance` | GPU kernel tuning, shared memory, coalescing |
| `p4-review` | Perforce code review and changelist comments |
| `p4-workflow` | Perforce changelist and shelf management |
| `research` | Technical investigation and synthesis |
| `writing` | Editing, summarization, style normalization |
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
