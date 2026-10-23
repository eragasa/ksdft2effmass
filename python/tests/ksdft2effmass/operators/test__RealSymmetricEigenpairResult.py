r"""Software verification of ``RealSymmetricEigenpairResult``.

Evidence profile: routine

Bounded artifact scope: public complete finite real-symmetric eigenpair ResultObject.

Facet and represented meaning

The result correlates one square represented operator with a full ordered spectrum and
column eigenvector basis.

Intrinsic and cross-object scope

Shape correlation, units, and immutable quantity storage are included.

VVUQ and scientific exclusions

This verifies result structure only, not eigensolver accuracy, scientific validation,
uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.linalg import (
    RealMatrixQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.operators import (
    RealSymmetricEigenpairResult,
)

pytestmark = pytest.mark.software_verification
SUT = RealSymmetricEigenpairResult


class TestRealSymmetricEigenpairResult:
    """Own software evidence for ``RealSymmetricEigenpairResult``."""

    def test_constructor__shape_correlation__retains_complete_eigenbasis(self) -> None:
        """Evidence ID: SV-OPERATORS-EIGENPAIR-001

        Requirement: Result dimensions match the selected eigenvalues and operator.

        Acceptance: A coherent two-dimensional result constructs and an eigenvector
        matrix inconsistent with the selected eigenvalue count is rejected.
        """
        operator = RealMatrixQuantity(np.diag([1.0, 2.0]), Unitless())
        result = RealSymmetricEigenpairResult(
            operator,
            VectorQuantity(np.array([1.0, 2.0]), Unitless()),
            RealMatrixQuantity(np.eye(2), Unitless()),
        )

        assert result.operator is operator
        with pytest.raises(ValueError, match="selected dimensions"):
            RealSymmetricEigenpairResult(
                operator,
                VectorQuantity(np.array([1.0, 2.0]), Unitless()),
                RealMatrixQuantity(np.ones((2, 1)), Unitless()),
            )
