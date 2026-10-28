# `Mathieu1dCalculationResult`

Implemented immutable root result for one direct Mathieu1D calculation.

It binds execution metadata and the exact `Mathieu1dConfiguration` to refinement, band
samples, complete transform, and the ordered range inventory. The root constructor owns
cross-section checks: authored coordinates and ranges, represented shapes, complete
representatives, candidate lengths, and configured tolerances must all agree.

```python
from ksdft2effmass.model_systems.mathieu1d import Mathieu1dCalculationResult
```

Canonical typed JSON bytes are the verifier subject. The root result is calculated data,
not independent verification or sealed evidence.
