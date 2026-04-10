# llm-config

Central repository for LLM and agent configuration, reusable skills, prompts, and operating conventions — in VS Code Copilot's native format.

## Installation

Run the setup script to install agents and skills either into your VS Code user-level directories or into a project's `.github` directory.

```bash
./setup.sh                          # symlink user-level install (default)
./setup.sh --copy                   # copy user-level install
./setup.sh --project /path/to/repo  # symlink project install into .github/
./setup.sh --project /path/to/repo --copy
```

User install targets:
- **Agents** → `~/.config/Code/User/prompts/*.agent.md`
- **Skills** → `~/.copilot/skills/<name>/SKILL.md`

Project install targets:
- **Agents** → `<project>/.github/agents/*.agent.md`
- **Skills** → `<project>/.github/skills/<name>/SKILL.md`
- **Instructions** → `<project>/.github/copilot-instructions.md` (generated as a normal file, not a symlink)

Restart VS Code or reload the window after running.

### Per-project usage

To install into a single project with the script:

```bash
./setup.sh --project /path/to/your-project
```

The installer creates `.github/copilot-instructions.md` if it does not already exist, and preserves an existing file so you can keep project-specific guidance there.

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

## Skills (15)

| Skill | Domain |
|-------|--------|
| `coding` | General implementation, debugging, refactoring |
| `shell` | Bash, zsh, csh/tcsh scripting, terminal automation, pipelines, portability, and shell debugging |
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
