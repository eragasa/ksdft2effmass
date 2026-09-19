r"""Numerical verification of ``HarmonicOscillatorComparator``.

Evidence profile: claim_bearing

Bounded artifact scope: analytical one-state pullback for HarmonicOscillatorComparator.

Facet and represented meaning

The class under test maps one dimensionless three-point Dirichlet grid and one
retained analytic ground state into common coordinates and compares the represented
Hamiltonians.

Intrinsic and cross-object scope

The independently hand-constructed three-by-three finite-difference matrix, normalized
analytic ground-state samples, scalar pullback, exact retained energy, and discrepancy
norms are the oracle. Campaign sweeps, JSON serialization, and retained artifacts are
excluded.

VVUQ and scientific exclusions

This is numerical verification for one finite binary64 representation. It establishes
neither continuum convergence nor model adequacy, semiconductor relevance, scientific
validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import (
    DirichletBoundaryCondition,
    DirichletInterval,
    UniformCartesianGrid1D,
)
from ksdft2effmass.analysis.model_systems.harmonic_oscillator import (
    HarmonicOscillatorAnalytical,
    HarmonicOscillatorComparator,
    HarmonicOscillatorComparisonRequest,
    HarmonicOscillatorFiniteDifference,
    HarmonicOscillatorLadderOperators,
    HarmonicOscillatorNondimensionalizer,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.operators import LadderOperator1D

pytestmark = pytest.mark.numerical_verification
SUT = HarmonicOscillatorComparator


class TestHarmonicOscillatorComparator:
    """Own numerical evidence for the harmonic-oscillator comparator."""

    def test_method__execute__matches_hand_constructed_ground_state_pullback(
        self,
    ) -> None:
        r"""Evidence ID: NV-MODEL-SYSTEM-HO-001

        Requirement: For :math:`\hbar=m=\omega=1`, ``b=1``, ``h=0.5``, and
        ``K=1``, execute returns the scalar pullback of the independently specified
        three-point Dirichlet Hamiltonian through normalized analytic ground-state
        samples, and compares it with the exact retained energy ``0.5``.

        Method: Execute the public comparator once and compare every represented
        scalar and array with a separately assembled three-point matrix calculation.

        Oracle: On coordinates ``(-0.5, 0, 0.5)``, the represented Hamiltonian is
        the explicit matrix with diagonal ``(4.125, 4, 4.125)`` and adjacent entries
        ``-2``. The injection is the normalized vector proportional to
        ``exp(-x**2/2)``; scalar normalization cancels the common quadrature and
        ``pi**(-1/4)`` factors.

        Acceptance: Coordinates and reference energy agree exactly; injection,
        pullback, signed difference, and reported norms agree with the independent
        construction to ``8e-15`` relative and ``2e-15`` absolute tolerance.

        Interpretation: Agreement establishes the declared finite binary64 pullback
        for this one analytically specified request.

        Limitations: This single exactly specified finite case does not establish an
        asymptotic convergence rate or behavior for larger retained spaces.
        """
        analytical = HarmonicOscillatorAnalytical(
            HarmonicOscillatorNondimensionalizer().execute(
                hbar=1.0, mass=1.0, omega=1.0
            )
        )
        request = HarmonicOscillatorComparisonRequest(
            analytical=analytical,
            finite_difference=HarmonicOscillatorFiniteDifference(
                analytical,
                DirichletInterval(
                    UniformCartesianGrid1D(
                        ScalarQuantity(-1.0, Unitless()),
                        ScalarQuantity(1.0, Unitless()),
                        ScalarQuantity(0.5, Unitless()),
                    ),
                    DirichletBoundaryCondition(ScalarQuantity(0.0, Unitless())),
                ),
            ),
            ladder_operators=HarmonicOscillatorLadderOperators(
                analytical, LadderOperator1D(1)
            ),
        )

        result = HarmonicOscillatorComparator().execute(request)

        coordinates = np.array([-0.5, 0.0, 0.5], dtype=np.float64)
        unnormalized = np.exp(-0.5 * np.square(coordinates))
        injection = unnormalized / np.linalg.norm(unnormalized)
        finite_hamiltonian = np.array(
            [
                [4.125, -2.0, 0.0],
                [-2.0, 4.0, -2.0],
                [0.0, -2.0, 4.125],
            ],
            dtype=np.float64,
        )
        pulled_back = float(injection @ finite_hamiltonian @ injection)
        difference = pulled_back - 0.5

        np.testing.assert_array_equal(result.grid_coordinates.magnitude, coordinates)
        np.testing.assert_allclose(
            result.injection.magnitude[:, 0], injection, rtol=8.0e-15, atol=2.0e-15
        )
        np.testing.assert_array_equal(
            result.reference_hamiltonian.magnitude,
            np.array([[0.5]], dtype=np.float64),
        )
        np.testing.assert_allclose(
            result.pulled_back_hamiltonian.magnitude,
            np.array([[pulled_back]], dtype=np.float64),
            rtol=8.0e-15,
            atol=2.0e-15,
        )
        np.testing.assert_allclose(
            result.difference.magnitude,
            np.array([[difference]], dtype=np.float64),
            rtol=8.0e-15,
            atol=2.0e-15,
        )
        np.testing.assert_allclose(
            result.absolute_discrepancy.magnitude,
            abs(difference),
            rtol=8.0e-15,
            atol=2.0e-15,
        )
        np.testing.assert_allclose(
            result.relative_discrepancy.magnitude,
            abs(difference) / 0.5,
            rtol=8.0e-15,
            atol=2.0e-15,
        )
        np.testing.assert_allclose(
            result.diagonal_discrepancy.magnitude,
            abs(difference),
            rtol=8.0e-15,
            atol=2.0e-15,
        )
        assert result.off_diagonal_discrepancy.magnitude == 0.0
