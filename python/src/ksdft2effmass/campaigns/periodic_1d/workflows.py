"""Versioned reusable orchestration for periodic-1D hopping reduction."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.analysis.hopping_diagnostics import (
    HoppingParsevalAnalyzer1D,
    HoppingParsevalResult1D,
)
from ksdft2effmass.analysis.hopping_fits import (
    BlockHoppingLeastSquaresFitResult1D,
    BlockHoppingLeastSquaresFitter1D,
    BlockHoppingModelComparator1D,
    BlockHoppingModelComparisonResult1D,
)
from ksdft2effmass.operators import ScalarQuantity, VectorQuantity
from ksdft2effmass.solid_state import (
    BlockHoppingTruncationResult1D,
    BlockHoppingTruncator1D,
    CenteredUniformReciprocalMesh1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorFourierTransformResult1D,
    ReciprocalOperatorSamples1D,
)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DHoppingReductionRequest:
    """Declare transform, truncation, fit, and comparison inputs without execution."""

    source: ReciprocalOperatorSamples1D
    mesh: CenteredUniformReciprocalMesh1D
    truncation_range: int
    fit_representatives: tuple[int, ...]
    fit_weights: VectorQuantity
    withheld_coordinates: VectorQuantity
    coordinate_absolute_tolerance: float
    reconstruction_absolute_tolerance: float
    parseval_absolute_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate closed request types and nonnegative scalar controls."""
        if type(self.source) is not ReciprocalOperatorSamples1D:
            raise TypeError("source must be ReciprocalOperatorSamples1D")
        if type(self.mesh) is not CenteredUniformReciprocalMesh1D:
            raise TypeError("mesh must be CenteredUniformReciprocalMesh1D")
        if type(self.truncation_range) is not int:
            raise TypeError("truncation_range must be a built-in int")
        if self.truncation_range < 0:
            raise ValueError("truncation_range must be nonnegative")
        if (
            not isinstance(self.fit_representatives, tuple)
            or not self.fit_representatives
        ):
            raise TypeError("fit_representatives must be a nonempty tuple")
        if type(self.fit_weights) is not VectorQuantity:
            raise TypeError("fit_weights must be VectorQuantity")
        if type(self.withheld_coordinates) is not VectorQuantity:
            raise TypeError("withheld_coordinates must be VectorQuantity")
        for name, value in (
            ("coordinate_absolute_tolerance", self.coordinate_absolute_tolerance),
            (
                "reconstruction_absolute_tolerance",
                self.reconstruction_absolute_tolerance,
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.parseval_absolute_tolerance) is not ScalarQuantity:
            raise TypeError("parseval_absolute_tolerance must be ScalarQuantity")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DHoppingReductionResult:
    """Retain distinct complete, truncated, fitted, and comparison outcomes."""

    transform: ReciprocalOperatorFourierTransformResult1D
    truncation: BlockHoppingTruncationResult1D
    parseval: HoppingParsevalResult1D
    fit: BlockHoppingLeastSquaresFitResult1D
    complete_vs_fit: BlockHoppingModelComparisonResult1D

    def __post_init__(self) -> None:
        """Validate exact result types without pooling their diagnostics."""
        expected = (
            (self.transform, ReciprocalOperatorFourierTransformResult1D),
            (self.truncation, BlockHoppingTruncationResult1D),
            (self.parseval, HoppingParsevalResult1D),
            (self.fit, BlockHoppingLeastSquaresFitResult1D),
            (self.complete_vs_fit, BlockHoppingModelComparisonResult1D),
        )
        if any(type(value) is not kind for value, kind in expected):
            raise TypeError(
                "every reduction outcome must use its exact AbstractResultObject"
            )


class Periodic1DHoppingReductionWorkflow:
    """Compose public periodic-1D Actions without filesystem or external execution."""

    __slots__ = ()

    def execute(
        self, request: Periodic1DHoppingReductionRequest
    ) -> Periodic1DHoppingReductionResult:
        """Run complete transform, truncation, fit, Parseval, and route comparisons."""
        if type(request) is not Periodic1DHoppingReductionRequest:
            raise TypeError("request must be Periodic1DHoppingReductionRequest")
        transform = ReciprocalOperatorFourierTransformer1D().execute(
            request.source,
            request.mesh,
            request.coordinate_absolute_tolerance,
            request.reconstruction_absolute_tolerance,
        )
        truncation = BlockHoppingTruncator1D().execute(
            transform.hopping_model, request.truncation_range
        )
        parseval = HoppingParsevalAnalyzer1D().execute(
            transform, truncation, request.parseval_absolute_tolerance
        )
        if request.fit_representatives != transform.hopping_model.representatives:
            raise ValueError(
                "fit_representatives must equal the complete mesh representatives"
            )
        fit = BlockHoppingLeastSquaresFitter1D().execute(
            request.source, request.fit_representatives, request.fit_weights
        )
        comparator = BlockHoppingModelComparator1D()
        return Periodic1DHoppingReductionResult(
            transform,
            truncation,
            parseval,
            fit,
            comparator.execute(
                transform.hopping_model,
                fit.fitted_model,
                request.withheld_coordinates,
            ),
        )
