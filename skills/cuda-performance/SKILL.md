---
name: cuda-performance
description: "Use when optimizing CUDA kernels, analyzing CUDA profiler reports, GPU memory hierarchy, shared memory, coalescing, launch configuration, occupancy, warp divergence, host-device transfers, and end-to-end GPU pipeline."
---

# CUDA Performance Skill

## Purpose
Optimize CUDA code for throughput, latency, memory efficiency, and predictable scaling while preserving correctness.

## When To Use
Use for kernel optimization, CUDA profiler report analysis, launch configuration tuning, memory hierarchy tuning, transfer reduction, and end-to-end GPU pipeline improvement.

## Priorities
1. Preserve correctness.
2. Measure before optimizing.
3. Optimize memory behavior before instruction-level tuning.
4. Prefer shared memory when it meaningfully reduces global memory traffic or enables cooperative data reuse.
5. Prefer 1D thread/block launch geometry and `threadIdx.x` indexing unless multidimensional launch geometry is required by an existing interface or clearly improves correctness/readability.
6. Optimize end-to-end runtime, not just isolated kernel duration.

## Workflow
1. Identify the dominant kernels and transfer costs from profiling reports or benchmarks.
2. Confirm the target metric: latency, throughput, utilization, or total pipeline time.
3. Check global memory access patterns for coalescing and unnecessary traffic.
4. Check whether shared memory can be used for tiling, staging, reuse, or cooperative access within a block.
5. Check shared memory bank conflicts, synchronization cost, and occupancy impact.
6. Check register pressure, launch configuration, and whether occupancy is being limited by registers or shared memory.
7. For new or refactored kernels, prefer a flat global thread id from `blockIdx.x * blockDim.x + threadIdx.x`; convert that id to logical 2D or 3D coordinates inside the kernel only when needed.
8. Check divergence, atomics, reductions, and other serialization points.
9. Check whether host-device transfers can be reduced, fused, or overlapped with compute.
10. Propose the smallest high-confidence optimization first.
11. Re-profile under the same conditions and report both kernel-level and end-to-end impact.

## CUDA Source File Policy
- Prefer `.cpp` / `.hpp` for host-side orchestration, CUDA runtime or toolkit-library calls, and code that uses or launches existing kernels through host-callable project APIs.
- Create or convert to `.cu` only when implementing or refactoring kernel/device code such as `__global__` / `__device__` functions, device lambdas, shared-memory tiling, warp-level device logic, or when following an existing project convention for CUDA-only implementation files.
- When existing kernel launch plumbing requires CUDA compilation, prefer reusing or extending the project's existing `.cu` wrapper boundary instead of creating new `.cu` callers by default.
- When adding new GPU behavior to a project that already separates kernels from callers, keep kernel implementations in `.cu` and put host-only integration, scheduling, validation, and higher-level API code in `.cpp`.

## GPU Execution And Sandbox Access
- When running a CUDA executable, test, benchmark, or profiler command inside the sandbox, treat "no GPU found" style failures as possibly caused by sandboxed device access rather than absent hardware.
- This includes errors such as no CUDA-capable device, `cudaGetDeviceCount` returning zero, `CUDA_ERROR_NO_DEVICE`, missing `/dev/nvidia*`, inaccessible `nvidia-smi`, or profiler failures that cannot see a GPU.
- If the command otherwise appears valid, ask to rerun the same executable or profiler command outside the sandbox with escalated permissions before concluding that the machine has no compatible GPU.
- Keep the rerun command as close as possible to the failing command so performance, correctness, and profiler results remain comparable.

## Profile Report Analysis
When given Nsight Compute (`ncu`), Nsight Systems (`nsys`), CUPTI, or benchmark profiler output:
- Treat the report as the source of truth and cite the specific kernel, metric, table, or timeline observation driving each conclusion.
- Separate kernel time, API time, transfer time, synchronization gaps, and total application time.
- Rank findings by measured impact, not by how interesting the metric looks.
- For Nsight Compute, map symptoms to likely causes: low memory throughput, poor coalescing, high replay, bank conflicts, low achieved occupancy, register pressure, divergence, instruction mix, or dependency stalls.
- For Nsight Systems, look for CPU-side launch overhead, serialized streams, implicit synchronizations, transfer/compute overlap gaps, allocator overhead, and idle GPU intervals.
- Distinguish measured facts from hypotheses; propose the next profiling counter or experiment when evidence is incomplete.
- Avoid recommending kernel rewrites from a single red metric unless it explains a meaningful share of runtime.

## Review Checklist
- Are global memory loads and stores coalesced?
- Is shared memory reducing expensive global traffic or enabling meaningful reuse?
- Are shared memory bank conflicts present?
- Is synchronization within the block justified and minimized?
- Is occupancy limited by registers, shared memory, or launch configuration?
- Does the kernel use a 1D launch and `threadIdx.x` where practical, mapping from flat ids to logical 2D/3D coordinates only when needed?
- Is warp divergence hurting throughput?
- Are atomics, reductions, or serialization points on the hot path?
- Is register pressure preventing useful parallelism?
- Are host-device transfers excessive or poorly overlapped?
- Is the optimization improving total runtime rather than only one kernel metric?
- Does the profile show whether the bottleneck is inside kernels, transfers, synchronization, launch overhead, or CPU-side orchestration?
- If a CUDA run reports no GPU, was sandboxed device access ruled out by asking to rerun the same command outside the sandbox?

## Constraints
- Do not claim performance improvements without profiling or benchmark evidence.
- Do not overfit to profiler percentages without checking absolute time and total pipeline impact.
- Do not use shared memory by default if coalesced global access and cache behavior are already sufficient.
- Do not optimize for occupancy alone; verify the actual bottleneck.
- Do not introduce synchronization or shared memory complexity unless the reuse benefit is plausible.
- Do not introduce `threadIdx.y`, `threadIdx.z`, `blockIdx.y`, or `blockIdx.z` by default; prefer flat 1D indexing and explain any exception.
- State tradeoffs in maintainability, numerical behavior, portability, and hardware sensitivity.
- Call out race-condition risks, reduction-order changes, and determinism issues when relevant.

## Output
Provide:
- the likely bottleneck
- whether it is memory-bound, compute-bound, or transfer-bound
- the profiler evidence behind that classification
- the proposed shared-memory, launch, or memory-access optimization
- why it is expected to help
- the main risks or tradeoffs
- the validation plan
