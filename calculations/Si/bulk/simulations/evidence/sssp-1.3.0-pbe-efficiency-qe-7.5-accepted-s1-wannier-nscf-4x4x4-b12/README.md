# Accepted-S1 4x4x4, 12-band Wannier-oriented NSCF occurrence

This directory retains the first authorized NSCF qualification occurrence for the
full ten-spatial-orbital component-operator route. It is not an accepted downstream
Wannier handoff.

## Authorization and execution

The operator authorized exactly one invocation with zero retries and stop on failure.
Exactly one single-process `pw.x` 7.5 invocation was made. It returned zero in about
15 seconds and printed `JOB DONE.` No retry occurred.

The exact pre-execution decision document is retained byte-for-byte as
[`input/wannier-interface-decision.txt`](input/wannier-interface-decision.txt), SHA-256
`191b3c9657271d4aa08096bae0509ba9c0b4976123317977a0a80fe45e8fd9d6`.

The occurrence used:

- exact accepted S1 structure;
- the authenticated accepted-parent SCF saved state;
- full unreduced Gamma-origin `4 x 4 x 4` sampling, 64 points;
- 12 scalar non-spin bands;
- 42/336 Ry cutoffs;
- fixed occupations;
- `cg` diagonalization with `diago_full_acc = .true.`; and
- requested `conv_thr = 1.0e-12 Ry`.

## Retained observations

The maintained `QuantumEspressoXsdDocumentParser` parsed QEXSD 25.05.21. The document
reports exit status zero, 64 sampled points, 12 bands, finite eigenvalues, and finite
occupations. Its SHA-256 is
`7c5394a73a565d9fa2a0580433af5656003d411fe0d255ac364ca12a871af96c`.

The maintained ProjectKoios saved-state verifier authenticated 67 files totalling
18,798,436 bytes. The child manifest SHA-256 is
`1b02e9c67140a085c473afb77016f2cae10fa4eea78e7a475e422f3cc560ad8f`.
The full external occurrence inventory contains 90 files totalling 36,100,867 bytes.

QE nevertheless emitted 41 `c_bands` warning lines reporting 44 unconverged
eigenvalues in total, at most two at one k point. The stderr IEEE flags remain retained
diagnostics. Unlike the otherwise clean earlier SCF occurrences, the explicit
`c_bands` diagnostics block acceptance of this saved state for Wannier preprocessing.

## Disposition

**Blocked for downstream qualification.** Native execution succeeded and all evidence
is retained, but this occurrence is not accepted as an NSCF handoff. Any revised
NSCF—such as a separately reviewed diagonalization strategy or tolerance—requires a
new preflight and explicit authorization. This record does not authorize Wannier90
preprocessing, `pw2wannier90.x`, localization, or a retry.

The local wrapper initially misclassified the successful native occurrence because it
expected status `completed` and field `return_code`; ProjectKoios authoritatively emits
status `succeeded` and field `returncode`. That postprocessing failure is recorded in
`campaign-result.json`; it did not cause a second calculator invocation.
