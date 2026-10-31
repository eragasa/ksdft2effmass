# Gamma-centered right-handed silicon k-point campaign

## Status

This directory retains compact evidence from four authorized Quantum ESPRESSO 7.5 SCF
occurrences on the right-handed provisional structure. The only varied coordinate is
the Gamma-centered cubic k-point mesh. No occurrence was retried.

The exact external evidence root is:

```text
/Users/eugene/projects/ksdft2effmass/
  si-kpoint-gamma-sssp-qe75-right-handed-20261031T054832Z/
```

[`external-artifact-inventory.json`](external-artifact-inventory.json) authenticates
the full external state. Large wavefunction, density, and saved-state files remain
outside Git.

## Bound settings

- structure: `Si.PrimitiveUnitCell.RightHanded`, SHA-256
  `7bef37dfe20ce58a137de942ec1fa0aa50d6e7049b0265790f12171bc834529a`;
- SSSP 1.3.0 PBE efficiency Si USPP, SHA-256
  `ae3aefd0811f9499dbc4a72f1f9ae02ef4fc7f3568bf6f559b68668719c69e2b`;
- QE 7.5 `pw.x`, SHA-256
  `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910`;
- wavefunction and density cutoffs: 48 and 384 Ry;
- meshes: K6, K8, K10, and K12;
- shift: `(0,0,0)`; and
- fixed occupations, spatial symmetry, and time reversal.

## Observations and selection

| Mesh | Irreducible points | Energy (eV/atom) | Difference from K12 (meV/atom) |
| --- | ---: | ---: | ---: |
| K6 | 16 | -155.36365365347790 | 11.912600670769 |
| K8 | 29 | -155.37369064132320 | 1.875612825472 |
| K10 | 47 | -155.37527665697056 | 0.289597178124 |
| K12 | 72 | -155.37556625414868 | 0 |

[`kpoint-selection.json`](kpoint-selection.json) applies
`kpoints_convergence_atol = 1.0 meV/atom`, zero relative tolerance, and K12 as the
densest sampled reference. The smallest passing mesh is **K10**.

ProjectKoios separately reported that its two-consecutive-tail-increment policy did not
pass because the K8-to-K10 change exceeds 1 meV/atom. That workflow assessment is
retained but is not the calculation-owned mesh-selection rule requested here.

All SCFs completed in five electronic iterations. QE did not report a negative lattice
determinant. Every occurrence retained the same four IEEE flags described in the
campaign result, so this finite-grid selection is not production acceptance.
