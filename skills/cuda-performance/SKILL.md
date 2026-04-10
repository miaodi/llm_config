# CUDA Performance Skill

## Purpose
Optimize CUDA code for throughput, latency, memory efficiency, and predictable scaling while preserving correctness.

## When To Use
Use for kernel optimization, launch configuration tuning, memory hierarchy tuning, transfer reduction, and end-to-end GPU pipeline improvement.

## Priorities
1. Preserve correctness.
2. Measure before optimizing.
3. Optimize memory behavior before instruction-level tuning.
4. Prefer shared memory when it meaningfully reduces global memory traffic or enables cooperative data reuse.
5. Optimize end-to-end runtime, not just isolated kernel duration.

## Workflow
1. Identify the dominant kernels and transfer costs from profiling or benchmarks.
2. Confirm the target metric: latency, throughput, utilization, or total pipeline time.
3. Check global memory access patterns for coalescing and unnecessary traffic.
4. Check whether shared memory can be used for tiling, staging, reuse, or cooperative access within a block.
5. Check shared memory bank conflicts, synchronization cost, and occupancy impact.
6. Check register pressure, launch configuration, and whether occupancy is being limited by registers or shared memory.
7. Check divergence, atomics, reductions, and other serialization points.
8. Check whether host-device transfers can be reduced, fused, or overlapped with compute.
9. Propose the smallest high-confidence optimization first.
10. Re-profile under the same conditions and report both kernel-level and end-to-end impact.

## Review Checklist
- Are global memory loads and stores coalesced?
- Is shared memory reducing expensive global traffic or enabling meaningful reuse?
- Are shared memory bank conflicts present?
- Is synchronization within the block justified and minimized?
- Is occupancy limited by registers, shared memory, or launch configuration?
- Is warp divergence hurting throughput?
- Are atomics, reductions, or serialization points on the hot path?
- Is register pressure preventing useful parallelism?
- Are host-device transfers excessive or poorly overlapped?
- Is the optimization improving total runtime rather than only one kernel metric?

## Constraints
- Do not claim performance improvements without profiling or benchmark evidence.
- Do not use shared memory by default if coalesced global access and cache behavior are already sufficient.
- Do not optimize for occupancy alone; verify the actual bottleneck.
- Do not introduce synchronization or shared memory complexity unless the reuse benefit is plausible.
- State tradeoffs in maintainability, numerical behavior, portability, and hardware sensitivity.
- Call out race-condition risks, reduction-order changes, and determinism issues when relevant.

## Output
Provide:
- the likely bottleneck
- whether it is memory-bound, compute-bound, or transfer-bound
- the proposed shared-memory, launch, or memory-access optimization
- why it is expected to help
- the main risks or tradeoffs
- the validation plan
