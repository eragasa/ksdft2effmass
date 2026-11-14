"""Software verification for the periodic-2D cosine-potential model."""

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)

from ksdft2effmass.periodic.models import PeriodicModelRole
from ksdft2effmass.periodic.periodic2d.models import (
    Periodic2DCosinePotentialModel,
    Periodic2DModel,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DCosinePotentialModel:
    """Own explicit role, exact coupling type, and finite-value evidence."""

    def test_init_retains_finite_dimensionless_couplings(self) -> None:
        """Three finite built-in floats define the represented cosine potential."""
        model = Periodic2DCosinePotentialModel(
            0.4, 0.7, -0.2, role=PeriodicModelRole.CONTROL_MODEL
        )

        assert isinstance(model, Periodic2DModel)
        assert model.model_id == (
            "ksdft2effmass.periodic2d-cosine-potential-model.v1:"
            "role-control_model:"
            "lambda-x-0x1.999999999999ap-2:"
            "lambda-y-0x1.6666666666666p-1:"
            "lambda-xy--0x1.999999999999ap-3"
        )
        assert model.model_role is PeriodicModelRole.CONTROL_MODEL
        assert model.spatial_dimension == 2
        assert model.lambda_x == 0.4
        assert model.lambda_y == 0.7
        assert model.lambda_xy == -0.2

        material_reference = Periodic2DCosinePotentialModel(
            0.4,
            0.7,
            -0.2,
            role=PeriodicModelRole.MATERIAL_REFERENCE,
        )
        assert material_reference.model_role is PeriodicModelRole.MATERIAL_REFERENCE
        assert material_reference.model_id != model.model_id

    def test_lattices_form_the_two_pi_dual_square_cell(self) -> None:
        """PhysKit lattice owners expose ``A=2*pi*I`` and its dual ``B=I``."""
        model = Periodic2DCosinePotentialModel(
            0.4, 0.7, -0.2, role=PeriodicModelRole.CONTROL_MODEL
        )

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
        """Wrong role, boolean, and nonfinite values cannot enter the model."""
        with pytest.raises(TypeError, match="role must be PeriodicModelRole"):
            Periodic2DCosinePotentialModel(
                0.4,
                0.7,
                0.0,
                role="control_model",  # type: ignore[arg-type]
            )
        with pytest.raises(TypeError, match="lambda_x must be a float"):
            Periodic2DCosinePotentialModel(
                True, 0.7, 0.0, role=PeriodicModelRole.CONTROL_MODEL
            )
        with pytest.raises(ValueError, match="lambda_x must be finite"):
            Periodic2DCosinePotentialModel(
                float("nan"), 0.7, 0.0, role=PeriodicModelRole.CONTROL_MODEL
            )
