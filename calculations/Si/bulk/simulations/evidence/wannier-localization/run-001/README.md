# Provider-eligible accepted-S1 `C6-B20-W21` precise-profile localization

This directory retains compact evidence for the separately authorized fresh Wannier90
3.1.0 localization occurrence and its no-calculator provider reverification. The
request SHA-256 was
`02375507dbe487f1ad5dee2569151faf04c2e5a5fa3aadd9b0007d977bc26aa7`.
Exactly one local calculator process ran with a 14,400-second timeout, 128 MiB ceiling,
zero retries, and no checkpoint or failed-output consumption.

## Native outcome

Wannier90 returned zero, emitted native completion, and completed in 184.507 seconds.
Both optimizations converged below their 40000-step ceilings:

- disentanglement converged at iteration 1517 under the dimensionless `2.0e-9` gate;
- Wannierisation converged at iteration 378 under the six-step `2.0e-9 angstrom^2`
  gate; and
- final reported total spread was `21.022751219 angstrom^2`.

No maximum-iteration warning was observed. This establishes native optimizer
convergence, not a global minimum or scientific adequacy.

## Corrected provider verification

The initial provider implementation produced a false negative by comparing `u` and
`u_dis` coordinates against lossy NNKP presentation values. NNKP writes eight decimal
places, while WIN supplies twelve and the matrix files write ten. For example, the same
coordinate appeared as `0.16666667` in NNKP and `0.1666666667` in `u`.

ProjectKoios now uses the canonical WIN k-point block for transformation-output order
and separately correlates NNKP to WIN under its native serialization bound. A
no-calculator reverification of the exact retained occurrence then measured:

- gauge k-point maximum residual: `3.300004713935323e-11`;
- disentanglement k-point maximum residual: `3.300004713935323e-11`;
- unchanged fractional k-point gate: `1.0e-10`;
- gauge-unitarity maximum: `2.0480683815549128e-10`;
- disentanglement-isometry maximum: `1.506470503898072e-10`;
- Hamiltonian Hermiticity maximum: `0.0 eV`; and
- Hamiltonian representative count: 279.

No tolerance changed and no calculator ran during reverification. The occurrence is
**provider-eligible after correction of a verifier reference-space defect**. The
original rejection is preserved as false-negative audit evidence; it is not the current
scientific disposition.

Provider eligibility permits full untruncated characterization. It does not establish
interpolation accuracy, development-target passage, confirmation, full-operator
acceptance, spatial-truncation acceptance, or Slater--Koster validity.

## Retention

The external occurrence contains 34 files and 66,862,500 bytes, below the 128 MiB
bound. Compact input, WOUT, execution, original-provider, reverification, and diagnostic
records are retained here. The larger interface and operator artifacts remain outside
Git; the external inventory authenticates them.

## Identities

| Artifact | SHA-256 |
|---|---|
| external inventory | `9158c61d9997e34662e9512c9442a318bb260fc819f7b32816fcb771e734ce54` |
| consumed authorization | `a55301c171769bf17e90a1bea88c7909f93fb7b1ba0fc649f31fe031c299245c` |
| original campaign result | `5727bb294590868e28a1fb57e0b847863c6b02b7ab669a8d71ac2a12bd5b9d3c` |
| original false-negative provider result | `2c373ab63e23b3be86b1c66c9da809e596805eaccbd052e2db2e441926cb2b64` |
| provider reverification result | `23a0a6fe182abd0b5d2f7dcd142f27f81d6d6cca4fe9852be1950b5b622548b6` |
| reconciled eligibility summary | `0b2a0e6bab52574c353d780f562afe11d07bb1400bf149fa1178ddb5e8504e4c` |
| original failure summary | `79fc6306e55581ae4b3fa90647d8f0c0b206f1339bdec332e064fd8c445dd135` |
| structural diagnostic | `95553e74ffe50177f859b5ec56627ffafeadc0b5c02a8e1745e9852938030618` |
| native format-precision observation | `d5826ea5555398ffd23ecdebf897d6dd0734409168e4ff4913949925e62ec5c9` |
| WOUT | `a909141e854129380aebd42acf58570d68df0451277c2bc0675a2c26ef3dd300` |
| eligible HR (external) | `24a411c875b3e66bba37e28cc6bf2d95c38ef521c39f81fde40cd0bfa294ea55` |
| eligible `u` (external) | `41758b721b79cae233689b4fb9fa359e750b82da8ed5bcd13b1d5faf3c5d8bf3` |
| eligible `u_dis` (external) | `3c1d3574f3bf783cf7b54d8e9fd00fa5811ef05a56240850d46f43a2c95b7ace` |

The complete occurrence remains outside Git at
`/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-c6-b20-w21-aiida-precise-v1`.

## Series disposition

S10 and S20 are complete. The next separately gated stage is S30 full untruncated
operator characterization. No 408-point development comparison, prediction freeze,
402-point confirmation, spatial truncation, or Slater--Koster work has been performed or
authorized by this correction.
