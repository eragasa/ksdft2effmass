# `ksdft2effmass.periodic.models`

## Status

Implemented owner of periodic scientific-model identity and rank-two block-hopping
models.

## Hierarchy

```text
Model
└── PeriodicModel
    └── PeriodicBlockHoppingModel
        └── PeriodicRank2BlockHoppingModel
            ├── Periodic1DRank2BlockHoppingModel
            ├── Periodic2DRank2BlockHoppingModel
            └── Periodic3DRank2BlockHoppingModel
```

`PeriodicRank2BlockHoppingModel` is the required shared parent of all three complete
dimensional models. It fixes retained band-subspace rank two while leaving dimension,
geometry, scientific role, model identity, and provider representation to the concrete
child.

The dimensional children are frozen, slotted values. They expose an exact PhysKit direct
lattice from immutable dimensional geometry and compose an immutable dense or sparse
PhysKit block-hopping model. The 1D child retains physical period and length unit. The 2D
and 3D children retain the ordered primitive-basis matrix and length unit through their
existing dimensional geometry values and derive `DirectLatticeMetric`. All validate
exact spatial dimension, retained basis size two, and complete
conjugate-displacement Hermiticity.

## Ownership

The KSD hierarchy owns:

- scientific-model identity;
- scientific role through the closed `PeriodicModelRole(StrWireEnum)` vocabulary;
- periodic spatial dimension;
- retained band-subspace rank;
- physical direct-lattice geometry correlation; and
- admissibility of the composed ordinary-lattice representation.

PhysKit owns dense and sparse coefficient storage, displacement records, units,
provider basis-identifier storage, and energy-reference representation. KSD owns
structured periodic basis identity and composes provider values without subclassing or
duplicating them. `PeriodicModelRole` supplies explicit `to_wire()` and `from_wire()`
mapping; it does not create role-specific package or class hierarchies.

Calculators, sampled Hamiltonian fields, Fourier transforms, gauge operations,
equivalence analyses, locality analyses, support decisions, campaign policy,
serialization, provenance, and scientific acceptance remain outside these model types.
The approved hierarchy contains no legacy-admission superclass, adapter subclass, or
parallel rank-two model. Any proposed new public class requires separate human approval
before architecture or implementation changes.

## Source mapping

- `python/src/ksdft2effmass/periodic/models/base.py` owns `PeriodicModel`,
  `PeriodicModelRole`, and `SpatialDimension`.
- `python/src/ksdft2effmass/periodic/models/block_hopping.py` owns
  `PeriodicBlockHoppingModel` and the shared
  `PeriodicRank2BlockHoppingModel` parent.
- `python/src/ksdft2effmass/periodic/periodic1d/rank2/models/block_hopping.py` owns the
  complete periodic-1D child.
- `python/src/ksdft2effmass/periodic/periodic2d/rank2/models/block_hopping.py` owns the
  complete periodic-2D child.
- `python/src/ksdft2effmass/periodic/periodic3d/rank2/models/block_hopping.py` owns the
  complete periodic-3D child.

The model hierarchy is nested beneath `ksdft2effmass.periodic`; calculators and
analyzers remain in their operation-owning packages and import these model types.

## Detailed architecture

- [`PeriodicRank2BlockHoppingModel`](PeriodicRank2BlockHoppingModel/index.md)
- [Periodic-1D concrete model](../periodic1d/rank2/models/Periodic1DRank2BlockHoppingModel/index.md)
- [Periodic-2D concrete model](../periodic2d/rank2/models/Periodic2DRank2BlockHoppingModel/index.md)
- [Periodic-3D concrete model](../periodic3d/rank2/models/Periodic3DRank2BlockHoppingModel/index.md)
