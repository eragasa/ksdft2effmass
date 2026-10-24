# `ksdft2effmass.linalg`

## Purpose and status

`ksdft2effmass.linalg` is a compatibility import surface over linear-algebra and
unit-bearing quantity capabilities owned by PhysKit. It defines no quantity wrappers,
conversion copies, matrix-verification algorithms, or KSD-owned converter singleton.

Source:

```text
python/src/ksdft2effmass/linalg/
├── __init__.py
├── matrices.py
└── quantities.py
```

## Public contract

The package deliberately re-exports exact PhysKit objects for:

- `PhysicalUnit`, `Unitless`, and `ModelSystemUnit`;
- `ScalarQuantity` and `VectorQuantity`;
- `RealMatrixQuantity`, an exact compatibility name for PhysKit's `MatrixQuantity`;
- `ComplexMatrixQuantity`;
- `CsrRealMatrixQuantity`, an exact compatibility name for PhysKit's
  `SparseMatrixQuantity`;
- `CsrComplexMatrixQuantity`, an exact compatibility name for PhysKit's
  `ComplexSparseMatrixQuantity`;
- `PintUnitConverter`;
- `VerifiedMatrix`, `CsrSparseMatrix`, `VerifiedMatrixUtils`, and `MatrixVerifier`.

The compatibility names introduce no subclasses or conversion records. Consequently,
values created through KSD and PhysKit have the same runtime type identities.

KSD does not alias or re-export PhysKit's shared `ModelSystemUnitConverter` object.
Consumers requiring that object import it directly from its owner:

```python
from projectkoios.physkit.units import ModelSystemUnitConverter
```

`VerifiedMatrixUtils(matrix: VerifiedMatrix)` retains an immutable quantity and
`to_dense_matrix()` returns a real or complex dense quantity, converting CSR storage
without changing its unit. `MatrixVerifier.is_hermitian(*, rtol=0.0, atol=0.0)`
supports dense and CSR-sparse real or complex representations. PhysKit owns the dense
and sparse decision algorithms, tolerance validation, and non-densification behavior.

## Ownership and dependency boundary

PhysKit owns generic numerical quantities, unit conversion, matrix admission and
canonicalization, dense conversion, and matrix-property verification. KSD owns
Hamiltonian wrappers, spectral subspaces, model reduction, diagnostic policy,
acceptance, serialization, and provenance.

The dependency direction is:

```text
ksdft2effmass  →  projectkoios.physkit
```

PhysKit must not import KSD. `ksdft2effmass.operators` consumes the compatibility
surface but does not own or re-export its implementation.

## Evidence and limitations

Focused tests require exact PhysKit identities and cover immutable dense and CSR
storage, real and complex quantities, strict scalar and tolerance boundaries,
raw-CSR canonicalization, exact and numerical Hermiticity, unit conversion,
JSON-facing behavior, and unsupported sparse-format rejection. This
is software and bounded numerical evidence, not scientific validation of an operator
or model.
