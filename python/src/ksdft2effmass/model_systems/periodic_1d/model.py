"""Unit-aware one-dimensional periodic Fourier model records."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)


@dataclass(frozen=True, slots=True, eq=False)
class PeriodicFourierPotential1D:
    r"""Represent a real finite Fourier potential of one coordinate.

    The represented function is

    .. math::

       V(x) = c_0 + \sum_{m=1}^{M}
       \left[c_m \cos(2\pi m x/a) + s_m \sin(2\pi m x/a)\right].

    Coefficients are normalized to the unit of ``constant_coefficient``. The period
    can be physical or explicitly unitless, but sampled coordinates must use a
    dimensionally compatible convention.
    """

    period: ScalarQuantity
    constant_coefficient: ScalarQuantity
    cosine_coefficients: VectorQuantity
    sine_coefficients: VectorQuantity

    def __post_init__(self) -> None:
        """Validate period and coefficient dimensional compatibility."""
        if type(self.period) is not ScalarQuantity:
            raise TypeError("period must be ScalarQuantity")
        if self.period.magnitude <= 0.0:
            raise ValueError("period must be positive")
        if type(self.constant_coefficient) is not ScalarQuantity:
            raise TypeError("constant_coefficient must be ScalarQuantity")
        if type(self.cosine_coefficients) is not VectorQuantity:
            raise TypeError("cosine_coefficients must be VectorQuantity")
        if type(self.sine_coefficients) is not VectorQuantity:
            raise TypeError("sine_coefficients must be VectorQuantity")
        if (
            self.cosine_coefficients.magnitude.shape
            != self.sine_coefficients.magnitude.shape
        ):
            raise ValueError(
                "cosine and sine coefficient inventories must have equal length"
            )
        converter = MODEL_SYSTEM_UNIT_CONVERTER
        if not converter.compatible(
            self.constant_coefficient.unit, self.cosine_coefficients.unit
        ) or not converter.compatible(
            self.constant_coefficient.unit, self.sine_coefficients.unit
        ):
            raise ValueError("all Fourier coefficients must have compatible units")
        object.__setattr__(
            self,
            "cosine_coefficients",
            converter.convert_vector(
                self.cosine_coefficients, self.constant_coefficient.unit
            ),
        )
        object.__setattr__(
            self,
            "sine_coefficients",
            converter.convert_vector(
                self.sine_coefficients, self.constant_coefficient.unit
            ),
        )

    @property
    def harmonic_count(self) -> int:
        """Return the number of retained positive Fourier harmonics."""
        return int(self.cosine_coefficients.magnitude.size)

    def evaluate(self, coordinates: VectorQuantity) -> VectorQuantity:
        """Evaluate the represented potential at finite coordinates."""
        if type(coordinates) is not VectorQuantity:
            raise TypeError("coordinates must be VectorQuantity")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            coordinates.unit, self.period.unit
        ):
            raise ValueError("coordinate and period units must be compatible")
        converted = MODEL_SYSTEM_UNIT_CONVERTER.convert_vector(
            coordinates, self.period.unit
        )
        angles = 2.0 * np.pi * converted.magnitude / self.period.magnitude
        values = np.full(
            converted.magnitude.shape,
            self.constant_coefficient.magnitude,
            dtype=np.float64,
        )
        for harmonic in range(1, self.harmonic_count + 1):
            values += self.cosine_coefficients.magnitude[harmonic - 1] * np.cos(
                float(harmonic) * angles
            )
            values += self.sine_coefficients.magnitude[harmonic - 1] * np.sin(
                float(harmonic) * angles
            )
        return VectorQuantity(values, self.constant_coefficient.unit)

    def reciprocal_period_in(self, target: ScalarQuantity) -> float:
        """Return ``2π/a`` in the unit carried by a positive reciprocal target.

        ``target`` supplies only the requested reciprocal unit. Its magnitude is not
        used. Unitless periods require a unitless target; physical periods require an
        inverse-length target unit.
        """
        if type(target) is not ScalarQuantity:
            raise TypeError("target must be ScalarQuantity")
        if target.magnitude <= 0.0:
            raise ValueError("target must be positive")
        if isinstance(self.period.unit, Unitless):
            if not isinstance(target.unit, Unitless):
                raise ValueError(
                    "a unitless period requires a unitless reciprocal unit"
                )
            return 2.0 * np.pi / self.period.magnitude
        if isinstance(target.unit, Unitless):
            raise ValueError("a physical period requires a physical reciprocal unit")
        if not isinstance(self.period.unit, PhysicalUnit):
            raise TypeError("period unit must be PhysicalUnit or Unitless")
        inverse_period_unit = PhysicalUnit(f"1 / ({self.period.unit.expression})")
        reciprocal_in_target = MODEL_SYSTEM_UNIT_CONVERTER.conversion_factor(
            inverse_period_unit, target.unit
        )
        return (2.0 * np.pi / self.period.magnitude) * reciprocal_in_target
