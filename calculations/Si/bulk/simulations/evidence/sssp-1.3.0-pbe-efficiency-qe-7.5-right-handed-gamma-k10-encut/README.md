# Gamma-centered K10 silicon cutoff campaign

## Status

This directory retains compact evidence for wavefunction-cutoff selection on the exact
right-handed, Gamma-centered K10 branch. Five new Quantum ESPRESSO 7.5 SCFs were
executed once each at 30, 36, 42, 54, and 60 Ry. The exact 48 Ry K10 observation was
reused from the preceding Gamma-centered k-point campaign; it was not rerun.

The exact external evidence root for the five new occurrences is:

```text
/Users/eugene/projects/ksdft2effmass/
  si-encut-gamma-k10-sssp-qe75-right-handed-20261031T054930Z/
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
- fixed mesh: Gamma-centered K10, shift `(0,0,0)`;
- density-cutoff ratio: 8; and
- fixed occupations, spatial symmetry, and time reversal.

## Observations and selection

| Wavefunction cutoff (Ry) | Density cutoff (Ry) | Energy (eV/atom) | Difference from 60 Ry (meV/atom) |
| ---: | ---: | ---: | ---: |
| 30 | 240 | -155.37386942013083 | 1.629213723021 |
| 36 | 288 | -155.37446745837207 | 1.031175481785 |
| 42 | 336 | -155.37486644532288 | 0.632188530972 |
| 48 | 384 | -155.37527665697056 | 0.221976883296 |
| 54 | 432 | -155.37544291854053 | 0.055715313323 |
| 60 | 480 | -155.37549863385385 | 0 |

[`encut-selection.json`](encut-selection.json) applies
`encut_convergence_atol = 1.0 meV/atom`, zero relative tolerance, and 60 Ry as the
densest sampled reference. The smallest passing wavefunction cutoff is **42 Ry**, with
corresponding density cutoff **336 Ry**.

ProjectKoios' separate adaptive tail assessment did not pass because the executed
five-point recipe omitted the already-retained 48 Ry point. It is not the selection
rule and does not include the combined six-point record in `encut-selection.json`.

All five new SCFs completed in five electronic iterations. Every occurrence retained
the same four IEEE flags described in the campaign result. The selected values are a
finite sampled-cutoff result, not production acceptance or independent validation.
