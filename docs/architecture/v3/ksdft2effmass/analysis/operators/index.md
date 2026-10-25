# `ksdft2effmass.analysis.operators`

## Purpose and status

This implemented subpackage owns source-neutral analyses of finite represented
operators. Existing leaves include diagnostics over PhysKit real-symmetric
eigensystems, kinetic-potential decomposition, and retained model-class fitting.
Hamiltonian spectral reduction and its orthogonal residual meanings belong to
`ksdft2effmass.hamiltonian`.
This tranche proposes typed leaves for retained-operator comparison and
analytical-reference residuals.

## Public contract map

- Existing `eigenpair_diagnostics.py` — algebraic residuals and optional
  reference-vector overlaps for exact PhysKit `Eigensystem` inputs.
- Existing `decomposition.py` — typed kinetic-potential decomposition results and
  analysis.
- Existing `model_fitting.py` — explicitly least-Frobenius retained model-class fits.
- Prospective [`retained`](retained/index.md) — analyses of already retained
  operators, beginning with signed comparison.
- Prospective [`residuals`](residuals/index.md) — operator residual analyses,
  beginning with analytical-reference action residuals.

Orthogonal-subspace comparison belongs to
[`ksdft2effmass.analysis.subspaces`](../subspaces/index.md), not this operator owner.

## Schematics

- [Request-bound action and outward composition diagrams](schematics.md)

## Ownership boundary

The subpackage accepts typed in-memory numerical objects. Its reusable result records
may own typed serialization boundaries, but it does not own paths, provenance,
plotting, command-line behavior, study aggregation, or a universal list of diagnostics.
Frobenius, spectral, or maximum-entry observations are selected outward
by composing the canonical PhysKit quantity-aware norm API at
`projectkoios.physkit.linalg.matrix.norm`, except where a leaf operation is explicitly
defined by a particular metric. KSD defines no matrix-norm facade or compatibility
surface.

## Dependency rules

The subpackage may import `ksdft2effmass.operators`, exact PhysKit eigensystem and
unit-free residual capabilities, and `ksdft2effmass.spaces.subspaces`. It must not
import concrete model systems,
experiments, calculations, or campaign composition. Typed result records may import
the KSD serialization contract.

## Code and evidence

- Implemented source: `python/src/ksdft2effmass/analysis/operators/`
- Prospective sources:
  - `python/src/ksdft2effmass/analysis/operators/retained/comparison.py`
  - `python/src/ksdft2effmass/analysis/operators/residuals/reference.py`

The prospective modules have no implementation, tests, supported exports, or retained
numerical evidence yet.
