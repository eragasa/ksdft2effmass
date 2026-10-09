"""Numerical verification for the reusable periodic2d finite-difference Action.

The synthetic case represents a unitless spinless scalar operator on the five-by-five
Euclidean site basis of a half-open period-``2*pi`` square cell in
``x_outer_y_inner`` order. Analytic centered-stencil entries are the oracle. Structural
zeros, request identity, Hermiticity, and storage immutability use exact comparison;
entries affected by binary64 arithmetic use complex absolute tolerance ``2e-15``.
The validity domain is this declared finite representation. The evidence does not
establish convergence to a continuum operator, physical adequacy, scientific
validation, uncertainty quantification, or acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import (
    FiniteDifferenceBlochHamiltonian2DConstructor,
    FiniteDifferenceBlochHamiltonian2DModel,
    FiniteDifferenceBlochHamiltonian2DRequest,
    FiniteDifferenceBlochHamiltonian2DResult,
    UniformPeriodicCoordinateBasis2D,
)
from ksdft2effmass.operators import MatrixQuantity, ScalarQuantity, Unitless

pytestmark = [pytest.mark.unit, pytest.mark.numerical_verification]


class TestFiniteDifferenceBlochHamiltonian2DConstructor:
    """Own analytic stencil, flattening, phase, and immutability evidence."""

    def test_execute_matches_declared_stencil_and_directed_bloch_seams(self) -> None:
        """Selected entries match an analytic centered-stencil oracle to roundoff."""
        points = 5
        period = 2.0 * np.pi
        scale = 1.7
        momentum = (0.13, -0.21)
        # Manufactured real samples vary by site so diagonal flattening is observable
        # independently of the analytic translation-invariant kinetic stencil.
        potential = np.arange(points**2, dtype=np.float64).reshape(points, points) / 10
        unit = Unitless()
        model = FiniteDifferenceBlochHamiltonian2DModel(
            basis=UniformPeriodicCoordinateBasis2D(period, points, "test.basis"),
            potential_samples=MatrixQuantity(potential, unit),
            kinetic_scale=ScalarQuantity(scale, unit),
            source_identifier="test.source",
            operator_identifier="test.operator",
            state_space_identifier="test.state-space",
            energy_reference="test.zero",
            provenance_identifier="test.provenance",
        )
        request = FiniteDifferenceBlochHamiltonian2DRequest(model, momentum)

        result = FiniteDifferenceBlochHamiltonian2DConstructor().execute(request)

        spacing = period / points
        off_diagonal = -scale / spacing**2
        matrix = result.represented_matrix.magnitude
        assert type(result) is FiniteDifferenceBlochHamiltonian2DResult
        assert result.request is request
        assert matrix.shape == (25, 25)
        assert matrix[0, 0] == pytest.approx(
            4.0 * scale / spacing**2 + potential[0, 0], abs=2.0e-15
        )
        assert matrix[0, 5] == pytest.approx(off_diagonal, abs=2.0e-15)
        assert matrix[0, 1] == pytest.approx(off_diagonal, abs=2.0e-15)
        assert matrix[0, 20] == pytest.approx(
            off_diagonal * np.exp(-1j * momentum[0] * period), abs=2.0e-15
        )
        assert matrix[0, 4] == pytest.approx(
            off_diagonal * np.exp(-1j * momentum[1] * period), abs=2.0e-15
        )
        assert matrix[20, 0] == matrix[0, 20].conjugate()
        assert matrix[4, 0] == matrix[0, 4].conjugate()
        assert matrix[0, 7] == 0.0 + 0.0j
        assert np.array_equal(matrix, matrix.conj().T)
        assert not matrix.flags.writeable
