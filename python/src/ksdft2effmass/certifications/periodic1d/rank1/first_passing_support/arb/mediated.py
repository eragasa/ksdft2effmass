"""Arb enclosure of the frozen transform-mediated maximum error."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import final

from flint import acb, arb, ctx

from ..records import (
    CONSTRUCTION_MESH_SIZE,
    EVALUATION_SHIFT_DENOMINATOR,
    EVALUATION_SHIFT_NUMERATOR,
    EVALUATION_SIZE,
    SUPPORT_INVENTORY,
    ExactRational,
    NonnegativeExactInterval,
)
from .parent import (
    _lowest_parent_eigenvalue,
    _phase,
    _signed_arb_fraction_interval,
    _validate_precision,
)
from .records import MediatedMaximumErrorEnclosure


@final
@dataclass(frozen=True, slots=True)
class MediatedMaximumErrorArbEncloser:
    """Enclose one mediated total maximum evaluation error.

    Parameters
    ----------
    maximum_range
        Dimensionless ordinary support in the closed inventory `0..15`.
    working_precision_bits
        Dimensionless built-in integer Arb precision, at least 64 bits.

    Notes
    -----
    The action uses the frozen 256-point construction mesh, 1025-point staggered
    evaluation mesh, forward-negative Fourier convention, and exact controlled parent.
    It covers only the transform-mediated candidate. It neither encloses the direct-fit
    objective nor produces a complete first-passing certificate.

    Python-FLINT's precision context is process-global. Execution restores the prior
    precision, but concurrent threaded calls are unsupported. Python integers have no
    fixed-width overflow; very large precision values remain a resource concern.
    """

    maximum_range: int
    working_precision_bits: int = 192

    def __post_init__(self) -> None:
        """Validate the frozen support inventory and working precision."""
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int excluding bool")
        if self.maximum_range not in SUPPORT_INVENTORY:
            raise ValueError("maximum_range is outside the frozen support inventory")
        _validate_precision(self.working_precision_bits)

    def execute(self) -> MediatedMaximumErrorEnclosure:
        """Return the finite mediated maximum-error enclosure.

        Returns
        -------
        MediatedMaximumErrorEnclosure
            Exact nonnegative interval in `E_ref` and endpoint-driver indices.

        Raises
        ------
        ValueError
            A parent eigensolve does not isolate one lowest eigenvalue or an absolute
            residual enclosure is invalid.
        """
        previous_precision = ctx.prec
        try:
            ctx.prec = self.working_precision_bits
            interval, lower_index, upper_index = self._compute()
        finally:
            ctx.prec = previous_precision
        return MediatedMaximumErrorEnclosure(
            maximum_range=self.maximum_range,
            working_precision_bits=self.working_precision_bits,
            interval=interval,
            lower_witness_index=lower_index,
            upper_driver_index=upper_index,
        )

    def _compute(self) -> tuple[NonnegativeExactInterval, int, int]:
        construction_values = tuple(
            _lowest_parent_eigenvalue(Fraction(index, CONSTRUCTION_MESH_SIZE))
            for index in range(CONSTRUCTION_MESH_SIZE)
        )
        coefficients = {
            representative: _fourier_coefficient(
                construction_values,
                representative,
            )
            for representative in range(-self.maximum_range, self.maximum_range + 1)
        }
        point_intervals: list[tuple[Fraction, Fraction]] = []
        for index in range(EVALUATION_SIZE):
            coordinate = Fraction(-1, 2) + Fraction(
                index * EVALUATION_SHIFT_DENOMINATOR + EVALUATION_SHIFT_NUMERATOR,
                EVALUATION_SHIFT_DENOMINATOR * EVALUATION_SIZE,
            )
            parent_value = _lowest_parent_eigenvalue(coordinate)
            candidate = acb(0)
            for representative in range(-self.maximum_range, self.maximum_range + 1):
                candidate += coefficients[representative] * _harmonic_phase(
                    coordinate,
                    representative,
                )
            point_intervals.append(
                _nonnegative_interval(abs(acb(parent_value) - candidate))
            )
        lower_index, lower = max(
            enumerate(value[0] for value in point_intervals),
            key=lambda item: item[1],
        )
        upper_index, upper = max(
            enumerate(value[1] for value in point_intervals),
            key=lambda item: item[1],
        )
        return _exact_nonnegative_interval(lower, upper), lower_index, upper_index


def _fourier_coefficient(
    construction_values: tuple[arb, ...],
    representative: int,
) -> acb:
    total = acb(0)
    for index, value in enumerate(construction_values):
        coordinate = Fraction(index, CONSTRUCTION_MESH_SIZE)
        total += acb(value) * _harmonic_phase(coordinate, -representative)
    return total / CONSTRUCTION_MESH_SIZE


def _harmonic_phase(coordinate: Fraction, harmonic: int) -> acb:
    return _phase(coordinate * harmonic)


def _nonnegative_interval(value: arb) -> tuple[Fraction, Fraction]:
    lower, upper = _signed_arb_fraction_interval(value)
    if upper < 0:
        raise ValueError("absolute residual enclosure must not be negative")
    return max(lower, Fraction(0, 1)), upper


def _exact_nonnegative_interval(
    lower: Fraction,
    upper: Fraction,
) -> NonnegativeExactInterval:
    return NonnegativeExactInterval(
        lower=ExactRational(lower.numerator, lower.denominator),
        upper=ExactRational(upper.numerator, upper.denominator),
    )


__all__ = ["MediatedMaximumErrorArbEncloser"]
