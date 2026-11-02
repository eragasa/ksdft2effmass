"""Periodic-2D rank-two band-equivalence/locality verification actions."""

from __future__ import annotations

from typing import override

from ksdft2effmass.band_equivalence_hopping_locality.calculation import (
    BandEquivalenceHoppingLocalityVerifier,
)
from ksdft2effmass.band_equivalence_hopping_locality.records import (
    BandEquivalenceHoppingLocalityDiagnostics,
)
from ksdft2effmass.band_equivalence_hopping_locality.verification import (
    BandEquivalenceHoppingLocalityResultVerifier,
    BandEquivalenceHoppingLocalityVerification,
    BandEquivalenceHoppingLocalityVerificationThresholds,
)
from ksdft2effmass.band_equivalence_hopping_locality.visualizations.data import (
    BandEquivalenceHoppingLocalityVisualizationData,
)
from ksdft2effmass.model_systems.analysis import ModelAnalysisVerificationResult
from ksdft2effmass.periodic2d.base import Periodic2DCapability

from .reference import (
    Periodic2DRank2BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer,
)
from .request import Periodic2DRank2BandEquivalenceHoppingLocalityRequest
from .result import Periodic2DRank2BandEquivalenceHoppingLocalityCalculationResult
from .visualizations.data import (
    Periodic2DRank2BandEquivalenceHoppingLocalityVisualizationData,
)


class Periodic2DRank2BandEquivalenceHoppingLocalityDiagnosticVerifier(
    BandEquivalenceHoppingLocalityVerifier,
    Periodic2DCapability,
):
    """Independently reconstruct diagnostics for one periodic-2D result."""

    __slots__ = ()

    def __init__(
        self,
        *,
        request: Periodic2DRank2BandEquivalenceHoppingLocalityRequest,
        result: BandEquivalenceHoppingLocalityDiagnostics,
    ) -> None:
        if type(request) is not Periodic2DRank2BandEquivalenceHoppingLocalityRequest:
            raise TypeError(
                "request must be Periodic2DRank2BandEquivalenceHoppingLocalityRequest"
            )
        super().__init__(request=request, result=result)


type _DiagnosticVerifier = (
    Periodic2DRank2BandEquivalenceHoppingLocalityDiagnosticVerifier
)
type _ShellPowerAnalyzer = (
    Periodic2DRank2BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer
)


class Periodic2DRank2BandEquivalenceHoppingLocalityResultVerifier(
    BandEquivalenceHoppingLocalityResultVerifier,
    Periodic2DCapability,
):
    """Authenticate periodic-2D result bytes through qualified independent routes."""

    __slots__ = ()

    def __init__(
        self,
        *,
        result_wire: bytes,
        diagnostic_verifier: _DiagnosticVerifier,
        shell_power_analyzer: _ShellPowerAnalyzer,
        thresholds: BandEquivalenceHoppingLocalityVerificationThresholds,
    ) -> None:
        result = (
            Periodic2DRank2BandEquivalenceHoppingLocalityCalculationResult.from_json(
                result_wire
            )
        )
        if diagnostic_verifier.request.to_json() != result.request.to_json():
            raise ValueError("diagnostic verifier request does not match result bytes")
        if shell_power_analyzer.request.to_json() != result.request.to_json():
            raise ValueError("shell-power analyzer request does not match result bytes")
        super().__init__(
            result_wire=result_wire,
            diagnostic_verifier=diagnostic_verifier,
            shell_power_analyzer=shell_power_analyzer,
            thresholds=thresholds,
        )

    @override
    def result(
        self,
    ) -> ModelAnalysisVerificationResult[
        BandEquivalenceHoppingLocalityVerification,
        Periodic2DRank2BandEquivalenceHoppingLocalityVisualizationData,
    ]:
        """Return verification with a periodic-2D visualization projection."""
        result = super().result()
        visualization_data = (
            Periodic2DRank2BandEquivalenceHoppingLocalityVisualizationData.from_dict(
                result.visualization_data.to_dict()
            )
        )
        return ModelAnalysisVerificationResult(
            verification=result.verification,
            visualization_data=visualization_data,
        )

    @override
    def admit_stored(
        self,
        *,
        verification: BandEquivalenceHoppingLocalityVerification,
        visualization_data: BandEquivalenceHoppingLocalityVisualizationData,
    ) -> ModelAnalysisVerificationResult[
        BandEquivalenceHoppingLocalityVerification,
        Periodic2DRank2BandEquivalenceHoppingLocalityVisualizationData,
    ]:
        """Admit stored evidence through the periodic-2D typed projection."""
        qualified_visualization_data = (
            Periodic2DRank2BandEquivalenceHoppingLocalityVisualizationData.from_dict(
                visualization_data.to_dict()
            )
        )
        admitted = super().admit_stored(
            verification=verification,
            visualization_data=qualified_visualization_data,
        )
        if not isinstance(
            admitted.visualization_data,
            Periodic2DRank2BandEquivalenceHoppingLocalityVisualizationData,
        ):
            raise TypeError("admitted visualization data lost periodic-2D ownership")
        return ModelAnalysisVerificationResult(
            verification=admitted.verification,
            visualization_data=admitted.visualization_data,
        )


__all__ = [
    "Periodic2DRank2BandEquivalenceHoppingLocalityDiagnosticVerifier",
    "Periodic2DRank2BandEquivalenceHoppingLocalityResultVerifier",
]
