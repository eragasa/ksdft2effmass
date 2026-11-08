"""Software verification for ``Periodic2DPlaneWaveBlochHamiltonianRequest``."""

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)
from projectkoios.physkit.units import (
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass.periodic.operators import PlaneWaveBasisCoordinate
from ksdft2effmass.periodic.periodic2d.models import (
    Periodic2DPlaneWaveBlochHamiltonianModel,
    Periodic2DPlaneWaveBlochHamiltonianRequest,
)
from ksdft2effmass.periodic.periodic2d.operators import Periodic2DBasisIdentity

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DPlaneWaveBlochHamiltonianRequest:
    """Own reduced-momentum and duality-tolerance input evidence."""

    @staticmethod
    def model() -> Periodic2DPlaneWaveBlochHamiltonianModel:
        """Return a zero-potential one-state model for request tests."""
        direct = DirectLattice2D(
            np.array((2.0 * np.pi, 0.0)),
            np.array((0.0, 2.0 * np.pi)),
        )
        reciprocal = ReciprocalLattice2D.from_direct_lattice(direct)
        return Periodic2DPlaneWaveBlochHamiltonianModel(
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
        request = Periodic2DPlaneWaveBlochHamiltonianRequest(
            self.model(), (0.25, -0.2), 1.0e-14
        )

        assert request.reduced_momentum == (0.25, -0.2)
        assert request.duality_absolute_tolerance == 1.0e-14

    def test_basis_identity__forwards_exact_model_coordinate_order(self) -> None:
        """The request correlates its matrix coordinates with the model basis value."""
        request = Periodic2DPlaneWaveBlochHamiltonianRequest(
            self.model(), (0.25, -0.2), 1.0e-14
        )

        assert type(request.basis_identity) is Periodic2DBasisIdentity
        assert request.basis_identity == request.model.basis_identity
        assert request.basis_identity.display_identifier == "basis"
        assert request.basis_identity.coordinates == (
            PlaneWaveBasisCoordinate(reciprocal_index=(0, 0)),
        )

    def test_construction__coercible_wrong_types__raises_type_error(self) -> None:
        """Boolean and NumPy scalar momentum components are not coerced."""
        with pytest.raises(TypeError, match="components"):
            Periodic2DPlaneWaveBlochHamiltonianRequest(
                self.model(),
                (True, 0.0),
                1.0e-14,
            )
        with pytest.raises(TypeError, match="components"):
            Periodic2DPlaneWaveBlochHamiltonianRequest(
                self.model(),
                (np.float64(0.0), 0.0),
                1.0e-14,
            )
