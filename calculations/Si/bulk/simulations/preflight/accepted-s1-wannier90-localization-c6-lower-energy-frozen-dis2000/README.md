# Accepted-S1 `C6` lower-energy-frozen localization preflight

This directory retains the no-execution preflight for the distinct `C6` Wannier90 3.1.0
localization occurrence. The prepared input changes only the Gamma-origin construction
mesh relative to the provider-eligible `C4` construction while retaining 12 bands, rank
10, the `Si:sp3` plus `Si:l=0:r=2` projections, the outer and frozen windows, and the
successful optimizer controls.

The exact input retains:

- `num_iter = 4000`, `conv_tol = 2e-9 angstrom^2`, and `conv_window = 6`;
- `dis_num_iter = 2000`, dimensionless `dis_conv_tol = 1e-10`,
  `dis_conv_window = 3`, and `dis_mix_ratio = 0.2`;
- `precond = true`, explicit `num_cg_steps = 200`, and the native default
  dimensionless `trial_step = 2.0`;
- no `fixed_step` and no guiding centres; and
- `write_hr` and unitary-matrix output enabled.

The maintained ProjectKoios localization input preparer authenticated the 216-point,
12-band, rank-10, eight-neighbor interface. The input manifest binds 11,202,725 bytes
across the WIN, NNKP, EIG, AMN, and MMN artifacts. The frozen state-count histogram is
129 points with four states, 84 with five, and three with six. No calculator was
invoked and no proposed occurrence root was created.

## Proposed occurrence

- root:
  `/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-c6-lower-energy-frozen-dis2000-v1`
- command: `wannier90.x silicon`
- executable SHA-256:
  `c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd`
- one process, one invocation, zero retries
- timeout: 600 seconds
- retained-byte ceiling: 64 MiB

Eligibility requires return code zero, native completion, converged disentanglement,
converged Wannierisation, no maximum-iteration warning, the declared HR and unitary
outputs, unitary/isometry residuals at most `1e-8`, k-point agreement within `1e-10`, and
Hamiltonian Hermiticity residual at most `1e-8 eV`. These are provider-eligibility
conditions, not scientific adequacy criteria.

## Identities

| Artifact | SHA-256 |
|---|---|
| prepared `silicon.win` | `0d5b693972309245f0ce04fca42e8806a8c33017af7d0e184424dec0b429694c` |
| localization input manifest | `2c7bc1b1cef5ae631f582849d5b18e12b79f6023b44d7c3fe759ce0c731099f7` |
| frozen-window analysis | `9930f430e81c3a920c76ac47911e52d03a41a5c62d994773e8b636ee9b8d6f63` |
| campaign preflight | `ab3025b9ec9a8a053b03f562a3b7134387b281517197884a45c1f3b2fac2ea4e` |
| authorization request | `7ed68715f0376b61999610343fa0833d7c04795280e9690088658eed8b468431` |

## Authorization boundary

Status: **authorization consumed by one occurrence**.

The immutable request retains its original `authorization_granted: false`; the separate
consumed-authorization record is retained with the occurrence. Native Wannier90 returned
zero, but the provider rejected the output because disentanglement did not converge by
iteration 2000. Evidence is retained under
[`../../evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-localization-c6-lower-energy-frozen-dis2000-blocked/`](../../evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-localization-c6-lower-energy-frozen-dis2000-blocked/).
A retry, budget extension, `C8`, `C12`, direct-parent confirmation, component-operator
construction, and Slater--Koster reduction are not authorized.
