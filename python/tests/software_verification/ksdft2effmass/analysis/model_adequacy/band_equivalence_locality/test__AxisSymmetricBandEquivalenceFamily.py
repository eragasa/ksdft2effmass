"""Software verification for the dimension-general scientific family."""

import itertools
import math

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension
from scipy.special import j0, jv  # type: ignore[import-untyped]

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.family import (
    AxisSymmetricFourStateParent,
    SeparableSineRotation,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestAxisSymmetricBandEquivalenceFamily:
    """Own dimensional specialization, covariance, and analytic-correlation evidence."""

    def test_parent__diagonal_specialization__reproduces_one_dimensional_field(
        self,
    ) -> None:
        """Equal coordinates cancel the axis average in every supported dimension."""
        coordinate = 0.173
        one = np.asarray(
            AxisSymmetricFourStateParent(LatticeDimension.ONE, 0.75).evaluate(
                (coordinate,)
            )
        )
        two = np.asarray(
            AxisSymmetricFourStateParent(LatticeDimension.TWO, 0.75).evaluate(
                (coordinate, coordinate)
            )
        )
        three = np.asarray(
            AxisSymmetricFourStateParent(LatticeDimension.THREE, 0.75).evaluate(
                (coordinate, coordinate, coordinate)
            )
        )

        np.testing.assert_allclose(two, one, rtol=0.0, atol=2.0e-16)
        np.testing.assert_allclose(three, one, rtol=0.0, atol=2.0e-16)

    def test_parent__axis_permutation_and_inversion__preserve_declared_covariance(
        self,
    ) -> None:
        """Axis order is irrelevant and global inversion gives complex conjugation."""
        parent = AxisSymmetricFourStateParent(LatticeDimension.THREE, 1.0)
        coordinate = (0.125, -0.2, 0.31)
        matrix = np.asarray(parent.evaluate(coordinate))
        permuted = np.asarray(
            parent.evaluate((coordinate[2], coordinate[0], coordinate[1]))
        )
        inverted = np.asarray(parent.evaluate(tuple(-value for value in coordinate)))

        np.testing.assert_allclose(permuted, matrix, rtol=0.0, atol=2.0e-16)
        np.testing.assert_allclose(inverted, matrix.conjugate(), rtol=0.0, atol=2.0e-16)
        np.testing.assert_allclose(matrix, matrix.conjugate().T, rtol=0.0, atol=0.0)

    def test_rotation__specialization_and_flat_correlation__follow_master_family(
        self,
    ) -> None:
        """Angles reproduce 1-D on the diagonal and Bessel laws factor by dimension."""
        amplitude = math.pi / 4.0
        coordinate = 0.137
        one = SeparableSineRotation(LatticeDimension.ONE, amplitude)
        two = SeparableSineRotation(LatticeDimension.TWO, amplitude)
        three = SeparableSineRotation(LatticeDimension.THREE, amplitude)

        assert two.angle((coordinate, coordinate)) == pytest.approx(
            one.angle((coordinate,)), abs=2.0e-16
        )
        assert three.angle((coordinate, coordinate, coordinate)) == pytest.approx(
            one.angle((coordinate,)), abs=2.0e-16
        )
        assert one.flat_parent_correlation == pytest.approx(float(j0(2.0 * amplitude)))
        assert two.flat_parent_correlation == pytest.approx(float(j0(amplitude)) ** 2)
        assert three.flat_parent_correlation == pytest.approx(
            float(j0(2.0 * amplitude / 3.0)) ** 3
        )

    def test_flat_parent__shell_coefficients_and_factorial_tail__match_direct_field(
        self,
    ) -> None:
        """Jacobi--Anger blocks and the complete-shell tail bound hold in 2-D/3-D."""
        amplitude = math.pi / 4.0
        sigma_x = np.array(((0.0, 1.0), (1.0, 0.0)), dtype=np.complex128)
        sigma_z = np.array(((1.0, 0.0), (0.0, -1.0)), dtype=np.complex128)
        for dimension, size in ((2, 24), (3, 16)):
            axis = -0.5 + (np.arange(size) + 0.5) / float(size)
            coordinates = np.stack(
                np.meshgrid(*(axis,) * dimension, indexing="ij"), axis=-1
            )
            angles = (
                amplitude
                * np.sum(np.sin(2.0 * np.pi * coordinates), axis=-1)
                / float(dimension)
            )
            field = (
                np.cos(2.0 * angles)[..., None, None] * sigma_z
                - np.sin(2.0 * angles)[..., None, None] * sigma_x
            )
            argument = 2.0 * amplitude / float(dimension)
            maximum_defect = 0.0
            for displacement in itertools.product(range(-2, 3), repeat=dimension):
                phase = np.exp(
                    -2.0j
                    * np.pi
                    * np.einsum(
                        "...d,d->...",
                        coordinates,
                        np.asarray(displacement, dtype=np.int64),
                    )
                )
                coefficient = np.mean(
                    phase[..., None, None] * field,
                    axis=tuple(range(dimension)),
                )
                factor = math.prod(float(jv(value, argument)) for value in displacement)
                expected = factor * (
                    sigma_z if sum(displacement) % 2 == 0 else 1.0j * sigma_x
                )
                maximum_defect = max(
                    maximum_defect,
                    float(np.linalg.norm(coefficient - expected)),
                )
            assert maximum_defect < 2.0e-12

            for shell_cap in (0, 1, 4):
                radius = math.isqrt(shell_cap)
                retained_weight = math.fsum(
                    math.prod(float(jv(value, argument)) ** 2 for value in displacement)
                    for displacement in itertools.product(
                        range(-radius, radius + 1), repeat=dimension
                    )
                    if sum(value * value for value in displacement) <= shell_cap
                )
                exact_tail = 1.0 - retained_weight
                lower_index = math.floor(math.sqrt(shell_cap / dimension)) + 1
                half_argument = abs(argument) / 2.0
                bound = (
                    2.0
                    * dimension
                    * math.exp(argument * argument / 2.0)
                    * half_argument ** (2 * lower_index)
                    / (
                        math.factorial(lower_index) ** 2
                        * (1.0 - half_argument**2 / float((lower_index + 1) ** 2))
                    )
                )
                assert exact_tail <= bound + 2.0e-15

    def test_inputs__invalid_numeric_or_coordinate_contracts__fail_closed(self) -> None:
        """Invalid numeric values and coordinates outside the cell fail closed."""
        with pytest.raises(TypeError, match="built-in float"):
            AxisSymmetricFourStateParent(LatticeDimension.TWO, True)
        with pytest.raises(ValueError, match=r"\[0, 1\]"):
            AxisSymmetricFourStateParent(LatticeDimension.TWO, 1.1)
        with pytest.raises(ValueError, match=r"\[0, pi/4\]"):
            SeparableSineRotation(LatticeDimension.THREE, math.pi / 3.0)

        parent = AxisSymmetricFourStateParent(LatticeDimension.TWO, 0.5)
        with pytest.raises(ValueError, match="length"):
            parent.evaluate((0.0,))
        with pytest.raises(TypeError, match="built-in float"):
            parent.evaluate((0.0, 0))
        with pytest.raises(ValueError, match=r"\[-1/2, 1/2\)"):
            parent.evaluate((0.0, 0.5))
