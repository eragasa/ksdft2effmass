# Accepted-S1 first Wannier90 preprocessing occurrence

This directory retains the first authorized Wannier90 3.1.0 preprocessing occurrence
for the rank-10 component-operator candidate.

## Authorization and execution

The operator authorized exactly one invocation with zero retries and stop on failure.
Exactly one single-process `wannier90.x -pp silicon` invocation was made through the
protected ProjectKoios calculator executor. It returned zero and wrote
`silicon.nnkp`. No retry occurred.

The executed input uses separate `Si:sp3` and `Si:l=0:r=2` declarations. The exact
pre-execution decision document is retained as
[`input/wannier-interface-decision.txt`](input/wannier-interface-decision.txt), SHA-256
`00ba0cb19789ff7349bf3b37784c4222eba758f90dd5be9d28c368763a892015`.
The superseded compact projection spelling was never executed and remains separately
retained.

## Retained observations

The native WOUT contains `Exiting... silicon.nnkp written.` The NNKP artifact has:

- 18,824 bytes;
- SHA-256 `4dd17877e0f3bc0b19a0f74ce539a91bd8ceb1c66a18d3f733f08e5d8ce07014`;
- 64 ordered k points;
- eight neighbors per point and 512 ordered neighbor records;
- no excluded bands; and
- ten expanded projections: eight nodeless `sp3` hybrids and two nodal s-like
  projections at the declared two Si centers.

The maintained bounded parser succeeded. Direct lattice, reciprocal lattice including
the native `2 pi` convention, ordered k points, and excluded bands agree with the
source declaration using explicit tolerances matching the NNKP serialization precision:
`1.0e-7 angstrom`, `1.0e-7 / angstrom`, and `1.0e-8` fractional.

The first postprocessing comparison used `1.0e-10` lattice tolerances, tighter than the
NNKP's seven-decimal lattice serialization, and failed closed. That superseded policy
attempt is retained in `result/postprocessing-attempts.json`; it caused no calculator
invocation.

Wannier90 emitted an `IEEE_OVERFLOW_FLAG` diagnostic on stderr. It is retained but is
not an automatic blocker because return status, native completion, bounded parsing,
and all finite semantic checks succeeded.

The full external occurrence inventory contains 22 files totalling 92,868 bytes.

## Disposition

**Eligible NNKP topology handoff for separately preflighted `pw2wannier90.x`
conversion.** This does not establish reciprocal-grid, band, projection, window,
localization, interpolation, or component-operator adequacy.

No converter, localization, retry, or other calculator occurrence is authorized by
this record.
