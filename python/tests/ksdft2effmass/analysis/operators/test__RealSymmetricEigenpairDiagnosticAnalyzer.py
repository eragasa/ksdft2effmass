"""Software verification for finite-eigenpair diagnostics."""

import numpy as np
import pytest
from projectkoios.physkit.linalg.eigen import SpectralDecomposition

from ksdft2effmass.analysis.operators import RealSymmetricEigenpairDiagnosticAnalyzer
from ksdft2effmass.linalg import RealMatrixQuantity, Unitless

pytestmark = pytest.mark.software_verification
SUT = RealSymmetricEigenpairDiagnosticAnalyzer


class TestRealSymmetricEigenpairDiagnosticAnalyzer:
    """Own software evidence for residual and overlap diagnostics."""

    def test_method__execute__separates_residuals_from_reference_overlaps(self) -> None:
        """Exact diagonal eigenpairs have zero algebraic and overlap defects."""
        operator = RealMatrixQuantity(np.diag([1.0, 3.0]), Unitless())
        eigensystem = SpectralDecomposition(operator).eigensystem()
        reference = RealMatrixQuantity(np.eye(2), Unitless())

        result = SUT().execute(eigensystem, reference)

        np.testing.assert_allclose(result.algebraic_residual.magnitude, 0.0)
        np.testing.assert_allclose(result.scaled_column_residuals.magnitude, 0.0)
        assert result.overlap_defects is not None
        np.testing.assert_allclose(result.overlap_defects.magnitude, 0.0)
