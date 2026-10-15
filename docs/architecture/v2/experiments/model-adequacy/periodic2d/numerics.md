# Periodic 2-D numerical method

## Finite coordinates

Two-dimensional children use one declared finite reciprocal mesh and one matching
integer representative domain.

- Mesh ordering is deterministic.
- Orbit ordering is deterministic.
- Multiplicities reconstruct complete represented block sums.
- Inactive class coordinates remain embedded and fixed rather than renormalized away.

## Channel calculation

The children construct spectral and operator losses in the same maximal coefficient
space.

- Spectral weights remain positive and are frozen before evaluation.
- Equal full-mesh weights are avoided when they would make the two channels Parseval-identical.
- Operator weighting counts represented blocks rather than free orbit labels unless a child states otherwise.
- Thresholds, boxes, metrics, and tolerances remain child-owned.

## Certificate calculation

Two-dimensional separation uses only a certificate reviewed for the actual child
domain.

- Feasible pairs supply upper bounds.
- Common points supply compatibility evidence.
- Directional support may supply a lower bound after domain premises are checked.
- Full-ellipsoid support requires verified containment or a conservative enclosure.
- Exact arithmetic and rounding details belong to the implementing module or class documentation.

## Deferred details

This package page intentionally remains coarser than its child and future class pages.

- It selects no common matrix shape.
- It selects no common threshold values.
- It selects no common certificate record.
- It selects no generic two-dimensional solver.
