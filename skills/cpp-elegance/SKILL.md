---
name: cpp-elegance
description: Use for C++ ownership, lifetime, API contracts, value semantics, and generic/compile-time design. Not for build configuration or performance tuning without a design question.
---

# C++ Design

## Scope

Own C++ interfaces, invariants, and maintainability. `coding` owns defect investigation;
`cpp-performance` owns measured CPU cost; the active build skill owns compiler configuration.

## Method

- Follow the project's supported language level and conventions. Use newer facilities only
  when supported and useful; do not upgrade the standard merely to modernize spelling.
- Make ownership, borrowing, lifetime, error handling, and thread-safety contracts explicit.
  Prefer value semantics and RAII; use shared ownership only when lifetimes require it.
- Check dangling views/references, iterator invalidation, exception guarantees, and move behavior.
- Prefer small cohesive functions and explicit data flow. Use composition before inheritance;
  introduce runtime interfaces only for actual substitution needs.
- Express generic requirements with clear constraints. Prefer `if constexpr` when compile-time
  alternatives require different valid code, without multiplying unnecessary instantiations.
- Use `constexpr`, `consteval`, and `static_assert` to express real static contracts, weighing
  diagnostic quality, build time, and binary size. Runtime data still needs runtime decisions.
- Prefer standard vocabulary types when their lifetime and cost semantics fit the interface.
- Apply cohesion and substitutability principles to concrete problems, not as a mandate for
  classes, extension points, or dependency-injection frameworks.

## Data flow and workspace

- Distinguish borrowed dependencies, configuration, persistent algorithmic state, caches,
  and temporary workspace. Keep members for a clear lifetime or reuse requirement, with
  explicit update points and cache-invalidation rules.
- Make computed outputs visible through return values or explicit output parameters/views.
  Avoid helper calls that silently populate a member consumed by another call; owning a
  reusable buffer does not require hiding writes to it.
- Prefer local values when reuse is unnecessary. When reusing storage, use cohesive named
  workspaces and overwrite scratch before reading it. Pass only the dependencies a helper
  needs; passing the entire implementation object merely relocates hidden coupling.
- Choose failure guarantees at the appropriate boundary. Preserve accepted state and
  transactional updates, but allow disposable evaluation outputs to be unspecified on
  failure when callers discard them. Do not add staging buffers and final copies solely
  to preserve scratch outputs without a required contract.
- Respect aliasing, borrowed views, and storage identity when removing temporaries; swapping
  buffers is not a general replacement for writing into caller-owned storage. Keep runtime
  performance claims subject to measurement through `cpp-performance`.

Respect existing include-guard conventions. Verify representative callers and supported build
configurations; explain behavioral/API changes and meaningful tradeoffs rather than listing features used.
