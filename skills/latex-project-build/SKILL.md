---
name: latex-project-build
description: Use for TeX engine/root detection, compilation, bibliography/index passes, and LaTeX build failures. Not for prose revision or figure design.
---

# LaTeX Project Build Skill

## Scope

Own compilation and build configuration. `latex-tikz` owns figures; `report-iteration-overleaf` owns revision and packaging.

## Workflow

1. Inventory the project: list top-level files, candidate `.tex` roots, `latexmkrc`, `.latexmkrc`, `Makefile`, `arara` directives, `Tectonic.toml`, `.bib`, `.bst`, `.cls`, `.sty`, image folders, and generated output directories.
2. Identify the root file by looking for `\documentclass`, `\begin{document}`, `% !TeX root`, `% !TeX program`, `\include`, `\input`, `\subfile`, and README or build script hints.
3. Detect the intended engine:
   - Prefer explicit project configuration: `latexmkrc`, magic comments, Makefile targets, CI commands, Overleaf settings, or arara rules.
   - Use `xelatex` or `lualatex` for `fontspec`, `unicode-math`, `polyglossia`, system fonts, or CJK/font shaping requirements.
   - Use `pdflatex` for traditional projects with `inputenc`, `fontenc`, and no Unicode/system-font requirements.
   - Use the configured DVI/PostScript route when the project depends on PSTricks or EPS-only workflows.
4. Compile through the existing entrypoint when present: `make`, `latexmk`, `arara`, project scripts, or documented CI commands. If no entrypoint exists, prefer `latexmk` with the detected engine.
5. For multi-file projects, keep chapter files included from the root. Only compile chapters directly when they use `subfiles`, standalone classes, or explicit per-chapter wrappers.
6. Let `latexmk` manage supported reruns; configure custom dependencies for index/glossary tools where the project needs them. If building manually, run the appropriate sequence for `bibtex` or `biber`, then rerun LaTeX until references stabilize.
7. Read the `.log`, `.blg`, `.ilg`, and tool output after a failure. Start at the first fatal error marker, inspect the nearby source line, and distinguish root causes from cascading undefined-control-sequence or missing-file noise.
8. After edits, recompile from a clean enough state to prove the fix. Remove stale auxiliary files only when they are likely causing the failure or after changing engines/bibliography tools.

## Common Commands

- Existing workflow: `make`, `make pdf`, `latexmk`, or the command documented in the project.
- pdfLaTeX: `latexmk -pdf main.tex`
- XeLaTeX: `latexmk -xelatex main.tex`
- LuaLaTeX: `latexmk -lualatex main.tex`
- Clean aux files managed by latexmk: `latexmk -c main.tex`
- `latexmk -C main.tex` also removes final outputs; use only when that cleanup is intended.

Use the actual root filename instead of `main.tex`.

## Constraints

- Do not switch engines just to make one error disappear without checking package and font requirements.
- Do not flatten `\input` or `\include` structure unless explicitly asked.
- Do not rewrite a working Makefile, `latexmkrc`, or CI build around a new tool unless there is a concrete reproducibility problem.
- Do not delete user-authored `.tex`, `.bib`, `.sty`, `.cls`, figure, or source files as part of cleanup.
- Avoid editing generated files such as `.aux`, `.bbl`, `.blg`, `.fls`, `.fdb_latexmk`, `.log`, `.out`, `.toc`, and `.synctex.gz` unless the project explicitly tracks them.
