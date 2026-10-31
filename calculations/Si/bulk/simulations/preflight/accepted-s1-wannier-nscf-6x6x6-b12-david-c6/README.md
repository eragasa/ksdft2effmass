# Accepted-S1 `C6` construction NSCF preflight

This directory retains the no-execution preflight for the first construction-mesh
successor declared in the bulk-silicon research protocol. `C6` changes only the full
Gamma-origin construction mesh from `4 x 4 x 4` (64 points) to `6 x 6 x 6` (216
points). The accepted structure and parent, SSSP pseudopotential, 42/336 Ry cutoffs,
12-band inventory, fixed occupations, Davidson diagonalization, full diagonalization
accuracy, symmetry settings, and electronic tolerance remain fixed.

The maintained ProjectKoios NSCF projector and dry-run runner rendered [`pw.in`](pw.in)
and reproduced it byte-for-byte under [`rendered/pw.in`](rendered/pw.in). The accepted
parent saved-state manifest and all 50 bound files totaling 6,720,372 bytes were verified
in place. No parent artifact was copied and no calculator was invoked.

## Planned occurrence

- proposed root:
  `/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier-nscf-6x6x6-b12-david-c6-v1`
- executable: QE 7.5 `pw.x`, SHA-256
  `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910`
- input: 13,911 bytes, SHA-256
  `dc5b913b0133b53968c1858dc984b408fcdc163b1fa654511f73c7098baa9bf3`
- scale: 216 explicit k-points, 12 bands, one local process
- timeout: 600 seconds
- retained-byte ceiling: 512 MiB
- nominal linear runtime estimate: 30--35 seconds, not guaranteed
- nominal linear saved-state estimate: 63,446,652 bytes, not guaranteed
- invocations: one
- retries: zero

Unconverged-eigenvalue diagnostics, non-finite data, corrupt or inconsistent QEXSD,
nonzero return, or timeout block handoff. A blocked occurrence receives no automatic
retry.

## Identities

| Artifact | SHA-256 |
|---|---|
| `pw.in` | `dc5b913b0133b53968c1858dc984b408fcdc163b1fa654511f73c7098baa9bf3` |
| `calculation.toml` | `ce9a8a896985335e06c6aca0b3e5a63a69176df27b818377ccd27f12744d28bd` |
| `rendered/input-manifest.json` | `490d410dbf035f9ea47ec83b3734e6f57e0349c3ecc942af555f17b791c618e3` |
| `campaign-preflight.json` | `7f25256c034a3078c43aaf12bdf3298a55af2dba28b6b31df0a840f4aded7190` |
| `authorization-request.json` | `eefee784368f186246f13da0dd97591dd1f0ec1d09c564262f1a2f3699c41a28` |

## Authorization boundary

Status: **authorization consumed by one occurrence**.

[`authorization-request.json`](authorization-request.json) remains immutable preflight
evidence with `authorization_granted: false`. The operator subsequently issued a
separate exact bounded authorization for its SHA-256 identity. Exactly one local
`pw.x` invocation completed with zero retries; compact evidence is retained under
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-6x6x6-b12-david-c6/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-6x6x6-b12-david-c6/).
The occurrence does not authorize Wannier90 preprocessing, conversion, localization,
`C8`, `C12`, confirmation-parent execution, or any retry.
