"""Assembly of public gauge-alignment evidence from typed scientific stages."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

from ksdft2effmass.periodic1d.rankN.hopping_locality import (
    Periodic1DRankNHoppingLocalityAnalysis,
)
from ksdft2effmass.periodic1d.rankN.support_truncation import (
    Periodic1DRankNSupportTruncationAnalysis,
)

from .fourier import Periodic1DRankNFourierAnalysis
from .interpolation import Periodic1DRankNInterpolationAnalysis
from .recovery import Periodic1DRankNRecoveryAnalysis
from .request import Periodic1DRankNGaugeAlignmentAnalysisRequest
from .results import Periodic1DRankNGaugeAlignmentMeshResult


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNGaugeAlignmentAssemblyRequest:
    """Bind one correlated set of typed gauge-alignment analyses."""

    analysis_request: Periodic1DRankNGaugeAlignmentAnalysisRequest
    recovery_analysis: Periodic1DRankNRecoveryAnalysis
    fourier_analysis: Periodic1DRankNFourierAnalysis
    interpolation_analysis: Periodic1DRankNInterpolationAnalysis
    hopping_locality_analysis: Periodic1DRankNHoppingLocalityAnalysis
    support_truncation_analysis: Periodic1DRankNSupportTruncationAnalysis

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DRankNGaugeAlignmentAnalysisRequest
        ):
            raise TypeError("analysis_request must be the exact analysis request")
        for analysis, expected_type, name in (
            (
                self.recovery_analysis,
                Periodic1DRankNRecoveryAnalysis,
                "recovery_analysis",
            ),
            (
                self.fourier_analysis,
                Periodic1DRankNFourierAnalysis,
                "fourier_analysis",
            ),
            (
                self.interpolation_analysis,
                Periodic1DRankNInterpolationAnalysis,
                "interpolation_analysis",
            ),
            (
                self.hopping_locality_analysis,
                Periodic1DRankNHoppingLocalityAnalysis,
                "hopping_locality_analysis",
            ),
            (
                self.support_truncation_analysis,
                Periodic1DRankNSupportTruncationAnalysis,
                "support_truncation_analysis",
            ),
        ):
            if type(analysis) is not expected_type:
                raise TypeError(f"{name} must have its exact analysis type")
            if analysis.analysis_request is not self.analysis_request:
                raise ValueError(f"{name} must derive from the bound request")


@final
class Periodic1DRankNGaugeAlignmentResultAssembler:
    """Assemble one public mesh result without recomputing scientific values."""

    __slots__ = ("_request",)

    def __init__(self, request: Periodic1DRankNGaugeAlignmentAssemblyRequest) -> None:
        if type(request) is not Periodic1DRankNGaugeAlignmentAssemblyRequest:
            raise TypeError(
                "request must be Periodic1DRankNGaugeAlignmentAssemblyRequest"
            )
        self._request = request

    @property
    def request(self) -> Periodic1DRankNGaugeAlignmentAssemblyRequest:
        """Return the exact assembly request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DRankNGaugeAlignmentMeshResult:
        """Return the public result assembled from correlated stage evidence."""
        request = self._request
        analysis_request = request.analysis_request
        recovery = request.recovery_analysis
        fourier = request.fourier_analysis
        interpolation = request.interpolation_analysis
        hopping_locality = request.hopping_locality_analysis
        support_truncation = request.support_truncation_analysis
        return Periodic1DRankNGaugeAlignmentMeshResult(
            status=analysis_request.status,
            transform_backend_identifier=fourier.transform.backend_identifier,
            transform_backend_version=fourier.transform.backend_version,
            fourier_representative_count=fourier.representative_count,
            fourier_representative_inventory_ordered_unique=(
                fourier.representative_inventory_ordered_unique
            ),
            fourier_inversion_closed=fourier.inversion_closed,
            fourier_index_bijection_pass=fourier.index_bijection_pass,
            nyquist_mode_disposition=fourier.nyquist_mode_disposition,
            coefficient_translations=fourier.coefficient_translations,
            block_raw_frobenius_norms=fourier.block_raw_frobenius_norms,
            block_normalized_frobenius_norms=(fourier.block_normalized_frobenius_norms),
            frame_recovery=recovery.frame_recovery,
            known_frame_recovery_pass=recovery.known_frame_recovery_pass,
            represented_operator_recovery=recovery.represented_operator_recovery,
            known_operator_recovery_pass=recovery.known_operator_recovery_pass,
            reconstruction=fourier.reconstruction,
            reconstruction_pass=fourier.reconstruction_pass,
            interpolation=interpolation.interpolation,
            final_interpolation_operator_pass=(
                interpolation.final_interpolation_operator_pass
            ),
            final_interpolation_spectrum_pass=(
                interpolation.final_interpolation_spectrum_pass
            ),
            parseval_relative_defect=fourier.parseval_relative_defect,
            parseval_pass=fourier.parseval_pass,
            ordinary_hermiticity_defect=fourier.ordinary_hermiticity_defect,
            ordinary_hermiticity_pass=fourier.ordinary_hermiticity_pass,
            twisted_cyclic_hermiticity_defect=(
                fourier.twisted_cyclic_hermiticity_defect
            ),
            twisted_cyclic_hermiticity_pass=(fourier.twisted_cyclic_hermiticity_pass),
            supports=support_truncation.supports,
            maximum_tail_increase=hopping_locality.maximum_tail_increase,
            all_tail_monotonicity_checks_pass=(
                hopping_locality.all_tail_monotonicity_checks_pass
            ),
        )


__all__ = [
    "Periodic1DRankNGaugeAlignmentAssemblyRequest",
    "Periodic1DRankNGaugeAlignmentResultAssembler",
]
