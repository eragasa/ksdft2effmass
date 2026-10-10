# `Periodic1DFiniteDifferenceConvergenceObservation`

## Purpose and contract

Immutable pair of one finite-difference point count and its maximum absolute band-energy
error relative to the declared plane-wave reference. `point_count` is an exact built-in
integer of at least three; the error is a finite nonnegative energy quantity.

## Correlation and interpretation

`Periodic1DIsolatedBandCalculationResult` requires exact order and identity with the
definition's `finite_difference_points`. Source:
`.../isolated_band/results.py`. This finite cross-discretization comparison is neither a
continuum theorem nor material validation.
