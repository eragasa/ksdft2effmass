"""Software verification for orthogonal-compression residual analysis."""

import numpy as np
import pytest
from projectkoios.physkit.linalg.eigen import SpectralDecomposition

from ksdft2effmass.analysis.operators import OrthogonalCompressionResidualAnalyzer
from ksdft2effmass.linalg import RealMatrixQuantity, Unitless
from ksdft2effmass.operators import (
    OperatorCompression,
    OrthogonalSpectralSubspaceSelector,
)

pytestmark = pytest.mark.software_verification
SUT = OrthogonalCompressionResidualAnalyzer


class TestOrthogonalCompressionResidualAnalyzer:
    """Own software evidence for distinct compression residual meanings."""

    def test_method__execute__separates_consistent_and_discarded_residuals(
        self,
    ) -> None:
        """Spectral compression is consistent and unmatched loss is discarded."""
        operator = RealMatrixQuantity(np.diag([1.0, 2.0, 4.0]), Unitless())
        eigensystem = SpectralDecomposition(operator).eigensystem()
        subspace = OrthogonalSpectralSubspaceSelector().execute(eigensystem, 2)
        compression = OperatorCompression().execute(operator, subspace)

        result = SUT().execute(operator, subspace, compression)

        np.testing.assert_allclose(result.consistent.magnitude, np.zeros((3, 3)))
        np.testing.assert_allclose(
            result.unmatched.magnitude, result.discarded_sector.magnitude
        )
        np.testing.assert_allclose(
            result.discarded_sector.magnitude, np.diag([0.0, 0.0, -4.0])
        )
