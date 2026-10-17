"""Constrained-Bessel tail diagnostics for selected non-orthogonal controls."""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from enum import StrEnum

from scipy.special import jv  # type: ignore[import-untyped]


class ConstrainedBesselGeometry(StrEnum):
    """Name one selected dependent positive-bond inventory."""

    TRIANGULAR = "triangular-three-bond"
    FCC = "fcc-six-bond"


@dataclass(frozen=True, slots=True)
class ConstrainedBesselZeroModeDiagnosticResult:
    """Retain a bounded zero-mode constrained-series evaluation."""

    geometry: ConstrainedBesselGeometry
    bessel_argument: float
    kernel_cap: int
    value: float
    remainder_bound: float


@dataclass(frozen=True, slots=True)
class ConstrainedBesselTailDiagnosticResult:
    """Retain one bounded evaluation of a proven analytic tail certificate.

    ``tail_power_upper_bound`` is unit-free and normalized by the total scalar Fourier
    power. It includes the explicitly supplied binary64 numerical margin in every
    retained coefficient. It is not a formal interval-arithmetic certificate.
    """

    geometry: ConstrainedBesselGeometry
    maximum_rotation_amplitude: float
    bessel_argument: float
    shell_cap: int
    kernel_cap: int
    retained_displacements: int
    coefficient_remainder_bound: float
    numerical_margin: float
    retained_power_lower_bound: float
    tail_power_upper_bound: float


def _finite_float(name: str, value: float) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _absolute_bessel_sum_bound(argument: float) -> float:
    half_argument = abs(argument) / 2.0
    return math.exp(half_argument**2) * (2.0 * math.exp(half_argument) - 1.0)


def _absolute_bessel_tail_bound(argument: float, kernel_cap: int) -> float:
    half_argument = abs(argument) / 2.0
    lower_index = kernel_cap + 1
    if half_argument == 0.0:
        return 0.0
    ratio = half_argument / float(lower_index + 1)
    return (
        2.0
        * math.exp(half_argument**2)
        * half_argument**lower_index
        / (float(math.factorial(lower_index)) * (1.0 - ratio))
    )


def _metric_shell(
    geometry: ConstrainedBesselGeometry, displacement: tuple[int, ...]
) -> int:
    if geometry is ConstrainedBesselGeometry.TRIANGULAR:
        first, second = displacement
        return first * first + second * second + first * second
    first, second, third = displacement
    return (
        first * first
        + second * second
        + third * third
        + first * second
        + first * third
        + second * third
    )


def _triangular_coefficient(
    displacement: tuple[int, ...], argument: float, kernel_cap: int
) -> float:
    first, second = displacement
    return math.fsum(
        float(
            jv(first - index, argument)
            * jv(second + index, argument)
            * jv(index, argument)
        )
        for index in range(-kernel_cap, kernel_cap + 1)
    )


def _fcc_coefficient(
    displacement: tuple[int, ...], argument: float, kernel_cap: int
) -> float:
    first, second, third = displacement
    indices = range(-kernel_cap, kernel_cap + 1)
    return math.fsum(
        float(
            jv(first + one + two, argument)
            * jv(second - one + three, argument)
            * jv(third - two - three, argument)
            * jv(one, argument)
            * jv(two, argument)
            * jv(three, argument)
        )
        for one, two, three in itertools.product(indices, repeat=3)
    )


@dataclass(frozen=True, slots=True)
class ConstrainedBesselZeroModeRequest:
    """Define one bounded constrained-series zero-mode evaluation."""

    geometry: ConstrainedBesselGeometry
    bessel_argument: float
    kernel_cap: int

    def __post_init__(self) -> None:
        if type(self.geometry) is not ConstrainedBesselGeometry:
            raise TypeError("geometry must be ConstrainedBesselGeometry")
        _finite_float("bessel_argument", self.bessel_argument)
        if not 0.0 <= self.bessel_argument <= math.pi / 2.0:
            raise ValueError("bessel_argument must lie in [0, pi/2]")
        if type(self.kernel_cap) is not int:
            raise TypeError("kernel_cap must be a built-in integer")
        maximum = 64 if self.geometry is ConstrainedBesselGeometry.TRIANGULAR else 12
        if not 0 <= self.kernel_cap <= maximum:
            raise ValueError("kernel_cap exceeds the geometry-specific resource bound")


class ConstrainedBesselZeroModeDiagnostic:
    """Evaluate one constrained scalar zero mode and its remainder bound."""

    __slots__ = ()

    def execute(
        self, request: ConstrainedBesselZeroModeRequest
    ) -> ConstrainedBesselZeroModeDiagnosticResult:
        if type(request) is not ConstrainedBesselZeroModeRequest:
            raise TypeError("request must be ConstrainedBesselZeroModeRequest")
        kernel_tail = _absolute_bessel_tail_bound(
            request.bessel_argument, request.kernel_cap
        )
        if request.geometry is ConstrainedBesselGeometry.TRIANGULAR:
            value = _triangular_coefficient(
                (0, 0), request.bessel_argument, request.kernel_cap
            )
            remainder = kernel_tail
        else:
            value = _fcc_coefficient(
                (0, 0, 0), request.bessel_argument, request.kernel_cap
            )
            remainder = (
                3.0
                * kernel_tail
                * _absolute_bessel_sum_bound(request.bessel_argument) ** 2
            )
        return ConstrainedBesselZeroModeDiagnosticResult(
            geometry=request.geometry,
            bessel_argument=request.bessel_argument,
            kernel_cap=request.kernel_cap,
            value=value,
            remainder_bound=remainder,
        )


@dataclass(frozen=True, slots=True)
class ConstrainedBesselTailRequest:
    """Define one bounded constrained-series tail evaluation."""

    geometry: ConstrainedBesselGeometry
    maximum_rotation_amplitude: float
    shell_cap: int
    kernel_cap: int
    numerical_margin: float

    def __post_init__(self) -> None:
        if type(self.geometry) is not ConstrainedBesselGeometry:
            raise TypeError("geometry must be ConstrainedBesselGeometry")
        _finite_float("maximum_rotation_amplitude", self.maximum_rotation_amplitude)
        _finite_float("numerical_margin", self.numerical_margin)
        if not 0.0 <= self.maximum_rotation_amplitude <= math.pi / 4.0:
            raise ValueError("maximum_rotation_amplitude must lie in [0, pi/4]")
        if type(self.shell_cap) is not int or type(self.kernel_cap) is not int:
            raise TypeError("shell_cap and kernel_cap must be built-in integers")
        if not 0 <= self.shell_cap <= 64:
            raise ValueError("shell_cap must lie in [0, 64]")
        maximum = 64 if self.geometry is ConstrainedBesselGeometry.TRIANGULAR else 12
        if not 0 <= self.kernel_cap <= maximum:
            raise ValueError("kernel_cap exceeds the geometry-specific resource bound")
        if not 0.0 <= self.numerical_margin <= 1.0e-8:
            raise ValueError("numerical_margin must lie in [0, 1e-8]")


class ConstrainedBesselTailDiagnostic:
    """Evaluate one constrained-series tail certificate."""

    __slots__ = ()

    def execute(
        self, request: ConstrainedBesselTailRequest
    ) -> ConstrainedBesselTailDiagnosticResult:
        """Return the selected resource-bounded tail diagnostic."""
        if type(request) is not ConstrainedBesselTailRequest:
            raise TypeError("request must be ConstrainedBesselTailRequest")
        geometry = request.geometry
        bond_count = 3 if geometry is ConstrainedBesselGeometry.TRIANGULAR else 6
        dimension = 2 if geometry is ConstrainedBesselGeometry.TRIANGULAR else 3
        argument = 2.0 * request.maximum_rotation_amplitude / float(bond_count)
        kernel_tail = _absolute_bessel_tail_bound(argument, request.kernel_cap)
        if geometry is ConstrainedBesselGeometry.TRIANGULAR:
            coefficient_remainder = kernel_tail
        else:
            coefficient_remainder = (
                3.0 * kernel_tail * _absolute_bessel_sum_bound(argument) ** 2
            )

        coordinate_cap = math.ceil(math.sqrt(2.0 * float(request.shell_cap)))
        retained_lower = 0.0
        retained_count = 0
        for displacement in itertools.product(
            range(-coordinate_cap, coordinate_cap + 1), repeat=dimension
        ):
            if _metric_shell(geometry, displacement) > request.shell_cap:
                continue
            retained_count += 1
            if geometry is ConstrainedBesselGeometry.TRIANGULAR:
                coefficient = _triangular_coefficient(
                    displacement, argument, request.kernel_cap
                )
            else:
                coefficient = _fcc_coefficient(
                    displacement, argument, request.kernel_cap
                )
            lower_absolute = max(
                0.0,
                abs(coefficient) - coefficient_remainder - request.numerical_margin,
            )
            retained_lower += lower_absolute**2

        retained_lower = min(1.0, retained_lower)
        return ConstrainedBesselTailDiagnosticResult(
            geometry=geometry,
            maximum_rotation_amplitude=request.maximum_rotation_amplitude,
            bessel_argument=argument,
            shell_cap=request.shell_cap,
            kernel_cap=request.kernel_cap,
            retained_displacements=retained_count,
            coefficient_remainder_bound=coefficient_remainder,
            numerical_margin=request.numerical_margin,
            retained_power_lower_bound=retained_lower,
            tail_power_upper_bound=max(0.0, 1.0 - retained_lower),
        )


__all__ = [
    "ConstrainedBesselGeometry",
    "ConstrainedBesselTailDiagnostic",
    "ConstrainedBesselTailDiagnosticResult",
    "ConstrainedBesselTailRequest",
    "ConstrainedBesselZeroModeDiagnostic",
    "ConstrainedBesselZeroModeDiagnosticResult",
    "ConstrainedBesselZeroModeRequest",
]
