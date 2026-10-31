# Accepted-S1 `C6-B20-W21` AiiDA-precise preprocessing evidence

This directory retains compact evidence for the separately authorized
`wannier90.x -pp silicon` occurrence using the selected 20-band target space and the
pinned AiiDA precise convergence adaptation. The authorization-request SHA-256 was
`c7d18564bfc163aea72f0975f343cfea409c4f66c6618333d7c7da54ca06996d`; the exact
10,413-byte input SHA-256 was
`b48069e4f8ecd7209a318c47c77691de063bd0575658eb88a1e662a359d3dcc8`.
Exactly one local process ran with a 120-second timeout, 32 MiB ceiling, and zero
retries.

Wannier90 3.1.0 returned zero and emitted the native completion line
`Exiting... silicon.nnkp written.` The maintained bounded NNKP parser and source verifier
confirmed:

- 216 source-ordered C6 k-points;
- eight neighbors per point and 1,728 ordered neighbor records;
- direct-lattice agreement within `1.0e-7 angstrom`;
- reciprocal-lattice agreement within `1.0e-7 inverse angstrom`;
- fractional k-point agreement within `1.0e-8`;
- no excluded bands; and
- ten expanded projections: eight nodeless `sp3` hybrids and two radial-index-two
  `s` functions at the declared silicon centers.

The external occurrence contains 18 files and 154,290 bytes. Wannier90 reported
`IEEE_OVERFLOW_FLAG` at termination; it remains a diagnostic because the native
completion message, return code, bounded parsing, source correlation, and all declared
NNKP invariants passed. Preprocessing performs no disentanglement or Wannierisation, so
this occurrence does not test the adopted 40000-step localization ceilings.

## Identities

| Artifact | SHA-256 |
|---|---|
| external inventory | `747604bb4d4f130251befc040f9618bf58703eb36d19700f7404d0f51e2a9f98` |
| consumed authorization | `809d9fbc3a801aede1937c58e24ed2f7b66258a2aff6ea3b7966a594ece0c278` |
| `silicon.win` | `b48069e4f8ecd7209a318c47c77691de063bd0575658eb88a1e662a359d3dcc8` |
| `silicon.nnkp` | `608b8e0aacb8adddcfc2b8e0090ce48f5b916aec0d321bb69aabf01af9462575` |
| `silicon.wout` | `7c7fffc718f6139b4daaf6dd54f9b78a2bc4c09b992830c3607eaca1476e583b` |
| diagnostic disposition | `72802334f306a1a26383549f5a765f85761cf59daa16e6b22995c348d8633b6f` |
| preprocessing result | `ca73c8e0384e5f8b3bccffbe1ab1b2e58d636876f802b380a06eec74f8c50e93` |
| campaign result | `406dd32755f52f39a01365d27a90eb970c49774d3abf21808963f02d592a32ad` |

The complete occurrence remains outside Git at
`/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-preprocess-c6-b20-w21-aiida-precise-v1`.

## Scientific disposition

This is an eligible `C6-B20-W21` NNKP topology handoff, not a converted 20-band
interface, localized operator, optimizer result, or intended-use result. The
authorization is consumed. `pw2wannier90.x`, localization, retries, `C6-B30`, `C8`,
`C12`, confirmation, component-operator construction, and Slater--Koster reduction
remain unauthorized.
