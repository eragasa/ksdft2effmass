"""Periodic-2D rank-two hopping-locality analysis action."""

from __future__ import annotations

from projectkoios.physkit.solidstate.tb.diagnostics import BlockHoppingPowerAnalyzer

from ksdft2effmass.band_equivalence_hopping_locality.shell_power import (  # noqa: E501
    BandEquivalenceHoppingLocalityFourierShellPowerAnalyzer,
)

from .base import Periodic2DRank2HoppingLocalityAnalyzerRole
from .request import Periodic2DRank2HoppingLocalityAnalysisRequest
from .result import Periodic2DRank2HoppingLocalityAnalysis


class Periodic2DRank2HoppingLocalityAnalyzer(
    Periodic2DRank2HoppingLocalityAnalyzerRole[
        Periodic2DRank2HoppingLocalityAnalysisRequest,
        Periodic2DRank2HoppingLocalityAnalysis,
    ]
):
    """Measure one periodic-2D channel without removing hopping support."""

    __slots__ = ("_power_analyzer", "_request")

    def __init__(
        self,
        *,
        request: Periodic2DRank2HoppingLocalityAnalysisRequest,
        power_analyzer: BlockHoppingPowerAnalyzer,
    ) -> None:
        if type(request) is not Periodic2DRank2HoppingLocalityAnalysisRequest:
            raise TypeError("request must be the exact periodic-2D rank-two request")
        if type(power_analyzer) is not BlockHoppingPowerAnalyzer:
            raise TypeError("power_analyzer must be BlockHoppingPowerAnalyzer")
        self._request = request
        self._power_analyzer = power_analyzer

    @property
    def request(self) -> Periodic2DRank2HoppingLocalityAnalysisRequest:
        """Return the immutable request bound to this action."""
        return self._request

    def execute(self) -> Periodic2DRank2HoppingLocalityAnalysis:
        """Return normalized unchanged hopping powers through PhysKit."""
        result = BandEquivalenceHoppingLocalityFourierShellPowerAnalyzer(
            identifier=self._request.identifier,
            energy_reference=self._request.energy_reference,
            basis_identifier=self._request.basis_identifier,
            series=self._request.series,
            shell_indices=self._request.shell_indices,
            retained_rank=2,
            power_analyzer=self._power_analyzer,
        ).execute()
        return Periodic2DRank2HoppingLocalityAnalysis(
            retained_rank=result.retained_rank,
            powers=result.powers,
            request=self._request,
        )


__all__ = ["Periodic2DRank2HoppingLocalityAnalyzer"]
