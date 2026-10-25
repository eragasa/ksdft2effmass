"""Software verification for decomposition analysis."""

from dataclasses import replace

import numpy as np
import pytest
from projectkoios.physkit.units import (
    MatrixQuantity,
    PhysicalUnit,
    Unitless,
)

from ksdft2effmass.analysis.operators import (
    KineticPotentialDecompositionAnalyzer,
    KineticPotentialDecompositionResult,
)

pytestmark = pytest.mark.software_verification
SUT = KineticPotentialDecompositionAnalyzer


class TestKineticPotentialDecompositionAnalyzer:
    """Own software evidence for exact alternative decompositions."""

    def test_method__execute__constructs_two_exact_decompositions(self) -> None:
        """A symmetric shift changes assignments without changing their sum."""
        hamiltonian = MatrixQuantity(np.diag([1.0, 3.0]), Unitless())
        shift = MatrixQuantity(np.array([[0.5, 0.25], [0.25, -0.5]]), Unitless())

        result = SUT().execute(hamiltonian, shift)

        np.testing.assert_allclose(
            result.physical_kinetic.magnitude + result.physical_potential.magnitude,
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
        reconstructed = KineticPotentialDecompositionResult.from_json(result.to_json())
        assert tuple(fit.name for fit in reconstructed.model_class_fits) == (
            "scalar",
            "diagonal",
            "tridiagonal",
            "real_symmetric",
        )

    def test_init__rejects_inconsistent_matrix_unit(self) -> None:
        """Every decomposition matrix belongs to one quantity space."""
        hamiltonian = MatrixQuantity(np.diag([1.0, 3.0]), Unitless())
        shift = MatrixQuantity(np.array([[0.5, 0.25], [0.25, -0.5]]), Unitless())
        result = SUT().execute(hamiltonian, shift)

        with pytest.raises(ValueError, match="matrix units must agree"):
            replace(
                result,
                alternative_potential=MatrixQuantity(
                    result.alternative_potential.magnitude,
                    PhysicalUnit("joule"),
                ),
            )

    def test_init__rejects_inconsistent_matrix_shape(self) -> None:
        """Every decomposition matrix acts on the same finite space."""
        hamiltonian = MatrixQuantity(np.diag([1.0, 3.0]), Unitless())
        shift = MatrixQuantity(np.array([[0.5, 0.25], [0.25, -0.5]]), Unitless())
        result = SUT().execute(hamiltonian, shift)

        with pytest.raises(ValueError, match="matrix shapes must agree"):
            replace(
                result,
                alternative_potential=MatrixQuantity(np.zeros((3, 3)), Unitless()),
            )

    def test_init__rejects_changed_model_class_order(self) -> None:
        """The retained model classes have one declared comparison order."""
        hamiltonian = MatrixQuantity(np.diag([1.0, 3.0]), Unitless())
        shift = MatrixQuantity(np.array([[0.5, 0.25], [0.25, -0.5]]), Unitless())
        result = SUT().execute(hamiltonian, shift)

        with pytest.raises(ValueError, match="declared ordering"):
            replace(result, model_class_fits=tuple(reversed(result.model_class_fits)))
