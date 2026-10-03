r"""Software verification of ``AbstractDirichletIntervalRepresentation``.

Evidence profile: routine

Bounded artifact scope: public nominal interval input contract for represented
Dirichlet operators.

Facet and represented meaning

The nominal ABC identifies grid and boundary components required by operator
construction while concrete interval ownership remains with model-system analysis.

Intrinsic and cross-object scope

Nominal recognition and structural-lookalike rejection are included.

VVUQ and scientific exclusions

This verifies software conformance only, not operator convergence, scientific
validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis.model_systems import (
    DirichletBoundaryCondition,
    DirichletInterval,
    ScalarQuantity,
    UniformCartesianGrid1D,
    Unitless,
)
from ksdft2effmass.operators import AbstractDirichletIntervalRepresentation

pytestmark = pytest.mark.software_verification
SUT = AbstractDirichletIntervalRepresentation


class TestDirichletIntervalRepresentation:
    """Own software evidence for the operator interval-input ABC."""

    def test_abc__rejects_non_inheriting_interval_lookalike(self) -> None:
        """Require nominal membership even when both interval properties match."""

        class IntervalLookalike:
            grid = UniformCartesianGrid1D(
                ScalarQuantity(-1.0, Unitless()),
                ScalarQuantity(1.0, Unitless()),
                ScalarQuantity(0.5, Unitless()),
            )
            boundary_condition = DirichletBoundaryCondition(
                ScalarQuantity(0.0, Unitless())
            )

        assert not isinstance(IntervalLookalike(), SUT)

    def test_abc__nominal_membership__accepts_public_dirichlet_interval(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-FD-007

        Requirement: Operator construction consumes a nominal interval ABC without
        importing the analysis implementation.

        Acceptance: The public DirichletInterval satisfies the nominal ABC and
        exposes conforming grid and boundary components.
        """
        interval = DirichletInterval(
            UniformCartesianGrid1D(
                ScalarQuantity(-1.0, Unitless()),
                ScalarQuantity(1.0, Unitless()),
                ScalarQuantity(0.5, Unitless()),
            ),
            DirichletBoundaryCondition(ScalarQuantity(0.0, Unitless())),
        )

        assert isinstance(interval, AbstractDirichletIntervalRepresentation)
        assert interval.grid.interior_point_count == 3
        assert interval.boundary_condition.condition_kind == "dirichlet"
