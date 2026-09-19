r"""Software verification of ``ScalarFiniteLatticeOperatorAdder``.

Evidence profile: routine

Bounded artifact scope: compatibility-gated sparse composition of scalar finite-lattice
operators.

Facet and represented meaning

The ActionObject adds parent and localized represented matrices only after receiving a
passing result correlated to those exact operands.

Intrinsic and cross-object scope

Uniform-link and independently constructed quotient-seam full operators are composed and
reconciled through the explicit gauge bridge.

VVUQ and scientific exclusions

This verifies represented sparse composition and route agreement for synthetic inputs,
not a finite-domain calculation, scientific validation, UQ, or human acceptance.
"""

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
    LocalizedPerturbationOperatorConstructor,
    QuotientSeamOperatorConstructor,
    ScalarFiniteLatticeOperatorAdder,
    ScalarFiniteLatticeOperatorCompatibilityAnalyzer,
    ScalarHoppingModel,
    ScalarHoppingTerm,
    TwistedSupercellOperatorConstructor,
    TwistGaugeBridgeConstructor,
    TwistGaugeEquivalenceAnalyzer,
)

pytestmark = pytest.mark.software_verification
SUT = ScalarFiniteLatticeOperatorAdder


class TestScalarFiniteLatticeOperatorAdder:
    """Own software evidence for ``ScalarFiniteLatticeOperatorAdder``."""

    def test_method__execute__composes_and_reconciles_both_gauge_routes(self) -> None:
        """Evidence ID: SV-SOLID-STATE-OPERATOR-ADDITION-001

        Requirement: Parent and perturbation are added sparsely within each compatible
        gauge before route comparison.

        Acceptance: Independently constructed three-site full operators are equivalent
        through the explicit bridge at ``1e-14`` and retain composition provenance.
        """
        shape = FiniteLatticeShape(LatticeDimension.ONE, (3,))
        twist = BoundaryTwistLift(LatticeDimension.ONE, (0.25,))
        unit = PhysicalUnit("electron_volt")
        model = ScalarHoppingModel(
            "parent",
            LatticeDimension.ONE,
            (
                ScalarHoppingTerm(
                    LatticeDisplacement(LatticeDimension.ONE, (-1,)), -1.0, 0.0
                ),
                ScalarHoppingTerm(
                    LatticeDisplacement(LatticeDimension.ONE, (1,)), -1.0, 0.0
                ),
            ),
            unit,
            "zero",
            "basis",
        )
        perturbation = LocalizedPerturbation(
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
        )
        uniform_parent = TwistedSupercellOperatorConstructor().execute(
            "uniform_parent", model, shape, twist
        )
        uniform_defect = LocalizedPerturbationOperatorConstructor().execute(
            "uniform_defect", perturbation, shape, twist
        )
        seam_constructor = QuotientSeamOperatorConstructor()
        seam_parent = seam_constructor.execute_hopping(
            "seam_parent", model, shape, twist
        )
        seam_defect = seam_constructor.execute_perturbation(
            "seam_defect", perturbation, shape, twist
        )
        compatibility = ScalarFiniteLatticeOperatorCompatibilityAnalyzer()
        adder = ScalarFiniteLatticeOperatorAdder()
        uniform_full = adder.execute(
            "uniform_full",
            uniform_parent,
            uniform_defect,
            compatibility.execute(uniform_parent, uniform_defect),
        )
        seam_full = adder.execute(
            "seam_full",
            seam_parent,
            seam_defect,
            compatibility.execute(seam_parent, seam_defect),
        )
        bridge = TwistGaugeBridgeConstructor().execute(shape, uniform_full.twist_fiber)

        result = TwistGaugeEquivalenceAnalyzer().execute(
            uniform_full, seam_full, bridge, absolute_tolerance=1.0e-14
        )

        assert result.is_equivalent
        assert uniform_full.matrix.nonzero_count == 7
        assert uniform_full.provenance == (
            ("composer", "ScalarFiniteLatticeOperatorAdder"),
            ("left_operator", "uniform_parent"),
            ("right_operator", "uniform_defect"),
        )
