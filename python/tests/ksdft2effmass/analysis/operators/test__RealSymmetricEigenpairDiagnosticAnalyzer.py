"""Software verification for finite-eigenpair diagnostics."""

import numpy as np
import pytest
from projectkoios.physkit.linalg.eigen import SpectralDecomposition
from projectkoios.physkit.units import (
    MatrixQuantity,
    Unitless,
)

from ksdft2effmass.analysis.operators import (
    RealSymmetricEigenpairDiagnosticAnalyzer,
    RealSymmetricEigenpairDiagnosticRequest,
)

pytestmark = pytest.mark.software_verification
SUT = RealSymmetricEigenpairDiagnosticAnalyzer


class TestRealSymmetricEigenpairDiagnosticAnalyzer:
    """Own software evidence for residual and overlap diagnostics."""

    def test_method__execute__separates_residuals_from_reference_overlaps(self) -> None:
        """Exact diagonal eigenpairs have zero algebraic and overlap defects."""
        operator = MatrixQuantity(np.diag([1.0, 3.0]), Unitless())
        eigensystem = SpectralDecomposition(operator).eigensystem()
        reference = MatrixQuantity(np.eye(2), Unitless())

        request = RealSymmetricEigenpairDiagnosticRequest(eigensystem, reference)
        analyzer = SUT(request)

        result = analyzer.execute()

        assert analyzer.request is request
        np.testing.assert_allclose(result.algebraic_residual.magnitude, 0.0)
        np.testing.assert_allclose(result.scaled_column_residuals.magnitude, 0.0)
        assert result.overlap_defects is not None
        np.testing.assert_allclose(result.overlap_defects.magnitude, 0.0)

    def test_request__different_reference_shape__raises_value_error(self) -> None:
        """Reference vectors must represent the same ordered eigenvector columns."""
        operator = MatrixQuantity(np.diag([1.0, 3.0]), Unitless())
        eigensystem = SpectralDecomposition(operator).eigensystem()
        reference = MatrixQuantity(np.eye(3), Unitless())

        with pytest.raises(ValueError, match="match eigenvector dimensions"):
            RealSymmetricEigenpairDiagnosticRequest(eigensystem, reference)
