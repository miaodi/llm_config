---
name: graph-algorithms
description: "Use when working with graph traversals (BFS, DFS, level-order), minimum spanning trees, strongly connected components, topological sort, graph coloring, bipartite detection, elimination trees, level-set extraction, parallel graph algorithms, task-tree parallelism, sparse graph representations, and exploiting graph structure for parallel sparse computations."
---

# Graph Algorithms Skill

## Purpose
Reason about, implement, optimize, and parallelize graph algorithms—especially those arising from sparse matrix computations, dependency analysis, and tree-based task decomposition.

## When To Use
Use when the task involves:
- Graph traversals: BFS, DFS, level-order, multi-source BFS.
- Shortest paths: Dijkstra, Bellman-Ford, delta-stepping (parallel SSSP).
- Minimum spanning tree (MST): Kruskal, Prim, Borůvka (parallelizable).
- Strongly connected components (SCC): Tarjan, Kosaraju, forward-backward (parallel).
- Topological sort: Kahn's algorithm (BFS-based), DFS-based, parallel prefix-sum variants.
- Graph coloring: greedy sequential, Jones-Plassmann (parallel), speculative/optimistic coloring, distance-1 and distance-2 coloring.
- Bipartite detection, bipartite matching, maximum matching.
- Elimination trees: construction, postordering, subtree sizes, column dependencies.
- Level-set extraction from elimination trees or DAGs for parallel scheduling.
- Tree parallelism: subtree-to-processor mapping, bottom-up aggregation, Euler-tour techniques.
- Parallel graph primitives: parallel BFS (direction-optimizing), parallel connected components (Shiloach-Vishkin, label propagation), parallel SCC.
- Graph partitioning: multilevel (Metis/Scotch), spectral bisection, edge/vertex separators.
- Sparse graph representations: adjacency arrays (CSR-like), edge lists, compressed adjacency.

## Priorities
1. Correctness of traversal order and dependency semantics—never violate topological constraints.
2. Identify available parallelism before choosing an algorithm variant; the structure of the graph dictates the concurrency.
3. Match the algorithm to the graph topology: dense short-diameter graphs favor BFS-based parallel methods; tree-like structures favor subtree parallelism.
4. Use the graph's sparse representation efficiently—avoid dense adjacency matrices; prefer CSR/CSC adjacency arrays.
5. Quantify parallelism: critical-path length, number of levels, average parallelism (work / depth).

## Core Knowledge

### Graph Traversals

| Algorithm | Sequential | Parallel variant | Parallelism characteristics |
|-----------|-----------|-----------------|---------------------------|
| BFS | O(V+E) queue-based | Direction-optimizing (top-down/bottom-up hybrid) | Level-synchronous; parallelism = vertices per frontier |
| DFS | O(V+E) stack-based | Inherently sequential in general; parallel DFS on trees via Euler tour | Poor parallelism on general graphs due to ordering constraints |
| Level-order | BFS-derived | Same as parallel BFS | Natural level sets = independent work per level |
| Multi-source BFS | O(V+E) from multiple roots | Parallel frontier expansion from all sources | Higher parallelism from combined frontiers |

**Key insight:** BFS produces level sets that are naturally parallel (all vertices in a level are independent of each other within that level). DFS is inherently sequential on general graphs but can be parallelized on trees via Euler-tour techniques.

### Minimum Spanning Tree (MST)

- **Kruskal:** Sort edges by weight, union-find to avoid cycles. Sequential O(E log E). Parallel: batch edge processing with concurrent union-find (limited scalability).
- **Prim:** Grow tree from a single vertex, priority queue for minimum crossing edge. Sequential O(E log V). Hard to parallelize effectively.
- **Borůvka:** Each component selects its lightest outgoing edge simultaneously; contract and repeat. O(E log V) sequential but **naturally parallel**—all components act independently per round. O(log V) rounds, each with O(E/P + V/P) parallel work.
- **Parallel MST strategy:** Borůvka for coarsening + Kruskal or Prim on the contracted graph.

### Strongly Connected Components (SCC)

- **Tarjan (sequential):** Single DFS with a stack. O(V+E). Standard for sequential SCC.
- **Kosaraju (sequential):** Two DFS passes (forward + transpose graph). O(V+E). Simple but requires two full traversals.
- **Forward-Backward (parallel):** Pick pivot, compute forward-reachable (BFS/DFS from pivot) and backward-reachable (BFS/DFS on transpose). Intersection = one SCC. Recurse on remaining subgraphs. Expected O(log²V) depth on random graphs; worst case still sequential.
- **Multistep (parallel):** Combines coloring/trimming with forward-backward. Trim vertices with in-degree or out-degree 0 (trivial SCCs). Color propagation to identify candidates.
- **Application in sparse solvers:** SCC decomposition → block triangular form → independent diagonal blocks can be solved in parallel.

### Topological Sort

- **Kahn's algorithm (BFS-based):** Maintain in-degree counts; enqueue vertices with in-degree 0. Dequeue, reduce neighbors' in-degrees. **Parallel variant:** all zero-in-degree vertices in the current frontier form a level set—process them in parallel, then update in-degrees atomically.
- **DFS-based:** Reverse DFS finish order. Inherently sequential.
- **Parallel prefix topological sort:** Assign topological numbers using parallel BFS levels. Vertices at the same BFS level from sources have no dependencies among themselves.
- **Level sets from topological sort = scheduling levels for parallel execution.**

### Graph Coloring

- **Greedy sequential:** Process vertices in some order, assign smallest available color. Quality depends on vertex ordering (smallest-last, largest-first, incidence-degree).
- **Jones-Plassmann (parallel):** Assign random priorities to vertices. A vertex colors itself when it has the highest priority among its uncolored neighbors. Expected O(log V / log log V) rounds on bounded-degree graphs.
- **Speculative / optimistic coloring:** Color all vertices tentatively in parallel (ignore conflicts). Detect conflicts. Re-color conflicting vertices. Iterate. Typically converges in 2–3 rounds on sparse graphs.
- **Distance-1 coloring:** Adjacent vertices get different colors. Used for parallel Gauss-Seidel (same-color rows are independent).
- **Distance-2 coloring:** Vertices within distance 2 get different colors. Used for sparse Jacobian computation via column compression (Curtis-Powell-Reid).
- **Applications in sparse parallelism:**
  - Multicolor ordering: reorder rows/columns by color → within each color, all rows are independent → parallel sweep.
  - Parallel ILU: color-ordered ILU allows level-free parallelism within each color group.

### Bipartite Graphs

- **Detection:** BFS/DFS 2-coloring. If successful, graph is bipartite.
- **Maximum matching:** Hopcroft-Karp O(E√V). Used in sparse matrix permutation to zero-free diagonal (maximum transversal).
- **Weighted bipartite matching:** Hungarian algorithm or auction algorithm (parallel).
- **Application in sparse solvers:** Row/column permutation for numerical stability (maximum transversal / maximum weight matching for large diagonal entries via MC64/HSL_MC64).

### Elimination Trees

The elimination tree is the fundamental structure connecting sparse factorization to parallelism.

- **Definition:** For SPD matrix A with Cholesky factor L, the elimination tree T has parent(j) = min{i > j : l_{ij} ≠ 0}. Vertex j's subtree determines which columns must be computed before column j.
- **Construction:** O(nnz) using the disjoint-set (union-find) algorithm of Liu (1990). Process columns left to right; for each off-diagonal entry l_{ij}, union j into i's set.
- **Properties:**
  - Column j depends only on columns in its subtree → **subtrees are independent and can execute in parallel**.
  - The tree height = critical-path length = minimum parallel time for the factorization.
  - Postordering the elimination tree improves memory locality (consecutive columns in the same subtree).
- **Supernodal elimination tree:** Merge consecutive columns with identical non-zero structure into supernodes → coarser tree with better BLAS-3 granularity.

### Level-Set Extraction from Elimination Trees

**This is the primary mechanism for parallel sparse factorization scheduling.**

1. **Compute tree levels:** Assign level(root) = height. For each vertex, level(v) = level(parent(v)) − 1. Or bottom-up: level(leaf) = 0, level(v) = max(level(children)) + 1.
2. **Level sets:** Group vertices (columns) by level. All columns at the same level have no mutual dependencies → execute in parallel.
3. **Bottom-up level sets (for factorization):** Level 0 = leaves (all independent). Level k = vertices whose children are all at level < k. Process levels 0, 1, 2, ... sequentially; within each level, all tasks are parallel.
4. **Top-down level sets (for triangular solve):** Used in SpTRSV. Level 0 = roots/sources (no incoming dependencies). Level k = vertices whose predecessors are all at level < k.
5. **Parallelism metric:** Average parallelism = (number of vertices) / (number of levels). Tall-skinny trees → poor parallelism. Bushy/wide trees → good parallelism.
6. **Improving parallelism:**
   - Reorder to produce wider elimination trees (nested dissection produces balanced separator trees → good parallelism).
   - Supernodal aggregation increases granularity per task (fewer, larger parallel tasks).
   - Relaxed supernodes: allow small extra fill to merge thin branches → fewer levels, more work per task.

### Tree Parallelism Patterns

General techniques for extracting parallelism from any rooted tree:

- **Subtree parallelism:** Independent subtrees execute concurrently. Load balance by assigning subtrees of similar weight to processors.
- **Euler-tour technique:** Flatten tree into a sequence via Euler tour → prefix sums on the tour compute tree aggregates (depth, subtree size, pre/post order) in O(log V) parallel depth.
- **Heavy-path decomposition:** Partition tree into heavy paths + light edges. Heavy paths are processed sequentially (good cache behavior); light subtrees spawn parallel tasks.
- **Bottom-up aggregation:** Process leaves first (all parallel), then their parents, etc. Natural for factorization.
- **Top-down broadcast:** Process root first, then its children (all parallel), etc. Natural for triangular solve forward-substitution from the root.

### Parallel Graph Algorithm Paradigms

| Paradigm | Description | Examples |
|----------|-------------|---------|
| Level-synchronous | Process all vertices at the same BFS level simultaneously; barrier between levels | Parallel BFS, parallel topological sort, level-scheduled SpTRSV |
| Label propagation | Each vertex adopts the label of a neighbor (e.g., minimum); iterate to convergence | Parallel connected components (Shiloach-Vishkin), parallel SCC trimming |
| Speculative execution | Optimistically perform work assuming no conflicts; detect and repair | Parallel coloring, parallel ordering, speculative SpTRSV |
| Divide and conquer | Recursively partition the graph; solve subproblems independently; combine | Nested dissection, parallel MST (Borůvka rounds), recursive graph bisection |
| Work-stealing / task-based | Subtrees or subgraphs as tasks; dynamic load balancing via work queues | Subtree-parallel factorization, parallel DFS on trees |

### Sparse Graph Representations

- **CSR adjacency (row_ptr, col_idx):** Same as sparse matrix CSR without values. O(1) degree lookup, efficient neighbor iteration. Default for most parallel graph frameworks.
- **CSC adjacency:** Transpose view. Efficient for reverse/predecessor queries (e.g., transpose graph for SCC).
- **Edge list:** Simple (src, dst, weight) triples. Good for sorting (Kruskal), partitioning, and streaming.
- **Compressed delta encoding:** For graphs with locality (social networks), store neighbor offsets as deltas. Reduces memory bandwidth.
- **Blocked/tiled adjacency:** Partition vertices into tiles; store sub-adjacency per tile. Improves cache behavior for partitioned parallel traversals.

### Complexity and Parallelism Summary

| Algorithm | Work (sequential) | Depth (parallel) | Parallelism (Work/Depth) |
|-----------|-------------------|-------------------|--------------------------|
| BFS | O(V+E) | O(diameter) | O((V+E)/diameter) |
| Borůvka MST | O(E log V) | O(log²V) | O(E / log V) |
| SCC (fwd-bwd) | O(V+E) expected | O(log²V) expected | O((V+E)/log²V) |
| Topological sort (Kahn) | O(V+E) | O(longest path) | O((V+E)/longest path) |
| Coloring (Jones-Plassmann) | O(V+E) expected | O(log V) expected | O((V+E)/log V) |
| Elimination tree levels | O(nnz) construction | O(tree height) schedule | O(n/tree height) |
| Euler tour + prefix sum | O(V) | O(log V) | O(V/log V) |

## Workflow
1. **Identify the graph:** Extract adjacency structure from the sparse matrix (or DAG, or explicit graph). Determine: directed/undirected, weighted/unweighted, size (V, E), structure (tree, DAG, general, planar).
2. **Determine the goal:** Traversal order? Decomposition (SCC, bipartite)? Scheduling (topological levels)? Coloring for independence? MST? Parallelism extraction?
3. **Assess parallelism potential:** Compute or estimate critical-path length (diameter, tree height, longest path). Calculate average parallelism = work / depth.
4. **Choose algorithm variant:** Sequential when V is small or graph is adversarial for parallel methods. Parallel variant when graph is large with good structure (low diameter, bushy trees, balanced partitions).
5. **Implement with sparse representation:** Use CSR/CSC adjacency arrays. Avoid materializing dense structures. For trees, parent-array or child-list representation suffices.
6. **Extract parallelism from trees/DAGs:** Compute level sets (bottom-up for factorization, top-down for solves). Map levels to barriers; within-level tasks are independent.
7. **Validate:** Check traversal visits all reachable vertices. Verify topological order respects all edges. Verify coloring has no conflicts. Verify level sets respect dependencies.
8. **Profile:** Measure load imbalance across levels/partitions. Identify bottleneck levels (levels with few tasks). Consider re-partitioning or supernodal merging to improve granularity.

## Review Checklist
- Does the traversal visit all intended vertices (handle disconnected components)?
- Is the directed/undirected distinction handled correctly (symmetric adjacency vs. asymmetric)?
- Are graph indices 0-based or 1-based consistently?
- For parallel BFS: is the frontier correctly synchronized between levels?
- For topological sort: does the output respect all edge directions? Are cycles detected/rejected?
- For SCC: is the transpose graph correctly constructed?
- For coloring: is the coloring valid (no adjacent same-color pair)? Is the number of colors reasonable (bounded by max-degree + 1)?
- For elimination trees: is the parent array correct? Does postordering preserve the tree structure?
- For level sets: do all dependencies point from lower levels to higher levels? Is no task scheduled before its predecessors complete?
- For parallel algorithms: is the work/depth tradeoff acceptable? Is synchronization overhead (barriers, atomics) amortized over sufficient parallel work?
- Is the sparse representation (CSR/CSC) correctly indexed (row_ptr has V+1 entries, col_idx has E entries)?

## Constraints
- Do not assume undirected graphs unless verified; SCC, topological sort, and reachability are direction-sensitive.
- Do not parallelize DFS on general graphs—the ordering semantics are inherently sequential; use BFS-based alternatives for parallelism.
- Do not ignore the critical-path length when claiming parallelism; a tall elimination tree yields negligible speedup regardless of processor count.
- Do not apply topological sort to graphs with cycles; detect and report cycles or decompose via SCC first.
- Do not confuse elimination tree height (factorization parallelism) with BFS depth (traversal parallelism)—they are different structural properties.
- Level-set parallelism is bounded by the narrowest level (Amdahl's law on the bottleneck level); report both average and minimum level width.
- Graph coloring with minimum colors is NP-hard; heuristics produce near-optimal results for sparse graphs but provide no approximation guarantee.
- When using speculative parallel methods (optimistic coloring, speculative SpTRSV), always include a conflict-detection and repair phase.

## Output
Provide:
- Graph characterization: type (directed/undirected, weighted, DAG, tree), size (V, E), structure (diameter, tree height, max degree).
- Algorithm selection with rationale: why this variant suits the graph's structure and the parallelism target.
- Parallelism analysis: critical-path length, number of levels, average parallelism, expected speedup bounds.
- Implementation sketch using sparse (CSR/CSC) representations.
- Level-set or scheduling strategy when the goal is parallel execution.
- Risks: adversarial graph structures, load imbalance, overhead from synchronization or speculation.
- Validation plan: correctness checks appropriate to the algorithm (cycle detection, coloring validity, topological order verification, dependency-respecting level assignment).
