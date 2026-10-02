"""Numerical verification for ``Periodic2DCommonSpaceOperatorComparator``."""

import numpy as np
import numpy.typing as npt
import pytest

from ksdft2effmass.periodic2d import (
    Periodic2DCommonSpaceComparisonRequest,
    Periodic2DCommonSpaceOperatorComparator,
)
from ksdft2effmass.periodic2d.model.toy_models import (
    Periodic2DCosinePotentialToyModel,
    Periodic2DFiniteDifferenceHamiltonianConstructor,
    Periodic2DFiniteDifferenceHamiltonianRequest,
    Periodic2DPlaneWaveHamiltonianConstructor,
    Periodic2DPlaneWaveHamiltonianRequest,
)

pytestmark = [pytest.mark.unit, pytest.mark.numerical_verification]


class TestPeriodic2DCommonSpaceOperatorComparator:
    """Own analytical discrete-dispersion and Fourier-coupling evidence."""

    @staticmethod
    def execute(
        model: Periodic2DCosinePotentialToyModel,
        momentum_x: float,
        momentum_y: float,
        points: int,
        cutoff: int,
    ) -> tuple[
        npt.NDArray[np.complex128],
        npt.NDArray[np.complex128],
        float,
        float,
    ]:
        """Return transported, difference, isometry, and Frobenius outputs."""
        plane = Periodic2DPlaneWaveHamiltonianConstructor().execute(
            Periodic2DPlaneWaveHamiltonianRequest(model, momentum_x, momentum_y, cutoff)
        )
        finite = Periodic2DFiniteDifferenceHamiltonianConstructor().execute(
            Periodic2DFiniteDifferenceHamiltonianRequest(
                model, momentum_x, momentum_y, points
            )
        )
        result = Periodic2DCommonSpaceOperatorComparator().execute(
            Periodic2DCommonSpaceComparisonRequest(
                plane, finite, "analytical-common-space"
            )
        )
        return (
            result.transported_finite_difference.magnitude,
            result.operator_difference.magnitude,
            result.isometry_frobenius_defect.magnitude,
            result.operator_frobenius_error.magnitude,
        )

    @staticmethod
    def discrete_kinetic_diagonal(
        momentum_x: float,
        momentum_y: float,
        points: int,
        cutoff: int,
    ) -> npt.NDArray[np.float64]:
        """Evaluate the centered-difference dispersion independently by mode."""
        spacing = 2.0 * np.pi / points
        values = []
        for p in range(-cutoff, cutoff + 1):
            for q in range(-cutoff, cutoff + 1):
                values.append(
                    4.0
                    / spacing**2
                    * (
                        np.sin(0.5 * (momentum_x + p) * spacing) ** 2
                        + np.sin(0.5 * (momentum_y + q) * spacing) ** 2
                    )
                )
        return np.asarray(values, dtype=np.float64)

    def test_execute__free_operator__matches_discrete_fourier_dispersion(self) -> None:
        """Transport diagonalizes the free grid operator at the analytical energies."""
        momentum_x = 0.13
        momentum_y = -0.21
        points = 5
        cutoff = 1

        transported, difference, isometry, frobenius = self.execute(
            Periodic2DCosinePotentialToyModel(0.0, 0.0, 0.0),
            momentum_x,
            momentum_y,
            points,
            cutoff,
        )

        discrete = self.discrete_kinetic_diagonal(
            momentum_x, momentum_y, points, cutoff
        )
        continuum = np.asarray(
            [
                (momentum_x + p) ** 2 + (momentum_y + q) ** 2
                for p in range(-cutoff, cutoff + 1)
                for q in range(-cutoff, cutoff + 1)
            ],
            dtype=np.float64,
        )
        expected_difference = discrete - continuum
        np.testing.assert_allclose(
            transported,
            np.diag(discrete),
            rtol=0.0,
            atol=4.0e-15,
        )
        np.testing.assert_allclose(
            difference,
            np.diag(expected_difference),
            rtol=0.0,
            atol=4.0e-15,
        )
        assert isometry < 4.0e-15
        assert abs(frobenius - np.linalg.norm(expected_difference)) < 4.0e-15

    def test_execute__cosine_operator__isolates_discrete_kinetic_error(self) -> None:
        """Resolved cosine Fourier blocks agree, leaving only diagonal kinetic error."""
        momentum_x = -0.17
        momentum_y = 0.09
        points = 7
        cutoff = 1

        _, difference, isometry, _ = self.execute(
            Periodic2DCosinePotentialToyModel(0.4, 0.7, 0.2),
            momentum_x,
            momentum_y,
            points,
            cutoff,
        )

        discrete = self.discrete_kinetic_diagonal(
            momentum_x, momentum_y, points, cutoff
        )
        continuum = np.asarray(
            [
                (momentum_x + p) ** 2 + (momentum_y + q) ** 2
                for p in range(-cutoff, cutoff + 1)
                for q in range(-cutoff, cutoff + 1)
            ],
            dtype=np.float64,
        )
        np.testing.assert_allclose(
            difference,
            np.diag(discrete - continuum),
            rtol=0.0,
            atol=6.0e-15,
        )
        assert isometry < 5.0e-15
