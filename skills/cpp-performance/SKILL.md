---
name: cpp-performance
description: "Use when optimizing C++ runtime performance, hot paths, allocations, cache efficiency, vectorization, branch reduction, parallelization, data-oriented design, and concurrency overhead."
---

# C++ Performance Skill

## Purpose
Optimize C++ code for runtime performance, memory efficiency, and predictable behavior without weakening correctness.

## When To Use
Use for hot-path optimization, allocator pressure reduction, cache efficiency, vectorization opportunities, branch reduction, routine parallelization, concurrency overhead analysis, and data-oriented redesign.

## Priorities
1. Preserve correctness.
2. Measure before optimizing.
3. Optimize hot paths before cold code.
4. Prefer algorithmic and data-layout wins before micro-optimizations.
5. Prefer the smallest change that is likely to produce measurable impact.

## Workflow
1. Identify the hot path from profiling data or benchmarks.
2. Confirm the performance goal: latency, throughput, memory footprint, or tail behavior.
3. Inspect algorithmic complexity before tuning low-level details.
4. Check allocations, copies, temporary objects, and ownership patterns.
5. Check data layout, cache locality, branch behavior, access patterns, and whether a data-oriented representation would better match the workload.
6. Check whether unpredictable branches can be removed, hoisted, turned into table lookups, masks, conditional moves, or other branchless forms without harming correctness.
7. Check whether the routine can be parallelized safely across data, tasks, or pipeline stages, and estimate whether the workload size justifies threading overhead.
8. Check whether abstractions prevent inlining, vectorization, or efficient code generation.
9. Check synchronization, contention, false sharing, and scheduling overhead in concurrent code.
10. Propose the smallest high-confidence change first.
11. Re-measure under the same conditions and report absolute and relative impact.

## Review Checklist
- Is this code on a measured hot path?
- Is the current algorithm appropriate for the workload?
- Are unnecessary allocations, copies, or temporaries present?
- Is data layout aligned with access patterns?
- Would a data-oriented layout improve locality, SIMD use, or traversal efficiency?
- Are containers appropriate for the usage pattern?
- Are unpredictable branches hurting throughput on the hot path?
- Can branch-heavy logic be rewritten in a branchless form without making the code unsafe or opaque?
- Can the routine be parallelized across independent work items?
- Is the problem size large enough to justify parallel overhead?
- Is the compiler likely blocked from inlining or vectorizing?
- Are branches predictable on the common path?
- Is synchronization heavier than necessary?
- Could false sharing or cache contention be present?
- Is the benchmark representative of production behavior?

## Constraints
- Do not claim performance improvements without measurement.
- Do not trade clarity for low-level tricks unless the code is proven hot.
- Do not force data-oriented rewrites unless the measured bottleneck is really driven by layout or traversal costs.
- Do not force branchless code where branches are already predictable or the transformed code becomes less maintainable without measurable gain.
- Do not parallelize routines unless independence, granularity, and memory behavior make the speedup plausible.
- Do not optimize microbenchmarks while ignoring end-to-end impact.
- State tradeoffs in readability, portability, compile time, and maintenance cost.
- Call out numerical or semantic risks if optimizations may change behavior.

## Output
Provide:
- the likely bottleneck
- the reason it is expensive
- the proposed optimization
- why it is expected to help
- the main risks or tradeoffs
- the validation plan
