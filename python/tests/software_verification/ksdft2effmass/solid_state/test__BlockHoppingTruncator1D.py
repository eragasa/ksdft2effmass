r"""Software verification of ``BlockHoppingTruncator1D``.

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

from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.solid_state import BlockHoppingModel1D, BlockHoppingTruncator1D

pytestmark = pytest.mark.software_verification
SUT = BlockHoppingTruncator1D


class TestBlockHoppingTruncator1D:
    """Verify symmetric finite-range block truncation."""

    def test_method__execute__retains_requested_range_and_reports_omitted_block_norm(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-006

        Requirement: The public contract enforces retains requested range and
        reports omitted block norm.

        Acceptance: The asserted values and failures match the declared contract.
        """
        values = (-0.2, 0.5, 2.0, 0.5, -0.2)
        model = BlockHoppingModel1D(
            ScalarQuantity(1.0, Unitless()),
            (-2, -1, 0, 1, 2),
            tuple(
                ComplexMatrixQuantity(np.asarray([[value]]), Unitless())
                for value in values
            ),
        )

        result = BlockHoppingTruncator1D().execute(model, 1)

        assert result.truncated.representatives == (-1, 0, 1)
        np.testing.assert_allclose(
            result.omitted_block_l2_norm, np.sqrt(0.08), atol=1.0e-15
        )
        assert result.source.representatives == (-2, -1, 0, 1, 2)
