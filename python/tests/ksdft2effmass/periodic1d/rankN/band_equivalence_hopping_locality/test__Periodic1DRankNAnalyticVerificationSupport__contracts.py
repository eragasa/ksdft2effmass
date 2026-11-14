"""Tests for the analytic higher-rank parent and frame-transformation owner."""

import importlib.util

import numpy as np
import pytest

from ksdft2effmass.periodic.catalog import PeriodicControlModelCatalog
from ksdft2effmass.periodic.models import PeriodicModelRole
from ksdft2effmass.periodic.operators import LabeledComponentBasisCoordinate
from ksdft2effmass.periodic.periodic1d.models import Periodic1DModel
from ksdft2effmass.periodic.periodic1d.rankN.models import (
    Periodic1DRankNModel,
    Periodic1DRankNParentModel,
)
from periodic1d_rankn_analytic_case_support import (
    SyntheticPeriodic1DRankNAnalyticCaseConstructor,
)
from periodic1d_rankn_analytic_oracle import analytic_fourier_givens_transformation
from periodic1d_rankn_control_basis_support import synthetic_basis_identity

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRankNAnalyticVerificationSupport:
    """Establish the exact parent spectrum, gauge action, and oracle recovery."""

    def test__Periodic1DRankNAnalyticCase__parent__is_the_registered_control_model(
        self,
    ) -> None:
        """Keep study composition separate from reusable parent-model identity."""
        model = SyntheticPeriodic1DRankNAnalyticCaseConstructor(
            retained_rank=3,
            circuit_depth=1,
            basis_identity=synthetic_basis_identity(3),
            gauge_transformation=analytic_fourier_givens_transformation(
                retained_rank=3,
                circuit_depth=1,
            ),
        ).execute()

        parent = model.parent_model

        assert not isinstance(model, Periodic1DModel)
        assert isinstance(parent, Periodic1DModel)
        assert isinstance(parent, Periodic1DRankNModel)
        assert isinstance(parent, Periodic1DRankNParentModel)
        assert parent.model_role is PeriodicModelRole.CONTROL_MODEL
        assert parent.model_id.endswith(":r03")
        assert model.basis_identity.dimension == model.band_subspace_rank == 3
        assert model.basis_identity.coordinates == (
            LabeledComponentBasisCoordinate(label="test-orbital-a"),
            LabeledComponentBasisCoordinate(label="test-orbital-b"),
            LabeledComponentBasisCoordinate(label="test-orbital-c"),
        )
        assert PeriodicControlModelCatalog((parent,)).model_ids == (parent.model_id,)
        with pytest.raises(ValueError):
            parent.reference_frame.setflags(write=True)
        with pytest.raises(ValueError):
            model.endpoint_sewing_map.setflags(write=True)

    def test__analytic_parent_formula__is_not_source_owned(self) -> None:
        """Keep the exact analytic family in calculation and verification support."""
        assert (
            importlib.util.find_spec(
                "ksdft2effmass.periodic.periodic1d.rankN.models.analytic"
            )
            is None
        )

    def test__constructor__rejects_a_basis_from_a_different_rank(self) -> None:
        """Require calculation composition to provide the exact structured basis."""
        with pytest.raises(ValueError, match="dimension must equal retained_rank"):
            SyntheticPeriodic1DRankNAnalyticCaseConstructor(
                retained_rank=4,
                circuit_depth=1,
                basis_identity=synthetic_basis_identity(3),
                gauge_transformation=analytic_fourier_givens_transformation(
                    retained_rank=4,
                    circuit_depth=1,
                ),
            ).execute()

    def test__Periodic1DRankNAnalyticCase__analytic_case__recovers_the_reference_frame_and_operator(  # noqa: E501
        self,
    ) -> None:
        """Verify analytic case recovers the reference frame and operator."""
        model = SyntheticPeriodic1DRankNAnalyticCaseConstructor(
            retained_rank=4,
            circuit_depth=8,
            basis_identity=synthetic_basis_identity(4),
            gauge_transformation=analytic_fourier_givens_transformation(
                retained_rank=4,
                circuit_depth=8,
            ),
        ).execute()
        coordinates = np.linspace(-0.5, 0.5, 65, endpoint=False, dtype=np.float64)

        gauge = model.gauge_transformation_unitaries(coordinates)
        reference = model.reference_frames(coordinates)
        gauge_transformed_frame = model.gauge_transformed_frames(coordinates)
        exact = model.exact_reduced_hamiltonians(coordinates)
        gauge_transformed_operator = model.gauge_transformed_reduced_hamiltonians(
            coordinates
        )
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
            gauge_transformed_frame @ gauge_adjoint,
            reference,
            rtol=0.0,
            atol=2.0e-15,
        )
        np.testing.assert_allclose(
            gauge @ gauge_transformed_operator @ gauge_adjoint,
            exact,
            rtol=0.0,
            atol=2.0e-15,
        )

    def test__Periodic1DRankNAnalyticCase__analytic_case__uses_the_protocol_real_givens_angle(  # noqa: E501
        self,
    ) -> None:
        """Verify analytic case uses the protocol real givens angle."""
        model = SyntheticPeriodic1DRankNAnalyticCaseConstructor(
            retained_rank=3,
            circuit_depth=1,
            basis_identity=synthetic_basis_identity(3),
            gauge_transformation=analytic_fourier_givens_transformation(
                retained_rank=3,
                circuit_depth=1,
            ),
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

        gauge = model.gauge_transformation_unitaries(
            np.asarray([0.25], dtype=np.float64)
        )[0]

        np.testing.assert_allclose(gauge, expected, rtol=0.0, atol=1.0e-15)
        assert np.max(np.abs(gauge.imag)) == 0.0
        assert np.linalg.det(gauge).real == pytest.approx(1.0, abs=1.0e-15)

    def test__Periodic1DRankNAnalyticCase__analytic_case__uses_the_declared_retained_and_exterior_energies(  # noqa: E501
        self,
    ) -> None:
        """Verify analytic case uses the declared retained and exterior energies."""
        model = SyntheticPeriodic1DRankNAnalyticCaseConstructor(
            retained_rank=3,
            circuit_depth=1,
            basis_identity=synthetic_basis_identity(3),
            gauge_transformation=analytic_fourier_givens_transformation(
                retained_rank=3,
                circuit_depth=1,
            ),
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
