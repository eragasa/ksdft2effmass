"""Tests for the specified periodic rank-two sinusoidal gauge rotation."""

from __future__ import annotations

import math

import numpy as np
import pytest

from ksdft2effmass.periodic1d.band_equivalence_locality.gauge import (
    Periodic1DRank2SinusoidalGaugeRotation,
)
from ksdft2effmass.solidstate import GaugeAttack

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRank2SinusoidalGaugeRotation:
    """Establish validation, construction, and gauge-action behavior."""

    def test_amplitude_requires_one_finite_builtin_float(self) -> None:
        with pytest.raises(TypeError, match="required positional argument"):
            Periodic1DRank2SinusoidalGaugeRotation()  # type: ignore[call-arg]
        with pytest.raises(TypeError, match="built-in float"):
            Periodic1DRank2SinusoidalGaugeRotation(True)
        with pytest.raises(ValueError, match="finite"):
            Periodic1DRank2SinusoidalGaugeRotation(math.inf)

    def test_definition_returns_special_orthogonal_rotations(self) -> None:
        coordinates = np.asarray((-0.5, -0.25, 0.0, 0.25), dtype=np.float64)
        rotation = Periodic1DRank2SinusoidalGaugeRotation(0.2)
        rotations = rotation.matrices(coordinates)
        identity = np.eye(2, dtype=np.complex128)
        assert rotation.rank == 2
        assert (
            np.max(
                np.abs(
                    np.swapaxes(rotations.conjugate(), -1, -2) @ rotations - identity
                )
            )
            < 1.0e-15
        )
        assert np.allclose(np.linalg.det(rotations), 1.0, rtol=0.0, atol=1.0e-15)

    def test_zero_amplitude_is_the_identity_attack(self) -> None:
        coordinates = np.asarray((-0.5, 0.0, 0.25), dtype=np.float64)
        matrices = np.asarray(
            [
                [[1.0, 0.2j], [-0.2j, -1.0]],
                [[0.5, 0.1], [0.1, -0.5]],
                [[2.0, -0.3j], [0.3j, -2.0]],
            ],
            dtype=np.complex128,
        )
        rotation = Periodic1DRank2SinusoidalGaugeRotation(0.0)
        transformed = GaugeAttack(rotation, 1.0e-14).apply(
            coordinates=coordinates,
            represented_matrices=matrices,
        )
        assert not transformed.flags.writeable
        assert np.array_equal(transformed, matrices)

    def test_attack_preserves_pointwise_sorted_spectra(self) -> None:
        coordinates = np.asarray((-0.4, -0.1, 0.2), dtype=np.float64)
        matrices = np.asarray(
            [
                [[1.0, 0.2j], [-0.2j, -1.0]],
                [[0.8, 0.1], [0.1, -0.4]],
                [[1.2, -0.3j], [0.3j, -0.7]],
            ],
            dtype=np.complex128,
        )
        rotation = Periodic1DRank2SinusoidalGaugeRotation(0.3)
        transformed = GaugeAttack(rotation, 1.0e-14).apply(
            coordinates=coordinates,
            represented_matrices=matrices,
        )
        assert np.allclose(
            np.linalg.eigvalsh(transformed),
            np.linalg.eigvalsh(matrices),
            rtol=0.0,
            atol=1.0e-14,
        )

    def test_definition_rejects_an_ambiguous_coordinate_representation(self) -> None:
        rotation = Periodic1DRank2SinusoidalGaugeRotation(0.2)
        coordinates = np.asarray((0, 1), dtype=np.int64)
        with pytest.raises(TypeError, match="dtype float64"):
            rotation.matrices(coordinates)  # type: ignore[arg-type]
