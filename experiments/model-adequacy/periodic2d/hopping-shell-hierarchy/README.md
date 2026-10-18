# Isotropic two-dimensional hopping-shell hierarchy

## Identity and status

This directory is the maintained, publication-independent design home for experiment
family

```text
ksdft2effmass.campaign.model-adequacy.periodic2d.hopping-shell-hierarchy
```

Historical label `HSH-1` is an alias only. The experiment is prospective and unexecuted.
It has no immutable `.v1`, run identity, result, retained evidence, scientific
validation, or publication claim.

The current work closes the exact square-symmetry orbit and nested-support inventory. It
does not freeze the remaining outcome-determining controls.

## Maintained design

- [`protocol.md`](protocol.md) records the selected parent and the boundary between
  selected and open controls.
- [`orbit-support-inventory.md`](orbit-support-inventory.md) fixes the exact operation,
  orbit-member, coefficient, and support-class ordering proposed for the first immutable
  experiment version.
- [`projection-and-loss-design.md`](projection-and-loss-design.md) records the disclosed
  donor-defect inspection and selects prospective source tolerances, projected
  coefficients, common energy shift, coefficient box, and spectral weights.
- [`sample-role-design.md`](sample-role-design.md) selects the objective-construction,
  evaluation, withheld, and locality inventories and their directional isolation.
- [`threshold-design.md`](threshold-design.md) records the disclosed outcome-informed
  study that selects prospective channel thresholds and separation resolution.
- [`execution-structure.md`](execution-structure.md) maps the existing periodic-1D
  experiment package pattern to this experiment's typed definition, Action, result,
  verifier, and serialization modules without adding a nested execution framework.
- [Architecture](../../../../docs/architecture/v2/experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/index.md)
  records scientific, numerical, implementation, and ownership boundaries.
- [Development task](../../../../docs/tasks/dev/experiments/isotropic2d/index.md) tracks
  mutable work toward a versioned experiment.

No Python package implementation, supported public import, schema, canonical input, or
evidence package exists yet. The flat module boundaries are selected, while detailed
class architecture must wait for those source contracts.

## Historical design sources

The publication-bound draft remains unchanged at
`calculations/ICMSEP2026/conference/paper_1/hopping-shell-hierarchy/`. It is a design
donor, not this experiment's maintained identity or evidence directory.

The selected parent donor is the retained synthetic periodic-2D calculation at
`calculations/research-monograph/periodic-2d/`. Reusing its compact result is source
binding, not a new calculation and not material validation.

## Ownership

The future experiment will compose owner capabilities directly rather than introduce a
KSD solver facade.

- PhysKit owns lattice, hopping, energy-unit, Bloch, and supplied-symmetry-operation
  semantics.
- Numerics owns owner-neutral finite Fourier arithmetic, finite-operation/orbit
  enumeration when its exact contract is reviewed, and conservative arithmetic.
- Optimization owns unit-free quadratic minimization, feasibility, support, and
  capability-specific separation mathematics.
- This experiment owns the parent binding, square-symmetry meaning, coefficient and
  support hierarchy, features, weights, thresholds, metric choice, sample roles,
  evidence policy, dispositions, and interpretation.

## Protected boundary

This design authorizes no Quantum ESPRESSO, Wannier90, remote, production, retained, or
confirmatory experiment execution. Passing future software tests will not establish
scientific correctness or material relevance.
