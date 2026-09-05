---
name: git-workflow
description: Use for Git branch integration, divergence, merge/rebase conflicts, cherry-picks, and recovery. Routine staging/publishing and commit-message wording are separate concerns.
---

# Git Integration

## Scope

Own history/topology changes and recovery. Routine commits/pushes belong to the Git Publisher
role; `commit-message` owns message format and `coding` owns semantic conflict validation.

## Method

1. Inspect status, current branch, upstream, and relevant history. Preserve unrelated uncommitted
   work; a dirty worktree does not automatically require stashing or discarding it.
2. Fetch only the relevant remote when current remote state is needed. Do not fetch/prune every
   remote for local-only tasks.
3. Choose merge, rebase, or cherry-pick based on the requested result and branch policy. Published
   history rewriting needs authorization; existing authorization is sufficient.
4. Record a recovery reference before a risky integration. Resolve conflicts from both intents,
   including rename/delete and generated-file relationships, then inspect the resulting diff.
5. Continue or abort the active operation deliberately. Validate changed behavior and inspect
   the resulting history before considering publication.
6. Push only when requested or included in the authorized workflow. For an authorized rewrite,
   use a lease tied to the expected remote tip; a lease is a guard, not permission to rewrite.

Prefer revert for undoing published changes when history should be preserved. Before destructive
recovery, identify what would be lost and the recovery reference. Do not force reset, discard
unrelated work, or blindly choose one conflict side to make the operation finish.
