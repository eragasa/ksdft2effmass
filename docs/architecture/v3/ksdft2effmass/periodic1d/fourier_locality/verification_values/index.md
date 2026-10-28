# `ksdft2effmass.periodic1d.fourier_locality.verification_values`

## Status and responsibility

Module for immutable independently reconstructed verification comparisons. It separates
independent scientific reconstruction from comparison aggregation and subject
authentication.

## Public classes

- [`Periodic1DFourierLocalityIndependentVerification`](Periodic1DFourierLocalityIndependentVerification/index.md)
- [`Periodic1DFourierLocalityIndependentVerifier`](Periodic1DFourierLocalityIndependentVerifier/index.md)

## Ownership

The module owns a direct NumPy reference verifier that independently recomputes the
declared parent, transform, truncation, fit, diagnostic, decision, refinement, and gap
channels as named comparisons. It also correlates every supplied projection field with
its corresponding admitted-result field. It never calls
`Periodic1DFourierLocalityAnalyzer` or its canonical transform, truncation, fit, and
diagnostic actions.

It does not own:

- the result subject digest;
- comparison tolerances or aggregate pass logic;
- file admission;
- rendering; or
- evidence promotion.

## Independence rule

Independent reconstruction may share immutable record classes and low-level NumPy/SciPy
primitives. It must not share the production analyzer or the production family-level
operations whose behavior is under comparison.

## Related pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Parent package](../index.md)
