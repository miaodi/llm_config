# Coding Assistant Instructions

## Language Preferences

- Default to **C++17/20** for compiled code unless the context specifies otherwise.
- For scripting or data analysis tasks, use **Python 3**.
- Follow the language's idiomatic style (e.g., RAII in C++, list comprehensions in Python).

## C++ Guidelines

- Prefer standard library types (`std::vector`, `std::array`, `std::span`) over raw arrays and pointers.
- Use smart pointers (`std::unique_ptr`, `std::shared_ptr`) instead of raw `new`/`delete`.
- Mark functions `const`, `noexcept`, and `[[nodiscard]]` where appropriate.
- Avoid `using namespace std;` in header files.
- For numerical/scientific code, favour **Eigen** for linear algebra and include relevant headers explicitly.
- Comment non-obvious mathematical steps with a reference (e.g., equation number or paper).

## Scientific Computing Context

- The codebase often involves finite element methods (FEM), isogeometric analysis (IGA), and linear algebra.
- Prefer cache-friendly data layouts (AoS vs SoA trade-offs matter).
- Distinguish between compile-time and runtime sizes; use templates for the former.

## General Coding Standards

- Write self-documenting code; add comments only when the intent is not obvious from the code.
- Every function should do one thing.
- Tests are preferred as standalone `main()` executables or Google Test/Catch2 cases.
- When suggesting CMake, use modern target-based syntax (`target_include_directories`, `target_link_libraries`).

## Response Format

- Show full, compilable examples when possible.
- When modifying existing code, show only the changed sections with enough context to locate them.
- State the C++ standard required by the snippet (e.g., "requires C++20").
