---
name: confluence-editing
description: "Use when editing, formatting, or refactoring Confluence pages—structure, macros, tables, code snippets, permissions, and optimizing for collaboration and searchability."
---

# Confluence Editing Skill

## Purpose
Support creation, editing, formatting, and optimization of Confluence pages with correct markup, clear navigation, proper macros, and team-friendly structure.

## When To Use
Use when creating or editing Confluence pages for team documentation, wikis, runbooks, design specs, or internal knowledge bases. Use for page structure, macro selection, permissions, labels, and cross-linking within Confluence.

## Priorities
1. Structure — clear hierarchy, navigation, and logical flow; parent/child relationships.
2. Macros — choose appropriate Confluence macros (TOC, code block, table, status, accordion, etc.).
3. Formatting — consistent use of headings, bold, lists, tables, and whitespace.
4. Discoverability — labels, searchable titles, linked references, and navigation breadcrumbs.
5. Collaboration — clear ownership, update instructions, and version history awareness.

## Workflow
1. Identify the page purpose, audience, and team context (which space, parent page, stakeholders).
2. Read or audit the current page structure and macro usage.
3. Fix heading hierarchy: ensure h1 is the page title, h2 for main sections, no skipped levels.
4. Choose and insert appropriate macros: 
   - `{toc}` for table of contents on long pages.
   - `{code}` blocks for code snippets with language and line numbers.
   - `{table-of-contents}` for hierarchical navigation trees.
   - `{expand}` or `{accordion}` for detailed sections that readers can collapse.
   - `{status}` for workflow indicators (Draft, Review, Published, etc.).
5. Refactor lists and tables for clarity: proper indentation, alignment, consistent formatting.
6. Add labels for filtering and discovery.
7. Check cross-links: verify parent/child page references, link to related pages.
8. Ensure permissions are correct: document who can view, edit, and comment.
9. Add "Last Updated" or maintenance instructions if the page requires regular updates.
10. Preview the rendered page and verify all macros display correctly.

## Review Checklist
- Is the page hierarchy correct (parent/child relationships)?
- Are all headings properly leveled without skips?
- Are appropriate Confluence macros used (TOC, code, status, etc.)?
- Are code snippets tagged with language and properly formatted?
- Are tables well-structured, sortable, and readable?
- Is the page labeled with relevant keywords for search and filtering?
- Are cross-links to related pages included and correct?
- Do the page permissions match the intended audience?
- Is there a clear indication of ownership or last update date?
- Does the page render correctly with all macros visible?

## Constraints
- Do not remove or drastically rewrite content without discussing with page owner.
- Do not use macros that are not available in the target Confluence version.
- Do not ignore team conventions for page naming, labeling, or structure.
- Do not over-macro simple pages; keep formatting clean and readable.
- Preserve page history and version tracking awareness.
- Respect existing permissions and access controls.

## Output
Provide:
- The updated Confluence page markup or a summary of structural changes.
- A list of macros applied and their purpose.
- Any labels or metadata added for searchability.
- Navigation or cross-link recommendations.
- A note on permissions and audience targeting.
- Before/after rendering preview if possible.
