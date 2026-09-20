r"""Software verification of ``DirichletInterval``.

Evidence profile: routine

Bounded artifact scope: public model-independent one-dimensional interval contract.

Facet and represented meaning

The class under test composes uniform spatial representation with prescribed endpoint
values without selecting a Hamiltonian or physical model.

Intrinsic and cross-object scope

Exact grid and boundary ownership, interior dimension, and acceptance of both
homogeneous and nonhomogeneous Dirichlet values are included.

VVUQ and scientific exclusions

This verifies representation only, not differential-operator semantics, convergence,
scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis import model_systems
from ksdft2effmass.analysis.model_systems import (
    DirichletBoundaryCondition,
    DirichletInterval,
    ScalarQuantity,
    UniformCartesianGrid1D,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = DirichletInterval


class TestDirichletInterval:
    """Own software evidence for the reusable Dirichlet interval."""

    def test_constructor__representation__preserves_grid_and_boundary(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-INTERVAL-001

        Requirement: DirichletInterval owns grid and endpoint-value representation but
        does not impose homogeneous or harmonic-oscillator policy.

        Acceptance: The public class retains a nonhomogeneous condition and reports
        the grid's three interior points exactly.
        """
        assert model_systems.DirichletInterval is DirichletInterval
        grid = UniformCartesianGrid1D(
            ScalarQuantity(-1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(0.5, Unitless()),
        )
        boundary = DirichletBoundaryCondition(ScalarQuantity(2.0, Unitless()))

        interval = DirichletInterval(grid, boundary)

        assert interval.grid is grid
        assert interval.boundary_condition is boundary
        assert interval.interior_points == 3
        assert not interval.boundary_condition.is_homogeneous
