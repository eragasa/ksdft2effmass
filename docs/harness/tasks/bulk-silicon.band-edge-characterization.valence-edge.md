<!-- Generated from SQLite control state; do not edit. -->
# Local valence-band-edge characterization

[Task index](index.md) · [Previous](./bulk-silicon.band-edge-characterization.symmetry-path.md) · [Next](./bulk-silicon.production-reference.md)

## Status

`blocked`: Conditional calculation/analysis branch for hole, acceptor, or multiband claims; the non-SOC pilot alone cannot establish final silicon hole parameters.

## Objective

Sample and analyze the valence-band maximum sufficiently to choose among directional curvature masses, scalar approximations, and a multiband Luttinger–Kohn description.

## Parent and prerequisites

- Parent: `bulk-silicon.band-edge-characterization`
- Depends on: `bulk-silicon.production-reference.scf`
- External prerequisite: `production_execution_authorization`
- External prerequisite: `valence_sampling_design_approval`
- External prerequisite: `valence_symmetry_evidence`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: calculation.
- Inputs are a compatible scalar-relativistic or fully relativistic SCF parent, local directions/samples, degeneracy tracking, gauge/subspace convention, fit model, and withheld data.
- Retain directional dispersions, curvature tensors or multiband fit records, anisotropy/residual plots, and split-off energy only for a compatible SOC branch.
- The human owns whether the use case requires scalar masses, directional masses, or Luttinger parameters and whether SOC is mandatory for the claim.

## Completion criteria

- Degenerate-band handling and direction conventions are explicit.
- Heavy-hole, light-hole, and split-off labels are used only with supporting symmetry/SOC evidence.
- Fit sensitivity and limitations of scalar parabolic models are retained.

## Exclusions

- Planning does not activate this Task or authorize any external or scientific execution.
- No production parameter or tolerance may be changed outside the owning accepted specification or an explicit human scientific decision.
- Successful execution alone does not establish numerical verification or physical validation.
- A single scalar valence mass is not treated as a complete silicon valence-band model.
- Non-SOC data cannot support final SOC acceptor claims.

## Historical source

No archived source.
