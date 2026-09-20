r"""Software verification of ``BandApproximationErrorAnalyzer1D``.

Evidence profile: routine

Bounded artifact scope: eigenvalue errors for represented reduced operators.

Facet and represented meaning

The ActionObject compares ordered Hermitian matrix eigenvalues with target bands.

Intrinsic and cross-object scope

Coordinate and energy-unit compatibility are included.

VVUQ and scientific exclusions

The error is a software comparison, not uncertainty quantification or validation.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.periodic_bands import (
    BandApproximationErrorAnalyzer1D,
    BandSpectrumSamples1D,
)
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import ReciprocalOperatorSamples1D

pytestmark = pytest.mark.software_verification
SUT = BandApproximationErrorAnalyzer1D


class TestBandApproximationErrorAnalyzer1D:
    """Own software evidence for ``BandApproximationErrorAnalyzer1D``."""

    def test_method__execute__compares_ordered_eigenvalues_across_energy_units(
        self,
    ) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-008

        Requirement: Candidate eigenvalues are converted to the target energy unit
        before their maximum absolute difference is measured.

        Acceptance: The authored scalar candidates have maximum error ``0.1 eV``.
        """
        coordinates = VectorQuantity(np.asarray([0.0, 0.25]), Unitless())
        target = BandSpectrumSamples1D(
            coordinates,
            ScalarQuantity(1.0, Unitless()),
            MatrixQuantity(
                np.asarray([[1.0], [2.0]]), PhysicalUnit("electron_volt")
            ),
        )
        candidate = ReciprocalOperatorSamples1D(
            coordinates,
            ScalarQuantity(1.0, Unitless()),
            (
                ComplexMatrixQuantity(
                    np.asarray([[900.0]]), PhysicalUnit("millielectron_volt")
                ),
                ComplexMatrixQuantity(
                    np.asarray([[2050.0]]), PhysicalUnit("millielectron_volt")
                ),
            ),
        )

        result = BandApproximationErrorAnalyzer1D().execute(
            target, candidate, 0.0
        )

        np.testing.assert_allclose(result.maximum_absolute_error.magnitude, 0.1)
        assert result.maximum_absolute_error.unit == target.eigenvalues.unit
