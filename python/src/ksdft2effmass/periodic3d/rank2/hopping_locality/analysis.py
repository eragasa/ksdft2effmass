"""Periodic-3D rank-two hopping-locality analysis action."""

from __future__ import annotations

from projectkoios.physkit.solidstate.tb.diagnostics import BlockHoppingPowerAnalyzer

from ksdft2effmass.band_equivalence_hopping_locality.shell_power import (  # noqa: E501
    BandEquivalenceHoppingLocalityFourierShellPowerAnalyzer,
)

from .base import Periodic3DRank2HoppingLocalityAnalyzerRole
from .request import Periodic3DRank2HoppingLocalityAnalysisRequest
from .result import Periodic3DRank2HoppingLocalityAnalysis


class Periodic3DRank2HoppingLocalityAnalyzer(
    Periodic3DRank2HoppingLocalityAnalyzerRole[
        Periodic3DRank2HoppingLocalityAnalysisRequest,
        Periodic3DRank2HoppingLocalityAnalysis,
    ]
):
    """Measure one periodic-3D channel without removing hopping support."""

    __slots__ = ("_power_analyzer", "_request")

    def __init__(
        self,
        *,
        request: Periodic3DRank2HoppingLocalityAnalysisRequest,
        power_analyzer: BlockHoppingPowerAnalyzer,
    ) -> None:
        if type(request) is not Periodic3DRank2HoppingLocalityAnalysisRequest:
            raise TypeError("request must be the exact periodic-3D rank-two request")
        if type(power_analyzer) is not BlockHoppingPowerAnalyzer:
            raise TypeError("power_analyzer must be BlockHoppingPowerAnalyzer")
        self._request = request
        self._power_analyzer = power_analyzer

    @property
    def request(self) -> Periodic3DRank2HoppingLocalityAnalysisRequest:
        """Return the immutable request bound to this action."""
        return self._request

    def execute(self) -> Periodic3DRank2HoppingLocalityAnalysis:
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
        return Periodic3DRank2HoppingLocalityAnalysis(
            retained_rank=result.retained_rank,
            powers=result.powers,
            request=self._request,
        )


__all__ = ["Periodic3DRank2HoppingLocalityAnalyzer"]
