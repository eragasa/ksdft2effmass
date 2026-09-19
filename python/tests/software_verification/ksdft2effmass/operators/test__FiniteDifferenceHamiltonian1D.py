r"""Software verification of ``FiniteDifferenceHamiltonian1D``.

Evidence profile: routine

Bounded artifact scope: public compatible kinetic-plus-potential composition contract.

Facet and represented meaning

The class under test composes two represented energy matrices only after exact grid and
unit compatibility.

Intrinsic and cross-object scope

Grid correlation, energy-unit compatibility, signed matrix addition, and immutability
are included.

VVUQ and scientific exclusions

This verifies represented operator composition only, not continuum convergence,
scientific validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass import operators
from ksdft2effmass.analysis.model_systems import (
    DirichletBoundaryCondition,
    DirichletInterval,
    ScalarQuantity,
    UniformCartesianGrid1D,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.operators import (
    FiniteDifferenceHamiltonian1D,
    SampledPotential1D,
    SchrodingerKineticEnergy1D,
    SecondOrderCentralDifferenceLaplacian1D,
)

pytestmark = pytest.mark.software_verification
SUT = FiniteDifferenceHamiltonian1D


class TestFiniteDifferenceHamiltonian1D:
    """Own software evidence for ``FiniteDifferenceHamiltonian1D``."""

    def test_method__matrix__adds_compatible_kinetic_and_potential_energies(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-FD-004

        Requirement: The Hamiltonian composes kinetic and potential matrices sharing
        the exact grid and compatible energy unit.

        Acceptance: The dimensionless three-point kinetic matrix plus potential
        ``diag(0.125,0,0.125)`` produces the exact declared immutable sum.
        """
        assert operators.FiniteDifferenceHamiltonian1D is (
            FiniteDifferenceHamiltonian1D
        )
        grid = UniformCartesianGrid1D(
            ScalarQuantity(-1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(0.5, Unitless()),
        )
        laplacian = SecondOrderCentralDifferenceLaplacian1D(
            DirichletInterval(
                grid, DirichletBoundaryCondition(ScalarQuantity(0.0, Unitless()))
            )
        )
        kinetic = SchrodingerKineticEnergy1D(
            laplacian,
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
        )
        potential = SampledPotential1D(
            grid, VectorQuantity(np.array([0.125, 0.0, 0.125]), Unitless())
        )

        matrix = FiniteDifferenceHamiltonian1D(kinetic, potential).matrix()

        np.testing.assert_array_equal(
            matrix.to_dense().magnitude,
            np.array([[4.125, -2.0, 0.0], [-2.0, 4.0, -2.0], [0.0, -2.0, 4.125]]),
        )
        assert isinstance(matrix.unit, Unitless)
        assert not matrix.data.flags.writeable
