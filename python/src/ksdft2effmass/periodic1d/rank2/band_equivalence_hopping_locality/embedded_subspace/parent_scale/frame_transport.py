"""Qualify the parent and compose PhysKit frame transport."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.optimization.alignment.closed_loop_polar_transport import (
    ClosedLoopPolarFrameTransportLinkDiagnostic,
    ClosedLoopPolarFrameTransportStatus,
)
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopFrameTransportOutcome,
    ClosedLoopPolarFrameTransportBackendFailure,
    ClosedLoopPolarFrameTransporter,
    FinitePeriodicMeshFrameInventory,
)

from .parent_hamiltonian import _Periodic1DRank2Parent
from .request import Periodic1DRank2Request
from .results import (
    Periodic1DRank2BandTransportBackendFailure,
    Periodic1DRank2BandTransportNumericallyUnresolved,
    Periodic1DRank2BandTransportThresholdFailure,
    Periodic1DRank2ExternalGapFailure,
    Periodic1DRank2Qualification,
    Periodic1DRank2QualifiedParent,
)


def _immutable_complex(values: Complex128Array) -> Complex128Array:
    result = np.array(values, dtype=np.complex128, copy=True)
    result.setflags(write=False)
    return result


def _immutable_real(values: Float64Array) -> Float64Array:
    result = np.array(values, dtype=np.float64, copy=True)
    result.setflags(write=False)
    return result


@dataclass(frozen=True, slots=True)
class _Periodic1DRank2TransportDiagnostics:
    minimum_singular_value: float
    maximum_rank_cutoff: float
    maximum_unitarity_defect: float
    maximum_primitive_link_frobenius_residual: float
    closure_phases: tuple[float, ...]
    closure_alignment_residual: float
    closure_alignment_unitarity_defect: float


class _Periodic1DRank2TransportDiagnosticAnalyzer:
    """Derive explicitly named KSD diagnostics from one PhysKit outcome."""

    __slots__ = ("_outcome",)

    def __init__(self, outcome: ClosedLoopFrameTransportOutcome) -> None:
        if type(outcome) is not ClosedLoopFrameTransportOutcome:
            raise TypeError("outcome must be ClosedLoopFrameTransportOutcome")
        self._outcome = outcome

    def execute(self) -> _Periodic1DRank2TransportDiagnostics:
        """Evaluate residuals from owner-produced primitive transported frames."""
        outcome = self._outcome
        transported = outcome.transported_frames
        closure_action = outcome.closure_alignment_right_action
        phases = outcome.ordered_closure_endpoint_mismatch_phases
        schur_vectors = outcome.closure_schur_vectors
        closure_residual = outcome.maximum_absolute_entry_closure_alignment_residual
        closure_unitarity = (
            outcome.maximum_absolute_entry_closure_alignment_unitarity_defect
        )
        if (
            transported is None
            or closure_action is None
            or phases is None
            or schur_vectors is None
            or closure_residual is None
            or closure_unitarity is None
        ):
            raise ValueError("qualified transport must expose complete diagnostics")
        diagnostics = outcome.link_diagnostics
        singular_values = tuple(
            value
            for diagnostic in diagnostics
            for value in (diagnostic.singular_values or ())
        )
        cutoffs = tuple(
            diagnostic.applied_rank_cutoff
            for diagnostic in diagnostics
            if diagnostic.applied_rank_cutoff is not None
        )
        unitarity = tuple(
            diagnostic.maximum_absolute_entry_unitarity_defect
            for diagnostic in diagnostics
            if diagnostic.maximum_absolute_entry_unitarity_defect is not None
        )
        primitive = self._primitive_frames(
            transported,
            schur_vectors,
            phases,
        )
        residuals = [
            float(np.linalg.norm(primitive[index] - primitive[index - 1]))
            for index in range(1, len(primitive))
        ]
        residuals.append(
            float(np.linalg.norm(primitive[-1] @ closure_action - primitive[0]))
        )
        return _Periodic1DRank2TransportDiagnostics(
            minimum_singular_value=float(min(singular_values, default=0.0)),
            maximum_rank_cutoff=float(max(cutoffs, default=0.0)),
            maximum_unitarity_defect=float(max(unitarity, default=0.0)),
            maximum_primitive_link_frobenius_residual=float(
                max(residuals, default=0.0)
            ),
            closure_phases=tuple(float(value) for value in phases),
            closure_alignment_residual=float(closure_residual),
            closure_alignment_unitarity_defect=float(closure_unitarity),
        )

    @staticmethod
    def _primitive_frames(
        transported: Complex128Array,
        schur_vectors: Complex128Array,
        phases: tuple[float, ...],
    ) -> tuple[Complex128Array, ...]:
        phase_array = np.asarray(phases, dtype=np.float64)
        primitive: list[Complex128Array] = []
        for index, frame in enumerate(transported):
            fraction = -float(index) / float(len(transported))
            correction = (
                schur_vectors
                @ np.diag(np.exp(1.0j * phase_array * fraction))
                @ schur_vectors.conj().T
            )
            primitive.append(
                np.asarray(frame @ correction.conj().T, dtype=np.complex128)
            )
        return tuple(primitive)


@dataclass(frozen=True, slots=True, eq=False)
class _Periodic1DRank2UnqualifiedPreparation:
    qualification: Periodic1DRank2Qualification


@dataclass(frozen=True, slots=True, eq=False)
class _Periodic1DRank2QualifiedPreparation:
    qualification: Periodic1DRank2QualifiedParent
    retained_matrices: Complex128Array
    traceless_matrices: Complex128Array
    mean_energies: Float64Array
    splitting_scale: float

    def __post_init__(self) -> None:
        size = self.retained_matrices.shape[0]
        if self.retained_matrices.shape != (size, 2, 2):
            raise ValueError("retained matrices must have shape (N, 2, 2)")
        if self.traceless_matrices.shape != (size, 2, 2):
            raise ValueError("traceless matrices must have shape (N, 2, 2)")
        if self.mean_energies.shape != (size,):
            raise ValueError("mean energies must have shape (N,)")
        for array in (
            self.retained_matrices,
            self.traceless_matrices,
            self.mean_energies,
        ):
            if array.flags.writeable:
                raise ValueError("qualified preparation arrays must be read-only")
        if type(self.splitting_scale) is not float:
            raise TypeError("splitting_scale must be a built-in float")
        if not math.isfinite(self.splitting_scale) or self.splitting_scale <= 0.0:
            raise ValueError("splitting_scale must be finite and positive")


type _Periodic1DRank2Preparation = (
    _Periodic1DRank2UnqualifiedPreparation | _Periodic1DRank2QualifiedPreparation
)


class _Periodic1DRank2ParentQualifier:
    """Apply external-gap and transport gates to one exact parent."""

    __slots__ = ("_parent", "_request", "_transporter")

    def __init__(
        self,
        *,
        request: Periodic1DRank2Request,
        parent: _Periodic1DRank2Parent,
        transporter: ClosedLoopPolarFrameTransporter,
    ) -> None:
        if type(request) is not Periodic1DRank2Request:
            raise TypeError("request must be Periodic1DRank2Request")
        if type(parent) is not _Periodic1DRank2Parent:
            raise TypeError("parent must be _Periodic1DRank2Parent")
        if type(transporter) is not ClosedLoopPolarFrameTransporter:
            raise TypeError("transporter must be ClosedLoopPolarFrameTransporter")
        self._request = request
        self._parent = parent
        self._transporter = transporter

    def execute(self) -> _Periodic1DRank2Preparation:
        """Return either one closed stop variant or qualified represented fields."""
        request = self._request
        parent = self._parent
        if parent.minimum_external_gap < request.minimum_external_gap:
            return _Periodic1DRank2UnqualifiedPreparation(
                Periodic1DRank2ExternalGapFailure(parent.minimum_external_gap)
            )
        source = FinitePeriodicMeshFrameInventory.from_arrays(
            mesh=CenteredUniformMesh(
                dimension=1,
                size=request.reciprocal_mesh_size,
                offsets=(0.0,),
            ),
            frames=parent.raw_retained_frames,
            endpoint_sewing_map=np.eye(4, dtype=np.complex128),
            ambient_basis_identifier=request.ambient_basis_identifier,
            retained_frame_identifier=request.retained_frame_identifier,
            endpoint_sewing_identifier=request.endpoint_sewing_identifier,
            principal_phase_branch=request.principal_phase_branch(),
            tolerance=request.transport_tolerance(),
        )
        try:
            outcome = self._transporter.transport(source)
        except ClosedLoopPolarFrameTransportBackendFailure as failure:
            return _Periodic1DRank2UnqualifiedPreparation(
                Periodic1DRank2BandTransportBackendFailure(
                    minimum_external_gap=parent.minimum_external_gap,
                    operation=failure.operation,
                    reason=failure.reason,
                    link_index=failure.link_index,
                )
            )
        minimum_singular = self._minimum_singular_value(outcome.link_diagnostics)
        if outcome.status is not ClosedLoopPolarFrameTransportStatus.QUALIFIED:
            return _Periodic1DRank2UnqualifiedPreparation(
                Periodic1DRank2BandTransportNumericallyUnresolved(
                    minimum_external_gap=parent.minimum_external_gap,
                    band_transport_status=outcome.status,
                    minimum_transport_singular_value=minimum_singular,
                )
            )
        if minimum_singular <= request.minimum_transport_singular_value:
            return _Periodic1DRank2UnqualifiedPreparation(
                Periodic1DRank2BandTransportThresholdFailure(
                    minimum_external_gap=parent.minimum_external_gap,
                    minimum_transport_singular_value=minimum_singular,
                )
            )
        transported = outcome.transported_frames
        if transported is None:
            raise ValueError("qualified transport must expose transported frames")
        diagnostics = _Periodic1DRank2TransportDiagnosticAnalyzer(outcome).execute()
        if diagnostics.minimum_singular_value != minimum_singular:
            raise ValueError("transport diagnostic minimum singular value changed")
        identity = np.eye(2, dtype=np.complex128)
        orthonormality_defect = float(
            max(
                np.linalg.norm(frame.conj().T @ frame - identity)
                for frame in transported
            )
        )
        retained = np.asarray(
            np.swapaxes(transported.conjugate(), -1, -2)
            @ parent.matrices
            @ transported,
            dtype=np.complex128,
        )
        hermiticity_defect = float(
            np.max(np.abs(retained - np.swapaxes(retained.conjugate(), -1, -2)))
        )
        means = np.asarray(
            np.trace(retained, axis1=1, axis2=2).real / 2.0,
            dtype=np.float64,
        )
        traceless = np.asarray(
            retained - means[:, None, None] * identity,
            dtype=np.complex128,
        )
        splitting_scale = float(
            np.mean(np.sum(np.abs(traceless) ** 2, axis=(1, 2))) / 2.0
        )
        qualification = Periodic1DRank2QualifiedParent(
            minimum_external_gap=parent.minimum_external_gap,
            minimum_transport_singular_value=minimum_singular,
            maximum_transport_rank_cutoff=diagnostics.maximum_rank_cutoff,
            maximum_transport_unitarity_defect=(diagnostics.maximum_unitarity_defect),
            maximum_primitive_link_frobenius_residual=(
                diagnostics.maximum_primitive_link_frobenius_residual
            ),
            closure_holonomy_phases=diagnostics.closure_phases,
            closure_alignment_residual=diagnostics.closure_alignment_residual,
            closure_alignment_unitarity_defect=(
                diagnostics.closure_alignment_unitarity_defect
            ),
            maximum_frame_orthonormality_defect=orthonormality_defect,
            maximum_reference_hermiticity_defect=hermiticity_defect,
        )
        return _Periodic1DRank2QualifiedPreparation(
            qualification=qualification,
            retained_matrices=_immutable_complex(retained),
            traceless_matrices=_immutable_complex(traceless),
            mean_energies=_immutable_real(means),
            splitting_scale=splitting_scale,
        )

    @staticmethod
    def _minimum_singular_value(
        diagnostics: tuple[ClosedLoopPolarFrameTransportLinkDiagnostic, ...],
    ) -> float:
        values = tuple(
            value
            for diagnostic in diagnostics
            for value in (diagnostic.singular_values or ())
        )
        return float(min(values, default=0.0))


__all__: list[str] = []
