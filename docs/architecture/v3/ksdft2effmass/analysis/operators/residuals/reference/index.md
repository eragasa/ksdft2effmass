# `ksdft2effmass.analysis.operators.residuals.reference`

## Purpose and status

This prospective module evaluates the action residual of one finite real-symmetric
operator and one orthogonal trial injection against a declared retained reference.

Target source: `python/src/ksdft2effmass/analysis/operators/residuals/reference.py`.

## Contract inventory

| Symbol | Role |
|---|---|
| [`RealSymmetricReferenceResidualRequest`](RealSymmetricReferenceResidualRequest/index.md) | Operator/trial/reference ActionRequest |
| [`RealSymmetricReferenceResidualResult`](RealSymmetricReferenceResidualResult/index.md) | Matrix residual ResultObject |
| [`RealSymmetricReferenceResidualAnalyzer`](RealSymmetricReferenceResidualAnalyzer/index.md) | Request-bound ActionObject with `analyze()` |

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Boundary and evidence

This module does not calculate Galerkin leakage, reduce the operator, choose a norm, or
classify error sources. It is prospective and has no implementation, tests, supported
import, or retained evidence yet.
