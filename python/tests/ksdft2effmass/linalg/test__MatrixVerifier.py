"""Software verification for dense-matrix property verification."""

from __future__ import annotations

import numpy as np
import pytest
import scipy.sparse as sp  # type: ignore[import-untyped]

from ksdft2effmass.linalg import (
    ComplexMatrixQuantity,
    CsrComplexMatrixQuantity,
    CsrRealMatrixQuantity,
    MatrixVerifier,
    RealMatrixQuantity,
    Unitless,
)

pytestmark = pytest.mark.software_verification


class TestMatrixVerifier:
    """Own Hermiticity decisions, tolerance validation, and input retention."""

    @pytest.mark.parametrize(
        "matrix",
        [
            np.array([[1.0, 2.0], [2.0, 3.0]], dtype=np.float64),
            np.array(
                [[1.0 + 0.0j, 2.0 + 3.0j], [2.0 - 3.0j, 4.0 + 0.0j]],
                dtype=np.complex128,
            ),
            RealMatrixQuantity(np.eye(2), Unitless()),
            ComplexMatrixQuantity(np.eye(2, dtype=np.complex128), Unitless()),
        ],
    )
    def test_is_hermitian__exact_real_complex_and_quantities__returns_true(
        self,
        matrix: np.ndarray | RealMatrixQuantity | ComplexMatrixQuantity,
    ) -> None:
        assert MatrixVerifier(matrix).is_hermitian()

    def test_is_hermitian__raw_and_quantity_sparse_inputs__returns_true(self) -> None:
        real = sp.csr_array(np.array([[1.0, 2.0], [2.0, 3.0]], dtype=np.float64))
        complex_matrix = sp.csr_array(
            np.array(
                [[1.0 + 0.0j, 2.0 + 3.0j], [2.0 - 3.0j, 4.0 + 0.0j]],
                dtype=np.complex128,
            )
        )
        real_quantity = CsrRealMatrixQuantity.from_csr(real, Unitless())
        complex_quantity = CsrComplexMatrixQuantity.from_csr(
            complex_matrix,
            Unitless(),
        )

        assert MatrixVerifier(real).is_hermitian()
        assert MatrixVerifier(complex_matrix).is_hermitian()
        assert MatrixVerifier(real_quantity).is_hermitian()
        assert MatrixVerifier(complex_quantity).is_hermitian()

    @pytest.mark.parametrize(
        "matrix",
        [
            np.array([[1.0, 1.0], [0.0, 1.0]], dtype=np.float64),
            np.array([[1.0 + 1.0j]], dtype=np.complex128),
            np.ones((2, 3), dtype=np.float64),
        ],
    )
    def test_is_hermitian__nonhermitian_or_rectangular__returns_false(
        self,
        matrix: np.ndarray,
    ) -> None:
        assert not MatrixVerifier(matrix).is_hermitian()

    def test_is_hermitian__nonhermitian_sparse_input__returns_false(self) -> None:
        matrix = sp.csr_array(np.array([[1.0, 1.0], [0.0, 1.0]], dtype=np.float64))

        assert not MatrixVerifier(matrix).is_hermitian()

    def test_is_hermitian__roundoff_asymmetry__uses_explicit_tolerances(self) -> None:
        matrix = np.array(
            [[1.0, 2.0 + 1.0e-14], [2.0, 3.0]],
            dtype=np.float64,
        )
        verifier = MatrixVerifier(matrix)

        assert not verifier.is_hermitian()
        assert verifier.is_hermitian(rtol=1.0e-14, atol=0.0)
        assert verifier.is_hermitian(rtol=0.0, atol=2.0e-14)

        sparse_verifier = MatrixVerifier(sp.csr_array(matrix))
        assert not sparse_verifier.is_hermitian()
        assert sparse_verifier.is_hermitian(rtol=1.0e-14, atol=0.0)
        assert sparse_verifier.is_hermitian(rtol=0.0, atol=2.0e-14)

    @pytest.mark.parametrize(
        "rtol, atol, exception, match",
        [
            (True, 0.0, TypeError, "rtol"),
            (0.0, 0, TypeError, "atol"),
            (np.float64(0.0), 0.0, TypeError, "rtol"),
            (-1.0, 0.0, ValueError, "rtol"),
            (0.0, float("inf"), ValueError, "atol"),
        ],
    )
    def test_is_hermitian__invalid_tolerance__rejects(
        self,
        rtol: object,
        atol: object,
        exception: type[Exception],
        match: str,
    ) -> None:
        verifier = MatrixVerifier(np.eye(2, dtype=np.float64))

        with pytest.raises(exception, match=match):
            verifier.is_hermitian(
                rtol=rtol,  # type: ignore[arg-type]
                atol=atol,  # type: ignore[arg-type]
            )

    def test_constructor__mutable_raw_array__retains_immutable_copy(self) -> None:
        source = np.eye(2, dtype=np.float64)
        verifier = MatrixVerifier(source)

        source[0, 1] = 1.0

        assert verifier.is_hermitian()
        assert isinstance(verifier.matrix, RealMatrixQuantity)
        with pytest.raises(ValueError, match="read-only"):
            verifier.matrix.magnitude[0, 0] = 2.0

    def test_constructor__mutable_raw_sparse__retains_immutable_quantity(self) -> None:
        source = sp.csr_array(np.array([[1.0, 2.0], [2.0, 3.0]], dtype=np.float64))
        verifier = MatrixVerifier(source)

        source.data[1] = 5.0

        assert verifier.is_hermitian()
        assert isinstance(verifier.matrix, CsrRealMatrixQuantity)
        with pytest.raises(ValueError, match="read-only"):
            verifier.matrix.data[0] = 2.0

    @pytest.mark.parametrize(
        "matrix, exception, match",
        [
            (np.eye(2, dtype=np.float32), TypeError, "dtype"),
            (np.array([1.0], dtype=np.float64), ValueError, "two-dimensional"),
            (
                np.array([[np.inf]], dtype=np.float64),
                ValueError,
                "finite",
            ),
            (
                sp.coo_array(np.eye(2, dtype=np.float64)),
                TypeError,
                "CSR-sparse",
            ),
            ([[1.0]], TypeError, "matrix must"),
        ],
    )
    def test_constructor__unsupported_matrix__rejects(
        self,
        matrix: object,
        exception: type[Exception],
        match: str,
    ) -> None:
        with pytest.raises(exception, match=match):
            MatrixVerifier(matrix)  # type: ignore[arg-type]
