r"""Software verification of ``ScalarHoppingBandShapeResult1D``.

Evidence profile: routine

Bounded artifact scope: correlated scalar periodic-1D hopping band-shape results.

Facet and represented meaning

The ResultObject retains bandwidth, curvature, imaginary residual, and disposition.

Intrinsic and cross-object scope

Scalar block dimension and pass consistency are included.

VVUQ and scientific exclusions

Result consistency does not establish effective-mass or material validation.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.hopping_diagnostics import (
    ScalarHoppingBandShapeAnalyzer1D,
    ScalarHoppingBandShapeResult1D,
)
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import BlockHoppingModel1D

pytestmark = pytest.mark.software_verification
SUT = ScalarHoppingBandShapeResult1D


class TestScalarHoppingBandShapeResult1D:
    """Own software evidence for ``ScalarHoppingBandShapeResult1D``."""

    def test_constructor__passes__rejects_imaginary_disposition_mismatch(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-023

        Requirement: Pass disposition follows imaginary residual and tolerance.

        Acceptance: Replacing a passing disposition with false raises ``ValueError``.
        """
        model = BlockHoppingModel1D(
            ScalarQuantity(1.0, Unitless()),
            (0,),
            (ComplexMatrixQuantity(np.asarray([[1.0]]), Unitless()),),
        )
        coordinates = VectorQuantity(np.asarray([0.0]), Unitless())
        valid = ScalarHoppingBandShapeAnalyzer1D().execute(
            model, coordinates, ScalarQuantity(0.0, Unitless())
        )

        with pytest.raises(ValueError, match="must match imaginary"):
            ScalarHoppingBandShapeResult1D(
                valid.model,
                valid.comparison_coordinates,
                valid.bandwidth,
                valid.zone_center_curvature,
                valid.maximum_imaginary_residual,
                valid.imaginary_absolute_tolerance,
                False,
            )
