"""Canonical retained records for periodic-1D band-equivalence locality."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .request import Periodic1DBandEquivalenceLocalityRequest
from .results import (
    Periodic1DBandEquivalenceHoppingPower,
    Periodic1DBandEquivalenceLocalityAnalysis,
    Periodic1DBandEquivalencePointAnalysis,
    Periodic1DBandEquivalenceRangeAnalysis,
)


def _fields(
    values: Mapping[str, SerializableValue], expected: set[str], name: str
) -> None:
    if set(values) != expected:
        raise ValueError(f"{name} fields do not match")


def _integer(values: Mapping[str, SerializableValue], name: str) -> int:
    value = values[name]
    if type(value) is not int:
        raise TypeError(f"{name} must decode to a built-in integer")
    return value


def _floating(values: Mapping[str, SerializableValue], name: str) -> float:
    value = values[name]
    if type(value) is not float:
        raise TypeError(f"{name} must decode to a built-in float")
    return value


def _mapping_value(
    values: Mapping[str, SerializableValue], name: str
) -> Mapping[str, SerializableValue]:
    value = values[name]
    if not isinstance(value, Mapping) or any(type(key) is not str for key in value):
        raise TypeError(f"{name} must decode to a string-keyed mapping")
    return value


def _mapping_tuple(
    values: Mapping[str, SerializableValue], name: str
) -> tuple[Mapping[str, SerializableValue], ...]:
    value = values[name]
    if type(value) is not tuple:
        raise TypeError(f"{name} must decode to a tuple")
    items: list[Mapping[str, SerializableValue]] = []
    for item in value:
        if not isinstance(item, Mapping) or any(type(key) is not str for key in item):
            raise TypeError(f"{name} must contain string-keyed mappings")
        items.append(item)
    return tuple(items)


def _request_mapping(
    request: Periodic1DBandEquivalenceLocalityRequest,
) -> Mapping[str, SerializableValue]:
    return {
        "parent_model_identifier": request.parent_model_identifier,
        "represented_basis_identifier": request.represented_basis_identifier,
        "energy_reference_identifier": request.energy_reference_identifier,
        "reciprocal_coordinate_convention": request.reciprocal_coordinate_convention,
        "gauge_attack_identifier": request.gauge_attack_identifier,
        "construction_size": request.construction_size,
        "evaluation_size": request.evaluation_size,
        "evaluation_shift_numerator": request.evaluation_shift_numerator,
        "evaluation_shift_denominator": request.evaluation_shift_denominator,
        "amplitudes": request.amplitudes,
        "maximum_ranges": request.maximum_ranges,
        "harmonic_absolute_degeneracy_tolerance": (
            request.harmonic_absolute_degeneracy_tolerance
        ),
        "harmonic_relative_degeneracy_tolerance": (
            request.harmonic_relative_degeneracy_tolerance
        ),
        "numerical_absolute_tolerance": request.numerical_absolute_tolerance,
    }


def _request_from_mapping(
    values: Mapping[str, SerializableValue],
) -> Periodic1DBandEquivalenceLocalityRequest:
    _fields(
        values,
        {
            "parent_model_identifier",
            "represented_basis_identifier",
            "energy_reference_identifier",
            "reciprocal_coordinate_convention",
            "gauge_attack_identifier",
            "construction_size",
            "evaluation_size",
            "evaluation_shift_numerator",
            "evaluation_shift_denominator",
            "amplitudes",
            "maximum_ranges",
            "harmonic_absolute_degeneracy_tolerance",
            "harmonic_relative_degeneracy_tolerance",
            "numerical_absolute_tolerance",
        },
        "request mapping",
    )
    identifiers: dict[str, str] = {}
    for name in (
        "parent_model_identifier",
        "represented_basis_identifier",
        "energy_reference_identifier",
        "reciprocal_coordinate_convention",
        "gauge_attack_identifier",
    ):
        identifier = values[name]
        if type(identifier) is not str:
            raise TypeError(f"{name} must decode to a built-in string")
        identifiers[name] = identifier
    amplitudes = values["amplitudes"]
    maximum_ranges = values["maximum_ranges"]
    if type(amplitudes) is not tuple or any(
        type(item) is not float for item in amplitudes
    ):
        raise TypeError("amplitudes must decode to a tuple of floats")
    if type(maximum_ranges) is not tuple or any(
        type(item) is not int for item in maximum_ranges
    ):
        raise TypeError("maximum_ranges must decode to a tuple of integers")
    return Periodic1DBandEquivalenceLocalityRequest(
        parent_model_identifier=identifiers["parent_model_identifier"],
        represented_basis_identifier=identifiers["represented_basis_identifier"],
        energy_reference_identifier=identifiers["energy_reference_identifier"],
        reciprocal_coordinate_convention=identifiers[
            "reciprocal_coordinate_convention"
        ],
        gauge_attack_identifier=identifiers["gauge_attack_identifier"],
        construction_size=_integer(values, "construction_size"),
        evaluation_size=_integer(values, "evaluation_size"),
        evaluation_shift_numerator=_integer(values, "evaluation_shift_numerator"),
        evaluation_shift_denominator=_integer(values, "evaluation_shift_denominator"),
        amplitudes=amplitudes,
        maximum_ranges=maximum_ranges,
        harmonic_absolute_degeneracy_tolerance=_floating(
            values, "harmonic_absolute_degeneracy_tolerance"
        ),
        harmonic_relative_degeneracy_tolerance=_floating(
            values, "harmonic_relative_degeneracy_tolerance"
        ),
        numerical_absolute_tolerance=_floating(values, "numerical_absolute_tolerance"),
    )


@dataclass(frozen=True, slots=True)
class Periodic1DBandEquivalenceHoppingPowerRecord(BaseTypedRecord):
    """Retain one normalized hopping-block power."""

    value: Periodic1DBandEquivalenceHoppingPower

    def __post_init__(self) -> None:
        if type(self.value) is not Periodic1DBandEquivalenceHoppingPower:
            raise TypeError("value must be Periodic1DBandEquivalenceHoppingPower")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "displacement": self.value.displacement,
            "normalized_squared_frobenius_norm": (
                self.value.normalized_squared_frobenius_norm
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(
            values,
            {"displacement", "normalized_squared_frobenius_norm"},
            "hopping-power record",
        )
        return cls(
            Periodic1DBandEquivalenceHoppingPower(
                displacement=_integer(values, "displacement"),
                normalized_squared_frobenius_norm=_floating(
                    values, "normalized_squared_frobenius_norm"
                ),
            )
        )


@dataclass(frozen=True, slots=True)
class Periodic1DBandEquivalenceRangeAnalysisRecord(BaseTypedRecord):
    """Retain one deliberate truncation analysis."""

    value: Periodic1DBandEquivalenceRangeAnalysis

    def __post_init__(self) -> None:
        if type(self.value) is not Periodic1DBandEquivalenceRangeAnalysis:
            raise TypeError("value must be Periodic1DBandEquivalenceRangeAnalysis")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        value = self.value
        return {
            "maximum_range": value.maximum_range,
            "ordinary_omitted_block_l2_norm": value.ordinary_omitted_block_l2_norm,
            "truncation_hamiltonian_maximum_error": (
                value.truncation_hamiltonian_maximum_error
            ),
            "total_hamiltonian_maximum_error": value.total_hamiltonian_maximum_error,
            "truncation_spectral_maximum_error": (
                value.truncation_spectral_maximum_error
            ),
            "total_spectral_maximum_error": value.total_spectral_maximum_error,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(
            values,
            {
                "maximum_range",
                "ordinary_omitted_block_l2_norm",
                "truncation_hamiltonian_maximum_error",
                "total_hamiltonian_maximum_error",
                "truncation_spectral_maximum_error",
                "total_spectral_maximum_error",
            },
            "range-analysis record",
        )
        return cls(
            Periodic1DBandEquivalenceRangeAnalysis(
                maximum_range=_integer(values, "maximum_range"),
                ordinary_omitted_block_l2_norm=_floating(
                    values, "ordinary_omitted_block_l2_norm"
                ),
                truncation_hamiltonian_maximum_error=_floating(
                    values, "truncation_hamiltonian_maximum_error"
                ),
                total_hamiltonian_maximum_error=_floating(
                    values, "total_hamiltonian_maximum_error"
                ),
                truncation_spectral_maximum_error=_floating(
                    values, "truncation_spectral_maximum_error"
                ),
                total_spectral_maximum_error=_floating(
                    values, "total_spectral_maximum_error"
                ),
            )
        )


@dataclass(frozen=True, slots=True)
class Periodic1DBandEquivalencePointAnalysisRecord(BaseTypedRecord):
    """Retain one separated flat-parent point analysis."""

    value: Periodic1DBandEquivalencePointAnalysis

    def __post_init__(self) -> None:
        if type(self.value) is not Periodic1DBandEquivalencePointAnalysis:
            raise TypeError("value must be Periodic1DBandEquivalencePointAnalysis")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        value = self.value
        return {
            "amplitude": value.amplitude,
            "maximum_band_defect": value.maximum_band_defect,
            "discrete_maximum_correlation": value.discrete_maximum_correlation,
            "analytic_maximum_correlation": value.analytic_maximum_correlation,
            "correlation_quadrature_defect": value.correlation_quadrature_defect,
            "global_alignment_angle": value.global_alignment_angle,
            "optimal_splitting_scale": value.optimal_splitting_scale,
            "irreducible_operator_squared_loss": (
                value.irreducible_operator_squared_loss
            ),
            "minimum_operator_threshold": value.minimum_operator_threshold,
            "exact_spectrum_joint_operator_threshold": (
                value.exact_spectrum_joint_operator_threshold
            ),
            "cyclic_nyquist_power": value.cyclic_nyquist_power,
            "reconstruction_maximum_frobenius_error": (
                value.reconstruction_maximum_frobenius_error
            ),
            "interpolation_hamiltonian_maximum_error": (
                value.interpolation_hamiltonian_maximum_error
            ),
            "interpolation_spectral_maximum_error": (
                value.interpolation_spectral_maximum_error
            ),
            "hopping_powers": tuple(
                Periodic1DBandEquivalenceHoppingPowerRecord(item).to_dict()
                for item in value.hopping_powers
            ),
            "ranges": tuple(
                Periodic1DBandEquivalenceRangeAnalysisRecord(item).to_dict()
                for item in value.ranges
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        scalar_names = {
            "amplitude",
            "maximum_band_defect",
            "discrete_maximum_correlation",
            "analytic_maximum_correlation",
            "correlation_quadrature_defect",
            "global_alignment_angle",
            "optimal_splitting_scale",
            "irreducible_operator_squared_loss",
            "minimum_operator_threshold",
            "exact_spectrum_joint_operator_threshold",
            "cyclic_nyquist_power",
            "reconstruction_maximum_frobenius_error",
            "interpolation_hamiltonian_maximum_error",
            "interpolation_spectral_maximum_error",
        }
        _fields(values, scalar_names | {"hopping_powers", "ranges"}, "point record")
        hopping = tuple(
            Periodic1DBandEquivalenceHoppingPowerRecord.from_dict(item).value
            for item in _mapping_tuple(values, "hopping_powers")
        )
        ranges = tuple(
            Periodic1DBandEquivalenceRangeAnalysisRecord.from_dict(item).value
            for item in _mapping_tuple(values, "ranges")
        )
        scalar = {name: _floating(values, name) for name in scalar_names}
        return cls(
            Periodic1DBandEquivalencePointAnalysis(
                amplitude=scalar["amplitude"],
                maximum_band_defect=scalar["maximum_band_defect"],
                discrete_maximum_correlation=scalar["discrete_maximum_correlation"],
                analytic_maximum_correlation=scalar["analytic_maximum_correlation"],
                correlation_quadrature_defect=scalar["correlation_quadrature_defect"],
                global_alignment_angle=scalar["global_alignment_angle"],
                optimal_splitting_scale=scalar["optimal_splitting_scale"],
                irreducible_operator_squared_loss=scalar[
                    "irreducible_operator_squared_loss"
                ],
                minimum_operator_threshold=scalar["minimum_operator_threshold"],
                exact_spectrum_joint_operator_threshold=scalar[
                    "exact_spectrum_joint_operator_threshold"
                ],
                cyclic_nyquist_power=scalar["cyclic_nyquist_power"],
                reconstruction_maximum_frobenius_error=scalar[
                    "reconstruction_maximum_frobenius_error"
                ],
                interpolation_hamiltonian_maximum_error=scalar[
                    "interpolation_hamiltonian_maximum_error"
                ],
                interpolation_spectral_maximum_error=scalar[
                    "interpolation_spectral_maximum_error"
                ],
                hopping_powers=hopping,
                ranges=ranges,
            )
        )


@dataclass(frozen=True, slots=True)
class Periodic1DBandEquivalenceLocalityAnalysisRecord(BaseTypedRecord):
    """Own canonical bytes for one immutable scientific analysis."""

    analysis: Periodic1DBandEquivalenceLocalityAnalysis

    def __post_init__(self) -> None:
        if type(self.analysis) is not Periodic1DBandEquivalenceLocalityAnalysis:
            raise TypeError(
                "analysis must be Periodic1DBandEquivalenceLocalityAnalysis"
            )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "request": _request_mapping(self.analysis.request),
            "points": tuple(
                Periodic1DBandEquivalencePointAnalysisRecord(point).to_dict()
                for point in self.analysis.points
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _fields(values, {"request", "points"}, "analysis record")
        request = _request_from_mapping(_mapping_value(values, "request"))
        points = tuple(
            Periodic1DBandEquivalencePointAnalysisRecord.from_dict(item).value
            for item in _mapping_tuple(values, "points")
        )
        return cls(Periodic1DBandEquivalenceLocalityAnalysis(request, points))


class Periodic1DBandEquivalenceLocalityAnalysisRecorder:
    """Project one bound scientific analysis into its retained wire owner."""

    __slots__ = ("_analysis",)

    def __init__(self, analysis: Periodic1DBandEquivalenceLocalityAnalysis) -> None:
        if type(analysis) is not Periodic1DBandEquivalenceLocalityAnalysis:
            raise TypeError(
                "analysis must be Periodic1DBandEquivalenceLocalityAnalysis"
            )
        self._analysis = analysis

    def result(self) -> Periodic1DBandEquivalenceLocalityAnalysisRecord:
        """Return the retained projection without rerunning its producer."""
        return Periodic1DBandEquivalenceLocalityAnalysisRecord(self._analysis)


__all__ = [
    "Periodic1DBandEquivalenceHoppingPowerRecord",
    "Periodic1DBandEquivalenceLocalityAnalysisRecord",
    "Periodic1DBandEquivalenceLocalityAnalysisRecorder",
    "Periodic1DBandEquivalencePointAnalysisRecord",
    "Periodic1DBandEquivalenceRangeAnalysisRecord",
]
