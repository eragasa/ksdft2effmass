"""Software verification for ``PlaneWaveBlochHamiltonian2DRequest``."""

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)

from ksdft2effmass.analysis.model_systems import (
    PlaneWaveBlochHamiltonian2DModel,
    PlaneWaveBlochHamiltonian2DRequest,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPlaneWaveBlochHamiltonian2DRequest:
    """Own reduced-momentum and duality-tolerance input evidence."""

    @staticmethod
    def model() -> PlaneWaveBlochHamiltonian2DModel:
        """Return a zero-potential one-state model for request tests."""
        direct = DirectLattice2D(
            np.array((2.0 * np.pi, 0.0)),
            np.array((0.0, 2.0 * np.pi)),
        )
        reciprocal = ReciprocalLattice2D.from_direct_lattice(direct)
        return PlaneWaveBlochHamiltonian2DModel(
            direct,
            reciprocal,
            0,
            (),
            ScalarQuantity(1.0, Unitless()),
            "state",
            "basis",
            "zero",
        )

    def test_fields__finite_reduced_momentum__retains_primitive_coordinates(
        self,
    ) -> None:
        """Finite reduced coordinates and tolerance are retained without conversion."""
        request = PlaneWaveBlochHamiltonian2DRequest(
            self.model(), (0.25, -0.2), 1.0e-14
        )

        assert request.reduced_momentum == (0.25, -0.2)
        assert request.duality_absolute_tolerance == 1.0e-14

    def test_construction__coercible_wrong_types__raises_type_error(self) -> None:
        """Boolean and NumPy scalar momentum components are not coerced."""
        with pytest.raises(TypeError, match="components"):
            PlaneWaveBlochHamiltonian2DRequest(
                self.model(),
                (True, 0.0),
                1.0e-14,  # type: ignore[arg-type]
            )
        with pytest.raises(TypeError, match="components"):
            PlaneWaveBlochHamiltonian2DRequest(
                self.model(),
                (np.float64(0.0), 0.0),
                1.0e-14,  # type: ignore[arg-type]
            )
