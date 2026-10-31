# S1 Gamma-centered K10 cutoff confirmation evidence

This directory retains compact evidence from the explicitly authorized five new SCF
occurrences on provisional
`Si.PrimitiveUnitCell.RightHanded.RelaxedS1` at Gamma-centered K10. The exact
previous K10/C42 occurrence was reused as instructed and was not rerun.

- structure byte size: `758`;
- structure SHA-256:
  `d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03`;
- new wavefunction cutoffs: 30, 36, 48, 54, and 60 Ry;
- reused wavefunction cutoff: 42 Ry;
- density-cutoff ratio: 8:1;
- executable: QE 7.5 `pw.x`, SHA-256
  `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910`;
- new invocation count: exactly five;
- C42 invocation count in this packet: zero;
- retries: zero; and
- process disposition: all five new occurrences returned zero, completed, and
  converged electronically.

The full external artifact root is:

`/Users/eugene/projects/ksdft2effmass/si-s1-cutoff-confirmation-k10-gamma-20261031T065302Z`

## Calculation-owned sampled-setting result

Using C60 as the finite reference and the declared `1.0 meV/atom` tolerance gives:

| Wavefunction cutoff (Ry) | Density cutoff (Ry) | Difference from C60 (meV/atom) |
| ---: | ---: | ---: |
| 30 | 240 | 1.5686683886144692 |
| 36 | 288 | 1.0103587713103934 |
| 42 | 336 | 0.6180386100993474 |
| 48 | 384 | 0.211364442662898 |
| 54 | 432 | 0.05462685788870658 |
| 60 | 480 | 0.0 |

The calculation-owned rule selects 42/336 Ry as the smallest passing sampled cutoff
pair on exact S1. Combined with the separately confirmed K10 axis, this reproduces the
provisional setting tuple used to relax S1. It creates a candidate stable pair for a
separate scientific disposition; it does not automatically accept that pair.

The reusable ProjectKoios neighboring-point sustained-tail policy remains separate and
reports that its generic policy is not satisfied. All new occurrences retained QE's
four IEEE flag classes after successful completion; these remain diagnostics rather
than automatic blockers in the absence of non-finite results or failed convergence.

This evidence does not authorize a downstream parent SCF and is not reused as that
parent occurrence.
