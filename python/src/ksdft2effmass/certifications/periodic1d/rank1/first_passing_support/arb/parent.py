"""Arb enclosure of the frozen controlled parent's lowest eigenvalue."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import ceil, log10
from typing import final

from flint import acb, acb_mat, arb, ctx

from ..records import (
    PARENT_ENTRY_DENOMINATOR,
    PARENT_ONSITE_NUMERATORS,
    PARENT_POSITIVE_HOPPING_NUMERATORS,
    ExactRational,
)
from .records import (
    ControlledParentLowestEigenvalueEnclosure,
    SignedExactInterval,
)


@final
@dataclass(frozen=True, slots=True)
class ControlledParentLowestEigenvalueArbEncloser:
    """Enclose the frozen parent's lowest eigenvalue at one exact coordinate.

    Parameters
    ----------
    reduced_momentum
        Exact dimensionless reduced reciprocal coordinate.
    working_precision_bits
        Dimensionless built-in integer Arb precision, at least 64 bits.

    Notes
    -----
    The action constructs the exact rational four-state parent directly inside Arb and
    requires the returned lowest eigenvalue ball to be separated from all other
    eigenvalue balls. Python-FLINT's precision context is process-global; execution
    restores the prior precision, but concurrent threaded calls are unsupported.

    Python integers have no fixed-width overflow. Very large precision or coordinate
    values may exhaust time or memory.
    """

    reduced_momentum: ExactRational
    working_precision_bits: int = 192

    def __post_init__(self) -> None:
        """Validate exact coordinate and working precision."""
        if type(self.reduced_momentum) is not ExactRational:
            raise TypeError("reduced_momentum must be ExactRational")
        _validate_precision(self.working_precision_bits)

    def execute(self) -> ControlledParentLowestEigenvalueEnclosure:
        """Return the isolated lowest-eigenvalue enclosure.

        Returns
        -------
        ControlledParentLowestEigenvalueEnclosure
            Exact rational enclosure in `E_ref` at the requested coordinate.

        Raises
        ------
        ValueError
            The Arb eigensolve does not return four real-axis balls or does not isolate
            one unique lowest eigenvalue.
        """
        previous_precision = ctx.prec
        try:
            ctx.prec = self.working_precision_bits
            value = _lowest_parent_eigenvalue(self.reduced_momentum.as_fraction())
            lower, upper = _signed_arb_fraction_interval(value)
        finally:
            ctx.prec = previous_precision
        return ControlledParentLowestEigenvalueEnclosure(
            reduced_momentum=self.reduced_momentum,
            working_precision_bits=self.working_precision_bits,
            interval=_signed_exact_interval(lower, upper),
        )


def _lowest_parent_eigenvalue(coordinate: Fraction) -> arb:
    eigenvalues, _ = _parent_matrix(coordinate).eig(right=True, algorithm="rump")
    if len(eigenvalues) != 4:
        raise ValueError("controlled parent eigensolve must return four eigenvalues")
    bounds: list[tuple[Fraction, Fraction, arb]] = []
    for eigenvalue in eigenvalues:
        if not eigenvalue.imag.contains(0):
            raise ValueError(
                "controlled Hermitian eigenvalue must contain zero imaginary part"
            )
        lower, upper = _signed_arb_fraction_interval(eigenvalue.real)
        bounds.append((lower, upper, eigenvalue.real))
    bounds.sort(key=lambda value: value[0])
    lowest = bounds[0]
    if any(lowest[1] >= other[0] for other in bounds[1:]):
        raise ValueError("Arb eigensolve did not isolate a unique lowest eigenvalue")
    return lowest[2]


def _parent_matrix(coordinate: Fraction) -> acb_mat:
    onsite = acb_mat(
        [
            [
                arb(PARENT_ONSITE_NUMERATORS[row][column])
                / arb(PARENT_ENTRY_DENOMINATOR)
                for column in range(4)
            ]
            for row in range(4)
        ]
    )
    hopping = acb_mat(
        [
            [
                arb(PARENT_POSITIVE_HOPPING_NUMERATORS[row][column])
                / arb(PARENT_ENTRY_DENOMINATOR)
                for column in range(4)
            ]
            for row in range(4)
        ]
    )
    phase = _phase(coordinate)
    return onsite + hopping * phase + hopping.transpose() * phase.conjugate()


def _phase(coordinate: Fraction) -> acb:
    angle = arb(2) * arb.pi() * arb(coordinate.numerator) / arb(coordinate.denominator)
    return acb(angle.cos(), angle.sin())


def _signed_arb_fraction_interval(value: arb) -> tuple[Fraction, Fraction]:
    digits = ceil(ctx.prec * log10(2)) + 12
    midpoint, radius, exponent = value.mid_rad_10exp(digits)
    power = int(exponent)
    if power < 0:
        denominator = 10 ** (-power)
        return (
            Fraction(int(midpoint) - int(radius), denominator),
            Fraction(int(midpoint) + int(radius), denominator),
        )
    multiplier = 10**power
    return (
        Fraction((int(midpoint) - int(radius)) * multiplier, 1),
        Fraction((int(midpoint) + int(radius)) * multiplier, 1),
    )


def _signed_exact_interval(
    lower: Fraction,
    upper: Fraction,
) -> SignedExactInterval:
    return SignedExactInterval(
        lower=ExactRational(lower.numerator, lower.denominator),
        upper=ExactRational(upper.numerator, upper.denominator),
    )


def _validate_precision(value: int) -> None:
    if type(value) is not int:
        raise TypeError("working_precision_bits must be a built-in int excluding bool")
    if value < 64:
        raise ValueError("working_precision_bits must be at least 64")


__all__ = ["ControlledParentLowestEigenvalueArbEncloser"]
