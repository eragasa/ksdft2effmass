"""Typed configuration for direct QHO1D spatial-truncation calculations."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, cast

import numpy as np

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .parameters import (
    Qho1dNondimensionalizationRequest,
    Qho1dNondimensionalizer,
    Qho1dParameters,
)


@dataclass(frozen=True, slots=True)
class Qho1dConfiguration(BaseTypedRecord):
    """Declare one nondimensional QHO1D comparison sweep.

    Parameters
    ----------
    hbar, mass, omega
        Positive finite nondimensional oscillator parameters.
    box_half_widths
        Strictly increasing positive finite box half-widths.
    grid_spacings
        Strictly decreasing positive finite requested grid spacings.
    retained_dimensions
        Strictly increasing positive retained number-state dimensions.
    selected_box_half_width, selected_grid_spacing, selected_retained_dimension
        One member of each sweep used for the state-resolved visualization.
    displayed_states
        Positive number of selected states rendered by state-resolved plots.

    Raises
    ------
    TypeError
        A scalar or tuple has the wrong exact built-in type.
    ValueError
        A value is nonfinite, nonpositive, incorrectly ordered, absent from its
        sweep, or incompatible with the displayed-state inventory.

    Notes
    -----
    This configuration declares a finite represented comparison. It does not define
    a continuum limit, physical uncertainty model, or semiconductor validation.
    """

    hbar: float
    mass: float
    omega: float
    box_half_widths: tuple[float, ...]
    grid_spacings: tuple[float, ...]
    retained_dimensions: tuple[int, ...]
    selected_box_half_width: float
    selected_grid_spacing: float
    selected_retained_dimension: int
    displayed_states: int

    def __post_init__(self) -> None:
        for name, value in (
            ("hbar", self.hbar),
            ("mass", self.mass),
            ("omega", self.omega),
            ("selected_box_half_width", self.selected_box_half_width),
            ("selected_grid_spacing", self.selected_grid_spacing),
        ):
            self._positive_float(value, name)
        self._float_sweep(self.box_half_widths, "box_half_widths", increasing=True)
        self._float_sweep(self.grid_spacings, "grid_spacings", increasing=False)
        self._integer_sweep(self.retained_dimensions, "retained_dimensions")
        for name, value in (
            ("selected_retained_dimension", self.selected_retained_dimension),
            ("displayed_states", self.displayed_states),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if self.selected_box_half_width not in self.box_half_widths:
            raise ValueError("selected_box_half_width must belong to box_half_widths")
        if self.selected_grid_spacing not in self.grid_spacings:
            raise ValueError("selected_grid_spacing must belong to grid_spacings")
        if self.selected_retained_dimension not in self.retained_dimensions:
            raise ValueError(
                "selected_retained_dimension must belong to retained_dimensions"
            )
        if self.displayed_states > self.selected_retained_dimension:
            raise ValueError("displayed_states exceeds selected_retained_dimension")

    @property
    def parameters(self) -> Qho1dParameters:
        """Return the first-class nondimensional oscillator parameters.

        Returns
        -------
        Qho1dParameters
            Unitless parameter aggregate consumed by the three QHO1D model owners.
        """
        return Qho1dNondimensionalizer(
            Qho1dNondimensionalizationRequest(self.hbar, self.mass, self.omega)
        ).execute()

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "hbar": self.hbar,
            "mass": self.mass,
            "omega": self.omega,
            "box_half_widths": self.box_half_widths,
            "grid_spacings": self.grid_spacings,
            "retained_dimensions": self.retained_dimensions,
            "selected_box_half_width": self.selected_box_half_width,
            "selected_grid_spacing": self.selected_grid_spacing,
            "selected_retained_dimension": self.selected_retained_dimension,
            "displayed_states": self.displayed_states,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        fields = {
            "hbar",
            "mass",
            "omega",
            "box_half_widths",
            "grid_spacings",
            "retained_dimensions",
            "selected_box_half_width",
            "selected_grid_spacing",
            "selected_retained_dimension",
            "displayed_states",
        }
        if set(values) != fields:
            raise ValueError("QHO1D configuration fields do not match")
        hbar = values["hbar"]
        mass = values["mass"]
        omega = values["omega"]
        box_half_widths = values["box_half_widths"]
        grid_spacings = values["grid_spacings"]
        retained_dimensions = values["retained_dimensions"]
        selected_box_half_width = values["selected_box_half_width"]
        selected_grid_spacing = values["selected_grid_spacing"]
        selected_retained_dimension = values["selected_retained_dimension"]
        displayed_states = values["displayed_states"]
        if any(
            type(value) is not float
            for value in (
                hbar,
                mass,
                omega,
                selected_box_half_width,
                selected_grid_spacing,
            )
        ):
            raise TypeError("QHO1D real configuration fields must decode to floats")
        if not (
            isinstance(box_half_widths, tuple)
            and all(type(value) is float for value in box_half_widths)
        ):
            raise TypeError("box_half_widths must decode to a tuple of floats")
        if not (
            isinstance(grid_spacings, tuple)
            and all(type(value) is float for value in grid_spacings)
        ):
            raise TypeError("grid_spacings must decode to a tuple of floats")
        if not (
            isinstance(retained_dimensions, tuple)
            and all(type(value) is int for value in retained_dimensions)
        ):
            raise TypeError("retained_dimensions must decode to a tuple of ints")
        if (
            type(selected_retained_dimension) is not int
            or type(displayed_states) is not int
        ):
            raise TypeError("QHO1D integer configuration fields must decode to ints")
        return cls(
            hbar=cast(float, hbar),
            mass=cast(float, mass),
            omega=cast(float, omega),
            box_half_widths=box_half_widths,
            grid_spacings=grid_spacings,
            retained_dimensions=retained_dimensions,
            selected_box_half_width=cast(float, selected_box_half_width),
            selected_grid_spacing=cast(float, selected_grid_spacing),
            selected_retained_dimension=selected_retained_dimension,
            displayed_states=displayed_states,
        )

    @staticmethod
    def _positive_float(value: float, name: str) -> None:
        if type(value) is not float:
            raise TypeError(f"{name} must be a built-in float")
        if not np.isfinite(value) or value <= 0.0:
            raise ValueError(f"{name} must be positive and finite")

    @classmethod
    def _float_sweep(
        cls,
        values: tuple[float, ...],
        name: str,
        *,
        increasing: bool,
    ) -> None:
        if not isinstance(values, tuple) or any(
            type(value) is not float for value in values
        ):
            raise TypeError(f"{name} must be a tuple of built-in floats")
        if not values:
            raise ValueError(f"{name} must be nonempty")
        for value in values:
            cls._positive_float(value, name)
        expected = tuple(sorted(set(values), reverse=not increasing))
        if values != expected:
            direction = "increasing" if increasing else "decreasing"
            raise ValueError(f"{name} must be strictly {direction}")

    @staticmethod
    def _integer_sweep(values: tuple[int, ...], name: str) -> None:
        if not isinstance(values, tuple) or any(
            type(value) is not int for value in values
        ):
            raise TypeError(f"{name} must be a tuple of built-in ints")
        if not values or any(value <= 0 for value in values):
            raise ValueError(f"{name} must contain positive values")
        if values != tuple(sorted(set(values))):
            raise ValueError(f"{name} must be strictly increasing")
