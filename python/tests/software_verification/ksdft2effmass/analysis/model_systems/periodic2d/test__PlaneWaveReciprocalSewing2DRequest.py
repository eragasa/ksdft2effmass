"""Software verification for ``PlaneWaveReciprocalSewing2DRequest``."""

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)

from ksdft2effmass.analysis.model_systems import (
    PlaneWaveBlochHamiltonian2DModel,
    PlaneWaveReciprocalSewing2DRequest,
    PositiveReciprocalDirection2D,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPlaneWaveReciprocalSewing2DRequest:
    """Own exact plane-wave model and direction request evidence."""

    @staticmethod
    def model() -> PlaneWaveBlochHamiltonian2DModel:
        """Return a cutoff-one square-lattice model for request tests."""
        direct = DirectLattice2D(
            np.array((2.0 * np.pi, 0.0)),
            np.array((0.0, 2.0 * np.pi)),
        )
        return PlaneWaveBlochHamiltonian2DModel(
            direct,
            ReciprocalLattice2D.from_direct_lattice(direct),
            1,
            (),
            ScalarQuantity(1.0, Unitless()),
            "state",
            "basis",
            "zero",
        )

    def test_construction__enum_direction__retains_exact_model(self) -> None:
        """The request retains the complete model and exact direction enum."""
        model = self.model()
        request = PlaneWaveReciprocalSewing2DRequest(
            model, PositiveReciprocalDirection2D.FIRST
        )

        assert request.model is model
        assert request.direction is PositiveReciprocalDirection2D.FIRST

    def test_construction__string_direction__raises_type_error(self) -> None:
        """An enum-like string is not coerced into a sewing direction."""
        with pytest.raises(TypeError, match="direction"):
            PlaneWaveReciprocalSewing2DRequest(
                self.model(),
                "plus_first_reciprocal_vector",  # type: ignore[arg-type]
            )
