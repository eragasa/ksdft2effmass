"""Software verification for ``PlaneWaveBlochHamiltonian2DResult``."""

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)

from ksdft2effmass.analysis.model_systems import (
    PlaneWaveBlochHamiltonian2DModel,
    PlaneWaveBlochHamiltonian2DRequest,
    PlaneWaveBlochHamiltonian2DResult,
)
from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPlaneWaveBlochHamiltonian2DResult:
    """Own result correlation, dimension, unit, and residual evidence."""

    @staticmethod
    def request() -> PlaneWaveBlochHamiltonian2DRequest:
        """Return one zero-potential one-state request for result tests."""
        direct = DirectLattice2D(
            np.array((2.0 * np.pi, 0.0)),
            np.array((0.0, 2.0 * np.pi)),
        )
        reciprocal = ReciprocalLattice2D.from_direct_lattice(direct)
        model = PlaneWaveBlochHamiltonian2DModel(
            direct,
            reciprocal,
            0,
            (),
            ScalarQuantity(1.0, Unitless()),
            "state",
            "basis",
            "zero",
        )
        return PlaneWaveBlochHamiltonian2DRequest(model, (0.0, 0.0), 1.0e-14)

    def test_construction__incompatible_matrix_shape__raises_value_error(self) -> None:
        """A represented matrix must match the request's ordered basis dimension."""
        with pytest.raises(ValueError, match="shape"):
            PlaneWaveBlochHamiltonian2DResult(
                self.request(),
                0.0,
                ComplexMatrixQuantity(
                    np.eye(2, dtype=np.complex128),
                    Unitless(),
                ),
            )

    def test_construction__residual_above_tolerance__raises_value_error(self) -> None:
        """A result cannot retain a duality residual rejected by its request."""
        with pytest.raises(ValueError, match="exceeds"):
            PlaneWaveBlochHamiltonian2DResult(
                self.request(),
                2.0e-14,
                ComplexMatrixQuantity(
                    np.eye(1, dtype=np.complex128),
                    Unitless(),
                ),
            )
