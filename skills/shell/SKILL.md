---
name: shell
description: "Use when writing, debugging, reviewing, or refactoring shell scripts and command lines in bash, zsh, csh, tcsh, POSIX sh, and terminal automation workflows."
---

# Shell Skill

## Purpose
Support shell scripting, command-line automation, and terminal troubleshooting across bash, zsh, csh, tcsh, and POSIX sh.

## When To Use
Use for shell scripts, login and startup files, aliases, functions, environment setup, build and deploy scripts, command pipelines, and terminal debugging.

## Priorities
1. Correct shell targeting - identify whether the script is for bash, zsh, csh/tcsh, or POSIX sh before changing syntax.
2. Safety - prevent quoting bugs, glob expansion surprises, destructive file operations, and silent failures.
3. Portability - prefer portable constructs when the target shell or platform is mixed.
4. Readability - keep scripts structured, explicit, and easy to audit.
5. Observability - make failures diagnosable with clear exit handling, logging, and reproducible commands.

## Coverage
- Shell language differences: bash, zsh, csh, tcsh, POSIX sh
- Quoting, word splitting, globbing, arrays, conditionals, loops, functions, subshells
- Pipelines and text processing with grep, sed, awk, cut, sort, uniq, tr, xargs, find, tee
- Process control: jobs, signals, traps, background tasks, exit codes, timeouts
- Filesystem and permissions: chmod, chown, umask, symlinks, temp files, atomic updates
- Environment management: PATH, exports, startup files, shell rc files, tool discovery
- Debugging: set -x, set -euo pipefail where appropriate, shell tracing, reproducer minimization
- Reliability: idempotent install scripts, input validation, dependency checks, cleanup handlers
- Performance: avoid useless subshells, inefficient loops over large files, and unnecessary process spawning
- Security: safe variable handling, command injection avoidance, secret leakage prevention, and cautious use of eval

## Workflow
1. Determine the exact target shell from the shebang, invocation, or surrounding environment. Do not assume bash if the script says zsh or csh.
2. Check shell-specific semantics before editing. In particular, csh/tcsh differs materially from Bourne-style shells and often needs a different structure rather than a syntax translation.
3. Read the full script and identify risky areas: unquoted expansions, unchecked commands, unsafe temporary files, recursive deletes, and shell-specific syntax traps.
4. Prefer simple data flow: clear variable names, small functions, and pipelines that are readable without unnecessary command chaining.
5. For bash or POSIX sh, use strict-mode patterns only when they match the script's behavior and error model.
6. For zsh, account for option-dependent behavior, array semantics, globbing differences, and interactive-vs-script contexts.
7. For csh/tcsh, avoid forcing Bourne-shell idioms into the script. Use native control flow and variable syntax, and call out maintainability risks when relevant.
8. Use established command-line tools when they are the simplest correct solution: grep, sed, awk, find, xargs, tar, rsync, curl, jq, and similar utilities.
9. Validate with the target shell directly when possible, not only with a different shell.
10. Document assumptions about platform, shell version, external tools, and environment variables.

## Review Checklist
- Does the shebang match the syntax actually used?
- Are variable expansions quoted correctly for the target shell?
- Are spaces, globs, and empty variables handled safely?
- Are destructive operations guarded and explicit?
- Are temporary files created safely and cleaned up?
- Are exit codes checked where failure matters?
- Are external tool dependencies documented or probed?
- Is the script idempotent if used for setup or deployment?
- Does the script avoid bash-only syntax when portability is required?
- If the script is csh/tcsh, are the semantics correct rather than only superficially similar?

## Constraints
- Do not present bash syntax as valid for zsh or csh without checking the differences.
- Do not recommend csh for new automation unless there is a compatibility requirement.
- Do not use eval unless there is a clear need and the input is controlled.
- Do not suppress errors blindly with constructs that hide failures.
- Do not assume GNU tool behavior on every platform when BSD variants may exist.
- Do not replace a clear awk or sed solution with a more complex shell loop unless there is a strong reason.

## Output
Provide:
- shell-aware code or command changes targeted to the correct shell
- a brief note on shell-specific assumptions or portability limits
- verification steps using the target shell and relevant tools
- any material risks around safety, portability, or maintainability