# `FourierLocalityVerification`

## Responsibility

Concrete `CompositeVerification` component grouping the independently reconstructed
scientific comparisons for Fourier locality. It excludes the separate visualization-
projection component so numerical/scientific checks and rendering-input correlation
remain distinguishable in the aggregate wire.

The inherited `evaluate()` action converts the named
`MaximumAbsoluteErrorComparison` values into immutable observations, tolerances, and
pass dispositions. The class adds no scientific arithmetic and carries no subject or
projection digest by itself.

## Public import

```python
from ksdft2effmass.periodic1d.fourier_locality import FourierLocalityVerification
```

## Pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Owning module](../index.md)
