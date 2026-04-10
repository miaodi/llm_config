# LaTeX TikZ Skill

## Purpose
Produce clear LaTeX and TikZ figures for technical reports, project writeups, and polished explanatory diagrams.

## When To Use
Use for course reports, algorithm diagrams, experimental schematics, architecture figures, and report-ready plots that should be authored directly in LaTeX/TikZ.

## Priorities
1. Make the figure communicate one clear idea.
2. Keep TikZ structure readable and maintainable.
3. Match the visual emphasis to the argument in the report.
4. Prefer consistency in naming, spacing, and styling.

## Workflow
1. Decide whether the figure is conceptual, schematic, or data-driven.
2. For conceptual figures, use TikZ directly with reusable styles and explicit layout.
3. For data-driven plots, prefer a clean pathway from experiment outputs to LaTeX-friendly plotting, and use TikZ/PGFPlots when practical.
4. Keep labels concise and mathematically precise.
5. Make the figure integrate cleanly into the surrounding report text.

## Review Checklist
- Does the figure answer a specific question?
- Is TikZ the right tool for this plot or diagram?
- Are labels concise and readable?
- Are axes, legends, and captions aligned with the experiment narrative?
- Is the figure simple enough to maintain?

## Constraints
- Do not create ornate TikZ that is hard to edit for little benefit.
- Do not use TikZ for dense data plots if it makes iteration impractical without a clear report-quality benefit.
- Prefer reusable styles over repeated formatting noise.

## Output
Provide:
- figure recommendation
- TikZ or PGFPlots structure
- caption guidance
- integration notes for the LaTeX report
