---
name: ncu-analysis
description: "Use when automating Nsight Compute (.ncu-rep) profiling, extracting metrics with ncu_report, comparing profiles, and diagnosing CUDA kernel bottlenecks."
---

# NCU Analysis Skill

## Purpose
Automate Nsight Compute profiling and report analysis so CUDA kernel performance regressions and bottlenecks can be found quickly and reproducibly.

## When To Use
Use for `.ncu-rep` generation, programmatic extraction of NCU metrics, profile-to-profile comparisons, CI performance checks, and memory-vs-compute bottleneck diagnosis.

## Priorities
1. Preserve measurement validity before optimizing.
2. Keep profiling runs reproducible (same kernel, shape, device, clocks, and launch path).
3. Extract a minimal, decision-driving metric set first.
4. Separate measured facts from hypotheses.
5. Report kernel-level and end-to-end impact.

## Workflow
1. Confirm experiment parity: same GPU, driver/CUDA stack, workload shape, warmup policy, and iteration count.
2. Capture `.ncu-rep` with stable commands and explicit output naming.
3. Extract key metrics (runtime, occupancy, memory throughput/utilization, cache behavior, stall reasons) using `ncu_report` or `ncu --csv` where appropriate.
4. Normalize and aggregate results by kernel name and shape, then export JSON/CSV artifacts.
5. Compare baseline vs candidate profile and compute deltas and percent changes.
6. Classify likely bottleneck type (memory-bound, compute-bound, latency/launch-bound, or occupancy-limited) using evidence from counters.
7. Propose the smallest high-confidence optimization and a re-profile validation plan.

## Reference Commands
```bash
# 1) Produce report files
ncu --set full --target-processes all -o run_a ./your_binary --your-args
ncu --set full --target-processes all -o run_b ./your_binary --your-args

# 2) Optional quick CSV export (without Python API)
ncu --import run_a.ncu-rep --csv --page raw > run_a.csv
ncu --import run_b.ncu-rep --csv --page raw > run_b.csv
```

## Programmatic Extraction Pattern
```python
# Requires Nsight Compute's Python module (commonly imported as ncu_report)
import json

# import ncu_report  # environment-specific import path

KEY_METRICS = [
    "gpu__time_duration.sum",
    "sm__throughput.avg.pct_of_peak_sustained_elapsed",
    "smsp__warps_active.avg.pct_of_peak_sustained_active",
    "dram__throughput.avg.pct_of_peak_sustained_elapsed",
    "l1tex__t_sectors_pipe_lsu_mem_global_op_ld_lookup_hit_rate.pct",
    "lts__t_sectors_srcunit_tex_op_read_lookup_hit_rate.pct",
]


def summarize_report(report_path: str) -> dict:
    # Pseudocode: adapt to the exact ncu_report API available in your environment.
    # report = ncu_report.load_report(report_path)
    # kernels = report.ranges[0].actions
    kernels = []
    rows = []
    for k in kernels:
        row = {"kernel": k.name()}
        for m in KEY_METRICS:
            # row[m] = k.metric_by_name(m).as_double()
            row[m] = None
        rows.append(row)
    return {"report": report_path, "rows": rows}


def compare_rows(a_rows: list[dict], b_rows: list[dict]) -> list[dict]:
    by_kernel_a = {r["kernel"]: r for r in a_rows}
    out = []
    for rb in b_rows:
        ra = by_kernel_a.get(rb["kernel"])
        if not ra:
            continue
        delta = {"kernel": rb["kernel"]}
        for k, vb in rb.items():
            if k == "kernel":
                continue
            va = ra.get(k)
            if isinstance(va, (int, float)) and isinstance(vb, (int, float)) and va != 0:
                delta[f"{k}_delta"] = vb - va
                delta[f"{k}_pct"] = (vb - va) / abs(va) * 100.0
        out.append(delta)
    return out


# Example artifact shape
# summary_a = summarize_report("run_a.ncu-rep")
# summary_b = summarize_report("run_b.ncu-rep")
# comparison = compare_rows(summary_a["rows"], summary_b["rows"])
# print(json.dumps(comparison, indent=2))
```

## Bottleneck Heuristics
- Memory-bound signal: high DRAM throughput utilization with low SM throughput and low arithmetic utilization.
- Compute-bound signal: high SM throughput with relatively lower memory pressure.
- Occupancy-limited signal: low active warps/occupancy with register or shared-memory pressure clues.
- Cache inefficiency signal: low L1/L2 hit rates with elevated memory transactions.
- Launch/latency issues: short kernels dominated by launch/synchronization overhead in the end-to-end timeline.

## Review Checklist
- Are baseline and candidate runs comparable (shape, clocks, software stack, warmup, repetitions)?
- Were hot kernels identified by absolute time contribution, not just percentages?
- Are metric names and units recorded exactly as reported by NCU?
- Did comparison output include both absolute deltas and percent deltas?
- Are conclusions tied to measured counters instead of assumptions?
- Is there a concrete validation loop (change, re-profile, confirm total runtime impact)?

## Constraints
- Do not claim wins without before/after measurements under matching conditions.
- Do not over-interpret a single red metric without checking total runtime contribution.
- Do not compare profiles across different hardware or incompatible software stacks.
- Keep metric sets stable across runs to preserve comparability.
- Call out uncertainty when required counters are missing.

## Output
Provide:
- profiling command(s) used and environment assumptions
- top kernels by runtime contribution
- extracted key metrics per kernel
- baseline vs candidate deltas (absolute and percent)
- bottleneck classification with evidence
- next optimization action and validation steps
