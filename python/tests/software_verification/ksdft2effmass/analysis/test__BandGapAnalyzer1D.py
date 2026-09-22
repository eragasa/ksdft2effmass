r"""Software verification of ``BandGapAnalyzer1D``.

Evidence profile: routine

Bounded artifact scope: sampled internal and external direct band gaps.

Facet and represented meaning

The ActionObject analyzes one explicit contiguous selection without thresholds.

Intrinsic and cross-object scope

Scalar and composite selections are included.

VVUQ and scientific exclusions

A calculated sampled gap is not material validation or proof of global isolation.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.periodic_bands import (
    BandGapAnalyzer1D,
    BandSpectrumSamples1D,
    ContiguousBandSelection,
)
from ksdft2effmass.operators import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

pytestmark = pytest.mark.software_verification
SUT = BandGapAnalyzer1D


class TestBandGapAnalyzer1D:
    """Own software evidence for ``BandGapAnalyzer1D``."""

    def test_method__execute__measures_isolated_band_external_gap(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-005

        Requirement: A scalar selection has no internal gap and keeps the nearest
        external adjacent-band gap.

        Acceptance: The authored spectrum gives external gap ``1.0``.
        """
        spectrum = BandSpectrumSamples1D(
            VectorQuantity(np.asarray([-0.5, 0.0, 0.5]), Unitless()),
            ScalarQuantity(1.0, Unitless()),
            MatrixQuantity(
                np.asarray([[0.0, 1.0, 4.0], [0.2, 1.4, 3.0], [0.0, 1.0, 4.0]]),
                Unitless(),
            ),
        )

        result = BandGapAnalyzer1D().execute(spectrum, ContiguousBandSelection(1, 1))

        assert result.internal_minimum_gap is None
        assert result.external_minimum_gap is not None
        np.testing.assert_allclose(result.external_minimum_gap.magnitude, 1.0)

    def test_method__execute__separates_composite_internal_and_external_gaps(
        self,
    ) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-006

        Requirement: Composite internal and external gaps remain separate.

        Acceptance: The authored spectrum gives gaps ``1.0`` and ``1.6``.
        """
        spectrum = BandSpectrumSamples1D(
            VectorQuantity(np.asarray([-0.5, 0.0, 0.5]), Unitless()),
            ScalarQuantity(1.0, Unitless()),
            MatrixQuantity(
                np.asarray([[0.0, 1.0, 4.0], [0.2, 1.4, 3.0], [0.0, 1.0, 4.0]]),
                Unitless(),
            ),
        )

        result = BandGapAnalyzer1D().execute(spectrum, ContiguousBandSelection(0, 1))

        assert result.internal_minimum_gap is not None
        assert result.external_minimum_gap is not None
        np.testing.assert_allclose(result.internal_minimum_gap.magnitude, 1.0)
        np.testing.assert_allclose(result.external_minimum_gap.magnitude, 1.6)
