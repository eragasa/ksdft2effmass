# `Mathieu1dTransformResult`

Implemented immutable section for the complete finite Fourier transform.

It owns the centered representative inventory, scalar complex hopping coefficients,
reconstructed training values, and reconstruction and Hermiticity diagnostics. Its
constructor requires the pairing and missing-opposite inventories to partition the
representatives and derives each pass disposition from the stored defect and tolerance.

```python
from ksdft2effmass.model_systems.mathieu1d import Mathieu1dTransformResult
```

This class records a finite-mesh transform. Reconstruction and conjugate pairing do not
establish continuum localization or a scientifically adequate hopping range.
