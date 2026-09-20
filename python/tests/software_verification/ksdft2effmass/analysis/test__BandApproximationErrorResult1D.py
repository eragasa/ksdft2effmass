r"""Software verification of ``BandApproximationErrorResult1D``.

Evidence profile: routine

Bounded artifact scope: correlated periodic-band approximation-error results.

Facet and represented meaning

The ResultObject correlates target bands, candidate matrices, and an energy error.

Intrinsic and cross-object scope

Band dimension and sample count are included.

VVUQ and scientific exclusions

Result consistency does not establish model validity or uncertainty bounds.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.periodic_bands import (
    BandApproximationErrorResult1D,
    BandSpectrumSamples1D,
)
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import ReciprocalOperatorSamples1D

pytestmark = pytest.mark.software_verification
SUT = BandApproximationErrorResult1D


class TestBandApproximationErrorResult1D:
    """Own software evidence for ``BandApproximationErrorResult1D``."""

    def test_constructor__matrix_dimension__rejects_target_rank_mismatch(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-009

        Requirement: Candidate matrix dimension equals the target band count.

        Acceptance: A two-dimensional candidate for one target band raises an error.
        """
        coordinates = VectorQuantity(np.asarray([0.0]), Unitless())
        target = BandSpectrumSamples1D(
            coordinates,
            ScalarQuantity(1.0, Unitless()),
            MatrixQuantity(np.asarray([[1.0]]), Unitless()),
        )
        candidate = ReciprocalOperatorSamples1D(
            coordinates,
            ScalarQuantity(1.0, Unitless()),
            (ComplexMatrixQuantity(np.eye(2), Unitless()),),
        )

        with pytest.raises(ValueError, match="dimension must equal"):
            BandApproximationErrorResult1D(
                target, candidate, ScalarQuantity(0.0, Unitless())
            )
