r"""Software verification of ``SchrodingerKineticEnergy1D``.

Evidence profile: routine

Bounded artifact scope: public unit-aware represented kinetic-energy contract.

Facet and represented meaning

The class under test applies the declared action and mass scale to one represented
finite-difference Laplacian.

Intrinsic and cross-object scope

Parameter dimensions, unit mode, sign, scaling, and represented matrix units are
included.

VVUQ and scientific exclusions

This verifies finite represented scaling only, not discretization convergence,
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
)
from ksdft2effmass.operators import (
    SchrodingerKineticEnergy1D,
    SecondOrderCentralDifferenceLaplacian1D,
)

pytestmark = pytest.mark.software_verification
SUT = SchrodingerKineticEnergy1D


class TestSchrodingerKineticEnergy1D:
    """Own software evidence for ``SchrodingerKineticEnergy1D``."""

    def test_method__matrix__applies_negative_half_laplacian_scale(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-FD-002

        Requirement: Unitless ``hbar=m=1`` produces ``-L/2`` on the exact Laplacian
        grid.

        Acceptance: The public export is exact and spacing ``0.5`` produces kinetic
        diagonal ``4`` with adjacent entries ``-2`` in Unitless.
        """
        assert operators.SchrodingerKineticEnergy1D is SchrodingerKineticEnergy1D
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
        matrix = SchrodingerKineticEnergy1D(
            laplacian,
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
        ).matrix()

        np.testing.assert_array_equal(
            matrix.to_dense().magnitude,
            np.array([[4.0, -2.0, 0.0], [-2.0, 4.0, -2.0], [0.0, -2.0, 4.0]]),
        )
        assert isinstance(matrix.unit, Unitless)
