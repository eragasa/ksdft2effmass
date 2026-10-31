"""Nested momentum refinement for the embedded-subspace rank-two control."""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from itertools import pairwise
from typing import final

import numpy as np
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.numerical_consistency import NumericalConsistency

from .analysis import Periodic1DEmbeddedSubspaceRank2Analyzer
from .parent import _Periodic1DEmbeddedSubspaceRank2ParentConstructor
from .request import Periodic1DEmbeddedSubspaceRank2Request
from .results import (
    Periodic1DEmbeddedSubspaceRank2Analysis,
    Periodic1DEmbeddedSubspaceRank2PointAnalysis,
    Periodic1DEmbeddedSubspaceRank2QualifiedParent,
)


def _positive_float(value: float, name: str) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _nonnegative_float(value: float, name: str) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds:
    """Declare separate finite stability and residual thresholds."""

    maximum_parent_diagnostic_change: float
    maximum_correlation_change: float
    maximum_threshold_change: float
    maximum_hopping_weight_change: float
    maximum_hopping_power_change: float
    maximum_angle_change: float
    maximum_band_defect: float
    maximum_reconstruction_defect: float
    maximum_parseval_defect: float

    def __post_init__(self) -> None:
        for name in (
            "maximum_parent_diagnostic_change",
            "maximum_correlation_change",
            "maximum_threshold_change",
            "maximum_hopping_weight_change",
            "maximum_hopping_power_change",
            "maximum_angle_change",
            "maximum_band_defect",
            "maximum_reconstruction_defect",
            "maximum_parseval_defect",
        ):
            _positive_float(getattr(self, name), name)


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest:
    """Bind nested doubling meshes to one unchanged scientific template."""

    template_request: Periodic1DEmbeddedSubspaceRank2Request
    reciprocal_mesh_sizes: tuple[int, ...]
    thresholds: Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds
    required_stable_refinements: int

    def __post_init__(self) -> None:
        if type(self.template_request) is not Periodic1DEmbeddedSubspaceRank2Request:
            raise TypeError(
                "template_request must be Periodic1DEmbeddedSubspaceRank2Request"
            )
        if (
            type(self.reciprocal_mesh_sizes) is not tuple
            or len(self.reciprocal_mesh_sizes) < 2
        ):
            raise TypeError("reciprocal_mesh_sizes must contain at least two integers")
        if any(type(size) is not int for size in self.reciprocal_mesh_sizes):
            raise TypeError("reciprocal_mesh_sizes must contain built-in integers")
        if self.reciprocal_mesh_sizes[0] != self.template_request.reciprocal_mesh_size:
            raise ValueError("template_request must describe the first mesh")
        if any(
            fine != 2 * coarse for coarse, fine in pairwise(self.reciprocal_mesh_sizes)
        ):
            raise ValueError("reciprocal_mesh_sizes must be nested doubling meshes")
        if type(self.thresholds) is not (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds
        ):
            raise TypeError("thresholds must be momentum-refinement thresholds")
        if type(self.required_stable_refinements) is not int:
            raise TypeError("required_stable_refinements must be a built-in int")
        if not 1 <= self.required_stable_refinements < len(self.reciprocal_mesh_sizes):
            raise ValueError("required_stable_refinements exceeds available mesh pairs")

    def request_at(
        self, reciprocal_mesh_size: int
    ) -> Periodic1DEmbeddedSubspaceRank2Request:
        """Return one declared mesh request with every other control unchanged."""
        if type(reciprocal_mesh_size) is not int:
            raise TypeError("reciprocal_mesh_size must be a built-in int")
        if reciprocal_mesh_size not in self.reciprocal_mesh_sizes:
            raise ValueError("reciprocal_mesh_size is not declared by this refinement")
        return replace(
            self.template_request,
            reciprocal_mesh_size=reciprocal_mesh_size,
        )


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2MomentumRefinementStep:
    """Retain separate changes and fine-mesh residuals for one doubling."""

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

    def __post_init__(self) -> None:
        if (
            type(self.coarse_mesh_size) is not int
            or type(self.fine_mesh_size) is not int
        ):
            raise TypeError("mesh sizes must be built-in integers")
        if self.fine_mesh_size != 2 * self.coarse_mesh_size:
            raise ValueError("mesh sizes must form one doubling pair")
        for name in (
            "maximum_parent_diagnostic_change",
            "maximum_shared_parent_eigenvalue_defect",
            "maximum_shared_parent_projector_defect",
            "maximum_correlation_change",
            "maximum_threshold_change",
            "maximum_hopping_weight_change",
            "maximum_hopping_power_change",
            "maximum_angle_change",
            "maximum_band_defect",
            "maximum_reconstruction_defect",
            "maximum_parseval_defect",
        ):
            _nonnegative_float(getattr(self, name), name)
        if type(self.maximizing_angle_dispositions_stable) is not bool:
            raise TypeError(
                "maximizing_angle_dispositions_stable must be a built-in bool"
            )
        if type(self.within_tolerances) is not bool:
            raise TypeError("within_tolerances must be a built-in bool")


class Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalysis(NumericalConsistency):
    """Identify one closed nested-momentum outcome variant."""

    __slots__ = ()

    request: Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest
    mesh_analyses: tuple[Periodic1DEmbeddedSubspaceRank2Analysis, ...]
    refinements: tuple[Periodic1DEmbeddedSubspaceRank2MomentumRefinementStep, ...]

    @property
    @final
    def converged(self) -> bool:
        """Return whether all required final qualified refinements passed."""
        return type(self) is Periodic1DEmbeddedSubspaceRank2MomentumRefinementConverged


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2MomentumRefinementQualificationStopped(
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalysis
):
    """Retain every mesh when at least one qualification gate stops comparison."""

    request: Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest
    mesh_analyses: tuple[Periodic1DEmbeddedSubspaceRank2Analysis, ...]
    refinements: tuple[Periodic1DEmbeddedSubspaceRank2MomentumRefinementStep, ...] = ()

    def __post_init__(self) -> None:
        _validate_refinement_outcome(self)
        if all(item.qualification.qualified for item in self.mesh_analyses):
            raise ValueError(
                "qualification-stopped outcome requires an unqualified mesh"
            )
        if self.refinements:
            raise ValueError("qualification-stopped outcome cannot retain refinements")


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2MomentumRefinementConverged(
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalysis
):
    """Retain a qualified study whose required final refinements all pass."""

    request: Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest
    mesh_analyses: tuple[Periodic1DEmbeddedSubspaceRank2Analysis, ...]
    refinements: tuple[Periodic1DEmbeddedSubspaceRank2MomentumRefinementStep, ...]

    def __post_init__(self) -> None:
        _validate_refinement_outcome(self)
        _validate_qualified_refinements(self, expected_converged=True)


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2MomentumRefinementUnresolved(
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalysis
):
    """Retain a qualified study without the required final stability evidence."""

    request: Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest
    mesh_analyses: tuple[Periodic1DEmbeddedSubspaceRank2Analysis, ...]
    refinements: tuple[Periodic1DEmbeddedSubspaceRank2MomentumRefinementStep, ...]

    def __post_init__(self) -> None:
        _validate_refinement_outcome(self)
        _validate_qualified_refinements(self, expected_converged=False)


def _validate_refinement_outcome(
    value: Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalysis,
) -> None:
    if type(value.request) is not (
        Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest
    ):
        raise TypeError("request must be a momentum-refinement request")
    if type(value.mesh_analyses) is not tuple or any(
        type(item) is not Periodic1DEmbeddedSubspaceRank2Analysis
        for item in value.mesh_analyses
    ):
        raise TypeError("mesh_analyses must be a typed tuple")
    if len(value.mesh_analyses) != len(value.request.reciprocal_mesh_sizes):
        raise ValueError("mesh_analyses must cover every declared mesh")
    template = value.request.template_request
    for analysis, size in zip(
        value.mesh_analyses,
        value.request.reciprocal_mesh_sizes,
        strict=True,
    ):
        if analysis.request.reciprocal_mesh_size != size:
            raise ValueError("mesh analysis does not match refinement inventory")
        if (
            replace(
                analysis.request,
                reciprocal_mesh_size=template.reciprocal_mesh_size,
            )
            != template
        ):
            raise ValueError("mesh analysis changes a non-mesh control")
    if type(value.refinements) is not tuple or any(
        type(item) is not Periodic1DEmbeddedSubspaceRank2MomentumRefinementStep
        for item in value.refinements
    ):
        raise TypeError("refinements must be a typed tuple")


def _validate_qualified_refinements(
    value: Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalysis,
    *,
    expected_converged: bool,
) -> None:
    if not all(item.qualification.qualified for item in value.mesh_analyses):
        raise ValueError("qualified refinement outcome requires qualified meshes")
    expected_pairs = tuple(pairwise(value.request.reciprocal_mesh_sizes))
    actual_pairs = tuple(
        (item.coarse_mesh_size, item.fine_mesh_size) for item in value.refinements
    )
    if actual_pairs != expected_pairs:
        raise ValueError("refinements must match every adjacent mesh pair")
    for item in value.refinements:
        if item.within_tolerances is not _within_thresholds(
            item, value.request.thresholds
        ):
            raise ValueError("refinement disposition does not match thresholds")
    required = value.request.required_stable_refinements
    converged = all(item.within_tolerances for item in value.refinements[-required:])
    if converged is not expected_converged:
        raise ValueError("outcome variant does not match final refinements")


def _within_thresholds(
    step: Periodic1DEmbeddedSubspaceRank2MomentumRefinementStep,
    thresholds: Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds,
) -> bool:
    return (
        step.maximizing_angle_dispositions_stable
        and step.maximum_parent_diagnostic_change
        <= thresholds.maximum_parent_diagnostic_change
        and step.maximum_correlation_change <= thresholds.maximum_correlation_change
        and step.maximum_threshold_change <= thresholds.maximum_threshold_change
        and step.maximum_hopping_weight_change
        <= thresholds.maximum_hopping_weight_change
        and step.maximum_hopping_power_change <= thresholds.maximum_hopping_power_change
        and step.maximum_angle_change <= thresholds.maximum_angle_change
        and step.maximum_band_defect <= thresholds.maximum_band_defect
        and step.maximum_reconstruction_defect
        <= thresholds.maximum_reconstruction_defect
        and step.maximum_parseval_defect <= thresholds.maximum_parseval_defect
    )


class Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalyzer:
    """Compose exact single-mesh owners and compare nested finite calculations."""

    __slots__ = ("_request", "_transporter")

    def __init__(
        self,
        *,
        request: Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest,
        transporter: ClosedLoopPolarFrameTransporter,
    ) -> None:
        if type(request) is not (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest
        ):
            raise TypeError("request must be a momentum-refinement request")
        if type(transporter) is not ClosedLoopPolarFrameTransporter:
            raise TypeError("transporter must be ClosedLoopPolarFrameTransporter")
        self._request = request
        self._transporter = transporter

    @property
    def request(self) -> Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest:
        """Return the immutable constructor-bound request."""
        return self._request

    def execute(self) -> Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalysis:
        """Return a qualification stop, converged result, or unresolved result."""
        mesh_analyses = tuple(
            Periodic1DEmbeddedSubspaceRank2Analyzer(
                request=self.request.request_at(size),
                transporter=self._transporter,
            ).execute()
            for size in self.request.reciprocal_mesh_sizes
        )
        if not all(item.qualification.qualified for item in mesh_analyses):
            return (
                Periodic1DEmbeddedSubspaceRank2MomentumRefinementQualificationStopped(
                    request=self.request,
                    mesh_analyses=mesh_analyses,
                )
            )
        refinements = tuple(
            self._refinement(coarse, fine) for coarse, fine in pairwise(mesh_analyses)
        )
        required = self.request.required_stable_refinements
        outcome_type = (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementConverged
            if all(item.within_tolerances for item in refinements[-required:])
            else Periodic1DEmbeddedSubspaceRank2MomentumRefinementUnresolved
        )
        return outcome_type(
            request=self.request,
            mesh_analyses=mesh_analyses,
            refinements=refinements,
        )

    def _refinement(
        self,
        coarse: Periodic1DEmbeddedSubspaceRank2Analysis,
        fine: Periodic1DEmbeddedSubspaceRank2Analysis,
    ) -> Periodic1DEmbeddedSubspaceRank2MomentumRefinementStep:
        coarse_qualification = coarse.qualification
        fine_qualification = fine.qualification
        if type(coarse_qualification) is not (
            Periodic1DEmbeddedSubspaceRank2QualifiedParent
        ) or type(fine_qualification) is not (
            Periodic1DEmbeddedSubspaceRank2QualifiedParent
        ):
            raise TypeError("refinement requires two qualified mesh analyses")
        eigenvalue_defect, projector_defect = self._shared_parent_defects(
            coarse.request,
            fine.request,
        )
        parent_change = max(
            eigenvalue_defect,
            projector_defect,
            *(
                abs(
                    getattr(fine_qualification, name)
                    - getattr(coarse_qualification, name)
                )
                for name in (
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
            ),
            *(
                _phase_distance(candidate, expected)
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
            _shared_hopping_power_change(coarse_point, fine_point)
            for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True)
        )
        statuses_stable = all(
            coarse_point.harmonic_maximum.status is fine_point.harmonic_maximum.status
            for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True)
        )
        angle_change = max(
            _angle_change(coarse_point, fine_point)
            for coarse_point, fine_point in zip(coarse.points, fine.points, strict=True)
        )
        step = Periodic1DEmbeddedSubspaceRank2MomentumRefinementStep(
            coarse_mesh_size=coarse.request.reciprocal_mesh_size,
            fine_mesh_size=fine.request.reciprocal_mesh_size,
            maximum_parent_diagnostic_change=parent_change,
            maximum_shared_parent_eigenvalue_defect=eigenvalue_defect,
            maximum_shared_parent_projector_defect=projector_defect,
            maximum_correlation_change=correlation_change,
            maximum_threshold_change=threshold_change,
            maximum_hopping_weight_change=hopping_weight_change,
            maximum_hopping_power_change=hopping_power_change,
            maximum_angle_change=angle_change,
            maximizing_angle_dispositions_stable=statuses_stable,
            maximum_band_defect=max(point.maximum_band_defect for point in fine.points),
            maximum_reconstruction_defect=max(
                point.minimum_loss_reconstruction_defect for point in fine.points
            ),
            maximum_parseval_defect=max(
                max(point.reference_parseval_defect, point.comparison_parseval_defect)
                for point in fine.points
            ),
            within_tolerances=False,
        )
        return replace(
            step,
            within_tolerances=_within_thresholds(step, self.request.thresholds),
        )

    @staticmethod
    def _shared_parent_defects(
        coarse_request: Periodic1DEmbeddedSubspaceRank2Request,
        fine_request: Periodic1DEmbeddedSubspaceRank2Request,
    ) -> tuple[float, float]:
        coarse = _Periodic1DEmbeddedSubspaceRank2ParentConstructor(
            coarse_request
        ).execute()
        fine = _Periodic1DEmbeddedSubspaceRank2ParentConstructor(fine_request).execute()
        shared_eigenvalues = fine.eigenvalues[::2]
        eigenvalue_defect = float(
            np.max(np.abs(shared_eigenvalues - coarse.eigenvalues))
        )
        coarse_projectors = (
            coarse.raw_retained_frames
            @ coarse.raw_retained_frames.conj().transpose(0, 2, 1)
        )
        shared_frames = fine.raw_retained_frames[::2]
        fine_projectors = shared_frames @ shared_frames.conj().transpose(0, 2, 1)
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


def _phase_distance(left: float, right: float) -> float:
    raw = abs(left - right) % (2.0 * math.pi)
    return min(raw, 2.0 * math.pi - raw)


def _angle_change(
    coarse: Periodic1DEmbeddedSubspaceRank2PointAnalysis,
    fine: Periodic1DEmbeddedSubspaceRank2PointAnalysis,
) -> float:
    coarse_angle = coarse.harmonic_maximum.canonical_maximizing_argument
    fine_angle = fine.harmonic_maximum.canonical_maximizing_argument
    if coarse_angle is None and fine_angle is None:
        return 0.0
    if coarse_angle is None or fine_angle is None:
        return coarse.harmonic_maximum.fundamental_period
    period = coarse.harmonic_maximum.fundamental_period
    raw = abs(fine_angle - coarse_angle) % period
    return min(raw, period - raw)


def _shared_hopping_power_change(
    coarse: Periodic1DEmbeddedSubspaceRank2PointAnalysis,
    fine: Periodic1DEmbeddedSubspaceRank2PointAnalysis,
) -> float:
    fine_by_displacement = {item.displacement: item for item in fine.hopping_powers}
    return max(
        max(
            abs(
                fine_by_displacement[
                    item.displacement
                ].reference_normalized_squared_frobenius_norm
                - item.reference_normalized_squared_frobenius_norm
            ),
            abs(
                fine_by_displacement[
                    item.displacement
                ].comparison_normalized_squared_frobenius_norm
                - item.comparison_normalized_squared_frobenius_norm
            ),
        )
        for item in coarse.hopping_powers
    )


__all__ = [
    "Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalysis",
    "Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalyzer",
    "Periodic1DEmbeddedSubspaceRank2MomentumRefinementConverged",
    "Periodic1DEmbeddedSubspaceRank2MomentumRefinementQualificationStopped",
    "Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest",
    "Periodic1DEmbeddedSubspaceRank2MomentumRefinementStep",
    "Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds",
    "Periodic1DEmbeddedSubspaceRank2MomentumRefinementUnresolved",
]
