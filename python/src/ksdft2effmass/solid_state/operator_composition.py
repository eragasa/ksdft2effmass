"""Compatibility-checked sparse composition of scalar finite-lattice operators."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ksdft2effmass.operators import ComplexSparseMatrixQuantity

from .represented_operators import ScalarFiniteLatticeOperator


class ScalarFiniteLatticeOperatorCompatibilityIssueCode(StrEnum):
    """Comparison-critical metadata mismatches that prohibit operator addition."""

    SHAPE = "shape"
    TWIST_FIBER = "twist_fiber"
    BASIS = "basis"
    UNIT = "unit"
    ENERGY_REFERENCE = "energy_reference"


@dataclass(frozen=True, slots=True)
class ScalarFiniteLatticeOperatorCompatibilityResult:
    """Retain the exact operands and structured compatibility outcome."""

    left: ScalarFiniteLatticeOperator
    right: ScalarFiniteLatticeOperator
    issue_codes: tuple[ScalarFiniteLatticeOperatorCompatibilityIssueCode, ...]

    def __post_init__(self) -> None:
        """Validate exact operands and canonical issue ordering."""
        if type(self.left) is not ScalarFiniteLatticeOperator:
            raise TypeError("left must be ScalarFiniteLatticeOperator")
        if type(self.right) is not ScalarFiniteLatticeOperator:
            raise TypeError("right must be ScalarFiniteLatticeOperator")
        if type(self.issue_codes) is not tuple or any(
            type(code) is not ScalarFiniteLatticeOperatorCompatibilityIssueCode
            for code in self.issue_codes
        ):
            raise TypeError(
                "issue_codes must contain "
                "ScalarFiniteLatticeOperatorCompatibilityIssueCode"
            )
        ordered = tuple(sorted(set(self.issue_codes), key=lambda code: code.value))
        if self.issue_codes != ordered:
            raise ValueError("issue_codes must be sorted and unique")
        expected: set[ScalarFiniteLatticeOperatorCompatibilityIssueCode] = set()
        if self.left.shape != self.right.shape:
            expected.add(ScalarFiniteLatticeOperatorCompatibilityIssueCode.SHAPE)
        if self.left.twist_fiber != self.right.twist_fiber:
            expected.add(ScalarFiniteLatticeOperatorCompatibilityIssueCode.TWIST_FIBER)
        if self.left.basis_identifier != self.right.basis_identifier:
            expected.add(ScalarFiniteLatticeOperatorCompatibilityIssueCode.BASIS)
        if self.left.matrix.unit != self.right.matrix.unit:
            expected.add(ScalarFiniteLatticeOperatorCompatibilityIssueCode.UNIT)
        if self.left.energy_reference != self.right.energy_reference:
            expected.add(
                ScalarFiniteLatticeOperatorCompatibilityIssueCode.ENERGY_REFERENCE
            )
        expected_ordered = tuple(sorted(expected, key=lambda code: code.value))
        if self.issue_codes != expected_ordered:
            raise ValueError("issue_codes must exactly describe operand compatibility")

    @property
    def compatible(self) -> bool:
        """Return whether direct represented matrix addition is defined."""
        return not self.issue_codes


class ScalarFiniteLatticeOperatorCompatibilityAnalyzer:
    """Check metadata required before adding represented scalar operators."""

    __slots__ = ()

    def execute(
        self,
        left: ScalarFiniteLatticeOperator,
        right: ScalarFiniteLatticeOperator,
    ) -> ScalarFiniteLatticeOperatorCompatibilityResult:
        """Return exact operands and all represented compatibility issues."""
        if type(left) is not ScalarFiniteLatticeOperator:
            raise TypeError("left must be ScalarFiniteLatticeOperator")
        if type(right) is not ScalarFiniteLatticeOperator:
            raise TypeError("right must be ScalarFiniteLatticeOperator")
        issues: set[ScalarFiniteLatticeOperatorCompatibilityIssueCode] = set()
        if left.shape != right.shape:
            issues.add(ScalarFiniteLatticeOperatorCompatibilityIssueCode.SHAPE)
        if left.twist_fiber != right.twist_fiber:
            issues.add(ScalarFiniteLatticeOperatorCompatibilityIssueCode.TWIST_FIBER)
        if left.basis_identifier != right.basis_identifier:
            issues.add(ScalarFiniteLatticeOperatorCompatibilityIssueCode.BASIS)
        if left.matrix.unit != right.matrix.unit:
            issues.add(ScalarFiniteLatticeOperatorCompatibilityIssueCode.UNIT)
        if left.energy_reference != right.energy_reference:
            issues.add(
                ScalarFiniteLatticeOperatorCompatibilityIssueCode.ENERGY_REFERENCE
            )
        return ScalarFiniteLatticeOperatorCompatibilityResult(
            left,
            right,
            tuple(sorted(issues, key=lambda code: code.value)),
        )


class ScalarFiniteLatticeOperatorAdder:
    """Add compatible scalar represented operators without implicit densification."""

    __slots__ = ()

    def execute(
        self,
        identifier: str,
        left: ScalarFiniteLatticeOperator,
        right: ScalarFiniteLatticeOperator,
        compatibility: ScalarFiniteLatticeOperatorCompatibilityResult,
    ) -> ScalarFiniteLatticeOperator:
        """Return the canonical sparse sum after correlated compatibility evidence."""
        if type(identifier) is not str:
            raise TypeError("identifier must be a string")
        if not identifier:
            raise ValueError("identifier must be nonempty")
        if type(left) is not ScalarFiniteLatticeOperator:
            raise TypeError("left must be ScalarFiniteLatticeOperator")
        if type(right) is not ScalarFiniteLatticeOperator:
            raise TypeError("right must be ScalarFiniteLatticeOperator")
        if type(compatibility) is not ScalarFiniteLatticeOperatorCompatibilityResult:
            raise TypeError(
                "compatibility must be ScalarFiniteLatticeOperatorCompatibilityResult"
            )
        if compatibility.left is not left or compatibility.right is not right:
            raise ValueError("compatibility result must correlate the exact operands")
        if not compatibility.compatible:
            raise ValueError("compatibility result must pass before operator addition")
        matrix = ComplexSparseMatrixQuantity.from_csr(
            left.matrix.to_csr() + right.matrix.to_csr(), left.matrix.unit
        )
        return ScalarFiniteLatticeOperator(
            identifier,
            matrix,
            left.shape,
            left.twist_fiber,
            left.basis_identifier,
            left.energy_reference,
            (
                ("composer", type(self).__name__),
                ("left_operator", left.identifier),
                ("right_operator", right.identifier),
            ),
        )
