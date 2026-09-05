---
name: graph-algorithms
description: Use for explicit graph traversal, reachability, SCCs, topological scheduling, coloring, matching, or partitioning. Sparse solver mathematics and elimination-tree interpretation belong to sparse-linear-algebra.
---

# Graph Algorithms

## Scope

Own graph invariants, representation, algorithm selection, and dependency scheduling.
`sparse-linear-algebra` defines what matrix dependencies mean; this skill works on the resulting graph.

## Method

1. Specify vertices, edge direction, weights, duplicates, self-loops, and disconnected components.
   For scheduling, define an edge `u -> v` to mean that `u` must finish before `v` starts.
2. Choose the algorithm for the required result: BFS for unweighted distances, DFS for traversal
   structure, SCC decomposition for directed cycles, topological order for a DAG, coloring for
   conflicts, or an MST method for an undirected weighted spanning forest.
3. Respect assumptions such as nonnegative weights for Dijkstra. Use CSR/CSC, edge lists, or
   parent/child arrays according to updates and access patterns rather than a universal format rule.
4. Verify invariants: reachable vertices, valid predecessor/distance relationships, all edges
   respected by topological order, valid coloring, or acyclicity and spanning coverage for forests.
5. For parallel work, include atomic updates, concurrent discoveries, high-degree imbalance,
   and completion publication in the algorithm, not just in the implementation afterthoughts.

## Dependency levels

For a DAG, assign sources level zero and each other vertex
`level(v) = 1 + max(level(u) for u in predecessors(v))`. Kahn's ready frontiers implement
this when vertices become ready only after all predecessors complete. Reject cycles.

BFS shortest-distance layers are **not** dependency levels. With edges `s -> a`, `s -> b`,
and `a -> b`, BFS puts `a` and `b` in the same layer even though `b` depends on `a`.
SCC condensation is a DAG; its blocks may still depend on one another.

## Parallelism claims

Define the task costs and execution model before quoting work `W`, span `S`, or speedup.
`max(W/P, S)` is a lower bound on time for `P` workers in the idealized model; overhead and
load imbalance add cost. Tree height is a span proxy only for the stated unit-cost task graph.
Minimum frontier width alone is not a bound on overall speedup.

Do not assert universal parallel depth, speculative-coloring round counts, or sequentiality
for all variants of an algorithm. Cite a specific algorithm and assumptions for such claims.

Reference: [Topological generations](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.topological_generations.html).
