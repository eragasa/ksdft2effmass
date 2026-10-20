# `ksdft2effmass.operators.transformations.identities` module

## Purpose and status

This implemented Phase 1 module owns the representation-transformation kind enum,
immutable directed edge identity, and its identity-only factory. It depends on intrinsic
node identities from `operators.representations.identities`.

## Contract inventory

| Symbol | Role |
|---|---|
| [`RepresentationTransformationKind`](RepresentationTransformationKind/index.md) | explicit computational and edge-kind discriminator |
| [`TransformationIdentity`](TransformationIdentity/index.md) | kind, method, orientation, and full source/target identities |
| [`TransformationIdentityFactory`](TransformationIdentityFactory/index.md) | carrier-compatible edge-identity construction only |

```python
from ksdft2effmass.operators.transformations.identities import (
    RepresentationTransformationKind,
    TransformationIdentity,
    TransformationIdentityFactory,
)
```

The enum is not a raw string, wire token, serializer contract, or universal operational
factory key. Its integer `.value` is internal.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Code and tests

- Source: `python/src/ksdft2effmass/operators/transformations/identities.py`
- Tests: class-matched modules under
  `python/tests/software_verification/ksdft2effmass/operators/transformations/`

Nominal role and enum agreement does not prove operation correctness, qualification,
evidence, or formal correspondence.
