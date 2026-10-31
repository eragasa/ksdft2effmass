"""Serialization-free truncation consequences for embedded rank-two fields."""

from __future__ import annotations

import math
from abc import ABC
from dataclasses import dataclass

from ..results import (
    Periodic1DEmbeddedSubspaceRank2BandTransportBackendFailure,
    Periodic1DEmbeddedSubspaceRank2BandTransportNumericallyUnresolved,
    Periodic1DEmbeddedSubspaceRank2BandTransportThresholdFailure,
    Periodic1DEmbeddedSubspaceRank2ExternalGapFailure,
    Periodic1DEmbeddedSubspaceRank2Qualification,
    Periodic1DEmbeddedSubspaceRank2QualifiedParent,
)
from .request import Periodic1DEmbeddedSubspaceRank2TruncationRequest


def _nonnegative(value: float, name: str) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2TruncationRange:
    """Retain consequences of one conjugate-closed ordinary cutoff."""

    maximum_range: int
    reference_ordinary_omitted_power: float
    comparison_ordinary_omitted_power: float
    reference_total_omitted_power: float
    comparison_total_omitted_power: float
    reference_truncation_hamiltonian_maximum_error: float
    reference_truncation_hamiltonian_rms_error: float
    reference_truncation_spectral_maximum_error: float
    reference_truncation_spectral_rms_error: float
    comparison_truncation_hamiltonian_maximum_error: float
    comparison_truncation_hamiltonian_rms_error: float
    comparison_truncation_spectral_maximum_error: float
    comparison_truncation_spectral_rms_error: float
    comparison_total_hamiltonian_maximum_error: float
    comparison_total_hamiltonian_rms_error: float
    comparison_total_spectral_maximum_error: float
    comparison_total_spectral_rms_error: float

    def __post_init__(self) -> None:
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if self.maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        for name in (
            "reference_ordinary_omitted_power",
            "comparison_ordinary_omitted_power",
            "reference_total_omitted_power",
            "comparison_total_omitted_power",
            "reference_truncation_hamiltonian_maximum_error",
            "reference_truncation_hamiltonian_rms_error",
            "reference_truncation_spectral_maximum_error",
            "reference_truncation_spectral_rms_error",
            "comparison_truncation_hamiltonian_maximum_error",
            "comparison_truncation_hamiltonian_rms_error",
            "comparison_truncation_spectral_maximum_error",
            "comparison_truncation_spectral_rms_error",
            "comparison_total_hamiltonian_maximum_error",
            "comparison_total_hamiltonian_rms_error",
            "comparison_total_spectral_maximum_error",
            "comparison_total_spectral_rms_error",
        ):
            _nonnegative(getattr(self, name), name)
        if self.reference_total_omitted_power < self.reference_ordinary_omitted_power:
            raise ValueError("reference total omitted power must include Nyquist power")
        if self.comparison_total_omitted_power < self.comparison_ordinary_omitted_power:
            raise ValueError(
                "comparison total omitted power must include Nyquist power"
            )


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2TruncationPoint:
    """Retain conversion, interpolation, and truncation channels at one amplitude."""

    amplitude: float
    reference_nyquist_power: float
    comparison_nyquist_power: float
    reference_ordinary_hermiticity_maximum_defect: float
    comparison_ordinary_hermiticity_maximum_defect: float
    direct_spectral_maximum_defect: float
    comparison_interpolation_hamiltonian_maximum_error: float
    comparison_interpolation_hamiltonian_rms_error: float
    comparison_interpolation_spectral_maximum_error: float
    comparison_interpolation_spectral_rms_error: float
    ranges: tuple[Periodic1DEmbeddedSubspaceRank2TruncationRange, ...]

    def __post_init__(self) -> None:
        for name in (
            "amplitude",
            "reference_nyquist_power",
            "comparison_nyquist_power",
            "reference_ordinary_hermiticity_maximum_defect",
            "comparison_ordinary_hermiticity_maximum_defect",
            "direct_spectral_maximum_defect",
            "comparison_interpolation_hamiltonian_maximum_error",
            "comparison_interpolation_hamiltonian_rms_error",
            "comparison_interpolation_spectral_maximum_error",
            "comparison_interpolation_spectral_rms_error",
        ):
            _nonnegative(getattr(self, name), name)
        if type(self.ranges) is not tuple or not self.ranges:
            raise TypeError("ranges must be a nonempty tuple")
        if any(
            type(item) is not Periodic1DEmbeddedSubspaceRank2TruncationRange
            for item in self.ranges
        ):
            raise TypeError("ranges must contain truncation range values")
        inventory = tuple(item.maximum_range for item in self.ranges)
        if inventory != tuple(sorted(set(inventory))):
            raise ValueError("range results must be unique and strictly increasing")
        if any(
            item.reference_total_omitted_power
            != item.reference_ordinary_omitted_power + self.reference_nyquist_power
            for item in self.ranges
        ):
            raise ValueError("reference total power must equal ordinary plus Nyquist")
        if any(
            item.comparison_total_omitted_power
            != item.comparison_ordinary_omitted_power + self.comparison_nyquist_power
            for item in self.ranges
        ):
            raise ValueError("comparison total power must equal ordinary plus Nyquist")


class Periodic1DEmbeddedSubspaceRank2TruncationAnalysis(ABC):
    """Identify one closed truncation outcome variant."""

    __slots__ = ()

    request: Periodic1DEmbeddedSubspaceRank2TruncationRequest
    qualification: Periodic1DEmbeddedSubspaceRank2Qualification

    @property
    def completed(self) -> bool:
        """Return whether qualification passed and consequences were evaluated."""
        return type(self) is Periodic1DEmbeddedSubspaceRank2TruncationCompleted


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2TruncationQualificationStopped(
    Periodic1DEmbeddedSubspaceRank2TruncationAnalysis
):
    """Retain qualification evidence when truncation evaluation cannot begin."""

    request: Periodic1DEmbeddedSubspaceRank2TruncationRequest
    qualification: Periodic1DEmbeddedSubspaceRank2Qualification

    def __post_init__(self) -> None:
        if type(self.request) is not Periodic1DEmbeddedSubspaceRank2TruncationRequest:
            raise TypeError("request must be a truncation request")
        if type(self.qualification) not in (
            Periodic1DEmbeddedSubspaceRank2ExternalGapFailure,
            Periodic1DEmbeddedSubspaceRank2BandTransportBackendFailure,
            Periodic1DEmbeddedSubspaceRank2BandTransportNumericallyUnresolved,
            Periodic1DEmbeddedSubspaceRank2BandTransportThresholdFailure,
        ):
            raise TypeError("qualification must be one closed unqualified variant")
        gap_failed = type(self.qualification) is (
            Periodic1DEmbeddedSubspaceRank2ExternalGapFailure
        )
        if gap_failed is not (
            self.qualification.minimum_external_gap
            < self.request.template_request.minimum_external_gap
        ):
            raise ValueError("external-gap disposition must match the request gate")
        if type(self.qualification) is (
            Periodic1DEmbeddedSubspaceRank2BandTransportThresholdFailure
        ) and (
            self.qualification.minimum_transport_singular_value
            > self.request.template_request.minimum_transport_singular_value
        ):
            raise ValueError("transport-threshold failure must match its gate")


@dataclass(frozen=True, slots=True)
class Periodic1DEmbeddedSubspaceRank2TruncationCompleted(
    Periodic1DEmbeddedSubspaceRank2TruncationAnalysis
):
    """Retain one complete pointwise finite-range consequence study."""

    request: Periodic1DEmbeddedSubspaceRank2TruncationRequest
    qualification: Periodic1DEmbeddedSubspaceRank2QualifiedParent
    evaluation_coordinate_offset: float
    minimum_construction_evaluation_separation: float
    points: tuple[Periodic1DEmbeddedSubspaceRank2TruncationPoint, ...]

    def __post_init__(self) -> None:
        if type(self.request) is not Periodic1DEmbeddedSubspaceRank2TruncationRequest:
            raise TypeError("request must be a truncation request")
        if type(self.qualification) is not (
            Periodic1DEmbeddedSubspaceRank2QualifiedParent
        ):
            raise TypeError("completed truncation requires a qualified parent")
        if (
            self.qualification.minimum_external_gap
            < self.request.template_request.minimum_external_gap
        ):
            raise ValueError("qualified parent must pass the external-gap gate")
        if (
            self.qualification.minimum_transport_singular_value
            <= self.request.template_request.minimum_transport_singular_value
        ):
            raise ValueError("qualified parent must pass the transport gate")
        _nonnegative(self.evaluation_coordinate_offset, "evaluation_coordinate_offset")
        _nonnegative(
            self.minimum_construction_evaluation_separation,
            "minimum_construction_evaluation_separation",
        )
        expected_offset = 1.0 / float(
            self.request.template_request.reciprocal_mesh_size + 1
        )
        if self.evaluation_coordinate_offset != expected_offset:
            raise ValueError("evaluation coordinate offset must match the request")
        if self.minimum_construction_evaluation_separation == 0.0:
            raise ValueError("construction and evaluation meshes must be disjoint")
        if type(self.points) is not tuple or any(
            type(point) is not Periodic1DEmbeddedSubspaceRank2TruncationPoint
            for point in self.points
        ):
            raise TypeError("points must contain truncation point values")
        if tuple(point.amplitude for point in self.points) != (
            self.request.template_request.amplitudes
        ):
            raise ValueError("point amplitudes must match the template request")
        expected_ranges = self.request.maximum_ranges
        if any(
            tuple(item.maximum_range for item in point.ranges) != expected_ranges
            for point in self.points
        ):
            raise ValueError("every point must report every requested cutoff")
        reference_channels = tuple(
            (
                item.reference_ordinary_omitted_power,
                item.reference_total_omitted_power,
                item.reference_truncation_hamiltonian_maximum_error,
                item.reference_truncation_hamiltonian_rms_error,
                item.reference_truncation_spectral_maximum_error,
                item.reference_truncation_spectral_rms_error,
            )
            for item in self.points[0].ranges
        )
        if any(
            point.reference_nyquist_power != self.points[0].reference_nyquist_power
            or point.reference_ordinary_hermiticity_maximum_defect
            != self.points[0].reference_ordinary_hermiticity_maximum_defect
            or tuple(
                (
                    item.reference_ordinary_omitted_power,
                    item.reference_total_omitted_power,
                    item.reference_truncation_hamiltonian_maximum_error,
                    item.reference_truncation_hamiltonian_rms_error,
                    item.reference_truncation_spectral_maximum_error,
                    item.reference_truncation_spectral_rms_error,
                )
                for item in point.ranges
            )
            != reference_channels
            for point in self.points[1:]
        ):
            raise ValueError("reference channels must be shared by every amplitude")


__all__ = [
    "Periodic1DEmbeddedSubspaceRank2TruncationAnalysis",
    "Periodic1DEmbeddedSubspaceRank2TruncationCompleted",
    "Periodic1DEmbeddedSubspaceRank2TruncationPoint",
    "Periodic1DEmbeddedSubspaceRank2TruncationQualificationStopped",
    "Periodic1DEmbeddedSubspaceRank2TruncationRange",
]
