# `Periodic1DIsolatedBandRangeResult`

## Purpose

Immutable correlated evidence for one declared symmetric hopping range.

## Fields and invariants

The record binds mediated `truncation`, training and evaluation
`BandApproximationErrorResult1D` objects, `HoppingParsevalResult1D`, direct
least-squares fit, direct-versus-mediated model comparison, and scalar band-shape
diagnostics. All objects must share range, coordinate roles, units, target identities,
and finite representative conventions.

`maximum_range` delegates to the truncation result and is the sorting/correlation key.

## Failures and evidence

Construction rejects wrong exact types and any incompatible range, target, mesh, unit,
or diagnostic identity. M1 execution and verification tests exercise all paths.

## Limitations

This record compares two finite-range constructions at one range. It does not choose an
optimal range or quantify model uncertainty.
