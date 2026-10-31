# Accepted-S1 `C6-B20` parent-band NSCF preflight

This directory retains a no-execution preflight for the first broader-parent candidate.
`C6-B20` changes only the NSCF parent-band count from 12 to 20 relative to the
authenticated `C6` occurrence. The accepted structure and parent, SSSP 1.3 PBE
efficiency pseudopotential, 42/336 Ry cutoffs, Gamma-origin `6 x 6 x 6` mesh and point
ordering, fixed occupations, `1.0e-12 Ry` electronic threshold, Davidson solver,
full-diagonalization accuracy, and symmetry controls remain fixed.

The 20-band choice is the calculation-owned application of the factor-two moderate
band-count heuristic in pinned [`aiida-wannier90-workflows` 3.1.0 commit
`1c0115cb7c77541a0bd549bc05005df435d651b6`](https://github.com/aiidateam/aiida-wannier90-workflows/tree/1c0115cb7c77541a0bd549bc05005df435d651b6).
The exact source identities, implementation links, derivation `max(8, 8, 20, 14) = 20`,
and adaptation boundary are retained in
[`aiida-workflow-reference.json`](aiida-workflow-reference.json). This adopts only the
band-count heuristic, not the workflow's complete protocol or its default PBEsol
pseudopotential.

The maintained ProjectKoios NSCF projector and dry-run runner rendered [`pw.in`](pw.in)
and reproduced it byte-for-byte under [`rendered/pw.in`](rendered/pw.in). A bytewise
comparison with the accepted 12-band C6 input changes only:

```diff
-    nbnd = 12
+    nbnd = 20
```

The accepted parent saved-state manifest and all 50 bound files totaling 6,720,372 bytes
were verified in place. No parent artifact was copied, no occurrence root was created,
and no calculator was invoked.

## Originally planned occurrence

- proposed root:
  `/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20-v1`
- executable: QE 7.5 `pw.x`, SHA-256
  `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910`
- input: 13,911 bytes, SHA-256
  `20a6ee6e55d632bb66b1afcaac91592bf49c73a3e53e275659d1ccb03e47e1f9`
- scale: 216 explicit k-points, 20 bands, one local process
- timeout: 600 seconds
- retained-byte ceiling: 512 MiB
- planning wall-time range: 42--57 seconds, not guaranteed
- linear saved-state estimate: 97,388,742 bytes, not guaranteed
- invocations: one
- retries: zero

Unconverged-eigenvalue diagnostics, non-finite data, corrupt or inconsistent QEXSD,
nonzero return, or timeout would have blocked handoff without an automatic retry. The
subsequently authorized occurrence met these gates and its 20 eigenvalues were
inventoried. Compact evidence is retained under
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20/).
This preflight still does not select a 20-band Wannier target space.

## Identities

| Artifact | SHA-256 |
|---|---|
| `pw.in` | `20a6ee6e55d632bb66b1afcaac91592bf49c73a3e53e275659d1ccb03e47e1f9` |
| `calculation.toml` | `ffaaa924f31df95b674763b2613d3202bc0607bc5210d729b5447db8091424b9` |
| `aiida-workflow-reference.json` | `241c438dc17d4c747cfb977225e627090bb4dc7de767949ee9730e1996f09ad9` |
| `rendered/input-manifest.json` | `6848a992dbacb675dab1e3ec37e6afb69f6d89b3af6d2f013f83bdbae16b8c14` |
| `campaign-preflight.json` | `86c870f7d5edd1750933ebc7c4cc081411ea11342b286e9adc9e2d9fc71c78f3` |
| `authorization-request.json` | `33a36570545ef5e7e5ffcc3a5d7b3aea5ca461359f4f80c24491e2811562633e` |

## Authorization boundary

Status: **request consumed by one separately authorized occurrence**.

[`authorization-request.json`](authorization-request.json) retains its original
preflight state, `authorization_granted: false`; the distinct consumed authorization
record is retained with the occurrence evidence. That authorization cannot be replayed
and does not authorize a retry, preprocessing, conversion, localization, `C6-B30`,
`C8`, `C12`, confirmation-parent execution, or reduction. Every downstream calculator
occurrence requires a new exact authorization.
