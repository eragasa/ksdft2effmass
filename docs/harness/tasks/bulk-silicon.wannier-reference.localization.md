<!-- Generated from SQLite control state; do not edit. -->
# Production Wannier construction and localization

[Task index](index.md) · [Previous](./bulk-silicon.wannier-reference.interpolation-verification.md) · [Next](./bulk-silicon.wannier-reference.uniform-nscf.md)

## Status

`blocked`: Essential protected Wannier90 calculation/analysis Task; blocked by complete interface artifacts and approved projection/window decisions.

## Objective

Construct candidate localized valence-plus-low-conduction Wannier representations and assess convergence and sensitivity without hiding gauge or disentanglement choices.

## Parent and prerequisites

- Parent: `bulk-silicon.wannier-reference`
- Depends on: `bulk-silicon.wannier-reference.interface`
- External prerequisite: `wannier90_execution_authorization`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: calculation.
- Inputs are complete interface artifacts, target rank, projections, frozen/outer windows, iteration/convergence settings, symmetry policy, and candidate sensitivity design.
- Retain .wout/.chk, centers, spreads, unitary/subspace data where available, real-space Hamiltonian, hopping decay, candidate identities, warnings/failures, and localization/window diagnostics.
- The human owns projections, windows, rank, symmetry/gauge constraints, localization and disentanglement acceptance, and candidate selection.

## Completion criteria

- Candidate constructions are reproducible and sensitivity to projections/windows/grid is quantified.
- Centers, spreads, disentanglement behavior, and hopping decay are retained without hidden truncation.
- One candidate may proceed only after the human-owned scientific decisions are explicit.

## Exclusions

- Planning does not activate this Task or authorize any external or scientific execution.
- No production parameter or tolerance may be changed outside the owning accepted specification or an explicit human scientific decision.
- Successful execution alone does not establish numerical verification or physical validation.
- Small spread is not sufficient evidence of band-edge fidelity or physical validation.

## Historical source

No archived source.
