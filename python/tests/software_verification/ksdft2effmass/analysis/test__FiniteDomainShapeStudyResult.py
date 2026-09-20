r"""Software verification of ``FiniteDomainShapeStudyResult``.

Evidence profile: routine

Bounded artifact scope: fixed-measure geometry contrasts for one scalar metric.

Facet and represented meaning

The ResultObject retains a declared reference, signed contrasts, and spread while
providing no convergence pass status.

Intrinsic and cross-object scope

Synthetic equal-area rectangles and an unequal-area adverse case are included.

VVUQ and scientific exclusions

Values are synthetic test data. This is not numerical or scientific validation, UQ,
campaign execution, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis.finite_domains import (
    FiniteDomainScalarMetric,
    FiniteDomainShapeStudyResult,
)
from ksdft2effmass.operators import Unitless
from ksdft2effmass.solid_state import FiniteLatticeShape, LatticeDimension

pytestmark = pytest.mark.software_verification
SUT = FiniteDomainShapeStudyResult


class TestFiniteDomainShapeStudyResult:
    """Own software evidence for the fixed-measure shape ResultObject."""

    def test_constructor__fixed_measure__retains_reference_contrasts_and_spread(
        self,
    ) -> None:
        """Evidence ID: SV-ANALYSIS-FINITE-DOMAIN-SHAPE-001

        Requirement: Shape results compare distinct equal-measure geometries only.

        Acceptance: Synthetic area-12 rectangles retain reference contrasts and spread;
        an area mismatch raises ``ValueError``.
        """
        shapes = (
            FiniteLatticeShape(LatticeDimension.TWO, (2, 6)),
            FiniteLatticeShape(LatticeDimension.TWO, (3, 4)),
            FiniteLatticeShape(LatticeDimension.TWO, (6, 2)),
        )
        result = FiniteDomainShapeStudyResult(
            identifier="shape",
            metric=FiniteDomainScalarMetric("synthetic_metric", Unitless()),
            shapes=shapes,
            values=(0.8, 0.5, 0.7),
            reference_shape=shapes[1],
        )

        assert result.contrasts == pytest.approx((0.3, 0.0, 0.2))
        assert result.spread == pytest.approx(0.3)
        with pytest.raises(ValueError, match="fixed cell count"):
            FiniteDomainShapeStudyResult(
                identifier="bad",
                metric=FiniteDomainScalarMetric("synthetic_metric", Unitless()),
                shapes=(shapes[0], FiniteLatticeShape(LatticeDimension.TWO, (4, 4))),
                values=(0.8, 0.5),
                reference_shape=shapes[0],
            )
        one_dimensional = FiniteLatticeShape(LatticeDimension.ONE, (12,))
        with pytest.raises(ValueError, match="inapplicable in 1D"):
            FiniteDomainShapeStudyResult(
                identifier="inapplicable",
                metric=FiniteDomainScalarMetric("synthetic_metric", Unitless()),
                shapes=(one_dimensional, one_dimensional),
                values=(0.5, 0.5),
                reference_shape=one_dimensional,
            )
