# Accepted-S1 `C6` Wannier90 preprocessing evidence

This directory retains compact evidence for the separately authorized `C6`
`wannier90.x -pp silicon` occurrence. The request SHA-256 was
`28599fee49e6b4b7050f2a9d714770bcaf6246be2aa99837a191352c5120a430` and the exact
10,417-byte input SHA-256 was
`2d5e4f0486e5062a8dd89a202845b8deac65efffea8acc0be05c192a4c12b604`.
Exactly one local process ran with a 120-second timeout, 32 MiB ceiling, and zero
retries.

Wannier90 3.1.0 returned zero and emitted the native completion line
`Exiting... silicon.nnkp written.` The maintained bounded NNKP parser and source verifier
confirmed:

- 216 source-ordered k-points;
- eight neighbors per point and 1,728 ordered neighbor records;
- direct lattice agreement within `1.0e-7 angstrom`;
- reciprocal lattice agreement within `1.0e-7 inverse angstrom`;
- fractional k-point agreement within `1.0e-8`;
- no excluded bands;
- ten expanded projections: eight nodeless `sp3` hybrids and two radial-index-two
  `s` functions at the declared silicon centers.

The external occurrence contains 16 files and 127,751 bytes. Wannier90 reported
`IEEE_OVERFLOW_FLAG` at termination; it remains a diagnostic because native completion,
bounded parsing, source correlation, and all declared invariants succeeded.

## Identities

| Artifact | SHA-256 |
|---|---|
| external inventory | `cc137101dc7b84baf8254ca192ae272992ca20f3a32b38f97d8a77c7487b78e3` |
| consumed authorization | `a66b6d4fbd67cc8a59b66daec4f896c31766522981175df2b57c54a1a7731d04` |
| `silicon.win` | `2d5e4f0486e5062a8dd89a202845b8deac65efffea8acc0be05c192a4c12b604` |
| `silicon.nnkp` | `f367195dcc42a72244104e8149bbc75b4ce623c67a6acc1d169c68b33aeffead` |
| preprocessing result | `8306f8b7340e1673a79342a8725b4ad2bd63e96ea078929b423f6d72145538a4` |
| campaign result | `1ac21c19acf2475d27a67ecf2441a37d19c93accd9bfe6784b8fc378335c4efe` |

The complete occurrence remains outside Git at
`/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-preprocess-c6-lower-energy-frozen-v1`.

## Scientific disposition

This is an eligible `C6` NNKP topology handoff, not a converted interface, localized
operator, or intended-use result. `pw2wannier90.x`, localization, retries, `C8`, and
`C12` require separate authorization.
