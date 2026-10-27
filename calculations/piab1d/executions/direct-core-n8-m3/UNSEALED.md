# Unsealed development execution

This directory contains the completed direct PIAB1D calculate → verify → render
stages for execution `direct-core-n8-m3`.

It was generated from clean KSD source commit
`c8d808c6b8959dec8338207dff0450ebacc31646`, which pins PhysKit commit
`9c74ffa2fa0f40792117ccaa6c0bf0bcb0e70fe5` and Project Koios Optimization
commit `2a18e485109e307b2f7928bd0418bcf796aeb0d5`.

At the operator's direction, this complete execution replaces the previously retained
execution at the same path. The preceding bytes remain recoverable from Git revision
`e7b8ab63f5efbe0458d3efbcfe2faedf45c8896c`. The current calculation writes its
result through the closed `Piab1dCalculationResult` typed boundary before publication.
The shared quadrature section retains the rule identifier, version, name, spacing,
weights, weighted Gram matrix, and weighted projector.

The execution is intentionally unsealed. `development-provenance.json` records its
source revision, dependencies, reproduction commands, artifact identities, and
replacement relationship. The execution has no seal, sealed source manifest, sealed
provenance record, or evidence-package identity. It remains illustrative development
output and does not constitute scientific validation, publication acceptance, or a
software release.
