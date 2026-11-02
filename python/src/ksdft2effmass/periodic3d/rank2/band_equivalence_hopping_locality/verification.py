"""Periodic-3D rank-two band-equivalence/locality verification actions."""

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

from .base import Periodic3DRank2BandEquivalenceHoppingLocalityAction
from .reference import (
    Periodic3DRank2BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer,
)
from .request import Periodic3DRank2BandEquivalenceHoppingLocalityRequest
from .result import Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult
from .visualizations.data import (
    Periodic3DRank2BandEquivalenceHoppingLocalityVisualizationData,
)


class Periodic3DRank2BandEquivalenceHoppingLocalityDiagnosticVerifier(
    BandEquivalenceHoppingLocalityVerifier,
    Periodic3DRank2BandEquivalenceHoppingLocalityAction,
):
    """Independently reconstruct diagnostics for one periodic-3D result."""

    __slots__ = ()

    def __init__(
        self,
        *,
        request: Periodic3DRank2BandEquivalenceHoppingLocalityRequest,
        result: BandEquivalenceHoppingLocalityDiagnostics,
    ) -> None:
        if type(request) is not Periodic3DRank2BandEquivalenceHoppingLocalityRequest:
            raise TypeError(
                "request must be Periodic3DRank2BandEquivalenceHoppingLocalityRequest"
            )
        super().__init__(request=request, result=result)


type _DiagnosticVerifier = (
    Periodic3DRank2BandEquivalenceHoppingLocalityDiagnosticVerifier
)
type _ShellPowerAnalyzer = (
    Periodic3DRank2BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer
)


class Periodic3DRank2BandEquivalenceHoppingLocalityResultVerifier(
    BandEquivalenceHoppingLocalityResultVerifier,
    Periodic3DRank2BandEquivalenceHoppingLocalityAction,
):
    """Authenticate periodic-3D result bytes through qualified independent routes."""

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
            Periodic3DRank2BandEquivalenceHoppingLocalityCalculationResult.from_json(
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
        Periodic3DRank2BandEquivalenceHoppingLocalityVisualizationData,
    ]:
        """Return verification with a periodic-3D visualization projection."""
        result = super().result()
        visualization_data = (
            Periodic3DRank2BandEquivalenceHoppingLocalityVisualizationData.from_dict(
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
        Periodic3DRank2BandEquivalenceHoppingLocalityVisualizationData,
    ]:
        """Admit stored evidence through the periodic-3D typed projection."""
        qualified_visualization_data = (
            Periodic3DRank2BandEquivalenceHoppingLocalityVisualizationData.from_dict(
                visualization_data.to_dict()
            )
        )
        admitted = super().admit_stored(
            verification=verification,
            visualization_data=qualified_visualization_data,
        )
        if not isinstance(
            admitted.visualization_data,
            Periodic3DRank2BandEquivalenceHoppingLocalityVisualizationData,
        ):
            raise TypeError("admitted visualization data lost periodic-3D ownership")
        return ModelAnalysisVerificationResult(
            verification=admitted.verification,
            visualization_data=admitted.visualization_data,
        )


__all__ = [
    "Periodic3DRank2BandEquivalenceHoppingLocalityDiagnosticVerifier",
    "Periodic3DRank2BandEquivalenceHoppingLocalityResultVerifier",
]
