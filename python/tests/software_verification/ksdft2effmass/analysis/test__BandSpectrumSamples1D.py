r"""Software verification of ``BandSpectrumSamples1D``.

Evidence profile: routine

Bounded artifact scope: sampled periodic-1D band-spectrum records.

Facet and represented meaning

The DataObject correlates reciprocal coordinates with a real energy table.

Intrinsic and cross-object scope

Coordinate normalization and sample dimensions are included.

VVUQ and scientific exclusions

This verifies software invariants, not the physical validity of sampled bands.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.periodic_bands import BandSpectrumSamples1D
from ksdft2effmass.operators import (
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

pytestmark = pytest.mark.software_verification
SUT = BandSpectrumSamples1D


class TestBandSpectrumSamples1D:
    """Own software evidence for ``BandSpectrumSamples1D``."""

    def test_constructor__samples__normalizes_reciprocal_coordinates(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-001

        Requirement: Coordinates are normalized to the reciprocal-period unit.

        Acceptance: Inverse-meter coordinates convert to inverse millimeters.
        """
        spectrum = BandSpectrumSamples1D(
            VectorQuantity(np.asarray([0.0, 500.0]), PhysicalUnit("1 / meter")),
            ScalarQuantity(1.0, PhysicalUnit("1 / millimeter")),
            MatrixQuantity(np.asarray([[1.0], [2.0]]), Unitless()),
        )

        np.testing.assert_allclose(spectrum.coordinates.magnitude, [0.0, 0.5])
        assert spectrum.sample_count == 2
        assert spectrum.band_count == 1

    def test_constructor__samples__rejects_row_count_mismatch(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-002

        Requirement: Every reciprocal coordinate has one eigenvalue row.

        Acceptance: A missing row raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="rows must equal"):
            BandSpectrumSamples1D(
                VectorQuantity(np.asarray([0.0, 0.5]), Unitless()),
                ScalarQuantity(1.0, Unitless()),
                MatrixQuantity(np.asarray([[1.0]]), Unitless()),
            )

    def test_constructor__samples__rejects_decreasing_band_order(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-010

        Requirement: Each retained row uses nondecreasing band-energy order.

        Acceptance: A decreasing row raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="nondecreasing"):
            BandSpectrumSamples1D(
                VectorQuantity(np.asarray([0.0]), Unitless()),
                ScalarQuantity(1.0, Unitless()),
                MatrixQuantity(np.asarray([[2.0, 1.0]]), Unitless()),
            )
