# Provider-eligible lower-energy frozen-window occurrence

This directory retains the single authorized fresh occurrence that changed only
`dis_num_iter` from 1000 to 2000 relative to the blocked lower-energy frozen-window
candidate. The executable returned zero, both native convergence messages were present,
and ProjectKoios classified the outputs as provider-eligible.

Provider eligibility is not scientific acceptance of the Wannier operator.

## Convergence

- Disentanglement converged at iteration 1290.
- Its final dimensionless fractional delta was `-9.691e-11`, below the strict
  `1.0e-10` threshold for the required three-iteration window.
- The calculated crossing agrees with the predecessor's explicitly labelled
  1274--1285 late-trend extrapolation to within five iterations.
- Wannierisation converged at iteration 189 under
  `conv_tol = 2.0e-9 angstrom^2`, window 6.
- Final total spread was `19.532839107 angstrom^2`.

## Structural provider checks

ProjectKoios verified:

- 64 rank-10 gauge matrices with maximum unitarity residual
  `1.5795521450794357e-10`;
- 64 `12 x 10` disentanglement matrices with maximum isometry residual
  `1.32123580246505e-10`;
- 93 rank-10 Hamiltonian representatives; and
- `0.0 eV` maximum Hamiltonian Hermiticity residual.

These checks establish structural validity only. Construction- and withheld-mesh
spectral tests, valley identity and location, edge energies, derivatives,
curvature/effective masses, locality/tail sensitivity, and component-operator evidence
remain pending.

## Provenance

The external occurrence remains at:

```text
/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-lower-energy-frozen-dis2000-20261031T100534Z
```

`external-artifact-inventory.json` authenticates 39 files totaling 12,779,316 bytes.
The retained summaries have SHA-256 identities:

- `campaign-result.json`:
  `510b2bf0602608dc9d6fe68c993d0987fdb5006641be40d0375a1299160efccd`;
- `eligibility-summary.json`:
  `de84d5c8eb6ec67ddd9facc6e18a25bc034d8c3624e2b94ed6bbbf242ef55504`; and
- `provider-result.json`:
  `ffff01cc1a542e3529be274cc1fd51092ebb46187cc662c36cd384ad5ab3b108`.

The authorization is consumed. No retry is authorized or needed for provider
eligibility. Any scientific acceptance analysis must be declared separately and should
reuse these retained matrices without a calculator invocation where possible.
