"""Software verification for the periodic2d cosine-potential toy model.

The synthetic tests establish exact nominal identity, dimensionless coupling storage,
strict scalar validation, and the fixed period-``2*pi`` direct/reciprocal lattice
convention. They do not establish a material Hamiltonian, discretization convergence,
scientific validation, or uncertainty quantification.
"""

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)

from ksdft2effmass.periodic import Periodic2DModel, PeriodicModelRole
from ksdft2effmass.periodic2d.model.toy_models import (
    Periodic2DCosinePotentialToyModel,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DCosinePotentialToyModel:
    """Own exact coupling-type and finite-value evidence for the toy model."""

    def test_init_retains_finite_dimensionless_couplings(self) -> None:
        """Finite couplings retain the configured parent and exact toy identity.

        The three authored built-in floats are synthetic dimensionless model inputs.
        Exact equality is the oracle because construction stores them without numerical
        transformation.
        """
        model = Periodic2DCosinePotentialToyModel(0.4, 0.7, -0.2)

        assert model.lambda_x == 0.4
        assert model.lambda_y == 0.7
        assert model.lambda_xy == -0.2
        assert isinstance(model, Periodic2DModel)
        assert model.model_id == "periodic2d.cosine-potential-toy"
        assert model.model_role is PeriodicModelRole.TOY
        assert model.spatial_dimension == 2

    def test_lattices_form_the_two_pi_dual_square_cell(self) -> None:
        """PhysKit owners expose the fixed ``A=2*pi*I`` and ``B=I`` convention.

        Exact analytic arrays provide the oracle for the dimensionless square cell and
        its two-pi dual. This verifies convention mapping, not a material lattice.
        """
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
        """Boolean and nonfinite values cannot enter the parent-model inputs.

        The negative cases establish the exact public scalar boundary and finite-value
        invariant; they do not test a physical range for the coupling coefficients.
        """
        with pytest.raises(TypeError, match="lambda_x must be a float"):
            Periodic2DCosinePotentialToyModel(True, 0.7, 0.0)
        with pytest.raises(ValueError, match="lambda_x must be finite"):
            Periodic2DCosinePotentialToyModel(float("nan"), 0.7, 0.0)
