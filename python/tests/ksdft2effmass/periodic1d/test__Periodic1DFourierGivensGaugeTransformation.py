"""Contracts for explicit periodic-1D Fourier-Givens transformations."""

import numpy as np
import pytest

from ksdft2effmass.gauge_transformation import (
    FiniteRankGivensCircuit,
    FiniteRankGivensLayer,
    FiniteRankGivensRotation,
)
from ksdft2effmass.periodic1d.gauge_transformation import (
    Periodic1DFourierGivensGaugeTransformation,
)


class TestPeriodic1DFourierGivensGaugeTransformation:
    """Establish explicit coefficient evaluation and sampled right actions."""

    @staticmethod
    def transformation() -> Periodic1DFourierGivensGaugeTransformation:
        return Periodic1DFourierGivensGaugeTransformation(
            transformation_identifier="test-periodic1d-fourier-givens",
            circuit=FiniteRankGivensCircuit(
                represented_rank=2,
                layers=(
                    FiniteRankGivensLayer(rotations=(FiniteRankGivensRotation(0, 1),)),
                ),
            ),
            continuum_angle_maximum_bound=0.4,
            constant_angles=np.asarray((0.1,), dtype=np.float64),
            cosine_coefficients=np.asarray(((0.2,),), dtype=np.float64),
            sine_coefficients=np.asarray(((-0.1,),), dtype=np.float64),
        )

    def test__angle_samples__evaluate_the_declared_fourier_series(self) -> None:
        transformation = self.transformation()
        coordinates = np.asarray((0.0, 0.25), dtype=np.float64)

        angles = transformation.angle_samples(coordinates)

        np.testing.assert_allclose(
            angles,
            np.asarray(((0.3,), (0.0,)), dtype=np.float64),
            rtol=0.0,
            atol=1.0e-15,
        )

    def test__unitaries__delegate_to_the_generic_givens_circuit(self) -> None:
        transformation = self.transformation()
        coordinates = np.asarray((0.0,), dtype=np.float64)
        theta = 0.3
        expected = np.asarray(
            (
                (np.cos(theta), -np.sin(theta)),
                (np.sin(theta), np.cos(theta)),
            ),
            dtype=np.complex128,
        )

        np.testing.assert_allclose(
            transformation.unitaries(coordinates)[0],
            expected,
            rtol=0.0,
            atol=1.0e-15,
        )

    def test__construction__rejects_a_nonexplicit_identifier(self) -> None:
        with pytest.raises(ValueError, match="nonempty"):
            Periodic1DFourierGivensGaugeTransformation(
                transformation_identifier="",
                circuit=self.transformation().circuit,
                continuum_angle_maximum_bound=0.4,
                constant_angles=np.asarray((0.0,), dtype=np.float64),
                cosine_coefficients=np.asarray(((0.0,),), dtype=np.float64),
                sine_coefficients=np.asarray(((0.0,),), dtype=np.float64),
            )
