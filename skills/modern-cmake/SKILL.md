---
name: modern-cmake
description: Use for CMake targets, presets, toolchains, dependencies, generated files, and install/export configuration. Compiler errors select this skill only when CMake configuration is implicated.
---

# Modern CMake

## Scope

Own the CMake build graph and its generated commands. Source-level C++ contracts belong to
`cpp-elegance`; GPU runtime behavior belongs to `cuda-performance`.

## Diagnose

1. Identify preset, generator, build directory, configuration, compiler/toolchain, and failing target.
2. Read the relevant target and module chain. Get the actual failing command with
   `cmake --build <build-dir> --target <target> --verbose` (and `--config` when applicable).
3. Trace source ownership, includes, definitions, compile features, link dependencies, generated
   outputs, and transitive usage requirements. Fix source defects in source when commands are correct.
4. Reconfigure when configuration changed; use a separate build directory to investigate stale
   state or a changed compiler rather than deleting useful build artifacts by default.

## Design

- Prefer target properties and imported package targets over global flags and raw library paths.
- `PRIVATE` applies to the target, `INTERFACE` to consumers, and `PUBLIC` to both. Interface
  requirements also apply to ordinary libraries whose consumers need them.
- Follow the existing dependency policy and supported CMake version. Do not add fetching,
  vendoring, or a version bump solely for style.
- Keep helper functions explicit about target inputs and side effects; prefer functions to
  macros when caller-scope mutation is unnecessary.
- Model generated outputs and dependencies accurately so incremental and parallel builds work.
- For packaging, validate an installed consumer, relocatable paths, exported dependencies,
  and build/install interfaces, not only an in-tree build.
- For broad cleanup, map all owned targets, modules, presets, custom commands, and exports
  before removing supposedly unused code. Preserve documented target names and options.

## CUDA

Enable CUDA language for device code/launch syntax needing CUDA compilation. Host-only runtime
or toolkit-library callers can remain C++ and use imported `CUDAToolkit` targets. Respect the
existing `.cpp`/`.cu` boundary. Configure architectures, language standards, host compiler,
and device linking on the targets that need them. Verify toolkit/host compatibility against
the installed versions rather than adding permissive flags to bypass it.

Verify the changed target, affected configurations, and installation path when relevant.
