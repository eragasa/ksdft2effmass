# `ksdft2effmass.periodic1d.admissible_sets.definition`

## Purpose and status

Implemented immutable M3 controls: per-case thresholds, composed rank-two M2 baseline,
finite two-parameter domain, three evaluation coordinates, separation resolution, and
quadratic/verification tolerances.

## Public contract

- [`Periodic1DAdmissibleSetThresholds`](Periodic1DAdmissibleSetThresholds/index.md)
- [`Periodic1DConstrainedAdmissibleSetCalculationDefinition`](Periodic1DConstrainedAdmissibleSetCalculationDefinition/index.md)

`contains(parameter)` performs strict finite-valued continuous-domain membership, and `parent_model`
returns the exact M2 parent.

## Ownership and dependencies

This module owns M3 controls and validation only. It composes M2; it does not execute
M2/M3, fit quadratics, choose witnesses after evaluation, or certify separation.

## Mapping and evidence

Source: `python/src/ksdft2effmass/periodic1d/admissible_sets/definition.py`.
Tests cover rank-two composition, Boolean rejection, deterministic configuration
materialization, and exact domain membership.

## Limitations

Thresholds are prospective pedagogical benchmark controls, not physical or
uncertainty-calibrated tolerances.
