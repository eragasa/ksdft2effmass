# `ksdft2effmass` source mirror

## Purpose and status

This directory mirrors selected maintained and prospective source contracts below
`python/src/ksdft2effmass/`. Architecture v3 records current ownership and proposed
contract changes separately; a prospective page does not claim that its source symbol
or supported import already exists.

## Child map

- [`operators`](operators/index.md): representation-independent finite-operator values
  and operations.
- [`spaces`](spaces/index.md): finite state-space and subspace contracts.
- [`analysis`](analysis/index.md): reusable analyses over already typed numerical
  objects.

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

The proposed reduction contracts linked below are documentation-first designs. They
have no source, test, Sphinx, retained-result, or scientific-validation evidence yet.
