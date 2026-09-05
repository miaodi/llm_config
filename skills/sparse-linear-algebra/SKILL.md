---
name: sparse-linear-algebra
description: Use for sparse storage invariants, matrix kernels, solver/preconditioner selection, convergence, factorization, reordering, and matrix-derived dependencies. Generic graph algorithms and hardware tuning are separate skills.
---

# Sparse Linear Algebra

## Scope

Own mathematical validity, sparse representations, and numerical tradeoffs. Use
`graph-algorithms` for graph primitives and `cpp-performance`/`cuda-performance` for hardware tuning.

## Characterize and validate

- Establish shape, index base/width, nnz, duplicate policy, sortedness, explicit zeros, and
  structural versus numerical symmetry. A symmetric pattern or positive diagonal does not prove SPD.
- Validate pointer bounds, monotonic offsets, indices, and conversion semantics. Choose CSR/CSC
  for the access direction; consider blocks or padding only after measuring their overhead.
- Compare kernels with small reference problems, including empty rows, duplicates, irregular
  structure, transpose operations, and supported scalar types.

## Solver decisions

- Standard CG assumes a symmetric/Hermitian positive-definite operator with compatible positive-
  definite preconditioning. Specialized semidefinite variants require their own assumptions.
- MINRES requires the appropriate symmetry and compatible SPD preconditioning; arbitrary ILU
  does not automatically preserve those requirements.
- GMRES is a general option; restart affects memory and convergence. Flexible variants handle
  changing preconditioning under their algorithm's assumptions. BiCGSTAB trades storage for
  less regular convergence and possible breakdown.
- Select preconditioning from structure and evidence. IC/ILU can break down; added fill does
  not guarantee improved numerical behavior. AMG suitability depends on the operator and hierarchy.
- Account for singular systems, nullspaces, boundary conditions, scaling, and precision explicitly.
  Do not infer a useful iteration-count range from matrix size alone.

## Dependencies and reordering

- Derive triangular-solve edges from the actual triangular operator and solve direction.
  Use topological dependency levels, not BFS distance or a generic root-first tree traversal.
- For Cholesky, an elimination tree summarizes structural dependencies; weighted tasks,
  supernodes, updates, and communication determine the actual schedule and critical path.
- Distinguish bandwidth/profile reduction from fill reduction and communication balance.
  Compare RCM, AMD, and nested dissection against the objective and matrix family.
- Coloring must represent actual conflicts, including fill or update conflicts where relevant.
  Reordering a Gauss-Seidel/ILU process can change its numerical behavior.
- SCC block triangularization does not make every diagonal block independently solvable;
  respect dependencies in the condensation DAG. Do not equate SCCs with the full
  Dulmage-Mendelsohn decomposition for rectangular/structurally singular systems.

## Acceptance

Compute the true residual `r = b - A*x` and state the norm and tolerance, for example
`||r|| <= atol + rtol*||b||`; handle zero right-hand sides explicitly. Distinguish true,
recursive, and preconditioned residuals. Monitor stagnation, breakdown, and nonfinite values.
Compare setup, factor/apply cost, memory/fill, iterations, and total time across representative
systems and repeated right-hand sides. A residual check alone does not bound forward error
without conditioning information.

Reference: [PETSc CG assumptions](https://petsc.org/release/manualpages/KSP/KSPCG/).
