# Accepted-S1 first pw2wannier90 conversion occurrence

This directory retains the first authorized rank-10 interface conversion occurrence
binding the verified NNKP topology to the authenticated Davidson NSCF saved state.

## Authorization and execution

The operator authorized exactly one invocation with zero retries and stop on failure.
Exactly one single-process `pw2wannier90.x -in pw2wannier90.in` invocation was made
through the maintained ProjectKoios runner. It returned zero and printed `JOB DONE.`
No retry occurred.

The exact pre-execution decision document is retained as
[`input/wannier-interface-decision.txt`](input/wannier-interface-decision.txt), SHA-256
`76b53356bb8aff1bfc7915900a7e8a3b4bab5bb724bb4a43bbb34e85dd01a152`.

## Retained observations

The maintained bounded parsers authenticated and parsed:

- AMN: 514,659 bytes, SHA-256
  `1fbc2b98f9c7222c726d694afc2582b6e8fb28f6f9b4668357d80b322c938efc`,
  64 k points, 12 bands, 10 projections;
- MMN: 2,754,147 bytes, SHA-256
  `1b4ebf8e6cff7c3c5491513707d969ddc988ed21a2dd2788bfdd6003de138e6f`,
  64 k points, 12 bands, eight neighbors per point and 512 records; and
- EIG: 29,952 bytes, SHA-256
  `e2a86cbab7f14a607987fe5d965449541703ebece16db8500b2b1cb74ecb743a`,
  64 k points and 12 bands in eV.

The MMN neighbor inventory exactly matches the NNKP source/target indices and
reciprocal-cell shifts. EIG agrees with the canonical Davidson QEXSD eigenvalues to a
maximum absolute difference of `5.258016244624741e-13 eV` after the declared Hartree
to eV conversion. All parsed numeric values and matrix norms are finite.

The native stdout reports that the real lattice, reciprocal lattice, k points,
rank-10 projection inventory, guiding functions, and all neighbors are acceptable,
followed by `AMN calculated`, `MMN calculated`, and `JOB DONE.` The stderr IEEE flags
remain retained nonblocking diagnostics.

The full external occurrence inventory contains 87 files totalling 22,173,836 bytes.

## Disposition

**Eligible AMN/MMN/EIG interface handoff for separately preflighted Wannier90
localization.** This does not establish localization or disentanglement convergence,
interpolation accuracy, effective-mass accuracy, or component-operator adequacy.

No localization, retry, or further calculator occurrence is authorized by this record.
