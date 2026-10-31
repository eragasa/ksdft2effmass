# Accepted-S1 4x4x4, 12-band Davidson NSCF occurrence

This directory retains the revised NSCF qualification occurrence for the full
ten-spatial-orbital component-operator route.

## Authorization and execution

The operator authorized exactly one Davidson invocation with zero retries and stop on
failure. Exactly one single-process `pw.x` 7.5 invocation was made. It returned zero
in about 9 seconds and printed `JOB DONE.` No retry occurred.

The exact pre-execution decision document is retained byte-for-byte as
[`input/wannier-interface-decision.txt`](input/wannier-interface-decision.txt), SHA-256
`7d53ee1092529b32dd9e2ddad289e222bb3f8c77f6ff150e9915e8cc2f9e0a77`.

All scientific and numerical coordinates match the blocked CG occurrence except for
the declared one-variable change from `diagonalization = 'cg'` to
`diagonalization = 'david'`. Full diagonalization accuracy and `1.0e-12 Ry` tolerance
were retained.

## Retained observations

The maintained `QuantumEspressoXsdDocumentParser` parsed QEXSD 25.05.21. The document
reports exit status zero, 64 sampled points, 12 bands, finite eigenvalues, and finite
occupations. Its SHA-256 is
`cc389a14d6b9f809eab69ba30b86129a01951788a3fdbc290589ef8f5f69adb0`.

No `c_bands` unconverged-eigenvalue diagnostic appears. The stderr IEEE flags remain
retained diagnostics and do not override the finite, internally consistent output.
The source-ordered Davidson and blocked-CG eigenvalue arrays differ by at most
`4.3716777753378606e-05 eV`; this is a mechanical comparison and does not rehabilitate
the CG occurrence.

The maintained ProjectKoios saved-state verifier authenticated 67 files totalling
18,799,008 bytes. The child manifest SHA-256 is
`cab588c939b3b9bdea95496458be414f465f38fb036d1ade62405f8d602bf4ce`.
The full external occurrence inventory contains 90 files totalling 36,102,836 bytes.

## Disposition

**Eligible candidate handoff for separately preflighted Wannier90 preprocessing.**
This establishes neither production adequacy nor acceptance of the 4x4x4 grid,
12-band retained space, windows, interpolation, band edges, derivatives, localization,
or component-operator transformation.

No Wannier90 preprocessing, `pw2wannier90.x`, localization, or further calculator
invocation is authorized by this occurrence.
