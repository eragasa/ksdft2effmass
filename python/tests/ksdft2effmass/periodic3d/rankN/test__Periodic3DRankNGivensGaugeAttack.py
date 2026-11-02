"""Periodic-3D arbitrary-rank synthetic gauge-attack contracts."""

from __future__ import annotations

import math

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array

from ksdft2effmass.periodic3d.rankN.gauge_alignment.attack import (
    Periodic3DRankNGaugeNormalizationEnum,
    Periodic3DRankNGivensGaugeAttack,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic3DRankNGivensGaugeAttack:
    """Qualify parent-independent attack construction and application."""

    @staticmethod
    def _coordinates() -> Float64Array:
        axis = np.asarray((0.0, 0.25), dtype=np.float64)
        return np.asarray(
            np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1),
            dtype=np.float64,
        )

    @staticmethod
    def _attack() -> Periodic3DRankNGivensGaugeAttack:
        return Periodic3DRankNGivensGaugeAttack(
            retained_rank=10,
            circuit_depth=3,
            harmonic_bonds=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            normalization=Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM,
            coefficient=math.pi / 4.0,
        )

    @staticmethod
    def _frames(coordinates: Float64Array) -> Complex128Array:
        frame = np.zeros((12, 10), dtype=np.complex128)
        frame[:10, :] = np.eye(10, dtype=np.complex128)
        return np.asarray(
            np.broadcast_to(frame, (*coordinates.shape[:-1], 12, 10)).copy(),
            dtype=np.complex128,
        )

    @staticmethod
    def _operators(coordinates: Float64Array) -> Complex128Array:
        base = np.diag(np.linspace(-1.0, 1.0, 10)).astype(np.complex128)
        base[0, 1] = 0.125 + 0.05j
        base[1, 0] = base[0, 1].conjugate()
        coordinate_shift = np.sum(coordinates, axis=-1)
        identity = np.eye(10, dtype=np.complex128)
        return np.asarray(
            base + 0.1 * coordinate_shift[..., None, None] * identity,
            dtype=np.complex128,
        )

    def test_applies_to_arbitrary_admitted_frame_and_operator_fields(self) -> None:
        attack = self._attack()
        coordinates = self._coordinates()
        frames = self._frames(coordinates)
        operators = self._operators(coordinates)

        gauge = attack.unitaries(coordinates)
        inverse = attack.inverse_right_actions(coordinates)
        attacked_frames = attack.apply_to_frames(coordinates, frames)
        attacked_operators = attack.apply_to_operators(coordinates, operators)

        assert attack.retained_rank == 10
        assert "alternating-givens-attack.v1" in attack.attack_identity
        assert attacked_frames == pytest.approx(frames @ gauge, abs=0.0)
        assert attacked_operators == pytest.approx(
            np.swapaxes(gauge.conjugate(), -1, -2) @ operators @ gauge,
            abs=0.0,
        )
        assert attacked_frames @ inverse == pytest.approx(frames, abs=3.0e-15)
        assert (
            np.swapaxes(inverse.conjugate(), -1, -2) @ attacked_operators @ inverse
        ) == pytest.approx(operators, abs=3.0e-15)
        assert np.linalg.eigvalsh(attacked_operators) == pytest.approx(
            np.linalg.eigvalsh(operators), abs=3.0e-15
        )
        assert not gauge.flags.writeable
        assert not inverse.flags.writeable
        assert not attacked_frames.flags.writeable
        assert not attacked_operators.flags.writeable

    def test_rejects_incompatible_rank_coordinate_and_field_shapes(self) -> None:
        with pytest.raises(ValueError, match="at least two"):
            Periodic3DRankNGivensGaugeAttack(
                retained_rank=1,
                circuit_depth=1,
                harmonic_bonds=((1, 0, 0),),
                normalization=Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM,
                coefficient=0.0,
            )

        attack = self._attack()
        coordinates = self._coordinates()
        with pytest.raises(ValueError, match=r"shape \(\.\.\., 3\)"):
            attack.unitaries(np.zeros((2, 2, 2), dtype=np.float64))
        with pytest.raises(ValueError, match="frame column count"):
            attack.apply_to_frames(
                coordinates,
                np.zeros((*coordinates.shape[:-1], 12, 9), dtype=np.complex128),
            )
        with pytest.raises(ValueError, match="operator shape"):
            attack.apply_to_operators(
                coordinates,
                np.zeros((*coordinates.shape[:-1], 9, 9), dtype=np.complex128),
            )
