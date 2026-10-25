# `RepresentationSpaceIdentity`

## Status and role

`RepresentationSpaceIdentity` is the implemented Phase 1 DataObject composing the
existing state-space, basis, geometry, and energy-reference owners with scalar-field and
field-coordinate identities.

## Public contract

```python
from ksdft2effmass.operators.representations.spaces import RepresentationSpaceIdentity
```

Stored fields are `identifier`, `state_space`, `basis`, `geometry`, `energy_reference`,
`scalar_field_id`, and `coordinate_convention_id`. `dimension` is derived.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Code and tests

- Source: `operators/representations/spaces.py`
- Tests: `test__RepresentationSpaceIdentity.py` and existing record-owner tests
