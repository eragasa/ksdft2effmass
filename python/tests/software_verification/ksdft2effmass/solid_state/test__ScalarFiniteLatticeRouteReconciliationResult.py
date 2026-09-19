r"""Software verification of ``ScalarFiniteLatticeRouteReconciliationResult``.

Evidence profile: routine

Bounded artifact scope: immutable correlation of two gauge routes and their three
comparison outcomes.

Facet and represented meaning

The ResultObject requires parent, perturbation, and full comparisons to retain the exact
corresponding operators and one shared bridge and tolerance.

Intrinsic and cross-object scope

A passing one-site result and an intentionally misbound comparison are included.

VVUQ and scientific exclusions

This verifies retained result consistency, not a finite-domain campaign, scientific
validation, UQ, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.operators import PhysicalUnit
from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
    LatticeDisplacement,
    LocalizedOnsiteTerm,
    LocalizedPerturbation,
    ScalarFiniteLatticeRouteReconciliationResult,
    ScalarFiniteLatticeRouteReconciliationWorkflow,
    ScalarHoppingModel,
    ScalarHoppingTerm,
)

pytestmark = pytest.mark.software_verification
SUT = ScalarFiniteLatticeRouteReconciliationResult


class TestScalarFiniteLatticeRouteReconciliationResult:
    """Own software evidence for the route reconciliation ResultObject."""

    def test_constructor__comparison_correlation__requires_exact_route_operators(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-ROUTE-RECONCILIATION-002

        Requirement: Each retained comparison is bound to its named route operators.

        Acceptance: A passing result reports reconciliation; substituting its full
        comparison into the parent slot raises ``ValueError``.
        """
        unit = PhysicalUnit("electron_volt")
        result = ScalarFiniteLatticeRouteReconciliationWorkflow().execute(
            "one_site",
            ScalarHoppingModel(
                "parent",
                LatticeDimension.ONE,
                (
                    ScalarHoppingTerm(
                        LatticeDisplacement(LatticeDimension.ONE, (1,)),
                        -1.0,
                        0.0,
                    ),
                ),
                unit,
                "zero",
                "basis",
            ),
            LocalizedPerturbation(
                "defect",
                LatticeDimension.ONE,
                (
                    LocalizedOnsiteTerm(
                        LatticeCoordinate(LatticeDimension.ONE, (0,)), 0.2, 0.0
                    ),
                ),
                unit,
                "zero",
                "basis",
            ),
            FiniteLatticeShape(LatticeDimension.ONE, (1,)),
            BoundaryTwistLift(LatticeDimension.ONE, (0.0,)),
            absolute_tolerance=0.0,
        )

        assert result.is_reconciled
        with pytest.raises(ValueError, match="exact route operators"):
            replace(result, parent_equivalence=result.full_equivalence)
