r"""Software verification of ``ObservedConvergenceOrderEstimator``.

Evidence profile: routine

Bounded artifact scope: adjacent-level observed-order calculation.

Facet and represented meaning

The ActionObject estimates one order for each adjacent positive error and spacing pair.

Intrinsic and cross-object scope

Ordering, units, and the historical leading-None representation are included.

VVUQ and scientific exclusions

This verifies the formula and does not establish convergence, validation, uncertainty
quantification, or human acceptance.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis import ObservedConvergenceOrderEstimator
from ksdft2effmass.operators import Unitless, VectorQuantity

pytestmark = pytest.mark.software_verification
SUT = ObservedConvergenceOrderEstimator


class TestObservedConvergenceOrderEstimator:
    """Own software evidence for ``ObservedConvergenceOrderEstimator``."""

    def test_method__execute__recovers_second_order_sequence(self) -> None:
        """Evidence ID: SV-ANALYSIS-ORDER-001

        Requirement: Adjacent orders use logarithmic error and spacing ratios.

        Acceptance: Errors proportional to spacing squared produce two orders equal
        to two and the retained leading-None sequence.
        """
        result = ObservedConvergenceOrderEstimator().execute(
            VectorQuantity(np.array([0.5, 0.25, 0.125]), Unitless()),
            VectorQuantity(np.array([0.25, 0.0625, 0.015625]), Unitless()),
        )

        assert result.nullable_orders() == (None, 2.0, 2.0)
