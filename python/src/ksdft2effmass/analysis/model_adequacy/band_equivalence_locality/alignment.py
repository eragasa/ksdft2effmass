"""Alignment-selection boundary for dimensional locality analysis.

Optimization owns scalar periodic-harmonic maximization and batched complex-unitary
Procrustes transformation selection. KSD owns reciprocal-neighbor topology, closure and
plaquette applicability, scientific thresholds, and interpretation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
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

from .definitions import TRANSPORT_RANK_DEFICIENT_REASON

type ComplexArray = NDArray[np.complex128]


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
    maximum_absolute_closure_phases: tuple[float, float] | None
    maximum_closure_unitarity_defect: float | None
    maximum_plaquette_phase: float | None


def _maximum_matrix_defect(left: ComplexArray, right: ComplexArray) -> float:
    return float(np.max(np.linalg.norm(left - right, axis=(-2, -1))))


def frame_transport_diagnostics(
    frame: ComplexArray,
    dimension: int,
    rank_absolute: float,
    rank_relative: float,
) -> FrameTransportDiagnostic:
    """Measure neighbor transport, loop closure, and plaquette sewing sparsely."""
    identity = np.eye(2, dtype=np.complex128)
    tolerance = ComplexUnitaryProcrustesTolerance(
        rank_absolute=rank_absolute,
        rank_relative=rank_relative,
    )
    solver = NumpyBatchedComplexUnitaryProcrustesSolver()
    minimum_singular = 1.0
    maximum_residual = 0.0
    maximum_squared_residual_roundoff_cutoff = 0.0
    maximum_unitarity = 0.0
    maximum_rank_cutoff = 0.0
    rank_deficient_link_count = 0
    link_unitaries: list[ComplexArray] = []
    for axis in range(dimension):
        neighbor = np.roll(frame, shift=-1, axis=axis)
        transport = solver.solve(
            NumpyBatchedComplexUnitaryProcrustesDefinition.from_arrays(
                source_matrices=frame,
                target_matrices=neighbor,
                tolerance=tolerance,
            )
        )
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

    maximum_phase = np.zeros(2, dtype=np.float64)
    maximum_closure_unitarity = 0.0
    for axis, links in enumerate(link_unitaries):
        ordered = np.moveaxis(links, axis, 0).reshape(links.shape[axis], -1, 2, 2)
        holonomy = np.broadcast_to(identity, (ordered.shape[1], 2, 2)).copy()
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
        maximum_absolute_closure_phases=(
            float(maximum_phase[0]),
            float(maximum_phase[1]),
        ),
        maximum_closure_unitarity_defect=maximum_closure_unitarity,
        maximum_plaquette_phase=maximum_plaquette_phase,
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
    "frame_transport_diagnostics",
    "restricted_alignment",
]
