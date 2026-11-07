"""Software verification for the periodic2d finite-difference Hamiltonian."""

import numpy as np
import pytest

from ksdft2effmass.periodic.periodic2d.models.control_models import (
    Periodic2DCosinePotentialControlModel,
    Periodic2DFiniteDifferenceHamiltonian,
    Periodic2DFiniteDifferenceHamiltonianRequest,
    Periodic2DFiniteDifferenceHamiltonianResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DFiniteDifferenceHamiltonian:
    """Own request binding, ordering, seam-phase, and Hermiticity evidence."""

    def test__Periodic2DFiniteDifferenceHamiltonian__result__preserves_request_identity_and_bloch_seams(  # noqa: E501
        self,
    ) -> None:
        """Flattened seam entries implement the declared conjugate Bloch phases."""
        model = Periodic2DCosinePotentialControlModel(0.0, 0.0, 0.0)
        request = Periodic2DFiniteDifferenceHamiltonianRequest(model, 0.13, -0.21, 7)

        hamiltonian = Periodic2DFiniteDifferenceHamiltonian(request)
        result = hamiltonian.result()

        seam_coefficient = -1.0 / request.spacing**2
        x_negative_seam = seam_coefficient * request.boundary_phase_x.conjugate()
        y_negative_seam = seam_coefficient * request.boundary_phase_y.conjugate()
        assert hamiltonian.request is request
        assert type(result) is Periodic2DFiniteDifferenceHamiltonianResult
        assert result.request is request
        assert result.matrix.shape == (49, 49)
        assert np.array_equal(result.matrix, result.matrix.conj().T)
        assert result.matrix[0, 42] == x_negative_seam
        assert result.matrix[0, 6] == y_negative_seam
        assert not result.matrix.flags.writeable

    def test__Periodic2DFiniteDifferenceHamiltonian__construction__rejects_other_request_types(  # noqa: E501
        self,
    ) -> None:
        """The represented Hamiltonian admits only its exact request owner."""
        with pytest.raises(
            TypeError, match="Periodic2DFiniteDifferenceHamiltonianRequest"
        ):
            Periodic2DFiniteDifferenceHamiltonian(None)  # type: ignore[arg-type]
