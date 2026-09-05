---
name: report-iteration-overleaf
description: Use to revise a report against prior feedback or new results, or package/sync existing Overleaf sources. Not for standalone prose edits, TikZ drawing, or TeX build failures.
---

# Report Iteration and Overleaf

## Scope

Own continuity between report versions and submission packaging. Use `writing` for prose,
`latex-tikz` for figures, and `latex-project-build` for compilation only as needed.

## Method

1. Read the current requirements, previous report, feedback, and available new results.
2. Map each requested revision to evidence and a section, table, figure, or appendix.
3. Reuse sound structure and notation; reassess claims, conclusions, dates, and numbers against
   current experiments. Do not carry forward unsupported conclusions.
4. Make the requested revision depth explicit in the artifact. A formatting-only request does
   not require new experiments or an unsolicited rewrite of the argument.
5. Validate cross-references and result provenance, then compile when sources/tools are available.
6. Package the root document, bibliography, required styles, figures, and data assets. Exclude
   generated clutter unless submission rules require it.
7. Use only the Overleaf workflow actually available: local sources, ZIP, or a configured remote.
   `git-workflow` handles integration conflicts. Publishing requires authorization in the task.

Report whether the result was edited locally, packaged, or synced; these are different outcomes.
