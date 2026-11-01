"""Typed frame-transport analysis for one rank-N construction mesh."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import final

import numpy as np
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransportBackendFailure,
    ClosedLoopPolarFrameTransporter,
    FinitePeriodicMeshFrameInventory,
)

from ksdft2effmass.periodic1d.rankN.band_alignment.calculation import (
    Periodic1DRankNAlignmentCalculationRequest,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.mesh_sample import (
    Periodic1DRankNAnalyticMeshSample,
)

from .failure import Periodic1DRankNAlignmentTransportBackendFailureResult
from .result import Periodic1DRankNAlignmentTransportOwnerResult


@dataclass(frozen=True, slots=True)
class Periodic1DRankNTransportAnalysisRequest:
    """Bind one calculation request to one immutable construction-mesh sample."""

    calculation_request: Periodic1DRankNAlignmentCalculationRequest
    sample: Periodic1DRankNAnalyticMeshSample

    def __post_init__(self) -> None:
        if (
            type(self.calculation_request)
            is not Periodic1DRankNAlignmentCalculationRequest
        ):
            raise TypeError("calculation_request must be the exact rank-N request")
        if type(self.sample) is not Periodic1DRankNAnalyticMeshSample:
            raise TypeError("sample must be the exact analytic mesh sample")
        request = self.calculation_request
        model = self.sample.model
        if (
            model.retained_rank != request.retained_rank
            or model.circuit_depth != request.circuit_depth
            or self.sample.construction_mesh_size
            not in request.configuration.construction_mesh_sizes
        ):
            raise ValueError("sample must match the calculation request")


@dataclass(frozen=True, slots=True)
class Periodic1DRankNResolvedTransportAnalysis:
    """Retain successful owner transport evidence and closure defects."""

    transport: Periodic1DRankNAlignmentTransportOwnerResult
    endpoint_closure_defect: float
    primitive_closure_defect: float

    def __post_init__(self) -> None:
        if type(self.transport) is not Periodic1DRankNAlignmentTransportOwnerResult:
            raise TypeError("transport must be the exact owner result")
        for value, name in (
            (self.endpoint_closure_defect, "endpoint_closure_defect"),
            (self.primitive_closure_defect, "primitive_closure_defect"),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DRankNFailedTransportAnalysis:
    """Retain one bounded backend failure without fabricated closure values."""

    failure: Periodic1DRankNAlignmentTransportBackendFailureResult

    def __post_init__(self) -> None:
        if (
            type(self.failure)
            is not Periodic1DRankNAlignmentTransportBackendFailureResult
        ):
            raise TypeError("failure must be the exact transport failure result")


type Periodic1DRankNTransportAnalysis = (
    Periodic1DRankNResolvedTransportAnalysis | Periodic1DRankNFailedTransportAnalysis
)


@final
class Periodic1DRankNTransportAnalyzer:
    """Adapt one PhysKit closed-loop transport into typed retained evidence."""

    __slots__ = ("_request", "_transporter")

    def __init__(
        self,
        request: Periodic1DRankNTransportAnalysisRequest,
        transporter: ClosedLoopPolarFrameTransporter,
    ) -> None:
        if type(request) is not Periodic1DRankNTransportAnalysisRequest:
            raise TypeError("request must be the exact transport-analysis request")
        if type(transporter) is not ClosedLoopPolarFrameTransporter:
            raise TypeError("transporter must be the canonical frame transporter")
        self._request = request
        self._transporter = transporter

    @property
    def request(self) -> Periodic1DRankNTransportAnalysisRequest:
        """Return the immutable transport-analysis request."""
        return self._request

    def execute(self) -> Periodic1DRankNTransportAnalysis:
        """Return resolved transport evidence or a typed bounded failure."""
        analysis_request = self._request
        calculation_request = analysis_request.calculation_request
        sample = analysis_request.sample
        model = sample.model
        mesh_size = sample.construction_mesh_size
        source = FinitePeriodicMeshFrameInventory.from_arrays(
            mesh=sample.mesh,
            frames=sample.reference_frames,
            endpoint_sewing_map=model.endpoint_sewing_map,
            ambient_basis_identifier=calculation_request.ambient_basis_identifier,
            retained_frame_identifier=calculation_request.retained_frame_identifier,
            endpoint_sewing_identifier=calculation_request.endpoint_sewing_identifier,
            principal_phase_branch=(
                calculation_request.configuration.principal_phase_branch
            ),
            tolerance=calculation_request.configuration.owner_transport_tolerance(),
        )
        try:
            outcome = self._transporter.transport(source)
        except ClosedLoopPolarFrameTransportBackendFailure as failure:
            failure_result_type = Periodic1DRankNAlignmentTransportBackendFailureResult
            return Periodic1DRankNFailedTransportAnalysis(
                failure=failure_result_type.from_owner_failure(
                    case_identity=calculation_request.case_identity,
                    retained_rank=calculation_request.retained_rank,
                    circuit_depth=calculation_request.circuit_depth,
                    construction_mesh_size=mesh_size,
                    failure=failure,
                )
            )
        transport = Periodic1DRankNAlignmentTransportOwnerResult.from_owner_outcome(
            request=calculation_request.transport_request(mesh_size),
            outcome=outcome,
        )
        if (
            outcome.transported_frames is None
            or outcome.closure_alignment_right_action is None
        ):
            raise ValueError("analytic reference transport must remain full rank")
        transported = outcome.transported_frames
        endpoint_defect = float(
            np.linalg.norm(transported[-1] - model.endpoint_sewing_map @ transported[0])
            / math.sqrt(model.retained_rank)
        )
        primitive_defect = float(
            np.linalg.norm(
                transported[-1] @ outcome.closure_alignment_right_action
                - model.endpoint_sewing_map @ transported[0]
            )
            / math.sqrt(model.retained_rank)
        )
        return Periodic1DRankNResolvedTransportAnalysis(
            transport=transport,
            endpoint_closure_defect=endpoint_defect,
            primitive_closure_defect=primitive_defect,
        )


__all__ = [
    "Periodic1DRankNFailedTransportAnalysis",
    "Periodic1DRankNResolvedTransportAnalysis",
    "Periodic1DRankNTransportAnalysis",
    "Periodic1DRankNTransportAnalysisRequest",
    "Periodic1DRankNTransportAnalyzer",
]
