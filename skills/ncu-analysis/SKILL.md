---
name: ncu-analysis
description: Use to collect, extract, or compare Nsight Compute .ncu-rep data and metrics. Not for application timeline analysis or implementing CUDA optimizations.
---

# Nsight Compute Analysis

## Scope

Own report generation, metric extraction, and comparable evidence. `cuda-performance` owns
optimization decisions; an application timeline is needed for host overhead and overlap.

## Method

1. Record the installed tool version, GPU, workload, launch selection, and capture options.
2. Query available sections/metrics for that version and device. Capture the smallest useful
   set for the hypothesis; a full set is a deliberate follow-up, not the default.
3. Account for replay, cache control, clock policy, kernel serialization, and profiling overhead.
   A profiled run's wall time is not an application benchmark.
4. Export with the installed CLI or `ncu_report` API. Verify actual API signatures and metric
   names; missing metrics are unavailable, not zero. Preserve reported units and action identity.
5. Match launches by workload, kernel, launch geometry, and invocation/range identity. Never
   collapse repeated launches into a dictionary keyed only by kernel name.
6. Compare matched observations, report unmatched rows, and distinguish a change in workload
   from a regression. Use absolute deltas; percentage changes need a meaningful nonzero baseline.
7. Relate counters to a specific hypothesis and request the next measurement if evidence is weak.
   High/low utilization or cache hit rate alone does not prove a bottleneck.

## Commands

Check `ncu --help` for options supported by the installed release. A captured report can be
exported without rerunning the workload:

```bash
ncu --import run.ncu-rep --csv --page raw > run.csv
```

Validate that extraction produced nonempty records, correct units, and the expected launches.
Do not deliver placeholder code that silently returns an empty analysis.

Reference: [NVIDIA profiling guide](https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html).
