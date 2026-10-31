"""Authenticated visualization projection for band-equivalence locality."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.visualizations import BaseVisualizationData

from ..results import Periodic1DBandEquivalenceLocalityAnalysis


def _float_tuple(
    values: Mapping[str, SerializableValue], name: str
) -> tuple[float, ...]:
    value = values[name]
    if type(value) is not tuple or any(type(item) is not float for item in value):
        raise TypeError(f"{name} must decode to a tuple of built-in floats")
    return value


def _int_tuple(values: Mapping[str, SerializableValue], name: str) -> tuple[int, ...]:
    value = values[name]
    if type(value) is not tuple or any(type(item) is not int for item in value):
        raise TypeError(f"{name} must decode to a tuple of built-in integers")
    return value


def _float_rows(
    values: Mapping[str, SerializableValue], name: str
) -> tuple[tuple[float, ...], ...]:
    value = values[name]
    if type(value) is not tuple:
        raise TypeError(f"{name} must decode to a tuple")
    rows: list[tuple[float, ...]] = []
    for row in value:
        if type(row) is not tuple or any(type(item) is not float for item in row):
            raise TypeError(f"{name} must contain tuples of built-in floats")
        rows.append(row)
    return tuple(rows)


@dataclass(frozen=True, slots=True)
class Periodic1DBandEquivalenceLocalityVisualizationData(BaseVisualizationData):
    """Retain only verifier-derived values admitted for rendering."""

    source_sha256: str
    amplitudes: tuple[float, ...]
    discrete_correlations: tuple[float, ...]
    analytic_correlations: tuple[float, ...]
    operator_thresholds: tuple[float, ...]
    joint_thresholds: tuple[float, ...]
    nyquist_powers: tuple[float, ...]
    maximum_ranges: tuple[int, ...]
    total_hamiltonian_errors: tuple[tuple[float, ...], ...]
    total_spectral_errors: tuple[tuple[float, ...], ...]
    hopping_displacements: tuple[int, ...]
    hopping_powers: tuple[tuple[float, ...], ...]

    def __post_init__(self) -> None:
        if (
            type(self.source_sha256) is not str
            or len(self.source_sha256) != 64
            or any(
                character not in "0123456789abcdef" for character in self.source_sha256
            )
        ):
            raise ValueError("source_sha256 must be a lowercase SHA-256 digest")
        point_count = len(self.amplitudes)
        if point_count == 0:
            raise ValueError("amplitudes must be nonempty")
        for name, values in (
            ("amplitudes", self.amplitudes),
            ("discrete_correlations", self.discrete_correlations),
            ("analytic_correlations", self.analytic_correlations),
            ("operator_thresholds", self.operator_thresholds),
            ("joint_thresholds", self.joint_thresholds),
            ("nyquist_powers", self.nyquist_powers),
        ):
            if type(values) is not tuple or len(values) != point_count:
                raise ValueError(f"{name} must match the amplitude inventory")
            if any(
                type(value) is not float or not math.isfinite(value) for value in values
            ):
                raise TypeError(f"{name} must contain finite built-in floats")
        for name, values in (
            ("maximum_ranges", self.maximum_ranges),
            ("hopping_displacements", self.hopping_displacements),
        ):
            if type(values) is not tuple or not values:
                raise TypeError(f"{name} must be a nonempty tuple")
            if any(type(value) is not int for value in values):
                raise TypeError(f"{name} must contain built-in integers")
        for name, rows, width in (
            (
                "total_hamiltonian_errors",
                self.total_hamiltonian_errors,
                len(self.maximum_ranges),
            ),
            (
                "total_spectral_errors",
                self.total_spectral_errors,
                len(self.maximum_ranges),
            ),
            ("hopping_powers", self.hopping_powers, len(self.hopping_displacements)),
        ):
            if type(rows) is not tuple or len(rows) != point_count:
                raise ValueError(f"{name} must match the amplitude inventory")
            for row in rows:
                if type(row) is not tuple or len(row) != width:
                    raise ValueError(f"{name} row width does not match its inventory")
                if any(
                    type(value) is not float or not math.isfinite(value) or value < 0.0
                    for value in row
                ):
                    raise ValueError(
                        f"{name} must contain finite nonnegative built-in floats"
                    )

    @classmethod
    def from_analysis(
        cls,
        analysis: Periodic1DBandEquivalenceLocalityAnalysis,
        *,
        source_sha256: str,
    ) -> Self:
        """Project authoritative values without rerunning their producer."""
        if type(analysis) is not Periodic1DBandEquivalenceLocalityAnalysis:
            raise TypeError(
                "analysis must be Periodic1DBandEquivalenceLocalityAnalysis"
            )
        first = analysis.points[0]
        return cls(
            source_sha256=source_sha256,
            amplitudes=tuple(point.amplitude for point in analysis.points),
            discrete_correlations=tuple(
                point.discrete_maximum_correlation for point in analysis.points
            ),
            analytic_correlations=tuple(
                point.analytic_maximum_correlation for point in analysis.points
            ),
            operator_thresholds=tuple(
                point.minimum_operator_threshold for point in analysis.points
            ),
            joint_thresholds=tuple(
                point.exact_spectrum_joint_operator_threshold
                for point in analysis.points
            ),
            nyquist_powers=tuple(
                point.cyclic_nyquist_power for point in analysis.points
            ),
            maximum_ranges=tuple(item.maximum_range for item in first.ranges),
            total_hamiltonian_errors=tuple(
                tuple(item.total_hamiltonian_maximum_error for item in point.ranges)
                for point in analysis.points
            ),
            total_spectral_errors=tuple(
                tuple(item.total_spectral_maximum_error for item in point.ranges)
                for point in analysis.points
            ),
            hopping_displacements=tuple(
                item.displacement for item in first.hopping_powers
            ),
            hopping_powers=tuple(
                tuple(
                    item.normalized_squared_frobenius_norm
                    for item in point.hopping_powers
                )
                for point in analysis.points
            ),
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "source_sha256": self.source_sha256,
            "amplitudes": self.amplitudes,
            "discrete_correlations": self.discrete_correlations,
            "analytic_correlations": self.analytic_correlations,
            "operator_thresholds": self.operator_thresholds,
            "joint_thresholds": self.joint_thresholds,
            "nyquist_powers": self.nyquist_powers,
            "maximum_ranges": self.maximum_ranges,
            "total_hamiltonian_errors": self.total_hamiltonian_errors,
            "total_spectral_errors": self.total_spectral_errors,
            "hopping_displacements": self.hopping_displacements,
            "hopping_powers": self.hopping_powers,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        expected = {
            "source_sha256",
            "amplitudes",
            "discrete_correlations",
            "analytic_correlations",
            "operator_thresholds",
            "joint_thresholds",
            "nyquist_powers",
            "maximum_ranges",
            "total_hamiltonian_errors",
            "total_spectral_errors",
            "hopping_displacements",
            "hopping_powers",
        }
        if set(values) != expected:
            raise ValueError("visualization-data fields do not match")
        digest = values["source_sha256"]
        if type(digest) is not str:
            raise TypeError("source_sha256 must decode to a built-in string")
        return cls(
            source_sha256=digest,
            amplitudes=_float_tuple(values, "amplitudes"),
            discrete_correlations=_float_tuple(values, "discrete_correlations"),
            analytic_correlations=_float_tuple(values, "analytic_correlations"),
            operator_thresholds=_float_tuple(values, "operator_thresholds"),
            joint_thresholds=_float_tuple(values, "joint_thresholds"),
            nyquist_powers=_float_tuple(values, "nyquist_powers"),
            maximum_ranges=_int_tuple(values, "maximum_ranges"),
            total_hamiltonian_errors=_float_rows(values, "total_hamiltonian_errors"),
            total_spectral_errors=_float_rows(values, "total_spectral_errors"),
            hopping_displacements=_int_tuple(values, "hopping_displacements"),
            hopping_powers=_float_rows(values, "hopping_powers"),
        )


__all__ = ["Periodic1DBandEquivalenceLocalityVisualizationData"]
