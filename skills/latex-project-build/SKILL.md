---
name: latex-project-build
description: "Use when configuring, diagnosing, or compiling LaTeX projects, especially multi-file reports, theses, books, chapter-based projects, Overleaf exports, latexmk/arara/Makefile workflows, bibliography/index/glossary passes, or projects that require pdflatex, xelatex, lualatex, latex->dvips, biber, or bibtex."
---

# LaTeX Project Build Skill

## Purpose
Configure and compile LaTeX projects reliably by identifying the root file, selecting the correct engine, preserving project-specific build conventions, and using log output to fix compilation failures.

## When To Use
Use for whole-project LaTeX work: compiling PDFs, repairing build errors, setting up `latexmkrc`, diagnosing engine mismatches, cleaning auxiliary files, handling bibliography/index/glossary passes, and making multi-chapter projects build reproducibly.

## Priorities
1. Preserve the project's existing build workflow when one exists.
2. Compile the root document rather than isolated chapter files unless the chapter is intentionally standalone.
3. Select the engine from project evidence instead of guessing.
4. Prefer `latexmk` or the project's existing wrapper for repeatable multi-pass builds.
5. Fix the first real error in the log before chasing downstream noise.

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
6. Let `latexmk` manage repeated passes for references, bibliography, index, glossary, and reruns. If building manually, run the appropriate sequence for `bibtex` or `biber`, then rerun LaTeX until references stabilize.
7. Read the `.log`, `.blg`, `.ilg`, and tool output after a failure. Start at the first fatal error marker, inspect the nearby source line, and distinguish root causes from cascading undefined-control-sequence or missing-file noise.
8. After edits, recompile from a clean enough state to prove the fix. Remove stale auxiliary files only when they are likely causing the failure or after changing engines/bibliography tools.

## Common Commands
- Existing workflow: `make`, `make pdf`, `latexmk`, or the command documented in the project.
- pdfLaTeX: `latexmk -pdf main.tex`
- XeLaTeX: `latexmk -xelatex main.tex`
- LuaLaTeX: `latexmk -lualatex main.tex`
- Clean aux files managed by latexmk: `latexmk -c main.tex`
- Full cleanup when stale outputs are suspect: `latexmk -C main.tex`

Use the actual root filename instead of `main.tex`.

## Review Checklist
- Is the root document identified with evidence?
- Does the engine match project configuration and package requirements?
- Are chapter files compiled through the root unless intentionally standalone?
- Are bibliography, index, glossary, and reference reruns handled?
- Is the first real log error fixed, not just a later symptom?
- Does the final build produce the expected PDF from the expected root?
- Are generated auxiliary files kept out of source edits unless the project tracks them intentionally?

## Constraints
- Do not switch engines just to make one error disappear without checking package and font requirements.
- Do not flatten `\input` or `\include` structure unless explicitly asked.
- Do not rewrite a working Makefile, `latexmkrc`, or CI build around a new tool unless there is a concrete reproducibility problem.
- Do not delete user-authored `.tex`, `.bib`, `.sty`, `.cls`, figure, or source files as part of cleanup.
- Avoid editing generated files such as `.aux`, `.bbl`, `.blg`, `.fls`, `.fdb_latexmk`, `.log`, `.out`, `.toc`, and `.synctex.gz` unless the project explicitly tracks them.

## Output
Provide:
- root file and selected engine, with evidence
- build command used or recommended
- configuration changes, if any
- first error diagnosed and fix applied
- verification result, including whether a PDF was produced
- remaining warnings or follow-up build risks
