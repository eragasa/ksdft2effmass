"""Frame and represented-operator recovery for one gauge alignment."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import final

import numpy as np

from ksdft2effmass.analysis.matrix_field.diagnostics import MatrixFieldErrorAnalyzer
from ksdft2effmass.representation_equivalence import RepresentationEquivalence

from ..band_alignment.composite.diagnostics import (
    Periodic1DRankNFrameErrorResult,
    Periodic1DRankNMatrixErrorResult,
)
from .definition import Periodic1DRankNGaugeAlignment
from .fields import (
    Periodic1DRankNGaugeAlignmentEvaluationRequest,
    Periodic1DRankNGaugeAlignmentEvaluator,
)
from .request import Periodic1DRankNGaugeAlignmentAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNRecoveryAnalysisRequest:
    """Bind one complete gauge-alignment request for recovery analysis."""

    analysis_request: Periodic1DRankNGaugeAlignmentAnalysisRequest

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DRankNGaugeAlignmentAnalysisRequest
        ):
            raise TypeError(
                "analysis_request must be the exact gauge-alignment request"
            )


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNRecoveryAnalysis(RepresentationEquivalence):
    """Store separate frame and represented-operator recovery diagnostics."""

    analysis_request: Periodic1DRankNGaugeAlignmentAnalysisRequest
    frame_recovery: Periodic1DRankNFrameErrorResult
    known_frame_recovery_pass: bool | None
    represented_operator_recovery: Periodic1DRankNMatrixErrorResult
    known_operator_recovery_pass: bool | None

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DRankNGaugeAlignmentAnalysisRequest
        ):
            raise TypeError("analysis_request must be the exact analysis request")
        if type(self.frame_recovery) is not Periodic1DRankNFrameErrorResult:
            raise TypeError("frame_recovery must be the exact frame-error record")
        if (
            type(self.represented_operator_recovery)
            is not Periodic1DRankNMatrixErrorResult
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
class Periodic1DRankNRecoveryAnalyzer:
    """Evaluate frame and represented-operator recovery in the selected gauge."""

    __slots__ = ("_request",)

    def __init__(self, request: Periodic1DRankNRecoveryAnalysisRequest) -> None:
        if type(request) is not Periodic1DRankNRecoveryAnalysisRequest:
            raise TypeError("request must be Periodic1DRankNRecoveryAnalysisRequest")
        self._request = request

    @property
    def request(self) -> Periodic1DRankNRecoveryAnalysisRequest:
        """Return the exact recovery request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DRankNRecoveryAnalysis:
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
        frame_recovery = Periodic1DRankNFrameErrorResult(
            rank=model.retained_rank,
            frobenius_maximum=float(np.max(frame_norms)),
            frobenius_rms=float(np.sqrt(np.mean(frame_norms**2))),
            normalized_frobenius_maximum=float(np.max(frame_norms) / frame_scale),
            normalized_frobenius_rms=float(
                np.sqrt(np.mean(frame_norms**2)) / frame_scale
            ),
        )
        direct_construction = Periodic1DRankNGaugeAlignmentEvaluator(
            Periodic1DRankNGaugeAlignmentEvaluationRequest(
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
            norm_energy_scale=controls.energy_reference,
        ).result()
        represented_operator_recovery = (
            Periodic1DRankNMatrixErrorResult.from_diagnostics(
                represented_operator_diagnostics
            )
        )
        known_recovery_applicable = fields.gauge_alignment in (
            Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY,
            Periodic1DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
        )
        return Periodic1DRankNRecoveryAnalysis(
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
    "Periodic1DRankNRecoveryAnalysis",
    "Periodic1DRankNRecoveryAnalysisRequest",
    "Periodic1DRankNRecoveryAnalyzer",
]
