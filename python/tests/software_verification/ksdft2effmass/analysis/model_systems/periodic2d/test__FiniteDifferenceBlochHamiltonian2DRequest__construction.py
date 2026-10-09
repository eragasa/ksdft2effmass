"""Software verification of finite-difference Bloch-request construction.

Synthetic requests establish reduced-momentum typing and representable seam-phase
arguments. They do not establish physical momentum adequacy, continuum convergence,
scientific validation, uncertainty quantification, or acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import (
    FiniteDifferenceBlochHamiltonian2DModel,
    FiniteDifferenceBlochHamiltonian2DRequest,
    UniformPeriodicCoordinateBasis2D,
)
from ksdft2effmass.operators import MatrixQuantity, ScalarQuantity, Unitless

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestFiniteDifferenceBlochHamiltonian2DRequestConstruction:
    """Own model correlation, momentum, and Bloch-seam argument evidence."""

    @staticmethod
    def model(
        period: float = 2.0 * np.pi,
        kinetic_scale: float = 1.0,
    ) -> FiniteDifferenceBlochHamiltonian2DModel:
        """Return a synthetic model with caller-selected representable scales."""
        unit = Unitless()
        return FiniteDifferenceBlochHamiltonian2DModel(
            basis=UniformPeriodicCoordinateBasis2D(period, 5, "test.basis"),
            potential_samples=MatrixQuantity(np.zeros((5, 5)), unit),
            kinetic_scale=ScalarQuantity(kinetic_scale, unit),
            source_identifier="test.source",
            operator_identifier="test.operator",
            state_space_identifier="test.state-space",
            energy_reference="test.zero",
            provenance_identifier="test.provenance",
        )

    def test_construction_exposes_declared_conjugate_seam_phases(self) -> None:
        """Finite reduced momentum determines the two positive seam phases."""
        momentum = (0.13, -0.21)
        model = self.model()

        request = FiniteDifferenceBlochHamiltonian2DRequest(model, momentum)

        assert request.model is model
        assert request.boundary_phase_x == complex(
            np.exp(1j * momentum[0] * model.basis.coordinate_period)
        )
        assert request.boundary_phase_y == complex(
            np.exp(1j * momentum[1] * model.basis.coordinate_period)
        )

    def test_construction_rejects_mistyped_or_nonfinite_momentum(self) -> None:
        """Momentum requires an exact tuple of two finite built-in floats."""
        model = self.model()

        with pytest.raises(TypeError, match="two-component tuple"):
            FiniteDifferenceBlochHamiltonian2DRequest(
                model,
                [0.0, 0.0],  # type: ignore[arg-type]
            )
        with pytest.raises(TypeError, match="built-in floats"):
            FiniteDifferenceBlochHamiltonian2DRequest(
                model,
                (0, 0),  # type: ignore[arg-type]
            )
        with pytest.raises(ValueError, match="finite"):
            FiniteDifferenceBlochHamiltonian2DRequest(model, (float("nan"), 0.0))

    def test_construction_rejects_binary64_seam_argument_overflow(self) -> None:
        """Finite factors cannot silently compose an undefined nonfinite phase."""
        model = self.model(period=1.0e150, kinetic_scale=1.0e308)

        with pytest.raises(OverflowError, match="seam phase argument"):
            FiniteDifferenceBlochHamiltonian2DRequest(model, (1.0e200, 0.0))
