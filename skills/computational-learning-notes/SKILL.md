---
name: computational-learning-notes
description: "Use when creating C++ learning notes or minimal experiments for low-level computational, numerical, CPU/GPU, compiler, and hardware concepts such as false sharing, floating point, registers, caches, SIMD, atomics, numerical stability, and benchmarking pitfalls."
---

# Computational Learning Notes Skill

## Purpose

Teach low-level computational and numerical concepts by turning them into small, demonstrative C++ examples with clear learning notes.

## When To Use

Use when the user wants to understand a software/hardware concept through a minimal example, especially in a learning repository such as `~/repo/cxx_learn`.

Typical topics include false sharing, floating-point behavior, registers, dependency chains, cache hierarchy, cache lines, locality, prefetching, branch prediction, SIMD, FMA, alignment, memory ordering, atomics, synchronization costs, compiler optimization, generated assembly, numerical accuracy, numerical stability, and benchmarking pitfalls.

## Priorities

1. Teach one concept clearly.
2. Default to C++20 unless the user asks for another language.
3. Prefer the smallest example that exposes the mechanism.
4. Make the expected observation explicit.
5. Separate deterministic correctness behavior from hardware-sensitive performance trends.
6. State compiler, OS, CPU, build-mode, and benchmark caveats honestly.

## Concept Coverage

- CPU caches, cache lines, spatial locality, temporal locality, prefetching, TLBs, and memory latency.
- Cache coherence, false sharing, true sharing, thread placement, and synchronization costs.
- Registers, dependency chains, instruction latency, throughput, out-of-order execution, register pressure, and memory-level parallelism.
- Branch prediction, control-flow predictability, branchless transforms, and pipeline effects.
- SIMD, auto-vectorization, alignment, FMA, reductions, and data layout for vector-friendly code.
- Floating-point bit layout, signed zero, subnormals, NaN, infinity, rounding, associativity failure, cancellation, and accumulation error.
- Numerical stability, conditioning, summation order, Kahan summation, pairwise summation, and reproducibility tradeoffs.
- C++ object layout, padding, alignment, copying, allocation, virtual dispatch, atomics, memory orders, data races, and happens-before relationships.
- Compiler behavior such as inlining, dead-code elimination, constant folding, loop unrolling, aliasing assumptions, vectorization reports, and generated assembly.
- Benchmark design issues such as warmup, timer resolution, CPU frequency scaling, turbo, thermal throttling, OS noise, small inputs, dead-code elimination, and hidden setup costs.
- CUDA or GPU concepts only when requested or already present in the task, such as coalescing, shared memory, bank conflicts, occupancy, register pressure, warp divergence, and host-device transfer scope.

## Workflow

1. Identify the exact concept the example should teach.
2. State the mechanism in plain language before writing code.
3. Choose the smallest C++ example that makes the mechanism visible.
4. Prefer one source file and one local `README.md` unless the existing project structure expects tests, benchmarks, or CMake targets.
5. Add a contrast when it improves learning, such as false sharing versus padded counters, strided versus contiguous access, branchy versus predictable branches, scalar versus vectorizable loops, naive summation versus compensated summation, or relaxed atomics versus stronger ordering.
6. Keep unrelated abstractions out of the example.
7. Preserve a simple correctness check when the example has optimized, parallel, or numerically approximate variants.
8. Control obvious confounders: optimization level, dead-code elimination, data size, alignment, warmup, thread scheduling, CPU frequency scaling, compiler version, and measurement overhead.
9. Explain what the learner should observe and why the result may vary across machines.
10. Write the note in the repository's learning-note style.

## Demonstrative Code Heuristics

- Use C++20 and the existing build style of the target repository.
- Keep the code close enough to the mechanism that a reader can map source lines to cache behavior, instructions, synchronization, or floating-point operations.
- Use explicit names such as `naive`, `padded`, `strided`, `contiguous`, `branchy`, `branchless`, `scalar`, `vectorizable`, `relaxed`, `acquire_release`, `kahan`, or `pairwise`.
- Use deterministic inputs when possible.
- Use `std::atomic`, `std::barrier`, `std::thread`, `alignas`, `std::chrono`, `std::numeric_limits`, and small standard-library facilities when they make the concept clearer.
- Use intrinsics, inline assembly, compiler-specific attributes, or disassembly only when the concept cannot be demonstrated cleanly with portable C++.
- For timing examples, keep setup outside the measured region and protect results from dead-code elimination.
- For floating-point examples, print enough digits and explain that algebraic identities may fail under finite precision.
- For concurrency examples, state whether the code is data-race-free and identify the intended happens-before relationship.
- For compiler examples, explain which optimization is being invited or prevented.

## Learning Note Shape

Prefer this structure for new or revised notes:

```text
# Example Name

## Concept
What hardware, compiler, C++, or numerical concept this demonstrates.

## Minimal Example
The smallest relevant code shape, or a pointer to the source file if the code is long.

## What To Run
The configure, build, test, benchmark, or executable command.

## What To Look For
The expected output, trend, comparison, or failure mode.

## Why It Happens
The CPU, memory-system, compiler, C++, CUDA, or numerical mechanism behind the result.

## Caveats
What depends on hardware, compiler, optimization level, OS scheduling, input size, or benchmark setup.

## Extensions
Small follow-up experiments the learner can try.
```

The note should be precise rather than long. A short explanation that names the mechanism and limitation is better than a broad tutorial.

## Review Checklist

- Does the example isolate one concept?
- Is C++ the default language unless another language is clearly better?
- Is there a visible contrast or observation?
- Can the compiler optimize away the behavior being demonstrated?
- Is the measured region free of avoidable setup work?
- Are results protected from dead-code elimination?
- Are correctness checks present for optimized, parallel, or approximate variants?
- Are cache-line, alignment, thread-scheduling, and memory-order assumptions stated when relevant?
- Are floating-point rounding, overflow, underflow, NaN, infinity, and associativity caveats stated when relevant?
- Are exact numbers avoided when only hardware-sensitive trends are justified?
- Does the note include what to run, what to look for, why it happens, and caveats?

## Constraints

- Do not turn a learning example into a reusable framework unless the user explicitly asks for one.
- Do not optimize production code under this skill; use `cpp-performance` for real hot-path optimization.
- Do not claim universal benchmark numbers.
- Do not hide the important mechanism behind generic abstractions, complicated templates, or large helper libraries.
- Do not introduce non-portable code unless it is necessary for the lesson and clearly labeled.
- Do not present undefined behavior, data races, or numerically unstable code as acceptable outside the demonstration.

## Output

Provide:

- the concept being taught
- the minimal C++ example or changed files
- how to build or run it
- what observation to expect
- the mechanism behind the observation
- caveats and machine-specific dependencies
- one or two small follow-up experiments when useful
