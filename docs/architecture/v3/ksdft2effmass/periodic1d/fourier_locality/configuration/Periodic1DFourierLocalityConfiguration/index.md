# `Periodic1DFourierLocalityConfiguration`

## Status and responsibility

Implemented immutable `BaseTypedRecord` in
`ksdft2effmass.periodic1d.fourier_locality.configuration`.

The class is the direct calculation input, following `Piab1dConfiguration`: fields are
explicit constructor arguments, constructor validation admits their intrinsic and
cross-field domains, and canonical typed decoding invokes the same constructor. It does
not create a model or perform calculation behavior.

## Public fields

- exact `parent_identity`, `onsite_numerators`, `positive_hopping_numerators`, and
  `coefficient_denominator`;
- `construction_mesh_sizes` and `production_construction_size`;
- `evaluation_size` and exact rational evaluation-shift numerator/denominator;
- ordered `maximum_ranges`;
- sampled-gap and application thresholds; and
- energy, relative, squared-energy, dimensionless, and refinement consistency terms.

## Deliberate omissions

There is no `standard()` constructor, schema identity field, basis prose field,
Fourier-sign field, decision-rule string, plot inventory, or runtime model property.
`construction_reduced_momenta()` and `evaluation_reduced_momenta()` are pure derived
coordinate methods using exact `Fraction` formulas before binary64 conversion; they do
not introduce additional authored state.

## Public import

```python
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityConfiguration,
)
```

## Related pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Owning module](../index.md)
