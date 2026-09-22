r"""Software verification of ``BlockHoppingModel1D``.

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
from ksdft2effmass.solid_state import BlockHoppingModel1D

pytestmark = pytest.mark.software_verification
SUT = BlockHoppingModel1D


class TestBlockHoppingModel1D:
    """Verify ordered matrix-valued cell-hopping models."""

    def test_constructor__hoppings__retains_block_dimension_and_maximum_range(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-003

        Requirement: The public contract enforces retains block dimension and
        maximum range.

        Acceptance: The asserted values and failures match the declared contract.
        """
        block = ComplexMatrixQuantity(np.eye(2), Unitless())

        model = BlockHoppingModel1D(
            ScalarQuantity(1.0, Unitless()), (-2, 0, 3), (block, block, block)
        )

        assert model.matrix_dimension == 2
        assert model.maximum_range == 3

    def test_constructor__hoppings__rejects_unsorted_or_duplicate_representatives(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-PERIODIC-ONE-D-004

        Requirement: The public contract enforces rejects unsorted or duplicate
        representatives.

        Acceptance: The asserted values and failures match the declared contract.
        """
        block = ComplexMatrixQuantity(np.eye(1), Unitless())

        with pytest.raises(ValueError, match="strictly increasing"):
            BlockHoppingModel1D(
                ScalarQuantity(1.0, Unitless()), (0, -1, 0), (block, block, block)
            )
