# S1 Gamma-centered fixed-C42 k-point confirmation evidence

This directory retains compact evidence from the explicitly authorized four-occurrence
SCF packet on provisional
`Si.PrimitiveUnitCell.RightHanded.RelaxedS1`:

- structure byte size: `758`;
- structure SHA-256:
  `d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03`;
- Gamma-centered meshes: K6, K8, K10, K12;
- wavefunction/density cutoffs: `42/336 Ry`;
- executable: QE 7.5 `pw.x`, SHA-256
  `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910`;
- pseudopotential: SSSP 1.3.0 PBE efficiency Si USPP, SHA-256
  `ae3aefd0811f9499dbc4a72f1f9ae02ef4fc7f3568bf6f559b68668719c69e2b`;
- invocation count: exactly four;
- retries: zero; and
- process disposition: all four returned zero, completed, and converged electronically.

The authorization, exact rendered inputs, native stdout/stderr, execution records,
compact result, scripts, and full external artifact inventory are retained here. Large
QE saved-state files remain in the authenticated external root:

`/Users/eugene/projects/ksdft2effmass/si-s1-kpoint-confirmation-c42-gamma-20261031T064459Z`

## Calculation-owned sampled-setting result

Using K12 as the finite reference and the prospectively declared absolute total-energy
tolerance of `1.0 meV/atom` gives:

| Mesh | Absolute difference from K12 (meV/atom) |
| --- | ---: |
| K6 | 11.726746902695595 |
| K8 | 1.8551362573191454 |
| K10 | 0.29027746276710786 |
| K12 | 0.0 |

The calculation-owned rule therefore selects K10 as the smallest passing sampled
mesh on this exact provisional S1 structure. The reusable ProjectKoios policy result
remains separate: it reports that its neighboring-point sustained-tail policy is not
satisfied and proposes K14/K16.

Every occurrence retained QE's
`IEEE_INVALID_FLAG`, `IEEE_DIVIDE_BY_ZERO`, `IEEE_OVERFLOW_FLAG`, and
`IEEE_UNDERFLOW_FLAG` diagnostics after `JOB DONE.`. They are preserved as native
warnings rather than treated as automatic blockers because all four processes
completed with finite energies and reported electronic convergence.

This evidence confirms only the sampled k-point-axis rule at fixed 42/336 Ry. It does
not confirm the cutoff axis, accept a stable structure/settings pair, authorize a
cutoff campaign, or create the downstream parent SCF.
