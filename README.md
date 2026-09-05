# llm-config

Central repository for LLM and agent configuration, reusable skills, prompts, and operating conventions.

## Installation

Requires Bash, Python 3.11 or newer, and PyYAML in the Python environment used by
`python3`. Install PyYAML with your system package manager or in a virtual environment.
For example, Debian/Ubuntu provides `python3-yaml`.

Choose one target per invocation:

```bash
./setup.sh --copilot
./setup.sh --codex
./setup.sh --opencode

./setup.sh --copilot-project /path/to/repo
./setup.sh --codex-project /path/to/repo
./setup.sh --opencode-project /path/to/repo

./setup.sh --codex --copy
```

`--project PATH` remains an alias for `--copilot-project PATH`. Project directories
must already exist. Bare `./setup.sh` prints an error instead of selecting a target.

| Product | Personal skills | Personal agents | Project skills | Project agents |
| --- | --- | --- | --- | --- |
| Copilot | `~/.agents/skills/` | `~/.copilot/agents/*.agent.md` | `.agents/skills/` | `.github/agents/*.agent.md` |
| Codex | `~/.agents/skills/` | `~/.codex/agents/*.toml` | `.agents/skills/` | `.codex/agents/*.toml` |
| OpenCode | `~/.agents/skills/` | `~/.config/opencode/agents/*.md` | `.agents/skills/` | `.opencode/agents/*.md` |

Each skill lives in `<name>/SKILL.md` with YAML `name` and `description` fields.
No extra skill registration is required. All three targets use the shared `.agents/skills`
location so installing several clients does not create duplicate skill entries. Matching
legacy product-specific skills are backed up outside discovery; modified copies are
retained with a warning for manual reconciliation.

### Copies, links, and updates

Skills and supporting resources are symlinked by default. Keep this checkout at a
stable path. `--copy` creates independent copies for machines where the source
checkout will not remain available. Agents are always generated as regular files:
their native metadata and resource paths depend on the destination product.

Re-run the same target command after changing agents or `memory/`, after adding
skills, or to update a copied install. Existing matching files are left alone.
Changed destinations and copy/link mode transitions are backed up under
`<product-config>/.llm-config-backups/`, outside skill and agent discovery paths.
Each backup records its original path. A repeated copy replaces the skill directory
instead of nesting another copy inside it. Unrelated skills and agents are preserved.

Restart the client after installation. Generated agents and managed instructions
contain installation-specific paths; rerun setup after relocating a copied install.
The installer does not edit model, provider, authentication, or project trust settings.

### Product configuration

- **Codex:** `CODEX_HOME` overrides the personal agent/config directory, but personal
  skills still go to `$HOME/.agents/skills`. Agents use native TOML with `name`,
  `description`, and `developer_instructions`. Agents without source `edit` access
  use a read-only sandbox. Copilot tool names do not map exactly to Codex tool
  permissions; other agents inherit the active Codex sandbox and approval policy.
  `child_agents_md` is not a registration mechanism. Matching legacy `.codex/skills`
  installs and `.agent.md` files are backed up and removed from discovery. Modified
  legacy skills are retained with a warning so local edits are not lost.
- **Copilot:** `COPILOT_HOME` overrides the personal CLI directory. VS Code uses
  the default `~/.copilot` directories unless separately configured. Source tool
  lists are retained; omitting `target` permits both supported target environments.
- **OpenCode:** `OPENCODE_CONFIG_DIR` overrides the personal installation directory;
  otherwise setup uses `${XDG_CONFIG_HOME:-$HOME/.config}/opencode`. Use the same
  variable when launching OpenCode. `OPENCODE_HOME` is not used. Generated agents
  use `mode: subagent` and permissions derived from their source tool lists. Unlisted
  tools are denied; read/search and skill loading are allowed when applicable;
  edit, terminal, and web capabilities require approval when included. User-level
  OpenCode permission rules are therefore supplemented by these explicit agent rules.

### Shared instructions and resources

The installer deploys `templates/`, `docs/`, source agent examples, and `memory/`
under `<product-config>/llm-config/`. Generated agents point to the installed skills
and resources. The commit-message skill uses the bundled template there.

A managed `llm-config:begin` / `llm-config:end` block embeds `memory/` and resource
lookup guidance in the following instruction files:

| Product | Personal instructions | Project instructions |
| --- | --- | --- |
| Codex | `$CODEX_HOME/AGENTS.md` (default `~/.codex/AGENTS.md`) | `AGENTS.md` |
| Copilot CLI | `~/.copilot/copilot-instructions.md` (or `$COPILOT_HOME`) | `.github/copilot-instructions.md` |
| OpenCode | `${XDG_CONFIG_HOME:-$HOME/.config}/opencode/AGENTS.md` | `AGENTS.md` |

Existing text outside the managed block is preserved. Edit shared preferences in
`memory/` and rerun setup; edits inside the managed block are regenerated. Global
Copilot instruction discovery described here is for Copilot CLI; use the project
install for repository instructions in VS Code. Generated agents also embed shared
memory so their behavior does not depend on personal instruction discovery.

### Verification

```bash
python3 -m unittest discover -s tests -v
```

In a new Codex session, use `/skills` to inspect skill discovery. Ask Codex to use
one of the installed skills explicitly, for example `$coding`. Custom agents are
separate from skills and require a client version supporting native TOML agents.
For OpenCode, use `opencode debug skill` and `opencode debug agent p4-reviewer`.

References: [Codex skills](https://learn.chatgpt.com/docs/build-skills),
[Codex agents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[Copilot skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills),
[Copilot agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration),
[OpenCode skills](https://opencode.ai/docs/skills/), and
[OpenCode agents](https://opencode.ai/docs/agents/).

## Structure

- `agents/` — agent definitions (`*.agent.md` with YAML frontmatter)
- `skills/` — reusable task skills (`SKILL.md` with YAML frontmatter, one per directory)
- `templates/` — starter templates for new configs
- `memory/` — long-lived preferences and conventions
- `docs/` — documentation for contributors

See [skill and agent ownership](docs/skill-map.md) for routing boundaries and the
[content review](docs/content-review.md) for the cleanup rationale.

## Agents

| Agent | Description |
|-------|-------------|
| `agents-md-writer` | Repository-specific AGENTS.md guidance |
| `sparse-parallel-engineer` | Sparse algorithms and parallel scheduling |
| `agent-creator` | Custom agent and skill design for this repository |
| `computational-learning-coach` | Low-level computational and numerical concepts taught through minimal C++ examples and learning notes |
| `cpp-engineer` | Modern C++ design, type safety, ownership, compile-time computation |
| `document-writer` | Markdown, Confluence, LaTeX, and report editing |
| `p4-reviewer` | Read-only Perforce changelist and shelf defect review |
| `p4-engineer` | Perforce sync, integration/resolve, changelist/shelf operations, and description generation/updates |
| `performance-engineer` | Runtime performance, profiling, bottleneck analysis, C++/CUDA tuning |
| `course-project-worker` | Course projects end-to-end: spec extraction, Python ML, RL, LaTeX reports |
| `build-engineer` | Boost.Build (b2/bjam), gcc/clang/nvcc error diagnosis, template errors, compilation speed |
| `cmake-project-builder` | Modern CMake projects, CMakePresets, C++/CUDA build errors, custom CMake functions |
| `git-integrator` | Git branch integration: merge/rebase strategy, conflict resolution, branch sync, and safe recovery |
| `git-publisher` | Git commit and push workflow: status, diff review, staging, commit messages, and publishing |

## Skills (27)

| Skill | Domain |
|-------|--------|
| `agent-customization` | Custom agent and skill scope, tools, and delegation wording |
| `commit-message` | Shared Git/P4 commit message format |
| `graph-algorithms` | Graph traversal, coloring, and dependency scheduling |
| `coding` | General implementation, debugging, refactoring |
| `git-workflow` | Git branch workflows, merge/rebase decisions, conflict resolution, history cleanup, and recovery |
| `shell` | Bash, POSIX sh, zsh, fish, csh/tcsh scripting, terminal automation, pipelines, portability, and shell debugging |
| `boost-build` | B2/Jam requirements, toolsets, and build graph behavior |
| `modern-cmake` | Modern CMake, target usage requirements, presets, toolchains, C++/CUDA/nvcc build diagnosis |
| `cpp-elegance` | Modern C++ clarity, RAII, concepts, and SOLID-informed API design |
| `cpp-performance` | C++ hot-path optimization, cache, vectorization |
| `computational-learning-notes` | Low-level computational, numerical, hardware, and compiler concepts taught through minimal C++ demos |
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
| `latex-project-build` | LaTeX project configuration, engine selection, multi-file compilation, and build diagnostics |
| `latex-tikz` | TikZ/PGFPlots figure source and layout |
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
4. Re-run `./setup.sh` with your chosen target to pick up new files.
