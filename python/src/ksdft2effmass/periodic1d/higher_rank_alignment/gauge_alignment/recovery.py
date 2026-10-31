"""Frame and represented-operator recovery for one gauge alignment."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import final

import numpy as np

from ksdft2effmass.analysis.matrix_field.diagnostics import MatrixFieldErrorAnalyzer
from ksdft2effmass.representation_equivalence import RepresentationEquivalence

from ..diagnostics import (
    Periodic1DHigherRankFrameErrorResult,
    Periodic1DHigherRankMatrixErrorResult,
)
from .definition import Periodic1DHigherRankGaugeAlignment
from .fields import (
    Periodic1DHigherRankGaugeAlignmentEvaluationRequest,
    Periodic1DHigherRankGaugeAlignmentEvaluator,
)
from .request import Periodic1DHigherRankGaugeAlignmentAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DHigherRankRecoveryAnalysisRequest:
    """Bind one complete gauge-alignment request for recovery analysis."""

    analysis_request: Periodic1DHigherRankGaugeAlignmentAnalysisRequest

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DHigherRankGaugeAlignmentAnalysisRequest
        ):
            raise TypeError(
                "analysis_request must be the exact gauge-alignment request"
            )


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DHigherRankRecoveryAnalysis(RepresentationEquivalence):
    """Store separate frame and represented-operator recovery diagnostics."""

    analysis_request: Periodic1DHigherRankGaugeAlignmentAnalysisRequest
    frame_recovery: Periodic1DHigherRankFrameErrorResult
    known_frame_recovery_pass: bool | None
    represented_operator_recovery: Periodic1DHigherRankMatrixErrorResult
    known_operator_recovery_pass: bool | None

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DHigherRankGaugeAlignmentAnalysisRequest
        ):
            raise TypeError("analysis_request must be the exact analysis request")
        if type(self.frame_recovery) is not Periodic1DHigherRankFrameErrorResult:
            raise TypeError("frame_recovery must be the exact frame-error record")
        if (
            type(self.represented_operator_recovery)
            is not Periodic1DHigherRankMatrixErrorResult
        ):
            raise TypeError(
                "represented_operator_recovery must be the exact matrix-error record"
            )
        for value, name in (
            (self.known_frame_recovery_pass, "known_frame_recovery_pass"),
            (self.known_operator_recovery_pass, "known_operator_recovery_pass"),
        ):
            if value is not None and type(value) is not bool:
                raise TypeError(f"{name} must be a built-in bool or None")


@final
class Periodic1DHigherRankRecoveryAnalyzer:
    """Evaluate frame and represented-operator recovery in the selected gauge."""

    __slots__ = ("_request",)

    def __init__(self, request: Periodic1DHigherRankRecoveryAnalysisRequest) -> None:
        if type(request) is not Periodic1DHigherRankRecoveryAnalysisRequest:
            raise TypeError(
                "request must be Periodic1DHigherRankRecoveryAnalysisRequest"
            )
        self._request = request

    @property
    def request(self) -> Periodic1DHigherRankRecoveryAnalysisRequest:
        """Return the exact recovery request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DHigherRankRecoveryAnalysis:
        """Return separate frame and represented-operator recovery diagnostics."""
        analysis_request = self._request.analysis_request
        calculation_request = analysis_request.calculation_request
        controls = calculation_request.controls
        model = analysis_request.model
        fields = analysis_request.aligned_fields
        coordinates = fields.coordinates
        reference_frames = model.reference_frames(coordinates)
        frame_norms = np.linalg.norm(
            fields.frames - reference_frames,
            axis=(-2, -1),
        )
        frame_scale = math.sqrt(model.retained_rank)
        frame_recovery = Periodic1DHigherRankFrameErrorResult(
            rank=model.retained_rank,
            frobenius_maximum=float(np.max(frame_norms)),
            frobenius_rms=float(np.sqrt(np.mean(frame_norms**2))),
            normalized_frobenius_maximum=float(np.max(frame_norms) / frame_scale),
            normalized_frobenius_rms=float(
                np.sqrt(np.mean(frame_norms**2)) / frame_scale
            ),
        )
        direct_construction = Periodic1DHigherRankGaugeAlignmentEvaluator(
            Periodic1DHigherRankGaugeAlignmentEvaluationRequest(
                calculation_request=calculation_request,
                model=model,
                gauge_alignment=fields.gauge_alignment,
                coordinates=coordinates,
                global_selection=analysis_request.global_selection,
            )
        ).execute()
        represented_operator_diagnostics = MatrixFieldErrorAnalyzer(
            approximation=fields.represented_operators,
            reference=direct_construction,
            energy_reference=controls.energy_reference,
        ).result()
        represented_operator_recovery = (
            Periodic1DHigherRankMatrixErrorResult.from_diagnostics(
                represented_operator_diagnostics
            )
        )
        known_recovery_applicable = fields.gauge_alignment in (
            Periodic1DHigherRankGaugeAlignment.POINTWISE_UNITARY,
            Periodic1DHigherRankGaugeAlignment.KNOWN_INVERSE_ORACLE,
        )
        return Periodic1DHigherRankRecoveryAnalysis(
            analysis_request=analysis_request,
            frame_recovery=frame_recovery,
            known_frame_recovery_pass=(
                frame_recovery.normalized_frobenius_maximum
                <= controls.direct_recovery_tolerance
                if known_recovery_applicable
                else None
            ),
            represented_operator_recovery=represented_operator_recovery,
            known_operator_recovery_pass=(
                represented_operator_recovery.normalized_matrix_frobenius_maximum
                <= controls.direct_recovery_tolerance
                if known_recovery_applicable
                else None
            ),
        )


__all__ = [
    "Periodic1DHigherRankRecoveryAnalysis",
    "Periodic1DHigherRankRecoveryAnalysisRequest",
    "Periodic1DHigherRankRecoveryAnalyzer",
]
