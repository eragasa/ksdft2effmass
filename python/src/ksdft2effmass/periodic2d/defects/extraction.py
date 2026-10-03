r"""Compatibility-gated extraction of a represented periodic-2D perturbation.

The extraction implements :math:`\Delta H=H_\mathrm{def}-H_0` only after the two
finite operators agree in geometry, boundary twist, basis, unit, and energy reference.
It performs no alignment and does not infer that compatibility from matrix values.
"""

from dataclasses import dataclass

from ksdft2effmass.operators import ComplexSparseMatrixQuantity
from ksdft2effmass.solid_state import (
    LatticeDimension,
    ScalarFiniteLatticeOperator,
    ScalarFiniteLatticeOperatorCompatibilityAnalyzer,
    ScalarFiniteLatticeOperatorCompatibilityResult,
)


@dataclass(frozen=True, slots=True)
class Periodic2DDefectExtractionRequest:
    """Request subtraction of an aligned defect and periodic bulk representation."""

    bulk_operator: ScalarFiniteLatticeOperator
    defect_operator: ScalarFiniteLatticeOperator

    def __post_init__(self) -> None:
        """Require exact two-dimensional represented operators."""
        if type(self.bulk_operator) is not ScalarFiniteLatticeOperator:
            raise TypeError("bulk_operator must be ScalarFiniteLatticeOperator")
        if type(self.defect_operator) is not ScalarFiniteLatticeOperator:
            raise TypeError("defect_operator must be ScalarFiniteLatticeOperator")
        if self.bulk_operator.dimension is not LatticeDimension.TWO:
            raise ValueError("bulk_operator must be two-dimensional")
        if self.defect_operator.dimension is not LatticeDimension.TWO:
            raise ValueError("defect_operator must be two-dimensional")


@dataclass(frozen=True, slots=True)
class Periodic2DDefectExtractionResult:
    """Retain aligned operands, compatibility evidence, and extracted change."""

    bulk_operator: ScalarFiniteLatticeOperator
    defect_operator: ScalarFiniteLatticeOperator
    compatibility: ScalarFiniteLatticeOperatorCompatibilityResult
    perturbation_operator: ScalarFiniteLatticeOperator

    def __post_init__(self) -> None:
        """Require exact correlated operands and a compatible extracted operator."""
        if type(self.bulk_operator) is not ScalarFiniteLatticeOperator:
            raise TypeError("bulk_operator must be ScalarFiniteLatticeOperator")
        if type(self.defect_operator) is not ScalarFiniteLatticeOperator:
            raise TypeError("defect_operator must be ScalarFiniteLatticeOperator")
        if (
            type(self.compatibility)
            is not ScalarFiniteLatticeOperatorCompatibilityResult
        ):
            raise TypeError("compatibility uses the wrong AbstractResultObject type")
        if type(self.perturbation_operator) is not ScalarFiniteLatticeOperator:
            raise TypeError("perturbation_operator must be ScalarFiniteLatticeOperator")
        if self.compatibility.left is not self.bulk_operator:
            raise ValueError("compatibility must retain the exact bulk operator")
        if self.compatibility.right is not self.defect_operator:
            raise ValueError("compatibility must retain the exact defect operator")
        if not self.compatibility.compatible:
            raise ValueError("bulk and defect operators must be compatible")
        if self.perturbation_operator.shape != self.bulk_operator.shape:
            raise ValueError("perturbation and bulk shapes must agree")
        if self.perturbation_operator.twist_fiber != self.bulk_operator.twist_fiber:
            raise ValueError("perturbation and bulk twist fibers must agree")
        if (
            self.perturbation_operator.basis_identifier
            != self.bulk_operator.basis_identifier
        ):
            raise ValueError("perturbation and bulk bases must agree")
        if (
            self.perturbation_operator.energy_reference
            != self.bulk_operator.energy_reference
        ):
            raise ValueError("perturbation and bulk energy references must agree")
        if self.perturbation_operator.matrix.unit != self.bulk_operator.matrix.unit:
            raise ValueError("perturbation and bulk energy units must agree")


class Periodic2DDefectPerturbationExtractor:
    """Extract a sparse represented perturbation from aligned finite operators."""

    __slots__ = ()

    compatibility_analyzer = ScalarFiniteLatticeOperatorCompatibilityAnalyzer()

    def execute(
        self, request: Periodic2DDefectExtractionRequest
    ) -> Periodic2DDefectExtractionResult:
        r"""Return :math:`H_\mathrm{def}-H_0` after compatibility succeeds.

        Parameters
        ----------
        request
            Explicit bulk and defect representations already expressed in the intended
            common geometry, twist, basis, unit, and energy-reference conventions.

        Returns
        -------
        Periodic2DDefectExtractionResult
            Exact operands, compatibility evidence, and sparse represented difference.

        Raises
        ------
        TypeError
            If ``request`` has the wrong exact semantic type.
        ValueError
            If represented metadata do not permit direct subtraction.
        """
        if type(request) is not Periodic2DDefectExtractionRequest:
            raise TypeError("request must be Periodic2DDefectExtractionRequest")
        compatibility = self.compatibility_analyzer.execute(
            request.bulk_operator, request.defect_operator
        )
        if not compatibility.compatible:
            issue_values = ", ".join(code.value for code in compatibility.issue_codes)
            raise ValueError(
                "bulk and defect operators are incompatible for subtraction: "
                f"{issue_values}"
            )
        matrix = ComplexSparseMatrixQuantity.from_csr(
            request.defect_operator.matrix.to_csr()
            - request.bulk_operator.matrix.to_csr(),
            request.bulk_operator.matrix.unit,
        )
        perturbation = ScalarFiniteLatticeOperator(
            f"{request.defect_operator.identifier}.minus.{request.bulk_operator.identifier}",
            matrix,
            request.bulk_operator.shape,
            request.bulk_operator.twist_fiber,
            request.bulk_operator.basis_identifier,
            request.bulk_operator.energy_reference,
            (
                ("bulk_operator", request.bulk_operator.identifier),
                ("defect_operator", request.defect_operator.identifier),
                ("extractor", type(self).__name__),
            ),
        )
        return Periodic2DDefectExtractionResult(
            request.bulk_operator,
            request.defect_operator,
            compatibility,
            perturbation,
        )
