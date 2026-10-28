# `Periodic1DFourierLocalityVisualizationData`

## Responsibility

Immutable authenticated projection containing exactly the scientific values
required by both native figures.

`Periodic1DFourierLocalityVerifier` constructs this projection from the admitted result.
Its independent reference implementation separately reconstructs and compares the
underlying scientific channels, checks every projection field against the corresponding
admitted-result field, and binds the projection's canonical bytes into verification. No
public constructor accepts an unverified producer result in the rendering lifecycle.

## Projection content

- evaluation lowest/adjacent bands, evaluation and production sampled-gap vectors,
  sampled minimum, and gap threshold;
- complete production hopping coefficients and support-indexed omitted norms;
- per-mesh interpolation maxima and adjacent-mesh refinement maxima;
- per-mesh truncation, mediated-total, and direct-total maximum series;
- per-mesh finite error--complexity masks and near-tie flags;
- application threshold, every mesh's first passage, and every sustained flag; and
- direct/mediated coefficient and construction-sample route defects.

## Public import

```python
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityVisualizationData,
)
```

## Pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Owning module](../index.md)
