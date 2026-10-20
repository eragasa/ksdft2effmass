"""Software verification for decomposition-identifiability analysis."""

import numpy as np
import pytest
from ksdft2effmass.analysis.operators import DecompositionIdentifiabilityAnalyzer
from ksdft2effmass.operators import MatrixQuantity, Unitless

pytestmark = pytest.mark.software_verification
SUT = DecompositionIdentifiabilityAnalyzer


class TestDecompositionIdentifiabilityAnalyzer:
    """Own software evidence for exact alternative decompositions."""

    def test_method__execute__constructs_two_exact_decompositions(self) -> None:
        """A symmetric shift changes assignments without changing their sum."""
        hamiltonian = MatrixQuantity(np.diag([1.0, 3.0]), Unitless())
        shift = MatrixQuantity(np.array([[0.5, 0.25], [0.25, -0.5]]), Unitless())

        result = SUT().execute(hamiltonian, shift)

        np.testing.assert_allclose(
            result.physical_kinetic.magnitude
            + result.physical_potential.magnitude,
            hamiltonian.magnitude,
        )
        np.testing.assert_allclose(
            result.alternative_kinetic.magnitude
            + result.alternative_potential.magnitude,
            hamiltonian.magnitude,
        )
        assert result.physical_reconstruction_error.magnitude == 0.0
        assert result.alternative_reconstruction_error.magnitude == 0.0
        assert result.model_class_fits[-1].unexplained_frobenius_norm.magnitude == 0.0
