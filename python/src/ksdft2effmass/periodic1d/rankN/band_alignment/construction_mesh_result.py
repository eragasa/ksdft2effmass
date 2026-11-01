"""Immutable aggregate results for one construction mesh."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.periodic1d.rankN._record_admission import (
    _decoded_optional_float,
    _finite_nonnegative,
    _mapping_value,
    _tuple_of_mappings,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.configuration import (
    Periodic1DRankNAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.procrustes.result import (
    Periodic1DRankNProcrustesDiagnostics,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .frame_transport.failure import (
    Periodic1DRankNAlignmentTransportBackendFailureResult,
)
from .frame_transport.result import Periodic1DRankNAlignmentTransportOwnerResult
from .gauge_case_result import Periodic1DRankNGaugeAlignmentMeshResult
from .model_diagnostics import Periodic1DRankNModelDiagnostics


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNMeshCalculationResult(BaseTypedRecord):
    """Retain one construction-mesh calculation with common transport evidence."""

    construction_mesh_size: int
    model_diagnostics: Periodic1DRankNModelDiagnostics
    transport: Periodic1DRankNAlignmentTransportOwnerResult | None
    transport_backend_failure: (
        Periodic1DRankNAlignmentTransportBackendFailureResult | None
    )
    endpoint_closure_defect: float | None
    primitive_closure_defect: float | None
    pointwise_selection: Periodic1DRankNProcrustesDiagnostics
    gauge_alignment_results: tuple[Periodic1DRankNGaugeAlignmentMeshResult, ...]

    def __post_init__(self) -> None:
        if (
            type(self.construction_mesh_size) is not int
            or self.construction_mesh_size
            not in Periodic1DRankNAlignmentConfiguration.CONSTRUCTION_MESH_SIZES
        ):
            raise ValueError("construction_mesh_size must be a frozen mesh size")
        if type(self.model_diagnostics) is not Periodic1DRankNModelDiagnostics:
            raise TypeError(
                "model_diagnostics must be the exact model diagnostic record"
            )
        if self.model_diagnostics.construction_mesh_size != self.construction_mesh_size:
            raise ValueError("model diagnostics must match the construction mesh")
        if (self.transport is None) == (self.transport_backend_failure is None):
            raise ValueError(
                "exactly one transport outcome or backend failure is required"
            )
        if self.transport is not None:
            if (
                type(self.transport) is not Periodic1DRankNAlignmentTransportOwnerResult
                or self.transport.construction_mesh_size != self.construction_mesh_size
            ):
                raise ValueError("transport result must match the construction mesh")
            if (
                self.endpoint_closure_defect is None
                or self.primitive_closure_defect is None
            ):
                raise ValueError(
                    "transport outcome requires normalized closure defects"
                )
        else:
            if (
                type(self.transport_backend_failure)
                is not Periodic1DRankNAlignmentTransportBackendFailureResult
            ):
                raise TypeError("transport_backend_failure must be its exact record")
            if (
                self.transport_backend_failure.construction_mesh_size
                != self.construction_mesh_size
            ):
                raise ValueError(
                    "transport backend failure must match the construction mesh"
                )
            if (
                self.endpoint_closure_defect is not None
                or self.primitive_closure_defect is not None
            ):
                raise ValueError("failed transport must not claim closure defects")
        for value, name in (
            (self.endpoint_closure_defect, "endpoint_closure_defect"),
            (self.primitive_closure_defect, "primitive_closure_defect"),
        ):
            if value is not None:
                _finite_nonnegative(value, name)
        if (
            type(self.pointwise_selection) is not Periodic1DRankNProcrustesDiagnostics
            or self.pointwise_selection.selection_mesh_size
            != self.construction_mesh_size
        ):
            raise ValueError("pointwise selection must match this construction mesh")
        if (
            type(self.gauge_alignment_results) is not tuple
            or tuple(
                item.status.gauge_alignment for item in self.gauge_alignment_results
            )
            != Periodic1DRankNAlignmentConfiguration.GAUGE_ALIGNMENTS
        ):
            raise ValueError(
                "gauge_alignment_results must use the frozen scientific order"
            )
        if any(
            item.status.construction_mesh_size != self.construction_mesh_size
            for item in self.gauge_alignment_results
        ):
            raise ValueError(
                "every gauge-alignment status must match the construction mesh"
            )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "construction_mesh_size": self.construction_mesh_size,
            "model_diagnostics": self.model_diagnostics,
            "transport": self.transport,
            "transport_backend_failure": self.transport_backend_failure,
            "endpoint_closure_defect": self.endpoint_closure_defect,
            "primitive_closure_defect": self.primitive_closure_defect,
            "pointwise_selection": self.pointwise_selection,
            "gauge_alignment_results": self.gauge_alignment_results,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "construction_mesh_size",
            "model_diagnostics",
            "transport",
            "transport_backend_failure",
            "endpoint_closure_defect",
            "primitive_closure_defect",
            "pointwise_selection",
            "gauge_alignment_results",
        }:
            raise ValueError("mesh calculation fields do not match")
        mesh = values["construction_mesh_size"]
        if type(mesh) is not int:
            raise TypeError("construction_mesh_size must decode to an integer")
        transport_value = values["transport"]
        failure_value = values["transport_backend_failure"]
        endpoint = values["endpoint_closure_defect"]
        primitive = values["primitive_closure_defect"]
        for value, name in (
            (endpoint, "endpoint_closure_defect"),
            (primitive, "primitive_closure_defect"),
        ):
            if value is not None and type(value) is not float:
                raise TypeError(f"{name} must decode to float or None")
        return cls(
            construction_mesh_size=mesh,
            model_diagnostics=Periodic1DRankNModelDiagnostics.from_dict(
                _mapping_value(values["model_diagnostics"], "model_diagnostics")
            ),
            transport=None
            if transport_value is None
            else Periodic1DRankNAlignmentTransportOwnerResult.from_dict(
                _mapping_value(transport_value, "transport")
            ),
            transport_backend_failure=None
            if failure_value is None
            else Periodic1DRankNAlignmentTransportBackendFailureResult.from_dict(
                _mapping_value(failure_value, "transport_backend_failure")
            ),
            endpoint_closure_defect=_decoded_optional_float(
                endpoint, "endpoint_closure_defect"
            ),
            primitive_closure_defect=_decoded_optional_float(
                primitive, "primitive_closure_defect"
            ),
            pointwise_selection=Periodic1DRankNProcrustesDiagnostics.from_dict(
                _mapping_value(values["pointwise_selection"], "pointwise_selection")
            ),
            gauge_alignment_results=tuple(
                Periodic1DRankNGaugeAlignmentMeshResult.from_dict(item)
                for item in _tuple_of_mappings(
                    values["gauge_alignment_results"], "gauge_alignment_results"
                )
            ),
        )


__all__ = ["Periodic1DRankNMeshCalculationResult"]
