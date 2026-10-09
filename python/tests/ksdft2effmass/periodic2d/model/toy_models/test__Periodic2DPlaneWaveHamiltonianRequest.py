"""Software verification for periodic2d plane-wave requests."""

import numpy as np
import pytest

from ksdft2effmass.periodic2d.model.toy_models import (
    Periodic2DCosinePotentialToyModel,
    Periodic2DPlaneWaveHamiltonianRequest,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DPlaneWaveHamiltonianRequest:
    """Own reciprocal-basis identity and runtime-input evidence."""

    @staticmethod
    def model() -> Periodic2DCosinePotentialToyModel:
        """Return one finite dimensionless cosine model."""
        return Periodic2DCosinePotentialToyModel(0.4, 0.7, 0.1)

    def test_properties_define_p_outer_q_inner_basis_order(self) -> None:
        """The cutoff determines one explicit ordered reciprocal basis."""
        request = Periodic2DPlaneWaveHamiltonianRequest(self.model(), 0.13, -0.21, 1)

        assert request.basis.cutoff == 1
        assert request.duality_absolute_tolerance == 4.0e-15
        assert request.basis_ordering == "p_outer_q_inner"
        assert request.represented_dimension == 9
        assert request.reciprocal_indices == (
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 0),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        )

    def test_init_rejects_coercible_non_builtin_numeric_values(self) -> None:
        """Booleans, numeric strings, and NumPy scalars are not coerced."""
        with pytest.raises(TypeError, match="reduced_momentum_x"):
            Periodic2DPlaneWaveHamiltonianRequest(
                self.model(),
                np.float64(0.0),
                0.0,
                1,
            )
        with pytest.raises(TypeError, match="reduced_momentum_x"):
            Periodic2DPlaneWaveHamiltonianRequest(
                self.model(),
                "0.0",  # type: ignore[arg-type]
                0.0,
                1,
            )
        with pytest.raises(TypeError, match="cutoff"):
            Periodic2DPlaneWaveHamiltonianRequest(
                self.model(),
                0.0,
                0.0,
                True,
            )
        with pytest.raises(TypeError, match="duality_absolute_tolerance"):
            Periodic2DPlaneWaveHamiltonianRequest(
                self.model(),
                0.0,
                0.0,
                1,
                True,
            )
