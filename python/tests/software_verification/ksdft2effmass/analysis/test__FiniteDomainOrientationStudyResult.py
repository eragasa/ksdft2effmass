r"""Software verification of ``FiniteDomainOrientationStudyResult``.

Evidence profile: routine

Bounded artifact scope: separate same-parent orientation contrasts and
transformed-parent covariance residuals.

Facet and represented meaning

The ResultObject keeps physical contrasts, which may be signed and nonzero, distinct
from nonnegative algebraic covariance residuals.

Intrinsic and cross-object scope

Two synthetic 2D orientation pairs and a negative-residual adverse case are included.

VVUQ and scientific exclusions

Values are synthetic test data. This is not numerical or scientific validation, UQ,
campaign execution, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis.finite_domains import (
    FiniteDomainOrientationStudyResult,
    FiniteDomainScalarMetric,
)
from ksdft2effmass.operators import PhysicalUnit
from ksdft2effmass.solid_state import FiniteLatticeShape, LatticeDimension

pytestmark = pytest.mark.software_verification
SUT = FiniteDomainOrientationStudyResult


class TestFiniteDomainOrientationStudyResult:
    """Own software evidence for the orientation-channel ResultObject."""

    def test_constructor__separate_outcomes__preserves_contrast_and_covariance(
        self,
    ) -> None:
        """Evidence ID: SV-ANALYSIS-FINITE-DOMAIN-ORIENTATION-001

        Requirement: Same-parent contrasts and transformed-parent residuals remain
        separate fields with different sign semantics.

        Acceptance: Signed contrasts are retained, while a negative covariance residual
        raises ``ValueError``.
        """
        pairs = (
            (
                FiniteLatticeShape(LatticeDimension.TWO, (2, 6)),
                FiniteLatticeShape(LatticeDimension.TWO, (6, 2)),
            ),
            (
                FiniteLatticeShape(LatticeDimension.TWO, (3, 4)),
                FiniteLatticeShape(LatticeDimension.TWO, (4, 3)),
            ),
        )
        result = FiniteDomainOrientationStudyResult(
            identifier="orientation",
            metric=FiniteDomainScalarMetric(
                "synthetic_energy", PhysicalUnit("electron_volt")
            ),
            shape_pairs=pairs,
            same_parent_contrasts=(-0.2, 0.1),
            transformed_parent_covariance_residuals=(1.0e-15, 2.0e-15),
        )

        assert result.same_parent_contrasts == (-0.2, 0.1)
        assert result.transformed_parent_covariance_residuals == (1.0e-15, 2.0e-15)
        with pytest.raises(ValueError, match="nonnegative"):
            FiniteDomainOrientationStudyResult(
                identifier="bad",
                metric=FiniteDomainScalarMetric(
                    "synthetic_energy", PhysicalUnit("electron_volt")
                ),
                shape_pairs=(pairs[0],),
                same_parent_contrasts=(0.2,),
                transformed_parent_covariance_residuals=(-1.0e-15,),
            )
