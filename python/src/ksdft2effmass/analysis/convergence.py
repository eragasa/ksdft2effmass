"""Public observed-order analysis for declared finite numerical sequences."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import ScalarQuantity, Unitless, VectorQuantity


@dataclass(frozen=True, slots=True)
class ObservedConvergenceOrder:
    """Record one adjacent-level observed convergence-order calculation."""

    coarse_spacing: ScalarQuantity
    fine_spacing: ScalarQuantity
    coarse_error: ScalarQuantity
    fine_error: ScalarQuantity
    order: ScalarQuantity

    def __post_init__(self) -> None:
        for quantity, name in (
            (self.coarse_spacing, "coarse_spacing"),
            (self.fine_spacing, "fine_spacing"),
            (self.coarse_error, "coarse_error"),
            (self.fine_error, "fine_error"),
            (self.order, "order"),
        ):
            if not isinstance(quantity, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
        if self.coarse_spacing.unit != self.fine_spacing.unit:
            raise ValueError("spacing units must agree exactly")
        if self.coarse_error.unit != self.fine_error.unit:
            raise ValueError("error units must agree exactly")
        if not isinstance(self.order.unit, Unitless):
            raise ValueError("observed order must be Unitless")
        if self.coarse_spacing.magnitude <= self.fine_spacing.magnitude:
            raise ValueError("coarse spacing must exceed fine spacing")
        if self.coarse_error.magnitude <= 0.0 or self.fine_error.magnitude <= 0.0:
            raise ValueError("errors must be positive")


@dataclass(frozen=True, slots=True)
class ObservedConvergenceOrderResult:
    """Retain one sequence and every adjacent-level observed order."""

    spacings: VectorQuantity
    errors: VectorQuantity
    orders: tuple[ObservedConvergenceOrder, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.spacings, VectorQuantity):
            raise TypeError("spacings must be VectorQuantity")
        if not isinstance(self.errors, VectorQuantity):
            raise TypeError("errors must be VectorQuantity")
        if self.spacings.magnitude.shape != self.errors.magnitude.shape:
            raise ValueError("spacings and errors must have equal lengths")
        if self.spacings.magnitude.size < 2:
            raise ValueError("at least two levels are required")
        if not isinstance(self.orders, tuple) or any(
            not isinstance(order, ObservedConvergenceOrder) for order in self.orders
        ):
            raise TypeError("orders must contain ObservedConvergenceOrder values")
        if len(self.orders) != self.spacings.magnitude.size - 1:
            raise ValueError("orders must cover every adjacent level pair")

    def nullable_orders(self) -> tuple[None | float, ...]:
        """Return the historical leading-None sequence representation."""
        return (None, *(order.order.magnitude for order in self.orders))


class ObservedConvergenceOrderEstimator:
    """Estimate adjacent-level orders from positive errors and decreasing spacings."""

    __slots__ = ()

    def execute(
        self, spacings: VectorQuantity, errors: VectorQuantity
    ) -> ObservedConvergenceOrderResult:
        """Return ``log(e_i/e_j) / log(h_i/h_j)`` for adjacent levels."""
        if not isinstance(spacings, VectorQuantity):
            raise TypeError("spacings must be VectorQuantity")
        if not isinstance(errors, VectorQuantity):
            raise TypeError("errors must be VectorQuantity")
        if spacings.magnitude.shape != errors.magnitude.shape:
            raise ValueError("spacings and errors must have equal lengths")
        if spacings.magnitude.size < 2:
            raise ValueError("at least two levels are required")
        if np.any(spacings.magnitude <= 0.0):
            raise ValueError("spacings must be positive")
        if np.any(errors.magnitude <= 0.0):
            raise ValueError("errors must be positive")
        if np.any(spacings.magnitude[1:] >= spacings.magnitude[:-1]):
            raise ValueError("spacings must be strictly decreasing")
        orders = tuple(
            ObservedConvergenceOrder(
                coarse_spacing=ScalarQuantity(float(coarse_h), spacings.unit),
                fine_spacing=ScalarQuantity(float(fine_h), spacings.unit),
                coarse_error=ScalarQuantity(float(coarse_error), errors.unit),
                fine_error=ScalarQuantity(float(fine_error), errors.unit),
                order=ScalarQuantity(
                    float(
                        np.log(coarse_error / fine_error) / np.log(coarse_h / fine_h)
                    ),
                    Unitless(),
                ),
            )
            for coarse_h, fine_h, coarse_error, fine_error in zip(
                spacings.magnitude[:-1],
                spacings.magnitude[1:],
                errors.magnitude[:-1],
                errors.magnitude[1:],
                strict=True,
            )
        )
        return ObservedConvergenceOrderResult(spacings, errors, orders)
