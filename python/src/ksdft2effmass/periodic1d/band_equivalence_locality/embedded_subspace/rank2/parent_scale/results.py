"""Serialization-free values for the nonflat embedded-subspace/rank2 parent control."""

from __future__ import annotations

import math
from abc import ABC
from dataclasses import dataclass
from typing import final

from projectkoios.optimization.alignment.closed_loop_polar_transport import (
    ClosedLoopPolarFrameTransportBackendFailureReason,
    ClosedLoopPolarFrameTransportBackendOperation,
    ClosedLoopPolarFrameTransportStatus,
)
from projectkoios.optimization.selection.harmonic import PeriodicHarmonicMaximum

from ksdft2effmass.periodic1d.hopping_locality import Periodic1DHoppingLocality
from ksdft2effmass.representation_equivalence import RepresentationEquivalence

from .request import Periodic1DRank2Request


def _nonnegative_float(value: float, name: str) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


class Periodic1DRank2Qualification(ABC):
    """Identify one closed qualification outcome variant."""

    __slots__ = ()

    minimum_external_gap: float

    @property
    @final
    def qualified(self) -> bool:
        """Return whether parent and transport gates both passed."""
        return type(self) is Periodic1DRank2QualifiedParent


@dataclass(frozen=True, slots=True)
class Periodic1DRank2ExternalGapFailure(Periodic1DRank2Qualification):
    """Retain an external-gap failure before transport is attempted."""

    minimum_external_gap: float

    def __post_init__(self) -> None:
        _nonnegative_float(self.minimum_external_gap, "minimum_external_gap")


@dataclass(frozen=True, slots=True)
class Periodic1DRank2BandTransportBackendFailure(Periodic1DRank2Qualification):
    """Retain a typed transport backend stop without numerical substitution."""

    minimum_external_gap: float
    operation: ClosedLoopPolarFrameTransportBackendOperation
    reason: ClosedLoopPolarFrameTransportBackendFailureReason
    link_index: int

    def __post_init__(self) -> None:
        _nonnegative_float(self.minimum_external_gap, "minimum_external_gap")
        if type(self.operation) is not ClosedLoopPolarFrameTransportBackendOperation:
            raise TypeError("operation must be a band-transport backend operation")
        if type(self.reason) is not ClosedLoopPolarFrameTransportBackendFailureReason:
            raise TypeError("reason must be a band-transport backend failure reason")
        if type(self.link_index) is not int:
            raise TypeError("link_index must be a built-in int")
        if self.link_index < 0:
            raise ValueError("link_index must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DRank2BandTransportNumericallyUnresolved(Periodic1DRank2Qualification):
    """Retain a numerical transport stop reported by the transport owner."""

    minimum_external_gap: float
    band_transport_status: ClosedLoopPolarFrameTransportStatus
    minimum_transport_singular_value: float

    def __post_init__(self) -> None:
        _nonnegative_float(self.minimum_external_gap, "minimum_external_gap")
        _nonnegative_float(
            self.minimum_transport_singular_value,
            "minimum_transport_singular_value",
        )
        if type(self.band_transport_status) is not ClosedLoopPolarFrameTransportStatus:
            raise TypeError("band_transport_status must be a band-transport status")
        if self.band_transport_status is ClosedLoopPolarFrameTransportStatus.QUALIFIED:
            raise ValueError("numerically unresolved transport cannot be qualified")


@dataclass(frozen=True, slots=True)
class Periodic1DRank2BandTransportThresholdFailure(Periodic1DRank2Qualification):
    """Retain failure of the stricter scientific transport threshold."""

    minimum_external_gap: float
    minimum_transport_singular_value: float

    def __post_init__(self) -> None:
        _nonnegative_float(self.minimum_external_gap, "minimum_external_gap")
        _nonnegative_float(
            self.minimum_transport_singular_value,
            "minimum_transport_singular_value",
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2QualifiedParent(Periodic1DRank2Qualification):
    """Retain complete diagnostics only for a fully qualified parent."""

    minimum_external_gap: float
    minimum_transport_singular_value: float
    maximum_transport_rank_cutoff: float
    maximum_transport_unitarity_defect: float
    maximum_primitive_link_frobenius_residual: float
    closure_holonomy_phases: tuple[float, ...]
    closure_alignment_residual: float
    closure_alignment_unitarity_defect: float
    maximum_frame_orthonormality_defect: float
    maximum_reference_hermiticity_defect: float

    def __post_init__(self) -> None:
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
        ):
            _nonnegative_float(getattr(self, name), name)
        if (
            type(self.closure_holonomy_phases) is not tuple
            or len(self.closure_holonomy_phases) != 2
        ):
            raise TypeError("closure_holonomy_phases must contain two phases")
        for phase in self.closure_holonomy_phases:
            if type(phase) is not float or not math.isfinite(phase):
                raise TypeError("closure phases must be finite built-in floats")
            if not -math.pi <= phase <= math.pi:
                raise ValueError("closure phases must lie in [-pi, pi]")
        if self.closure_holonomy_phases != tuple(sorted(self.closure_holonomy_phases)):
            raise ValueError("closure phases must be ordered")


@dataclass(frozen=True, slots=True)
class Periodic1DRank2HoppingPower(Periodic1DHoppingLocality):
    """Retain reference and attacked block power at one cyclic representative."""

    displacement: int
    reference_normalized_squared_frobenius_norm: float
    comparison_normalized_squared_frobenius_norm: float

    def __post_init__(self) -> None:
        if type(self.displacement) is not int:
            raise TypeError("displacement must be a built-in int")
        _nonnegative_float(
            self.reference_normalized_squared_frobenius_norm,
            "reference_normalized_squared_frobenius_norm",
        )
        _nonnegative_float(
            self.comparison_normalized_squared_frobenius_norm,
            "comparison_normalized_squared_frobenius_norm",
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2PointAnalysis(RepresentationEquivalence):
    """Retain nonflat band, restricted-alignment, and hopping channels."""

    amplitude: float
    maximum_band_defect: float
    splitting_scale: float
    harmonic_maximum: PeriodicHarmonicMaximum
    discrete_maximum_correlation: float
    minimum_operator_threshold: float
    exact_spectrum_joint_operator_threshold: float
    minimum_loss_reconstruction_defect: float
    reference_nonzero_hopping_weight: float
    comparison_nonzero_hopping_weight: float
    reference_parseval_defect: float
    comparison_parseval_defect: float
    hopping_powers: tuple[Periodic1DRank2HoppingPower, ...]

    def __post_init__(self) -> None:
        for name in (
            "amplitude",
            "maximum_band_defect",
            "splitting_scale",
            "minimum_operator_threshold",
            "exact_spectrum_joint_operator_threshold",
            "minimum_loss_reconstruction_defect",
            "reference_nonzero_hopping_weight",
            "comparison_nonzero_hopping_weight",
            "reference_parseval_defect",
            "comparison_parseval_defect",
        ):
            _nonnegative_float(getattr(self, name), name)
        if self.splitting_scale == 0.0:
            raise ValueError("splitting_scale must be positive")
        if type(self.discrete_maximum_correlation) is not float or not math.isfinite(
            self.discrete_maximum_correlation
        ):
            raise TypeError("discrete_maximum_correlation must be a finite float")
        if not -1.0 <= self.discrete_maximum_correlation <= 1.0:
            raise ValueError("discrete_maximum_correlation must lie in [-1, 1]")
        if type(self.harmonic_maximum) is not PeriodicHarmonicMaximum:
            raise TypeError("harmonic_maximum must be PeriodicHarmonicMaximum")
        if type(self.hopping_powers) is not tuple or not self.hopping_powers:
            raise TypeError("hopping_powers must be a nonempty tuple")
        if any(
            type(item) is not Periodic1DRank2HoppingPower
            for item in self.hopping_powers
        ):
            raise TypeError(
                "hopping_powers must contain embedded-subspace/rank2 hopping powers"
            )
        displacements = tuple(item.displacement for item in self.hopping_powers)
        if tuple(sorted(set(displacements))) != displacements or 0 not in displacements:
            raise ValueError(
                "hopping displacements must be ordered, unique, and include zero"
            )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2Analysis:
    """Retain one qualified or explicitly stopped calculation."""

    request: Periodic1DRank2Request
    qualification: Periodic1DRank2Qualification
    points: tuple[Periodic1DRank2PointAnalysis, ...]

    def __post_init__(self) -> None:
        if type(self.request) is not Periodic1DRank2Request:
            raise TypeError("request must be Periodic1DRank2Request")
        allowed_qualification_types = (
            Periodic1DRank2ExternalGapFailure,
            Periodic1DRank2BandTransportBackendFailure,
            Periodic1DRank2BandTransportNumericallyUnresolved,
            Periodic1DRank2BandTransportThresholdFailure,
            Periodic1DRank2QualifiedParent,
        )
        if type(self.qualification) not in allowed_qualification_types:
            raise TypeError("qualification must be one closed rank-two outcome variant")
        external_gap_failed = (
            type(self.qualification) is Periodic1DRank2ExternalGapFailure
        )
        if external_gap_failed is not (
            self.qualification.minimum_external_gap < self.request.minimum_external_gap
        ):
            raise ValueError("external-gap disposition must match the request gate")
        if type(self.qualification) is Periodic1DRank2QualifiedParent:
            if (
                self.qualification.minimum_transport_singular_value
                <= self.request.minimum_transport_singular_value
            ):
                raise ValueError(
                    "qualified transport must pass the scientific threshold"
                )
        if (
            type(self.qualification) is Periodic1DRank2BandTransportThresholdFailure
            and self.qualification.minimum_transport_singular_value
            > self.request.minimum_transport_singular_value
        ):
            raise ValueError("transport-threshold failure must match its gate")
        if type(self.points) is not tuple or any(
            type(point) is not Periodic1DRank2PointAnalysis for point in self.points
        ):
            raise TypeError("points must be a typed tuple")
        expected = self.request.amplitudes if self.qualification.qualified else ()
        if tuple(point.amplitude for point in self.points) != expected:
            raise ValueError("points must match amplitudes exactly when qualified")


__all__ = [
    "Periodic1DRank2Analysis",
    "Periodic1DRank2ExternalGapFailure",
    "Periodic1DRank2HoppingPower",
    "Periodic1DRank2PointAnalysis",
    "Periodic1DRank2Qualification",
    "Periodic1DRank2QualifiedParent",
    "Periodic1DRank2BandTransportBackendFailure",
    "Periodic1DRank2BandTransportNumericallyUnresolved",
    "Periodic1DRank2BandTransportThresholdFailure",
]
