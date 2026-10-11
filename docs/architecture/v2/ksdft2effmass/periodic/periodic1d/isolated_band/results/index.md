# `ksdft2effmass.periodic1d.isolated_band.results`

## Purpose and status

Implemented immutable result contracts for every M1 evidence layer.

## Public contract

- [`Periodic1DPlaneWaveConvergenceObservation`](Periodic1DPlaneWaveConvergenceObservation/index.md)
- [`Periodic1DFiniteDifferenceConvergenceObservation`](Periodic1DFiniteDifferenceConvergenceObservation/index.md)
- [`Periodic1DIsolatedBandRangeResult`](Periodic1DIsolatedBandRangeResult/index.md)
- [`Periodic1DIsolatedBandCalculationResult`](Periodic1DIsolatedBandCalculationResult/index.md)

## Ownership and invariants

These records correlate results with the exact definition, reference spectrum,
training/evaluation target identity, transform mesh, units, ordered ranges, and diagnostic
owners. They reject compatible-shaped but unrelated objects. They do not perform a new
scientific calculation or acceptance decision.

## Mapping and evidence

Source: `python/src/ksdft2effmass/periodic1d/isolated_band/results.py`.
Construction is exercised transitively by every M1 execution, determinism, serializer,
and verifier test.

## Limitations

Immutability is operational for the dataclass graph maintained by these records; it
does not make mutable third-party arrays globally immutable outside their owning domain
objects.
