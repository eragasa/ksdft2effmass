# `Periodic1DAdmissibleSetParameterEvaluation`

## Purpose

Immutable evaluation of one identified M3 parameter and selected global rotation.

## Fields and roles

The record binds exact `role`, finite two-component `parameter`, declared
`selected_alignment_angle`, training and evaluation spectral/operator RMS losses, and
ordered locality summaries. Supported retained roles are
`compatible-common-witness`, `separated-spectral-boundary`, and
`separated-operator-boundary`.

## Invariants

All numeric values are finite nonnegative built-in floats where appropriate; Booleans
are rejected. Locality ranges are unique/increasing. Aggregate construction verifies
parameter-domain membership, best-angle selection, quadratic agreement, and role-specific
identity.

## Evidence and limitations

The independent verifier reconstructs each role and a wrong role contributes defect
`1.0`. Evaluation data are diagnostic and cannot alter thresholds or dispositions.
