"""Alignment-selection boundary for dimensional locality analysis.

Optimization owns scalar periodic-harmonic maximization and batched complex-unitary
Procrustes transformation selection. KSD owns reciprocal-neighbor topology, closure and
plaquette applicability, scientific thresholds, and interpretation.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesResult,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesTolerance,
)
from projectkoios.optimization.selection.harmonic import (
    PeriodicHarmonic,
    PeriodicHarmonicMaximizer,
    PeriodicHarmonicMaximumStatus,
)

from ksdft2effmass.solidstate.reciprocal_sewing import (
    ReciprocalEndpointSewingInventory,
)

from .definitions import TRANSPORT_RANK_DEFICIENT_REASON

type ComplexArray = NDArray[np.complex128]
type _ProcrustesSolve = Callable[
    [ComplexArray, ComplexArray, ComplexUnitaryProcrustesTolerance],
    NumpyBatchedComplexUnitaryProcrustesResult,
]


@dataclass(frozen=True, slots=True)
class RestrictedAlignmentDiagnostic:
    """Retain one restricted global rank-two alignment outcome."""

    rotation_angle: float | None
    rotation_degenerate: bool
    splitting_scale: float
    maximum_correlation: float | None
    minimum_operator_threshold: float
    exact_spectrum_joint_operator_threshold: float

    def __post_init__(self) -> None:
        if self.rotation_angle is not None:
            if type(self.rotation_angle) is not float:
                raise TypeError("rotation_angle must be a built-in float or None")
            if not math.isfinite(self.rotation_angle):
                raise ValueError("rotation_angle must be finite or None")
        if type(self.rotation_degenerate) is not bool:
            raise TypeError("rotation_degenerate must be a built-in bool")
        if self.maximum_correlation is not None:
            if type(self.maximum_correlation) is not float:
                raise TypeError("maximum_correlation must be a built-in float or None")
            if not math.isfinite(self.maximum_correlation) or not (
                -1.0 <= self.maximum_correlation <= 1.0
            ):
                raise ValueError("maximum_correlation must lie in [-1, 1] or be None")
        for name in (
            "splitting_scale",
            "minimum_operator_threshold",
            "exact_spectrum_joint_operator_threshold",
        ):
            value = getattr(self, name)
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if (self.rotation_angle is None) is not (self.maximum_correlation is None):
            raise ValueError("rotation and correlation applicability must agree")
        if self.rotation_angle is None and not self.rotation_degenerate:
            raise ValueError("inapplicable alignment must be rotation-degenerate")


@dataclass(frozen=True, slots=True)
class FrameTransportDiagnostic:
    """Retain sparse batched transport, closure, and plaquette diagnostics."""

    minimum_singular_value: float
    maximum_procrustes_residual: float
    maximum_squared_residual_roundoff_cutoff: float
    maximum_unitarity_defect: float
    maximum_rank_cutoff: float
    rank_deficient_link_count: int
    closure_and_plaquette_applicable: bool
    closure_and_plaquette_inapplicable_reason: str | None
    maximum_absolute_closure_phases: tuple[float, ...] | None
    maximum_closure_unitarity_defect: float | None
    maximum_plaquette_phase: float | None

    def __post_init__(self) -> None:
        for name in (
            "minimum_singular_value",
            "maximum_procrustes_residual",
            "maximum_squared_residual_roundoff_cutoff",
            "maximum_unitarity_defect",
            "maximum_rank_cutoff",
        ):
            value = getattr(self, name)
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if type(self.rank_deficient_link_count) is not int:
            raise TypeError("rank_deficient_link_count must be a built-in int")
        if self.rank_deficient_link_count < 0:
            raise ValueError("rank_deficient_link_count must be nonnegative")
        if type(self.closure_and_plaquette_applicable) is not bool:
            raise TypeError("closure_and_plaquette_applicable must be a built-in bool")
        if self.closure_and_plaquette_applicable != (
            self.rank_deficient_link_count == 0
        ):
            raise ValueError("topology applicability must match numerical link rank")
        topology_values = (
            self.maximum_absolute_closure_phases,
            self.maximum_closure_unitarity_defect,
            self.maximum_plaquette_phase,
        )
        if self.closure_and_plaquette_applicable:
            if self.closure_and_plaquette_inapplicable_reason is not None:
                raise ValueError("applicable topology diagnostics cannot have a reason")
            if any(value is None for value in topology_values):
                raise ValueError("applicable topology diagnostics must be complete")
        else:
            if (
                self.closure_and_plaquette_inapplicable_reason
                != TRANSPORT_RANK_DEFICIENT_REASON
            ):
                raise ValueError("inapplicable topology requires the stable reason")
            if any(value is not None for value in topology_values):
                raise ValueError("inapplicable topology prohibits diagnostic values")
        phases = self.maximum_absolute_closure_phases
        if phases is not None:
            if type(phases) is not tuple or not phases:
                raise TypeError(
                    "maximum_absolute_closure_phases must be a nonempty tuple"
                )
            if any(
                type(value) is not float
                or not math.isfinite(value)
                or not 0.0 <= value <= math.pi
                for value in phases
            ):
                raise ValueError("closure phases must be finite values in [0, pi]")
        for name in (
            "maximum_closure_unitarity_defect",
            "maximum_plaquette_phase",
        ):
            value = getattr(self, name)
            if value is not None:
                if type(value) is not float:
                    raise TypeError(f"{name} must be a built-in float or None")
                if not math.isfinite(value) or value < 0.0:
                    raise ValueError(f"{name} must be finite and nonnegative or None")
        if (
            self.maximum_plaquette_phase is not None
            and self.maximum_plaquette_phase > math.pi
        ):
            raise ValueError("maximum_plaquette_phase cannot exceed pi")


def _maximum_matrix_defect(left: ComplexArray, right: ComplexArray) -> float:
    return float(np.max(np.linalg.norm(left - right, axis=(-2, -1))))


def _default_procrustes_solve(
    source: ComplexArray,
    target: ComplexArray,
    tolerance: ComplexUnitaryProcrustesTolerance,
) -> NumpyBatchedComplexUnitaryProcrustesResult:
    """Return Project Koios pointwise right-unitary selections."""
    return NumpyBatchedComplexUnitaryProcrustesSolver().solve(
        NumpyBatchedComplexUnitaryProcrustesDefinition.from_arrays(
            source_matrices=source,
            target_matrices=target,
            tolerance=tolerance,
        )
    )


def frame_transport_diagnostics(
    frame: ComplexArray,
    dimension: int,
    rank_absolute: float,
    rank_relative: float,
    *,
    endpoint_sewing: ReciprocalEndpointSewingInventory,
    procrustes_solve: _ProcrustesSolve | None = None,
) -> FrameTransportDiagnostic:
    """Measure neighbor transport, sewn loop closure, and plaquettes sparsely."""
    if type(dimension) is not int or dimension <= 0:
        raise ValueError("dimension must be a positive built-in integer")
    if frame.ndim != dimension + 2:
        raise ValueError("frame tensor rank must match the spatial dimension")
    retained_rank = int(frame.shape[-1])
    ambient_dimension = int(frame.shape[-2])
    if retained_rank <= 0 or ambient_dimension < retained_rank:
        raise ValueError("frame must have a positive admitted retained rank")
    if type(endpoint_sewing) is not ReciprocalEndpointSewingInventory:
        raise TypeError("endpoint_sewing must be ReciprocalEndpointSewingInventory")
    if endpoint_sewing.spatial_dimension != dimension:
        raise ValueError("endpoint sewing must match the spatial dimension")
    if endpoint_sewing.ambient_dimension != ambient_dimension:
        raise ValueError("endpoint sewing must match the frame ambient dimension")
    identity = np.eye(retained_rank, dtype=np.complex128)
    tolerance = ComplexUnitaryProcrustesTolerance(
        rank_absolute=rank_absolute,
        rank_relative=rank_relative,
    )
    solve = _default_procrustes_solve if procrustes_solve is None else procrustes_solve
    minimum_singular = 1.0
    maximum_residual = 0.0
    maximum_squared_residual_roundoff_cutoff = 0.0
    maximum_unitarity = 0.0
    maximum_rank_cutoff = 0.0
    rank_deficient_link_count = 0
    link_unitaries: list[ComplexArray] = []
    for axis in range(dimension):
        neighbor = np.roll(frame, shift=-1, axis=axis)
        # ``np.roll`` identifies the last point directly with the first. Replace only
        # that wrap target so interior links remain ordinary same-chart overlaps.
        boundary_source = np.take(frame, indices=0, axis=axis)
        sewing_matrix = endpoint_sewing.map_for_axis(axis).coefficient_map.magnitude
        sewn_boundary = np.einsum(
            "ab,...br->...ar",
            sewing_matrix,
            boundary_source,
        )
        boundary_index: list[slice | int] = [slice(None)] * frame.ndim
        boundary_index[axis] = -1
        neighbor[tuple(boundary_index)] = sewn_boundary
        transport = solve(frame, neighbor, tolerance)
        links = transport.right_unitary_completions
        singular_values = transport.cross_singular_values
        link_unitaries.append(links)
        minimum_singular = min(minimum_singular, float(np.min(singular_values)))
        maximum_residual = max(
            maximum_residual,
            float(np.max(transport.optimal_residual_frobenius_norms)),
        )
        maximum_squared_residual_roundoff_cutoff = max(
            maximum_squared_residual_roundoff_cutoff,
            float(np.max(transport.applied_residual_roundoff_cutoffs)),
        )
        maximum_unitarity = max(
            maximum_unitarity,
            _maximum_matrix_defect(
                np.swapaxes(links.conjugate(), -1, -2) @ links,
                np.broadcast_to(identity, links.shape),
            ),
        )
        maximum_rank_cutoff = max(
            maximum_rank_cutoff,
            float(np.max(transport.applied_rank_cutoffs)),
        )
        rank_deficient_link_count += transport.rank_deficient_count

    if rank_deficient_link_count:
        return FrameTransportDiagnostic(
            minimum_singular_value=minimum_singular,
            maximum_procrustes_residual=maximum_residual,
            maximum_squared_residual_roundoff_cutoff=(
                maximum_squared_residual_roundoff_cutoff
            ),
            maximum_unitarity_defect=maximum_unitarity,
            maximum_rank_cutoff=maximum_rank_cutoff,
            rank_deficient_link_count=rank_deficient_link_count,
            closure_and_plaquette_applicable=False,
            closure_and_plaquette_inapplicable_reason=(TRANSPORT_RANK_DEFICIENT_REASON),
            maximum_absolute_closure_phases=None,
            maximum_closure_unitarity_defect=None,
            maximum_plaquette_phase=None,
        )

    maximum_phase = np.zeros(retained_rank, dtype=np.float64)
    maximum_closure_unitarity = 0.0
    for axis, links in enumerate(link_unitaries):
        ordered = np.moveaxis(links, axis, 0).reshape(
            links.shape[axis], -1, retained_rank, retained_rank
        )
        holonomy = np.broadcast_to(
            identity, (ordered.shape[1], retained_rank, retained_rank)
        ).copy()
        for link in ordered:
            holonomy = holonomy @ link
        maximum_closure_unitarity = max(
            maximum_closure_unitarity,
            _maximum_matrix_defect(
                np.swapaxes(holonomy.conjugate(), -1, -2) @ holonomy,
                np.broadcast_to(identity, holonomy.shape),
            ),
        )
        phases = np.sort(np.angle(np.linalg.eigvals(holonomy)), axis=-1)
        maximum_phase = np.maximum(maximum_phase, np.max(np.abs(phases), axis=0))

    maximum_plaquette_phase = 0.0
    for first_axis in range(dimension):
        for second_axis in range(first_axis + 1, dimension):
            first = link_unitaries[first_axis]
            second = link_unitaries[second_axis]
            plaquette = (
                first
                @ np.roll(second, shift=-1, axis=first_axis)
                @ np.swapaxes(
                    np.roll(first, shift=-1, axis=second_axis).conjugate(), -1, -2
                )
                @ np.swapaxes(second.conjugate(), -1, -2)
            )
            maximum_plaquette_phase = max(
                maximum_plaquette_phase,
                float(np.max(np.abs(np.angle(np.linalg.eigvals(plaquette))))),
            )
    return FrameTransportDiagnostic(
        minimum_singular_value=minimum_singular,
        maximum_procrustes_residual=maximum_residual,
        maximum_squared_residual_roundoff_cutoff=(
            maximum_squared_residual_roundoff_cutoff
        ),
        maximum_unitarity_defect=maximum_unitarity,
        maximum_rank_cutoff=maximum_rank_cutoff,
        rank_deficient_link_count=0,
        closure_and_plaquette_applicable=True,
        closure_and_plaquette_inapplicable_reason=None,
        maximum_absolute_closure_phases=tuple(float(value) for value in maximum_phase),
        maximum_closure_unitarity_defect=maximum_closure_unitarity,
        maximum_plaquette_phase=maximum_plaquette_phase,
    )


def restricted_alignment_diagnostic(
    reference: ComplexArray,
    comparison: ComplexArray,
) -> RestrictedAlignmentDiagnostic:
    """Return a typed diagnostic for one restricted global alignment."""
    values = restricted_alignment(reference, comparison)
    return RestrictedAlignmentDiagnostic(
        rotation_angle=values[0],
        rotation_degenerate=values[1],
        splitting_scale=values[2],
        maximum_correlation=values[3],
        minimum_operator_threshold=values[4],
        exact_spectrum_joint_operator_threshold=values[5],
    )


def restricted_alignment(
    reference: ComplexArray, comparison: ComplexArray
) -> tuple[float | None, bool, float, float | None, float, float]:
    """Repeat Paper 1's global-rotation and positive-splitting minimization."""
    identity = np.eye(2, dtype=np.complex128)
    reference_trace = np.trace(reference, axis1=-2, axis2=-1).real / 2.0
    comparison_trace = np.trace(comparison, axis1=-2, axis2=-1).real / 2.0
    reference_traceless = reference - reference_trace[..., None, None] * identity
    comparison_traceless = comparison - comparison_trace[..., None, None] * identity
    splitting_scale = float(
        np.mean(np.sum(np.abs(reference_traceless) ** 2, axis=(-2, -1))) / 2.0
    )
    if splitting_scale <= 1.0e-30:
        return None, True, splitting_scale, None, 0.0, 0.0

    def correlation_numerator(angle: float) -> float:
        cosine = math.cos(angle)
        sine = math.sin(angle)
        rotation = np.array([[cosine, -sine], [sine, cosine]], dtype=np.complex128)
        rotated = rotation.T @ reference_traceless @ rotation
        products = np.einsum(
            "...ij,...ij->...", rotated.conjugate(), comparison_traceless
        )
        return float(np.mean(products.real) / 2.0)

    positive_quarter = correlation_numerator(math.pi / 4.0)
    negative_quarter = correlation_numerator(-math.pi / 4.0)
    constant = (positive_quarter + negative_quarter) / 2.0
    harmonic = PeriodicHarmonic(
        offset=constant,
        cosine_coefficient=correlation_numerator(0.0) - constant,
        sine_coefficient=(positive_quarter - negative_quarter) / 2.0,
        harmonic_order=2,
        fundamental_interval_start=-math.pi / 2.0,
    )
    maximum = PeriodicHarmonicMaximizer(
        absolute_degeneracy_tolerance=0.0,
        relative_degeneracy_tolerance=1.0e-15,
    ).maximize(harmonic)
    degenerate = maximum.status is PeriodicHarmonicMaximumStatus.NUMERICALLY_CONSTANT
    angle = (
        0.0
        if maximum.canonical_maximizing_argument is None
        else maximum.canonical_maximizing_argument
    )
    correlation = max(-1.0, min(1.0, maximum.maximum_value / splitting_scale))
    # Deferred TD-BEL-001: replace proximity-only snapping with an independently
    # verified exact-identity gate before this can support qualified evidence.
    if abs(1.0 - correlation) <= 64.0 * np.finfo(np.float64).eps:
        correlation = 1.0
    elif abs(-1.0 - correlation) <= 64.0 * np.finfo(np.float64).eps:
        correlation = -1.0
    positive_scale = max(0.0, correlation)
    minimum_threshold = math.sqrt(max(0.0, splitting_scale * (1.0 - positive_scale**2)))
    exact_spectrum_threshold = math.sqrt(
        max(0.0, 2.0 * splitting_scale * (1.0 - correlation))
    )
    return (
        angle,
        degenerate,
        splitting_scale,
        correlation,
        minimum_threshold,
        exact_spectrum_threshold,
    )


__all__ = [
    "FrameTransportDiagnostic",
    "RestrictedAlignmentDiagnostic",
    "frame_transport_diagnostics",
    "restricted_alignment",
    "restricted_alignment_diagnostic",
]
