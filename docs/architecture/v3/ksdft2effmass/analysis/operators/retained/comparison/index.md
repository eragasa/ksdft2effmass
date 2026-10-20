# `ksdft2effmass.analysis.operators.retained.comparison`

## Purpose and status

This prospective module compares exactly two real-symmetric retained operators already
declared in one coordinate system. It owns the signed difference and its coordinate-
dependent diagonal/off-diagonal split.

Target source:
`python/src/ksdft2effmass/analysis/operators/retained/comparison.py`.

## Contract inventory

| Symbol | Role |
|---|---|
| [`RealSymmetricRetainedOperatorComparisonRequest`](RealSymmetricRetainedOperatorComparisonRequest/index.md) | Candidate/reference ActionRequest |
| [`RealSymmetricRetainedOperatorComparisonResult`](RealSymmetricRetainedOperatorComparisonResult/index.md) | Signed matrix ResultObject |
| [`RealSymmetricRetainedOperatorComparator`](RealSymmetricRetainedOperatorComparator/index.md) | Request-bound ActionObject with `compare()` |

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Boundary

The module does not reduce ambient operators, align coordinate systems, infer an energy
reference, calculate norms, or decide adequacy. The caller must supply the common
coordinate identity explicitly.

## Evidence

Prospective architecture only; no implementation, supported import, tests, or retained
numerical evidence exists yet.
