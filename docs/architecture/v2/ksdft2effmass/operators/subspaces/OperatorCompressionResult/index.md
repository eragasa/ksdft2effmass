# `OperatorCompressionResult`

## Purpose and status

This implemented row-027 DataObject correlates one finite real represented matrix `H`,
one orthonormal column embedding `Q`, retained coordinates `Q^T H Q`, and ambient
embedding `Q(Q^T H Q)Q^T = P H P`.

## Contract

Intrinsic checks require supported dense/sparse parent data, exact numerical subspace
and matrix result types, matching ambient and retained dimensions, and output units
identical to the input matrix unit. The DataObject validates correlations; it does not
recompute the products.

## Scientific boundary

The result carries no stable parent-model/operator identity, mathematical state space,
retention definition, basis, gauge, energy zero, invariance result, or provenance. It is
therefore not a `PeriodicRetainedOperator`. If the subspace is invariant, coordinates
represent the exact restriction of this finite operator. Otherwise they produce Ritz
compression. Neither is energy-dependent downfolding.

## Evidence and limitations

`TestOperatorCompression` uses hand-computed matrix products and checks dimension/unit
contradictions. Passing establishes finite represented algebra only, not invariance,
scientific retention, convergence, model adequacy, validation, UQ, or acceptance.
