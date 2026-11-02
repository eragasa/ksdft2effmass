"""Periodic-2D arbitrary-rank analytic parent and gauge-circuit contracts."""

from __future__ import annotations

import math

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Float64Array

from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.model import (
    Periodic2DRankNAnalyticCase,
    Periodic2DRankNGaugeNormalizationEnum,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DRankNAnalyticCase:
    """Qualify exact model structure without presenting a calculated study result."""

    @staticmethod
    def _coordinates() -> Float64Array:
        first = np.arange(3, dtype=np.float64) / 3.0
        second = np.arange(4, dtype=np.float64) / 4.0
        mesh = np.stack(np.meshgrid(first, second, indexing="ij"), axis=-1)
        return np.asarray(mesh, dtype=np.float64)

    @staticmethod
    def _case(retained_rank: int = 3) -> Periodic2DRankNAnalyticCase:
        return Periodic2DRankNAnalyticCase(
            case_identifier="square-axis-control",
            retained_rank=retained_rank,
            circuit_depth=2,
            positive_bonds=((1, 0), (0, 1)),
            gauge_normalization=(Periodic2DRankNGaugeNormalizationEnum.AXIS_MAXIMUM),
            parent_scale=1.0,
            attack_coefficient=math.pi / 4.0,
        )

    def test_parent_has_selected_shape_ordering_and_gap_bound(self) -> None:
        case = self._case(retained_rank=4)
        coordinates = self._coordinates()

        retained = case.retained_energies(coordinates)
        exterior = case.exterior_energies(coordinates)
        parent = case.parent_hamiltonians(coordinates)
        frame = case.reference_frames(coordinates)

        assert case.ambient_dimension == 8
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
        attacked_frame = case.attacked_frames(coordinates)
        attacked_operator = case.attacked_reduced_hamiltonians(coordinates)
        identity = np.eye(case.retained_rank, dtype=np.complex128)

        assert np.swapaxes(gauge.conjugate(), -1, -2) @ gauge == pytest.approx(
            np.broadcast_to(identity, gauge.shape), abs=2.0e-15
        )
        assert np.linalg.det(gauge) == pytest.approx(
            np.ones(coordinates.shape[:-1]), abs=2.0e-15
        )
        assert attacked_frame @ inverse == pytest.approx(
            case.reference_frames(coordinates), abs=2.0e-15
        )
        assert (
            np.swapaxes(inverse.conjugate(), -1, -2) @ attacked_operator @ inverse
        ) == pytest.approx(case.exact_reduced_hamiltonians(coordinates), abs=2.0e-15)
        assert not gauge.flags.writeable

    def test_rejects_unselected_rank_dimension_and_attack_bound(self) -> None:
        with pytest.raises(ValueError, match="retained_rank"):
            self._case(retained_rank=5)
        with pytest.raises(ValueError, match=r"shape \(\.\.\., 2\)"):
            self._case().parent_hamiltonians(np.zeros((2, 2, 3), dtype=np.float64))
        with pytest.raises(ValueError, match="pi/4"):
            Periodic2DRankNAnalyticCase(
                case_identifier="triangular-control",
                retained_rank=3,
                circuit_depth=1,
                positive_bonds=((1, 0), (0, 1), (1, -1)),
                gauge_normalization=(Periodic2DRankNGaugeNormalizationEnum.BOND_RMS),
                parent_scale=0.0,
                attack_coefficient=math.pi / 4.0,
            )
