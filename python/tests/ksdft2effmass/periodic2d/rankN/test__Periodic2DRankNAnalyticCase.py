"""Periodic-2D arbitrary-rank parent, gauge, and case-composition contracts."""

from __future__ import annotations

import math

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Float64Array

from ksdft2effmass.periodic.models import PeriodicModelRole
from ksdft2effmass.periodic.operators import (
    LabeledComponentBasisCoordinate,
    PeriodicBasisInventory,
    PeriodicBasisInventoryEntry,
)
from ksdft2effmass.periodic.periodic2d.operators import Periodic2DBasisIdentity
from ksdft2effmass.periodic.periodic2d.rankN.models import (
    Periodic2DRankNAnalyticParentModel,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.case import (
    Periodic2DRankNAnalyticCase,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.transformation import (
    Periodic2DRankNGaugeNormalizationEnum,
    Periodic2DRankNGivensGaugeTransformation,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]

_TEST_BASIS_INVENTORY = PeriodicBasisInventory(
    entries=tuple(
        PeriodicBasisInventoryEntry(
            retained_rank=rank,
            basis_identity=Periodic2DBasisIdentity(
                display_identifier=f"periodic2d-rankN-test-basis-r{rank}",
                coordinates=tuple(
                    LabeledComponentBasisCoordinate(
                        label=f"test-retained-orbital-{index:02d}"
                    )
                    for index in range(rank)
                ),
            ),
        )
        for rank in (3, 4, 8)
    )
)


class TestPeriodic2DRankNAnalyticCase:
    """Qualify separated parent, gauge transformation, and study-case composition."""

    @staticmethod
    def _coordinates() -> Float64Array:
        first = np.arange(3, dtype=np.float64) / 3.0
        second = np.arange(4, dtype=np.float64) / 4.0
        mesh = np.stack(np.meshgrid(first, second, indexing="ij"), axis=-1)
        return np.asarray(mesh, dtype=np.float64)

    @staticmethod
    def _case(retained_rank: int = 3) -> Periodic2DRankNAnalyticCase:
        bonds = ((1, 0), (0, 1))
        return Periodic2DRankNAnalyticCase(
            case_identifier="square-axis-control",
            parent_model=Periodic2DRankNAnalyticParentModel(
                retained_rank=retained_rank,
                positive_bonds=bonds,
                parent_scale=1.0,
                basis=(_TEST_BASIS_INVENTORY.basis_identity_for_rank(retained_rank)),
                role=PeriodicModelRole.CONTROL_MODEL,
            ),
            gauge_transformation=Periodic2DRankNGivensGaugeTransformation(
                retained_rank=retained_rank,
                circuit_depth=2,
                harmonic_bonds=bonds,
                normalization=Periodic2DRankNGaugeNormalizationEnum.AXIS_MAXIMUM,
                coefficient=math.pi / 4.0,
            ),
        )

    def test_parent_has_selected_shape_ordering_gap_and_basis(self) -> None:
        case = self._case(retained_rank=4)
        coordinates = self._coordinates()

        retained = case.retained_energies(coordinates)
        exterior = case.exterior_energies(coordinates)
        parent = case.parent_hamiltonians(coordinates)
        frame = case.reference_frames(coordinates)

        assert case.ambient_dimension == 8
        assert case.parent_model.model_role is PeriodicModelRole.CONTROL_MODEL
        assert case.basis_identity.dimension == 4
        assert retained.shape == (3, 4, 4)
        assert exterior.shape == (3, 4, 4)
        assert parent.shape == (3, 4, 8, 8)
        assert frame.shape == (3, 4, 8, 4)
        assert float(np.min(np.diff(retained, axis=-1))) > 0.0
        sampled_gap = float(np.min(exterior[..., 0] - retained[..., -1]))
        assert sampled_gap >= case.EXTERNAL_GAP_LOWER_BOUND - 1.0e-15
        projected = np.swapaxes(frame.conjugate(), -1, -2) @ parent @ frame
        assert projected == pytest.approx(case.exact_reduced_hamiltonians(coordinates))
        assert not parent.flags.writeable
        assert not frame.flags.writeable

    def test_gauge_is_special_unitary_and_oracle_restores_reference(self) -> None:
        case = self._case()
        coordinates = self._coordinates()

        gauge = case.gauge_unitaries(coordinates)
        inverse = case.known_inverse_right_actions(coordinates)
        gauge_transformed_frame = case.gauge_transformed_frames(coordinates)
        gauge_transformed_operator = case.gauge_transformed_reduced_hamiltonians(
            coordinates
        )
        identity = np.eye(case.retained_rank, dtype=np.complex128)

        assert np.swapaxes(gauge.conjugate(), -1, -2) @ gauge == pytest.approx(
            np.broadcast_to(identity, gauge.shape), abs=2.0e-15
        )
        assert np.linalg.det(gauge) == pytest.approx(
            np.ones(coordinates.shape[:-1]), abs=2.0e-15
        )
        assert gauge_transformed_frame @ inverse == pytest.approx(
            case.reference_frames(coordinates), abs=2.0e-15
        )
        assert (
            np.swapaxes(inverse.conjugate(), -1, -2)
            @ gauge_transformed_operator
            @ inverse
        ) == pytest.approx(case.exact_reduced_hamiltonians(coordinates), abs=2.0e-15)
        assert not gauge.flags.writeable

    def test_gauge_transformation_supports_rank_two_with_even_circuit_depth(
        self,
    ) -> None:
        transformation = Periodic2DRankNGivensGaugeTransformation(
            retained_rank=2,
            circuit_depth=2,
            harmonic_bonds=((1, 0), (0, 1)),
            normalization=Periodic2DRankNGaugeNormalizationEnum.AXIS_MAXIMUM,
            coefficient=0.2,
        )

        gauge = transformation.unitaries(self._coordinates())

        assert gauge.shape == (3, 4, 2, 2)
        assert np.swapaxes(gauge.conjugate(), -1, -2) @ gauge == pytest.approx(
            np.broadcast_to(np.eye(2, dtype=np.complex128), gauge.shape),
            abs=2.0e-15,
        )

    def test_rejects_parent_transformation_mismatch_and_transformation_bound(
        self,
    ) -> None:
        case = self._case()
        with pytest.raises(ValueError, match=r"shape \(\.\.\., 2\)"):
            case.parent_hamiltonians(np.zeros((2, 2, 3), dtype=np.float64))

        with pytest.raises(ValueError, match="retained ranks"):
            Periodic2DRankNAnalyticCase(
                case_identifier="mismatched-rank",
                parent_model=case.parent_model,
                gauge_transformation=Periodic2DRankNGivensGaugeTransformation(
                    retained_rank=4,
                    circuit_depth=1,
                    harmonic_bonds=case.positive_bonds,
                    normalization=(Periodic2DRankNGaugeNormalizationEnum.AXIS_MAXIMUM),
                    coefficient=0.0,
                ),
            )

        with pytest.raises(ValueError, match="pi/4"):
            Periodic2DRankNGivensGaugeTransformation(
                retained_rank=3,
                circuit_depth=1,
                harmonic_bonds=((1, 0), (0, 1), (1, -1)),
                normalization=Periodic2DRankNGaugeNormalizationEnum.BOND_RMS,
                coefficient=math.pi / 4.0,
            )
