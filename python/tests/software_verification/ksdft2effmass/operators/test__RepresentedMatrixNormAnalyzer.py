r"""Software verification of ``RepresentedMatrixNormAnalyzer``.

Evidence profile: routine

Bounded artifact scope: explicit dense and sparse represented-matrix norm analysis.

Facet and represented meaning

The ActionObject reports Frobenius, spectral, and maximum-entry norms with units.

Intrinsic and cross-object scope

Dense/sparse agreement and componentwise normalization are included.

VVUQ and scientific exclusions

This verifies finite matrix metrics, not representation independence, convergence,
scientific validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import (
    MatrixQuantity,
    RepresentedMatrixNormAnalyzer,
    SparseMatrixQuantity,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = RepresentedMatrixNormAnalyzer


class TestRepresentedMatrixNormAnalyzer:
    """Own software evidence for ``RepresentedMatrixNormAnalyzer``."""

    def test_method__execute__agrees_for_dense_and_sparse_representations(self) -> None:
        """Evidence ID: SV-OPERATORS-MATRIX-NORM-001

        Requirement: Equal dense and CSR matrices produce equal declared norms.

        Acceptance: ``diag(3,4)`` has Frobenius five, spectral four, maximum entry
        four, and normalizing the result by itself yields three unit ratios.
        """
        dense = MatrixQuantity(np.diag([3.0, 4.0]), Unitless())
        sparse_quantity = SparseMatrixQuantity.from_csr(
            sparse.diags([3.0, 4.0], offsets=0, format="csr"), Unitless()
        )
        analyzer = RepresentedMatrixNormAnalyzer()

        dense_result = analyzer.execute(dense)
        sparse_result = analyzer.execute(sparse_quantity)

        assert dense_result == sparse_result
        assert dense_result.frobenius.magnitude == 5.0
        assert dense_result.spectral.magnitude == 4.0
        assert dense_result.maximum_entry.magnitude == 4.0
        normalized = dense_result.normalized_by(dense_result)
        assert normalized.frobenius.magnitude == 1.0
        assert normalized.spectral.magnitude == 1.0
        assert normalized.maximum_entry.magnitude == 1.0
