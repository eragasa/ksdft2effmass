"""Software verification for the periodic2d plane-wave constructor."""

import numpy as np
import pytest

from ksdft2effmass.campaigns.periodic2d.model.toy_models import (
    Periodic2DCosinePotentialToyModel,
    Periodic2DPlaneWaveHamiltonianConstructor,
    Periodic2DPlaneWaveHamiltonianRequest,
    Periodic2DPlaneWaveHamiltonianResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DPlaneWaveHamiltonianConstructor:
    """Own represented-matrix and separable-operator evidence."""

    def test_execute_preserves_request_identity_and_kronecker_sum(self) -> None:
        """Zero mixed coupling gives the exact finite Kronecker-sum representation."""
        model = Periodic2DCosinePotentialToyModel(0.4, 0.7, 0.0)
        request = Periodic2DPlaneWaveHamiltonianRequest(model, 0.13, -0.21, 2)

        result = Periodic2DPlaneWaveHamiltonianConstructor().execute(request)

        indices = np.arange(-2, 3, dtype=np.float64)
        x_matrix = np.diag(np.square(0.13 + indices))
        x_matrix += np.diag(np.full(4, model.lambda_x / 2.0), 1)
        x_matrix += np.diag(np.full(4, model.lambda_x / 2.0), -1)
        y_matrix = np.diag(np.square(-0.21 + indices))
        y_matrix += np.diag(np.full(4, model.lambda_y / 2.0), 1)
        y_matrix += np.diag(np.full(4, model.lambda_y / 2.0), -1)
        expected = np.kron(x_matrix, np.eye(5)) + np.kron(np.eye(5), y_matrix)

        assert type(result) is Periodic2DPlaneWaveHamiltonianResult
        assert result.request is request
        assert result.matrix.shape == (25, 25)
        assert result.maximum_duality_residual <= request.duality_absolute_tolerance
        assert np.array_equal(result.matrix, result.matrix.conj().T)
        assert float(np.max(np.abs(result.matrix - expected))) < 2.0e-15
        assert not result.matrix.flags.writeable
