r"""Software verification of ``ScalarFiniteLatticeOperatorCompatibilityResult``.

Evidence profile: routine

Bounded artifact scope: immutable correlated outcomes for represented scalar operator
compatibility.

Facet and represented meaning

The ResultObject retains exact operands and requires issue codes to describe their
metadata agreement completely.

Intrinsic and cross-object scope

A contradictory manually authored passing outcome is rejected.

VVUQ and scientific exclusions

This verifies result consistency, not matrix addition, physical alignment, scientific
validation, UQ, or human acceptance.
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
    ScalarFiniteLatticeOperatorCompatibilityResult,
    TwistFiber,
    TwistGaugeRepresentation,
)

pytestmark = pytest.mark.software_verification
SUT = ScalarFiniteLatticeOperatorCompatibilityResult


class TestScalarFiniteLatticeOperatorCompatibilityResult:
    """Own software evidence for the operator compatibility result."""

    def test_constructor__issue_codes__must_exactly_describe_operands(self) -> None:
        """Evidence ID: SV-SOLID-STATE-OPERATOR-COMPATIBILITY-002

        Requirement: A result cannot claim compatibility for mismatched operands.

        Acceptance: Removing the basis issue from an analyzed mismatch raises
        ``ValueError`` during immutable dataclass replacement.
        """
        shape = FiniteLatticeShape(LatticeDimension.ONE, (1,))
        fiber = TwistFiber(
            BoundaryTwistReducer().execute(
                BoundaryTwistLift(LatticeDimension.ONE, (0.0,))
            ),
            TwistGaugeRepresentation.CENTERED_UNIFORM_LINK,
        )
        matrix = ComplexSparseMatrixQuantity.from_csr(
            sparse.csr_array(np.array([[1.0 + 0.0j]])), Unitless()
        )
        left = ScalarFiniteLatticeOperator(
            "left", matrix, shape, fiber, "basis", "zero", ()
        )
        right = replace(left, identifier="right", basis_identifier="other_basis")
        result = ScalarFiniteLatticeOperatorCompatibilityAnalyzer().execute(left, right)

        assert not result.compatible
        with pytest.raises(ValueError, match="exactly describe"):
            replace(result, issue_codes=())
