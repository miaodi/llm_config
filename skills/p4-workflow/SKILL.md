---
name: p4-workflow
description: Use for Perforce workspace, changelist, shelf, stream, integrate/resolve, and submission state changes. Code-review findings belong to p4-review; description format belongs to commit-message.
---

# Perforce Workflow

## Scope

Own Perforce state inspection and authorized mutations. `p4-review` owns review findings;
`commit-message` owns description wording and STARs metadata.

## Method

1. Establish client, stream/depot, changelist, and whether the relevant content is local,
   shelved, or submitted. Infer IDs from explicit context; ask only when the target is ambiguous.
2. Inspect file actions, base revisions, open files, and outstanding resolves before changing state.
3. Preserve unrelated opened work and changelist membership. Preview operations where supported.
4. Apply only the requested operation: edit/reconcile, move/reopen, shelve, integrate/resolve,
   sync, or submit. One does not imply authorization for all the others.
5. Verify resulting file actions, membership, revisions, and remaining resolves. Report the
   resulting changelist/shelf/submission identifier and what remains local.

Pending workspace content can differ from its shelf. Do not review or overwrite one as though
it were the other. Description-only updates must preserve the form's file membership and other
fields. Do not use the default changelist as a substitute for an unspecified review target.
