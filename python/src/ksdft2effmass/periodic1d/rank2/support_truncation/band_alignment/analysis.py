"""Support-truncation analysis for the rank-two band-alignment study."""

from __future__ import annotations

from typing import final

import numpy as np
from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.analysis.periodic_bands import (
    BandApproximationErrorAnalyzer1D,
    BandApproximationErrorRequest1D,
)
from ksdft2effmass.periodic1d.support_truncation.base import (
    Periodic1DSupportTruncationAnalyzer,
)
from ksdft2effmass.solidstate.hopping_transforms import (
    BlockHoppingInterpolationRequest1D,
    BlockHoppingInterpolator1D,
    BlockHoppingTruncationRequest1D,
    BlockHoppingTruncator1D,
    ReciprocalOperatorSamples1D,
)

from .request import Periodic1DRank2SupportTruncationAnalysisRequest
from .result import (
    Periodic1DRank2SupportResult,
    Periodic1DRank2SupportTruncationAnalysis,
)


@final
class Periodic1DRank2SupportTruncationAnalyzer(
    Periodic1DSupportTruncationAnalyzer[
        Periodic1DRank2SupportTruncationAnalysisRequest,
        Periodic1DRank2SupportTruncationAnalysis,
    ]
):
    """Remove one channel's symmetric support and retain distinct errors."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic1DRank2SupportTruncationAnalysisRequest,
    ) -> None:
        if type(request) is not Periodic1DRank2SupportTruncationAnalysisRequest:
            raise TypeError("request must be the exact support-truncation request")
        self._request = request

    @property
    def request(self) -> Periodic1DRank2SupportTruncationAnalysisRequest:
        """Return the complete immutable support-truncation request."""
        return self._request

    def execute(self) -> Periodic1DRank2SupportTruncationAnalysis:
        """Return consequences of every frozen symmetric support removal."""
        request = self.request
        model = request.hopping_locality_analysis.request.ordinary_model
        supports = []
        for tail in request.hopping_locality_analysis.tails:
            truncation = BlockHoppingTruncator1D(
                BlockHoppingTruncationRequest1D(
                    model,
                    tail.maximum_range,
                )
            ).execute()
            construction = BlockHoppingInterpolator1D(
                BlockHoppingInterpolationRequest1D(
                    truncation.truncated,
                    request.construction_target.coordinates,
                )
            ).execute()
            evaluation = BlockHoppingInterpolator1D(
                BlockHoppingInterpolationRequest1D(
                    truncation.truncated,
                    request.direct_evaluation.coordinates,
                )
            ).execute()
            truncation_errors = self._maximum_error_channels(
                evaluation,
                request.complete_evaluation,
            )
            total_errors = self._maximum_error_channels(
                evaluation,
                request.direct_evaluation,
            )
            construction_error = BandApproximationErrorAnalyzer1D(
                BandApproximationErrorRequest1D(
                    request.construction_target,
                    construction,
                    request.configuration.dimensionless_absolute_tolerance,
                )
            ).execute()
            supports.append(
                Periodic1DRank2SupportResult(
                    maximum_range=tail.maximum_range,
                    construction_total_spectral_maximum_error=(
                        construction_error.maximum_absolute_error
                    ),
                    evaluation_truncation_hamiltonian_maximum_error=ScalarQuantity(
                        truncation_errors[0],
                        Unitless(),
                    ),
                    evaluation_total_hamiltonian_maximum_error=ScalarQuantity(
                        total_errors[0],
                        Unitless(),
                    ),
                    evaluation_truncation_spectral_maximum_error=ScalarQuantity(
                        truncation_errors[1],
                        Unitless(),
                    ),
                    evaluation_total_spectral_maximum_error=ScalarQuantity(
                        total_errors[1],
                        Unitless(),
                    ),
                )
            )
        return Periodic1DRank2SupportTruncationAnalysis(
            request=request,
            supports=tuple(supports),
        )

    @staticmethod
    def _maximum_error_channels(
        candidate: ReciprocalOperatorSamples1D,
        reference: ReciprocalOperatorSamples1D,
    ) -> tuple[float, float]:
        if len(candidate.matrices) != len(reference.matrices):
            raise ValueError("error-channel operator inventories must have equal size")
        hamiltonian_errors: list[float] = []
        spectral_errors: list[float] = []
        for candidate_matrix, reference_matrix in zip(
            candidate.matrices,
            reference.matrices,
            strict=True,
        ):
            hamiltonian_errors.append(
                float(
                    np.linalg.norm(
                        candidate_matrix.magnitude - reference_matrix.magnitude
                    )
                    / np.sqrt(2.0)
                )
            )
            candidate_hermitian = 0.5 * (
                candidate_matrix.magnitude + candidate_matrix.magnitude.conj().T
            )
            reference_hermitian = 0.5 * (
                reference_matrix.magnitude + reference_matrix.magnitude.conj().T
            )
            spectral_errors.append(
                float(
                    np.max(
                        np.abs(
                            np.linalg.eigvalsh(candidate_hermitian)
                            - np.linalg.eigvalsh(reference_hermitian)
                        )
                    )
                )
            )
        return max(hamiltonian_errors), max(spectral_errors)


__all__ = ["Periodic1DRank2SupportTruncationAnalyzer"]
