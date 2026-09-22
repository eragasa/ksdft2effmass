r"""Software verification of ``ScalarFiniteLatticeOperatorCompatibilityAnalyzer``.

Evidence profile: routine

Bounded artifact scope: structured metadata prerequisites for represented scalar
operator addition.

Facet and represented meaning

The ActionObject compares shape, twist fiber, basis identity, unit, and energy reference
without performing matrix arithmetic.

Intrinsic and cross-object scope

Matching operands and simultaneous basis/reference mismatches are included.

VVUQ and scientific exclusions

This is software compatibility evidence, not physical alignment, scientific validation,
UQ, or human acceptance.
"""

from dataclasses import replace

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import ComplexSparseMatrixQuantity, Unitless
from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    BoundaryTwistReducer,
    FiniteLatticeShape,
    LatticeDimension,
    ScalarFiniteLatticeOperator,
    ScalarFiniteLatticeOperatorCompatibilityAnalyzer,
    ScalarFiniteLatticeOperatorCompatibilityIssueCode,
    TwistFiber,
    TwistGaugeRepresentation,
)

pytestmark = pytest.mark.software_verification
SUT = ScalarFiniteLatticeOperatorCompatibilityAnalyzer


class TestScalarFiniteLatticeOperatorCompatibilityAnalyzer:
    """Own software evidence for the operator compatibility analyzer."""

    def test_method__execute__reports_all_metadata_mismatches(self) -> None:
        """Evidence ID: SV-SOLID-STATE-OPERATOR-COMPATIBILITY-001

        Requirement: Compatibility is exact and reports every mismatched prerequisite.

        Acceptance: Equal operands pass; changed basis and energy-reference identities
        return both canonical issue codes without matrix arithmetic.
        """
        shape = FiniteLatticeShape(LatticeDimension.ONE, (1,))
        reduction = BoundaryTwistReducer().execute(
            BoundaryTwistLift(LatticeDimension.ONE, (0.0,))
        )
        fiber = TwistFiber(reduction, TwistGaugeRepresentation.CENTERED_UNIFORM_LINK)
        matrix = ComplexSparseMatrixQuantity.from_csr(
            sparse.csr_array(np.array([[1.0 + 0.0j]])), Unitless()
        )
        left = ScalarFiniteLatticeOperator(
            "left", matrix, shape, fiber, "basis", "zero", ()
        )
        analyzer = ScalarFiniteLatticeOperatorCompatibilityAnalyzer()

        passing = analyzer.execute(left, replace(left, identifier="right"))
        failing = analyzer.execute(
            left,
            replace(
                left,
                identifier="different",
                basis_identifier="other_basis",
                energy_reference="other_zero",
            ),
        )

        assert passing.compatible
        assert failing.issue_codes == (
            ScalarFiniteLatticeOperatorCompatibilityIssueCode.BASIS,
            ScalarFiniteLatticeOperatorCompatibilityIssueCode.ENERGY_REFERENCE,
        )
        assert not failing.compatible
