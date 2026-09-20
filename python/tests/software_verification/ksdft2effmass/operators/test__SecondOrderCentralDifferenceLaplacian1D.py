r"""Software verification of ``SecondOrderCentralDifferenceLaplacian1D``.

Evidence profile: routine

Bounded artifact scope: public represented one-dimensional Laplacian contract.

Facet and represented meaning

The class under test owns the centered second-order matrix on interior points of one
uniform grid with homogeneous Dirichlet data.

Intrinsic and cross-object scope

Grid correlation, boundary admissibility, stencil coefficients, units, and immutable
storage are included.

VVUQ and scientific exclusions

This verifies one finite stencil. It does not establish convergence to the continuum
Laplacian, scientific validation, uncertainty quantification, or human acceptance.
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
    SecondOrderCentralDifferenceLaplacian1D,
)

pytestmark = pytest.mark.software_verification
SUT = SecondOrderCentralDifferenceLaplacian1D


class TestSecondOrderCentralDifferenceLaplacian1D:
    """Own software evidence for the represented one-dimensional Laplacian."""

    def test_method__matrix__matches_centered_dirichlet_stencil(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-FD-001

        Requirement: The public Laplacian builds the centered three-point stencil on
        ordered interior points and requires homogeneous Dirichlet data.

        Acceptance: Spacing ``0.5`` produces diagonal ``-8`` and adjacent ``4`` in a
        Unitless immutable matrix; nonhomogeneous data are rejected.
        """
        assert operators.SecondOrderCentralDifferenceLaplacian1D is (
            SecondOrderCentralDifferenceLaplacian1D
        )
        grid = UniformCartesianGrid1D(
            ScalarQuantity(-1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(0.5, Unitless()),
        )
        condition = DirichletBoundaryCondition(ScalarQuantity(0.0, Unitless()))
        matrix = SecondOrderCentralDifferenceLaplacian1D(
            DirichletInterval(grid, condition)
        ).matrix()

        np.testing.assert_array_equal(
            matrix.to_dense().magnitude,
            np.array([[-8.0, 4.0, 0.0], [4.0, -8.0, 4.0], [0.0, 4.0, -8.0]]),
        )
        assert isinstance(matrix.unit, Unitless)
        assert not matrix.data.flags.writeable
        with pytest.raises(ValueError, match="requires homogeneous"):
            SecondOrderCentralDifferenceLaplacian1D(
                DirichletInterval(
                    grid,
                    DirichletBoundaryCondition(ScalarQuantity(1.0, Unitless())),
                )
            )
