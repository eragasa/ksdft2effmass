"""Software verification for verified-matrix representation conversion."""

from __future__ import annotations

import numpy as np
import pytest
import scipy.sparse as sp  # type: ignore[import-untyped]

from ksdft2effmass.linalg import (
    ComplexMatrixQuantity,
    CsrComplexMatrixQuantity,
    CsrRealMatrixQuantity,
    RealMatrixQuantity,
    Unitless,
    VerifiedMatrixUtils,
)

pytestmark = pytest.mark.software_verification


class TestVerifiedMatrixUtils:
    """Own conversion among verified finite matrix representations."""

    @pytest.mark.parametrize(
        "quantity",
        [
            RealMatrixQuantity(np.eye(2, dtype=np.float64), Unitless()),
            ComplexMatrixQuantity(np.eye(2, dtype=np.complex128), Unitless()),
        ],
    )
    def test_to_dense_matrix__dense_quantity__returns_retained_quantity(
        self,
        quantity: RealMatrixQuantity | ComplexMatrixQuantity,
    ) -> None:
        assert VerifiedMatrixUtils(quantity).to_dense_matrix() is quantity

    @pytest.mark.parametrize(
        "matrix, dense_type",
        [
            (
                CsrRealMatrixQuantity.from_csr(
                    sp.csr_array(np.eye(2, dtype=np.float64)),
                    Unitless(),
                ),
                RealMatrixQuantity,
            ),
            (
                CsrComplexMatrixQuantity.from_csr(
                    sp.csr_array(np.eye(2, dtype=np.complex128)),
                    Unitless(),
                ),
                ComplexMatrixQuantity,
            ),
        ],
    )
    def test_to_dense_matrix__sparse_quantity__preserves_values_unit_and_kind(
        self,
        matrix: CsrRealMatrixQuantity | CsrComplexMatrixQuantity,
        dense_type: type[RealMatrixQuantity] | type[ComplexMatrixQuantity],
    ) -> None:
        dense = VerifiedMatrixUtils(matrix).to_dense_matrix()

        assert isinstance(dense, dense_type)
        np.testing.assert_array_equal(dense.magnitude, np.eye(2))
        assert dense.unit == matrix.unit
