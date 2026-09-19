r"""Software verification of ``BoundaryPhaseStudyResult``.

Evidence profile: routine

Bounded artifact scope: one scalar metric and below-edge counts over an explicit twist
set for one finite geometry.

Facet and represented meaning

The ResultObject retains no-bound-state outcomes and excludes unavailable state-only
values from band summaries without treating them as process failures or zeros.

Intrinsic and cross-object scope

A synthetic 2D twist set with one no-bound-state outcome and invalid unavailable value
correlation are included.

VVUQ and scientific exclusions

Values are synthetic test data. This is not numerical or scientific validation, UQ,
campaign execution, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis.finite_domains import (
    BoundaryPhaseStudyResult,
    FiniteDomainScalarMetric,
)
from ksdft2effmass.operators import PhysicalUnit
from ksdft2effmass.solid_state import (
    BoundaryTwistMesh,
    FiniteLatticeShape,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = BoundaryPhaseStudyResult


class TestBoundaryPhaseStudyResult:
    """Own software evidence for the boundary-phase ResultObject."""

    def test_constructor__no_bound_state__retains_absence_without_zero_imputation(
        self,
    ) -> None:
        """Evidence ID: SV-ANALYSIS-BOUNDARY-PHASE-001

        Requirement: Unavailable state-only values correspond to zero below-edge states
        and are omitted, not zero-filled, in center and width summaries.

        Acceptance: One missing synthetic value yields one no-bound-state case and
        summaries over the two available values; contradictory absence raises.
        """
        mesh = BoundaryTwistMesh(LatticeDimension.TWO, (1, 3))
        result = BoundaryPhaseStudyResult(
            identifier="boundary_phase",
            metric=FiniteDomainScalarMetric(
                "synthetic_binding_energy", PhysicalUnit("electron_volt")
            ),
            shape=FiniteLatticeShape(LatticeDimension.TWO, (4, 4)),
            mesh=mesh,
            metric_values=(-0.2, None, -0.1),
            below_edge_state_counts=(1, 0, 1),
        )

        assert result.no_bound_state_count == 1
        assert result.band_center == pytest.approx(-0.15)
        assert result.band_width == pytest.approx(0.1)
        with pytest.raises(ValueError, match="zero below-edge"):
            BoundaryPhaseStudyResult(
                identifier="bad",
                metric=FiniteDomainScalarMetric(
                    "synthetic_binding_energy", PhysicalUnit("electron_volt")
                ),
                shape=result.shape,
                mesh=mesh,
                metric_values=(-0.2, None, -0.1),
                below_edge_state_counts=(1, 1, 1),
            )
