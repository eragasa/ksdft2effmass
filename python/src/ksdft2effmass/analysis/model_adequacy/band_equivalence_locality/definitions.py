"""Immutable family-owned controls for locality development calculations."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

from projectkoios.physkit.periodic.lattice import DirectLatticeMetric

TRANSPORT_RANK_DEFICIENT_REASON = (
    "rank-deficient neighbor overlap does not identify unique transport"
)


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


class BandEquivalenceLocalityFamily(StrEnum):
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
class BandEquivalenceLocalityCase:
    """Define one parent and geometry inside an experiment family."""

    name: str
    dimension: int
    parent_kind: ParentKind
    gauge_normalization: GaugeNormalization
    positive_bonds: tuple[tuple[int, ...], ...]
    direct_metric: DirectLatticeMetric
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
        if type(self.positive_bonds) is not tuple or not self.positive_bonds:
            raise TypeError("positive_bonds must be a nonempty tuple")
        if any(
            type(bond) is not tuple
            or len(bond) != self.dimension
            or any(type(component) is not int for component in bond)
            for bond in self.positive_bonds
        ):
            raise TypeError(
                "positive_bonds must contain built-in integer tuples matching dimension"
            )
        if type(self.direct_metric) is not DirectLatticeMetric:
            raise TypeError("direct_metric must be DirectLatticeMetric")
        if self.direct_metric.dimension != self.dimension:
            raise ValueError("direct metric dimension must match the case")
        _finite_float("shell_metric_scale", self.shell_metric_scale)
        if self.shell_metric_scale <= 0.0:
            raise ValueError("shell_metric_scale must be positive")
        if type(self.basis_offsets) is not tuple:
            raise TypeError("basis_offsets must be a tuple")
        if any(
            type(offset) is not tuple
            or len(offset) != self.dimension
            or any(
                type(component) is not float or not math.isfinite(component)
                for component in offset
            )
            for offset in self.basis_offsets
        ):
            raise TypeError(
                "basis_offsets must contain finite built-in float tuples matching "
                "dimension"
            )


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityRequest:
    """Freeze one bounded, non-evidentiary experiment execution."""

    family: BandEquivalenceLocalityFamily
    cases: tuple[BandEquivalenceLocalityCase, ...]
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
        if type(self.family) is not BandEquivalenceLocalityFamily:
            raise TypeError("family must be BandEquivalenceLocalityFamily")
        if type(self.cases) is not tuple or not self.cases:
            raise TypeError("cases must be a nonempty tuple")
        if any(type(case) is not BandEquivalenceLocalityCase for case in self.cases):
            raise TypeError("cases must contain BandEquivalenceLocalityCase values")
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
    "BandEquivalenceLocalityCase",
    "BandEquivalenceLocalityRequest",
    "BandEquivalenceLocalityFamily",
    "GaugeNormalization",
    "ParentKind",
    "TRANSPORT_RANK_DEFICIENT_REASON",
]
