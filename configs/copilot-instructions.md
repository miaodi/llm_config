# GitHub Copilot Workspace Instructions

Place this file at `.github/copilot-instructions.md` inside any repository to give
Copilot context about that project. The content below can be copied there directly.

## How to apply

1. In the target repository, create `.github/copilot-instructions.md`.
2. Paste (and adapt) the template below.

---

## Template

```markdown
# Copilot Instructions

## Project context
<!-- Briefly describe what this repository does. -->

## Language & toolchain
- Language: C++17/20
- Build system: CMake (modern target-based syntax)
- Linear algebra: Eigen
- Testing: Google Test / Catch2

## Coding conventions
- Use RAII; prefer `std::unique_ptr` / `std::shared_ptr` over raw pointers.
- No `using namespace std;` in headers.
- Mark functions `const`, `noexcept`, and `[[nodiscard]]` where appropriate.
- Keep functions focused on a single responsibility.
- Comment non-obvious mathematical steps with an equation reference.

## Suggestions
- Prefer standard library algorithms over hand-rolled loops.
- When adding CMake targets, use `target_include_directories` and
  `target_link_libraries` with `PUBLIC`/`PRIVATE`/`INTERFACE` correctly.
- For new numerical routines, add a minimal unit test alongside the implementation.
```
