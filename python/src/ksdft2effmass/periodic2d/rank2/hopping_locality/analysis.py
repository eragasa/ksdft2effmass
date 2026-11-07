"""Periodic-2D rank-two hopping-locality analysis action."""

from __future__ import annotations

from projectkoios.physkit.periodic.lattice.hopping import DenseBlockHoppingModel
from projectkoios.physkit.solidstate.tb.diagnostics import BlockHoppingPowerAnalyzer

from ksdft2effmass.band_equivalence_hopping_locality.shell_power import (  # noqa: E501
    MetricShellHoppingPowerAnalyzer,
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
    """Measure one periodic-2D model without removing hopping support.

    Parameters
    ----------
    request
        Exact model and term-to-shell correlation to analyze.
    power_analyzer
        PhysKit collaborator that computes raw block Frobenius powers.

    Notes
    -----
    The action is descriptive. It neither truncates terms nor decides whether a model
    satisfies a locality or scientific-acceptance threshold.

    """

    __slots__ = ("_power_analyzer", "_request")

    def __init__(
        self,
        *,
        request: Periodic2DRank2HoppingLocalityAnalysisRequest,
        power_analyzer: BlockHoppingPowerAnalyzer,
    ) -> None:
        """Bind one exact request and raw-power collaborator.

        Raises
        ------
        TypeError
            If either collaborator lacks its exact nominal owner.

        """
        if type(request) is not Periodic2DRank2HoppingLocalityAnalysisRequest:
            raise TypeError("request must be the exact periodic-2D rank-two request")
        if type(power_analyzer) is not BlockHoppingPowerAnalyzer:
            raise TypeError("power_analyzer must be BlockHoppingPowerAnalyzer")
        self._request = request
        self._power_analyzer = power_analyzer

    @property
    def request(self) -> Periodic2DRank2HoppingLocalityAnalysisRequest:
        """Return the immutable request bound to this action.

        Returns
        -------
        Periodic2DRank2HoppingLocalityAnalysisRequest
            Exact request retained by identity.

        """
        return self._request

    def execute(self) -> Periodic2DRank2HoppingLocalityAnalysis:
        """Return normalized unchanged hopping powers through PhysKit.

        Returns
        -------
        Periodic2DRank2HoppingLocalityAnalysis
            Immutable rank-two powers correlated with the exact input request.

        Raises
        ------
        TypeError
            If the admitted scientific model composes a sparse representation; the
            installed PhysKit raw-power collaborator currently requires dense storage.

        """
        representation = self._request.model.block_hopping_model
        # Sparse values remain valid scientific models, but this numerical route is
        # deliberately not allowed to densify them implicitly at analysis time.
        if type(representation) is not DenseBlockHoppingModel:
            raise TypeError("hopping-locality analysis requires a dense representation")
        # Normalization by retained rank belongs to the KSD metric-shell analyzer;
        # PhysKit continues to own only the raw coefficient powers.
        result = MetricShellHoppingPowerAnalyzer(
            model=representation,
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
