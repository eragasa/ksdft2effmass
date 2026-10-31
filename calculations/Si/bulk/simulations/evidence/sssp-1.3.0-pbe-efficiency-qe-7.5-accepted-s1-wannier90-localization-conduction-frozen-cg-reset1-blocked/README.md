# Blocked conduction-frozen CG-reset-1 occurrence

This directory retains the single authorized occurrence that changed only
`num_cg_steps` from its verified native default 5 to 1. The executable returned zero
and printed its native completion message, but ProjectKoios classified the output as
ineligible because Wannierisation again lacked its convergence-criteria-satisfied
message.

## Default verification

`cg-reset-default-verification.json` authenticates the source default, confirms that the
unguided predecessor omitted the control, and records the predecessor WOUT value 5.
The successor retains the default parabolic line search and `trial_step = 2.0` while
resetting the Fletcher--Reeves conjugate direction more frequently.

## Convergence disposition

- Disentanglement reproduced convergence at iteration 531.
- Its final dimensionless fractional delta was `9.017e-11`, below `1.0e-10`.
- Wannierisation reached 1000 iterations without convergence.
- Its final spread change was `-1.17e-2 angstrom^2`, versus the absolute
  `1.0e-10 angstrom^2` threshold.
- The final total spread was `57.056694066 angstrom^2`, substantially higher than the
  default-CG-reset comparator's `37.128984231 angstrom^2`.
- Late excursions persisted. More frequent CG resets did not resolve this
  conduction-frozen localization problem.

The generated Hamiltonian remains diagnostic output and is not accepted.

## Parsed diagnostic outputs

Maintained bounded ProjectKoios parsers verified:

- 64 rank-10 gauge matrices, maximum unitarity residual
  `1.7953805109272025e-10`;
- 64 `12 x 10` disentanglement matrices, maximum isometry residual
  `1.4772050249689528e-10`; and
- 93 rank-10 Hamiltonian representatives, complete negative-representative pairing,
  and `0.0 eV` maximum Hermiticity residual.

## Provenance

The external occurrence remains at:

```text
/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-conduction-frozen-cg-reset1-20261031T092409Z
```

`external-artifact-inventory.json` authenticates 37 files totaling 13,703,397 bytes.
The retained `campaign-result.json` SHA-256 is
`1ed4f81452200f222e823947586b2f4fe95fa03fa8027325aef0a3a98e83e593`.

The authorization is consumed. No retry is authorized.
