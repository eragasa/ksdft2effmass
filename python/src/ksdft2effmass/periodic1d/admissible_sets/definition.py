"""Typed configuration and request for constrained admissible-set analysis."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass, field
from math import isfinite
from typing import Self

from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..rank2.band_alignment.composite.result import (
    Periodic1DCompositeBandAlignmentCalculationResult,
)


def _finite_float(name: str, value: float) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


def _positive_float(name: str, value: float) -> None:
    _finite_float(name, value)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")


@dataclass(frozen=True, slots=True)
class Periodic1DAdmissibleSetThresholds(BaseTypedRecord):
    """Freeze one named pair of dimensionless RMS design thresholds."""

    case_id: str
    spectral_rms_threshold: float
    operator_rms_threshold: float

    def __post_init__(self) -> None:
        if type(self.case_id) is not str or not self.case_id:
            raise ValueError("case_id must be a nonempty built-in string")
        _positive_float("spectral_rms_threshold", self.spectral_rms_threshold)
        _positive_float("operator_rms_threshold", self.operator_rms_threshold)

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "case_id": self.case_id,
            "spectral_rms_threshold": self.spectral_rms_threshold,
            "operator_rms_threshold": self.operator_rms_threshold,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "case_id",
            "spectral_rms_threshold",
            "operator_rms_threshold",
        }:
            raise ValueError("threshold fields do not match")
        case_id = values["case_id"]
        spectral = values["spectral_rms_threshold"]
        operator = values["operator_rms_threshold"]
        if (
            type(case_id) is not str
            or type(spectral) is not float
            or type(operator) is not float
        ):
            raise TypeError("threshold fields decode to wrong types")
        return cls(case_id, spectral, operator)


@dataclass(frozen=True, slots=True)
class Periodic1DConstrainedAdmissibleSetConfiguration(BaseTypedRecord):
    """Freeze M3 controls and an exact canonical upstream-result identity."""

    calculation_id: str
    upstream_result_sha256: str
    energy_shift_ratio_bounds: tuple[float, float]
    splitting_scale_bounds: tuple[float, float]
    alignment_angles: tuple[float, ...]
    loss_energy_scale: ScalarQuantity
    compatible_thresholds: Periodic1DAdmissibleSetThresholds
    separated_thresholds: Periodic1DAdmissibleSetThresholds
    compatible_witness: tuple[float, float]
    locality_ranges: tuple[int, ...]
    separation_resolution: float
    quadratic_absolute_tolerance: float
    verification_absolute_tolerance: float

    def __post_init__(self) -> None:
        if type(self.calculation_id) is not str or not self.calculation_id:
            raise ValueError("calculation_id must be a nonempty built-in string")
        if (
            type(self.upstream_result_sha256) is not str
            or len(self.upstream_result_sha256) != 64
            or any(
                character not in "0123456789abcdef"
                for character in self.upstream_result_sha256
            )
        ):
            raise ValueError("upstream_result_sha256 must be a lowercase SHA-256")
        for name, bounds in (
            ("energy_shift_ratio_bounds", self.energy_shift_ratio_bounds),
            ("splitting_scale_bounds", self.splitting_scale_bounds),
        ):
            if not isinstance(bounds, tuple) or len(bounds) != 2:
                raise TypeError(f"{name} must be a length-two tuple")
            _finite_float(f"{name}[0]", bounds[0])
            _finite_float(f"{name}[1]", bounds[1])
            if bounds[0] >= bounds[1]:
                raise ValueError(f"{name} must be strictly increasing")
        if self.splitting_scale_bounds[0] <= 0.0:
            raise ValueError("splitting_scale_bounds must remain strictly positive")
        if (
            not isinstance(self.alignment_angles, tuple)
            or len(self.alignment_angles) < 2
        ):
            raise TypeError("alignment_angles must contain at least two values")
        for index, angle in enumerate(self.alignment_angles):
            _finite_float(f"alignment_angles[{index}]", angle)
        if tuple(sorted(set(self.alignment_angles))) != self.alignment_angles:
            raise ValueError("alignment_angles must be unique and strictly increasing")
        if not any(angle != 0.0 for angle in self.alignment_angles):
            raise ValueError("alignment family must contain a nonidentity rotation")
        if type(self.loss_energy_scale) is not ScalarQuantity:
            raise TypeError("loss_energy_scale must be ScalarQuantity")
        if not isinstance(self.loss_energy_scale.unit, Unitless):
            raise ValueError(
                "loss_energy_scale must use the unitless parent-energy unit"
            )
        if self.loss_energy_scale.magnitude <= 0.0:
            raise ValueError("loss_energy_scale must be positive")
        if (
            type(self.compatible_thresholds) is not Periodic1DAdmissibleSetThresholds
            or type(self.separated_thresholds) is not Periodic1DAdmissibleSetThresholds
        ):
            raise TypeError("threshold controls have the wrong exact type")
        if self.compatible_thresholds.case_id == self.separated_thresholds.case_id:
            raise ValueError("threshold cases must have distinct identities")
        if (
            not isinstance(self.compatible_witness, tuple)
            or len(self.compatible_witness) != 2
        ):
            raise TypeError("compatible_witness must be a length-two tuple")
        for index, value in enumerate(self.compatible_witness):
            _finite_float(f"compatible_witness[{index}]", value)
        if not self.contains(self.compatible_witness):
            raise ValueError("compatible_witness must lie in the parameter domain")
        if not isinstance(self.locality_ranges, tuple) or not self.locality_ranges:
            raise TypeError("locality_ranges must be a nonempty tuple")
        if any(type(value) is not int for value in self.locality_ranges):
            raise TypeError("locality_ranges must contain built-in integers")
        if tuple(sorted(set(self.locality_ranges))) != self.locality_ranges:
            raise ValueError("locality_ranges must be unique and strictly increasing")
        if self.locality_ranges[0] < 0:
            raise ValueError("locality_ranges must be nonnegative")
        _positive_float("separation_resolution", self.separation_resolution)
        _positive_float(
            "quadratic_absolute_tolerance", self.quadratic_absolute_tolerance
        )
        _positive_float(
            "verification_absolute_tolerance", self.verification_absolute_tolerance
        )

    def contains(self, parameter: tuple[float, float]) -> bool:
        """Return whether a strict numeric pair lies in the closed rectangle."""
        if not isinstance(parameter, tuple) or len(parameter) != 2:
            raise TypeError("parameter must be a length-two tuple")
        for index, value in enumerate(parameter):
            _finite_float(f"parameter[{index}]", value)
        return (
            self.energy_shift_ratio_bounds[0]
            <= parameter[0]
            <= self.energy_shift_ratio_bounds[1]
            and self.splitting_scale_bounds[0]
            <= parameter[1]
            <= self.splitting_scale_bounds[1]
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "calculation_id": self.calculation_id,
            "upstream_result_sha256": self.upstream_result_sha256,
            "energy_shift_ratio_bounds": self.energy_shift_ratio_bounds,
            "splitting_scale_bounds": self.splitting_scale_bounds,
            "alignment_angles": self.alignment_angles,
            "loss_energy_scale": self.loss_energy_scale,
            "compatible_thresholds": self.compatible_thresholds,
            "separated_thresholds": self.separated_thresholds,
            "compatible_witness": self.compatible_witness,
            "locality_ranges": self.locality_ranges,
            "separation_resolution": self.separation_resolution,
            "quadratic_absolute_tolerance": self.quadratic_absolute_tolerance,
            "verification_absolute_tolerance": self.verification_absolute_tolerance,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "calculation_id",
            "upstream_result_sha256",
            "energy_shift_ratio_bounds",
            "splitting_scale_bounds",
            "alignment_angles",
            "loss_energy_scale",
            "compatible_thresholds",
            "separated_thresholds",
            "compatible_witness",
            "locality_ranges",
            "separation_resolution",
            "quadratic_absolute_tolerance",
            "verification_absolute_tolerance",
        }
        if set(values) != required:
            raise ValueError("configuration fields do not match")
        calculation_id = values["calculation_id"]
        digest = values["upstream_result_sha256"]
        scale = values["loss_energy_scale"]
        compatible = values["compatible_thresholds"]
        separated = values["separated_thresholds"]
        if type(calculation_id) is not str or type(digest) is not str:
            raise TypeError("configuration identities must decode to strings")
        if type(scale) is not ScalarQuantity:
            raise TypeError("loss_energy_scale must decode to ScalarQuantity")
        if not isinstance(compatible, Mapping) or not isinstance(separated, Mapping):
            raise TypeError("thresholds must decode to mappings")

        def float_pair(name: str) -> tuple[float, float]:
            value = values[name]
            if (
                not isinstance(value, tuple)
                or len(value) != 2
                or any(type(item) is not float for item in value)
            ):
                raise TypeError(f"{name} must decode to a float pair")
            return value

        angles = values["alignment_angles"]
        ranges = values["locality_ranges"]
        if not isinstance(angles, tuple) or any(
            type(item) is not float for item in angles
        ):
            raise TypeError("alignment_angles must decode to floats")
        if not isinstance(ranges, tuple) or any(
            type(item) is not int for item in ranges
        ):
            raise TypeError("locality_ranges must decode to integers")
        separation_resolution = values["separation_resolution"]
        quadratic_absolute_tolerance = values["quadratic_absolute_tolerance"]
        verification_absolute_tolerance = values["verification_absolute_tolerance"]
        if type(separation_resolution) is not float:
            raise TypeError("separation_resolution must decode to a float")
        if type(quadratic_absolute_tolerance) is not float:
            raise TypeError("quadratic_absolute_tolerance must decode to a float")
        if type(verification_absolute_tolerance) is not float:
            raise TypeError("verification_absolute_tolerance must decode to a float")
        return cls(
            calculation_id=calculation_id,
            upstream_result_sha256=digest,
            energy_shift_ratio_bounds=float_pair("energy_shift_ratio_bounds"),
            splitting_scale_bounds=float_pair("splitting_scale_bounds"),
            alignment_angles=angles,
            loss_energy_scale=scale,
            compatible_thresholds=Periodic1DAdmissibleSetThresholds.from_dict(
                compatible
            ),
            separated_thresholds=Periodic1DAdmissibleSetThresholds.from_dict(separated),
            compatible_witness=float_pair("compatible_witness"),
            locality_ranges=ranges,
            separation_resolution=separation_resolution,
            quadratic_absolute_tolerance=quadratic_absolute_tolerance,
            verification_absolute_tolerance=verification_absolute_tolerance,
        )


@dataclass(frozen=True, slots=True)
class Periodic1DConstrainedAdmissibleSetAnalysisRequest:
    """Bind one configuration to exact canonical upstream result bytes."""

    configuration: Periodic1DConstrainedAdmissibleSetConfiguration
    upstream_result_wire: bytes
    _upstream_result: Periodic1DCompositeBandAlignmentCalculationResult = field(
        init=False,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        if (
            type(self.configuration)
            is not Periodic1DConstrainedAdmissibleSetConfiguration
        ):
            raise TypeError("configuration has the wrong exact type")
        if type(self.upstream_result_wire) is not bytes:
            raise TypeError("upstream_result_wire must be built-in bytes")
        upstream = Periodic1DCompositeBandAlignmentCalculationResult.from_json(
            self.upstream_result_wire
        )
        if upstream.to_json() != self.upstream_result_wire:
            raise ValueError("upstream_result_wire must be canonical typed JSON bytes")
        if (
            hashlib.sha256(self.upstream_result_wire).hexdigest()
            != self.configuration.upstream_result_sha256
        ):
            raise ValueError("upstream result bytes differ from the configured SHA-256")
        if upstream.configuration.retained_rank != 2:
            raise ValueError(
                "admissible-set analysis requires a rank-two upstream result"
            )
        if (
            self.configuration.locality_ranges[-1]
            >= upstream.configuration.construction_size // 2
        ):
            raise ValueError("locality ranges must exclude the cyclic Nyquist class")
        object.__setattr__(self, "_upstream_result", upstream)

    @property
    def upstream_result(self) -> Periodic1DCompositeBandAlignmentCalculationResult:
        """Return the typed result reconstructed from the exact admitted bytes."""
        return self._upstream_result


__all__ = [
    "Periodic1DAdmissibleSetThresholds",
    "Periodic1DConstrainedAdmissibleSetAnalysisRequest",
    "Periodic1DConstrainedAdmissibleSetConfiguration",
]
