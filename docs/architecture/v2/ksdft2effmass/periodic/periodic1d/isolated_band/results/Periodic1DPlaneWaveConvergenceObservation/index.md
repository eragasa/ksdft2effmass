# `Periodic1DPlaneWaveConvergenceObservation`

## Purpose and contract

Immutable pair of one positive exact plane-wave cutoff and its nonnegative finite
maximum absolute band-energy error relative to the declared finite reference. The error
must have energy dimensions compatible with the M1 parent.

Construction rejects Boolean/non-integer cutoffs, nonpositive cutoffs, wrong quantity
types, negative/nonfinite errors, and incompatible units when correlated by the
aggregate result.

## Mapping and interpretation

Source: `.../isolated_band/results.py`. The aggregate result requires one observation
per declared cutoff in exact order. This is a finite discretization diagnostic, not a
continuum error bound or uncertainty estimate.
