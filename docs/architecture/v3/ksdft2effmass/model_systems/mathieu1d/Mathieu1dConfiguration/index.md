# `Mathieu1dConfiguration`

## Status and responsibility

Implemented immutable typed record in
`python/src/ksdft2effmass/model_systems/mathieu1d/configuration.py`.

The record is the single owner of the finite parent, sampling, range, fitting, and
tolerance controls consumed by `Mathieu1dAnalyzer`.

## Correlated controls

- period, reciprocal vector, recoil energy, and one-harmonic potential;
- ordered plane-wave cutoffs and larger finite reference cutoff;
- ordered periodic finite-difference grid sizes;
- sampled parent momenta and spectral prefix;
- selected band and even complete training-mesh size;
- disjoint half-open evaluation coordinates;
- symmetric hopping ranges and positive training weights; and
- coordinate, reconstruction, Hermiticity, Parseval, and imaginary tolerances.

`training_reduced_momenta` is derived as `-1/2 + j/N`; it is not serialized a second
time.

## Invariants

- Public numeric values use exact built-in types; Booleans and numeric strings fail.
- All floating values are finite.
- `period * reciprocal_vector` equals `2π` within the declared tolerance.
- Ordered inventories are nonempty, unique, and strictly increasing.
- The represented bases contain every requested band.
- Ranges are smaller than half the even training mesh.
- Training and evaluation coordinates are disjoint within coordinate tolerance.
- Decoding invokes the same constructor invariants as direct construction.

## Public import

```python
from ksdft2effmass.model_systems.mathieu1d import Mathieu1dConfiguration
```

## Claim boundary

Configuration validity establishes a coherent finite request only. It does not establish
that a range, representation, or sampled gap is scientifically adequate.
