"""Semantic result sections for one direct QHO1D comparison case."""

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

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue


def _unitless(
    value: ScalarQuantity | VectorQuantity | MatrixQuantity, name: str
) -> None:
    if not isinstance(value.unit, Unitless):
        raise ValueError(f"{name} must use Unitless")


def _quantity[QuantityT: (ScalarQuantity, VectorQuantity, MatrixQuantity)](
    values: Mapping[str, SerializableValue],
    name: str,
    expected: type[QuantityT],
) -> QuantityT:
    value = values[name]
    if not isinstance(value, expected):
        raise TypeError(f"{name} must decode to {expected.__name__}")
    return value


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dSpatialRepresentationResult(BaseTypedRecord):
    """Describe one finite Dirichlet spatial representation."""

    box_half_width: ScalarQuantity
    requested_grid_spacing: ScalarQuantity
    grid_spacing: ScalarQuantity
    retained_dimension: int
    interior_points: int
    grid_coordinates: VectorQuantity

    def __post_init__(self) -> None:
        for name in ("box_half_width", "requested_grid_spacing", "grid_spacing"):
            value = getattr(self, name)
            if not isinstance(value, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
            _unitless(value, name)
            if not np.isfinite(value.magnitude) or value.magnitude <= 0.0:
                raise ValueError(f"{name} must be positive and finite")
        for name in ("retained_dimension", "interior_points"):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if self.retained_dimension > self.interior_points:
            raise ValueError("retained_dimension exceeds interior_points")
        if not isinstance(self.grid_coordinates, VectorQuantity):
            raise TypeError("grid_coordinates must be VectorQuantity")
        _unitless(self.grid_coordinates, "grid_coordinates")
        if self.grid_coordinates.magnitude.shape != (self.interior_points,):
            raise ValueError("grid_coordinates shape does not match interior_points")
        if not np.all(np.diff(self.grid_coordinates.magnitude) > 0.0):
            raise ValueError("grid_coordinates must be strictly increasing")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "box_half_width": self.box_half_width,
            "requested_grid_spacing": self.requested_grid_spacing,
            "grid_spacing": self.grid_spacing,
            "retained_dimension": self.retained_dimension,
            "interior_points": self.interior_points,
            "grid_coordinates": self.grid_coordinates,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        fields = {
            "box_half_width",
            "requested_grid_spacing",
            "grid_spacing",
            "retained_dimension",
            "interior_points",
            "grid_coordinates",
        }
        if set(values) != fields:
            raise ValueError("spatial-representation fields do not match")
        retained = values["retained_dimension"]
        points = values["interior_points"]
        if type(retained) is not int or type(points) is not int:
            raise TypeError("spatial dimensions must decode to built-in ints")
        return cls(
            box_half_width=_quantity(values, "box_half_width", ScalarQuantity),
            requested_grid_spacing=_quantity(
                values, "requested_grid_spacing", ScalarQuantity
            ),
            grid_spacing=_quantity(values, "grid_spacing", ScalarQuantity),
            retained_dimension=retained,
            interior_points=points,
            grid_coordinates=_quantity(values, "grid_coordinates", VectorQuantity),
        )


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dSampledStateAlignmentResult(BaseTypedRecord):
    """Retain the sampled-state Gram correction and coordinate injection."""

    injection: MatrixQuantity
    gram_matrix: MatrixQuantity
    gram_inverse_square_root: MatrixQuantity
    gram_deviation: ScalarQuantity
    gram_condition_number: ScalarQuantity
    injection_isometry_error: ScalarQuantity

    def __post_init__(self) -> None:
        for name in ("injection", "gram_matrix", "gram_inverse_square_root"):
            value = getattr(self, name)
            if not isinstance(value, MatrixQuantity):
                raise TypeError(f"{name} must be MatrixQuantity")
            _unitless(value, name)
        for name in (
            "gram_deviation",
            "gram_condition_number",
            "injection_isometry_error",
        ):
            value = getattr(self, name)
            if not isinstance(value, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
            _unitless(value, name)
            if not np.isfinite(value.magnitude):
                raise ValueError(f"{name} must be finite")
        if self.gram_deviation.magnitude < 0.0:
            raise ValueError("gram_deviation must be nonnegative")
        if self.gram_condition_number.magnitude <= 0.0:
            raise ValueError("gram_condition_number must be positive")
        if self.injection_isometry_error.magnitude < 0.0:
            raise ValueError("injection_isometry_error must be nonnegative")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {name: getattr(self, name) for name in self.__dataclass_fields__}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != set(cls.__dataclass_fields__):
            raise ValueError("sampled-state-alignment fields do not match")
        return cls(
            injection=_quantity(values, "injection", MatrixQuantity),
            gram_matrix=_quantity(values, "gram_matrix", MatrixQuantity),
            gram_inverse_square_root=_quantity(
                values, "gram_inverse_square_root", MatrixQuantity
            ),
            gram_deviation=_quantity(values, "gram_deviation", ScalarQuantity),
            gram_condition_number=_quantity(
                values, "gram_condition_number", ScalarQuantity
            ),
            injection_isometry_error=_quantity(
                values, "injection_isometry_error", ScalarQuantity
            ),
        )


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dHamiltonianComparisonResult(BaseTypedRecord):
    """Retain aligned Hamiltonians and discrepancy channels."""

    pulled_back_hamiltonian: MatrixQuantity
    reference_hamiltonian: MatrixQuantity
    difference: MatrixQuantity
    absolute_discrepancy: ScalarQuantity
    relative_discrepancy: ScalarQuantity
    diagonal_discrepancy: ScalarQuantity
    off_diagonal_discrepancy: ScalarQuantity

    def __post_init__(self) -> None:
        for name in (
            "pulled_back_hamiltonian",
            "reference_hamiltonian",
            "difference",
        ):
            value = getattr(self, name)
            if not isinstance(value, MatrixQuantity):
                raise TypeError(f"{name} must be MatrixQuantity")
            _unitless(value, name)
        for name in (
            "absolute_discrepancy",
            "relative_discrepancy",
            "diagonal_discrepancy",
            "off_diagonal_discrepancy",
        ):
            value = getattr(self, name)
            if not isinstance(value, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
            _unitless(value, name)
            if not np.isfinite(value.magnitude) or value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative and finite")
        if not np.array_equal(
            self.pulled_back_hamiltonian.magnitude
            - self.reference_hamiltonian.magnitude,
            self.difference.magnitude,
        ):
            raise ValueError("difference must equal pullback minus reference")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {name: getattr(self, name) for name in self.__dataclass_fields__}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != set(cls.__dataclass_fields__):
            raise ValueError("Hamiltonian-comparison fields do not match")
        return cls(
            pulled_back_hamiltonian=_quantity(
                values, "pulled_back_hamiltonian", MatrixQuantity
            ),
            reference_hamiltonian=_quantity(
                values, "reference_hamiltonian", MatrixQuantity
            ),
            difference=_quantity(values, "difference", MatrixQuantity),
            absolute_discrepancy=_quantity(
                values, "absolute_discrepancy", ScalarQuantity
            ),
            relative_discrepancy=_quantity(
                values, "relative_discrepancy", ScalarQuantity
            ),
            diagonal_discrepancy=_quantity(
                values, "diagonal_discrepancy", ScalarQuantity
            ),
            off_diagonal_discrepancy=_quantity(
                values, "off_diagonal_discrepancy", ScalarQuantity
            ),
        )


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dResidualResult(BaseTypedRecord):
    """Retain the full-space intertwining residual norm."""

    frobenius: ScalarQuantity

    def __post_init__(self) -> None:
        if not isinstance(self.frobenius, ScalarQuantity):
            raise TypeError("frobenius must be ScalarQuantity")
        _unitless(self.frobenius, "frobenius")
        if not np.isfinite(self.frobenius.magnitude) or self.frobenius.magnitude < 0.0:
            raise ValueError("frobenius must be nonnegative and finite")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"frobenius": self.frobenius}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {"frobenius"}:
            raise ValueError("residual fields do not match")
        return cls(frobenius=_quantity(values, "frobenius", ScalarQuantity))
