r"""Software verification of ``OperatorCompression``.

Evidence profile: routine

Bounded artifact scope: orthogonal represented-operator compression.

Facet and represented meaning

The ActionObject constructs retained-coordinate and embedded full-space operators.

Intrinsic and cross-object scope

Dense and sparse operator application, units, and correlation are included.

VVUQ and scientific exclusions

This verifies one represented transformation, not physical alignment, continuum
convergence, scientific validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import (
    OperatorCompression,
    OrthogonalSpectralSubspaceSelector,
    RealSymmetricEigenpairSolver,
    SparseMatrixQuantity,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = OperatorCompression


class TestOperatorCompression:
    """Own software evidence for ``OperatorCompression``."""

    def test_method__execute__constructs_correlated_coordinate_and_embedding_forms(
        self,
    ) -> None:
        """Evidence ID: SV-OPERATORS-COMPRESSION-001

        Requirement: Compression uses one declared orthogonal embedding for both
        retained coordinates and the embedded full-space operator.

        Acceptance: Retaining two states of a three-state sparse diagonal operator
        yields ``diag(1,2)`` and ``diag(1,2,0)`` in the respective spaces.
        """
        operator = SparseMatrixQuantity.from_csr(
            sparse.diags([1.0, 2.0, 3.0], offsets=0, format="csr"), Unitless()
        )
        eigenpairs = RealSymmetricEigenpairSolver().execute(operator)
        subspace = OrthogonalSpectralSubspaceSelector().execute(eigenpairs, 2)

        result = OperatorCompression().execute(operator, subspace)

        np.testing.assert_array_equal(result.coordinates.magnitude, np.diag([1.0, 2.0]))
        np.testing.assert_array_equal(
            result.embedded.magnitude, np.diag([1.0, 2.0, 0.0])
        )
