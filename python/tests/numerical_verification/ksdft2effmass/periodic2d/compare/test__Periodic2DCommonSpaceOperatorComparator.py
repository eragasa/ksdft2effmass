"""Numerical verification for ``Periodic2DCommonSpaceOperatorComparator``.

Discrete Fourier orthogonality, independently written centered-difference dispersion,
and bounded resolved-cosine Fourier transfer are three versioned analytic oracles for
synthetic operators on odd period-``2*pi`` grids. Complex128 matrices and scalar
isometry/Frobenius diagnostics use stated absolute tolerances at the observed small test
scale; the checks apply no production acceptance threshold.

This consumer module deliberately encodes no mutable oracle status. Its results count as
accepted numerical-verification evidence only while the disposition ledger contains
applicable terminal ``QUALIFIED`` decisions for the current record digests and reviewed
evidence revision and the corresponding proposal acceptance gate has passed. Candidate,
suspended, retired, or out-of-domain uses remain provisional. The checks do not
establish continuum convergence, parent-model adequacy, scientific validation,
uncertainty quantification, or human acceptance.
"""

import numpy as np
import numpy.typing as npt
import pytest

from ksdft2effmass.periodic2d.compare.common_space import (
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
    """Own provisional consumers of three common-space candidate oracles."""

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
        """Execute the production consumer route for one fixed synthetic case.

        Parameters
        ----------
        model
            Exact dimensionless cosine-family parent used by both representations.
        momentum_x, momentum_y
            Reduced Bloch momentum components.
        points
            Uniform grid points per direction.
        cutoff
            Symmetric plane-wave reciprocal cutoff.

        Returns
        -------
        tuple[numpy.ndarray, numpy.ndarray, float, float]
            Transported finite-difference matrix, signed finite-minus-plane-wave
            difference, unitless column-isometry Frobenius defect, and dimensionless
            operator-difference Frobenius norm. No returned value is an acceptance
            classification.
        """
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
        """Evaluate the analytic centered-difference dispersion by ordered mode.

        Parameters
        ----------
        momentum_x, momentum_y
            Reduced Bloch momentum components in the period-``2*pi`` convention.
        points
            Uniform grid points per direction.
        cutoff
            Symmetric retained reciprocal cutoff.

        Returns
        -------
        numpy.ndarray
            Binary64 diagonal values in ``p``-outer, ``q``-inner order and the
            dimensionless model-energy convention.
        """
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

    def test_execute__equal_basis_and_grid_sides__map_is_unitary(self) -> None:
        """At N=2M+1, both map products equal identity within roundoff."""
        model = Periodic2DCosinePotentialToyModel(0.0, 0.0, 0.0)
        plane = Periodic2DPlaneWaveHamiltonianConstructor().execute(
            Periodic2DPlaneWaveHamiltonianRequest(model, 0.13, -0.21, 2)
        )
        finite = Periodic2DFiniteDifferenceHamiltonianConstructor().execute(
            Periodic2DFiniteDifferenceHamiltonianRequest(model, 0.13, -0.21, 5)
        )

        result = Periodic2DCommonSpaceOperatorComparator().execute(
            Periodic2DCommonSpaceComparisonRequest(
                plane, finite, "square-unitary-common-space"
            )
        )

        sampling = result.plane_wave_to_grid.magnitude
        identity = np.eye(25, dtype=np.complex128)
        # The DFT orthogonality oracle applies on both sides only at the allowed square
        # boundary. This distinguishes full-space unitary similarity from the proper
        # rectangular compression exercised by cutoff-one tests below.
        np.testing.assert_allclose(
            sampling.conj().T @ sampling,
            identity,
            rtol=0.0,
            atol=6.0e-15,
        )
        np.testing.assert_allclose(
            sampling @ sampling.conj().T,
            identity,
            rtol=0.0,
            atol=6.0e-15,
        )

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
        # The fixed rectangular DFT candidate owns the column-isometry threshold;
        # the dispersion candidate owns the scalar norm of the expected difference.
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
        # This isometry assertion is a second consumer of the fixed-domain DFT
        # candidate; it is distinct from cosine-transfer cancellation.
        assert isometry < 5.0e-15
