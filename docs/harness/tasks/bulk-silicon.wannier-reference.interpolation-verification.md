<!-- Generated from SQLite control state; do not edit. -->
# Wannier interpolation numerical verification

[Task index](index.md) · [Previous](./bulk-silicon.wannier-reference.interface.md) · [Next](./bulk-silicon.wannier-reference.localization.md)

## Status

`blocked`: Essential deterministic numerical-verification Task; blocked by candidate Wannier constructions and independent production QE validation samples.

## Objective

Verify Wannier-interpolated bands and derivatives against direct QE samples on training and withheld domains before freezing the real-space Hamiltonian.

## Parent and prerequisites

- Parent: `bulk-silicon.wannier-reference`
- Depends on: `bulk-silicon.band-edge-characterization.conduction-valley`
- Depends on: `bulk-silicon.band-edge-characterization.symmetry-path`
- Depends on: `bulk-silicon.wannier-reference.localization`

## Authority references

- docs/computational/bulk-silicon-production-program.md
- specification/ksdft2Effmass.numerical-specification.v1.md
- specification/ksdft2Effmass.physical-specification.v1.md

## Authorized scope

- Task kind: numerical verification.
- Inputs are candidate H_W(R), direct QE path/valley/withheld records, energy alignment, band/subspace correspondence, interpolation grid, and accepted metrics.
- Deterministic outputs include QE-versus-Wannier bands, residual panels, edge/gap/valley/mass errors, spread/center/hopping diagnostics, and band-window/disentanglement sensitivity.
- The human owns metric/tolerance disposition, validation domain, correspondence policy, and final BulkSiWannier-v1 acceptance.

## Completion criteria

- Training and withheld samples are separate and representation/energy compatibility is explicit.
- Interpolation, band-edge, derivative, localization, and real-space-decay criteria are evaluated separately.
- Residuals and failed candidates remain retained.

## Exclusions

- This Task executes no scientific program, does not validate the parent PBE physics, and does not treat agreement on one path as Brillouin-zone validation.

## Historical source

No archived source.
