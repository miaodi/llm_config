---
name: latex-tikz
description: Use to author or repair TikZ/PGFPlots figures, diagram layout, labels, axes, or reusable styles. Not for general LaTeX prose or whole-project compilation.
---

# TikZ and PGFPlots

## Scope

Own figure source and visual encoding. `latex-project-build` owns compilation;
`writing` and `report-iteration-overleaf` own report text and argument.

## Method

- Identify the figure's question, intended dimensions, and surrounding notation.
- Use TikZ for diagrams and PGFPlots for manageable data plots; use conventional plotting tools
  for dense datasets when that gives a smaller, more reproducible artifact.
- Keep styles reusable and layout explicit. Prefer clear grouping over decorative complexity.
- Preserve data provenance; label quantities and units, explain normalization, and choose axes
  and scales that do not conceal relevant effects.
- Keep labels legible at the final document size. Check clipping, overlap, color contrast,
  legends, and caption consistency.
- Compile through the project's existing workflow and inspect the rendered figure when possible.
- Deliver editable source and any referenced data/assets, not just an image with no reproduction path.
