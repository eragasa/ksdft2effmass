"""Independent nested-momentum reconstruction for embedded-subspace rank two."""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import pairwise

import numpy as np

from .reference import (
    Periodic1DEmbeddedSubspaceRank2IndependentReferenceAnalyzer,
    _parent_matrices,
)
from .refinement import (
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds,
)
from .request import Periodic1DEmbeddedSubspaceRank2Request
from .results import (
    Periodic1DEmbeddedSubspaceRank2Analysis,
    Periodic1DEmbeddedSubspaceRank2PointAnalysis,
    Periodic1DEmbeddedSubspaceRank2QualifiedParent,
)


@dataclass(frozen=True, slots=True)
class _IndependentMomentumRefinementStep:
    coarse_mesh_size: int
    fine_mesh_size: int
    maximum_parent_diagnostic_change: float
    maximum_shared_parent_eigenvalue_defect: float
    maximum_shared_parent_projector_defect: float
    maximum_correlation_change: float
    maximum_threshold_change: float
    maximum_hopping_weight_change: float
    maximum_hopping_power_change: float
    maximum_angle_change: float
    maximizing_angle_dispositions_stable: bool
    maximum_band_defect: float
    maximum_reconstruction_defect: float
    maximum_parseval_defect: float
    within_tolerances: bool


@dataclass(frozen=True, slots=True)
class _IndependentMomentumQualificationStopped:
    request: Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest
    mesh_analyses: tuple[Periodic1DEmbeddedSubspaceRank2Analysis, ...]
    refinements: tuple[_IndependentMomentumRefinementStep, ...] = ()


@dataclass(frozen=True, slots=True)
class _IndependentMomentumConverged:
    request: Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest
    mesh_analyses: tuple[Periodic1DEmbeddedSubspaceRank2Analysis, ...]
    refinements: tuple[_IndependentMomentumRefinementStep, ...]


@dataclass(frozen=True, slots=True)
class _IndependentMomentumUnresolved:
    request: Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest
    mesh_analyses: tuple[Periodic1DEmbeddedSubspaceRank2Analysis, ...]
    refinements: tuple[_IndependentMomentumRefinementStep, ...]


_IndependentMomentumReference = (
    _IndependentMomentumQualificationStopped
    | _IndependentMomentumConverged
    | _IndependentMomentumUnresolved
)


class Periodic1DEmbeddedSubspaceRank2MomentumRefinementIndependentReferenceAnalyzer:
    """Rebuild every mesh and refinement without production refinement actions."""

    __slots__ = ("_request",)

    def __init__(
        self,
        request: Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest,
    ) -> None:
        if type(request) is not (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest
        ):
            raise TypeError("request must be a momentum-refinement request")
        self._request = request

    def execute(self) -> _IndependentMomentumReference:
        """Return one independently reconstructed closed refinement outcome."""
        meshes = tuple(
            Periodic1DEmbeddedSubspaceRank2IndependentReferenceAnalyzer(
                _independent_mesh_request(self._request, size)
            ).execute()
            for size in self._request.reciprocal_mesh_sizes
        )
        if not all(item.qualification.qualified for item in meshes):
            return _IndependentMomentumQualificationStopped(self._request, meshes)
        steps = tuple(
            _independent_step(self._request.thresholds, coarse, fine)
            for coarse, fine in pairwise(meshes)
        )
        required = self._request.required_stable_refinements
        if all(item.within_tolerances for item in steps[-required:]):
            return _IndependentMomentumConverged(self._request, meshes, steps)
        return _IndependentMomentumUnresolved(self._request, meshes, steps)


def _independent_mesh_request(
    refinement: Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest,
    size: int,
) -> Periodic1DEmbeddedSubspaceRank2Request:
    template = refinement.template_request
    return Periodic1DEmbeddedSubspaceRank2Request(
        reciprocal_mesh_size=size,
        amplitudes=template.amplitudes,
        parent_hopping_scale=template.parent_hopping_scale,
        minimum_external_gap=template.minimum_external_gap,
        minimum_transport_singular_value=template.minimum_transport_singular_value,
        frame_absolute_tolerance=template.frame_absolute_tolerance,
        transport_rank_relative_tolerance=template.transport_rank_relative_tolerance,
        transport_validation_relative_tolerance=(
            template.transport_validation_relative_tolerance
        ),
        harmonic_absolute_degeneracy_tolerance=(
            template.harmonic_absolute_degeneracy_tolerance
        ),
        harmonic_relative_degeneracy_tolerance=(
            template.harmonic_relative_degeneracy_tolerance
        ),
    )


def _independent_step(
    thresholds: Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds,
    coarse: Periodic1DEmbeddedSubspaceRank2Analysis,
    fine: Periodic1DEmbeddedSubspaceRank2Analysis,
) -> _IndependentMomentumRefinementStep:
    coarse_qualification = coarse.qualification
    fine_qualification = fine.qualification
    if type(coarse_qualification) is not (
        Periodic1DEmbeddedSubspaceRank2QualifiedParent
    ) or type(fine_qualification) is not (
        Periodic1DEmbeddedSubspaceRank2QualifiedParent
    ):
        raise TypeError("independent refinement requires qualified meshes")
    eigenvalue_defect, projector_defect = _independent_parent_defects(
        coarse.request.reciprocal_mesh_size,
        fine.request.reciprocal_mesh_size,
        coarse.request.parent_hopping_scale,
    )
    scalar_names = (
        "minimum_external_gap",
        "minimum_transport_singular_value",
        "maximum_transport_rank_cutoff",
        "maximum_transport_unitarity_defect",
        "maximum_primitive_link_frobenius_residual",
        "closure_alignment_residual",
        "closure_alignment_unitarity_defect",
        "maximum_frame_orthonormality_defect",
        "maximum_reference_hermiticity_defect",
    )
    parent_change = max(
        eigenvalue_defect,
        projector_defect,
        *(
            abs(getattr(fine_qualification, name) - getattr(coarse_qualification, name))
            for name in scalar_names
        ),
        *(
            _wrapped_phase_distance(candidate, expected)
            for candidate, expected in zip(
                fine_qualification.closure_holonomy_phases,
                coarse_qualification.closure_holonomy_phases,
                strict=True,
            )
        ),
    )
    correlation_change = max(
        abs(
            fine_point.discrete_maximum_correlation
            - coarse_point.discrete_maximum_correlation
        )
        for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True)
    )
    threshold_change = max(
        max(
            abs(
                fine_point.minimum_operator_threshold
                - coarse_point.minimum_operator_threshold
            ),
            abs(
                fine_point.exact_spectrum_joint_operator_threshold
                - coarse_point.exact_spectrum_joint_operator_threshold
            ),
        )
        for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True)
    )
    hopping_weight_change = max(
        max(
            abs(
                fine_point.reference_nonzero_hopping_weight
                - coarse_point.reference_nonzero_hopping_weight
            ),
            abs(
                fine_point.comparison_nonzero_hopping_weight
                - coarse_point.comparison_nonzero_hopping_weight
            ),
        )
        for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True)
    )
    hopping_power_change = max(
        _independent_hopping_change(coarse_point, fine_point)
        for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True)
    )
    statuses_stable = all(
        coarse_point.harmonic_maximum.status is fine_point.harmonic_maximum.status
        for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True)
    )
    angle_change = max(
        _independent_angle_change(coarse_point, fine_point)
        for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True)
    )
    values = {
        "maximum_parent_diagnostic_change": parent_change,
        "maximum_correlation_change": correlation_change,
        "maximum_threshold_change": threshold_change,
        "maximum_hopping_weight_change": hopping_weight_change,
        "maximum_hopping_power_change": hopping_power_change,
        "maximum_angle_change": angle_change,
        "maximum_band_defect": max(point.maximum_band_defect for point in fine.points),
        "maximum_reconstruction_defect": max(
            point.minimum_loss_reconstruction_defect for point in fine.points
        ),
        "maximum_parseval_defect": max(
            max(point.reference_parseval_defect, point.comparison_parseval_defect)
            for point in fine.points
        ),
    }
    within = statuses_stable and all(
        values[name] <= getattr(thresholds, name) for name in values
    )
    return _IndependentMomentumRefinementStep(
        coarse_mesh_size=coarse.request.reciprocal_mesh_size,
        fine_mesh_size=fine.request.reciprocal_mesh_size,
        maximum_shared_parent_eigenvalue_defect=eigenvalue_defect,
        maximum_shared_parent_projector_defect=projector_defect,
        maximizing_angle_dispositions_stable=statuses_stable,
        within_tolerances=within,
        **values,
    )


def _independent_parent_defects(
    coarse_size: int,
    fine_size: int,
    parent_hopping_scale: float,
) -> tuple[float, float]:
    coarse_coordinates = np.asarray(
        tuple(-0.5 + float(index) / float(coarse_size) for index in range(coarse_size)),
        dtype=np.float64,
    )
    fine_coordinates = np.asarray(
        tuple(-0.5 + float(index) / float(fine_size) for index in range(fine_size)),
        dtype=np.float64,
    )
    coarse_values, coarse_vectors = np.linalg.eigh(
        _parent_matrices(coarse_coordinates, parent_hopping_scale)
    )
    fine_values, fine_vectors = np.linalg.eigh(
        _parent_matrices(fine_coordinates, parent_hopping_scale)
    )
    eigenvalue_defect = float(np.max(np.abs(fine_values[::2] - coarse_values)))
    coarse_frames = coarse_vectors[:, :, :2]
    fine_frames = fine_vectors[::2, :, :2]
    coarse_projectors = coarse_frames @ coarse_frames.conj().transpose(0, 2, 1)
    fine_projectors = fine_frames @ fine_frames.conj().transpose(0, 2, 1)
    projector_defect = float(
        np.max(
            np.linalg.norm(
                fine_projectors - coarse_projectors,
                axis=(1, 2),
                ord="fro",
            )
        )
    )
    return eigenvalue_defect, projector_defect


def _wrapped_phase_distance(left: float, right: float) -> float:
    distance = abs(left - right) % math.tau
    return min(distance, math.tau - distance)


def _independent_angle_change(
    coarse: Periodic1DEmbeddedSubspaceRank2PointAnalysis,
    fine: Periodic1DEmbeddedSubspaceRank2PointAnalysis,
) -> float:
    left = coarse.harmonic_maximum.canonical_maximizing_argument
    right = fine.harmonic_maximum.canonical_maximizing_argument
    period = coarse.harmonic_maximum.fundamental_period
    if left is None and right is None:
        return 0.0
    if left is None or right is None:
        return period
    distance = abs(left - right) % period
    return min(distance, period - distance)


def _independent_hopping_change(
    coarse: Periodic1DEmbeddedSubspaceRank2PointAnalysis,
    fine: Periodic1DEmbeddedSubspaceRank2PointAnalysis,
) -> float:
    fine_inventory = {item.displacement: item for item in fine.hopping_powers}
    defects: list[float] = []
    for coarse_item in coarse.hopping_powers:
        fine_item = fine_inventory[coarse_item.displacement]
        defects.extend(
            (
                abs(
                    fine_item.reference_normalized_squared_frobenius_norm
                    - coarse_item.reference_normalized_squared_frobenius_norm
                ),
                abs(
                    fine_item.comparison_normalized_squared_frobenius_norm
                    - coarse_item.comparison_normalized_squared_frobenius_norm
                ),
            )
        )
    return max(defects)


__all__ = [
    "Periodic1DEmbeddedSubspaceRank2MomentumRefinementIndependentReferenceAnalyzer"
]
