r"""Software verification of ``UniformCartesianGrid1D``.

Evidence profile: routine

Bounded artifact scope: public one-dimensional uniform Cartesian grid contract.

Facet and represented meaning

The class under test owns ordered unit-aware axis geometry including boundaries.

Intrinsic and cross-object scope

Coordinate ordering, spacing, interior selection, divisibility, and unit conversion are
included.

VVUQ and scientific exclusions

This verifies represented grid mechanics. It establishes no discretization convergence,
scientific validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis import model_systems
from ksdft2effmass.analysis.model_systems import (
    ScalarQuantity,
    UniformCartesianGrid1D,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = UniformCartesianGrid1D


class TestUniformCartesianGrid1D:
    """Own software evidence for ``UniformCartesianGrid1D``."""

    def test_public_api__package__exports_supported_grid_class(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-GRID-001

        Requirement: UniformCartesianGrid1D is publicly exported.

        Acceptance: The package binding is the documented class object.
        """
        assert model_systems.UniformCartesianGrid1D is UniformCartesianGrid1D

    def test_method__interior_coordinates__preserves_uniform_order_and_unit(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-GRID-002

        Requirement: A one-dimensional grid includes both boundaries, exposes its
        ordered interior coordinates, and rejects a nondivisible requested spacing.

        Acceptance: ``[-1,1]`` with spacing ``0.5`` has five points and interior
        coordinates ``(-0.5,0,0.5)`` in Unitless; spacing ``0.3`` is rejected.
        """
        grid = UniformCartesianGrid1D(
            ScalarQuantity(-1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(0.5, Unitless()),
        )

        assert grid.point_count == 5
        assert grid.interior_point_count == 3
        assert grid.spacing == ScalarQuantity(0.5, Unitless())
        np.testing.assert_array_equal(
            grid.interior_coordinates().magnitude, [-0.5, 0.0, 0.5]
        )
        with pytest.raises(ValueError, match="must divide"):
            UniformCartesianGrid1D(
                ScalarQuantity(-1.0, Unitless()),
                ScalarQuantity(1.0, Unitless()),
                ScalarQuantity(0.3, Unitless()),
            )
