r"""Software verification of ``ScalarHoppingBandShapeAnalyzer1D``.

Evidence profile: routine

Bounded artifact scope: scalar periodic-1D hopping bandwidth and curvature.

Facet and represented meaning

The ActionObject evaluates real band shape and imaginary residual separately.

Intrinsic and cross-object scope

Sampled bandwidth and analytical reduced-coordinate center curvature are included.

VVUQ and scientific exclusions

Band-shape diagnostics do not establish effective-mass validation.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.hopping_diagnostics import (
    ScalarHoppingBandShapeAnalyzer1D,
)
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import BlockHoppingModel1D

pytestmark = pytest.mark.software_verification
SUT = ScalarHoppingBandShapeAnalyzer1D


class TestScalarHoppingBandShapeAnalyzer1D:
    """Own software evidence for ``ScalarHoppingBandShapeAnalyzer1D``."""

    def test_method__execute__evaluates_cosine_bandwidth_and_curvature(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-022

        Requirement: ``T[-1]=T[1]=0.5`` and ``T[0]=2`` represent
        ``2 + cos(2 pi k)`` in reduced momentum.

        Acceptance: Bandwidth is two and zone-center curvature is ``-4 pi^2``.
        """
        model = BlockHoppingModel1D(
            ScalarQuantity(1.0, Unitless()),
            (-1, 0, 1),
            (
                ComplexMatrixQuantity(np.asarray([[0.5]]), Unitless()),
                ComplexMatrixQuantity(np.asarray([[2.0]]), Unitless()),
                ComplexMatrixQuantity(np.asarray([[0.5]]), Unitless()),
            ),
        )

        result = ScalarHoppingBandShapeAnalyzer1D().execute(
            model,
            VectorQuantity(np.asarray([-0.5, 0.0, 0.5]), Unitless()),
            ScalarQuantity(1.0e-14, Unitless()),
        )

        np.testing.assert_allclose(result.bandwidth.magnitude, 2.0)
        np.testing.assert_allclose(
            result.zone_center_curvature.magnitude, -4.0 * np.pi**2
        )
        assert result.maximum_imaginary_residual.magnitude == 0.0
        assert result.passes
