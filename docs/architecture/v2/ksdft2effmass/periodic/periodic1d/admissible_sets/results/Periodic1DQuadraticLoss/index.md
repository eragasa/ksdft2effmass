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

## Channel and common-primitive boundary

The M3 wrapper identifies the represented function as spectral $L_E^2$ or one
alignment-constrained operator $L_H^2$. Its `channel_id`, `alignment_angle`, and exact
shift/splitting coordinate convention therefore remain M3-owned.

The generic facade now exists at
`projectkoios.optimization.adapters.PositiveDefiniteQuadraticLoss` in exact-pinned owner
commit `ec3d290…`. A later M3 implementation may delegate completed-square validation
and evaluation through that facade while preserving this class's constructor, supported
import, M3-specific fields, and schema-v1 wire identity. This class does not
become an alias or subclass of the external type. The retained verifier continues
independent formula reconstruction.

## Invariants and evidence

Symmetry and positive curvature are checked at construction and independently by the
retained verifier. The aggregate result correlates every quadratic with every sampled
training loss. Adversarial tests shift centers, alter either cross term, break symmetry,
and remove positive curvature.

## Limitations

The quadratic is exact over the continuous declared parameter rectangle only for the
frozen constructed M3 channel and parameter convention. It is not a probabilistic loss
model.
