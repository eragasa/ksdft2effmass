"""Shifted-mesh interpolation for one gauge-aligned Fourier series."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

import numpy as np
from projectkoios.numerics.numpy.validation import (
    NumpyImmutableArrayConstructor,
    NumpyImmutableArrayValidator,
)
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray
from projectkoios.physkit.solidstate.tb import (
    FinitePeriodicMatrixFourierTensorEvaluator,
)

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    MatrixFieldComparisonAnalyzer,
)

from ..diagnostics import Periodic1DHigherRankMatrixComparisonResult
from .fields import (
    Periodic1DHigherRankGaugeAlignmentEvaluationRequest,
    Periodic1DHigherRankGaugeAlignmentEvaluator,
)
from .fourier import Periodic1DHigherRankFourierAnalysis
from .request import Periodic1DHigherRankGaugeAlignmentAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DHigherRankInterpolationAnalysisRequest:
    """Bind Fourier evidence and the scientific request for shifted evaluation."""

    analysis_request: Periodic1DHigherRankGaugeAlignmentAnalysisRequest
    fourier_analysis: Periodic1DHigherRankFourierAnalysis

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
        if self.fourier_analysis.analysis_request is not self.analysis_request:
            raise ValueError("Fourier analysis must derive from the bound request")
        if (
            self.fourier_analysis.representative_count
            != self.analysis_request.mesh.size
        ):
            raise ValueError("Fourier analysis must match the construction mesh")


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DHigherRankInterpolationAnalysis:
    """Store shifted coordinates, evaluated fields, and interpolation diagnostics."""

    analysis_request: Periodic1DHigherRankGaugeAlignmentAnalysisRequest
    evaluation_coordinates: RealArray
    full_evaluation: ComplexArray
    direct_evaluation: ComplexArray
    interpolation: Periodic1DHigherRankMatrixComparisonResult
    final_interpolation_operator_pass: bool
    final_interpolation_spectrum_pass: bool

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DHigherRankGaugeAlignmentAnalysisRequest
        ):
            raise TypeError("analysis_request must be the exact analysis request")
        coordinates = NumpyImmutableArrayValidator(
            self.evaluation_coordinates,
            "evaluation_coordinates",
            np.dtype(np.float64),
        ).execute()
        full_evaluation = NumpyImmutableArrayValidator(
            self.full_evaluation,
            "full_evaluation",
            np.dtype(np.complex128),
        ).execute()
        direct_evaluation = NumpyImmutableArrayValidator(
            self.direct_evaluation,
            "direct_evaluation",
            np.dtype(np.complex128),
        ).execute()
        rank = self.analysis_request.model.retained_rank
        expected_shape = (coordinates.size, rank, rank)
        if coordinates.ndim != 1:
            raise ValueError("evaluation_coordinates must be one-dimensional")
        if full_evaluation.shape != expected_shape:
            raise ValueError("full_evaluation must have shape (N, r, r)")
        if direct_evaluation.shape != expected_shape:
            raise ValueError("direct_evaluation must have shape (N, r, r)")
        evaluation_mesh_size = (
            self.analysis_request.calculation_request.configuration.evaluation_mesh_size
        )
        if coordinates.size != evaluation_mesh_size:
            raise ValueError("evaluation coordinates must match the declared mesh")
        if type(self.interpolation) is not Periodic1DHigherRankMatrixComparisonResult:
            raise TypeError("interpolation must be the exact comparison record")
        if type(self.final_interpolation_operator_pass) is not bool:
            raise TypeError("final_interpolation_operator_pass must be a built-in bool")
        if type(self.final_interpolation_spectrum_pass) is not bool:
            raise TypeError("final_interpolation_spectrum_pass must be a built-in bool")


@final
class Periodic1DHigherRankInterpolationAnalyzer:
    """Evaluate a Fourier series on the disjoint shifted mesh."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic1DHigherRankInterpolationAnalysisRequest,
    ) -> None:
        if type(request) is not Periodic1DHigherRankInterpolationAnalysisRequest:
            raise TypeError(
                "request must be Periodic1DHigherRankInterpolationAnalysisRequest"
            )
        self._request = request

    @property
    def request(self) -> Periodic1DHigherRankInterpolationAnalysisRequest:
        """Return the exact interpolation request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DHigherRankInterpolationAnalysis:
        """Return shifted-mesh interpolation fields and diagnostics."""
        request = self._request
        analysis_request = request.analysis_request
        calculation_request = analysis_request.calculation_request
        controls = calculation_request.controls
        configuration = calculation_request.configuration
        evaluation_coordinates = NumpyImmutableArrayConstructor(
            np.asarray(
                -0.5
                + (
                    np.arange(configuration.evaluation_mesh_size, dtype=np.float64)
                    + configuration.evaluation_shift_numerator
                    / configuration.evaluation_shift_denominator
                )
                / configuration.evaluation_mesh_size,
                dtype=np.float64,
            ),
            "evaluation_coordinates",
            np.dtype(np.float64),
        ).execute()
        full_evaluation_values = (
            FinitePeriodicMatrixFourierTensorEvaluator(
                series=request.fourier_analysis.transform.series,
                coordinate_axes=(evaluation_coordinates,),
                maximum_working_elements=controls.maximum_working_elements,
            )
            .result()
            .matrix_values
        )
        full_evaluation = NumpyImmutableArrayConstructor(
            np.asarray(full_evaluation_values, dtype=np.complex128),
            "full_evaluation",
            np.dtype(np.complex128),
        ).execute()
        direct_evaluation = Periodic1DHigherRankGaugeAlignmentEvaluator(
            Periodic1DHigherRankGaugeAlignmentEvaluationRequest(
                calculation_request=calculation_request,
                model=analysis_request.model,
                gauge_alignment=analysis_request.status.gauge_alignment,
                coordinates=evaluation_coordinates,
                global_selection=analysis_request.global_selection,
            )
        ).execute()
        interpolation_diagnostics = MatrixFieldComparisonAnalyzer(
            approximation=full_evaluation,
            reference=direct_evaluation,
            energy_reference=controls.energy_reference,
            saturation_denominator_floor=controls.saturation_denominator_floor,
        ).execute()
        interpolation = Periodic1DHigherRankMatrixComparisonResult.from_diagnostics(
            interpolation_diagnostics,
            controls.perturbation_bound_tolerance,
        )
        return Periodic1DHigherRankInterpolationAnalysis(
            analysis_request=analysis_request,
            evaluation_coordinates=evaluation_coordinates,
            full_evaluation=full_evaluation,
            direct_evaluation=direct_evaluation,
            interpolation=interpolation,
            final_interpolation_operator_pass=(
                interpolation.errors.normalized_matrix_frobenius_maximum
                <= controls.final_interpolation_operator_tolerance
            ),
            final_interpolation_spectrum_pass=(
                interpolation.errors.normalized_ordered_spectrum_maximum
                <= controls.final_interpolation_spectrum_tolerance
            ),
        )


__all__ = [
    "Periodic1DHigherRankInterpolationAnalysis",
    "Periodic1DHigherRankInterpolationAnalysisRequest",
    "Periodic1DHigherRankInterpolationAnalyzer",
]
