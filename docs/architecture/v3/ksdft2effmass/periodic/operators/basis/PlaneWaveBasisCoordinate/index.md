# `PlaneWaveBasisCoordinate`

## Contract and identity

Frozen coordinate keyed by an exact one-, two-, or three-dimensional reciprocal-lattice
integer index and an optional exact internal-component label.

## Invariants

Indices are tuples of built-in integers; booleans are rejected. `None` means a scalar
coefficient, not an unknown component. Reciprocal-axis order is semantic.

## Dependencies and flow

A provider or analytic basis supplies native ordered reciprocal indices, which enter an
ordered `PeriodicBasisIdentity` without sorting.

## Serialization

The record stores `kind = plane_wave`, `reciprocal_index`, and `component_label` through
`BaseTypedRecord`.

## Scientific boundary

It does not own reciprocal geometry, cutoff completeness, coefficient gauge, or
finite-shift sewing.

## Mappings

Source: `python/src/ksdft2effmass/periodic/operators/basis.py`; tests:
`python/tests/ksdft2effmass/periodic/operators/test__PeriodicBasisIdentity.py`; Sphinx:
`doc/sphinx/api/periodic-basis.rst`.

## Provenance and evidence

The key follows maintained exact reciprocal-index inventories. Tests are software
verification, not plane-wave convergence evidence.

## Limitations

Provider adapters and finite-cutoff reciprocal-shift admission remain unimplemented.

## Navigation

- [Module](../index.md)
- [Embedding boundary](../../../basis_embedding/index.md)
