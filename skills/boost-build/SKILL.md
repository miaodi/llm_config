---
name: boost-build
description: Use for Boost.Build/B2 Jamfiles, requirements propagation, toolsets, and build graph problems. Compiler messages alone do not select this skill; confirm a B2 build first.
---

# Boost.Build / B2

## Scope

Own Jamroot/Jamfile configuration and B2 behavior. Use `cpp-elegance` for source type/design
issues and `coding` for implementation defects. CMake projects use `modern-cmake`.

## Method

1. Identify the target, active toolset/configuration, B2 version, and invocation.
2. Recover the generated command with a dry run (`b2 -n`) or command logging (`b2 -d+2`).
3. Trace project/target requirements, conditional requirements, dependencies, and usage-requirements.
   Expose a requirement to consumers only when their compilation or linking actually needs it.
4. Distinguish configuration errors from source diagnostics and linker failures. Trace template
   diagnostics back to the relevant user call/constraint rather than assuming the deepest frame is wrong.
5. Use supported B2 features such as `<cxxstd>` instead of injecting conflicting compiler flags.
   Verify feature names and compiler-wrapper/PCH syntax against the installed B2 version.
6. Rebuild the affected target/configuration and check that dependents receive the intended requirements.

## Build-time work

Only optimize compile time when requested or necessary to resolve the task. Measure clean and
incremental builds separately. Bound job parallelism by memory as well as CPU availability.
Investigate invalidated dependencies, heavy includes, repeated template work, and cache misses.
Do not disable exceptions/RTTI, weaken debug information, or add global aliases merely to make
compilation faster; these are project semantics and workflow choices.

Reference: [B2 manual](https://www.bfgroup.xyz/b2/manual/release/index.html).
