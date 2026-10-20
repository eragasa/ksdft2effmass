# `ksdft2effmass.analysis.subspaces.comparison`

## Purpose and status

This prospective module compares exactly two compatible typed orthogonal subspaces by
their projectors. It avoids sign-dependent column-by-column eigenvector comparison.

Target source: `python/src/ksdft2effmass/analysis/subspaces/comparison.py`.

## Contract inventory

| Symbol | Role |
|---|---|
| [`OrthogonalSubspaceComparisonRequest`](OrthogonalSubspaceComparisonRequest/index.md) | Candidate/reference subspace ActionRequest |
| [`OrthogonalSubspaceComparisonResult`](OrthogonalSubspaceComparisonResult/index.md) | Projector-difference ResultObject |
| [`OrthogonalSubspaceComparator`](OrthogonalSubspaceComparator/index.md) | Request-bound ActionObject with `compare()` |

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Boundary and evidence

The module does not choose subspaces, align unequal dimensions, take norms, set
thresholds, or classify equivalence. It is prospective and has no implementation,
tests, supported import, or retained evidence yet.
