# `ksdft2effmass.periodic1d.fourier_locality.reference`

## Status and responsibility

This module owns immutable independent-reference comparisons, their complete request,
and the request-bound analyzer that reconstructs them. It separates independent
scientific reconstruction from byte-owning verification and authentication.

## Public classes

- [`Periodic1DFourierLocalityIndependentReference`](Periodic1DFourierLocalityIndependentReference/index.md)
- `Periodic1DFourierLocalityIndependentReferenceRequest`
- [`Periodic1DFourierLocalityIndependentReferenceAnalyzer`](Periodic1DFourierLocalityIndependentReferenceAnalyzer/index.md)

## Ownership

The analyzer independently recomputes the declared parent, transform, truncation, fit,
diagnostic, decision, refinement, gap, and verifier-derived projection channels. Its
constructor binds the exact admitted result and projection. Its zero-argument
`execute()` never calls `Periodic1DFourierLocalityAnalyzer` or the production
family-level actions under comparison.

It does not own:

- result-byte admission or the subject digest;
- comparison tolerances or aggregate pass logic;
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
