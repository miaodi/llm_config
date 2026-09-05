---
name: cpp-performance
description: Use to measure and improve CPU-side C++ latency, throughput, allocations, locality, vectorization, or concurrency cost. Excludes GPU kernel tuning and compile-time optimization.
---

# C++ Runtime Performance

## Scope

Own CPU performance experiments and implementation cost. `cpp-elegance` owns API design;
`cuda-performance` owns GPU work; `computational-learning-notes` owns teaching demonstrations.

## Method

1. Define the workload and metric: latency, throughput, memory, or tail behavior. Establish a
   representative baseline with compiler flags, hardware, inputs, warmup, and repetitions recorded.
2. Locate significant cost with profiling. Inspect algorithmic work, allocations/copies,
   memory access, vectorization barriers, branches, and synchronization only where relevant.
3. Form a testable hypothesis and change one coherent mechanism at a time.
4. Verify outputs before comparing speed. Control setup costs, dead-code elimination, input
   distribution, scheduling, and measurement noise; report absolute and relative results.
5. Check end-to-end impact and adverse cases. A local speedup can lose through conversion,
   allocation, contention, or code-size overhead elsewhere.

## Decision checks

- Data layout should follow access patterns, not a blanket preference for AoS or SoA.
- Branchless transforms may increase work; inspect generated code when the hypothesis depends on it.
- Parallelism needs independence and useful granularity. Account for false sharing, reductions,
  synchronization, NUMA placement, and thread startup when relevant.
- Floating-point reassociation, reduced precision, and approximate arithmetic change semantics;
  evaluate error and determinism along with time.

If execution is unavailable, label proposals as hypotheses and give a focused validation path.
