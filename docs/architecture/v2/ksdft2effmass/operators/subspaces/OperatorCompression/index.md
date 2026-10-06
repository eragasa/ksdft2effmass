# `OperatorCompression`

## Purpose and status

This implemented row-027 Action evaluates finite real-matrix compression through an
orthonormal embedding.

## Operation

For ambient represented matrix `H` and orthonormal columns `Q`, the Action computes
`Q^T H Q` and `P H P = Q(Q^T H Q)Q^T`, retaining the input matrix and subspace in an
`OperatorCompressionResult`. Dense and supported sparse inputs are accepted; ambient
dimensions must agree.

## Ownership boundary

The Action owns numerical matrix multiplication only. It does not classify invariance,
construct a scientific retained space, attach parent/basis/gauge/energy/provenance
identity, fit an effective model, or perform downfolding. Row 023 therefore uses its
separately identified finite-parent invariant route rather than retrofitting this generic
result.

`TestOperatorCompression` provides hand-derived oracle and negative contract evidence.
Passing does not establish scientific validity or acceptance.
