"""Software verification for the periodic2d finite-difference constructor."""

import numpy as np
import pytest

from ksdft2effmass.periodic2d.model.toy_models import (
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

    def test_execute_preserves_the_established_cosine_matrix_values(self) -> None:
        """Reusable delegation is exactly equal to the prior explicit formula."""
        model = Periodic2DCosinePotentialToyModel(0.4, -0.7, 0.3)
        request = Periodic2DFiniteDifferenceHamiltonianRequest(model, 0.13, -0.21, 5)

        result = Periodic2DFiniteDifferenceHamiltonianConstructor().execute(request)

        points = request.points_per_direction
        spacing = request.spacing
        off_diagonal = -1.0 / spacing**2
        kinetic_blocks = []
        for momentum in (request.reduced_momentum_x, request.reduced_momentum_y):
            block = np.diag(np.full(points, 2.0 / spacing**2)).astype(np.complex128)
            block += np.diag(np.full(points - 1, off_diagonal), 1)
            block += np.diag(np.full(points - 1, off_diagonal), -1)
            block[0, -1] = off_diagonal * np.exp(-1j * momentum * request.period)
            block[-1, 0] = off_diagonal * np.exp(1j * momentum * request.period)
            kinetic_blocks.append(block)
        identity = np.eye(points, dtype=np.complex128)
        expected = np.kron(kinetic_blocks[0], identity) + np.kron(
            identity, kinetic_blocks[1]
        )
        coordinate = np.arange(points, dtype=np.float64) * request.period / points
        potential = (
            model.lambda_x * np.cos(coordinate)[:, None]
            + model.lambda_y * np.cos(coordinate)[None, :]
            + model.lambda_xy
            * np.cos(coordinate)[:, None]
            * np.cos(coordinate)[None, :]
        )
        expected += np.diag(potential.ravel())

        assert result.request is request
        assert np.array_equal(result.matrix, expected)
