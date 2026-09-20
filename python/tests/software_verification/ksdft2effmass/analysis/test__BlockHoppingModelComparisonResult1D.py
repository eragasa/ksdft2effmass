r"""Software verification of ``BlockHoppingModelComparisonResult1D``.

Evidence profile: routine

Bounded artifact scope: correlated periodic-1D hopping-route comparison results.

Facet and represented meaning

The ResultObject retains compatible routes and nonnegative energy defects.

Intrinsic and cross-object scope

Representative compatibility and defect units are included.

VVUQ and scientific exclusions

Result consistency does not establish scientific equivalence.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.hopping_fits import BlockHoppingModelComparisonResult1D
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import BlockHoppingModel1D

pytestmark = pytest.mark.software_verification
SUT = BlockHoppingModelComparisonResult1D


class TestBlockHoppingModelComparisonResult1D:
    """Own software evidence for ``BlockHoppingModelComparisonResult1D``."""

    def test_constructor__defects__rejects_negative_magnitude(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-016

        Requirement: Every retained route defect is nonnegative.

        Acceptance: A negative coefficient defect raises ``ValueError``.
        """
        block = ComplexMatrixQuantity(np.asarray([[1.0]]), Unitless())
        model = BlockHoppingModel1D(
            ScalarQuantity(1.0, Unitless()), (0,), (block,)
        )

        with pytest.raises(ValueError, match="must be nonnegative"):
            BlockHoppingModelComparisonResult1D(
                model,
                model,
                VectorQuantity(np.asarray([0.0]), Unitless()),
                ScalarQuantity(-1.0, Unitless()),
                ScalarQuantity(0.0, Unitless()),
                ScalarQuantity(0.0, Unitless()),
            )
