"""Constrained-Bessel tail diagnostics for selected non-orthogonal controls."""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

from scipy.special import jv  # type: ignore[import-untyped]

from ksdft2effmass.serialization import StringWireEnum


class ConstrainedBesselGeometryEnum(StringWireEnum):
    """Name one selected dependent positive-bond inventory."""

    TRIANGULAR = "triangular-three-bond"
    FCC = "fcc-six-bond"


@dataclass(frozen=True, slots=True)
class ConstrainedBesselZeroModeDiagnosticResult:
    """Retain a bounded zero-mode constrained-series evaluation."""

    geometry: ConstrainedBesselGeometryEnum
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

    geometry: ConstrainedBesselGeometryEnum
    maximum_rotation_amplitude: float
    bessel_argument: float
    shell_cap: int
    kernel_cap: int
    retained_displacements: int
    coefficient_remainder_bound: float
    numerical_margin: float
    retained_power_lower_bound: float
    tail_power_upper_bound: float


class ConstrainedBesselKernel:
    """Own one geometry-specific bounded constrained-Bessel kernel."""

    __slots__ = ("_argument", "_geometry", "_kernel_cap")

    def __init__(
        self,
        *,
        geometry: ConstrainedBesselGeometryEnum,
        argument: float,
        kernel_cap: int,
    ) -> None:
        if type(geometry) is not ConstrainedBesselGeometryEnum:
            raise TypeError("geometry must be ConstrainedBesselGeometryEnum")
        if type(argument) is not float:
            raise TypeError("argument must be a built-in float")
        if not math.isfinite(argument):
            raise ValueError("argument must be finite")
        if type(kernel_cap) is not int:
            raise TypeError("kernel_cap must be a built-in integer")
        self._geometry = geometry
        self._argument = argument
        self._kernel_cap = kernel_cap

    def absolute_sum_bound(self) -> float:
        """Return the absolute bilateral Bessel-series bound."""
        half_argument = abs(self._argument) / 2.0
        return math.exp(half_argument**2) * (2.0 * math.exp(half_argument) - 1.0)

    def absolute_tail_bound(self) -> float:
        """Return the omitted bilateral Bessel-index bound."""
        half_argument = abs(self._argument) / 2.0
        lower_index = self._kernel_cap + 1
        if half_argument == 0.0:
            return 0.0
        ratio = half_argument / float(lower_index + 1)
        return (
            2.0
            * math.exp(half_argument**2)
            * half_argument**lower_index
            / (float(math.factorial(lower_index)) * (1.0 - ratio))
        )

    def metric_shell(self, displacement: tuple[int, ...]) -> int:
        """Return the integer metric shell for one displacement."""
        if self._geometry is ConstrainedBesselGeometryEnum.TRIANGULAR:
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

    def coefficient(self, displacement: tuple[int, ...]) -> float:
        """Return the bounded constrained coefficient for one displacement."""
        if self._geometry is ConstrainedBesselGeometryEnum.TRIANGULAR:
            first, second = displacement
            return math.fsum(
                float(
                    jv(first - index, self._argument)
                    * jv(second + index, self._argument)
                    * jv(index, self._argument)
                )
                for index in range(-self._kernel_cap, self._kernel_cap + 1)
            )
        first, second, third = displacement
        indices = range(-self._kernel_cap, self._kernel_cap + 1)
        return math.fsum(
            float(
                jv(first + one + two, self._argument)
                * jv(second - one + three, self._argument)
                * jv(third - two - three, self._argument)
                * jv(one, self._argument)
                * jv(two, self._argument)
                * jv(three, self._argument)
            )
            for one, two, three in itertools.product(indices, repeat=3)
        )


@dataclass(frozen=True, slots=True)
class ConstrainedBesselZeroModeRequest:
    """Define one bounded constrained-series zero-mode evaluation."""

    geometry: ConstrainedBesselGeometryEnum
    bessel_argument: float
    kernel_cap: int

    def __post_init__(self) -> None:
        if type(self.geometry) is not ConstrainedBesselGeometryEnum:
            raise TypeError("geometry must be ConstrainedBesselGeometryEnum")
        if type(self.bessel_argument) is not float:
            raise TypeError("bessel_argument must be a built-in float")
        if not math.isfinite(self.bessel_argument):
            raise ValueError("bessel_argument must be finite")
        if not 0.0 <= self.bessel_argument <= math.pi / 2.0:
            raise ValueError("bessel_argument must lie in [0, pi/2]")
        if type(self.kernel_cap) is not int:
            raise TypeError("kernel_cap must be a built-in integer")
        maximum = (
            64 if self.geometry is ConstrainedBesselGeometryEnum.TRIANGULAR else 12
        )
        if not 0 <= self.kernel_cap <= maximum:
            raise ValueError("kernel_cap exceeds the geometry-specific resource bound")


class ConstrainedBesselZeroModeDiagnostic:
    """Evaluate one bound constrained scalar zero-mode request."""

    __slots__ = ("_request",)

    def __init__(self, *, request: ConstrainedBesselZeroModeRequest) -> None:
        if type(request) is not ConstrainedBesselZeroModeRequest:
            raise TypeError("request must be ConstrainedBesselZeroModeRequest")
        self._request = request

    @property
    def request(self) -> ConstrainedBesselZeroModeRequest:
        """Return the immutable zero-mode request."""
        return self._request

    def result(self) -> ConstrainedBesselZeroModeDiagnosticResult:
        """Return the bounded zero-mode diagnostic."""
        request = self._request
        kernel = ConstrainedBesselKernel(
            geometry=request.geometry,
            argument=request.bessel_argument,
            kernel_cap=request.kernel_cap,
        )
        kernel_tail = kernel.absolute_tail_bound()
        if request.geometry is ConstrainedBesselGeometryEnum.TRIANGULAR:
            value = kernel.coefficient((0, 0))
            remainder = kernel_tail
        else:
            value = kernel.coefficient((0, 0, 0))
            remainder = 3.0 * kernel_tail * kernel.absolute_sum_bound() ** 2
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

    geometry: ConstrainedBesselGeometryEnum
    maximum_rotation_amplitude: float
    shell_cap: int
    kernel_cap: int
    numerical_margin: float

    def __post_init__(self) -> None:
        if type(self.geometry) is not ConstrainedBesselGeometryEnum:
            raise TypeError("geometry must be ConstrainedBesselGeometryEnum")
        if type(self.maximum_rotation_amplitude) is not float:
            raise TypeError("maximum_rotation_amplitude must be a built-in float")
        if not math.isfinite(self.maximum_rotation_amplitude):
            raise ValueError("maximum_rotation_amplitude must be finite")
        if type(self.numerical_margin) is not float:
            raise TypeError("numerical_margin must be a built-in float")
        if not math.isfinite(self.numerical_margin):
            raise ValueError("numerical_margin must be finite")
        if not 0.0 <= self.maximum_rotation_amplitude <= math.pi / 4.0:
            raise ValueError("maximum_rotation_amplitude must lie in [0, pi/4]")
        if type(self.shell_cap) is not int or type(self.kernel_cap) is not int:
            raise TypeError("shell_cap and kernel_cap must be built-in integers")
        if not 0 <= self.shell_cap <= 64:
            raise ValueError("shell_cap must lie in [0, 64]")
        maximum = (
            64 if self.geometry is ConstrainedBesselGeometryEnum.TRIANGULAR else 12
        )
        if not 0 <= self.kernel_cap <= maximum:
            raise ValueError("kernel_cap exceeds the geometry-specific resource bound")
        if not 0.0 <= self.numerical_margin <= 1.0e-8:
            raise ValueError("numerical_margin must lie in [0, 1e-8]")


class ConstrainedBesselTailDiagnostic:
    """Evaluate one bound constrained-series tail request."""

    __slots__ = ("_request",)

    def __init__(self, *, request: ConstrainedBesselTailRequest) -> None:
        if type(request) is not ConstrainedBesselTailRequest:
            raise TypeError("request must be ConstrainedBesselTailRequest")
        self._request = request

    @property
    def request(self) -> ConstrainedBesselTailRequest:
        """Return the immutable tail request."""
        return self._request

    def result(self) -> ConstrainedBesselTailDiagnosticResult:
        """Return the selected resource-bounded tail diagnostic."""
        request = self._request
        geometry = request.geometry
        bond_count = 3 if geometry is ConstrainedBesselGeometryEnum.TRIANGULAR else 6
        dimension = 2 if geometry is ConstrainedBesselGeometryEnum.TRIANGULAR else 3
        argument = 2.0 * request.maximum_rotation_amplitude / float(bond_count)
        kernel = ConstrainedBesselKernel(
            geometry=geometry,
            argument=argument,
            kernel_cap=request.kernel_cap,
        )
        kernel_tail = kernel.absolute_tail_bound()
        if geometry is ConstrainedBesselGeometryEnum.TRIANGULAR:
            coefficient_remainder = kernel_tail
        else:
            coefficient_remainder = 3.0 * kernel_tail * kernel.absolute_sum_bound() ** 2

        coordinate_cap = math.ceil(math.sqrt(2.0 * float(request.shell_cap)))
        retained_lower = 0.0
        retained_count = 0
        for displacement in itertools.product(
            range(-coordinate_cap, coordinate_cap + 1), repeat=dimension
        ):
            if kernel.metric_shell(displacement) > request.shell_cap:
                continue
            retained_count += 1
            coefficient = kernel.coefficient(displacement)
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
    "ConstrainedBesselGeometryEnum",
    "ConstrainedBesselTailDiagnostic",
    "ConstrainedBesselTailDiagnosticResult",
    "ConstrainedBesselTailRequest",
    "ConstrainedBesselZeroModeDiagnostic",
    "ConstrainedBesselZeroModeDiagnosticResult",
    "ConstrainedBesselZeroModeRequest",
]
