# `Periodic1DConstrainedAdmissibleSetCalculationDefinition`

## Purpose

Immutable complete control record for one M3 calculation.

## Inputs

It binds calculation identity, exact rank-two M2 baseline, a continuous rectangular
domain in energy-shift ratio and splitting scale, finite ordered alignment angles,
energy normalization scale, compatible and
separated thresholds, prospective compatible witness, locality ranges, separation
resolution, and quadratic/final verification tolerances.

## Invariants

Bounds are finite strictly increasing built-in-float pairs; the parameter domain is the
closed Cartesian product of the two intervals and includes all required
witness/certificate points. Angles and ranges are finite, unique, and ordered. The loss
scale is positive and compatible with the M2 parent energy unit. Case identities differ.
Resolution is nonnegative; retained verification contracts require strictly positive
quadratic and final tolerances. The composed M2 rank is exactly two.

`contains(parameter)` rejects malformed/Boolean/nonfinite inputs and tests domain
membership. `parent_model` returns the composed baseline parent.

## Evidence and limitations

Composition, non-rank-two rejection, domain Boolean rejection, and deterministic input
materialization are directly tested. The definition freezes a finite synthetic family;
it does not define a universal admissible set.
