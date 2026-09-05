---
name: confluence-editing
description: Use for Confluence page representation, macros, version-aware updates, hierarchy, and links. Use writing for prose; this skill does not authorize publishing or permission changes.
---

# Confluence Editing

## Scope

Own Confluence-specific document operations. Prose quality belongs to `writing`.

## Method

1. Read the target page, version, and relevant parent/space context through the available integration.
2. Determine the representation the integration accepts (for example storage format or editor
   document format). Do not assume legacy `{macro}` wiki syntax is accepted by a modern editor/API.
3. Preserve existing page structure, attachments, links, macros, and user content outside the edit.
4. Use only macros supported by the target instance. Do not invent macro names or IDs.
5. Apply the requested content changes with the current version; on a version conflict, reread
   and reconcile rather than overwriting concurrent edits.
6. Inspect the updated page or rendering to verify tables, code blocks, and links survived.

Change labels, hierarchy, restrictions, or ownership only when the request includes them.
An authorized page edit does not require an additional page-owner confirmation. If write access
is unavailable, provide a concrete draft and identify what remains unapplied.
