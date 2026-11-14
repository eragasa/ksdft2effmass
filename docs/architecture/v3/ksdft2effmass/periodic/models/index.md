# `ksdft2effmass.periodic.models`

## Status

Implemented owner of periodic scientific-model identity and dimension-neutral
block-hopping representation behavior.

## Inheritance refinement

The hierarchy separates dimensional finite-rank identity from represented-operator
capability:

```text
PeriodicModel
├── PeriodicBlockHoppingModel
├── Periodic1DRankNModel
│   └── Periodic1DRank2Model
├── Periodic2DRankNModel
│   └── Periodic2DRank2Model
└── Periodic3DRankNModel
    └── Periodic3DRank2Model
```

Each complete rank-two block-hopping model combines its dimensional rank-two owner with
`PeriodicBlockHoppingModel`:

```text
Periodic1DRank2Model + PeriodicBlockHoppingModel
    -> Periodic1DRank2BlockHoppingModel
Periodic2DRank2Model + PeriodicBlockHoppingModel
    -> Periodic2DRank2BlockHoppingModel
Periodic3DRank2Model + PeriodicBlockHoppingModel
    -> Periodic3DRank2BlockHoppingModel
```

There is no separate public dimension-neutral fixed-rank block-hopping owner. Rank two
refines each dimensional finite-rank model; block hopping remains dimension-neutral
reusable behavior. This structure preserves dimensional nominal types without
duplicating rank and validation logic.

The dimensional children are frozen, slotted values. Each retains an exact dimensional
structured basis identity, explicit unit-bearing lattice geometry, and an immutable
dense or sparse PhysKit block-hopping representation. Construction verifies exact owner
types, basis coordinate count, provider block size, spatial dimension, and complete
conjugate-displacement Hermiticity.

## Ownership

The KSD hierarchy owns:

- scientific-model identity;
- scientific role through `PeriodicModelRole(StrWireEnum)`;
- periodic spatial dimension;
- retained band-subspace rank;
- exact ordered structured basis identity;
- physical direct-lattice geometry correlation; and
- admissibility of the composed ordinary-lattice representation.

PhysKit owns dense and sparse coefficient storage, lattice-displacement records, units,
provider basis-identifier storage, energy-reference representation, and raw
block-hopping mechanics. Provider basis strings remain descriptive and do not establish
structured basis compatibility.

Calculators, sampled Hamiltonian fields, Fourier transforms, gauge operations,
equivalence analyses, locality analyses, support decisions, campaign policy,
serialization, provenance, and scientific acceptance remain outside these model types.

## Source mapping

- `python/src/ksdft2effmass/periodic/models/base.py` owns `PeriodicModel`,
  `PeriodicModelRole`, and `SpatialDimension`.
- `python/src/ksdft2effmass/periodic/models/block_hopping.py` owns
  `PeriodicBlockHoppingModel`.
- Dimensional `rankN/models/base.py` modules own finite-rank contracts and exact
  dimensional basis requirements.
- Dimensional `rank2/models/base.py` modules refine finite-rank contracts to rank two.
- Dimensional `rank2/models/block_hopping.py` modules own the three complete composed
  models.

## Detailed architecture

- [`PeriodicBlockHoppingModel`](PeriodicBlockHoppingModel/index.md)
- [Periodic-1D rank-two models](../periodic1d/rank2/models/index.md)
- [Periodic-2D rank-two models](../periodic2d/rank2/models/index.md)
- [Periodic-3D rank-two models](../periodic3d/rank2/models/index.md)
