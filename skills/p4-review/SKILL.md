---
name: p4-review
description: Use to review Perforce changelists or shelves for defects, regressions, and missing validation. Does not manage changelist membership, submit work, or require STARs metadata to begin a code review.
---

# Perforce Review

## Scope

Own review findings and evidence. `p4-workflow` owns state changes; `commit-message` owns
requested description drafts and metadata. A missing STARs ID does not block reviewing code.

## Method

1. Establish the intended changelist and whether to inspect workspace, shelf, or submitted content.
   Use clear prior context; ask when more than one plausible review target remains.
2. Inspect the complete file/action list and correct base revisions, including moves, integrates,
   dependencies on other changes, and unresolved files.
3. Read changed behavior and enough surrounding code/callers to evaluate it. Prioritize concrete
   correctness bugs, regressions, and meaningful validation gaps.
4. Attach a trigger, impact, and file/line reference to each finding. Separate evidence from
   speculation; do not manufacture findings to fill a severity checklist.
5. Report limitations in review coverage and tests. No findings is not a submission approval.

Review requests are read-only. Drafting a description does not authorize updating Perforce;
if an update is requested, keep it metadata-only and preserve membership. Do not submit, shelve,
reopen, or move files as an incidental part of reviewing them.
