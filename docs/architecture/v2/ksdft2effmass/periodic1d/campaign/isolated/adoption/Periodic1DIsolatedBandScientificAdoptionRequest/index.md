# `Periodic1DIsolatedBandScientificAdoptionRequest`

## Purpose and status

This implemented row-023 immutable Action request supplies the exact authenticated
campaign definition, historical result, replay aggregate, and optional energy-valued
comparison allowance.

## Correlation and scalar contract

The definition and result must be the exact immutable objects retained by the replay
aggregate; equal identifiers are insufficient. `absolute_tolerance` is either `None` or
an exact finite nonnegative built-in `float`. Booleans, integers, numeric strings,
negative values, NaN, and infinity are rejected.

`None` calculates a separate binary64 allowance for each energy comparison using
machine epsilon, comparison dimension, and reference norm. Reciprocal-coordinate
comparison always owns an independent coordinate-scale allowance. An explicit float
replaces only the energy-valued allowances.

## Claim boundary and evidence

These allowances are software/numerical comparison policy, not rigorous forward-error
bounds, physical uncertainty, validation thresholds, or acceptance criteria. Tests
cover calculated and explicit policies, invalid scalars, and same-identifier source
substitution.
