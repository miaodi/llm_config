---
name: git-workflow
description: "Use when planning or executing Git branch workflows, especially merge/rebase across branches, conflict resolution, safe history rewriting, and recovery from mistakes."
---

# Git Workflow Skill

## Purpose
Help users integrate branches safely and confidently, with practical, beginner-friendly guidance for merge, rebase, conflict resolution, and recovery.

## When To Use
Use for branch sync, pull request preparation, merge vs rebase decisions, conflict handling, rebasing feature branches, preserving a shared branch history, undoing bad integrations, and explaining Git commands before running them.

## Priorities
1. Safety first - avoid data loss and risky history rewrites.
2. Clarity - explain why each command is used.
3. Correctness - preserve intended code changes during integration.
4. Recoverability - always keep a path to undo.
5. Team compatibility - prefer workflows that match shared branch policies.

## Coverage
- Branch graph understanding and branch hygiene
- Merge workflows (fast-forward, no-fast-forward, and merge commits)
- Rebase workflows (interactive and non-interactive)
- Conflict resolution for merge and rebase
- Commit cleanup before PR (squash, reorder, edit messages)
- Commit message drafting using the shared `commit-message` skill/template
- Cherry-pick for selective change transfer
- Syncing from remote and handling divergence
- Recovery with reflog, reset, revert, and abort commands
- Force-push safety (`--force-with-lease`, never blind `--force`)

## Merge Vs Rebase
- Choose merge when preserving true branch history matters, the branch is shared, or policy prefers merge commits.
- Choose rebase when you want a linear history and the branch is private or not yet widely shared.
- Never rebase published/shared branches without explicit agreement.

## Workflow
1. Preflight safety checks.
   - `git status` to ensure a clean state.
   - `git fetch --all --prune` to refresh remote state.
   - `git branch --show-current` and `git log --oneline --graph --decorate --all -n 30` to confirm branch topology.
2. Pick integration strategy intentionally.
   - Merge path: `git checkout <target>` then `git merge <source>`.
   - Rebase path: `git checkout <feature>` then `git rebase <base>`.
3. Resolve conflicts carefully.
   - Inspect files with conflict markers.
   - Keep intended logic, then `git add <resolved-files>`.
   - Continue with `git merge --continue` or `git rebase --continue`.
   - If needed, stop safely with `git merge --abort` or `git rebase --abort`.
4. Validate result.
   - Re-run tests/build relevant to touched code.
   - Review history with `git log --oneline --graph -n 30`.
5. Publish safely.
   - For rebased branches, use `git push --force-with-lease`.
   - For merged branches, use normal `git push`.
6. Recover if something went wrong.
   - Use `git reflog` to locate prior HEAD.
   - Use `git reset --hard <reflog-entry>` only with explicit confirmation.
   - Prefer `git revert` for undoing changes on shared branches.

## Conflict Resolution Playbook
1. Identify conflict scope: file-level and commit-level intent.
2. Prefer semantic resolution (correct behavior) over mechanical marker deletion.
3. Resolve one file at a time and stage incrementally.
4. Re-run focused validation after each major conflict cluster.
5. If conflict density is high, abort and retry with smaller steps.

## Review Checklist
- Is the chosen strategy (merge/rebase) appropriate for this branch and team policy?
- Is the branch clean and synced before integration?
- Were all conflicts resolved intentionally (not accidentally dropped)?
- Is commit history understandable for reviewers?
- Was force push done only with `--force-with-lease` and only when appropriate?
- Is there a clear rollback path documented if needed?

## Commit Messages
When drafting, editing, or reviewing a Git commit message, read `../commit-message/SKILL.md` and follow the shared Git/P4 commit message template referenced there.

## Constraints
- Do not recommend rewriting shared branch history without explicit approval.
- Do not use blind `git push --force`.
- Do not continue a conflicted merge/rebase without reviewing every conflict chunk.
- Do not suggest destructive commands (`reset --hard`, branch deletion) without warning and recovery guidance.
- Do not hide uncertainty; call out assumptions about branch ownership and remote policy.

## Output
Provide:
- a concrete command sequence tailored to the current branch situation
- a merge vs rebase rationale in plain language
- conflict-resolution guidance for the exact files or conflict types involved
- a rollback/recovery plan before risky steps
- post-integration validation steps
