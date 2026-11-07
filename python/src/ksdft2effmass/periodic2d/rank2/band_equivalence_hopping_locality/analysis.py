"""Periodic-2D rank-two band-equivalence/locality analysis action."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, cast

from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)
from projectkoios.numerics.numpy.typing import Complex128Array

from ksdft2effmass.band_equivalence_hopping_locality.alignment import (
    FrameTransportDiagnostic,
    RestrictedAlignmentDiagnostic,
)
from ksdft2effmass.band_equivalence_hopping_locality.analysis import (
    BandEquivalenceHoppingLocalityAnalysis,
    Rank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.band_equivalence_hopping_locality.results import (
    BandEquivalenceHoppingLocalityErrorChannels,
)
from ksdft2effmass.band_equivalence_hopping_locality.shell_power import (
    MetricShellHoppingPowerResult,
)
from ksdft2effmass.periodic2d.rank2.band_alignment.frame_transport.analysis import (
    Periodic2DRank2TransportAnalyzer,
)
from ksdft2effmass.periodic2d.rank2.band_alignment.frame_transport.request import (
    Periodic2DRank2TransportAnalysisRequest,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.base import (
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalysisRole,
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzerRole,
)
from ksdft2effmass.periodic2d.rank2.gauge_alignment.analysis import (
    Periodic2DRank2RestrictedGaugeAlignmentAnalyzer,
)
from ksdft2effmass.periodic2d.rank2.gauge_alignment.request import (
    Periodic2DRank2RestrictedGaugeAlignmentAnalysisRequest,
)
from ksdft2effmass.periodic2d.rank2.support_truncation.analysis import (
    Periodic2DRank2SupportTruncationAnalyzer,
)
from ksdft2effmass.periodic2d.rank2.support_truncation.request import (
    Periodic2DRank2SupportTruncationAnalysisRequest,
    Periodic2DRank2SupportTruncationChannelEnum,
)
from ksdft2effmass.real_space_support_truncation import (
    MetricShellSupportInventory,
    RealSpaceSupportTruncationModelToleranceSelection,
)

from .request import Periodic2DRank2BandEquivalenceHoppingLocalityRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis(
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalysisRole[
        Periodic2DRank2BandEquivalenceHoppingLocalityRequest
    ],
    BandEquivalenceHoppingLocalityAnalysis,
):
    """Retain one complete periodic-2D rank-two scientific analysis."""

    request: Periodic2DRank2BandEquivalenceHoppingLocalityRequest

    def __post_init__(self) -> None:
        if (
            type(self.request)
            is not Periodic2DRank2BandEquivalenceHoppingLocalityRequest
        ):
            raise TypeError(
                "request must be Periodic2DRank2BandEquivalenceHoppingLocalityRequest"
            )
        super().__post_init__()


class Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer(
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzerRole[
        Periodic2DRank2BandEquivalenceHoppingLocalityRequest
    ],
    Rank2BandEquivalenceHoppingLocalityAnalyzer,
):
    """Compose periodic-2D rank-two capability actions around shared arithmetic."""

    __slots__ = ()

    def __init__(
        self,
        *,
        request: Periodic2DRank2BandEquivalenceHoppingLocalityRequest,
    ) -> None:
        if type(request) is not Periodic2DRank2BandEquivalenceHoppingLocalityRequest:
            raise TypeError(
                "request must be Periodic2DRank2BandEquivalenceHoppingLocalityRequest"
            )
        super().__init__(request=request)

    @property
    def request(self) -> Periodic2DRank2BandEquivalenceHoppingLocalityRequest:
        """Return the exact immutable request bound to this action."""
        return cast(
            Periodic2DRank2BandEquivalenceHoppingLocalityRequest, super().request
        )

    def analyze_frame_transport(
        self,
        *,
        frame: Complex128Array,
        dimension: int,
        rank_absolute: float,
        rank_relative: float,
    ) -> FrameTransportDiagnostic:
        """Route frame transport through its periodic-2D capability owner."""
        if dimension != 2:
            raise ValueError("dimension must be two")
        return Periodic2DRank2TransportAnalyzer(
            request=Periodic2DRank2TransportAnalysisRequest(
                frame=frame,
                rank_absolute=rank_absolute,
                rank_relative=rank_relative,
            )
        ).execute()

    def analyze_restricted_gauge_alignment(
        self,
        *,
        reference: Complex128Array,
        comparison: Complex128Array,
    ) -> RestrictedAlignmentDiagnostic:
        """Route restricted alignment through its periodic-2D capability owner."""
        return Periodic2DRank2RestrictedGaugeAlignmentAnalyzer(
            request=Periodic2DRank2RestrictedGaugeAlignmentAnalysisRequest(
                reference=reference,
                comparison=comparison,
            )
        ).execute()

    def analyze_ordinary_hopping_locality(
        self,
        *,
        channel: Literal["reference", "comparison"],
        energy_reference: str,
        basis_identifier: str,
        series: NumpyFiniteFourierMatrixSeries,
        shell_indices: tuple[int, ...],
        retained_rank: int,
    ) -> MetricShellHoppingPowerResult:
        """Preserve the legacy Fourier-channel diagnostic without model promotion."""
        if retained_rank != 2:
            raise ValueError("retained_rank must be two")
        # Transformed floating-point coefficients need not satisfy the exact model
        # admissibility contract byte-for-byte. Keep this legacy diagnostic at the
        # representation boundary rather than misclassifying it as an exact model.
        return super().analyze_ordinary_hopping_locality(
            channel=channel,
            energy_reference=energy_reference,
            basis_identifier=basis_identifier,
            series=series,
            shell_indices=shell_indices,
            retained_rank=retained_rank,
        )

    def analyze_support_truncation(
        self,
        *,
        channel: Literal["reference", "comparison"],
        support_inventory: MetricShellSupportInventory,
        total_errors: tuple[BandEquivalenceHoppingLocalityErrorChannels, ...],
        tolerance: float,
    ) -> RealSpaceSupportTruncationModelToleranceSelection:
        """Route one channel through its periodic-2D support-decision owner."""
        return Periodic2DRank2SupportTruncationAnalyzer(
            request=Periodic2DRank2SupportTruncationAnalysisRequest(
                channel=Periodic2DRank2SupportTruncationChannelEnum(channel),
                support_inventory=support_inventory,
                total_errors=total_errors,
                tolerance=tolerance,
            )
        ).execute()

    def execute(self) -> Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis:
        """Execute the shared composition and retain the rank-first owner type."""
        analysis = Rank2BandEquivalenceHoppingLocalityAnalyzer.execute(self)
        return Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis(
            request=self.request,
            status=analysis.status,
            cases=analysis.cases,
        )


__all__ = [
    "Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis",
    "Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer",
]
