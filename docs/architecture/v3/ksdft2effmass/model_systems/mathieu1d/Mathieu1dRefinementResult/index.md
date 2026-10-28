# `Mathieu1dRefinementResult`

## Status and responsibility

Implemented immutable result section in
`python/src/ksdft2effmass/model_systems/mathieu1d/result.py`.

It correlates one parent momentum inventory and finite reference spectrum with ordered
plane-wave-cutoff and periodic finite-difference-grid discrepancy vectors.

## Invariants

- Every quantity is explicitly `Unitless()`.
- Reference-spectrum rows match the parent coordinate inventory.
- Each discrepancy vector matches its ordered representation inventory.
- Cutoffs and grid sizes are positive and strictly increasing.
- Discrepancies are finite and nonnegative.

## Public import

```python
from ksdft2effmass.model_systems.mathieu1d import Mathieu1dRefinementResult
```

## Claim boundary

The discrepancies compare finite representations at common sampled momenta and band
indices. They are not continuum errors, convergence rates, or uncertainties.
