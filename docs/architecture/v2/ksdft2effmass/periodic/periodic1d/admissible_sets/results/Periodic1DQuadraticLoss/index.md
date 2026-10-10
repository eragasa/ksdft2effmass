# `Periodic1DQuadraticLoss`

## Purpose

Immutable analytic proof object for one M3 squared-loss channel.

## Contract

It binds nonempty `channel_id`, optional finite `alignment_angle`, finite two-component
`center`, finite symmetric positive-definite $2\times2$ `quadratic_matrix`, and finite
nonnegative `minimum_squared_loss`. Exact built-in floats are required; Boolean entries
are rejected.

`squared_loss(parameter)` evaluates `EQ-M3-QUADRATIC-003`; `rms_loss(parameter)` returns
the nonnegative square root. Both reject malformed/nonfinite/Boolean parameters.

## Invariants and evidence

Symmetry and positive curvature are checked at construction and independently by the
retained verifier. The aggregate result correlates every quadratic with every sampled
training loss. Adversarial tests shift centers, alter either cross term, break symmetry,
and remove positive curvature.

## Limitations

The quadratic is exact over the continuous declared parameter rectangle only for the
frozen constructed M3 channel and parameter convention. It is not a probabilistic loss
model.
