"""Explicit finite-extent analysis for represented periodic-2D defects."""

from dataclasses import dataclass

from ksdft2effmass.analysis.finite_domain_locality import (
    MinimumImageChebyshevPartition,
    MinimumImageChebyshevPartitioner,
    SparseLocalityResidualAnalyzer,
    SparseLocalityResidualResult,
)
from ksdft2effmass.operators import MODEL_SYSTEM_UNIT_CONVERTER, ScalarQuantity
from ksdft2effmass.solid_state import (
    LatticeCoordinate,
    LatticeDimension,
    ScalarFiniteLatticeOperator,
    ScalarFiniteLatticeOperatorCompatibilityAnalyzer,
    ScalarFiniteLatticeOperatorCompatibilityResult,
)


@dataclass(frozen=True, slots=True)
class Periodic2DDefectLocalityRequest:
    """Request a minimum-image locality assessment of a represented defect.

    Parameters
    ----------
    bulk_operator
        Periodic parent in the common represented conventions.
    defect_operator
        Modified operator in those same conventions.
    origin
        Canonical finite-lattice coordinate defining the defect center.
    core_radius
        Nonnegative Chebyshev radius in integer lattice-cell units.
    exterior_frobenius_tolerance
        Maximum accepted perturbation norm entirely outside the declared core.
    core_exterior_frobenius_tolerance
        Maximum accepted perturbation norm coupling core and exterior sites.
    """

    bulk_operator: ScalarFiniteLatticeOperator
    defect_operator: ScalarFiniteLatticeOperator
    origin: LatticeCoordinate
    core_radius: int
    exterior_frobenius_tolerance: ScalarQuantity
    core_exterior_frobenius_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Require exact two-dimensional operands and explicit nonnegative controls."""
        if type(self.bulk_operator) is not ScalarFiniteLatticeOperator:
            raise TypeError("bulk_operator must be ScalarFiniteLatticeOperator")
        if type(self.defect_operator) is not ScalarFiniteLatticeOperator:
            raise TypeError("defect_operator must be ScalarFiniteLatticeOperator")
        if self.bulk_operator.dimension is not LatticeDimension.TWO:
            raise ValueError("bulk_operator must be two-dimensional")
        if self.defect_operator.dimension is not LatticeDimension.TWO:
            raise ValueError("defect_operator must be two-dimensional")
        if type(self.origin) is not LatticeCoordinate:
            raise TypeError("origin must be LatticeCoordinate")
        if self.origin.dimension is not LatticeDimension.TWO:
            raise ValueError("origin must be two-dimensional")
        if type(self.core_radius) is not int:
            raise TypeError("core_radius must be a built-in int")
        if self.core_radius < 0:
            raise ValueError("core_radius must be nonnegative")
        for name, tolerance in (
            ("exterior_frobenius_tolerance", self.exterior_frobenius_tolerance),
            (
                "core_exterior_frobenius_tolerance",
                self.core_exterior_frobenius_tolerance,
            ),
        ):
            if type(tolerance) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if tolerance.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic2DDefectLocalityResult:
    """Retain the locality partition, residual metrics, controls, and disposition."""

    compatibility: ScalarFiniteLatticeOperatorCompatibilityResult
    partition: MinimumImageChebyshevPartition
    residual: SparseLocalityResidualResult
    exterior_frobenius_tolerance: ScalarQuantity
    core_exterior_frobenius_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact correlated findings and tolerance units."""
        if (
            type(self.compatibility)
            is not ScalarFiniteLatticeOperatorCompatibilityResult
        ):
            raise TypeError("compatibility uses the wrong ResultObject type")
        if not self.compatibility.compatible:
            raise ValueError("locality analysis requires compatible operators")
        if type(self.partition) is not MinimumImageChebyshevPartition:
            raise TypeError("partition must be MinimumImageChebyshevPartition")
        if type(self.residual) is not SparseLocalityResidualResult:
            raise TypeError("residual must be SparseLocalityResidualResult")
        if self.residual.reference is not self.compatibility.left:
            raise ValueError("residual must retain the compatible bulk operator")
        if self.residual.candidate is not self.compatibility.right:
            raise ValueError("residual must retain the compatible defect operator")
        if self.residual.partition is not self.partition:
            raise ValueError("residual must retain the exact locality partition")
        for name, tolerance in (
            ("exterior_frobenius_tolerance", self.exterior_frobenius_tolerance),
            (
                "core_exterior_frobenius_tolerance",
                self.core_exterior_frobenius_tolerance,
            ),
        ):
            if type(tolerance) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if tolerance.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
            if tolerance.unit != self.residual.unit:
                raise ValueError(f"{name} must use the represented energy unit")

    @property
    def passes(self) -> bool:
        """Return whether the represented perturbation is confined to the core."""
        return (
            self.residual.exterior_frobenius_residual
            <= self.exterior_frobenius_tolerance.magnitude
            and self.residual.core_exterior_frobenius_residual
            <= self.core_exterior_frobenius_tolerance.magnitude
        )


class Periodic2DDefectLocalityAnalyzer:
    """Assess finite represented extent using explicit minimum-image controls."""

    __slots__ = ()

    compatibility_analyzer = ScalarFiniteLatticeOperatorCompatibilityAnalyzer()
    partitioner = MinimumImageChebyshevPartitioner()
    residual_analyzer = SparseLocalityResidualAnalyzer()

    def execute(
        self, request: Periodic2DDefectLocalityRequest
    ) -> Periodic2DDefectLocalityResult:
        """Return partition-resolved perturbation norms and bounded disposition.

        Parameters
        ----------
        request
            Compatible represented operands, defect origin, core radius, and explicit
            energy-unit tolerances.

        Returns
        -------
        Periodic2DDefectLocalityResult
            Minimum-image partition, sparse residual metrics, and finite-extent
            disposition.

        Raises
        ------
        TypeError
            If ``request`` has the wrong exact semantic type.
        ValueError
            If represented metadata, geometry, origin, or tolerance units are
            incompatible.
        """
        if type(request) is not Periodic2DDefectLocalityRequest:
            raise TypeError("request must be Periodic2DDefectLocalityRequest")
        compatibility = self.compatibility_analyzer.execute(
            request.bulk_operator, request.defect_operator
        )
        if not compatibility.compatible:
            issue_values = ", ".join(code.value for code in compatibility.issue_codes)
            raise ValueError(
                "bulk and defect operators are incompatible for locality analysis: "
                f"{issue_values}"
            )
        partition = self.partitioner.execute(
            request.bulk_operator.shape,
            request.origin,
            core_radius=request.core_radius,
        )
        residual = self.residual_analyzer.execute(
            request.bulk_operator,
            request.defect_operator,
            compatibility,
            partition,
        )
        exterior_tolerance = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            request.exterior_frobenius_tolerance, residual.unit
        )
        coupling_tolerance = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            request.core_exterior_frobenius_tolerance, residual.unit
        )
        return Periodic2DDefectLocalityResult(
            compatibility,
            partition,
            residual,
            exterior_tolerance,
            coupling_tolerance,
        )
