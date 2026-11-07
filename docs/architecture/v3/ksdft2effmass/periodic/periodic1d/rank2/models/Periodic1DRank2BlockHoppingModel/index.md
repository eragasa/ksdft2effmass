# `Periodic1DRank2BlockHoppingModel`

## Status and responsibility

Implemented frozen, slotted scientific-model value in
`python/src/ksdft2effmass/periodic/periodic1d/rank2/models/block_hopping.py`.

The class directly inherits `PeriodicRank2BlockHoppingModel`. It completes the shared
contract with exact one-dimensional geometry, identity, role, and one composed PhysKit
dense or sparse block-hopping representation.

## Construction boundary

Construction requires:

- a nonempty built-in string identity;
- one exact `PeriodicModelRole`;
- an immutable `Periodic1DLatticeGeometry` with an explicit physical length unit;
- provider dimension one;
- exact `2 x 2` coefficient blocks; and
- complete exactly Hermitian ordinary-lattice support.

`Periodic1DLatticeGeometry` reconstructs the PhysKit `DirectLattice1D` primitive rather
than retaining a mutable provider object. The model contains no mesh, tolerance, gauge
analysis, truncation policy, campaign, persistence, or execution identity.

## Legacy representation boundary

The existing `BlockHoppingModel1D` remains a distinct representation owner. It preserves
intermediate Fourier coefficients, arbitrary square block rank, reciprocal-period
metadata, and historical study contracts. The existing
`CenteredEvenMeshCyclicToOrdinaryResult1D` remains the explicit cyclic-to-ordinary
conversion value and retains the removed negative-Nyquist channel.

Neither existing value inherits from this model, and this model does not inherit from or
alias either value. A maintained study may construct this model only after its existing
composition root explicitly supplies physical geometry, model role, model identity,
ordered basis identity, and energy reference and preserves the ordinary source and
conversion evidence separately.

No shared legacy-admission class is approved. The model hierarchy remains exactly the
approved hierarchy documented in [`ksdft2effmass.periodic.models`](../../../../models/index.md).
The existing `BlockHoppingModel1D` exposes the additive
`to_physkit_ordinary_representation()` method, which maps its declared ordinary support to
provider-owned dense storage while preserving arbitrary block rank. This method is a
representation conversion on the existing class; it does not construct a KSD scientific
model or change the inheritance outline. Any proposed new class or public conversion
type requires separate human approval before it is documented or implemented.

## Transitional migration policy

`BlockHoppingModel1D` and its conversion values remain active until every maintained
consumer has migrated study by study. Migration must not mutate historical bytes, add a
compatibility alias, introduce dual writes, or silently infer the direct period from the
legacy reciprocal period.

A study may leave the legacy boundary only after source-to-model correlation, numerical
parity, retained-result replay, and provenance checks pass under unchanged declared
tolerances. Active legacy-source retirement remains a separately authorized action.

## Source mapping

- `python/src/ksdft2effmass/solidstate/hopping_transforms.py` retains
  `BlockHoppingModel1D`, the cyclic-to-ordinary conversion values, and the additive
  provider-representation method.
- `python/src/ksdft2effmass/periodic/periodic1d/rank2/models/block_hopping.py`
  retains the approved concrete scientific model.

## Detailed documents

- [Numerics](numerics.md)
- [Schematic](schematics.md)
- [Scientific interpretation](scientifics.md)
