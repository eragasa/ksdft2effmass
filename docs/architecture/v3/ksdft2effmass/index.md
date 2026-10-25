# `ksdft2effmass` source mirror

## Purpose and status

This directory mirrors selected maintained and prospective source contracts below
`python/src/ksdft2effmass/`. Architecture v3 records current ownership and proposed
contract changes separately; a prospective page does not claim that its source symbol
or supported import already exists.

## Child map

- [`hamiltonian`](hamiltonian/index.md): Hamiltonian records, spectral spaces,
  reduction, diagnostics, and decomposition.
- [`operators`](operators/index.md): representation-independent finite-operator values
  and operations.
- [`spaces`](spaces/index.md): finite state-space and subspace contracts.
- [`analysis`](analysis/index.md): reusable analyses over already typed numerical
  objects.
- [`serialization`](serialization/index.md): typed scientific JSON normalization and
  final record boundaries.
- [`model_systems/piab1d`](model_systems/piab1d/index.md): the complete typed PIAB1D
  calculate, verify, and render vertical slice.

Only touched source areas are mirrored in this tranche. Absence from this directory is
not an ownership reassignment.

## Ownership boundary

Model construction remains under `ksdft2effmass.model_systems`. Selection and
composition of multiple diagnostics remain with `experiments/` or `calculations/`.
This source mirror does not define a workflow engine, registry, or universal diagnostic
suite.

## Code mapping

- Source root: `python/src/ksdft2effmass/`
- Architecture ownership map: [`../index.md`](../index.md)

## Evidence and limitations

Implemented reduction contracts have focused software evidence. They do not establish
scientific validation, retained-result acceptance, or publication status.
