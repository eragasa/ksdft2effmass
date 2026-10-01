"""Software verification for represented periodic2d plane-wave results."""

import numpy as np
import pytest

from ksdft2effmass.campaigns.periodic2d.model.toy_models import (
    Periodic2DCosinePotentialToyModel,
    Periodic2DPlaneWaveHamiltonianRequest,
    Periodic2DPlaneWaveHamiltonianResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DPlaneWaveHamiltonianResult:
    """Own plane-wave matrix-to-basis compatibility evidence."""

    def test_init_rejects_matrix_dimension_incompatible_with_request(self) -> None:
        """Equal square dimensions are insufficient when the basis has another size."""
        request = Periodic2DPlaneWaveHamiltonianRequest(
            Periodic2DCosinePotentialToyModel(0.0, 0.0, 0.0), 0.0, 0.0, 1
        )

        with pytest.raises(ValueError, match="plane-wave basis"):
            Periodic2DPlaneWaveHamiltonianResult(
                matrix=np.eye(4, dtype=np.complex128),
                request=request,
                maximum_duality_residual=0.0,
            )

    def test_init_rejects_duality_residual_above_request_tolerance(self) -> None:
        """The adapter result retains the generic constructor's duality evidence."""
        request = Periodic2DPlaneWaveHamiltonianRequest(
            Periodic2DCosinePotentialToyModel(0.0, 0.0, 0.0), 0.0, 0.0, 0
        )

        with pytest.raises(ValueError, match="exceeds"):
            Periodic2DPlaneWaveHamiltonianResult(
                matrix=np.eye(1, dtype=np.complex128),
                request=request,
                maximum_duality_residual=5.0e-15,
            )
