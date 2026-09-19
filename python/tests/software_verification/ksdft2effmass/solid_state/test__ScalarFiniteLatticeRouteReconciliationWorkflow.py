r"""Software verification of ``ScalarFiniteLatticeRouteReconciliationWorkflow``.

Evidence profile: routine

Bounded artifact scope: reusable one-case orchestration of uniform-link and
independently constructed quotient-seam scalar operators.

Facet and represented meaning

The Workflow constructs parent, localized perturbation, and composed full operators in
both gauges, then retains three explicit sparse gauge-equivalence analyses.

Intrinsic and cross-object scope

A two-dimensional synthetic case includes onsite and boundary-crossing directed bonds.

VVUQ and scientific exclusions

This is software route reconciliation for synthetic inputs. It is not finite-domain
campaign execution, numerical validation of a material model, UQ, or human acceptance.
"""

import pytest

from ksdft2effmass.operators import PhysicalUnit
from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
    LatticeDisplacement,
    LocalizedBondTerm,
    LocalizedOnsiteTerm,
    LocalizedPerturbation,
    ScalarFiniteLatticeRouteReconciliationWorkflow,
    ScalarHoppingModel,
    ScalarHoppingTerm,
    TwistGaugeRepresentation,
)

pytestmark = pytest.mark.software_verification
SUT = ScalarFiniteLatticeRouteReconciliationWorkflow


class TestScalarFiniteLatticeRouteReconciliationWorkflow:
    """Own software evidence for the one-case route Workflow."""

    def test_method__execute__reconciles_parent_perturbation_and_full_routes(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-ROUTE-RECONCILIATION-001

        Requirement: One execution retains both independent gauge routes and separately
        compares parent, perturbation, and composed full operators.

        Acceptance: All three synthetic 2D residuals pass at ``1e-14`` with their exact
        expected gauges and deterministic identifiers.
        """
        unit = PhysicalUnit("electron_volt")
        model = ScalarHoppingModel(
            "parent",
            LatticeDimension.TWO,
            (
                ScalarHoppingTerm(
                    LatticeDisplacement(LatticeDimension.TWO, (-1, 0)), -1.0, 0.0
                ),
                ScalarHoppingTerm(
                    LatticeDisplacement(LatticeDimension.TWO, (0, -1)), -0.8, 0.0
                ),
                ScalarHoppingTerm(
                    LatticeDisplacement(LatticeDimension.TWO, (0, 1)), -0.8, 0.0
                ),
                ScalarHoppingTerm(
                    LatticeDisplacement(LatticeDimension.TWO, (1, 0)), -1.0, 0.0
                ),
            ),
            unit,
            "zero",
            "basis",
        )
        perturbation = LocalizedPerturbation(
            "defect",
            LatticeDimension.TWO,
            (
                LocalizedOnsiteTerm(
                    LatticeCoordinate(LatticeDimension.TWO, (0, 0)), 0.2, 0.0
                ),
                LocalizedBondTerm(
                    LatticeCoordinate(LatticeDimension.TWO, (-1, 0)),
                    LatticeDisplacement(LatticeDimension.TWO, (1, 0)),
                    0.04,
                    0.0,
                ),
                LocalizedBondTerm(
                    LatticeCoordinate(LatticeDimension.TWO, (0, 0)),
                    LatticeDisplacement(LatticeDimension.TWO, (-1, 0)),
                    0.04,
                    0.0,
                ),
            ),
            unit,
            "zero",
            "basis",
        )

        result = ScalarFiniteLatticeRouteReconciliationWorkflow().execute(
            "case",
            model,
            perturbation,
            FiniteLatticeShape(LatticeDimension.TWO, (2, 3)),
            BoundaryTwistLift(LatticeDimension.TWO, (0.25, -0.125)),
            absolute_tolerance=1.0e-14,
        )

        assert result.is_reconciled
        assert result.uniform_parent.identifier == "case.uniform.parent"
        assert result.seam_full.identifier == "case.seam.full"
        assert (
            result.uniform_full.twist_fiber.gauge
            is TwistGaugeRepresentation.CENTERED_UNIFORM_LINK
        )
        assert (
            result.seam_full.twist_fiber.gauge is TwistGaugeRepresentation.QUOTIENT_SEAM
        )
        assert result.parent_equivalence.maximum_absolute_residual is not None
        assert result.parent_equivalence.maximum_absolute_residual <= 1.0e-15
        assert result.perturbation_equivalence.maximum_absolute_residual is not None
        assert result.perturbation_equivalence.maximum_absolute_residual <= 1.0e-15
        assert result.full_equivalence.maximum_absolute_residual is not None
        assert result.full_equivalence.maximum_absolute_residual <= 1.0e-15
