# `ksdft2effmass.periodic1d.isolated_band.calculate`

## Purpose and status

Implemented M1 producer module. It composes maintained parent constructors,
Fourier/hopping transforms, finite-range reduction routes, and diagnostics into one
deterministic in-process calculation.

## Public contract

- [`Periodic1DIsolatedBandCalculator`](Periodic1DIsolatedBandCalculator/index.md)

The public `execute(definition)` method accepts the exact M1 definition type and returns
one immutable correlated result. Private methods own nontrivial orchestration: parent
spectra, physical-coordinate conversion, range studies, scalar operator conversion, and
maximum-error evaluation.

## Ownership and dependencies

The calculator owns sequencing and correlation, not the reusable numerical algorithms
it composes. It performs no external execution and no file I/O.

## Mapping and evidence

Source: `python/src/ksdft2effmass/periodic1d/isolated_band/calculate.py`.
Algorithm details are in [implementation](../implementation.md) and direct evidence is
mapped in [testing](../testing.md).

## Limitations

The output is bounded synthetic numerical evidence. Successful execution does not
establish continuum convergence, physical isolation, material validity, or acceptance.
