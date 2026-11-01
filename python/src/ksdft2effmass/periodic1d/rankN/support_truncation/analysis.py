"""Rank-N symmetric-support truncation analysis for periodic one dimension."""

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
)
from ksdft2effmass.periodic1d.higher_rank_alignment.diagnostics import (
    Periodic1DRankNMatrixComparisonResult,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.gauge_alignment.fourier import (
    Periodic1DRankNFourierAnalysis,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.gauge_alignment.interpolation import (  # noqa: E501
    Periodic1DRankNInterpolationAnalysis,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.gauge_alignment.request import (
    Periodic1DRankNGaugeAlignmentAnalysisRequest,
)
from ksdft2effmass.periodic1d.rankN.hopping_locality import (
    Periodic1DRankNHoppingLocalityAnalysis,
    Periodic1DRankNHoppingLocalityAnalysisRequest,
    Periodic1DRankNHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.support_truncation import (
    Periodic1DSupportTruncation,
)

from .result import Periodic1DRankNSupportResult


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNSupportTruncationAnalysisRequest:
    """Bind locality, Fourier, and interpolation evidence for support removal."""

    analysis_request: Periodic1DRankNGaugeAlignmentAnalysisRequest
    fourier_analysis: Periodic1DRankNFourierAnalysis
    interpolation_analysis: Periodic1DRankNInterpolationAnalysis
    hopping_locality_analysis: Periodic1DRankNHoppingLocalityAnalysis

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DRankNGaugeAlignmentAnalysisRequest
        ):
            raise TypeError(
                "analysis_request must be the exact gauge-alignment request"
            )
        if type(self.fourier_analysis) is not Periodic1DRankNFourierAnalysis:
            raise TypeError("fourier_analysis must be the exact Fourier analysis")
        if (
            type(self.interpolation_analysis)
            is not Periodic1DRankNInterpolationAnalysis
        ):
            raise TypeError(
                "interpolation_analysis must be the exact interpolation analysis"
            )
        if (
            type(self.hopping_locality_analysis)
            is not Periodic1DRankNHoppingLocalityAnalysis
        ):
            raise TypeError(
                "hopping_locality_analysis must be the exact locality analysis"
            )
        if self.fourier_analysis.analysis_request is not self.analysis_request:
            raise ValueError("Fourier analysis must derive from the bound request")
        if self.interpolation_analysis.analysis_request is not self.analysis_request:
            raise ValueError(
                "interpolation analysis must derive from the bound request"
            )
        if self.hopping_locality_analysis.analysis_request is not self.analysis_request:
            raise ValueError("locality analysis must derive from the bound request")
        expected_size = (
            self.analysis_request.calculation_request.configuration.evaluation_mesh_size
        )
        if self.interpolation_analysis.evaluation_coordinates.size != expected_size:
            raise ValueError("interpolation analysis must match the evaluation mesh")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNSupportTruncationAnalysis(Periodic1DSupportTruncation):
    """Retain consequences of irreversible symmetric-support removal."""

    analysis_request: Periodic1DRankNGaugeAlignmentAnalysisRequest
    supports: tuple[Periodic1DRankNSupportResult, ...]

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DRankNGaugeAlignmentAnalysisRequest
        ):
            raise TypeError("analysis_request must be the exact analysis request")
        if type(self.supports) is not tuple or not all(
            type(item) is Periodic1DRankNSupportResult for item in self.supports
        ):
            raise TypeError("supports must contain exact support-result records")
        expected_ranges = (
            self.analysis_request.calculation_request.controls.support_radii
        )
        if tuple(item.maximum_range for item in self.supports) != expected_ranges:
            raise ValueError("supports must follow the frozen support inventory")


@final
class Periodic1DRankNSupportTruncationAnalyzer:
    """Construct truncated operators and retain their distinct error channels."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic1DRankNSupportTruncationAnalysisRequest,
    ) -> None:
        if type(request) is not Periodic1DRankNSupportTruncationAnalysisRequest:
            raise TypeError(
                "request must be Periodic1DRankNSupportTruncationAnalysisRequest"
            )
        self._request = request

    @property
    def request(self) -> Periodic1DRankNSupportTruncationAnalysisRequest:
        """Return the exact support-truncation request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DRankNSupportTruncationAnalysis:
        """Return support-removal and separate matrix-error diagnostics."""
        request = self._request
        analysis_request = request.analysis_request
        controls = analysis_request.calculation_request.controls
        model = analysis_request.model
        coordinates = analysis_request.aligned_fields.coordinates
        transform = request.fourier_analysis.transform
        interpolation = request.interpolation_analysis
        evaluation_coordinates = interpolation.evaluation_coordinates
        full_evaluation = interpolation.full_evaluation
        direct_evaluation = interpolation.direct_evaluation
        support_results: list[Periodic1DRankNSupportResult] = []
        modes = transform.series.integer_modes[:, 0]
        for tail in request.hopping_locality_analysis.tails:
            retained_mask = np.abs(modes) <= tail.maximum_range
            indices = tuple(int(index) for index in np.flatnonzero(retained_mask))
            omitted_indices = tuple(
                int(index) for index in np.flatnonzero(np.logical_not(retained_mask))
            )
            truncated_series = transform.series.take(indices)
            omitted_series = transform.series.take(omitted_indices)
            truncated_evaluation = (
                FinitePeriodicMatrixFourierTensorEvaluator(
                    series=truncated_series,
                    coordinate_axes=(evaluation_coordinates,),
                    maximum_working_elements=controls.maximum_working_elements,
                )
                .result()
                .matrix_values
            )
            omitted_construction = (
                FinitePeriodicMatrixFourierTensorEvaluator(
                    series=omitted_series,
                    coordinate_axes=(coordinates,),
                    maximum_working_elements=controls.maximum_working_elements,
                )
                .result()
                .matrix_values
            )
            truncation_diagnostics = MatrixFieldComparisonAnalyzer(
                approximation=truncated_evaluation,
                reference=full_evaluation,
                norm_energy_scale=controls.energy_reference,
                saturation_denominator_floor=controls.saturation_denominator_floor,
            ).execute()
            total_diagnostics = MatrixFieldComparisonAnalyzer(
                approximation=truncated_evaluation,
                reference=direct_evaluation,
                norm_energy_scale=controls.energy_reference,
                saturation_denominator_floor=controls.saturation_denominator_floor,
            ).execute()
            decomposition = MatrixErrorDecompositionAnalyzer(
                interpolation_error=full_evaluation - direct_evaluation,
                truncation_error=truncated_evaluation - full_evaluation,
                total_error=truncated_evaluation - direct_evaluation,
                norm_energy_scale=controls.energy_reference,
            ).execute()
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
                Periodic1DRankNSupportResult(
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
                        Periodic1DRankNMatrixComparisonResult.from_diagnostics(
                            truncation_diagnostics,
                            controls.perturbation_bound_tolerance,
                        )
                    ),
                    total=Periodic1DRankNMatrixComparisonResult.from_diagnostics(
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
        return Periodic1DRankNSupportTruncationAnalysis(
            analysis_request=analysis_request,
            supports=tuple(support_results),
        )


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNLocalityAnalysisRequest:
    """Historical request adapter for the former combined locality action."""

    analysis_request: Periodic1DRankNGaugeAlignmentAnalysisRequest
    fourier_analysis: Periodic1DRankNFourierAnalysis
    interpolation_analysis: Periodic1DRankNInterpolationAnalysis

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DRankNGaugeAlignmentAnalysisRequest
        ):
            raise TypeError(
                "analysis_request must be the exact gauge-alignment request"
            )
        if type(self.fourier_analysis) is not Periodic1DRankNFourierAnalysis:
            raise TypeError("fourier_analysis must be the exact Fourier analysis")
        if (
            type(self.interpolation_analysis)
            is not Periodic1DRankNInterpolationAnalysis
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


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNLocalityAnalysis(Periodic1DSupportTruncation):
    """Historical combined view retained while consumers migrate by capability."""

    analysis_request: Periodic1DRankNGaugeAlignmentAnalysisRequest
    supports: tuple[Periodic1DRankNSupportResult, ...]
    maximum_tail_increase: float
    all_tail_monotonicity_checks_pass: bool

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DRankNGaugeAlignmentAnalysisRequest
        ):
            raise TypeError("analysis_request must be the exact analysis request")
        if type(self.supports) is not tuple or not all(
            type(item) is Periodic1DRankNSupportResult for item in self.supports
        ):
            raise TypeError("supports must contain exact support-result records")
        if type(self.maximum_tail_increase) is not float:
            raise TypeError("maximum_tail_increase must be a built-in float")
        if type(self.all_tail_monotonicity_checks_pass) is not bool:
            raise TypeError("all_tail_monotonicity_checks_pass must be a built-in bool")


@final
class Periodic1DRankNLocalityAnalyzer:
    """Compatibility action composing the separated locality and truncation owners."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic1DRankNLocalityAnalysisRequest,
    ) -> None:
        if type(request) is not Periodic1DRankNLocalityAnalysisRequest:
            raise TypeError("request must be Periodic1DRankNLocalityAnalysisRequest")
        self._request = request

    @property
    def request(self) -> Periodic1DRankNLocalityAnalysisRequest:
        """Return the exact historical request bound to this adapter."""
        return self._request

    def execute(self) -> Periodic1DRankNLocalityAnalysis:
        """Compose the separated channels into the historical combined view."""
        request = self._request
        hopping_locality = Periodic1DRankNHoppingLocalityAnalyzer(
            request=Periodic1DRankNHoppingLocalityAnalysisRequest(
                analysis_request=request.analysis_request,
                fourier_analysis=request.fourier_analysis,
            )
        ).execute()
        support_truncation = Periodic1DRankNSupportTruncationAnalyzer(
            request=Periodic1DRankNSupportTruncationAnalysisRequest(
                analysis_request=request.analysis_request,
                fourier_analysis=request.fourier_analysis,
                interpolation_analysis=request.interpolation_analysis,
                hopping_locality_analysis=hopping_locality,
            )
        ).execute()
        return Periodic1DRankNLocalityAnalysis(
            analysis_request=request.analysis_request,
            supports=support_truncation.supports,
            maximum_tail_increase=hopping_locality.maximum_tail_increase,
            all_tail_monotonicity_checks_pass=(
                hopping_locality.all_tail_monotonicity_checks_pass
            ),
        )


__all__ = [
    "Periodic1DRankNLocalityAnalysis",
    "Periodic1DRankNLocalityAnalysisRequest",
    "Periodic1DRankNLocalityAnalyzer",
    "Periodic1DRankNSupportTruncationAnalysis",
    "Periodic1DRankNSupportTruncationAnalysisRequest",
    "Periodic1DRankNSupportTruncationAnalyzer",
]
