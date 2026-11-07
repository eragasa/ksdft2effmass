"""Request-bound typed result for band-equivalence locality calculations."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue
from ksdft2effmass.solidstate.reciprocal_sewing import (
    IdentityReciprocalSewing,
    ReciprocalEndpointSewingInventory,
)

from .analysis import BandEquivalenceHoppingLocalityAnalysis
from .definitions import BandEquivalenceHoppingLocalityRequest
from .records import BandEquivalenceHoppingLocalityDiagnostics, CaseDiagnostic


@dataclass(frozen=True, slots=True)
class BandEquivalenceHoppingLocalityCalculationResult(BaseTypedRecord):
    """Retain one complete calculation with its exact scientific request."""

    request: BandEquivalenceHoppingLocalityRequest
    diagnostics: BandEquivalenceHoppingLocalityDiagnostics

    def __post_init__(self) -> None:
        if not isinstance(self.request, BandEquivalenceHoppingLocalityRequest):
            raise TypeError("request must be BandEquivalenceHoppingLocalityRequest")
        if type(self.diagnostics) is not BandEquivalenceHoppingLocalityDiagnostics:
            raise TypeError(
                "diagnostics must be BandEquivalenceHoppingLocalityDiagnostics"
            )
        if self.diagnostics.family is not self.request.family:
            raise ValueError("diagnostics family must match the request")
        if (
            self.diagnostics.construction_size != self.request.construction_size
            or self.diagnostics.evaluation_size != self.request.evaluation_size
        ):
            raise ValueError("diagnostic mesh sizes must match the request")
        if tuple(case.name for case in self.diagnostics.cases) != tuple(
            case.name for case in self.request.cases
        ):
            raise ValueError("diagnostic case inventory must match the request")
        expected_points = tuple(
            (parent_scale, amplitude)
            for parent_scale in self.request.parent_scales
            for amplitude in self.request.amplitudes
        )
        for case in self.diagnostics.cases:
            actual_points = tuple(
                (point.parent_scale, point.amplitude) for point in case.points
            )
            if actual_points != expected_points:
                raise ValueError("diagnostic point controls must match the request")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"request": self.request, "diagnostics": self.diagnostics}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"request", "diagnostics"}:
            raise ValueError("band-equivalence calculation-result fields do not match")
        request = values["request"]
        diagnostics = values["diagnostics"]
        if not isinstance(request, Mapping) or not isinstance(diagnostics, Mapping):
            raise TypeError("calculation-result values must decode to mappings")
        return cls(
            request=BandEquivalenceHoppingLocalityRequest.from_dict(request),
            diagnostics=BandEquivalenceHoppingLocalityDiagnostics.from_dict(
                diagnostics
            ),
        )


@dataclass(frozen=True, slots=True)
class SewnBandEquivalenceResult(BaseTypedRecord):
    """Retain a calculation together with its exact ordered sewing maps."""

    calculation: BandEquivalenceHoppingLocalityCalculationResult
    endpoint_sewing: ReciprocalEndpointSewingInventory

    def __post_init__(self) -> None:
        if not isinstance(
            self.calculation,
            BandEquivalenceHoppingLocalityCalculationResult,
        ):
            raise TypeError(
                "calculation must be BandEquivalenceHoppingLocalityCalculationResult"
            )
        if type(self.endpoint_sewing) is not ReciprocalEndpointSewingInventory:
            raise TypeError("endpoint_sewing must be ReciprocalEndpointSewingInventory")
        request = self.calculation.request
        if self.endpoint_sewing.spatial_dimension != request.dimension:
            raise ValueError("endpoint sewing must match the request dimension")
        ambient_dimension = int(
            request.synthetic_model.retained_seed.magnitude.shape[0]
        )
        if self.endpoint_sewing.ambient_dimension != ambient_dimension:
            raise ValueError("endpoint sewing must match the parent ambient dimension")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "calculation": self.calculation,
            "endpoint_sewing": self.endpoint_sewing,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"calculation", "endpoint_sewing"}:
            raise ValueError("sewn band-equivalence result fields do not match")
        calculation = values["calculation"]
        endpoint_sewing = values["endpoint_sewing"]
        if not isinstance(calculation, Mapping) or not isinstance(
            endpoint_sewing, Mapping
        ):
            raise TypeError("sewn result values must decode to mappings")
        return cls(
            calculation=BandEquivalenceHoppingLocalityCalculationResult.from_dict(
                calculation
            ),
            endpoint_sewing=ReciprocalEndpointSewingInventory.from_dict(
                endpoint_sewing
            ),
        )


class BandEquivalenceHoppingLocalityAnalysisRecorder:
    """Project one bound scientific analysis into its retained record graph."""

    __slots__ = ("_analysis",)

    def __init__(self, analysis: BandEquivalenceHoppingLocalityAnalysis) -> None:
        if not isinstance(analysis, BandEquivalenceHoppingLocalityAnalysis):
            raise TypeError("analysis must be BandEquivalenceHoppingLocalityAnalysis")
        self._analysis = analysis

    @property
    def analysis(self) -> BandEquivalenceHoppingLocalityAnalysis:
        """Return the immutable scientific analysis bound to this recorder."""
        return self._analysis

    def result(self) -> BandEquivalenceHoppingLocalityCalculationResult:
        """Return the retained v1 projection without rerunning the analyzer."""
        analysis = self._analysis
        ambient_dimension = analysis.endpoint_sewing.ambient_dimension
        expected_identity = np.eye(ambient_dimension, dtype=np.complex128)
        # Historical v1 result bytes have no sewing field. Keep that wire honest by
        # admitting only the one deterministic named identity construction.
        for endpoint_map in analysis.endpoint_sewing.positive_axis_maps:
            if endpoint_map.identifier != IdentityReciprocalSewing.IDENTIFIER or not (
                np.array_equal(
                    endpoint_map.coefficient_map.magnitude,
                    expected_identity,
                )
            ):
                raise ValueError(
                    "the v1 calculation result records only named identity sewing"
                )
        return _calculation_result_from_analysis(analysis)


class SewnBandEquivalenceRecorder:
    """Project any explicit sewing choice into a self-contained retained result."""

    __slots__ = ("_analysis",)

    def __init__(self, analysis: BandEquivalenceHoppingLocalityAnalysis) -> None:
        if not isinstance(analysis, BandEquivalenceHoppingLocalityAnalysis):
            raise TypeError("analysis must be BandEquivalenceHoppingLocalityAnalysis")
        self._analysis = analysis

    def result(self) -> SewnBandEquivalenceResult:
        """Return the exact calculation and ordered endpoint maps together."""
        analysis = self._analysis
        return SewnBandEquivalenceResult(
            calculation=_calculation_result_from_analysis(analysis),
            endpoint_sewing=analysis.endpoint_sewing,
        )


def _calculation_result_from_analysis(
    analysis: BandEquivalenceHoppingLocalityAnalysis,
) -> BandEquivalenceHoppingLocalityCalculationResult:
    request = analysis.request
    return BandEquivalenceHoppingLocalityCalculationResult(
        request=request,
        diagnostics=BandEquivalenceHoppingLocalityDiagnostics(
            family=request.family,
            status=analysis.status,
            construction_size=request.construction_size,
            evaluation_size=request.evaluation_size,
            cases=tuple(CaseDiagnostic.from_analysis(case) for case in analysis.cases),
        ),
    )


__all__ = [
    "BandEquivalenceHoppingLocalityAnalysisRecorder",
    "BandEquivalenceHoppingLocalityCalculationResult",
    "SewnBandEquivalenceRecorder",
    "SewnBandEquivalenceResult",
]
