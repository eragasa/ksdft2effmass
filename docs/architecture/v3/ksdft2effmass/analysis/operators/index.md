# `ksdft2effmass.analysis.operators`

## Purpose and status

This implemented subpackage owns source-neutral analyses of finite represented
operators. Existing leaves include compression residuals, diagnostics over PhysKit
real-symmetric eigensystems, additive decomposition identifiability, and retained
model-class fitting.
This tranche proposes typed leaves for orthogonal reduction, retained-operator
comparison, and analytical-reference residuals.

## Public contract map

- Existing `compression_residuals.py` — consistent, unmatched, and discarded-sector
  residual matrices.
- Existing `eigenpair_diagnostics.py` — algebraic residuals and optional
  reference-vector overlaps for exact PhysKit `Eigensystem` inputs.
- Existing `decomposition_identifiability.py` — retained additive decomposition
  analysis.
- Existing `model_fitting.py` — explicitly least-Frobenius retained model-class fits.
- Prospective [`reduction`](reduction/index.md) — reduction of one represented
  operator through one declared orthogonal subspace.
- Prospective [`retained`](retained/index.md) — analyses of already retained
  operators, beginning with signed comparison.
- Prospective [`residuals`](residuals/index.md) — operator residual analyses,
  beginning with analytical-reference action residuals.

Orthogonal-subspace comparison belongs to
[`ksdft2effmass.analysis.subspaces`](../subspaces/index.md), not this operator owner.

## Schematics

- [Request-bound action and outward composition diagrams](schematics.md)

## Ownership boundary

The subpackage accepts typed in-memory numerical objects. It does not own paths, JSON,
provenance, plotting, command-line behavior, study aggregation, or a universal list of
diagnostics. Frobenius, spectral, or maximum-entry observations are selected outward
by composing the existing general matrix-norm analyzer, except where a leaf operation
is explicitly defined by a particular metric.

## Dependency rules

The subpackage may import `ksdft2effmass.operators`, exact PhysKit eigensystem and
unit-free residual capabilities, and `ksdft2effmass.spaces.subspaces`. It must not
import concrete model systems,
experiments, calculations, campaign composition, or serializers.

## Code and evidence

- Implemented source: `python/src/ksdft2effmass/analysis/operators/`
- Prospective sources:
  - `python/src/ksdft2effmass/analysis/operators/reduction.py`
  - `python/src/ksdft2effmass/analysis/operators/retained/comparison.py`
  - `python/src/ksdft2effmass/analysis/operators/residuals/reference.py`

The prospective modules have no implementation, tests, supported exports, or retained
numerical evidence yet.
