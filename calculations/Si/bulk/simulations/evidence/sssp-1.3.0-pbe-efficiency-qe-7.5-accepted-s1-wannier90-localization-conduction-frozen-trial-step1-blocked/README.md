# Blocked conduction-frozen trial-step-1 occurrence

This directory retains the single authorized one-variable occurrence that explicitly
changed Wannier90's dimensionless `trial_step` from the effective native default `2.0`
to `1.0`. The executable returned zero and printed its completion message, but
ProjectKoios classified the output as ineligible because Wannierisation again lacked
its convergence-criteria-satisfied message.

## Default verification

`trial-step-default-verification.json` records that:

- Wannier90 3.1.0 source sets `trial_step = 2.0_dp`;
- the unguided 1000-iteration predecessor omitted both `trial_step` and `fixed_step`;
- that predecessor's WOUT reported an effective trial step of `2.000`; and
- this successor alone explicitly sets the dimensionless value `1.0`.

Thus the scientific comparison is `2.0` default versus explicit `1.0`, not an unknown
prior setting.

## Convergence disposition

- Disentanglement reproduced convergence at iteration 531.
- Its final dimensionless fractional delta was `9.017e-11`, below `1.0e-10`.
- Wannierisation reached 1000 iterations without convergence.
- Its final spread change was `-3.50e-3 angstrom^2`, versus the absolute
  `1.0e-10 angstrom^2` threshold.
- The final total spread was `43.536848529 angstrom^2`, higher than the default-step
  comparator's `37.128984231 angstrom^2`.
- Late excursions persisted. Halving the parabolic trial step did not resolve this
  conduction-frozen localization problem.

The generated Hamiltonian remains diagnostic output and is not accepted.

## Parsed diagnostic outputs

Maintained bounded ProjectKoios parsers verified:

- 64 rank-10 gauge matrices, maximum unitarity residual
  `1.6702839111815138e-10`;
- 64 `12 x 10` disentanglement matrices, maximum isometry residual
  `1.4772050249689528e-10`; and
- 93 rank-10 Hamiltonian representatives, complete negative-representative pairing,
  and `0.0 eV` maximum Hermiticity residual.

## Provenance

The external occurrence remains at:

```text
/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-conduction-frozen-trial-step1-20261031T091249Z
```

`external-artifact-inventory.json` authenticates 37 files totaling 13,700,863 bytes.
The retained `campaign-result.json` SHA-256 is
`db99578a2d91eab6c567b294899544d0e24b2e9d0fd530867c2d271ba09440f1`.

The authorization is consumed. No retry is authorized.
