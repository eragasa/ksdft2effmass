r"""Software verification of ``BlockHoppingModelComparator1D``.

Evidence profile: routine

Bounded artifact scope: periodic-1D hopping-route coefficient and operator defects.

Facet and represented meaning

The ActionObject compares compatible block models before and after interpolation.

Intrinsic and cross-object scope

Coefficient and sampled Frobenius defects with energy conversion are included.

VVUQ and scientific exclusions

Route agreement is not physical model validation or uncertainty quantification.
"""

import numpy as np
import pytest

from ksdft2effmass.analysis.hopping_fits import BlockHoppingModelComparator1D
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import BlockHoppingModel1D

pytestmark = pytest.mark.software_verification
SUT = BlockHoppingModelComparator1D


class TestBlockHoppingModelComparator1D:
    """Own software evidence for ``BlockHoppingModelComparator1D``."""

    def test_method__execute__separates_coefficient_and_sampled_defects(self) -> None:
        """Evidence ID: SV-ANALYSIS-PERIODIC-ONE-D-015

        Requirement: Coefficient and reciprocal-space defects remain separate metrics.

        Acceptance: An onsite ``0.1 eV`` offset gives coefficient ``0.1 eV`` and two-
        sample L2 defect ``sqrt(0.02) eV``.
        """
        reference = BlockHoppingModel1D(
            ScalarQuantity(1.0, Unitless()),
            (0,),
            (
                ComplexMatrixQuantity(
                    np.asarray([[1.0]]), PhysicalUnit("electron_volt")
                ),
            ),
        )
        candidate = BlockHoppingModel1D(
            ScalarQuantity(1.0, Unitless()),
            (0,),
            (
                ComplexMatrixQuantity(
                    np.asarray([[1100.0]]), PhysicalUnit("millielectron_volt")
                ),
            ),
        )

        result = BlockHoppingModelComparator1D().execute(
            reference,
            candidate,
            VectorQuantity(np.asarray([-0.25, 0.25]), Unitless()),
        )

        np.testing.assert_allclose(
            result.coefficient_l2_frobenius_defect.magnitude, 0.1
        )
        np.testing.assert_allclose(
            result.sampled_l2_frobenius_defect.magnitude, np.sqrt(0.02)
        )
        np.testing.assert_allclose(
            result.sampled_maximum_frobenius_defect.magnitude, 0.1
        )
