# `ksdft2effmass.linalg`

## Purpose and status

`ksdft2effmass.linalg` is the implemented owner of immutable finite numerical
quantities, explicit units, dense and canonical CSR matrix representations, unit
conversion, and matrix-property verification.

Source:

```text
python/src/ksdft2effmass/linalg/
├── __init__.py
├── matrices.py
└── quantities.py
```

## Public contract

The package deliberately exports:

- `PhysicalUnit`, `Unitless`, and `ModelSystemUnit`;
- `ScalarQuantity` and `VectorQuantity`;
- `RealMatrixQuantity` and `ComplexMatrixQuantity` for dense binary64 matrices;
- `CsrRealMatrixQuantity` and `CsrComplexMatrixQuantity` for immutable canonical CSR
  matrices;
- `PintUnitConverter` and `MODEL_SYSTEM_UNIT_CONVERTER`;
- the `VerifiedMatrix` union of validated dense and CSR quantity representations and
  the separate raw `CsrSparseMatrix` structural boundary;
- `VerifiedMatrixUtils`, including dense conversion; and
- `MatrixVerifier`.

`VerifiedMatrixUtils(matrix: VerifiedMatrix)` retains an immutable quantity and
`to_dense_matrix()` returns a real or complex dense quantity, converting CSR storage
without changing its unit. `MatrixVerifier.is_hermitian(*, rtol=0.0, atol=0.0)`
supports dense and CSR-sparse real
or complex representations. Dense decisions delegate to
`scipy.linalg.ishermitian`. Sparse decisions apply the same elementwise closeness
criterion to sparse differences without densification. Both tolerances are explicit,
finite, nonnegative built-in floats; zero defaults recover exact finite-representation
Hermiticity.

## Ownership and dependency boundary

Linear-algebra representations do not own Hamiltonian, spectral-subspace, physical
model, discretization, eigensolver, compression, or scientific-acceptance semantics.
Those owners consume `ksdft2effmass.linalg`; this package does not depend on
`ksdft2effmass.operators`, model systems, analyses, calculations, serializers, or
provenance.

The dependency direction is therefore:

```text
ksdft2effmass.operators  →  ksdft2effmass.linalg
```

`ksdft2effmass.operators` does not re-export the linear-algebra surface.

## Evidence and limitations

Focused tests cover immutable dense and CSR storage, real and complex quantities,
strict scalar and tolerance boundaries, raw-CSR canonicalization, exact and numerical
Hermiticity, and rejection of unsupported sparse formats. This is software and bounded
numerical evidence, not scientific validation of an operator or model.
