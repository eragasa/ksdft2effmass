# `Periodic1DMultibandAlignmentRangeResult`

## Purpose

Immutable M2 evidence for one hopping range across reference, attacked, and pointwise-
aligned channels.

## Fields and invariants

It contains three truncation results and six band-approximation errors: training and
staggered evaluation errors for each channel. All truncations must have the same range,
modulus, internal rank, and energy unit. All errors must target the corresponding common
spectra and coordinate roles.

`maximum_range` is delegated from the reference truncation and is used to correlate the
ordered `range_study`.

## Interpretation

The object separates gauge-locality effects from invariant spectral targets. It does not
contain the globally constrained channel as a complete Fourier model and does not select
an optimal range.
