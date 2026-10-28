# `ksdft2effmass.periodic1d.fourier_locality.result`

## Status and responsibility

Implemented direct result module for the compatible rank-one Fourier-locality
calculation. The module contains four frozen, slotted typed records and one supported
calculation-family identity. It defines no execution identity, schema prose, evidence
state, serializer class, validation framework, or compatibility facade.

## Public classes

- [`Periodic1DFourierLocalityEvaluationResult`](Periodic1DFourierLocalityEvaluationResult/index.md)
  owns the common withheld evaluation samples.
- [`Periodic1DFourierLocalityRangeResult`](Periodic1DFourierLocalityRangeResult/index.md)
  owns one attained ordinary-support comparison.
- [`Periodic1DFourierLocalityMeshResult`](Periodic1DFourierLocalityMeshResult/index.md)
  owns one construction mesh, its complete transform values, and ordered range table.
- [`Periodic1DFourierLocalityCalculationResult`](Periodic1DFourierLocalityCalculationResult/index.md)
  composes the authored configuration, ordered meshes, refinement values, and sampled-gap
  summary.

Each record uses explicit `_mapping()` and `_from_mapping()` implementations through
`BaseTypedRecord`. Canonical JSON decoding enters the same constructors as direct Python
construction.

## Admission boundary

Section constructors reject malformed local types, units, shapes, ordering, and stored
local dispositions. The root constructor correlates configuration inventories, complete
and finite-support coefficients with their candidates, decisive threshold passages,
adjacent-mesh refinement values, and the sampled-gap minimizer.

These checks admit a self-consistent finite result. Independent verification remains a
separate operation and must reconstruct the authoritative values without invoking the
production analyzer.

## Related pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Parent package](../index.md)
