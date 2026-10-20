# `MomentumSampleRole`

## Status and role

`MomentumSampleRole` is the implemented Phase 1 semantic `Enum` distinguishing general,
construction, and evaluation uses of one finite momentum mesh.

## Public contract

```python
from ksdft2effmass.operators.representations.domains import MomentumSampleRole

role = MomentumSampleRole.construction
```

The enum members are:

- `MomentumSampleRole.general`;
- `MomentumSampleRole.construction`;
- `MomentumSampleRole.evaluation`.

Callers pass these enum members, not raw strings. Their integer `.value` fields are
internal discriminants and are not serialization values.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Limitations

A role identifies intended use only. It does not establish sample independence,
withholding, convergence, or evaluation non-influence.
