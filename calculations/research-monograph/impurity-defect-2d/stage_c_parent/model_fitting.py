"""Ordered model fitting and route-independence policy for Stage C."""

from __future__ import annotations

import hashlib
from typing import cast

import numpy as np

from .model import (
    ComplexMatrix,
    FloatPair,
    JsonValue,
    LocalBond,
    ParentControls,
    PointOperation,
)
from .operator_construction import ParentMatrixConstructor


class ParentModelFitter:
    """Fit each oriented frozen real model class and retain locality residuals."""

    __slots__ = ("_matrix",)

    def __init__(self, matrix: ParentMatrixConstructor) -> None:
        self._matrix = matrix

    def execute(
        self,
        controls: ParentControls,
        target: ComplexMatrix,
        twist: FloatPair,
        route: str,
        operation: PointOperation,
        model_class: str,
    ) -> dict[str, JsonValue]:
        basis = self._basis(controls, twist, route, operation, model_class)
        columns = np.column_stack(
            [
                np.concatenate((value.real.ravel(), value.imag.ravel()))
                for _, value in basis
            ]
        )
        vector = np.concatenate((target.real.ravel(), target.imag.ravel()))
        coefficients, _, rank, _ = np.linalg.lstsq(columns, vector, rcond=None)
        fitted = np.zeros_like(target)
        coefficient_record: dict[str, JsonValue] = {}
        for coefficient, (name, value) in zip(coefficients, basis, strict=True):
            fitted += float(coefficient) * value
            coefficient_record[name] = float(coefficient)
        residual = target - fitted
        maximum = self._matrix.maximum(residual)
        frobenius = float(np.linalg.norm(residual, ord="fro"))
        spectral = float(np.linalg.norm(residual, ord=2))
        shell = self._shell(controls, residual)
        core_exterior = self._core_exterior(controls, residual)
        basis_support = np.zeros_like(target)
        for _, value in basis:
            basis_support += np.abs(value)
        target_support_sha256 = self._support_digest(target)
        fitted_support_sha256 = self._support_digest(fitted)
        exact_support_match = target_support_sha256 == fitted_support_sha256
        return {
            "model_class": model_class,
            "coefficients": coefficient_record,
            "basis_rank": int(rank),
            "residual_maximum_absolute": maximum,
            "residual_frobenius": frobenius,
            "residual_spectral": spectral,
            "residual_shells": cast(JsonValue, shell),
            "core_exterior_coupling_frobenius": core_exterior,
            "basis_support_sha256": self._support_digest(basis_support),
            "target_support_sha256": target_support_sha256,
            "fitted_support_sha256": fitted_support_sha256,
            "residual_support_sha256": self._support_digest(residual),
            "exact_support_match": exact_support_match,
            "accepted": (
                maximum <= controls.criteria["fit_maximum_absolute_EG"]
                and frobenius <= controls.criteria["fit_frobenius_EG"]
                and shell["exterior"]["maximum_absolute"]
                <= controls.criteria["radius_two_exterior_maximum_absolute_EG"]
                and exact_support_match
            ),
        }

    def _basis(
        self,
        controls: ParentControls,
        twist: FloatPair,
        route: str,
        operation: PointOperation,
        model_class: str,
    ) -> tuple[tuple[str, ComplexMatrix], ...]:
        def transformed(term: LocalBond) -> ComplexMatrix:
            return self._matrix.defect(
                controls,
                (self._matrix.transform_bond(term, operation),),
                twist,
                route,
            )

        origin = self._matrix.transform_bond(
            LocalBond((0, 0), (1, 0), 0.0), operation
        ).start
        x_site = self._matrix.transform_bond(
            LocalBond((1, 0), (1, 0), 0.0), operation
        ).start
        y_site = self._matrix.transform_bond(
            LocalBond((0, 1), (1, 0), 0.0), operation
        ).start
        onsite = ("origin_onsite", self._matrix.onsite(controls, origin))
        x_onsite = (
            "positive_x_neighbor_onsite",
            self._matrix.onsite(controls, x_site),
        )
        y_onsite = (
            "positive_y_neighbor_onsite",
            self._matrix.onsite(controls, y_site),
        )
        x_bond = transformed(LocalBond((0, 0), (1, 0), 1.0))
        y_bond = transformed(LocalBond((0, 0), (0, 1), 1.0))
        diagonal = transformed(LocalBond((0, 0), (1, 1), 1.0))
        if model_class == "point_scalar_onsite":
            return (onsite,)
        if model_class == "finite_support_diagonal_onsite":
            return onsite, x_onsite, y_onsite
        if model_class == "onsite_plus_isotropic_nearest_neighbor":
            return onsite, ("isotropic_nearest_neighbor", x_bond + y_bond)
        if model_class == "onsite_plus_directional_nearest_neighbor":
            return (
                onsite,
                ("positive_x_bond", x_bond),
                (
                    "positive_y_bond",
                    y_bond,
                ),
            )
        if model_class == "finite_range_nonlocal_radius_two":
            return (
                onsite,
                ("positive_x_bond", x_bond),
                ("positive_y_bond", y_bond),
                ("positive_diagonal_bond", diagonal),
            )
        raise ValueError(f"unsupported model class {model_class}")

    @staticmethod
    def _shell(
        controls: ParentControls, residual: ComplexMatrix
    ) -> dict[str, dict[str, float]]:
        values: dict[str, list[complex]] = {
            "0": [],
            "1": [],
            "2": [],
            "exterior": [],
        }
        for row in range(controls.dimension):
            rx, ry = divmod(row, controls.ny)
            for column in range(controls.dimension):
                value = complex(residual[row, column])
                if value == 0.0:
                    continue
                cx, cy = divmod(column, controls.ny)
                shell = max(
                    min(rx, controls.nx - rx),
                    min(ry, controls.ny - ry),
                    min(cx, controls.nx - cx),
                    min(cy, controls.ny - cy),
                )
                key = str(shell) if shell <= 2 else "exterior"
                values[key].append(value)
        return {
            key: {
                "maximum_absolute": max((abs(value) for value in entries), default=0.0),
                "frobenius": float(np.sqrt(sum(abs(value) ** 2 for value in entries))),
            }
            for key, entries in values.items()
        }

    @staticmethod
    def _core_exterior(controls: ParentControls, matrix: ComplexMatrix) -> float:
        core: list[int] = []
        for index in range(controls.dimension):
            x, y = divmod(index, controls.ny)
            if max(min(x, controls.nx - x), min(y, controls.ny - y)) <= 2:
                core.append(index)
        exterior = [index for index in range(controls.dimension) if index not in core]
        return float(
            np.sqrt(
                np.linalg.norm(matrix[np.ix_(core, exterior)], ord="fro") ** 2
                + np.linalg.norm(matrix[np.ix_(exterior, core)], ord="fro") ** 2
            )
        )

    @staticmethod
    def _support_digest(matrix: ComplexMatrix) -> str:
        support = np.argwhere(np.abs(matrix) > 1.0e-12)
        return hashlib.sha256(
            np.ascontiguousarray(support, dtype="<i8").tobytes()
        ).hexdigest()


class RouteIndependenceGate:
    """Reject a route constructor that declares another route as its source."""

    __slots__ = ()

    @staticmethod
    def execute(route: str, source: str) -> None:
        expected = {
            "A_centered_uniform": "compact_parent_inputs",
            "B_reduced_seam": "compact_parent_inputs",
        }
        if route not in expected:
            raise ValueError(f"unsupported route provenance {route}")
        if source != expected[route]:
            raise ValueError("DEFECT_2D.ROUTE_INDEPENDENCE_VIOLATION")
