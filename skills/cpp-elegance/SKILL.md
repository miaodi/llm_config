---
name: cpp-elegance
description: "Use when writing modern C++ for clarity, expressiveness, type safety, API design, RAII, value semantics, constexpr, concepts, traits, and compile-time design."
---

# C++ Elegance Skill

## Purpose
Write modern C++ that is clear, expressive, type-safe, and efficient by construction.

## When To Use
Use for general C++ implementation, refactoring, API design, code cleanup, and compile-time design when readability, maintainability, and correctness matter as much as performance.

## Priorities
1. Preserve correctness and invariants.
2. Make intent obvious in the type system and interfaces.
3. Prefer simple designs over clever ones.
4. Keep each function focused on one clear responsibility.
5. Prefer stateless functions and functional-style composition when they keep behavior clearer and easier to test.
6. Prefer C++20 language and standard library features when they make the design clearer and the environment supports them.
7. Do work at compile time when it improves clarity or removes unnecessary runtime cost.
8. Keep the generated runtime behavior straightforward and predictable.
9. Use traits, concepts, and compile-time constraints to make generic code explicit and safe when they improve the design.

## Workflow
1. Start from the domain model and choose names that reflect intent.
2. Express invariants in types, constructors, and function signatures.
3. Prefer value semantics and RAII unless shared or dynamic ownership is necessary.
4. Keep each function narrow in purpose; if it starts mixing validation, transformation, coordination, or side effects, split it into clearer pieces.
5. Prefer pure or near-pure helper functions (explicit inputs, explicit outputs, minimal hidden state) before introducing mutable shared state.
6. Reach for C++20 facilities first when they simplify the code, such as concepts, ranges, `std::span`, `std::string_view`, `constexpr`, and stronger standard-library vocabulary types.
7. Prefer compile-time computation with `constexpr`, `consteval`, and `static_assert` when the logic is naturally static and the code remains readable.
8. Use traits, concepts, and type-level constraints to express intent when generic code is necessary, but keep the metaprogramming surface small.
9. Prefer standard library facilities and simple composition over custom frameworks or inheritance-heavy designs.
10. Keep control flow explicit and data ownership easy to trace.
11. Remove incidental complexity, duplicated logic, and weak abstractions.
12. Check whether the code is easy to test, reason about, and optimize.

## Review Checklist
- Do names reflect the actual domain meaning?
- Are invariants enforced by the type system where practical?
- Does each function have one clear purpose that matches its name and signature?
- If this is a header, does it use `#pragma once` unless there is a concrete reason not to?
- Is ownership explicit and easy to follow?
- Is RAII used to manage resources safely?
- Would value semantics simplify the design?
- Can mutable state be reduced by using stateless or pure-function structure?
- Would a C++20 facility express the intent more directly or remove custom boilerplate?
- Is compile-time evaluation appropriate here?
- Would `constexpr`, `consteval`, or `static_assert` make the code safer or simpler?
- Would traits or concepts clarify generic intent, or would they only add indirection?
- Is generic code justified, or is it adding complexity without enough benefit?
- Is inheritance necessary, or would composition be clearer?
- Are error cases explicit and hard to ignore?
- Can another experienced C++ developer understand the code quickly?

## Constraints
- Do not use templates or metaprogramming only to look advanced.
- Do not use traits, concepts, or type tricks if simpler code expresses the idea more clearly.
- Do not default to legacy pre-C++20 patterns when a clearer C++20 approach is available and supported.
- Do not push logic to compile time if it harms readability, diagnostics, or compile time without a clear benefit.
- Do not let a single function accumulate unrelated responsibilities when splitting it would make intent clearer.
- Do not introduce manual include guards by default when `#pragma once` is acceptable for the project.
- Do not hide ownership, lifetime, or control flow behind weak abstractions.
- Do not introduce dynamic polymorphism when static structure is sufficient.
- Prefer small, composable abstractions over large generic frameworks.
- Do not introduce hidden mutable shared state when explicit data flow would be clearer.

## Output
Provide:
- the design improvement being made
- why the new structure is clearer
- any compile-time techniques used
- tradeoffs in flexibility, compile time, or complexity
- any follow-up cleanup that would further simplify the code
