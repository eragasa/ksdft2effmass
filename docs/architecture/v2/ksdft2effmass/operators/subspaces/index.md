# `operators.subspaces`

## Purpose and status

This implemented module owns numerical orthogonal spectral-subspace data, selection,
and finite real-matrix compression. It does not assign periodic scientific parentage or
retention meaning.

## Row-027 owners

- [`OperatorCompressionResult`](OperatorCompressionResult/index.md): immutable input
  and output represented matrices;
- [`OperatorCompression`](OperatorCompression/index.md): Action that evaluates the
  matrix products.

`OrthogonalSpectralSubspace` supplies numerical eigenvalues and orthonormal embedding.
A separate scientific aggregate is required to identify a parent operator, retained
space, basis/gauge, energy zero, invariance status, construction, and provenance.

Source is `python/src/ksdft2effmass/operators/subspaces.py`; software evidence is
`python/tests/software_verification/ksdft2effmass/operators/test__OperatorCompression.py`;
Sphinx coverage is `doc/sphinx/api/operators.rst` and the scientific-retention concept.
