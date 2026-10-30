"""Aggregate immutable result for one higher-rank alignment calculation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ._record_admission import _mapping_value, _tuple_of_mappings
from .calculation import Periodic1DHigherRankAlignmentCalculationRequest
from .definition import (
    Periodic1DHigherRankAlignmentStatus,
)
from .diagnostics import Periodic1DHigherRankProcrustesDiagnostics
from .gauge_alignment.definition import Periodic1DHigherRankGaugeAlignment
from .gauge_alignment.results import Periodic1DHigherRankMeshCalculationResult
from .provenance import Periodic1DHigherRankEvaluationIndependenceResult
from .refinement_results import (
    Periodic1DHigherRankBlockRefinementResult,
    Periodic1DHigherRankScalarRefinementResult,
)
from .scalar_diagnostics import (
    Periodic1DHigherRankScalarDiagnosticInventoryExtractor,
)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DHigherRankAlignmentCalculationResult(BaseTypedRecord):
    """Retain one complete request-bound rank/depth calculation."""

    request: Periodic1DHigherRankAlignmentCalculationRequest
    global_selection: Periodic1DHigherRankProcrustesDiagnostics
    meshes: tuple[Periodic1DHigherRankMeshCalculationResult, ...]
    evaluation_independence: Periodic1DHigherRankEvaluationIndependenceResult
    block_refinements: tuple[Periodic1DHigherRankBlockRefinementResult, ...]
    scalar_refinements: tuple[Periodic1DHigherRankScalarRefinementResult, ...]

    def __post_init__(self) -> None:
        if type(self.request) is not Periodic1DHigherRankAlignmentCalculationRequest:
            raise TypeError("request must be the exact calculation request")
        if type(self.global_selection) is not Periodic1DHigherRankProcrustesDiagnostics:
            raise TypeError("global_selection must be the exact Procrustes record")
        if (
            self.global_selection.status.gauge_alignment
            is not Periodic1DHigherRankGaugeAlignment.GLOBAL_UNITARY
        ):
            raise ValueError("global_selection must describe global-unitary alignment")
        if (
            self.global_selection.selection_mesh_size
            != self.request.configuration.global_unitary_selection_mesh_size
        ):
            raise ValueError("global selection must use the frozen selection mesh")
        global_status = self.global_selection.status
        if (
            global_status.case_identity != self.request.case_identity
            or global_status.retained_rank != self.request.retained_rank
            or global_status.circuit_depth != self.request.circuit_depth
        ):
            raise ValueError("global selection must match the calculation request")
        if (
            type(self.meshes) is not tuple
            or tuple(item.construction_mesh_size for item in self.meshes)
            != self.request.configuration.construction_mesh_sizes
        ):
            raise ValueError("meshes must match the complete construction inventory")
        for mesh in self.meshes:
            expected_transport_request = self.request.transport_request(
                mesh.construction_mesh_size
            )
            if (
                mesh.transport is not None
                and mesh.transport.request != expected_transport_request
            ):
                raise ValueError("mesh transport must match the calculation request")
            failure = mesh.transport_backend_failure
            if failure is not None and (
                failure.case_identity != self.request.case_identity
                or failure.retained_rank != self.request.retained_rank
                or failure.circuit_depth != self.request.circuit_depth
                or failure.construction_mesh_size != mesh.construction_mesh_size
            ):
                raise ValueError(
                    "mesh transport backend failure must match the calculation request"
                )
            model_diagnostics = mesh.model_diagnostics
            if (
                model_diagnostics.case_identity != self.request.case_identity
                or model_diagnostics.retained_rank != self.request.retained_rank
                or model_diagnostics.circuit_depth != self.request.circuit_depth
                or model_diagnostics.construction_mesh_size
                != mesh.construction_mesh_size
            ):
                raise ValueError("model diagnostics must match the calculation request")
            statuses = (
                mesh.pointwise_selection.status,
                *(
                    gauge_alignment.status
                    for gauge_alignment in mesh.gauge_alignment_results
                ),
            )
            if any(
                status.case_identity != self.request.case_identity
                or status.retained_rank != self.request.retained_rank
                or status.circuit_depth != self.request.circuit_depth
                for status in statuses
            ):
                raise ValueError("mesh status must match the calculation request")
        if (
            type(self.evaluation_independence)
            is not Periodic1DHigherRankEvaluationIndependenceResult
        ):
            raise TypeError(
                "evaluation_independence must be the exact provenance record"
            )
        if (
            self.evaluation_independence.construction_mesh_sizes
            != self.request.configuration.construction_mesh_sizes
            or self.evaluation_independence.evaluation_mesh_size
            != self.request.configuration.evaluation_mesh_size
        ):
            raise ValueError(
                "evaluation-independence provenance must match the request"
            )
        if type(self.block_refinements) is not tuple or any(
            type(item) is not Periodic1DHigherRankBlockRefinementResult
            for item in self.block_refinements
        ):
            raise TypeError("block_refinements must contain exact refinement records")
        expected_pairs = tuple(
            zip(
                self.request.configuration.construction_mesh_sizes[:-1],
                self.request.configuration.construction_mesh_sizes[1:],
                strict=True,
            )
        )
        expected_keys = tuple(
            (gauge_alignment, coarse, fine)
            for gauge_alignment in self.request.configuration.gauge_alignments
            for coarse, fine in expected_pairs
            if all(
                next(
                    result
                    for result in mesh.gauge_alignment_results
                    if result.status.gauge_alignment is gauge_alignment
                ).status.status
                is Periodic1DHigherRankAlignmentStatus.QUALIFIED
                for mesh in self.meshes
                if mesh.construction_mesh_size in (coarse, fine)
            )
        )
        actual_keys = tuple(
            (item.gauge_alignment, item.coarse_mesh_size, item.fine_mesh_size)
            for item in self.block_refinements
        )
        if actual_keys != expected_keys:
            raise ValueError(
                "block_refinements must match all qualified adjacent mesh pairs"
            )
        meshes_by_size = {mesh.construction_mesh_size: mesh for mesh in self.meshes}
        for refinement in self.block_refinements:
            coarse_gauge_alignment_result = next(
                result
                for result in meshes_by_size[
                    refinement.coarse_mesh_size
                ].gauge_alignment_results
                if result.status.gauge_alignment is refinement.gauge_alignment
            )
            fine_gauge_alignment_result = next(
                result
                for result in meshes_by_size[
                    refinement.fine_mesh_size
                ].gauge_alignment_results
                if result.status.gauge_alignment is refinement.gauge_alignment
            )
            if (
                not np.array_equal(
                    refinement.translations,
                    coarse_gauge_alignment_result.coefficient_translations,
                )
                or not np.array_equal(
                    refinement.translations,
                    fine_gauge_alignment_result.coefficient_translations,
                )
                or not np.array_equal(
                    refinement.coarse_normalized_block_norms,
                    coarse_gauge_alignment_result.block_normalized_frobenius_norms,
                )
                or not np.array_equal(
                    refinement.fine_normalized_block_norms,
                    fine_gauge_alignment_result.block_normalized_frobenius_norms,
                )
            ):
                raise ValueError(
                    "block refinement values must match their source alignments"
                )
        if type(self.scalar_refinements) is not tuple or any(
            type(item) is not Periodic1DHigherRankScalarRefinementResult
            for item in self.scalar_refinements
        ):
            raise TypeError(
                "scalar_refinements must contain exact scalar refinement records"
            )
        scalar_keys = tuple(
            (item.gauge_alignment, item.diagnostic_path)
            for item in self.scalar_refinements
        )
        if len(set(scalar_keys)) != len(scalar_keys):
            raise ValueError("scalar refinement alignment/path keys must be unique")
        coarse_size, fine_size = self.request.configuration.construction_mesh_sizes[-2:]
        final_meshes = {
            mesh.construction_mesh_size: mesh
            for mesh in self.meshes
            if mesh.construction_mesh_size in (coarse_size, fine_size)
        }
        expected_scalar_gauge_alignments = tuple(
            gauge_alignment
            for gauge_alignment in self.request.configuration.gauge_alignments
            if all(
                next(
                    result
                    for result in final_meshes[size].gauge_alignment_results
                    if result.status.gauge_alignment is gauge_alignment
                ).status.status
                is Periodic1DHigherRankAlignmentStatus.QUALIFIED
                for size in (coarse_size, fine_size)
            )
        )
        if tuple(
            dict.fromkeys(item.gauge_alignment for item in self.scalar_refinements)
        ) != (expected_scalar_gauge_alignments):
            raise ValueError(
                "scalar refinements must cover every qualified final-mesh alignment"
            )
        expected_scalar_values: list[
            tuple[Periodic1DHigherRankGaugeAlignment, str, float, float]
        ] = []
        for gauge_alignment in expected_scalar_gauge_alignments:
            coarse_gauge_alignment_result = next(
                result
                for result in final_meshes[coarse_size].gauge_alignment_results
                if result.status.gauge_alignment is gauge_alignment
            )
            fine_gauge_alignment_result = next(
                result
                for result in final_meshes[fine_size].gauge_alignment_results
                if result.status.gauge_alignment is gauge_alignment
            )
            coarse_inventory = Periodic1DHigherRankScalarDiagnosticInventoryExtractor(
                coarse_gauge_alignment_result
            ).execute()
            fine_inventory = Periodic1DHigherRankScalarDiagnosticInventoryExtractor(
                fine_gauge_alignment_result
            ).execute()
            if tuple(path for path, _ in coarse_inventory) != tuple(
                path for path, _ in fine_inventory
            ):
                raise ValueError("final scalar source inventories must agree")
            expected_scalar_values.extend(
                (gauge_alignment, coarse_item[0], coarse_item[1], fine_item[1])
                for coarse_item, fine_item in zip(
                    coarse_inventory, fine_inventory, strict=True
                )
            )
        actual_scalar_values = [
            (
                item.gauge_alignment,
                item.diagnostic_path,
                item.coarse_value,
                item.fine_value,
            )
            for item in self.scalar_refinements
        ]
        if actual_scalar_values != expected_scalar_values:
            raise ValueError(
                "scalar refinement values must match their source alignments"
            )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "request": self.request,
            "global_selection": self.global_selection,
            "meshes": self.meshes,
            "evaluation_independence": self.evaluation_independence,
            "block_refinements": self.block_refinements,
            "scalar_refinements": self.scalar_refinements,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "request",
            "global_selection",
            "meshes",
            "evaluation_independence",
            "block_refinements",
            "scalar_refinements",
        }:
            raise ValueError("calculation result fields do not match")
        return cls(
            request=Periodic1DHigherRankAlignmentCalculationRequest.from_dict(
                _mapping_value(values["request"], "request")
            ),
            global_selection=Periodic1DHigherRankProcrustesDiagnostics.from_dict(
                _mapping_value(values["global_selection"], "global_selection")
            ),
            meshes=tuple(
                Periodic1DHigherRankMeshCalculationResult.from_dict(item)
                for item in _tuple_of_mappings(values["meshes"], "meshes")
            ),
            evaluation_independence=(
                Periodic1DHigherRankEvaluationIndependenceResult.from_dict(
                    _mapping_value(
                        values["evaluation_independence"],
                        "evaluation_independence",
                    )
                )
            ),
            block_refinements=tuple(
                Periodic1DHigherRankBlockRefinementResult.from_dict(item)
                for item in _tuple_of_mappings(
                    values["block_refinements"], "block_refinements"
                )
            ),
            scalar_refinements=tuple(
                Periodic1DHigherRankScalarRefinementResult.from_dict(item)
                for item in _tuple_of_mappings(
                    values["scalar_refinements"], "scalar_refinements"
                )
            ),
        )
