r"""Software verification of ``FiniteDomainMeasureStudyResult``.

Evidence profile: routine

Bounded artifact scope: one scalar metric over an ordered finite-domain measure
sequence.

Facet and represented meaning

The ResultObject retains increasing geometries and signed adjacent changes without
creating a pooled or inferred convergence status.

Intrinsic and cross-object scope

A 2D square sequence and nonincreasing adverse sequence are included.

VVUQ and scientific exclusions

Values are synthetic test data. This is not numerical or scientific validation, UQ,
campaign execution, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis.finite_domains import (
    FiniteDomainMeasureStudyResult,
    FiniteDomainScalarMetric,
)
from ksdft2effmass.operators import Unitless
from ksdft2effmass.solid_state import FiniteLatticeShape, LatticeDimension

pytestmark = pytest.mark.software_verification
SUT = FiniteDomainMeasureStudyResult


class TestFiniteDomainMeasureStudyResult:
    """Own software evidence for the measure-channel ResultObject."""

    def test_constructor__ordered_measure__retains_only_adjacent_changes(self) -> None:
        """Evidence ID: SV-ANALYSIS-FINITE-DOMAIN-MEASURE-001

        Requirement: Measure results require strictly increasing cell counts and expose
        ordered signed changes without a convergence classification.

        Acceptance: Synthetic square values yield exact adjacent and final changes;
        reversing the final measure raises ``ValueError``.
        """
        shapes = (
            FiniteLatticeShape(LatticeDimension.TWO, (2, 2)),
            FiniteLatticeShape(LatticeDimension.TWO, (3, 3)),
            FiniteLatticeShape(LatticeDimension.TWO, (4, 4)),
        )
        result = FiniteDomainMeasureStudyResult(
            identifier="area",
            metric=FiniteDomainScalarMetric("synthetic_metric", Unitless()),
            shapes=shapes,
            values=(1.0, 0.6, 0.5),
            reference_shape=shapes[-1],
        )

        assert result.adjacent_changes == pytest.approx((-0.4, -0.1))
        assert result.final_change == pytest.approx(-0.1)
        with pytest.raises(ValueError, match="strictly increasing"):
            FiniteDomainMeasureStudyResult(
                identifier="bad",
                metric=FiniteDomainScalarMetric("synthetic_metric", Unitless()),
                shapes=(shapes[0], shapes[2], shapes[1]),
                values=(1.0, 0.5, 0.6),
                reference_shape=shapes[1],
            )
