r"""Software verification of ``ComplexHermitianEigenpairResult``.

Evidence profile: routine

Bounded artifact scope: retained lowest complex-Hermitian eigenvalues and dense selected
vectors for one immutable sparse operator.

Facet and represented meaning

The ResultObject validates dimensions, units, ascending order, and binary64
orthonormality but does not claim the vectors solve the operator.

Intrinsic and cross-object scope

A diagonal three-state representation and unordered-eigenvalue attack are included.

VVUQ and scientific exclusions

Inputs are synthetic test data. This is software contract evidence, not eigensolver
validation, scientific validation, UQ, campaign execution, or human acceptance.
"""

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import (
    ComplexHermitianEigenpairResult,
    ComplexMatrixQuantity,
    ComplexSparseHermiticityAnalyzer,
    ComplexSparseMatrixQuantity,
    HermitianEigenpairSelection,
    PhysicalUnit,
    Unitless,
    VectorQuantity,
)

pytestmark = pytest.mark.software_verification
SUT = ComplexHermitianEigenpairResult


class TestComplexHermitianEigenpairResult:
    """Own software evidence for retained complex-Hermitian eigenpairs."""

    def test_constructor__ordered_orthonormal_eigenpairs__rejects_order_drift(
        self,
    ) -> None:
        """Evidence ID: SV-OPERATORS-COMPLEX-EIGENPAIR-001

        Requirement: Selected eigenvalues are ascending and vectors are unitless
        orthonormal columns matching the sparse operator dimension.

        Acceptance: The canonical diagonal basis passes; reversing two eigenvalues
        raises ``ValueError``.
        """
        unit = PhysicalUnit("electron_volt")
        operator = ComplexSparseMatrixQuantity.from_csr(
            sparse.diags([-2.0, -1.0, 1.0], format="csr"), unit
        )
        vectors = ComplexMatrixQuantity(np.eye(3, dtype=np.complex128), Unitless())
        hermiticity = ComplexSparseHermiticityAnalyzer().execute(
            operator, absolute_tolerance=0.0
        )
        result = ComplexHermitianEigenpairResult(
            operator,
            hermiticity,
            VectorQuantity(np.array([-2.0, -1.0, 1.0]), unit),
            vectors,
            HermitianEigenpairSelection.LOWEST,
        )

        assert result.full_dimension == 3
        assert result.selected_count == 3
        with pytest.raises(ValueError, match="ordered"):
            ComplexHermitianEigenpairResult(
                operator,
                hermiticity,
                VectorQuantity(np.array([-1.0, -2.0, 1.0]), unit),
                vectors,
                HermitianEigenpairSelection.LOWEST,
            )
