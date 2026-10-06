"""Software verification of finite-difference represented-result construction.

Synthetic matrices establish request, dimension, energy-unit, Hermiticity, and
immutability invariants. They do not establish continuum accuracy, scientific
validation, uncertainty quantification, or acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import (
    FiniteDifferenceBlochHamiltonian2DModel,
    FiniteDifferenceBlochHamiltonian2DRequest,
    FiniteDifferenceBlochHamiltonian2DResult,
    UniformPeriodicCoordinateBasis2D,
)
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestFiniteDifferenceBlochHamiltonian2DResultConstruction:
    """Own represented-matrix correlation and invariant evidence."""

    @staticmethod
    def request() -> FiniteDifferenceBlochHamiltonian2DRequest:
        """Return one synthetic unitless five-by-five-grid construction request."""
        unit = Unitless()
        model = FiniteDifferenceBlochHamiltonian2DModel(
            basis=UniformPeriodicCoordinateBasis2D(2.0 * np.pi, 5, "test.basis"),
            potential_samples=MatrixQuantity(np.zeros((5, 5)), unit),
            kinetic_scale=ScalarQuantity(1.0, unit),
            source_identifier="test.source",
            operator_identifier="test.operator",
            state_space_identifier="test.state-space",
            energy_reference="test.zero",
            provenance_identifier="test.provenance",
        )
        return FiniteDifferenceBlochHamiltonian2DRequest(model, (0.0, 0.0))

    def test_construction_retains_exact_request_and_immutable_matrix(self) -> None:
        """A valid result preserves request identity and non-writeable matrix values."""
        request = self.request()

        result = FiniteDifferenceBlochHamiltonian2DResult(
            request,
            ComplexMatrixQuantity(np.eye(25), Unitless()),
        )

        assert result.request is request
        assert result.represented_matrix.magnitude.shape == (25, 25)
        assert not result.represented_matrix.magnitude.flags.writeable

    def test_construction_rejects_wrong_dimension_unit_and_hermiticity(self) -> None:
        """A square array alone does not establish the declared represented operator."""
        request = self.request()

        with pytest.raises(ValueError, match="shape"):
            FiniteDifferenceBlochHamiltonian2DResult(
                request,
                ComplexMatrixQuantity(np.eye(4), Unitless()),
            )
        with pytest.raises(ValueError, match="energy unit"):
            FiniteDifferenceBlochHamiltonian2DResult(
                request,
                ComplexMatrixQuantity(np.eye(25), PhysicalUnit("joule")),
            )
        nonhermitian = np.eye(25, dtype=np.complex128)
        nonhermitian[0, 1] = 1.0
        with pytest.raises(ValueError, match="Hermitian"):
            FiniteDifferenceBlochHamiltonian2DResult(
                request,
                ComplexMatrixQuantity(nonhermitian, Unitless()),
            )
