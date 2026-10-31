# Blocked first rank-10 Wannier90 localization occurrence

This directory retains the first separately authorized Wannier90 localization
occurrence for the accepted-S1 12-band-to-rank-10 construction.

## Authorization and process outcome

The operator authorized exactly one invocation with zero retries and stop on failure.
Exactly one single-process Wannier90 3.1.0 invocation was made through the ProjectKoios
localization runner:

```text
/Users/eugene/projects/wannier90-3.1.0/wannier90.x silicon
```

The process returned zero, wrote the native completion line, and produced all four
selected outputs. No retry occurred. Native process success is recorded separately
from provider eligibility.

## Convergence disposition

The occurrence is **blocked**:

- disentanglement reached its declared 200-iteration budget and explicitly reported
  `Maximum number of disentanglement iterations reached` and
  `Disentanglement convergence criteria not satisfied`;
- its final dimensionless fractional delta was `1.191e-4`, versus the declared
  dimensionless `1.0e-10` convergence tolerance; see
  [`../../disentanglement-convergence-tolerance.md`](../../disentanglement-convergence-tolerance.md);
- Wannierisation reached its declared 100-iteration budget without printing the
  required convergence-criteria-satisfied message; and
- therefore the provider correctly returned `output-ineligible` despite native return
  code zero and `All done: wannier90 exiting`.

## Retained diagnostic outputs

Maintained bounded parsers successfully read the ineligible outputs:

- `silicon.wout`: 159,827 bytes, SHA-256
  `6e453927c5940a0a1120fd41f282381d42ce27db3159730cf51b4926ca59cb6e`;
- `silicon_u.mat`: 64 rank-10 matrices, maximum unitarity residual
  `1.9299517539650424e-10`;
- `silicon_u_dis.mat`: 64 matrices of shape 12 by 10, maximum isometry residual
  `1.3814217151920927e-10`; and
- `silicon_hr.dat`: 93 rank-10 representatives, complete negative-representative
  pairing, and maximum Hermiticity residual `0.0 eV` at retained precision.

The reported final total spread was `21.190106168 angstrom^2`. These are diagnostic
observations only. The matrices and Hamiltonian are not an accepted Wannier operator
because their generating optimization did not meet the declared convergence criteria.

The external occurrence inventory contains 34 files totalling 12,575,213 bytes. The
checkpoint and incidental Wigner-Seitz-vector output remain in the external occurrence
and inventory but are not promoted as eligible route outputs or restart authorization.

## Next-step boundary

No retry is authorized. Any revised convergence controls, projection/window choice,
initialization, or iteration budget requires a new calculation-owned declaration,
new preflight, and separate execution authorization. Interpolation, component-operator
acceptance, and Slater–Koster fitting remain blocked.
