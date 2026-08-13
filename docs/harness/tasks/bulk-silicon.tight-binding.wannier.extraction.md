<!-- Generated from SQLite control state; do not edit. -->
# Wannier tutorial Hamiltonian extraction

[Task index](index.md) · [Previous](./bulk-silicon.tight-binding.wannier.bridge.md) · [Next](./bulk-silicon.wannier-reference.md)

## Status

`superseded`: Never-launched tutorial-reproduction Hamiltonian-extraction identity, superseded by the inactive production Stage 03 Task bulk-silicon.wannier-reference.localization. Supersession does not activate the replacement or authorize execution.

## Objective

Reproduce an authorized Wannier90 silicon tutorial and extract its represented Wannier-basis Hamiltonian.

## Parent and prerequisites

- Depends on: `bulk-silicon.tight-binding.wannier.bridge`
- External prerequisite: `wannier_tutorial_execution_authorization`
- Superseded by: `bulk-silicon.wannier-reference.localization`

## Authority references

- docs/computational/ksdft2effmass.computational.bootstrap.md
- harness/reports/simulation-first-task-migration.md

## Authorized scope

- Execute only the approved Wannier90 tutorial stages.
- Retain immutable request, result, failure, and artifact identities.
- Extract the real-space Hamiltonian with explicit basis, centers, lattice, unit, energy reference, settings, and parent provenance.

## Completion criteria

- The represented Hamiltonian is reproducible from retained tutorial inputs and artifacts.
- Localization and disentanglement settings are retained.
- Process and numerical failures remain explicit.
- Any truncation is separately represented.

## Exclusions

- No execution occurs without separate authorization.
- Wannierization is not described as a low-rank approximation.
- The extracted Hamiltonian is not automatically an impurity operator.
- No basis, gauge, unit, geometry, or energy-zero transformation is hidden.

## Historical source

No archived source.
