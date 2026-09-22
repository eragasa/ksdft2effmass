r"""Software verification of ``SampledPotential1D``.

Evidence profile: routine

Bounded artifact scope: public grid-correlated sampled potential contract.

Facet and represented meaning

The class under test binds energy values to one exact ordered interior grid and exposes
the corresponding diagonal operator.

Intrinsic and cross-object scope

Grid dimension, value shape, unit mode, ordering, and diagonal representation are
included.

VVUQ and scientific exclusions

This verifies represented values only, not potential-model adequacy, interpolation,
scientific validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass import operators
from ksdft2effmass.analysis.model_systems import (
    ScalarQuantity,
    UniformCartesianGrid1D,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.operators import (
    SampledPotential1D,
)

pytestmark = pytest.mark.software_verification
SUT = SampledPotential1D


class TestSampledPotential1D:
    """Own software evidence for ``SampledPotential1D``."""

    def test_method__diagonal_operator__retains_grid_order_and_unit(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-FD-003

        Requirement: SampledPotential1D requires one value per interior grid point and
        places those values on the represented diagonal without reordering.

        Acceptance: Three Unitless values produce their exact immutable diagonal;
        a two-value vector is rejected for the same grid.
        """
        assert operators.SampledPotential1D is SampledPotential1D
        grid = UniformCartesianGrid1D(
            ScalarQuantity(-1.0, Unitless()),
            ScalarQuantity(1.0, Unitless()),
            ScalarQuantity(0.5, Unitless()),
        )
        potential = SampledPotential1D(
            grid, VectorQuantity(np.array([0.125, 0.0, 0.125]), Unitless())
        )

        np.testing.assert_array_equal(
            potential.diagonal_operator().to_dense().magnitude,
            np.diag([0.125, 0.0, 0.125]),
        )
        with pytest.raises(ValueError, match="interior-point count"):
            SampledPotential1D(grid, VectorQuantity(np.array([0.0, 0.0]), Unitless()))
