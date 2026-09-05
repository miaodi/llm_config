---
name: cuda-performance
description: Use to optimize CUDA kernels or GPU pipeline runtime using measurement. Owns launch, memory, synchronization, transfers, and overlap; ncu-analysis owns report collection/extraction.
---

# CUDA Performance

## Scope

Own GPU implementation and pipeline optimization. Use `ncu-analysis` for Nsight Compute
report mechanics and the active build skill for CUDA compilation/toolchain configuration.

## Method

1. Identify workload, GPU, precision, correctness tolerance, and the end-to-end metric.
2. Use an application timeline to distinguish kernel, transfer, host, launch, and synchronization
   costs. Use kernel counters to investigate a specific mechanism, not to replace application timing.
3. Check memory transactions and reuse, register pressure, synchronization, divergence, and
   serialized work where evidence points. Occupancy is a constraint, not an objective by itself.
4. Evaluate tiling/shared memory against its traffic savings, bank conflicts, synchronization,
   and resource cost. Caches may already provide the desired reuse.
5. Choose launch geometry to match data access and correctness. Flat indexing is a simple
   starting point, not a restriction against useful multidimensional blocks or grids.
6. Check tail bounds, warp masks, barrier participation, stream dependencies, buffer lifetimes,
   and host/device races. Test irregular sizes and use appropriate sanitizers when warranted.
7. Re-measure the same workload outside profiler replay. Report kernel and application effects,
   numerical changes, and hardware-sensitive limitations.

## Integration

Keep host-only runtime/library orchestration in `.cpp` where the build permits it; kernel
code and launch syntax requiring CUDA compilation belong at the existing `.cu` boundary.
When a GPU command fails, distinguish driver/device availability, sandbox access, and profiling
permissions. Use the host's supported approval mechanism only when additional access is needed;
do not assume every environment supports escalation or that every failure is a sandbox problem.
