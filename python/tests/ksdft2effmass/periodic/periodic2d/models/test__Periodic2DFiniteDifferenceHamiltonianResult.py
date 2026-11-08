"""Software verification for represented periodic2d coordinate results."""

import numpy as np
import pytest

from ksdft2effmass.periodic.models import PeriodicModelRole
from ksdft2effmass.periodic.periodic2d.models import (
    Periodic2DCosinePotentialModel,
    Periodic2DFiniteDifferenceHamiltonianRequest,
    Periodic2DFiniteDifferenceHamiltonianResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DFiniteDifferenceHamiltonianResult:
    """Own coordinate-matrix-to-grid compatibility evidence."""

    def test_init_rejects_matrix_dimension_incompatible_with_request(self) -> None:
        """A square matrix must also match the declared coordinate grid."""
        request = Periodic2DFiniteDifferenceHamiltonianRequest(
            Periodic2DCosinePotentialModel(
                0.0, 0.0, 0.0, role=PeriodicModelRole.CONTROL_MODEL
            ),
            0.0,
            0.0,
            5,
        )

        with pytest.raises(ValueError, match="coordinate grid"):
            Periodic2DFiniteDifferenceHamiltonianResult(
                matrix=np.eye(4, dtype=np.complex128),
                request=request,
            )
