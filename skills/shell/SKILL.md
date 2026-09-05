---
name: shell
description: Use for shell-language semantics, startup configuration, command composition, and script reliability in Bash, POSIX sh, zsh, fish, or csh/tcsh. Running a shell command alone does not require this skill.
---

# Shell

## Scope

Own quoting, process behavior, shell configuration, and filesystem-safe scripting. The command's
domain semantics belong to Git, build, profiling, or other specialized skills.

## Method

- Identify the actual shell, version, OS/tool variants, and interactive/login mode. Bash, fish,
  and csh syntax are not interchangeable; check zsh options and POSIX constraints when relevant.
- Treat command strings as code. Prefer argument arrays in host languages; quote expansions
  and use `--` where supported. JSON encoding is not shell escaping.
- Keep data out of `eval` and command construction. Use files/stdin for multiline bodies;
  avoid leaking secrets through tracing, process arguments, or error output.
- Check failure propagation in pipelines, substitutions, conditionals, and subshells. Strict
  mode is not a substitute for deliberate error handling, and `pipefail` is not portable POSIX sh.
- Handle spaces, empty values, leading dashes, symlinks, and existing destinations. Repeated
  installs must update rather than nest copies or follow links back into source files.
- Use scoped temporary directories and cleanup ownership. Preserve unrelated files and state;
  never reuse standard environment variable names for temporary scratch values.
- Make PATH/startup edits idempotent and respect the intended shell startup file.
- Validate with the target shell's syntax checker and meaningful failure-path/repeat-run tests.

Prefer clear pipelines and existing utilities over clever escaping or unnecessary shell frameworks.
