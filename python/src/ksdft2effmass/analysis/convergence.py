"""Public observed-order analysis for declared finite numerical sequences."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.serialization import SerializableValue


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


@dataclass(frozen=True, slots=True, eq=False)
class RelativeErrorConvergenceResult:
    """Retain relative errors and observed orders for multiple numeric series."""

    spacings: VectorQuantity
    relative_errors: MatrixQuantity
    order_columns: tuple[int, ...]
    observed_orders: MatrixQuantity

    def __post_init__(self) -> None:
        if not isinstance(self.spacings, VectorQuantity):
            raise TypeError("spacings must be VectorQuantity")
        if not isinstance(self.relative_errors, MatrixQuantity):
            raise TypeError("relative_errors must be MatrixQuantity")
        if not isinstance(self.relative_errors.unit, Unitless):
            raise ValueError("relative_errors must be unitless")
        if not isinstance(self.order_columns, tuple) or any(
            type(column) is not int for column in self.order_columns
        ):
            raise TypeError("order_columns must contain built-in integers")
        if not self.order_columns or len(set(self.order_columns)) != len(
            self.order_columns
        ):
            raise ValueError("order_columns must be nonempty and unique")
        if not isinstance(self.observed_orders, MatrixQuantity):
            raise TypeError("observed_orders must be MatrixQuantity")
        if not isinstance(self.observed_orders.unit, Unitless):
            raise ValueError("observed_orders must be unitless")
        levels, series = self.relative_errors.magnitude.shape
        if levels < 2:
            raise ValueError("at least two convergence levels are required")
        spacing_values = self.spacings.magnitude
        error_values = self.relative_errors.magnitude
        if spacing_values.shape != (levels,):
            raise ValueError("spacings must cover every error level")
        if np.any(spacing_values <= 0.0):
            raise ValueError("spacings must be positive")
        if np.any(spacing_values[1:] >= spacing_values[:-1]):
            raise ValueError("spacings must be strictly decreasing")
        if np.any(error_values < 0.0):
            raise ValueError("relative errors must be nonnegative")
        if any(column < 0 or column >= series for column in self.order_columns):
            raise ValueError("order_columns must select available series")
        selected_errors = error_values[:, self.order_columns]
        if np.any(selected_errors <= 0.0):
            raise ValueError("selected relative-error series must be positive")
        observed_values = self.observed_orders.magnitude
        if observed_values.shape != (levels - 1, len(self.order_columns)):
            raise ValueError("observed_orders must cover adjacent selected series")
        expected_orders = np.log(selected_errors[:-1] / selected_errors[1:]) / np.log(
            spacing_values[:-1, np.newaxis] / spacing_values[1:, np.newaxis]
        )
        comparison_scale = max(1.0, float(np.max(np.abs(expected_orders))))
        arithmetic_tolerance = 64.0 * np.finfo(np.float64).eps * comparison_scale
        if not np.allclose(
            observed_values,
            expected_orders,
            rtol=0.0,
            atol=arithmetic_tolerance,
        ):
            raise ValueError(
                "observed_orders must agree with spacings and selected errors"
            )

    def to_dict(self) -> Mapping[str, SerializableValue]:
        """Return the typed scientific values without JSON normalization."""
        return {
            "spacings": self.spacings,
            "relative_errors": self.relative_errors,
            "order_columns": self.order_columns,
            "observed_orders": self.observed_orders,
        }

    @classmethod
    def from_dict(cls, values: Mapping[str, SerializableValue]) -> Self:
        """Reconstruct a result from values restored by the generic codec."""
        if not isinstance(values, Mapping):
            raise TypeError("values must be a mapping")
        if set(values) != {
            "spacings",
            "relative_errors",
            "order_columns",
            "observed_orders",
        }:
            raise ValueError("relative-error convergence fields do not match")
        spacings = values["spacings"]
        relative_errors = values["relative_errors"]
        order_columns = values["order_columns"]
        observed_orders = values["observed_orders"]
        if not isinstance(spacings, VectorQuantity):
            raise TypeError("spacings must decode to VectorQuantity")
        if not isinstance(relative_errors, MatrixQuantity):
            raise TypeError("relative_errors must decode to MatrixQuantity")
        if not isinstance(order_columns, tuple) or any(
            type(column) is not int for column in order_columns
        ):
            raise TypeError("order_columns must decode to an integer tuple")
        if not isinstance(observed_orders, MatrixQuantity):
            raise TypeError("observed_orders must decode to MatrixQuantity")
        return cls(spacings, relative_errors, order_columns, observed_orders)


class RelativeErrorConvergenceAnalyzer:
    """Analyze relative errors and adjacent-level orders for numeric series."""

    __slots__ = ("_order_estimator",)

    def __init__(self) -> None:
        """Compose the reusable adjacent-level order estimator."""
        self._order_estimator = ObservedConvergenceOrderEstimator()

    def execute(
        self,
        *,
        spacings: VectorQuantity,
        approximations: MatrixQuantity,
        references: MatrixQuantity,
        order_columns: tuple[int, ...],
    ) -> RelativeErrorConvergenceResult:
        """Return unitless relative errors and selected observed orders."""
        if not isinstance(spacings, VectorQuantity):
            raise TypeError("spacings must be VectorQuantity")
        if not isinstance(approximations, MatrixQuantity):
            raise TypeError("approximations must be MatrixQuantity")
        if not isinstance(references, MatrixQuantity):
            raise TypeError("references must be MatrixQuantity")
        if approximations.unit != references.unit:
            raise ValueError("approximation and reference units must agree")
        if approximations.magnitude.shape != references.magnitude.shape:
            raise ValueError("approximation and reference shapes must agree")
        if spacings.magnitude.shape != (approximations.magnitude.shape[0],):
            raise ValueError("spacings must cover every approximation level")
        if np.any(references.magnitude == 0.0):
            raise ValueError("references must be nonzero for relative errors")
        if not isinstance(order_columns, tuple) or any(
            type(column) is not int for column in order_columns
        ):
            raise TypeError("order_columns must contain built-in integers")
        series = approximations.magnitude.shape[1]
        if not order_columns or len(set(order_columns)) != len(order_columns):
            raise ValueError("order_columns must be nonempty and unique")
        if any(column < 0 or column >= series for column in order_columns):
            raise ValueError("order_columns must select available series")
        relative_errors = MatrixQuantity(
            np.abs(approximations.magnitude - references.magnitude)
            / np.abs(references.magnitude),
            Unitless(),
        )
        observed_columns = tuple(
            np.asarray(
                [
                    order.order.magnitude
                    for order in self._order_estimator.execute(
                        spacings,
                        VectorQuantity(
                            relative_errors.magnitude[:, column], Unitless()
                        ),
                    ).orders
                ],
                dtype=np.float64,
            )
            for column in order_columns
        )
        observed_orders = MatrixQuantity(
            np.column_stack(observed_columns),
            Unitless(),
        )
        return RelativeErrorConvergenceResult(
            spacings=spacings,
            relative_errors=relative_errors,
            order_columns=order_columns,
            observed_orders=observed_orders,
        )
