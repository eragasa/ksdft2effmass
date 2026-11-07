"""Software verification for the periodic2d plane-wave Hamiltonian."""

import numpy as np
import pytest

from ksdft2effmass.periodic.periodic2d.models.control_models import (
    Periodic2DCosinePotentialControlModel,
    Periodic2DPlaneWaveHamiltonian,
    Periodic2DPlaneWaveHamiltonianRequest,
    Periodic2DPlaneWaveHamiltonianResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DPlaneWaveHamiltonian:
    """Own request binding, represented-matrix, and separable-operator evidence."""

    def test__Periodic2DPlaneWaveHamiltonian__result__preserves_request_identity_and_kronecker_sum(  # noqa: E501
        self,
    ) -> None:
        """Zero mixed coupling gives the exact finite Kronecker-sum representation."""
        model = Periodic2DCosinePotentialControlModel(0.4, 0.7, 0.0)
        request = Periodic2DPlaneWaveHamiltonianRequest(model, 0.13, -0.21, 2)

        hamiltonian = Periodic2DPlaneWaveHamiltonian(request)
        result = hamiltonian.result()

        indices = np.arange(-2, 3, dtype=np.float64)
        x_matrix = np.diag(np.square(0.13 + indices))
        x_matrix += np.diag(np.full(4, model.lambda_x / 2.0), 1)
        x_matrix += np.diag(np.full(4, model.lambda_x / 2.0), -1)
        y_matrix = np.diag(np.square(-0.21 + indices))
        y_matrix += np.diag(np.full(4, model.lambda_y / 2.0), 1)
        y_matrix += np.diag(np.full(4, model.lambda_y / 2.0), -1)
        expected = np.kron(x_matrix, np.eye(5)) + np.kron(np.eye(5), y_matrix)

        assert hamiltonian.request is request
        assert type(result) is Periodic2DPlaneWaveHamiltonianResult
        assert result.request is request
        assert result.matrix.shape == (25, 25)
        assert result.maximum_duality_residual <= request.duality_absolute_tolerance
        assert np.array_equal(result.matrix, result.matrix.conj().T)
        assert float(np.max(np.abs(result.matrix - expected))) < 2.0e-15
        assert not result.matrix.flags.writeable

    def test__Periodic2DPlaneWaveHamiltonian__construction__rejects_other_request_types(
        self,
    ) -> None:
        """The represented Hamiltonian admits only its exact request owner."""
        with pytest.raises(TypeError, match="Periodic2DPlaneWaveHamiltonianRequest"):
            Periodic2DPlaneWaveHamiltonian(None)  # type: ignore[arg-type]
