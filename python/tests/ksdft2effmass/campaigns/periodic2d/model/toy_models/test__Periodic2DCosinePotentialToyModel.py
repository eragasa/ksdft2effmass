"""Software verification for the periodic2d cosine-potential toy model."""

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)

from ksdft2effmass.campaigns.periodic2d.model.toy_models import (
    Periodic2DCosinePotentialToyModel,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DCosinePotentialToyModel:
    """Own exact coupling-type and finite-value evidence for the toy model."""

    def test_init_retains_finite_dimensionless_couplings(self) -> None:
        """Three finite built-in floats define the represented cosine potential."""
        model = Periodic2DCosinePotentialToyModel(0.4, 0.7, -0.2)

        assert model.lambda_x == 0.4
        assert model.lambda_y == 0.7
        assert model.lambda_xy == -0.2

    def test_lattices_form_the_two_pi_dual_square_cell(self) -> None:
        """PhysKit lattice owners expose ``A=2*pi*I`` and its dual ``B=I``."""
        model = Periodic2DCosinePotentialToyModel(0.4, 0.7, -0.2)

        direct = model.direct_lattice
        reciprocal = model.reciprocal_lattice

        assert type(direct) is DirectLattice2D
        assert type(reciprocal) is ReciprocalLattice2D
        assert np.array_equal(direct.A, 2.0 * np.pi * np.eye(2))
        assert np.array_equal(reciprocal.B, np.eye(2))
        assert np.array_equal(direct.A.T @ reciprocal.B, 2.0 * np.pi * np.eye(2))
        assert not direct.A.flags.writeable
        assert not reciprocal.B.flags.writeable

    def test_init_rejects_boolean_and_nonfinite_couplings(self) -> None:
        """Boolean and nonfinite values cannot enter the numerical model."""
        with pytest.raises(TypeError, match="lambda_x must be a float"):
            Periodic2DCosinePotentialToyModel(True, 0.7, 0.0)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="lambda_x must be finite"):
            Periodic2DCosinePotentialToyModel(float("nan"), 0.7, 0.0)
