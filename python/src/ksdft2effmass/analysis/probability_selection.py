"""Reusable finite-probability tail selection."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np
from projectkoios.physkit.units import Unitless, VectorQuantity

from ksdft2effmass.serialization import SerializableValue


@dataclass(frozen=True, slots=True, eq=False)
class TailProbabilitySelection:
    """Retain cumulative omitted probabilities and the first passing count."""

    probabilities: VectorQuantity
    omitted_probabilities: VectorQuantity
    tolerance: float
    selected_count: int

    def __post_init__(self) -> None:
        if not isinstance(self.probabilities, VectorQuantity):
            raise TypeError("probabilities must be VectorQuantity")
        if not isinstance(self.probabilities.unit, Unitless):
            raise ValueError("probabilities must be unitless")
        if not isinstance(self.omitted_probabilities, VectorQuantity):
            raise TypeError("omitted_probabilities must be VectorQuantity")
        if not isinstance(self.omitted_probabilities.unit, Unitless):
            raise ValueError("omitted_probabilities must be unitless")
        probabilities = self.probabilities.magnitude
        omitted = self.omitted_probabilities.magnitude
        if probabilities.size == 0:
            raise ValueError("probabilities must be nonempty")
        if omitted.shape != probabilities.shape:
            raise ValueError("omitted probabilities must cover every candidate count")
        if np.any(probabilities < 0.0):
            raise ValueError("probabilities must be nonnegative")
        arithmetic_tolerance = (
            64.0 * np.finfo(np.float64).eps * max(1, probabilities.size)
        )
        if not np.isclose(
            np.sum(probabilities),
            1.0,
            rtol=0.0,
            atol=arithmetic_tolerance,
        ):
            raise ValueError("probabilities must sum to one")
        expected_omitted = np.concatenate(
            (
                np.cumsum(probabilities[:0:-1], dtype=np.float64)[::-1],
                np.asarray([0.0], dtype=np.float64),
            )
        )
        if not np.allclose(
            omitted,
            expected_omitted,
            rtol=0.0,
            atol=arithmetic_tolerance,
        ):
            raise ValueError(
                "omitted_probabilities must equal cumulative probability tails"
            )
        if np.any(omitted[1:] > omitted[:-1] + arithmetic_tolerance):
            raise ValueError("omitted probabilities must be nonincreasing")
        if type(self.tolerance) is not float or not np.isfinite(self.tolerance):
            raise TypeError("tolerance must be a finite built-in float")
        if not 0.0 < self.tolerance < 1.0:
            raise ValueError("tolerance must lie strictly between zero and one")
        if type(self.selected_count) is not int:
            raise TypeError("selected_count must be a built-in integer")
        if not 1 <= self.selected_count <= probabilities.size:
            raise ValueError("selected_count must select an available candidate")
        passing = np.flatnonzero(omitted <= self.tolerance)
        if passing.size == 0 or self.selected_count != int(passing[0]) + 1:
            raise ValueError("selected_count must be the first passing candidate")

    def to_dict(self) -> Mapping[str, SerializableValue]:
        """Return typed scientific values without JSON normalization."""
        return {
            "probabilities": self.probabilities,
            "omitted_probabilities": self.omitted_probabilities,
            "tolerance": self.tolerance,
            "selected_count": self.selected_count,
        }

    @classmethod
    def from_dict(cls, values: Mapping[str, SerializableValue]) -> Self:
        """Reconstruct a selection from values restored by the generic codec."""
        if not isinstance(values, Mapping):
            raise TypeError("values must be a mapping")
        if set(values) != {
            "probabilities",
            "omitted_probabilities",
            "tolerance",
            "selected_count",
        }:
            raise ValueError("tail-probability selection fields do not match")
        probabilities = values["probabilities"]
        omitted_probabilities = values["omitted_probabilities"]
        tolerance = values["tolerance"]
        selected_count = values["selected_count"]
        if not isinstance(probabilities, VectorQuantity):
            raise TypeError("probabilities must decode to VectorQuantity")
        if not isinstance(omitted_probabilities, VectorQuantity):
            raise TypeError("omitted_probabilities must decode to VectorQuantity")
        if type(tolerance) is not float:
            raise TypeError("tolerance must decode to a built-in float")
        if type(selected_count) is not int:
            raise TypeError("selected_count must decode to a built-in integer")
        return cls(
            probabilities=probabilities,
            omitted_probabilities=omitted_probabilities,
            tolerance=tolerance,
            selected_count=selected_count,
        )


@dataclass(frozen=True, slots=True, eq=False)
class TailProbabilitySelectionRequest:
    """Bind one normalized finite probability inventory and tail tolerance."""

    probabilities: VectorQuantity
    tolerance: float

    def __post_init__(self) -> None:
        """Admit normalization, nonnegativity, and the strict tail tolerance."""
        if not isinstance(self.probabilities, VectorQuantity):
            raise TypeError("probabilities must be VectorQuantity")
        if not isinstance(self.probabilities.unit, Unitless):
            raise ValueError("probabilities must be unitless")
        values = self.probabilities.magnitude
        if values.size == 0:
            raise ValueError("probabilities must be nonempty")
        if np.any(values < 0.0):
            raise ValueError("probabilities must be nonnegative")
        arithmetic_tolerance = 64.0 * np.finfo(np.float64).eps * max(1, values.size)
        if not np.isclose(
            np.sum(values),
            1.0,
            rtol=0.0,
            atol=arithmetic_tolerance,
        ):
            raise ValueError("probabilities must sum to one")
        if type(self.tolerance) is not float or not np.isfinite(self.tolerance):
            raise TypeError("tolerance must be a finite built-in float")
        if not 0.0 < self.tolerance < 1.0:
            raise ValueError("tolerance must lie strictly between zero and one")


class TailProbabilitySelector:
    """Select a prefix for one constructor-bound finite probability inventory."""

    __slots__ = ("_request",)

    def __init__(self, request: TailProbabilitySelectionRequest) -> None:
        if type(request) is not TailProbabilitySelectionRequest:
            raise TypeError("request must be TailProbabilitySelectionRequest")
        self._request = request

    @property
    def request(self) -> TailProbabilitySelectionRequest:
        """Return the complete immutable tail-selection request."""
        return self._request

    def execute(self) -> TailProbabilitySelection:
        """Return cumulative tails and the first candidate within tolerance."""
        probabilities = self.request.probabilities
        tolerance = self.request.tolerance
        values = probabilities.magnitude
        omitted = np.concatenate(
            (
                np.cumsum(values[:0:-1], dtype=np.float64)[::-1],
                np.asarray([0.0], dtype=np.float64),
            )
        )
        passing = np.flatnonzero(omitted <= tolerance)
        if passing.size == 0:
            raise RuntimeError("no retained count satisfies the tail tolerance")
        return TailProbabilitySelection(
            probabilities=probabilities,
            omitted_probabilities=VectorQuantity(omitted, Unitless()),
            tolerance=tolerance,
            selected_count=int(passing[0]) + 1,
        )
