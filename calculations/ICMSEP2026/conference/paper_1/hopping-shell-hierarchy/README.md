# Certified two-dimensional hopping-shell hierarchy plan

This directory contains the draft plan for a controlled synthetic experiment
that would replace the current generic two-dimensional summary figure in
Conference Paper 1 V2 if, and only if, the experiment is prospectively frozen,
executed, independently verified, and accepted for that bounded use.

Working calculation identity:

`icmsep2026.paper1.periodic2d.hopping-shell-hierarchy.v1`

Working planning label: **HSH-1** (hopping-shell hierarchy 1). It is not an
extension or amendment of the sealed M3 evidence and does not conflict with the
separate draft M4 common-space calculation. A final manuscript number is not
assigned by this planning record.

## Status

**Draft and unexecuted.** No result, separation bound, common witness, critical
shell, or figure is reported. No Quantum ESPRESSO, Wannier90, or other external
scientific calculator is required or authorized by this plan.

## Intended role

The experiment tests a nested sequence of hopping-support model classes against
one fixed spectral objective and one fixed real-space operator objective. It is
designed to determine the smallest tested shell class for which one explicit
model satisfies both criteria, while using certified positive lower bounds to
exclude smaller classes where possible.

The experiment is planned as an upgrade of V2 Figure `fig:2d`, currently sourced
from:

`calculations/research-monograph/periodic-2d/summary.png`

The existing two-dimensional parent, coupling, reconstruction, and interpolation
controls would remain evidence and move to the supplementary discussion. The
new hierarchy figure must not replace M3's admissible-set geometry, the
composite-frame gauge-locality figure, or either silicon preview figure.

## Draft software architecture

The prospective package, module, class, scientific, numerical, implementation,
and testing boundaries are documented in the
[HSH-1 experiment architecture](../../../../../docs/architecture/v2/experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/index.md).
Those pages describe target ownership only: no listed Python module, supported
export, test evidence, or Sphinx API exists yet.

## Planned package

Only `README.md` and `protocol.md` exist in this calculation directory at the
planning stage. A later implementation must add, before protocol freeze:

- an editable configuration and deterministic input builder;
- a canonical generated input document;
- typed producer and result definitions;
- a standalone verifier that does not import the producer;
- focused software and adversarial tests;
- source and source-parent correlation manifests; and
- a prospective freeze record.

Only after those gates may a local synthetic run create result, verification,
figure-data, figure, report, and software records. Thresholds, weights, and a
visually favorable transition must not be chosen after confirmatory execution.

See [`protocol.md`](protocol.md) for the complete proposed design and unresolved
pre-freeze decisions.
