r"""Software verification of ``BlockHoppingTruncationResult1D``.

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
from ksdft2effmass.solid_state import (
    BlockHoppingModel1D,
    BlockHoppingTruncationResult1D,
)

pytestmark = pytest.mark.software_verification
SUT = BlockHoppingTruncationResult1D


class TestBlockHoppingTruncationResult1D:
    """Verify correlations retained by a block-hopping truncation result."""

    def test_constructor__truncation__rejects_representatives_inconsistent_with_range(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-005

        Requirement: The public contract enforces rejects representatives
        inconsistent with range.

        Acceptance: The asserted values and failures match the declared contract.
        """
        block = ComplexMatrixQuantity(np.asarray([[1.0]]), Unitless())
        source = BlockHoppingModel1D(
            ScalarQuantity(1.0, Unitless()), (-1, 0, 1), (block, block, block)
        )
        invalid = BlockHoppingModel1D(
            ScalarQuantity(1.0, Unitless()), (-1, 0), (block, block)
        )

        with pytest.raises(ValueError, match="match maximum_range"):
            BlockHoppingTruncationResult1D(source, 0, invalid, 1.0)
