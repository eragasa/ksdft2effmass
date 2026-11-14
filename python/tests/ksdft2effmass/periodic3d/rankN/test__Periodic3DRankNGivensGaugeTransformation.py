"""Periodic-3D arbitrary-rank synthetic gauge-transformation contracts."""

from __future__ import annotations

import math

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array

from ksdft2effmass.periodic3d.rankN.gauge_alignment.transformation import (
    Periodic3DRankNGaugeNormalizationEnum,
    Periodic3DRankNGivensGaugeTransformation,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic3DRankNGivensGaugeTransformation:
    """Qualify parent-independent transformation construction and application."""

    @staticmethod
    def _coordinates() -> Float64Array:
        axis = np.asarray((0.0, 0.25), dtype=np.float64)
        return np.asarray(
            np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1),
            dtype=np.float64,
        )

    @staticmethod
    def _transformation() -> Periodic3DRankNGivensGaugeTransformation:
        return Periodic3DRankNGivensGaugeTransformation(
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
        transformation = self._transformation()
        coordinates = self._coordinates()
        frames = self._frames(coordinates)
        operators = self._operators(coordinates)

        gauge = transformation.unitaries(coordinates)
        inverse = transformation.inverse_right_actions(coordinates)
        gauge_transformed_frames = transformation.transform_frames(coordinates, frames)
        gauge_transformed_operators = transformation.transform_operators(
            coordinates, operators
        )

        assert transformation.retained_rank == 10
        assert (
            "alternating-givens-transformation.v1"
            in transformation.transformation_identity
        )
        assert gauge_transformed_frames == pytest.approx(frames @ gauge, abs=0.0)
        assert gauge_transformed_operators == pytest.approx(
            np.swapaxes(gauge.conjugate(), -1, -2) @ operators @ gauge,
            abs=0.0,
        )
        assert gauge_transformed_frames @ inverse == pytest.approx(frames, abs=3.0e-15)
        assert (
            np.swapaxes(inverse.conjugate(), -1, -2)
            @ gauge_transformed_operators
            @ inverse
        ) == pytest.approx(operators, abs=3.0e-15)
        assert np.linalg.eigvalsh(gauge_transformed_operators) == pytest.approx(
            np.linalg.eigvalsh(operators), abs=3.0e-15
        )
        assert not gauge.flags.writeable
        assert not inverse.flags.writeable
        assert not gauge_transformed_frames.flags.writeable
        assert not gauge_transformed_operators.flags.writeable

    def test_supports_rank_two_with_even_circuit_depth(self) -> None:
        transformation = Periodic3DRankNGivensGaugeTransformation(
            retained_rank=2,
            circuit_depth=2,
            harmonic_bonds=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            normalization=Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM,
            coefficient=0.2,
        )

        gauge = transformation.unitaries(self._coordinates())

        assert gauge.shape == (2, 2, 2, 2, 2)
        assert np.swapaxes(gauge.conjugate(), -1, -2) @ gauge == pytest.approx(
            np.broadcast_to(np.eye(2, dtype=np.complex128), gauge.shape),
            abs=2.0e-15,
        )

    def test_rejects_incompatible_rank_coordinate_and_field_shapes(self) -> None:
        with pytest.raises(ValueError, match="at least two"):
            Periodic3DRankNGivensGaugeTransformation(
                retained_rank=1,
                circuit_depth=1,
                harmonic_bonds=((1, 0, 0),),
                normalization=Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM,
                coefficient=0.0,
            )

        transformation = self._transformation()
        coordinates = self._coordinates()
        with pytest.raises(ValueError, match=r"shape \(\.\.\., 3\)"):
            transformation.unitaries(np.zeros((2, 2, 2), dtype=np.float64))
        with pytest.raises(ValueError, match="frame column count"):
            transformation.transform_frames(
                coordinates,
                np.zeros((*coordinates.shape[:-1], 12, 9), dtype=np.complex128),
            )
        with pytest.raises(ValueError, match="operator shape"):
            transformation.transform_operators(
                coordinates,
                np.zeros((*coordinates.shape[:-1], 9, 9), dtype=np.complex128),
            )
