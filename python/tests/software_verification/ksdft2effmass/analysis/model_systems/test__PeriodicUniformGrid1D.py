r"""Software verification of ``PeriodicUniformGrid1D``.

Evidence profile: routine

Bounded artifact scope: extracted Appendix G periodic-1D public contract.

Facet and represented meaning

The public class retains or transforms the explicitly represented periodic-1D values.

Intrinsic and cross-object scope

Construction invariants and the demonstrated public operation are included.

VVUQ and scientific exclusions

This is software verification, not a rerun or scientific validation of Appendix G.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.model_systems import PeriodicUniformGrid1D
from ksdft2effmass.operators import PhysicalUnit, ScalarQuantity

pytestmark = pytest.mark.software_verification
SUT = PeriodicUniformGrid1D


class TestPeriodicUniformGrid1D:
    """Verify half-open periodic Cartesian grids."""

    def test_constructor__geometry__enumerates_half_open_points_in_period_units(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PERIODIC-ONE-D-006

        Requirement: The public contract enforces enumerates half open points in
        period units.

        Acceptance: The asserted values and failures match the declared contract.
        """
        grid = PeriodicUniformGrid1D(
            ScalarQuantity(500.0, PhysicalUnit("picometer")),
            ScalarQuantity(2.0, PhysicalUnit("nanometer")),
            4,
        )

        np.testing.assert_allclose(grid.origin.magnitude, 0.5)
        np.testing.assert_allclose(grid.spacing.magnitude, 0.5)
        np.testing.assert_allclose(grid.coordinates.magnitude, [0.5, 1.0, 1.5, 2.0])
        assert grid.coordinates.magnitude.flags.writeable is False

    def test_constructor__geometry__rejects_grid_with_fewer_than_three_points(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-PERIODIC-ONE-D-007

        Requirement: The public contract enforces rejects grid with fewer than
        three points.

        Acceptance: The asserted values and failures match the declared contract.
        """
        with pytest.raises(ValueError, match="at least three"):
            PeriodicUniformGrid1D(
                ScalarQuantity(0.0, PhysicalUnit("meter")),
                ScalarQuantity(1.0, PhysicalUnit("meter")),
                2,
            )
