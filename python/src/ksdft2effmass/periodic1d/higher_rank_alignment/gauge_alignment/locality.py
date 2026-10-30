"""Symmetric-support locality analysis for one gauge-aligned Fourier series."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

import numpy as np
from projectkoios.physkit.solidstate.tb import (
    FinitePeriodicMatrixFourierTensorEvaluator,
)

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    MatrixErrorDecompositionAnalyzer,
    MatrixFieldComparisonAnalyzer,
    SymmetricRangeTailAnalyzer1D,
    SymmetricRangeTailMonotonicityAnalyzer1D,
)

from ..diagnostics import Periodic1DHigherRankMatrixComparisonResult
from .fourier import Periodic1DHigherRankFourierAnalysis
from .interpolation import Periodic1DHigherRankInterpolationAnalysis
from .request import Periodic1DHigherRankGaugeAlignmentAnalysisRequest
from .results import Periodic1DHigherRankSupportResult


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DHigherRankLocalityAnalysisRequest:
    """Bind Fourier and interpolation evidence for support analysis."""

    analysis_request: Periodic1DHigherRankGaugeAlignmentAnalysisRequest
    fourier_analysis: Periodic1DHigherRankFourierAnalysis
    interpolation_analysis: Periodic1DHigherRankInterpolationAnalysis

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DHigherRankGaugeAlignmentAnalysisRequest
        ):
            raise TypeError(
                "analysis_request must be the exact gauge-alignment request"
            )
        if type(self.fourier_analysis) is not Periodic1DHigherRankFourierAnalysis:
            raise TypeError("fourier_analysis must be the exact Fourier analysis")
        if (
            type(self.interpolation_analysis)
            is not Periodic1DHigherRankInterpolationAnalysis
        ):
            raise TypeError(
                "interpolation_analysis must be the exact interpolation analysis"
            )
        if self.fourier_analysis.analysis_request is not self.analysis_request:
            raise ValueError("Fourier analysis must derive from the bound request")
        if self.interpolation_analysis.analysis_request is not self.analysis_request:
            raise ValueError(
                "interpolation analysis must derive from the bound request"
            )
        expected_size = (
            self.analysis_request.calculation_request.configuration.evaluation_mesh_size
        )
        if self.interpolation_analysis.evaluation_coordinates.size != expected_size:
            raise ValueError("interpolation analysis must match the evaluation mesh")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DHigherRankLocalityAnalysis:
    """Store support diagnostics and tail-monotonicity evidence."""

    analysis_request: Periodic1DHigherRankGaugeAlignmentAnalysisRequest
    supports: tuple[Periodic1DHigherRankSupportResult, ...]
    maximum_tail_increase: float
    all_tail_monotonicity_checks_pass: bool

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DHigherRankGaugeAlignmentAnalysisRequest
        ):
            raise TypeError("analysis_request must be the exact analysis request")
        if type(self.supports) is not tuple or any(
            type(item) is not Periodic1DHigherRankSupportResult
            for item in self.supports
        ):
            raise TypeError("supports must contain exact support-result records")
        if type(self.maximum_tail_increase) is not float:
            raise TypeError("maximum_tail_increase must be a built-in float")
        if type(self.all_tail_monotonicity_checks_pass) is not bool:
            raise TypeError("all_tail_monotonicity_checks_pass must be a built-in bool")


@final
class Periodic1DHigherRankLocalityAnalyzer:
    """Analyze support truncation, tails, and error decomposition."""

    __slots__ = ("_request", "_fourier_evaluator")

    def __init__(
        self,
        *,
        request: Periodic1DHigherRankLocalityAnalysisRequest,
        fourier_evaluator: FinitePeriodicMatrixFourierTensorEvaluator,
    ) -> None:
        if type(request) is not Periodic1DHigherRankLocalityAnalysisRequest:
            raise TypeError(
                "request must be Periodic1DHigherRankLocalityAnalysisRequest"
            )
        if type(fourier_evaluator) is not FinitePeriodicMatrixFourierTensorEvaluator:
            raise TypeError(
                "fourier_evaluator must be the PhysKit finite-periodic evaluator"
            )
        self._request = request
        self._fourier_evaluator = fourier_evaluator

    @property
    def request(self) -> Periodic1DHigherRankLocalityAnalysisRequest:
        """Return the exact locality request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DHigherRankLocalityAnalysis:
        """Return support, tail, and error-decomposition diagnostics."""
        request = self._request
        analysis_request = request.analysis_request
        calculation_request = analysis_request.calculation_request
        controls = calculation_request.controls
        model = analysis_request.model
        coordinates = analysis_request.aligned_fields.coordinates
        transform = request.fourier_analysis.transform
        interpolation = request.interpolation_analysis
        evaluation_coordinates = interpolation.evaluation_coordinates
        full_evaluation = interpolation.full_evaluation
        direct_evaluation = interpolation.direct_evaluation
        tail_analyzer = SymmetricRangeTailAnalyzer1D()
        tails = tuple(
            tail_analyzer.execute(
                transform.series,
                support,
                controls.energy_reference,
            )
            for support in controls.support_radii
        )
        support_results: list[Periodic1DHigherRankSupportResult] = []
        modes = transform.series.integer_modes[:, 0]
        for tail in tails:
            retained_mask = np.abs(modes) <= tail.maximum_range
            indices = tuple(int(index) for index in np.flatnonzero(retained_mask))
            omitted_indices = tuple(
                int(index) for index in np.flatnonzero(np.logical_not(retained_mask))
            )
            truncated_series = transform.series.take(indices)
            omitted_series = transform.series.take(omitted_indices)
            truncated_evaluation = self._fourier_evaluator.evaluate(
                truncated_series,
                (evaluation_coordinates,),
                controls.maximum_working_elements,
            ).matrix_values
            omitted_construction = self._fourier_evaluator.evaluate(
                omitted_series,
                (coordinates,),
                controls.maximum_working_elements,
            ).matrix_values
            truncation_diagnostics = MatrixFieldComparisonAnalyzer().execute(
                truncated_evaluation,
                full_evaluation,
                controls.energy_reference,
                controls.saturation_denominator_floor,
            )
            total_diagnostics = MatrixFieldComparisonAnalyzer().execute(
                truncated_evaluation,
                direct_evaluation,
                controls.energy_reference,
                controls.saturation_denominator_floor,
            )
            decomposition = MatrixErrorDecompositionAnalyzer().execute(
                full_evaluation - direct_evaluation,
                truncated_evaluation - full_evaluation,
                truncated_evaluation - direct_evaluation,
                controls.energy_reference,
            )
            construction_weight = float(
                np.mean(
                    np.linalg.norm(
                        omitted_construction,
                        axis=(-2, -1),
                    )
                    ** 2
                )
            )
            parseval_denominator = max(
                construction_weight,
                tail.omitted_squared_frobenius_weight,
                model.retained_rank * controls.saturation_denominator_floor,
            )
            support_results.append(
                Periodic1DHigherRankSupportResult(
                    maximum_range=tail.maximum_range,
                    rank=model.retained_rank,
                    energy_reference=controls.energy_reference,
                    retained_translations=tail.retained_translations,
                    omitted_squared_frobenius_weight=(
                        tail.omitted_squared_frobenius_weight
                    ),
                    normalized_omitted_squared_frobenius_weight=(
                        tail.normalized_omitted_squared_frobenius_weight
                    ),
                    omitted_frobenius_l2_norm=tail.omitted_frobenius_l2_norm,
                    normalized_omitted_frobenius_l2_norm=(
                        tail.normalized_omitted_frobenius_l2_norm
                    ),
                    omitted_block_l1_norm=tail.omitted_block_l1_norm,
                    normalized_omitted_block_l1_norm=(
                        tail.normalized_omitted_block_l1_norm
                    ),
                    construction_parseval_relative_defect=(
                        abs(construction_weight - tail.omitted_squared_frobenius_weight)
                        / parseval_denominator
                    ),
                    construction_parseval_pass=(
                        abs(construction_weight - tail.omitted_squared_frobenius_weight)
                        / parseval_denominator
                        <= controls.fourier_consistency_tolerance
                    ),
                    truncation=(
                        Periodic1DHigherRankMatrixComparisonResult.from_diagnostics(
                            truncation_diagnostics,
                            controls.perturbation_bound_tolerance,
                        )
                    ),
                    total=Periodic1DHigherRankMatrixComparisonResult.from_diagnostics(
                        total_diagnostics,
                        controls.perturbation_bound_tolerance,
                    ),
                    error_decomposition_defect=(decomposition.maximum_frobenius_defect),
                    normalized_error_decomposition_defect=(
                        decomposition.normalized_maximum_frobenius_defect
                    ),
                    error_decomposition_pass=(
                        decomposition.normalized_maximum_frobenius_defect
                        <= controls.error_decomposition_tolerance
                    ),
                )
            )
        monotonicity = SymmetricRangeTailMonotonicityAnalyzer1D().execute(
            tails,
            controls.tail_monotonicity_tolerance,
        )
        maximum_tail_increase = max(
            max(
                item.normalized_squared_weight_increase,
                item.normalized_l2_norm_increase,
                item.normalized_l1_norm_increase,
            )
            for item in monotonicity
        )
        return Periodic1DHigherRankLocalityAnalysis(
            analysis_request=analysis_request,
            supports=tuple(support_results),
            maximum_tail_increase=maximum_tail_increase,
            all_tail_monotonicity_checks_pass=all(item.passes for item in monotonicity),
        )


__all__ = [
    "Periodic1DHigherRankLocalityAnalysis",
    "Periodic1DHigherRankLocalityAnalysisRequest",
    "Periodic1DHigherRankLocalityAnalyzer",
]
