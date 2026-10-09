# `solidstate/wignerseitz`

## Responsibility

This package owns finite Wigner–Seitz represented-operator inventories, residue lifting,
interpolation, and Cartesian derivatives. Python implementation:
`ksdft2effmass.solid_state.wignerseitz`.

The package does not decode native Wannier90 files, infer inventory identity from array
shape, select a retained space, establish interpolation convergence, or validate a
physical interpretation.

Tests mirror the implementation namespace under
`python/tests/software_verification/ksdft2effmass/solid_state/wignerseitz/` and import
from the implementation owner rather than the root `solid_state` facade.

## Scientific reference and claim boundary

The name follows E. Wigner and F. Seitz, “On the Constitution of Metallic Sodium,”
*Physical Review* 43(10), 804–810 (1933),
[doi:10.1103/PhysRev.43.804](https://doi.org/10.1103/PhysRev.43.804). The bibliographic
metadata was checked against the Crossref DOI record on 2026-10-07. The citation
preserves the provenance of the Wigner–Seitz name and cell construction; it does not
validate this implementation's finite-mesh representatives, replica selection,
normalization, interpolation accuracy, or scientific application.

The authoritative mathematical contract and complete citation provenance are in
[`ksdft2Effmass.wigner-seitz-operator-interpolation.v1.md`](../../../../../../specification/ksdft2Effmass.wigner-seitz-operator-interpolation.v1.md).
