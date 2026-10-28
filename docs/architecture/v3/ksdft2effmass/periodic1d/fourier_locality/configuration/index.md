# `ksdft2effmass.periodic1d.fourier_locality.configuration`

## Status and responsibility

Implemented direct-calculation configuration module. It owns one immutable typed input
record for the compatible rank-one Fourier-locality calculation.

Like the direct PIAB1D configuration, the record stores only genuine authored
calculation inputs. Fixed algorithm behavior—ordered lowest-band selection, centered
reduced-momentum conventions, Fourier signs, equal fitting weights, inclusive decision
directions, and rendering inventory—belongs to the calculation, verifier, or visualizer
that performs it.

## Public class

- [`Periodic1DFourierLocalityConfiguration`](Periodic1DFourierLocalityConfiguration/index.md)

## Owned controls

- exact controlled-parent identity, integer numerator matrices, and positive common denominator;
- construction mesh extents and selected production extent;
- exact rational evaluation stagger;
- ordinary support-radius inventory;
- sampled-gap and application thresholds; and
- energy, squared-energy, dimensionless, and refinement consistency terms.

## Exclusions

The module constructs no Hamiltonian or operator. It derives the exact-rational
construction and evaluation point inventories as immutable binary64 tuples so every
consumer receives the same coordinates. It executes no eigensolve, transform, fit,
verification, or rendering and owns no schema identity, plot inventory, filesystem path,
or evidence status.

## Related pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Parent package](../index.md)
