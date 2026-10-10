# `Periodic1DAdmissibleSetCaseResult`

## Purpose

Immutable proof outcome for one named M3 threshold pair.

## Fields

It binds thresholds, disposition, feasible operator-angle subset, optional common
witness, spectral and operator certificate evaluations, separation lower/upper bounds,
and declared resolution.

## Disposition invariants

`compatible-witness` requires a non-null common witness satisfying both thresholds.
`certified-separated` requires no common witness and a lower bound exceeding resolution
within tolerance. `unresolved` forbids unsupported stronger claims. Bounds are finite,
nonnegative, ordered, and correlated with certificate points and the analytic
quadratics. Feasible angles must be an ordered subset of the definition.

## Evidence and limitations

Execution and independent verification tests exercise compatible and separated paths.
The certificate remains limited to the continuous frozen rectangle, finite angle
inventory, and unclipped-ellipse premises; the enum is not a material verdict.
