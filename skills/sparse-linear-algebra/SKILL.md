---
name: sparse-linear-algebra
description: "Use when working with sparse matrices, sparse storage formats (CSR, CSC, COO, BSR, ELL), sparse matrix-vector multiply (SpMV), sparse matrix-matrix multiply (SpGEMM), triangular solves, level scheduling, ILU and IC preconditioners, iterative solvers (CG, GMRES, BiCGSTAB), algebraic multigrid, reordering (RCM, AMD, nested dissection, Metis), fill-in analysis, graph-based sparsity reasoning, graph partitioning, coloring, and sparse direct solvers."
---

# Sparse Linear Algebra Skill

## Purpose
Reason about, implement, optimize, and debug sparse matrix algorithms, iterative and direct solvers, preconditioners, reorderings, and the graph-theoretic structure underlying sparsity patterns.

## When To Use
Use when the task involves:
- Sparse storage formats and conversions (CSR, CSC, COO, BSR, ELL, DIA, HYB, blocked variants).
- Sparse kernels: SpMV, SpMM, SpGEMM, sparse triangular solve (SpTRSV), sparse transpose.
- Iterative Krylov solvers: CG, PCG, GMRES, FGMRES, BiCGSTAB, TFQMR, MINRES, QMR.
- Preconditioners: Jacobi, block-Jacobi, Gauss-Seidel, SOR/SSOR, ILU(k), ILUT, IC(k), ICT, approximate inverse (AINV, SPAI), algebraic multigrid (AMG), domain decomposition.
- Level scheduling and dependency analysis for parallel triangular solves.
- Fill-in estimation and symbolic factorization.
- Sparse direct solvers and their phases: symbolic analysis, numerical factorization, solve.
- Reordering and permutation: RCM (reverse Cuthill-McKee), AMD (approximate minimum degree), nested dissection, Metis/ParMetis, Scotch, Sloan.
- Graph interpretation of sparse matrices: adjacency structure, graph Laplacian, bandwidth, envelope, strongly connected components, bipartite matching, elimination trees, supernodes.
- Graph partitioning, coloring (distance-1, distance-2), and independent sets for parallelism.
- Convergence diagnostics, spectral analysis, condition number estimation.
- Libraries: Eigen (sparse module), PETSc, Trilinos, HYPRE, cuSPARSE, cuSOLVER, MKL Pardiso, SuiteSparse (CHOLMOD, UMFPACK, SPQR, AMD, COLAMD), SuperLU, AMGX, MUMPS, HSL.

## Priorities
1. Correctness of the numerical algorithm: verify symmetry requirements, definiteness assumptions, and convergence conditions before optimizing.
2. Choose the right algorithm before tuning the implementation—solver/preconditioner selection dominates iteration count.
3. Understand the sparsity structure and its graph-theoretic meaning before choosing formats or reorderings.
4. Minimize fill-in and preserve structure through reordering before factoring.
5. Exploit parallelism through level sets, coloring, partitioning, or block structure—not by ignoring dependencies.
6. Match storage format to the dominant kernel and hardware target.

## Core Knowledge

### Sparse Storage Formats
| Format | Best for | Notes |
|--------|----------|-------|
| CSR (Compressed Sparse Row) | row-wise SpMV, general kernels | most common default; row pointers + column indices + values |
| CSC (Compressed Sparse Column) | column-wise access, direct solvers | transpose of CSR; natural for column-oriented factorization |
| COO (Coordinate) | assembly, incremental construction, format conversion | simple triplet storage; sort by row or column for conversion |
| BSR (Block Sparse Row) | FEM matrices with fixed block size | block entries stored as dense sub-matrices; improves register reuse |
| ELL (ELLPACK) | GPU SpMV with uniform row lengths | padded to max nnz per row; wasteful if row lengths vary widely |
| DIA (Diagonal) | banded/stencil matrices | stores offsets + dense diagonals; very efficient for structured grids |
| HYB (Hybrid ELL+COO) | GPU SpMV with skewed row-length distribution | ELL for bulk, COO for outlier rows |

### Iterative Solvers
- **CG (Conjugate Gradient):** SPD matrices only. Optimal Krylov method for SPD systems. Convergence depends on condition number κ(A); with a good preconditioner, iteration count ~ √κ(M⁻¹A).
- **GMRES:** General non-singular systems. Minimizes residual over Krylov subspace. Restart parameter m controls memory; unrestarted GMRES converges monotonically but costs O(m) vectors and O(m²) Gram-Schmidt work per cycle.
- **FGMRES (Flexible GMRES):** Allows variable (nonlinear) preconditioners per iteration—needed when inner solve is inexact or changes between iterations.
- **BiCGSTAB:** Non-symmetric systems. Lower memory than GMRES (fixed short recurrence). Can exhibit irregular convergence; stabilized variant of BiCG.
- **MINRES:** Symmetric indefinite systems. Minimizes residual norm with short recurrence.
- **TFQMR:** Transpose-free variant; useful when A^T-vector product is expensive.

### Preconditioners
- **Jacobi / Block-Jacobi:** Diagonal or block-diagonal scaling. Cheap, embarrassingly parallel. Effective when diagonal dominance is strong.
- **Gauss-Seidel / SOR / SSOR:** Sequential sweeps; good smoother for multigrid. Parallel variants require coloring or domain decomposition.
- **ILU(k):** Incomplete LU with level-of-fill k. ILU(0) preserves the sparsity pattern of A. Higher k improves approximation but increases fill and cost. Level-of-fill determined by symbolic factorization on the elimination graph.
- **ILUT:** Threshold-based ILU. Drop entries below τ; keep at most p entries per row. More adaptive than level-based ILU but harder to tune.
- **IC(k) / ICT:** Incomplete Cholesky for SPD systems. Analogous to ILU(k)/ILUT but exploits symmetry, storing only one triangle. Breakdown possible if matrix is not sufficiently diagonally dominant—compensated IC adds diagonal shifts.
- **Approximate Inverse (AINV, SPAI):** Compute M ≈ A⁻¹ directly in sparse form. Inherently parallel application (SpMV instead of triangular solve). Higher setup cost.
- **Algebraic Multigrid (AMG):** Multi-level hierarchy built from matrix entries. Classical (Ruge-Stüben) or aggregation-based (smoothed aggregation, unsmoothed). Near-optimal for elliptic PDE discretizations. Setup cost amortized over many solves or time steps.
- **Domain Decomposition:** Additive/multiplicative Schwarz, restricted additive Schwarz (RAS). Natural parallelism. Overlap and coarse-grid correction control effectiveness.

### Triangular Solve and Level Scheduling
- SpTRSV is inherently sequential along dependency chains.
- **Level scheduling:** Compute the topological levels of the DAG defined by the triangular matrix's non-zero pattern. Rows in the same level are independent and can execute in parallel.
- Level-set computation: BFS/topological sort on the dependency graph of L or U.
- Parallelism is limited by the critical-path length (number of levels). Matrices from structured grids often have O(n^{1/d}) levels in d dimensions.
- Alternatives to level scheduling: self-scheduling, block-level scheduling, wavefront, and approximate inverse preconditioners that avoid triangular solves entirely.

### Reordering
- **RCM (Reverse Cuthill-McKee):** Reduces bandwidth. BFS-based; start node selection matters (pseudo-peripheral node heuristic). Good for banded solvers and cache locality.
- **AMD (Approximate Minimum Degree):** Reduces fill-in during factorization. Greedy elimination ordering approximating minimum degree. Widely used in direct solvers.
- **Nested Dissection:** Recursively bisect the adjacency graph; order separators last. Produces O(n log n) fill for 2D and O(n^{4/3}) for 3D problems. Optimal asymptotic fill for regular meshes.
- **Metis / ParMetis / Scotch:** Multilevel graph partitioning heuristics. Used for nested dissection orderings, domain decomposition, and parallel load balancing.
- **Sloan:** Reduces profile/wavefront. Combines BFS-level and degree priority.

### Graph–Matrix Duality
- A sparse matrix A defines a directed graph G(A): vertex i → vertex j if a_{ij} ≠ 0.
- Symmetric structure ↔ undirected graph.
- Strongly connected components of G(A) ↔ irreducible diagonal blocks under permutation to block triangular form (Dulmage-Mendelsohn decomposition).
- Elimination tree of A (SPD): tree on columns where parent(j) = min{i > j : l_{ij} ≠ 0}. Encodes column dependencies in Cholesky factorization; enables subtree parallelism.
- Supernodes: consecutive columns with identical non-zero structure in L. Enable dense BLAS-3 kernels inside sparse factorization.
- Graph Laplacian L = D − A: encodes diffusion, spectral partitioning (Fiedler vector), algebraic connectivity.
- Graph coloring (distance-1): rows/columns of same color are independent for Jacobi-like sweeps. Distance-2 coloring needed for efficient Jacobian computation via finite differences.

### Graph Partitioning and Coloring
- **Partitioning:** Divide graph into k balanced subsets minimizing edge cut. Used for parallel distribution, nested dissection, and domain decomposition.
- **Coloring:** Assign colors so no two adjacent vertices share a color. Enables parallel Gauss-Seidel (color-by-color sweeps), parallel ILU, and sparse Jacobian computation.
- **Independent sets:** Maximal independent sets used in AMG coarsening and multicolor ordering.

## Workflow
1. **Characterize the system:** Determine size, nnz, symmetry, definiteness, conditioning, and origin (PDE type, mesh dimension, physics).
2. **Examine sparsity structure:** Visualize or query the non-zero pattern. Identify bandwidth, block structure, diagonal dominance, and whether the graph is structured or unstructured.
3. **Select solver class:** SPD → CG; symmetric indefinite → MINRES; non-symmetric → GMRES or BiCGSTAB; very ill-conditioned or robust need → direct solver or AMG-preconditioned Krylov.
4. **Select preconditioner:** Match to problem physics and structure. ILU(0) as baseline; AMG for elliptic-dominant; block preconditioners for multi-physics; approximate inverse for GPU.
5. **Choose reordering:** RCM for bandwidth/cache; AMD or nested dissection for fill minimization in direct or ILU factors.
6. **Choose storage format:** CSR for CPU SpMV; BSR if natural block structure; ELL/HYB for GPU; CSC for column-oriented factorization.
7. **Implement or configure:** Use established libraries when available. Hand-roll only when library gaps exist or kernel-level tuning is required.
8. **Validate correctness:** Check residual ‖b − Ax‖ / ‖b‖, compare against direct solve on small instance, verify preconditioner does not break symmetry if CG is used.
9. **Profile and tune:** Measure iteration count, time per iteration, preconditioner setup cost, and total solve time. Adjust fill level, drop tolerance, restart parameter, or AMG settings.

## Review Checklist
- Is the matrix symmetric? Positive definite? Is the solver compatible with these properties?
- Is the preconditioner preserving the symmetry required by the solver (e.g., SPD preconditioner for CG)?
- Is the reordering appropriate for the goal (bandwidth reduction vs. fill reduction)?
- Is the storage format matched to the dominant kernel and target hardware?
- Are triangular-solve dependencies respected in parallel implementations?
- Is level scheduling correctly computed (no circular dependencies, correct topological order)?
- Is fill-in controlled? Is the ILU/IC factorization stable (no zero/negative pivots in IC)?
- Is the convergence criterion appropriate (relative residual, preconditioned residual, energy norm)?
- Are iteration counts reasonable for the problem class? If not, is the preconditioner effective?
- For graph operations: is the adjacency structure correctly extracted from the matrix (handling symmetric vs. non-symmetric, self-loops/diagonal)?
- Is the graph coloring valid (no adjacent vertices share a color)?
- Is partitioning balanced? Is the edge cut or communication volume acceptable?
- Are boundary conditions handled correctly in the matrix assembly and not breaking solver assumptions?

## Constraints
- Do not assume SPD without verification; applying CG to a non-SPD system will silently produce wrong results or diverge.
- Do not conflate bandwidth reduction (RCM) with fill reduction (AMD/ND); they are different objectives.
- Do not ignore the preconditioner setup cost when reporting solver performance—it can dominate for single solves.
- Do not parallelize triangular solves by ignoring dependencies; this changes the numerical result and may diverge.
- Do not over-fill ILU/IC (high k or low τ): memory and apply-cost may exceed the benefit of fewer iterations.
- State the assumptions on matrix structure (symmetric, definite, diagonal dominance, well-conditioned) that the chosen algorithm relies on.
- When comparing solvers or preconditioners, report total time (setup + iterations × per-iteration cost), not just iteration count.

## Output
Provide:
- characterization of the matrix / sparsity pattern / graph structure
- the recommended solver, preconditioner, reordering, and format with rationale
- key implementation details or library configuration
- expected behavior (iteration count range, fill ratio, level count)
- risks: convergence failure modes, stability concerns, scalability limits
- validation plan: residual check, comparison to reference, sensitivity to parameters
