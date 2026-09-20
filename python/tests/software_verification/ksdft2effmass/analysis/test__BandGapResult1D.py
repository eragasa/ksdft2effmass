r"""Software verification of ``BandGapResult1D``.

Evidence profile: routine

Bounded artifact scope: correlated sampled band-gap results.

Facet and represented meaning

The ResultObject distinguishes unavailable internal and external gaps.

Intrinsic and cross-object scope

Selection rank and retained-spectrum bounds are included.

VVUQ and scientific exclusions

Result consistency does not establish global or material band isolation.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.periodic_bands import (
    BandGapResult1D,
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
SUT = BandGapResult1D


class TestBandGapResult1D:
    """Own software evidence for ``BandGapResult1D``."""

    def test_constructor__gap_availability__rejects_scalar_internal_gap(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-007

        Requirement: A one-band selection has no internal adjacent-band gap.

        Acceptance: A numeric internal gap raises ``ValueError``.
        """
        spectrum = BandSpectrumSamples1D(
            VectorQuantity(np.asarray([0.0]), Unitless()),
            ScalarQuantity(1.0, Unitless()),
            MatrixQuantity(np.asarray([[0.0, 1.0]]), Unitless()),
        )

        with pytest.raises(ValueError, match="no internal gap"):
            BandGapResult1D(
                spectrum,
                ContiguousBandSelection(0, 0),
                ScalarQuantity(1.0, Unitless()),
                ScalarQuantity(1.0, Unitless()),
            )
