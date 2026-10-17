"""Immutable family-owned controls for locality development calculations."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

import numpy as np


def _finite_float(name: str, value: float) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _increasing_unit_interval(name: str, values: tuple[float, ...]) -> None:
    _increasing_nonnegative(name, values)
    if values[-1] > 1.0:
        raise ValueError(f"{name} must not exceed one")


def _increasing_nonnegative(name: str, values: tuple[float, ...]) -> None:
    if type(values) is not tuple or not values:
        raise TypeError(f"{name} must be a nonempty tuple")
    if any(type(value) is not float or not math.isfinite(value) for value in values):
        raise TypeError(f"{name} must contain finite built-in floats")
    if any(value < 0.0 for value in values):
        raise ValueError(f"{name} must be nonnegative")
    if values != tuple(sorted(set(values))):
        raise ValueError(f"{name} must be unique and increasing")


class DevelopmentFamily(StrEnum):
    """Name one independently interpreted development replication."""

    SQUARE = (
        "ksdft2effmass.campaign.model-adequacy.periodic2d."
        "band-equivalence-versus-hopping-locality"
    )
    GRAPHENE_INSPIRED = (
        "ksdft2effmass.campaign.model-adequacy.periodic2d-nonorthogonal."
        "band-equivalence-versus-hopping-locality"
    )
    SIMPLE_CUBIC = (
        "ksdft2effmass.campaign.model-adequacy.periodic3d."
        "band-equivalence-versus-hopping-locality"
    )
    SILICON_INSPIRED = (
        "ksdft2effmass.campaign.model-adequacy.periodic3d-nonorthogonal."
        "band-equivalence-versus-hopping-locality"
    )


class ParentKind(StrEnum):
    """Select one exact four-state synthetic parent law."""

    DIRECTED_AXIS = "directed-axis"
    HERMITIAN_BRAVAIS = "hermitian-bravais"
    BIPARTITE_INSPIRED = "bipartite-inspired"


class GaugeNormalization(StrEnum):
    """Select the declared interpretation of the gauge amplitude."""

    AXIS_MAXIMUM = "axis-maximum"
    BOND_RMS = "bond-rms"


@dataclass(frozen=True, slots=True)
class DevelopmentCase:
    """Define one parent and geometry inside an experiment family."""

    name: str
    dimension: int
    parent_kind: ParentKind
    gauge_normalization: GaugeNormalization
    positive_bonds: tuple[tuple[int, ...], ...]
    metric: tuple[tuple[float, ...], ...]
    shell_metric_scale: float
    basis_offsets: tuple[tuple[float, ...], ...] = ()

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name:
            raise TypeError("name must be a nonempty built-in str")
        if type(self.dimension) is not int or self.dimension not in (2, 3):
            raise ValueError("dimension must be the built-in integer 2 or 3")
        if type(self.parent_kind) is not ParentKind:
            raise TypeError("parent_kind must be ParentKind")
        if type(self.gauge_normalization) is not GaugeNormalization:
            raise TypeError("gauge_normalization must be GaugeNormalization")
        if not self.positive_bonds:
            raise ValueError("positive_bonds must not be empty")
        if any(len(bond) != self.dimension for bond in self.positive_bonds):
            raise ValueError("every bond must match dimension")
        if len(self.metric) != self.dimension or any(
            len(row) != self.dimension for row in self.metric
        ):
            raise ValueError("metric must be a square dimension-matched matrix")
        metric = np.asarray(self.metric, dtype=np.float64)
        if not bool(np.all(np.isfinite(metric))):
            raise ValueError("metric entries must be finite")
        if not np.array_equal(metric, metric.T):
            raise ValueError("metric must be symmetric")
        if float(np.min(np.linalg.eigvalsh(metric))) <= 0.0:
            raise ValueError("metric must be positive definite")
        _finite_float("shell_metric_scale", self.shell_metric_scale)
        if self.shell_metric_scale <= 0.0:
            raise ValueError("shell_metric_scale must be positive")
        if self.basis_offsets and any(
            len(offset) != self.dimension for offset in self.basis_offsets
        ):
            raise ValueError("every basis offset must match dimension")


@dataclass(frozen=True, slots=True)
class DevelopmentDefinition:
    """Freeze one bounded, non-evidentiary experiment execution."""

    family: DevelopmentFamily
    cases: tuple[DevelopmentCase, ...]
    construction_size: int
    evaluation_size: int
    evaluation_shift: float
    parent_scales: tuple[float, ...]
    amplitudes: tuple[float, ...]
    band_tolerances: tuple[float, ...]
    shell_cap: int
    amplitude_resolution_intervals: tuple[int, ...] = (
        8,
        16,
        32,
        64,
        128,
        256,
        512,
        1024,
        2048,
        4096,
    )
    transport_rank_absolute: float = 1.0e-10
    transport_rank_relative: float = 1.0e-12

    def __post_init__(self) -> None:
        if type(self.family) is not DevelopmentFamily:
            raise TypeError("family must be DevelopmentFamily")
        if type(self.cases) is not tuple or not self.cases:
            raise TypeError("cases must be a nonempty tuple")
        if any(type(case) is not DevelopmentCase for case in self.cases):
            raise TypeError("cases must contain DevelopmentCase values")
        dimensions = {case.dimension for case in self.cases}
        if len(dimensions) != 1:
            raise ValueError("all cases in one family must have one dimension")
        if type(self.construction_size) is not int or self.construction_size < 4:
            raise ValueError("construction_size must be an integer of at least four")
        if self.construction_size % 2:
            raise ValueError("construction_size must be even")
        if type(self.evaluation_size) is not int or self.evaluation_size < 3:
            raise ValueError("evaluation_size must be an integer of at least three")
        _finite_float("evaluation_shift", self.evaluation_shift)
        if not 0.0 < self.evaluation_shift < 1.0:
            raise ValueError("evaluation_shift must lie strictly between zero and one")
        _increasing_unit_interval("parent_scales", self.parent_scales)
        _increasing_nonnegative("amplitudes", self.amplitudes)
        if type(self.band_tolerances) is not tuple or not self.band_tolerances:
            raise TypeError("band_tolerances must be a nonempty tuple")
        if any(
            type(value) is not float or value <= 0.0 for value in self.band_tolerances
        ):
            raise ValueError("band_tolerances must contain positive built-in floats")
        if self.band_tolerances != tuple(
            sorted(set(self.band_tolerances), reverse=True)
        ):
            raise ValueError("band_tolerances must be unique and decreasing")
        if type(self.shell_cap) is not int or self.shell_cap < 0:
            raise ValueError("shell_cap must be a nonnegative built-in int")
        if (
            type(self.amplitude_resolution_intervals) is not tuple
            or not self.amplitude_resolution_intervals
            or any(
                type(value) is not int or value < 1
                for value in self.amplitude_resolution_intervals
            )
        ):
            raise ValueError(
                "amplitude_resolution_intervals must contain positive built-in integers"
            )
        if any(
            fine != 2 * coarse
            for coarse, fine in zip(
                self.amplitude_resolution_intervals[:-1],
                self.amplitude_resolution_intervals[1:],
                strict=True,
            )
        ):
            raise ValueError(
                "amplitude resolution intervals must form a doubling ladder"
            )
        for name, value in (
            ("transport_rank_absolute", self.transport_rank_absolute),
            ("transport_rank_relative", self.transport_rank_relative),
        ):
            _finite_float(name, value)
            if value <= 0.0:
                raise ValueError(f"{name} must be positive")

    @property
    def dimension(self) -> int:
        """Return the common dimension of this family."""
        return self.cases[0].dimension


__all__ = [
    "DevelopmentCase",
    "DevelopmentDefinition",
    "DevelopmentFamily",
    "GaugeNormalization",
    "ParentKind",
]
