---
name: modern-cmake
description: "Use when creating, refactoring, cleaning up, structurally analyzing, or diagnosing CMake projects, CMakePresets, target-based modern CMake, custom functions/macros, dependency discovery, C++ compiler errors, CUDA language support, nvcc errors, toolchains, install/export rules, or cross-platform build configuration."
---

# Modern CMake Skill

## Purpose
Build, repair, parse, and clean up CMake-based C++ and CUDA projects using target-based modern CMake, precise compiler diagnostics, and project-consistent structure.

## When To Use
Use for `CMakeLists.txt`, `*.cmake`, `CMakePresets.json`, toolchain files, package config files, install/export rules, dependency integration, C++ compilation errors, CUDA/nvcc compilation errors, custom CMake functions or macros, or whole-project CMake cleanup/rework.

## Priorities
1. Diagnose from the generated build command and CMake target graph, not from guesses.
2. Prefer target properties and usage requirements over global flags.
3. Keep CMake code portable across Ninja, Makefiles, MSVC, gcc, clang, and nvcc where the project requires it.
4. Make dependency and option behavior explicit, reproducible, and easy to inspect.
5. When asked to clean up or rework a project, parse the full project structure before editing and produce clean, cohesive CMake rather than local cosmetic changes.
6. Preserve the project's existing layout and conventions unless they are the cause of the failure or the user asked for structural cleanup.

## Workflow
1. Identify the active configure/build command, generator, preset, build directory, compiler, CMake version, and failing target.
2. For configuration errors, read the root `CMakeLists.txt`, relevant subdirectory `CMakeLists.txt` files, included `*.cmake` modules, presets, and toolchain file.
3. For build errors, get the full compile or link command:
   - Ninja: `ninja -C build -v <target>`
   - CMake wrapper: `cmake --build build --target <target> --verbose`
   - Makefiles: `make VERBOSE=1 <target>`
4. Trace the failing target's sources, include directories, compile definitions, compile features, link libraries, and transitive usage requirements.
5. Decide whether the root cause is CMake configuration, dependency discovery, compiler flags, source compatibility, ABI mismatch, host/device compilation, or link semantics.
6. Apply the smallest targeted fix and verify with a clean configure only when cache state may be part of the problem; otherwise prefer an incremental rebuild of the failing target.

## Whole-Project Structure Parsing
When the request is to understand, clean up, modernize, or rework CMake, first build a project map:
- Find every `CMakeLists.txt`, `*.cmake`, preset file, toolchain file, package config template, generated-code rule, vendored dependency entry point, and CI configure/build command.
- Identify each target, alias target, imported target, object library, interface library, executable, test target, install/export target, and custom command/target.
- Trace target relationships: source ownership, include propagation, compile definitions, compile features, link dependencies, generated files, CUDA device-link behavior, and install/export membership.
- Identify directory-level state: global flags, `include_directories`, `add_definitions`, `link_directories`, cache variables, policies, options, and variables that affect subdirectories.
- Separate public API requirements from private build requirements by reading public headers and consumer targets.
- Note external dependency policy: `find_package`, `FetchContent`, `add_subdirectory` vendoring, package managers, environment variables, and manually supplied paths.
- Summarize the current structure before large edits when the cleanup is broad or risky.

## Cleanup And Rework Mode
Use this mode only when the user asks to clean up, modernize, refactor, reorganize, or rework project CMake.
- Convert global or directory-level build state into target-level usage requirements where behavior can be preserved.
- Consolidate repeated target setup into small target-oriented functions only when repetition is real and the function boundary is clear.
- Remove dead variables, duplicate option handling, stale compatibility branches, and unused helper modules after verifying they are not referenced.
- Normalize naming, option definitions, preset layout, dependency wrappers, and install/export rules without changing build semantics unexpectedly.
- Prefer a clear root orchestration file plus focused subdirectory files over one monolithic file or many tiny opaque helper modules.
- Keep custom functions readable: explicit arguments, `cmake_parse_arguments`, target names as inputs, documented side effects through code shape rather than comments.
- Stage risky reworks: first preserve behavior, then simplify; verify after each meaningful phase when possible.
- If build outputs, installed package names, target names, or dependency acquisition behavior would change, call that out before making the change.

## Modern CMake Defaults
- Require the lowest CMake version that supports the features actually used; avoid gratuitous version bumps.
- Use `project(... LANGUAGES CXX CUDA)` when CUDA is a first-class language, not ad hoc `nvcc` custom commands.
- Prefer `add_library` / `add_executable` with `target_sources`, `target_include_directories`, `target_compile_features`, `target_compile_definitions`, `target_compile_options`, and `target_link_libraries`.
- Use `PUBLIC`, `PRIVATE`, and `INTERFACE` deliberately:
  - `PRIVATE`: needed only to build the target.
  - `PUBLIC`: needed by the target and consumers.
  - `INTERFACE`: needed only by consumers of an interface target.
- Prefer imported targets from `find_package` (`Pkg::Lib`) over raw include directories and library paths.
- Model header-only libraries as `INTERFACE` targets.
- Use generator expressions only when they clarify configuration-specific, compiler-specific, or language-specific behavior.
- Prefer `CMakePresets.json` for repeatable local and CI configure/build/test workflows.

## C++ Compilation Errors
- Read the first real compiler error and the innermost user-code instantiation frame before changing CMake.
- If the full command lacks include paths, definitions, language standard, or ABI flags, fix the target's usage requirements.
- If the command is correct, fix the source code rather than masking the error with broad flags.
- For template errors, distinguish library diagnostic noise from the user-code location that supplied the incompatible type or constraint.
- For standard-version issues, prefer `target_compile_features(target PUBLIC cxx_std_20)` or the narrowest appropriate scope.

## CUDA And nvcc
- Enable CUDA as a language for normal `.cu` compilation; use `find_package(CUDAToolkit)` for toolkit libraries such as `CUDA::cudart`, `CUDA::cublas`, or `CUDA::cusparse`.
- Set CUDA standards with target properties or compile features where supported: `CUDA_STANDARD`, `CUDA_STANDARD_REQUIRED`, and `target_compile_features`.
- Use `$<COMPILE_LANGUAGE:CUDA>` generator expressions for CUDA-only options and `$<COMPILE_LANG_AND_ID:CUDA,NVIDIA>` when nvcc-specific behavior matters.
- Check host compiler compatibility before treating nvcc failures as source errors. Verify `CMAKE_CUDA_HOST_COMPILER`, `CMAKE_CUDA_COMPILER`, toolkit version, and target architecture.
- Set architectures with `CMAKE_CUDA_ARCHITECTURES` or target property `CUDA_ARCHITECTURES`; avoid hard-coding obsolete `-gencode` flags unless the project already does.
- Separate host compilation errors from device compilation errors. Watch for unsupported device-side C++ features, missing `__host__` / `__device__` annotations, wrong lambda annotations, and host-only APIs used in device code.
- For separable compilation or device linking, use target properties such as `CUDA_SEPARABLE_COMPILATION` and `CUDA_RESOLVE_DEVICE_SYMBOLS` only when needed.

## Custom Functions And Modules
- Prefer functions over macros so variables do not leak into caller scope.
- Design custom functions around targets, not raw directory variables.
- Validate required arguments with `cmake_parse_arguments` and fail with actionable `message(FATAL_ERROR ...)` text.
- Avoid hidden global state. If state is unavoidable, name cache variables and global properties clearly.
- Keep helper modules idempotent; repeated inclusion should not redefine targets or append flags repeatedly.
- When wrapping common target setup, expose the meaningful policy knobs rather than forcing every target into one build profile.

## Common Fix Patterns
- **Missing include path**: add `target_include_directories(provider PUBLIC include)` if consumers need headers; otherwise `PRIVATE`.
- **Missing compile definition**: add `target_compile_definitions` to the target that owns the requirement.
- **Wrong language standard**: add `target_compile_features` or target standard properties with the narrowest correct scope.
- **Dependency not propagating**: link the dependency as `PUBLIC` or `INTERFACE` from the library whose public headers require it.
- **Link errors**: prefer `target_link_libraries` with targets; check symbol ownership, static library order, visibility, and ABI mismatch.
- **Generator-specific behavior**: fix with generator expressions or presets, not shell-specific command strings.
- **Stale cache**: remove or regenerate the build directory when compilers, toolchains, CUDA architectures, or dependency paths changed.

## Review Checklist
- Are all includes, defines, features, and libraries attached to the correct targets?
- Are public headers supported by matching `PUBLIC` or `INTERFACE` usage requirements?
- Is the C++ or CUDA standard explicit and consistent where needed?
- Are CUDA architectures and host compiler choices intentional?
- Are dependencies found through package targets or well-scoped fallback logic?
- Are custom functions target-oriented, argument-checked, and free of surprising global side effects?
- Are install/export rules present and correct when the project is meant to be consumed by other CMake projects?
- Does the verification command exercise the exact failing target or configuration?

## Constraints
- Do not solve target-specific problems by adding broad global `include_directories`, `add_definitions`, or `CMAKE_CXX_FLAGS` changes unless the project already centralizes configuration that way.
- Do not hide compiler errors behind warning suppressions, permissive flags, or forced casts.
- Do not vendor or fetch dependencies without checking existing dependency policy.
- Do not assume CUDA support is available just because `.cu` files exist; verify language enablement and toolkit discovery.
- Do not rewrite a build system wholesale when a narrow target fix will handle the request.

## Output
Provide:
- the root cause and the CMake target or source file involved
- the relevant configure/build command or compiler diagnostic
- the minimal CMake or source change
- the verification command
- any remaining portability, cache, toolchain, or CUDA architecture risk
