"""Software verification for periodic2d finite-difference requests."""

import numpy as np
import pytest

from ksdft2effmass.periodic2d.model.toy_models import (
    Periodic2DCosinePotentialToyModel,
    Periodic2DFiniteDifferenceHamiltonianRequest,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DFiniteDifferenceHamiltonianRequest:
    """Own coordinate-grid and Bloch-fiber identity evidence."""

    @staticmethod
    def model() -> Periodic2DCosinePotentialToyModel:
        """Return one finite dimensionless cosine model."""
        return Periodic2DCosinePotentialToyModel(0.4, 0.7, 0.1)

    def test_properties_define_grid_order_and_positive_seam_phases(self) -> None:
        """The request exposes its grid geometry and positive-direction seam phases."""
        request = Periodic2DFiniteDifferenceHamiltonianRequest(
            self.model(), 0.13, -0.21, 7
        )

        assert request.grid.points_per_direction == 7
        assert request.site_ordering == "x_outer_y_inner"
        assert request.represented_dimension == 49
        assert request.period == 2.0 * np.pi
        assert request.spacing == request.period / 7
        assert request.boundary_phase_x == complex(np.exp(1j * 0.13 * 2.0 * np.pi))
        assert request.boundary_phase_y == complex(np.exp(-1j * 0.21 * 2.0 * np.pi))

    def test_init_rejects_wrong_scalar_types_and_even_grids(self) -> None:
        """The public boundary rejects coercible values and invalid grid parity."""
        with pytest.raises(TypeError, match="reduced_momentum_x"):
            Periodic2DFiniteDifferenceHamiltonianRequest(
                self.model(),
                np.float64(0.0),
                0.0,
                7,
            )
        with pytest.raises(TypeError, match="points_per_direction"):
            Periodic2DFiniteDifferenceHamiltonianRequest(
                self.model(),
                0.0,
                0.0,
                True,
            )
        with pytest.raises(ValueError, match="odd and at least five"):
            Periodic2DFiniteDifferenceHamiltonianRequest(self.model(), 0.0, 0.0, 6)
