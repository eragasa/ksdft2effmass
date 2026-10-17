"""Alignment-selection boundary for dimensional locality development.

The scalar restricted global rotation delegates periodic-harmonic maximization to
``projectkoios-optimization``. Batched neighbor transport remains a local, isolated
mechanism under the currently pinned dependency; converting every tensor-grid link to
that revision's one-pair object API would defeat the bounded sparse execution design.
A separately published batch contract is tracked for adoption under ``TD-BEL-002``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from projectkoios.optimization.selection.harmonic import (
    PeriodicHarmonic,
    PeriodicHarmonicMaximizer,
    PeriodicHarmonicMaximumStatus,
)

type ComplexArray = NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class FrameTransportDiagnostic:
    """Retain sparse batched transport, closure, and plaquette diagnostics."""

    minimum_singular_value: float
    maximum_procrustes_residual: float
    maximum_unitarity_defect: float
    maximum_rank_cutoff: float
    maximum_absolute_closure_phases: tuple[float, float]
    maximum_closure_unitarity_defect: float
    maximum_plaquette_phase: float


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
    minimum_singular = 1.0
    maximum_residual = 0.0
    maximum_unitarity = 0.0
    maximum_rank_cutoff = 0.0
    maximum_phase = np.zeros(2, dtype=np.float64)
    maximum_closure_unitarity = 0.0
    link_unitaries: list[ComplexArray] = []
    for axis in range(dimension):
        neighbor = np.roll(frame, shift=-1, axis=axis)
        overlap = np.swapaxes(frame.conjugate(), -1, -2) @ neighbor
        left, singular_values, right_h = np.linalg.svd(overlap)
        links = left @ right_h
        link_unitaries.append(links)
        minimum_singular = min(minimum_singular, float(np.min(singular_values)))
        maximum_residual = max(
            maximum_residual,
            float(
                np.sqrt(
                    np.max(
                        np.maximum(
                            0.0,
                            4.0 - 2.0 * np.sum(singular_values, axis=-1),
                        )
                    )
                )
            ),
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
            max(rank_absolute, rank_relative * float(np.max(singular_values))),
        )
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
        maximum_unitarity_defect=maximum_unitarity,
        maximum_rank_cutoff=maximum_rank_cutoff,
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
