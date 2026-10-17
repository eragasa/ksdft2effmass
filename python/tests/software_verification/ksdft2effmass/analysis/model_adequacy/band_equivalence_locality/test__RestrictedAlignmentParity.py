"""Verify the restricted rank-two alignment in mathematical terms."""

from __future__ import annotations

import math

import numpy as np
import pytest
from numpy.typing import NDArray

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.alignment import (
    restricted_alignment,
)

type ComplexArray = NDArray[np.complex128]


def _rotation(angle: float) -> ComplexArray:
    cosine = math.cos(angle)
    sine = math.sin(angle)
    return np.asarray(((cosine, -sine), (sine, cosine)), dtype=np.complex128)


def _traceless_fields() -> tuple[ComplexArray, ComplexArray]:
    coordinates = np.arange(19, dtype=np.float64) / 19.0
    means = 0.17 * np.cos(2.0 * np.pi * coordinates)
    diagonal = 0.8 + 0.21 * np.cos(4.0 * np.pi * coordinates)
    offdiagonal = 0.31 * np.sin(2.0 * np.pi * coordinates)
    reference = np.zeros((coordinates.size, 2, 2), dtype=np.complex128)
    reference[:, 0, 0] = means + diagonal
    reference[:, 1, 1] = means - diagonal
    reference[:, 0, 1] = offdiagonal
    reference[:, 1, 0] = offdiagonal

    comparison = np.empty_like(reference)
    for index, coordinate in enumerate(coordinates):
        rotation = _rotation(0.43 * math.sin(2.0 * math.pi * coordinate))
        comparison[index] = rotation.T @ reference[index] @ rotation
    return reference, comparison


def _traceless(matrices: ComplexArray) -> ComplexArray:
    identity = np.eye(2, dtype=np.complex128)
    means = np.trace(matrices, axis1=-2, axis2=-1).real / 2.0
    return matrices - means[:, None, None] * identity


def _correlation_numerator(
    reference: ComplexArray, comparison: ComplexArray, angle: float
) -> float:
    rotation = _rotation(angle)
    aligned = rotation.T @ reference @ rotation
    products = np.einsum("nij,nij->n", aligned.conjugate(), comparison, optimize=True)
    return float(np.mean(products.real) / 2.0)


class TestRestrictedAlignmentParity:
    """Establish the positive-scale and unit-scale Paper 1 distinctions."""

    def test_positive_scale_minimum_and_unit_scale_threshold_are_distinct(self) -> None:
        reference, comparison = _traceless_fields()
        (
            angle,
            degenerate,
            splitting_scale,
            correlation,
            minimum_threshold,
            exact_spectrum_threshold,
        ) = restricted_alignment(reference, comparison)

        assert angle is not None
        assert correlation is not None
        assert not degenerate
        reference_traceless = _traceless(reference)
        comparison_traceless = _traceless(comparison)
        expected_splitting = float(
            np.mean(np.sum(np.abs(reference_traceless) ** 2, axis=(-2, -1))) / 2.0
        )
        expected_correlation = (
            _correlation_numerator(reference_traceless, comparison_traceless, angle)
            / expected_splitting
        )
        positive_scale = max(0.0, expected_correlation)
        rotation = _rotation(angle)
        globally_aligned = rotation.T @ reference_traceless @ rotation
        optimized_residual_squared = float(
            np.mean(
                np.sum(
                    np.abs(positive_scale * globally_aligned - comparison_traceless)
                    ** 2,
                    axis=(-2, -1),
                )
            )
            / 2.0
        )
        unit_scale_residual_squared = float(
            np.mean(
                np.sum(
                    np.abs(globally_aligned - comparison_traceless) ** 2,
                    axis=(-2, -1),
                )
            )
            / 2.0
        )

        assert splitting_scale == pytest.approx(expected_splitting, abs=2.0e-15)
        assert correlation == pytest.approx(expected_correlation, abs=2.0e-15)
        assert minimum_threshold**2 == pytest.approx(
            optimized_residual_squared, abs=3.0e-15
        )
        assert exact_spectrum_threshold**2 == pytest.approx(
            unit_scale_residual_squared, abs=3.0e-15
        )
        assert minimum_threshold < exact_spectrum_threshold

    def test_selected_angle_maximizes_the_continuous_second_harmonic(self) -> None:
        reference, comparison = _traceless_fields()
        angle, _, splitting_scale, correlation, _, _ = restricted_alignment(
            reference, comparison
        )

        assert angle is not None
        assert correlation is not None
        reference_traceless = _traceless(reference)
        comparison_traceless = _traceless(comparison)
        constant = 0.5 * (
            _correlation_numerator(
                reference_traceless, comparison_traceless, math.pi / 4.0
            )
            + _correlation_numerator(
                reference_traceless, comparison_traceless, -math.pi / 4.0
            )
        )
        cosine_coefficient = (
            _correlation_numerator(reference_traceless, comparison_traceless, 0.0)
            - constant
        )
        sine_coefficient = 0.5 * (
            _correlation_numerator(
                reference_traceless, comparison_traceless, math.pi / 4.0
            )
            - _correlation_numerator(
                reference_traceless, comparison_traceless, -math.pi / 4.0
            )
        )
        expected_maximum = constant + math.hypot(cosine_coefficient, sine_coefficient)

        assert correlation == pytest.approx(
            expected_maximum / splitting_scale, abs=2.0e-15
        )
        assert _correlation_numerator(
            reference_traceless, comparison_traceless, angle
        ) == pytest.approx(expected_maximum, abs=2.0e-15)
