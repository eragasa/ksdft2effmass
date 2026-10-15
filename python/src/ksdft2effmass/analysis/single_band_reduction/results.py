"""Correlated results for reusable one-dimensional single-band reduction."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.analysis.hopping_diagnostics import (
    BlockHoppingHermiticityResult1D,
    HoppingParsevalResult1D,
    ScalarHoppingBandShapeResult1D,
)
from ksdft2effmass.analysis.hopping_fits import (
    BlockHoppingLeastSquaresFitResult1D,
    BlockHoppingModelComparisonResult1D,
)
from ksdft2effmass.analysis.periodic_bands import BandApproximationErrorResult1D
from ksdft2effmass.solid_state import (
    BlockHoppingTruncationResult1D,
    ReciprocalOperatorFourierTransformResult1D,
    ReciprocalOperatorSamples1D,
)

from .definition import SingleBandHoppingReductionRequest1D


@dataclass(frozen=True, slots=True, eq=False)
class SingleBandHoppingRangeReductionResult1D:
    """Retain both reduction routes and diagnostics for one hopping range."""

    truncation: BlockHoppingTruncationResult1D
    training_error: BandApproximationErrorResult1D
    evaluation_error: BandApproximationErrorResult1D
    parseval: HoppingParsevalResult1D
    direct_fit: BlockHoppingLeastSquaresFitResult1D
    route_comparison: BlockHoppingModelComparisonResult1D
    band_shape: ScalarHoppingBandShapeResult1D

    def __post_init__(self) -> None:
        """Require exact types and one consistently correlated mediated model."""
        if type(self.truncation) is not BlockHoppingTruncationResult1D:
            raise TypeError("truncation must be BlockHoppingTruncationResult1D")
        if type(self.training_error) is not BandApproximationErrorResult1D:
            raise TypeError("training_error must be BandApproximationErrorResult1D")
        if type(self.evaluation_error) is not BandApproximationErrorResult1D:
            raise TypeError("evaluation_error must be BandApproximationErrorResult1D")
        if type(self.parseval) is not HoppingParsevalResult1D:
            raise TypeError("parseval must be HoppingParsevalResult1D")
        if type(self.direct_fit) is not BlockHoppingLeastSquaresFitResult1D:
            raise TypeError("direct_fit must be BlockHoppingLeastSquaresFitResult1D")
        if type(self.route_comparison) is not BlockHoppingModelComparisonResult1D:
            raise TypeError(
                "route_comparison must be BlockHoppingModelComparisonResult1D"
            )
        if type(self.band_shape) is not ScalarHoppingBandShapeResult1D:
            raise TypeError("band_shape must be ScalarHoppingBandShapeResult1D")
        mediated = self.truncation.truncated
        if self.training_error.candidate.matrix_dimension != 1:
            raise ValueError("training candidate must represent one scalar band")
        if self.evaluation_error.candidate.matrix_dimension != 1:
            raise ValueError("evaluation candidate must represent one scalar band")
        if self.parseval.truncation is not self.truncation:
            raise ValueError("parseval must use the same truncation")
        if self.direct_fit.representatives != mediated.representatives:
            raise ValueError("direct fit must use the mediated representatives")
        if self.route_comparison.reference is not mediated:
            raise ValueError(
                "route comparison must use the mediated model as reference"
            )
        if self.route_comparison.candidate is not self.direct_fit.fitted_model:
            raise ValueError("route comparison must use the direct-fit model")
        if self.band_shape.model is not mediated:
            raise ValueError("band-shape diagnostics must use the mediated model")

    @property
    def maximum_range(self) -> int:
        """Return the symmetric cell range of the mediated model."""
        return self.truncation.maximum_range


@dataclass(frozen=True, slots=True, eq=False)
class SingleBandHoppingReductionResult1D:
    """Retain a complete transform and ordered finite-range reduction results."""

    request: SingleBandHoppingReductionRequest1D
    training_source: ReciprocalOperatorSamples1D
    complete_transform: ReciprocalOperatorFourierTransformResult1D
    hopping_hermiticity: BlockHoppingHermiticityResult1D
    range_study: tuple[SingleBandHoppingRangeReductionResult1D, ...]

    def __post_init__(self) -> None:
        """Validate all request, transform, and range-result correlations."""
        if type(self.request) is not SingleBandHoppingReductionRequest1D:
            raise TypeError("request must be SingleBandHoppingReductionRequest1D")
        if type(self.training_source) is not ReciprocalOperatorSamples1D:
            raise TypeError("training_source must be ReciprocalOperatorSamples1D")
        if self.training_source.matrix_dimension != 1:
            raise ValueError("training_source must represent one scalar band")
        if (
            type(self.complete_transform)
            is not ReciprocalOperatorFourierTransformResult1D
        ):
            raise TypeError(
                "complete_transform must be ReciprocalOperatorFourierTransformResult1D"
            )
        if type(self.hopping_hermiticity) is not BlockHoppingHermiticityResult1D:
            raise TypeError(
                "hopping_hermiticity must be BlockHoppingHermiticityResult1D"
            )
        if not isinstance(self.range_study, tuple) or not self.range_study:
            raise TypeError("range_study must be a nonempty tuple")
        if any(
            type(item) is not SingleBandHoppingRangeReductionResult1D
            for item in self.range_study
        ):
            raise TypeError("range_study must contain typed range results")
        if tuple(item.maximum_range for item in self.range_study) != (
            self.request.hopping_ranges
        ):
            raise ValueError("range_study must match the requested range inventory")
        if self.complete_transform.source is not self.training_source:
            raise ValueError("complete_transform must use training_source")
        if self.complete_transform.mesh is not self.request.transform_mesh:
            raise ValueError("complete_transform must use the requested transform mesh")
        if self.hopping_hermiticity.model is not (
            self.complete_transform.hopping_model
        ):
            raise ValueError("Hermiticity must analyze the complete hopping model")

        target = self.request.training_target
        if not np.array_equal(
            self.training_source.coordinates.magnitude,
            target.coordinates.magnitude,
        ):
            raise ValueError("training_source coordinates must match training_target")
        values = np.asarray(
            [matrix.magnitude[0, 0] for matrix in self.training_source.matrices],
            dtype=np.complex128,
        )
        if np.any(values.imag != 0.0) or not np.array_equal(
            values.real, target.eigenvalues.magnitude[:, 0]
        ):
            raise ValueError("training_source must embed the real training band")

        for item in self.range_study:
            if item.truncation.source is not self.complete_transform.hopping_model:
                raise ValueError("every truncation must use the complete hopping model")
            if item.parseval.transform is not self.complete_transform:
                raise ValueError(
                    "every Parseval result must use the complete transform"
                )
            if item.direct_fit.source is not self.training_source:
                raise ValueError("every direct fit must use training_source")
            if item.direct_fit.weights is not self.request.fitting_weights:
                raise ValueError("every direct fit must use the requested weights")
            if item.training_error.target is not self.request.training_target:
                raise ValueError("training errors must use training_target")
            if item.evaluation_error.target is not self.request.evaluation_target:
                raise ValueError("evaluation errors must use evaluation_target")
            if item.route_comparison.comparison_coordinates is not (
                self.request.training_target.coordinates
            ):
                raise ValueError("route comparison must use training coordinates")
            if item.band_shape.comparison_coordinates is not (
                self.request.evaluation_target.coordinates
            ):
                raise ValueError("band shape must use evaluation coordinates")


__all__ = [
    "SingleBandHoppingRangeReductionResult1D",
    "SingleBandHoppingReductionResult1D",
]
