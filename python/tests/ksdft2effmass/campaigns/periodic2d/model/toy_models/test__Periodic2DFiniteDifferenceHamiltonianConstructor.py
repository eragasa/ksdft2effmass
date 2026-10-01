"""Software verification for the periodic2d finite-difference constructor."""

import numpy as np
import pytest

from ksdft2effmass.campaigns.periodic2d.model.toy_models import (
    Periodic2DCosinePotentialToyModel,
    Periodic2DFiniteDifferenceHamiltonianConstructor,
    Periodic2DFiniteDifferenceHamiltonianRequest,
    Periodic2DFiniteDifferenceHamiltonianResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DFiniteDifferenceHamiltonianConstructor:
    """Own coordinate ordering, seam phase, and Hermiticity evidence."""

    def test_execute_preserves_request_identity_and_bloch_seams(self) -> None:
        """Flattened seam entries implement the declared conjugate Bloch phases."""
        model = Periodic2DCosinePotentialToyModel(0.0, 0.0, 0.0)
        request = Periodic2DFiniteDifferenceHamiltonianRequest(model, 0.13, -0.21, 7)

        result = Periodic2DFiniteDifferenceHamiltonianConstructor().execute(request)

        seam_coefficient = -1.0 / request.spacing**2
        x_negative_seam = seam_coefficient * request.boundary_phase_x.conjugate()
        y_negative_seam = seam_coefficient * request.boundary_phase_y.conjugate()
        assert type(result) is Periodic2DFiniteDifferenceHamiltonianResult
        assert result.request is request
        assert result.matrix.shape == (49, 49)
        assert np.array_equal(result.matrix, result.matrix.conj().T)
        assert result.matrix[0, 42] == x_negative_seam
        assert result.matrix[0, 6] == y_negative_seam
        assert not result.matrix.flags.writeable
