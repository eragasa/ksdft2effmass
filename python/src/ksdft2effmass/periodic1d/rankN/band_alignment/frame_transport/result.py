"""Typed closed-loop frame-transport evidence for the higher-rank study."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite, pi
from typing import Self

import numpy as np
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopFrameTransportOutcome,
    ClosedLoopPolarFrameTransportLinkKind,
    ClosedLoopPolarFrameTransportLinkStatus,
    ClosedLoopPolarFrameTransportPrincipalPhaseBranch,
    ClosedLoopPolarFrameTransportStatus,
    EndpointSewingAction,
    FinitePeriodicMeshFrameInventory,
    FrameRotationAction,
)
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.periodic1d.rankN.band_alignment.configuration import (
    Periodic1DRankNAlignmentConfiguration,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ._decoding import _Periodic1DRankNTransportRecordDecoder
from .link import Periodic1DRankNAlignmentTransportLinkResult
from .request import Periodic1DRankNAlignmentTransportRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNAlignmentTransportOwnerResult(BaseTypedRecord):
    """Record one request-matched closed-loop frame-transport calculation.

    Parameters
    ----------
    request
        Immutable selection of configuration, rank, depth, construction mesh, ambient
        basis, retained frame, and endpoint sewing.
    case_identity, retained_rank, circuit_depth, construction_mesh_size
        Values repeated from ``request`` for direct correlation and indexing.
    ambient_dimension
        Built-in integer ambient-space dimension ``2 * retained_rank``.
    ambient_basis_identifier, retained_frame_identifier, endpoint_sewing_identifier
        Nonempty semantic identities repeated from ``request``.
    frame_rotation_action, endpoint_sewing_action, principal_phase_branch
        Right-frame action, left-ambient sewing action, and ``(-pi, pi]`` branch.
    status
        Qualified or rank-deficient transport outcome.
    link_results
        Increasing tuple of exactly ``construction_mesh_size`` link diagnostics.
    deficient_link_indices, unattempted_link_indices
        Exact tuples of zero-based built-in integer route indices.
    ordered_closure_endpoint_mismatch_phases
        Increasing tuple of binary64 phases in radians and in ``(-pi, pi]``, or ``None``
        when transport is rank deficient. Ordering is storage-only, not a band label.
    primitive_last_to_sewn_first_right_unitary
        Unitless immutable rank-by-rank complex matrix mapping the primitive transported
        endpoint to the sewn initial frame.
    sewn_first_to_primitive_last_right_unitary
        Unitless immutable adjoint of the preceding matrix.
    distributed_closure_correction_right_unitary_step
        Unitless immutable rank-by-rank complex matrix whose ``M``-th power is the
        primitive-last-to-sewn-first transformation.
    maximum_absolute_entry_closure_alignment_residual
        Finite nonnegative unitless binary64 backend-validation residual.
    maximum_absolute_entry_closure_alignment_unitarity_defect
        Finite nonnegative unitless binary64 backend unitarity residual.
    svd_backend_identifier, svd_backend_version
        Nonempty numerical-backend metadata.
    schur_backend_identifier, schur_backend_version
        Nonempty metadata for qualified closure decomposition; ``None`` for deficient
        transport.

    Notes
    -----
    Maximum-entry residuals are backend checks, not normalized-Frobenius scientific
    diagnostics. Python integers do not overflow and are bounded by frozen inventories.
    Nonfinite phases, residuals, and matrix entries are rejected. Matrix arrays are
    copied into immutable byte-backed PhysKit quantities.
    """

    request: Periodic1DRankNAlignmentTransportRequest
    case_identity: str
    retained_rank: int
    circuit_depth: int
    construction_mesh_size: int
    ambient_dimension: int
    ambient_basis_identifier: str
    retained_frame_identifier: str
    endpoint_sewing_identifier: str
    frame_rotation_action: FrameRotationAction
    endpoint_sewing_action: EndpointSewingAction
    principal_phase_branch: ClosedLoopPolarFrameTransportPrincipalPhaseBranch
    status: ClosedLoopPolarFrameTransportStatus
    link_results: tuple[Periodic1DRankNAlignmentTransportLinkResult, ...]
    deficient_link_indices: tuple[int, ...]
    unattempted_link_indices: tuple[int, ...]
    ordered_closure_endpoint_mismatch_phases: tuple[float, ...] | None
    primitive_last_to_sewn_first_right_unitary: ComplexMatrixQuantity | None
    sewn_first_to_primitive_last_right_unitary: ComplexMatrixQuantity | None
    distributed_closure_correction_right_unitary_step: ComplexMatrixQuantity | None
    maximum_absolute_entry_closure_alignment_residual: float | None
    maximum_absolute_entry_closure_alignment_unitarity_defect: float | None
    svd_backend_identifier: str
    svd_backend_version: str
    schur_backend_identifier: str | None
    schur_backend_version: str | None

    def __post_init__(self) -> None:
        """Validate case, route, closure, and status correlations."""
        self._validate_request_and_identity()
        self._validate_actions()
        self._validate_links()
        self._validate_closure_evidence()
        self._validate_status_evidence()

    def _validate_request_and_identity(self) -> None:
        """Validate request correlation, dimensions, identities, and metadata."""
        if type(self.request) is not Periodic1DRankNAlignmentTransportRequest:
            raise TypeError("request must be Periodic1DRankNAlignmentTransportRequest")
        if type(self.case_identity) is not str:
            raise TypeError("case_identity must be a built-in string")
        if not self.case_identity:
            raise ValueError("case_identity must be nonempty")
        if self.case_identity != f"r{self.retained_rank:02d}-L{self.circuit_depth:02d}":
            raise ValueError("case_identity is inconsistent with rank and depth")
        for integer_value, name, allowed in (
            (
                self.retained_rank,
                "retained_rank",
                Periodic1DRankNAlignmentConfiguration.RETAINED_RANKS,
            ),
            (
                self.circuit_depth,
                "circuit_depth",
                Periodic1DRankNAlignmentConfiguration.CIRCUIT_DEPTHS,
            ),
            (
                self.construction_mesh_size,
                "construction_mesh_size",
                Periodic1DRankNAlignmentConfiguration.CONSTRUCTION_MESH_SIZES,
            ),
        ):
            if type(integer_value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if integer_value not in allowed:
                raise ValueError(f"{name} is not in the frozen inventory")
        if (
            self.case_identity != self.request.case_identity
            or self.retained_rank != self.request.retained_rank
            or self.circuit_depth != self.request.circuit_depth
            or self.construction_mesh_size != self.request.construction_mesh_size
        ):
            raise ValueError("transport result case and mesh disagree with its request")
        if type(self.ambient_dimension) is not int:
            raise TypeError("ambient_dimension must be a built-in integer")
        if self.ambient_dimension != 2 * self.retained_rank:
            raise ValueError("ambient_dimension must equal twice the retained rank")
        for text_value, name in (
            (self.ambient_basis_identifier, "ambient_basis_identifier"),
            (self.retained_frame_identifier, "retained_frame_identifier"),
            (self.endpoint_sewing_identifier, "endpoint_sewing_identifier"),
            (self.svd_backend_identifier, "svd_backend_identifier"),
            (self.svd_backend_version, "svd_backend_version"),
        ):
            if type(text_value) is not str:
                raise TypeError(f"{name} must be a built-in string")
            if not text_value:
                raise ValueError(f"{name} must be nonempty")
        if (
            self.ambient_basis_identifier != self.request.ambient_basis_identifier
            or self.retained_frame_identifier != self.request.retained_frame_identifier
            or self.endpoint_sewing_identifier
            != self.request.endpoint_sewing_identifier
        ):
            raise ValueError("transport result identities disagree with its request")
        for optional_text_value, name in (
            (self.schur_backend_identifier, "schur_backend_identifier"),
            (self.schur_backend_version, "schur_backend_version"),
        ):
            if optional_text_value is not None:
                if type(optional_text_value) is not str:
                    raise TypeError(f"{name} must be a built-in string or None")
                if not optional_text_value:
                    raise ValueError(f"{name} must be nonempty when present")

    def _validate_actions(self) -> None:
        """Validate frame, sewing, phase-branch, and status enums."""
        if type(self.frame_rotation_action) is not FrameRotationAction:
            raise TypeError("frame_rotation_action must be FrameRotationAction")
        if self.frame_rotation_action is not FrameRotationAction.RIGHT:
            raise ValueError("frame rotations must act on the right")
        if type(self.endpoint_sewing_action) is not EndpointSewingAction:
            raise TypeError("endpoint_sewing_action must be EndpointSewingAction")
        if self.endpoint_sewing_action is not EndpointSewingAction.LEFT_AMBIENT:
            raise ValueError("endpoint sewing must act on the left ambient space")
        if type(self.principal_phase_branch) is not (
            ClosedLoopPolarFrameTransportPrincipalPhaseBranch
        ):
            raise TypeError("principal_phase_branch must be the exact owner enum")
        if self.principal_phase_branch is not (
            ClosedLoopPolarFrameTransportPrincipalPhaseBranch.negative_pi_open
        ):
            raise ValueError("transport result must use the (-pi, pi] branch")
        if type(self.status) is not ClosedLoopPolarFrameTransportStatus:
            raise TypeError("status must be the exact owner transport status enum")

    def _validate_links(self) -> None:
        """Validate complete ordered link evidence and derived index inventories."""
        if type(self.link_results) is not tuple or any(
            type(result) is not Periodic1DRankNAlignmentTransportLinkResult
            for result in self.link_results
        ):
            raise TypeError("link_results must contain exact transport-link records")
        if len(self.link_results) != self.construction_mesh_size:
            raise ValueError("link_results must contain one result per route link")
        expected_indices = tuple(range(self.construction_mesh_size))
        if tuple(result.index for result in self.link_results) != expected_indices:
            raise ValueError("link_results must use complete increasing route indices")
        if any(
            result.kind is not ClosedLoopPolarFrameTransportLinkKind.NEIGHBOR
            for result in self.link_results[:-1]
        ) or self.link_results[-1].kind is not (
            ClosedLoopPolarFrameTransportLinkKind.CLOSURE
        ):
            raise ValueError("only the final route link may be the closure link")
        for result in self.link_results:
            if result.singular_values is not None and len(result.singular_values) != (
                self.retained_rank
            ):
                raise ValueError("attempted link spectra must match the retained rank")
        if type(self.deficient_link_indices) is not tuple or any(
            type(value) is not int for value in self.deficient_link_indices
        ):
            raise TypeError("deficient_link_indices must be an exact integer tuple")
        if type(self.unattempted_link_indices) is not tuple or any(
            type(value) is not int for value in self.unattempted_link_indices
        ):
            raise TypeError("unattempted_link_indices must be an exact integer tuple")
        expected_deficient = tuple(
            result.index
            for result in self.link_results
            if result.status is ClosedLoopPolarFrameTransportLinkStatus.RANK_DEFICIENT
        )
        expected_unattempted = tuple(
            result.index
            for result in self.link_results
            if result.status is ClosedLoopPolarFrameTransportLinkStatus.UNATTEMPTED
        )
        if self.deficient_link_indices != expected_deficient:
            raise ValueError("deficient_link_indices disagree with link results")
        if self.unattempted_link_indices != expected_unattempted:
            raise ValueError("unattempted_link_indices disagree with link results")

    def _validate_closure_evidence(self) -> None:
        """Validate closure phases, right actions, and numerical residuals."""
        phases = self.ordered_closure_endpoint_mismatch_phases
        if phases is not None:
            if type(phases) is not tuple or any(
                type(value) is not float or not isfinite(value) for value in phases
            ):
                raise TypeError(
                    "closure phases must be an exact tuple of finite floats"
                )
            if len(phases) != self.retained_rank:
                raise ValueError("closure phase count must equal the retained rank")
            if any(not (-pi < value <= pi) for value in phases):
                raise ValueError("closure phases must lie in (-pi, pi]")
            if any(
                left > right for left, right in zip(phases, phases[1:], strict=False)
            ):
                raise ValueError(
                    "closure phases must use deterministic increasing storage"
                )
        closure_right_unitaries = (
            self.primitive_last_to_sewn_first_right_unitary,
            self.sewn_first_to_primitive_last_right_unitary,
            self.distributed_closure_correction_right_unitary_step,
        )
        for matrix in closure_right_unitaries:
            if matrix is None:
                continue
            if type(matrix) is not ComplexMatrixQuantity or not isinstance(
                matrix.unit, Unitless
            ):
                raise TypeError("closure actions must be unitless complex matrices")
            if matrix.magnitude.shape != (self.retained_rank, self.retained_rank):
                raise ValueError("closure actions must match the retained-rank space")
        primitive_to_sewn = self.primitive_last_to_sewn_first_right_unitary
        sewn_to_primitive = self.sewn_first_to_primitive_last_right_unitary
        correction_step = self.distributed_closure_correction_right_unitary_step
        if (
            primitive_to_sewn is not None
            and sewn_to_primitive is not None
            and correction_step is not None
        ):
            if not np.allclose(
                sewn_to_primitive.magnitude,
                primitive_to_sewn.magnitude.conjugate().T,
                rtol=(
                    Periodic1DRankNAlignmentConfiguration.BACKEND_VALIDATION_RELATIVE_TOLERANCE
                ),
                atol=(
                    Periodic1DRankNAlignmentConfiguration.BACKEND_VALIDATION_ABSOLUTE_TOLERANCE
                ),
            ):
                raise ValueError(
                    "sewn-first-to-primitive-last unitary must be the adjoint of "
                    "the primitive-last-to-sewn-first unitary"
                )
            if not np.allclose(
                np.linalg.matrix_power(
                    correction_step.magnitude,
                    self.construction_mesh_size,
                ),
                primitive_to_sewn.magnitude,
                rtol=(
                    Periodic1DRankNAlignmentConfiguration.BACKEND_VALIDATION_RELATIVE_TOLERANCE
                ),
                atol=(
                    Periodic1DRankNAlignmentConfiguration.BACKEND_VALIDATION_ABSOLUTE_TOLERANCE
                ),
            ):
                raise ValueError(
                    "distributed closure-correction step must close to the "
                    "primitive-last-to-sewn-first unitary"
                )
        for optional_float, name in (
            (
                self.maximum_absolute_entry_closure_alignment_residual,
                "maximum_absolute_entry_closure_alignment_residual",
            ),
            (
                self.maximum_absolute_entry_closure_alignment_unitarity_defect,
                "maximum_absolute_entry_closure_alignment_unitarity_defect",
            ),
        ):
            if optional_float is not None:
                if type(optional_float) is not float:
                    raise TypeError(f"{name} must be a built-in float or None")
                if not isfinite(optional_float) or optional_float < 0.0:
                    raise ValueError(f"{name} must be finite and nonnegative")

    def _validate_status_evidence(self) -> None:
        """Validate qualified versus rank-deficient evidence availability."""
        phases = self.ordered_closure_endpoint_mismatch_phases
        closure_right_unitaries = (
            self.primitive_last_to_sewn_first_right_unitary,
            self.sewn_first_to_primitive_last_right_unitary,
            self.distributed_closure_correction_right_unitary_step,
        )
        if self.status is ClosedLoopPolarFrameTransportStatus.QUALIFIED:
            if any(
                result.status is not ClosedLoopPolarFrameTransportLinkStatus.QUALIFIED
                for result in self.link_results
            ):
                raise ValueError("qualified transport requires every link to qualify")
            if phases is None:
                raise ValueError("qualified transport requires closure phases")
            if any(matrix is None for matrix in closure_right_unitaries):
                raise ValueError(
                    "qualified transport requires all three closure right unitaries"
                )
            if (
                self.maximum_absolute_entry_closure_alignment_residual is None
                or self.maximum_absolute_entry_closure_alignment_unitarity_defect
                is None
            ):
                raise ValueError(
                    "qualified transport requires closure validation evidence"
                )
            if (
                self.schur_backend_identifier is None
                or self.schur_backend_version is None
            ):
                raise ValueError("qualified transport requires Schur backend metadata")
            return
        if not self.deficient_link_indices:
            raise ValueError("rank-deficient transport requires a deficient link")
        first_deficient = self.deficient_link_indices[0]
        if self.deficient_link_indices != (first_deficient,):
            raise ValueError("transport stops after the first deficient link")
        expected_unattempted_after = tuple(
            range(first_deficient + 1, self.construction_mesh_size)
        )
        if self.unattempted_link_indices != expected_unattempted_after:
            raise ValueError("links after the first deficiency must be unattempted")
        if any(
            result.status is not ClosedLoopPolarFrameTransportLinkStatus.QUALIFIED
            for result in self.link_results[:first_deficient]
        ):
            raise ValueError("links before the deficiency must be qualified")
        if any(
            value is not None
            for value in (
                phases,
                *closure_right_unitaries,
                self.maximum_absolute_entry_closure_alignment_residual,
                self.maximum_absolute_entry_closure_alignment_unitarity_defect,
                self.schur_backend_identifier,
                self.schur_backend_version,
            )
        ):
            raise ValueError(
                "rank-deficient transport must not claim closure or Schur evidence"
            )

    @classmethod
    def from_owner_outcome(
        cls,
        *,
        request: Periodic1DRankNAlignmentTransportRequest,
        outcome: ClosedLoopFrameTransportOutcome,
    ) -> Self:
        """Record one request-matched PhysKit outcome without mutable aliases."""
        if type(request) is not Periodic1DRankNAlignmentTransportRequest:
            raise TypeError("request must be Periodic1DRankNAlignmentTransportRequest")
        if type(outcome) is not ClosedLoopFrameTransportOutcome:
            raise TypeError("outcome must be ClosedLoopFrameTransportOutcome")
        source = outcome.source
        if type(source) is not FinitePeriodicMeshFrameInventory:
            raise TypeError("outcome source must be FinitePeriodicMeshFrameInventory")
        if source.mesh.dimension != 1:
            raise ValueError("transport source mesh must be one-dimensional")
        if source.mesh.size != request.construction_mesh_size:
            raise ValueError("transport source mesh size disagrees with the request")
        if source.mesh.offsets != (0.0,):
            raise ValueError("transport source must use the unshifted centered mesh")
        if outcome.rank != request.retained_rank:
            raise ValueError("transport outcome rank disagrees with the request")
        if outcome.ambient_dimension != request.ambient_dimension:
            raise ValueError(
                "transport outcome ambient dimension disagrees with the request"
            )
        if (
            outcome.ambient_basis_identifier != request.ambient_basis_identifier
            or outcome.retained_frame_identifier != request.retained_frame_identifier
            or outcome.endpoint_sewing_identifier != request.endpoint_sewing_identifier
        ):
            raise ValueError("transport outcome identities disagree with the request")
        configuration = request.configuration
        if outcome.frame_rotation_action is not configuration.frame_rotation_action:
            raise ValueError("transport frame action disagrees with the configuration")
        if outcome.endpoint_sewing_action is not configuration.endpoint_sewing_action:
            raise ValueError("transport sewing action disagrees with the configuration")
        if outcome.principal_phase_branch is not configuration.principal_phase_branch:
            raise ValueError("transport phase branch disagrees with the configuration")
        if outcome.tolerance != configuration.owner_transport_tolerance():
            raise ValueError("transport tolerance disagrees with the configuration")
        canonical_closure_matrices: dict[str, ComplexMatrixQuantity | None] = {}
        for name, matrix in (
            (
                "primitive_last_to_sewn_first_right_unitary",
                outcome.closure_alignment_right_action,
            ),
            (
                "sewn_first_to_primitive_last_right_unitary",
                outcome.closure_endpoint_mismatch,
            ),
            (
                "distributed_closure_correction_right_unitary_step",
                outcome.distributed_closure_correction_step,
            ),
        ):
            if matrix is None:
                canonical_closure_matrices[name] = None
                continue
            normalized = np.array(matrix, dtype=np.complex128, copy=True)
            normalized.real[normalized.real == 0.0] = 0.0
            normalized.imag[normalized.imag == 0.0] = 0.0
            canonical_closure_matrices[name] = ComplexMatrixQuantity(
                normalized,
                Unitless(),
            )
        return cls(
            request=request,
            case_identity=request.case_identity,
            retained_rank=request.retained_rank,
            circuit_depth=request.circuit_depth,
            construction_mesh_size=outcome.point_count,
            ambient_dimension=outcome.ambient_dimension,
            ambient_basis_identifier=outcome.ambient_basis_identifier,
            retained_frame_identifier=outcome.retained_frame_identifier,
            endpoint_sewing_identifier=outcome.endpoint_sewing_identifier,
            frame_rotation_action=outcome.frame_rotation_action,
            endpoint_sewing_action=outcome.endpoint_sewing_action,
            principal_phase_branch=outcome.principal_phase_branch,
            status=outcome.status,
            link_results=tuple(
                Periodic1DRankNAlignmentTransportLinkResult.from_owner_diagnostic(
                    diagnostic
                )
                for diagnostic in outcome.link_diagnostics
            ),
            deficient_link_indices=outcome.deficient_link_indices,
            unattempted_link_indices=outcome.unattempted_link_indices,
            ordered_closure_endpoint_mismatch_phases=(
                outcome.ordered_closure_endpoint_mismatch_phases
            ),
            primitive_last_to_sewn_first_right_unitary=(
                canonical_closure_matrices["primitive_last_to_sewn_first_right_unitary"]
            ),
            sewn_first_to_primitive_last_right_unitary=(
                canonical_closure_matrices["sewn_first_to_primitive_last_right_unitary"]
            ),
            distributed_closure_correction_right_unitary_step=(
                canonical_closure_matrices[
                    "distributed_closure_correction_right_unitary_step"
                ]
            ),
            maximum_absolute_entry_closure_alignment_residual=(
                outcome.maximum_absolute_entry_closure_alignment_residual
            ),
            maximum_absolute_entry_closure_alignment_unitarity_defect=(
                outcome.maximum_absolute_entry_closure_alignment_unitarity_defect
            ),
            svd_backend_identifier=outcome.svd_backend_identifier,
            svd_backend_version=outcome.svd_backend_version,
            schur_backend_identifier=outcome.schur_backend_identifier,
            schur_backend_version=outcome.schur_backend_version,
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "request": self.request,
            "case_identity": self.case_identity,
            "retained_rank": self.retained_rank,
            "circuit_depth": self.circuit_depth,
            "construction_mesh_size": self.construction_mesh_size,
            "ambient_dimension": self.ambient_dimension,
            "ambient_basis_identifier": self.ambient_basis_identifier,
            "retained_frame_identifier": self.retained_frame_identifier,
            "endpoint_sewing_identifier": self.endpoint_sewing_identifier,
            "frame_rotation_action": self.frame_rotation_action.value,
            "endpoint_sewing_action": self.endpoint_sewing_action.value,
            "principal_phase_branch": self.principal_phase_branch.value,
            "status": self.status.value,
            "link_results": self.link_results,
            "deficient_link_indices": self.deficient_link_indices,
            "unattempted_link_indices": self.unattempted_link_indices,
            "ordered_closure_endpoint_mismatch_phases": (
                self.ordered_closure_endpoint_mismatch_phases
            ),
            "primitive_last_to_sewn_first_right_unitary": (
                self.primitive_last_to_sewn_first_right_unitary
            ),
            "sewn_first_to_primitive_last_right_unitary": (
                self.sewn_first_to_primitive_last_right_unitary
            ),
            "distributed_closure_correction_right_unitary_step": (
                self.distributed_closure_correction_right_unitary_step
            ),
            "maximum_absolute_entry_closure_alignment_residual": (
                self.maximum_absolute_entry_closure_alignment_residual
            ),
            "maximum_absolute_entry_closure_alignment_unitarity_defect": (
                self.maximum_absolute_entry_closure_alignment_unitarity_defect
            ),
            "svd_backend_identifier": self.svd_backend_identifier,
            "svd_backend_version": self.svd_backend_version,
            "schur_backend_identifier": self.schur_backend_identifier,
            "schur_backend_version": self.schur_backend_version,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "request",
            "case_identity",
            "retained_rank",
            "circuit_depth",
            "construction_mesh_size",
            "ambient_dimension",
            "ambient_basis_identifier",
            "retained_frame_identifier",
            "endpoint_sewing_identifier",
            "frame_rotation_action",
            "endpoint_sewing_action",
            "principal_phase_branch",
            "status",
            "link_results",
            "deficient_link_indices",
            "unattempted_link_indices",
            "ordered_closure_endpoint_mismatch_phases",
            "primitive_last_to_sewn_first_right_unitary",
            "sewn_first_to_primitive_last_right_unitary",
            "distributed_closure_correction_right_unitary_step",
            "maximum_absolute_entry_closure_alignment_residual",
            "maximum_absolute_entry_closure_alignment_unitarity_defect",
            "svd_backend_identifier",
            "svd_backend_version",
            "schur_backend_identifier",
            "schur_backend_version",
        }
        if set(values) != required:
            raise ValueError("transport owner result fields do not match")
        decoder = _Periodic1DRankNTransportRecordDecoder(values)

        request_value = values["request"]
        if not isinstance(request_value, Mapping):
            raise TypeError("request must decode to a mapping")
        request = Periodic1DRankNAlignmentTransportRequest.from_dict(request_value)

        string_names = (
            "case_identity",
            "ambient_basis_identifier",
            "retained_frame_identifier",
            "endpoint_sewing_identifier",
            "frame_rotation_action",
            "endpoint_sewing_action",
            "principal_phase_branch",
            "status",
            "svd_backend_identifier",
            "svd_backend_version",
        )
        strings: dict[str, str] = {}
        for name in string_names:
            string_value = values[name]
            if type(string_value) is not str:
                raise TypeError(f"{name} must decode to a string")
            strings[name] = string_value
        integer_names = (
            "retained_rank",
            "circuit_depth",
            "construction_mesh_size",
            "ambient_dimension",
        )
        integers: dict[str, int] = {}
        for name in integer_names:
            integer_value = values[name]
            if type(integer_value) is not int:
                raise TypeError(f"{name} must decode to a built-in integer")
            integers[name] = integer_value

        link_results_value = values["link_results"]
        deficient_indices = decoder.integer_tuple("deficient_link_indices")
        unattempted_indices = decoder.integer_tuple("unattempted_link_indices")
        phases = decoder.optional_float_tuple(
            "ordered_closure_endpoint_mismatch_phases"
        )
        if not isinstance(link_results_value, tuple):
            raise TypeError("link_results must decode to a tuple")
        decoded_links: list[Periodic1DRankNAlignmentTransportLinkResult] = []
        for link_value in link_results_value:
            if type(link_value) is Periodic1DRankNAlignmentTransportLinkResult:
                decoded_links.append(link_value)
            elif isinstance(link_value, Mapping):
                decoded_links.append(
                    Periodic1DRankNAlignmentTransportLinkResult.from_dict(link_value)
                )
            else:
                raise TypeError("link_results entries must decode to mappings")
        link_results = tuple(decoded_links)

        primitive_last_to_sewn_first_right_unitary = decoder.optional_complex_matrix(
            "primitive_last_to_sewn_first_right_unitary"
        )
        sewn_first_to_primitive_last_right_unitary = decoder.optional_complex_matrix(
            "sewn_first_to_primitive_last_right_unitary"
        )
        distributed_closure_correction_right_unitary_step = (
            decoder.optional_complex_matrix(
                "distributed_closure_correction_right_unitary_step"
            )
        )
        closure_residual = decoder.optional_float(
            "maximum_absolute_entry_closure_alignment_residual"
        )
        closure_unitarity = decoder.optional_float(
            "maximum_absolute_entry_closure_alignment_unitarity_defect"
        )
        schur_identifier = decoder.optional_text("schur_backend_identifier")
        schur_version = decoder.optional_text("schur_backend_version")

        return cls(
            request=request,
            case_identity=strings["case_identity"],
            retained_rank=integers["retained_rank"],
            circuit_depth=integers["circuit_depth"],
            construction_mesh_size=integers["construction_mesh_size"],
            ambient_dimension=integers["ambient_dimension"],
            ambient_basis_identifier=strings["ambient_basis_identifier"],
            retained_frame_identifier=strings["retained_frame_identifier"],
            endpoint_sewing_identifier=strings["endpoint_sewing_identifier"],
            frame_rotation_action=FrameRotationAction(strings["frame_rotation_action"]),
            endpoint_sewing_action=EndpointSewingAction(
                strings["endpoint_sewing_action"]
            ),
            principal_phase_branch=(
                ClosedLoopPolarFrameTransportPrincipalPhaseBranch(
                    strings["principal_phase_branch"]
                )
            ),
            status=ClosedLoopPolarFrameTransportStatus(strings["status"]),
            link_results=link_results,
            deficient_link_indices=deficient_indices,
            unattempted_link_indices=unattempted_indices,
            ordered_closure_endpoint_mismatch_phases=phases,
            primitive_last_to_sewn_first_right_unitary=(
                primitive_last_to_sewn_first_right_unitary
            ),
            sewn_first_to_primitive_last_right_unitary=(
                sewn_first_to_primitive_last_right_unitary
            ),
            distributed_closure_correction_right_unitary_step=(
                distributed_closure_correction_right_unitary_step
            ),
            maximum_absolute_entry_closure_alignment_residual=closure_residual,
            maximum_absolute_entry_closure_alignment_unitarity_defect=(
                closure_unitarity
            ),
            svd_backend_identifier=strings["svd_backend_identifier"],
            svd_backend_version=strings["svd_backend_version"],
            schur_backend_identifier=schur_identifier,
            schur_backend_version=schur_version,
        )


__all__ = [
    "Periodic1DRankNAlignmentTransportOwnerResult",
]
