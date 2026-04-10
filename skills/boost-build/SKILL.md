---
name: boost-build
description: "Use when working with Boost.Build (b2/bjam), Jamfiles, Jamroot, toolset configuration, submodule dependencies, feature propagation, or diagnosing gcc/clang/nvcc compilation errors and C++ template error messages."
---

# Boost.Build Skill

## Purpose
Navigate Boost.Build (b2/bjam) configuration, diagnose build failures, and interpret gcc/clang/nvcc error messages — especially deep template instantiation errors.

## When To Use
Use when working with Jamfiles, Jamroot, project-config.jam, user-config.jam, toolset configuration, library dependencies, feature propagation, or when build errors from gcc, clang, or nvcc need interpretation.

## Priorities
1. Understand the build system structure before changing rules.
2. Trace the actual error cause before fixing symptoms.
3. Translate compiler diagnostics into actionable root causes.
4. Keep Jamfile changes minimal and consistent with existing conventions.

## Boost.Build Concepts
- **Jamroot / Jamfile**: project definition files; Jamroot marks the project root.
- **project rule**: declares project name, requirements, default-build, and usage-requirements.
- **lib / exe / alias**: target rules for libraries, executables, and grouping.
- **requirements**: conditions applied when building a target (`<include>`, `<define>`, `<link>`, `<threading>`, etc.).
- **usage-requirements**: conditions propagated to dependents.
- **conditional requirements**: `<toolset>gcc:<cxxflags>-Wextra` — applied only when condition matches.
- **feature propagation**: how requirements flow from dependencies to dependents through usage-requirements.
- **toolset**: compiler configuration (`gcc`, `clang`, `nvcc`, `msvc`) defined in user-config.jam or project-config.jam.
- **variant**: `debug`, `release`, `profile` — predefined build configurations.
- **subproject**: a Jamfile in a subdirectory that inherits from the parent project.

## Workflow
1. Identify the failing target and the full compiler command (use `b2 -d+2` or `-n` for dry run).
2. Read the Jamfile chain from the failing target up to Jamroot to understand requirements, usage-requirements, and feature propagation.
3. Check toolset configuration in user-config.jam / project-config.jam.
4. For compilation errors:
   - Identify whether the error is a missing include path, missing define, ABI mismatch, or language-standard issue.
   - For template errors: find the innermost "required from here" or "in instantiation of" line — that is usually the real cause.
   - For nvcc errors: check host-compiler compatibility, `__host__`/`__device__` annotation issues, and unsupported C++ features in device code.
5. For link errors: check library ordering, missing `<library>` dependencies, and symbol visibility.
6. Propose the minimal Jamfile or config change and verify with a rebuild.

## Reading Template Error Messages
- **gcc/clang**: Scroll past the wall of "required from" / "in instantiation of" lines. The actual error is usually at the top or the bottom. The innermost instantiation context is the most actionable.
- **Nested template errors**: Map each "required from" frame to a source location. The deepest frame that is in your code (not library internals) is usually where the fix belongs.
- **Concept/constraint failures (C++20)**: Look for "constraints not satisfied" and read which specific constraint failed.
- **nvcc**: nvcc wraps host compiler errors; look for the host compiler error nested inside nvcc output. Watch for `__host__ __device__` annotation mismatches and unsupported language features in device code.
- **Substitution failures (SFINAE)**: "in substitution of" lines show which overload was rejected and why. The candidate list shows what the compiler tried.

## Common Boost.Build Issues
- **Missing include path**: Add `<include>path` to requirements or usage-requirements.
- **Wrong C++ standard**: Add `<cxxstd>17` or `<cxxflags>-std=c++20` to requirements.
- **Feature not propagating**: Move requirement to `usage-requirements` so dependents inherit it.
- **Toolset not found**: Check `using gcc : version : /path/to/g++ ;` in user-config.jam.
- **nvcc + host compiler mismatch**: Ensure nvcc's `-ccbin` points to a compatible host compiler version.
- **Conditional not matching**: Verify exact feature spelling (`<toolset>gcc` not `<toolset>g++`).
- **Link order issues**: Boost.Build handles ordering, but external libraries via `<linkflags>` bypass this — use `<library>` when possible.

## Review Checklist
- Is the Jamfile target correctly declaring its dependencies?
- Are usage-requirements set so dependents get needed includes/defines?
- Is the toolset configured with the right compiler path and flags?
- Is the C++ standard consistent across all targets in the dependency chain?
- For template errors: is the root cause in your code or a misconfigured type/trait?
- For nvcc errors: is the code compatible with device compilation constraints?
- Is `b2 -d+2` output consistent with what the Jamfile intends?

## Constraints
- Do not guess Jamfile syntax — verify against Boost.Build documentation patterns.
- Do not add global flags when a per-target requirement is sufficient.
- Do not mask template errors with casts or suppression — find the type mismatch.
- Do not assume nvcc supports the same C++ features as the host compiler.
- State clearly when the error is in library code vs. user code.

## Speeding Up Compilation

### Parallelism
- Use `b2 -j$(nproc)` (or `-jN`) to run N compile jobs in parallel.
- Set `BJAM_JOBS` or alias `b2` to always pass `-j` so it's never forgotten.

### Precompiled Headers (PCH)
- Identify the most-included heavy headers (Boost headers, STL containers, Eigen, etc.).
- Create a single PCH target and add it as a dependency; Boost.Build supports `<pch-header>` and `<pch-source>` properties.
- Keep the PCH stable — any change to it triggers a full rebuild.

### Forward Declarations & Include Pruning
- Replace `#include` with forward declarations in headers whenever the full definition isn't needed.
- Use include-what-you-use (`iwyu`) or manual inspection to remove unused includes.
- Move heavy includes from headers to `.cpp` files when possible.

### Reducing Template Instantiation Cost
- Extern template (`extern template class X<T>;`) in headers, explicit instantiation in one `.cpp`.
- Move non-dependent helpers out of templates into non-template base classes or free functions.
- Consider type-erasure or PIMPL when a template is only used with a few types.

### Compiler Flags for Speed
- Use `-pipe` (gcc/clang) to avoid temporary files.
- In debug builds, use `-O0 -g1` instead of `-O0 -g` to reduce debug-info overhead.
- Consider `-gsplit-dwarf` (gcc/clang) to defer debug-info linking.
- Consider `-fno-exceptions` or `-fno-rtti` if the code doesn't use them.

### Build Caching
- Use `ccache` or `sccache` as the compiler wrapper (`using gcc : : ccache g++ ;` in user-config.jam).
- Ensure the cache directory has enough space and is on fast storage.

### Incremental Build Hygiene
- Keep generated files out of tracked directories so they don't trigger spurious rebuilds.
- Avoid modifying widely-included headers; split stable interfaces from volatile implementation.

## Output
Provide:
- the root cause of the build failure (or the bottleneck if the goal is speed)
- the relevant Jamfile / config context
- the specific compiler diagnostic decoded into plain language
- the minimal fix (Jamfile change, code change, or config change)
- verification command to confirm the fix
- when applicable, concrete suggestions to reduce wall-clock compile time
