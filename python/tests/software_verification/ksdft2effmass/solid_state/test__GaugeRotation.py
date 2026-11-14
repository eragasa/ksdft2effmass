"""Tests for generic gauge-rotation definitions and transformations."""

from __future__ import annotations

import numpy as np
import pytest
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array

from ksdft2effmass.solidstate import GaugeRotation, GaugeTransformation


class TestGaugeRotation:
    """Establish definition, validation, alignment, and action behavior."""

    class _FixedGaugeRotation(GaugeRotation):
        __slots__ = ("_values",)
        _values: Complex128Array

        def __init__(self, values: Complex128Array) -> None:
            if values.ndim != 3 or values.shape[1] != values.shape[2]:
                raise ValueError("values must be a square matrix field")
            object.__setattr__(self, "_values", values)
            super().__init__(rank=int(values.shape[1]))

        def matrices(self, coordinates: Float64Array) -> Complex128Array:
            if coordinates.shape[0] != self._values.shape[0]:
                raise ValueError("coordinate inventory does not match values")
            return self._values

    class _TwoCoordinateRank3GaugeRotation(GaugeRotation):
        __slots__ = ()

        def __init__(self) -> None:
            super().__init__(rank=3)

        def matrices(self, coordinates: Float64Array) -> Complex128Array:
            phases = np.stack(
                (
                    coordinates[:, 0],
                    coordinates[:, 1],
                    -coordinates[:, 0] - coordinates[:, 1],
                ),
                axis=1,
            )
            values = np.zeros((coordinates.shape[0], 3, 3), dtype=np.complex128)
            diagonal = np.arange(3)
            values[:, diagonal, diagonal] = np.exp(1.0j * phases)
            return values

    @staticmethod
    def _rotation_values() -> Complex128Array:
        angle = np.asarray((0.0, 0.2), dtype=np.float64)
        values = np.empty((2, 2, 2), dtype=np.complex128)
        values[:, 0, 0] = np.cos(angle)
        values[:, 0, 1] = -np.sin(angle)
        values[:, 1, 0] = np.sin(angle)
        values[:, 1, 1] = np.cos(angle)
        return values

    def test_generic_rotation_is_abstract_and_requires_rank(self) -> None:
        assert GaugeRotation.__abstractmethods__ == frozenset({"matrices"})
        with pytest.raises(TypeError, match="abstract class"):
            GaugeRotation(rank=2)  # type: ignore[abstract]

    def test_transformation_applies_the_right_acting_similarity_transform(self) -> None:
        coordinates = np.asarray((0.0, 0.5), dtype=np.float64)
        rotation = self._FixedGaugeRotation(self._rotation_values())
        matrices = np.asarray(
            (
                ((1.0, 0.0), (0.0, -1.0)),
                ((2.0, 0.3j), (-0.3j, -0.5)),
            ),
            dtype=np.complex128,
        )
        gauge_transformed = GaugeTransformation(rotation, 1.0e-14).transform_operators(
            coordinates=coordinates,
            represented_matrices=matrices,
        )
        rotations = rotation.matrices(coordinates)
        expected = np.swapaxes(rotations.conjugate(), -1, -2) @ matrices @ rotations
        assert not gauge_transformed.flags.writeable
        assert np.array_equal(gauge_transformed, expected)

    def test_transformation_supports_multidimensional_coordinates_and_higher_rank(
        self,
    ) -> None:
        coordinates = np.asarray(((0.1, 0.2), (0.3, -0.4)), dtype=np.float64)
        matrices = np.asarray(
            (
                np.diag((1.0, 2.0, 3.0)),
                np.diag((-1.0, 0.5, 4.0)),
            ),
            dtype=np.complex128,
        )
        gauge_transformed = GaugeTransformation(
            self._TwoCoordinateRank3GaugeRotation(),
            1.0e-14,
        ).transform_operators(
            coordinates=coordinates,
            represented_matrices=matrices,
        )
        assert gauge_transformed.shape == (2, 3, 3)
        assert np.allclose(gauge_transformed, matrices, rtol=0.0, atol=1.0e-15)

    def test_transformation_rejects_nonunitary_rotation_values(self) -> None:
        coordinates = np.asarray((0.0, 0.5), dtype=np.float64)
        values = self._rotation_values()
        values[0, 0, 0] = 2.0
        transformation = GaugeTransformation(self._FixedGaugeRotation(values), 1.0e-14)
        matrices = np.zeros((2, 2, 2), dtype=np.complex128)
        with pytest.raises(ValueError, match="unitarity tolerance"):
            transformation.transform_operators(
                coordinates=coordinates,
                represented_matrices=matrices,
            )

    def test_transformation_rejects_boolean_tolerance(self) -> None:
        rotation = self._FixedGaugeRotation(self._rotation_values())
        with pytest.raises(TypeError, match="built-in float"):
            GaugeTransformation(rotation, True)

    def test_transformation_rejects_a_misaligned_sample_or_rank_inventory(self) -> None:
        coordinates = np.asarray((0.0, 0.5), dtype=np.float64)
        transformation = GaugeTransformation(
            self._FixedGaugeRotation(self._rotation_values()),
            1.0e-14,
        )
        with pytest.raises(ValueError, match="coordinate count and rotation rank"):
            transformation.transform_operators(
                coordinates=coordinates,
                represented_matrices=np.zeros((2, 3, 3), dtype=np.complex128),
            )
