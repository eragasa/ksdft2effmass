"""Tests for the analytic higher-rank parent and frame-attack owner."""

import numpy as np
import pytest

from ksdft2effmass.periodic import (
    Periodic1DModel,
    PeriodicModelRole,
    PeriodicToyModelCatalog,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.model import (
    Periodic1DHigherRankAnalyticCaseConstructor,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DHigherRankAnalyticCase:
    """Establish the exact parent spectrum, gauge action, and oracle recovery."""

    def test__analytic_case__is_an_immutable_registered_periodic_toy_model(
        self,
    ) -> None:
        model = Periodic1DHigherRankAnalyticCaseConstructor(
            retained_rank=3,
            circuit_depth=1,
        ).execute()

        assert isinstance(model, Periodic1DModel)
        assert model.model_role is PeriodicModelRole.TOY
        assert model.model_id.endswith(":r03-L01")
        assert PeriodicToyModelCatalog((model,)).model_ids == (model.model_id,)
        with pytest.raises(ValueError):
            model.reference_frame.setflags(write=True)
        with pytest.raises(ValueError):
            model.endpoint_sewing_map.setflags(write=True)

    def test__analytic_case__recovers_the_reference_frame_and_operator(self) -> None:
        model = Periodic1DHigherRankAnalyticCaseConstructor(
            retained_rank=4,
            circuit_depth=8,
        ).execute()
        coordinates = np.linspace(-0.5, 0.5, 65, endpoint=False, dtype=np.float64)

        gauge = model.gauge_unitaries(coordinates)
        reference = model.reference_frames(coordinates)
        attacked_frame = model.attacked_frames(coordinates)
        exact = model.exact_reduced_hamiltonians(coordinates)
        attacked_operator = model.attacked_reduced_hamiltonians(coordinates)
        gauge_adjoint = np.swapaxes(gauge.conjugate(), -1, -2)

        assert (
            np.max(
                np.linalg.norm(
                    gauge_adjoint @ gauge - np.eye(4, dtype=np.complex128),
                    axis=(-2, -1),
                )
            )
            < 1.0e-12
        )
        np.testing.assert_allclose(
            attacked_frame @ gauge_adjoint,
            reference,
            rtol=0.0,
            atol=2.0e-15,
        )
        np.testing.assert_allclose(
            gauge @ attacked_operator @ gauge_adjoint,
            exact,
            rtol=0.0,
            atol=2.0e-15,
        )

    def test__analytic_case__uses_the_protocol_real_givens_angle(self) -> None:
        model = Periodic1DHigherRankAnalyticCaseConstructor(
            retained_rank=3,
            circuit_depth=1,
        ).execute()
        theta = 0.35 * (1.0 + 0.15 * (-0.5)) * 0.75
        expected = np.asarray(
            [
                [np.cos(theta), -np.sin(theta), 0.0],
                [np.sin(theta), np.cos(theta), 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.complex128,
        )

        gauge = model.gauge_unitaries(np.asarray([0.25], dtype=np.float64))[0]

        np.testing.assert_allclose(gauge, expected, rtol=0.0, atol=1.0e-15)
        assert np.max(np.abs(gauge.imag)) == 0.0
        assert np.linalg.det(gauge).real == pytest.approx(1.0, abs=1.0e-15)

    def test__analytic_case__uses_the_declared_retained_and_exterior_energies(
        self,
    ) -> None:
        model = Periodic1DHigherRankAnalyticCaseConstructor(
            retained_rank=3,
            circuit_depth=1,
        ).execute()
        coordinates = np.asarray([0.0], dtype=np.float64)

        np.testing.assert_allclose(
            model.retained_energies(coordinates),
            np.asarray([[-0.2, 0.25, 0.7]], dtype=np.float64),
            rtol=0.0,
            atol=0.0,
        )
        np.testing.assert_allclose(
            model.exterior_energies(coordinates),
            np.asarray([[2.8, 3.1, 3.4]], dtype=np.float64),
            rtol=0.0,
            atol=1.0e-15,
        )
        parent = model.parent_hamiltonians(coordinates)
        np.testing.assert_allclose(
            np.linalg.eigvalsh(parent)[0],
            np.asarray([-0.2, 0.25, 0.7, 2.8, 3.1, 3.4]),
            rtol=0.0,
            atol=1.0e-15,
        )
