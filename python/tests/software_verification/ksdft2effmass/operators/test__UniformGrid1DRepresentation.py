r"""Software verification of ``UniformGrid1DRepresentation``.

Evidence profile: routine

Bounded artifact scope: public structural input contract for one-dimensional uniform
finite-difference grids.

Facet and represented meaning

The protocol identifies the coordinate unit, spacing, and interior dimension required
by represented operator constructors without reversing the analysis-to-operator
package dependency.

Intrinsic and cross-object scope

Runtime structural recognition of the public Cartesian grid is included.

VVUQ and scientific exclusions

This verifies software conformance only, not grid adequacy, discretization convergence,
scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis.model_systems import (
    ScalarQuantity,
    UniformCartesianGrid1D,
    Unitless,
)
from ksdft2effmass.operators import UniformGrid1DRepresentation

pytestmark = pytest.mark.software_verification
SUT = UniformGrid1DRepresentation


class TestUniformGrid1DRepresentation:
    """Own software evidence for the operator grid-input protocol."""

    def test_protocol__runtime_contract__accepts_public_uniform_cartesian_grid(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-FD-005

        Requirement: Operator construction depends on a structural uniform-grid input
        contract rather than importing the model-system implementation.

        Acceptance: The public UniformCartesianGrid1D satisfies the runtime protocol
        and exposes the declared Unitless spacing and interior count.
        """
        grid = UniformCartesianGrid1D(
            ScalarQuantity(-1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(0.5, Unitless()),
        )

        assert isinstance(grid, UniformGrid1DRepresentation)
        assert grid.interior_point_count == 3
        assert grid.spacing == ScalarQuantity(0.5, Unitless())
