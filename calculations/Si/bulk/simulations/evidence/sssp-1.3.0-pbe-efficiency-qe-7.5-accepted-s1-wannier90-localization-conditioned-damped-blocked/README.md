# Blocked conditioned and damped localization occurrence

This directory retains the separately authorized fresh convergence-control revision of
the first rank-10 Wannier90 localization candidate.

## Authorized revision

Relative to the first occurrence, this candidate enabled `precond`, raised `num_iter`
from 100 to 500, reduced `dis_mix_ratio` from 0.5 to 0.2, and raised `dis_num_iter`
from 200 to 1000. It kept the `1.0e-10 angstrom^2` Wannierisation absolute
tolerance and dimensionless `1.0e-10` disentanglement fractional tolerance, all
physical and interface choices, and all NNKP/AMN/MMN/EIG bytes unchanged. It did not
consume the blocked checkpoint. See
[`../../disentanglement-convergence-tolerance.md`](../../disentanglement-convergence-tolerance.md)
for the native distinction.

Exactly one Wannier90 3.1.0 process was invoked. It returned zero and printed native
completion. No retry occurred.

## Convergence disposition

Conditioning resolved the Wannierisation failure: the native output reports
`Wannierisation convergence criteria satisfied` at iteration 86.

Disentanglement remains unconverged and blocks the occurrence:

- it exhausted the revised 1000-iteration budget;
- it explicitly reported `Maximum number of disentanglement iterations reached` and
  `Disentanglement convergence criteria not satisfied`; and
- its final dimensionless fractional delta was `3.815e-6`, still above the declared
  dimensionless `1.0e-10` tolerance.

The provider therefore correctly returned `output-ineligible` despite native process
success and successful conditioned Wannierisation.

## Diagnostic outputs

Maintained bounded parsers verified:

- 64 rank-10 gauge matrices, maximum unitarity residual
  `1.7945089858528718e-10`;
- 64 disentanglement matrices of shape 12 by 10, maximum isometry residual
  `1.527513671106817e-10`;
- 93 rank-10 Hamiltonian representatives with complete negative pairing and maximum
  Hermiticity residual `0.0 eV`; and
- final reported total spread `21.731283428 angstrom^2`.

These are diagnostic observations only. Because disentanglement did not satisfy its
declared convergence criterion, the matrices and Hamiltonian are not an accepted
Wannier operator.

The external occurrence inventory contains 35 files totalling 12,621,701 bytes. The
checkpoint and incidental Wigner-Seitz-vector output remain external and do not grant
restart authority.

No retry is authorized. Any tolerance change, window/frozen-subspace change, mixing
revision, or other successor requires a new declaration, preflight, and authorization.
