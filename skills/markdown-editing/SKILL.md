---
name: markdown-editing
description: Use for Markdown rendering, headings, lists, tables, fences, anchors, and links. A prose edit in a Markdown file alone does not require this skill.
---

# Markdown Editing

## Scope

Own markup and renderer compatibility. `writing` owns prose and argument; domain skills own
technical content. Preserve meaning unless the user also requests content changes.

## Method

- Identify the renderer and existing conventions: CommonMark, GitHub, or a documentation framework.
- Preserve frontmatter, generated sections, embedded directives, and significant whitespace.
- Keep heading levels logical; avoid duplicating a title already supplied by the page framework.
- Separate paragraphs and lists with blank lines. Indent nested lists and code consistently.
- Use language-tagged fences where the language is known; use a longer outer fence when nesting examples.
- Check table column counts, escaped pipes, inline code, relative links, anchors, and image paths.
- Resolve relative links from the containing file. Check referenced local files actually exist.
- Do not introduce renderer extensions without confirming support or rewrite unaffected formatting.
- Use existing lint/preview tools when rendering risk warrants it. Distinguish a source inspection
  from a rendered preview in the result.
