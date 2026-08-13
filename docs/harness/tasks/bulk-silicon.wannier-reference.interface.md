<!-- Generated from SQLite control state; do not edit. -->
# Production QE–Wannier90 interface artifacts

[Task index](index.md) · [Previous](./bulk-silicon.wannier-reference.md) · [Next](./bulk-silicon.wannier-reference.interpolation-verification.md)

## Status

`blocked`: Essential extraction/interface Task; blocked by the accepted uniform NSCF state and separate interface execution authorization.

## Objective

Generate and inventory the exact Wannier90 preprocessing and pw2wannier90.x interface artifacts for the approved production subspace.

## Parent and prerequisites

- Parent: `bulk-silicon.wannier-reference`
- Depends on: `bulk-silicon.wannier-reference.uniform-nscf`
- External prerequisite: `wannier_interface_execution_authorization`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: extraction.
- Inputs are the approved .win design, wannier90 -pp neighbor data, uniform NSCF state, parent manifest, executable compatibility identities, and pw2wannier90 request.
- Expected external artifacts include .nnkp, .amn, .mmn, .eig and approved optional spin/position/interface files; retain compact manifests, schemas, roles, checksums, settings, and failures.
- Deterministic outputs are interface compatibility and completeness reports; the human owns projections, windows, optional artifacts, and compatibility disposition.

## Completion criteria

- Required versus optional artifacts and their producers are explicit.
- QE, pw2wannier90, and Wannier90 identities/formats are compatible and the complete lineage is reproducible.
- No interface artifact is confused with projwfc.x output or a neutral periodic record.

## Exclusions

- Planning does not activate this Task or authorize any external or scientific execution.
- No production parameter or tolerance may be changed outside the owning accepted specification or an explicit human scientific decision.
- Successful execution alone does not establish numerical verification or physical validation.
- Interface success does not establish localization, interpolation accuracy, or operator acceptance.

## Historical source

No archived source.
