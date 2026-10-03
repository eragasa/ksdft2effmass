r"""Software verification of ``AbstractUniformGrid1DRepresentation``.

Evidence profile: routine

Bounded artifact scope: public nominal input contract for one-dimensional uniform
finite-difference grids.

Facet and represented meaning

The nominal ABC identifies the coordinate unit, spacing, and interior dimension required
by represented operator constructors without reversing the analysis-to-operator
package dependency.

Intrinsic and cross-object scope

Nominal recognition and structural-lookalike rejection are included.

VVUQ and scientific exclusions

This verifies software conformance only, not grid adequacy, discretization convergence,
scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

import ksdft2effmass.operators as operator_api
from ksdft2effmass.analysis.model_systems import (
    ScalarQuantity,
    UniformCartesianGrid1D,
    Unitless,
)
from ksdft2effmass.operators import AbstractUniformGrid1DRepresentation

pytestmark = pytest.mark.software_verification
SUT = AbstractUniformGrid1DRepresentation


class TestUniformGrid1DRepresentation:
    """Own software evidence for the operator grid-input ABC."""

    def test_public_api__retired_representation_names_are_absent(self) -> None:
        """Expose only nominal ABC names at the operator package boundary."""
        retired = (
            "UniformGrid1DRepresentation",
            "DirichletBoundaryConditionRepresentation",
            "DirichletIntervalRepresentation",
        )

        assert all(not hasattr(operator_api, name) for name in retired)

    def test_abc__rejects_non_inheriting_grid_lookalike(self) -> None:
        """Require nominal membership even when all grid properties match."""

        class GridLookalike:
            coordinate_unit = Unitless()
            spacing = ScalarQuantity(0.5, Unitless())
            interior_point_count = 3

        assert not isinstance(GridLookalike(), SUT)

    def test_abc__nominal_membership__accepts_public_uniform_cartesian_grid(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-FD-005

        Requirement: Operator construction depends on a nominal uniform-grid ABC
        rather than importing the model-system implementation.

        Acceptance: The public UniformCartesianGrid1D satisfies the nominal ABC
        and exposes the declared Unitless spacing and interior count.
        """
        grid = UniformCartesianGrid1D(
            ScalarQuantity(-1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(0.5, Unitless()),
        )

        assert isinstance(grid, AbstractUniformGrid1DRepresentation)
        assert grid.interior_point_count == 3
        assert grid.spacing == ScalarQuantity(0.5, Unitless())
