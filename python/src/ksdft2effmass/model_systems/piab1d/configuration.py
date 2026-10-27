"""Typed PIAB1D calculation configuration consumed by verification."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue


@dataclass(frozen=True, slots=True)
class Piab1dConfiguration(BaseTypedRecord):
    """Retain the closed represented-PIAB1D configuration contract.

    Parameters
    ----------
    unit_system
        Exact ``"nondimensional"`` model-system identifier.
    hbar
        Reduced Planck constant. The successor convention requires exactly ``1.0``.
    length
        Positive dimensionless box length.
    mass
        Positive dimensionless particle mass.
    interior_points
        Number of finite-difference interior degrees of freedom; greater than one.
    retained_dimension
        Number of lowest-energy states retained in the spectral reduction.
    boundary_condition
        Exact ``"homogeneous Dirichlet"`` boundary identifier.
    grid_convention
        Exact represented-grid coordinate convention.
    euclidean_normalization
        Exact normalization convention of the solver eigenvectors.

    Raises
    ------
    TypeError
        A scalar or dimension has the wrong exact type or is nonfinite.
    ValueError
        A convention label, positivity rule, or retained-space bound is invalid.

    Notes
    -----
    The record declares a mathematical and numerical convention. It carries no
    verification tolerance and grants no execution authority.
    """

    unit_system: str
    hbar: float
    length: float
    mass: float
    interior_points: int
    retained_dimension: int
    boundary_condition: str
    grid_convention: str
    euclidean_normalization: str

    def __post_init__(self) -> None:
        if self.unit_system != "nondimensional":
            raise ValueError("unit_system must be nondimensional")
        for value, name in (
            (self.hbar, "hbar"),
            (self.length, "length"),
            (self.mass, "mass"),
        ):
            if type(value) is not float or not np.isfinite(value):
                raise TypeError(f"{name} must be a finite built-in float")
        if self.hbar != 1.0:
            raise ValueError("hbar must equal one for this convention")
        if self.length <= 0.0 or self.mass <= 0.0:
            raise ValueError("length and mass must be positive")
        if type(self.interior_points) is not int or self.interior_points <= 1:
            raise ValueError("interior_points must be a built-in integer above one")
        if (
            type(self.retained_dimension) is not int
            or not 1 <= self.retained_dimension <= self.interior_points
        ):
            raise ValueError("retained_dimension must select the represented space")
        if self.boundary_condition != "homogeneous Dirichlet":
            raise ValueError("boundary_condition must be homogeneous Dirichlet")
        if self.grid_convention != ("uniform full grid with interior-only Hamiltonian"):
            raise ValueError("grid_convention does not identify the represented grid")
        if self.euclidean_normalization != "finite-dimensional Euclidean":
            raise ValueError("euclidean_normalization convention is unsupported")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "unit_system": self.unit_system,
            "hbar": self.hbar,
            "length": self.length,
            "mass": self.mass,
            "interior_points": self.interior_points,
            "retained_dimension": self.retained_dimension,
            "boundary_condition": self.boundary_condition,
            "grid_convention": self.grid_convention,
            "euclidean_normalization": self.euclidean_normalization,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "unit_system",
            "hbar",
            "length",
            "mass",
            "interior_points",
            "retained_dimension",
            "boundary_condition",
            "grid_convention",
            "euclidean_normalization",
        }
        if set(values) != required:
            raise ValueError("PIAB1D configuration fields do not match")
        unit_system = values["unit_system"]
        hbar = values["hbar"]
        length = values["length"]
        mass = values["mass"]
        interior_points = values["interior_points"]
        retained_dimension = values["retained_dimension"]
        boundary_condition = values["boundary_condition"]
        grid_convention = values["grid_convention"]
        euclidean_normalization = values["euclidean_normalization"]
        if (
            type(unit_system) is not str
            or type(boundary_condition) is not str
            or type(grid_convention) is not str
            or type(euclidean_normalization) is not str
        ):
            raise TypeError("configuration labels must be built-in strings")
        if (
            type(hbar) is not float
            or type(length) is not float
            or type(mass) is not float
        ):
            raise TypeError("configuration scalars must be built-in floats")
        if type(interior_points) is not int or type(retained_dimension) is not int:
            raise TypeError("configuration dimensions must be built-in integers")
        return cls(
            unit_system=unit_system,
            hbar=hbar,
            length=length,
            mass=mass,
            interior_points=interior_points,
            retained_dimension=retained_dimension,
            boundary_condition=boundary_condition,
            grid_convention=grid_convention,
            euclidean_normalization=euclidean_normalization,
        )
