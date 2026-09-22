r"""Software verification of ``UniformCartesianGrid3D``.

Evidence profile: routine

Bounded artifact scope: public three-dimensional Cartesian tensor-product contract.

Facet and represented meaning

The class under test composes three ordered uniform axes with explicit indexing and
flattening conventions.

Intrinsic and cross-object scope

Axis correlation, shape, interior shape, indexing, and flattening order are included.

VVUQ and scientific exclusions

This verifies represented grid mechanics only, not numerical convergence, scientific
validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis import model_systems
from ksdft2effmass.analysis.model_systems import (
    ScalarQuantity,
    UniformCartesianGrid1D,
    UniformCartesianGrid3D,
    Unitless,
)

pytestmark = pytest.mark.software_verification
SUT = UniformCartesianGrid3D


class TestUniformCartesianGrid3D:
    """Own software evidence for ``UniformCartesianGrid3D``."""

    @staticmethod
    def axis() -> UniformCartesianGrid1D:
        """Return one three-point Unitless axis."""
        return UniformCartesianGrid1D(
            ScalarQuantity(-1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
        )

    def test_property__shape__uses_ij_tensor_product_order(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-GRID-004

        Requirement: The public three-dimensional grid composes three compatible axes
        and declares ``ij`` indexing with row-major flattening.

        Acceptance: Three three-point axes produce shape ``(3,3,3)``, interior shape
        ``(1,1,1)``, ``ij`` indexing, and ``C`` flattening.
        """
        assert model_systems.UniformCartesianGrid3D is UniformCartesianGrid3D
        grid = UniformCartesianGrid3D(self.axis(), self.axis(), self.axis())

        assert grid.shape == (3, 3, 3)
        assert grid.interior_shape == (1, 1, 1)
        assert grid.indexing == "ij"
        assert grid.flattening_order == "C"
        assert len(grid.coordinate_axes()) == 3
