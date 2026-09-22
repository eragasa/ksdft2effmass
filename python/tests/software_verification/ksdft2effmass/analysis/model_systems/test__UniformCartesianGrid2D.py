r"""Software verification of ``UniformCartesianGrid2D``.

Evidence profile: routine

Bounded artifact scope: public two-dimensional Cartesian tensor-product contract.

Facet and represented meaning

The class under test composes two ordered uniform axes with explicit indexing and
flattening conventions.

Intrinsic and cross-object scope

Axis correlation, shape, interior shape, indexing, and flattening order are included.

VVUQ and scientific exclusions

This verifies represented grid mechanics only, not numerical convergence, scientific
validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis import model_systems
from ksdft2effmass.analysis.model_systems import (
    ScalarQuantity,
    UniformCartesianGrid1D,
    UniformCartesianGrid2D,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = UniformCartesianGrid2D


class TestUniformCartesianGrid2D:
    """Own software evidence for ``UniformCartesianGrid2D``."""

    def test_property__shape__uses_ij_tensor_product_order(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-GRID-003

        Requirement: The public two-dimensional grid composes two compatible axes and
        declares ``ij`` indexing with row-major flattening.

        Acceptance: Axes with five and three points produce shape ``(5,3)``, interior
        shape ``(3,1)``, ``ij`` indexing, and ``C`` flattening.
        """
        assert model_systems.UniformCartesianGrid2D is UniformCartesianGrid2D
        first = UniformCartesianGrid1D(
            ScalarQuantity(-1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(0.5, Unitless()),
        )
        second = UniformCartesianGrid1D(
            ScalarQuantity(0.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(0.5, Unitless()),
        )

        grid = UniformCartesianGrid2D(first, second)

        assert grid.shape == (5, 3)
        assert grid.interior_shape == (3, 1)
        assert grid.indexing == "ij"
        assert grid.flattening_order == "C"
        axes = grid.coordinate_axes()
        np.testing.assert_array_equal(axes[0].magnitude, first.coordinates().magnitude)
        np.testing.assert_array_equal(axes[1].magnitude, second.coordinates().magnitude)
