---
name: markdown-editing
description: "Use when editing, formatting, or refactoring markdown files—structuring headers, lists, code blocks, tables, links, and improving readability for GitHub, documentation sites, or READMEs."
---

# Markdown Editing Skill

## Purpose
Support creation, editing, formatting, and refactoring of markdown files with correct syntax, clear structure, and optimal readability.

## When To Use
Use when working with markdown files (*.md) for documentation, READMEs, GitHub wiki pages, blog posts, or any technical writing that must render cleanly with proper formatting.

## Priorities
1. Structure — organize headers, sections, and content hierarchy logically.
2. Syntax — correct markdown syntax (lists, code blocks, tables, links, emphasis).
3. Readability — short lines, white space, scannable content.
4. Consistency — uniform formatting, list styles, and heading levels throughout.
5. Rendering — preview and verify the output renders correctly across platforms (GitHub, docs sites, VSCode).

## Workflow
1. Identify the markdown dialect (GitHub Flavored Markdown, CommonMark, etc.) and target platform.
2. Read the full file and assess current structure, hierarchy, and formatting issues.
3. Fix header hierarchy: ensure h1 is used once, h2 sections align with content, no skipped levels.
4. Normalize list formatting: choose consistent bullet/number styles, indent nested lists properly.
5. Fix code blocks: add language tags for syntax highlighting, ensure triple backticks are correct.
6. Verify tables: align pipes, check column counts, ensure headers and separators are correct.
7. Check links: fix relative paths, verify anchor links, test external URLs if possible.
8. Improve spacing: add blank lines between sections, avoid dense text blocks.
9. Test rendering: preview in target platform or VSCode markdown preview.
10. Preserve content intent while improving presentation.

## Review Checklist
- Is the header hierarchy correct (only one h1, no skipped levels)?
- Are all code blocks properly tagged with language identifiers?
- Are lists consistently formatted (bullets, numbering, indentation)?
- Are tables well-aligned and properly structured?
- Are links valid, using relative paths where appropriate?
- Is there adequate white space and visual separation between sections?
- Does the file render cleanly in the target platform?
- Is the table of contents (if present) accurate and linked?
- Are inline code, bold, and italic used appropriately?
- Is the overall structure scannable and easy to navigate?

## Constraints
- Do not change the semantic content or intent of the document.
- Do not add or remove information unless explicitly requested.
- Do not use non-standard markdown extensions unless the target platform supports them.
- Do not over-format simple prose into unnecessary lists or tables.
- Preserve the author's voice and level of detail.
- Test code examples and command snippets for accuracy where possible.

## Output
Provide:
- The corrected markdown file with improved structure and formatting.
- A brief summary of changes made (structure fixes, syntax corrections, consistency improvements).
- Any recommendations for further improvement (breaking long sections, adding a TOC, etc.).
- A verification note on rendering if checked against target platform.
