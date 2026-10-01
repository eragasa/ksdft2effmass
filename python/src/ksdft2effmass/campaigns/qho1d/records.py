"""Immutable records for the research-monograph harmonic-oscillator study."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.analysis.model_systems.harmonic_oscillator import (
    HarmonicOscillatorComparisonResult,
    HarmonicOscillatorParameters,
)


@dataclass(frozen=True, slots=True)
class HarmonicOscillatorStudyDefinition:
    """Define the exact finite harmonic-oscillator parameter sweep.

    Parameters
    ----------
    study_id
        Nonempty stable study identifier.
    evidence_status
        Exact evidence label. Version one requires
        ``"illustrative numerical experiment"``.
    parameters
        Harmonic-oscillator physical parameters.
    box_half_widths
        Nonempty strictly increasing tuple of positive built-in ``float`` values.
    grid_spacings
        Nonempty strictly decreasing tuple of positive built-in ``float`` values.
    retained_dimensions
        Nonempty strictly increasing tuple of positive built-in ``int`` values.
    spatial_representation
        Nonempty description of the finite spatial representation.
    comparison_map
        Nonempty description of the map into common coordinates.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If a field violates the closed study invariants.
    """

    study_id: str
    evidence_status: str
    parameters: HarmonicOscillatorParameters
    box_half_widths: tuple[float, ...]
    grid_spacings: tuple[float, ...]
    retained_dimensions: tuple[int, ...]
    spatial_representation: str
    comparison_map: str

    def __post_init__(self) -> None:
        if not isinstance(self.study_id, str):
            raise TypeError("study_id must be a string")
        if not self.study_id:
            raise ValueError("study_id must be nonempty")
        if not isinstance(self.evidence_status, str):
            raise TypeError("evidence_status must be a string")
        if self.evidence_status != "illustrative numerical experiment":
            raise ValueError("evidence_status must identify an illustrative experiment")
        if not isinstance(self.parameters, HarmonicOscillatorParameters):
            raise TypeError("parameters must be HarmonicOscillatorParameters")
        self.validate_real_sweep(
            self.box_half_widths, "box_half_widths", increasing=True
        )
        self.validate_real_sweep(self.grid_spacings, "grid_spacings", increasing=False)
        if not isinstance(self.retained_dimensions, tuple):
            raise TypeError("retained_dimensions must be a tuple")
        if not self.retained_dimensions:
            raise ValueError("retained_dimensions must be nonempty")
        if any(type(value) is not int for value in self.retained_dimensions):
            raise TypeError("retained_dimensions values must be built-in ints")
        if any(value <= 0 for value in self.retained_dimensions):
            raise ValueError("retained_dimensions values must be positive")
        if tuple(sorted(set(self.retained_dimensions))) != self.retained_dimensions:
            raise ValueError("retained_dimensions must be strictly increasing")
        self.validate_nonempty_string(
            self.spatial_representation, "spatial_representation"
        )
        self.validate_nonempty_string(self.comparison_map, "comparison_map")

    @staticmethod
    def validate_nonempty_string(value: str, name: str) -> None:
        """Validate one intrinsic nonempty built-in string field."""
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string")
        if not value:
            raise ValueError(f"{name} must be nonempty")

    @staticmethod
    def validate_real_sweep(
        values: tuple[float, ...], name: str, *, increasing: bool
    ) -> None:
        """Validate one ordered positive finite built-in-float sweep."""
        if not isinstance(values, tuple):
            raise TypeError(f"{name} must be a tuple")
        if not values:
            raise ValueError(f"{name} must be nonempty")
        if any(type(value) is not float for value in values):
            raise TypeError(f"{name} values must be built-in floats")
        if any(not np.isfinite(value) or value <= 0.0 for value in values):
            raise ValueError(f"{name} values must be positive and finite")
        expected = tuple(sorted(set(values), reverse=not increasing))
        if expected != values:
            direction = "increasing" if increasing else "decreasing"
            raise ValueError(f"{name} must be strictly {direction}")


@dataclass(frozen=True, slots=True)
class HarmonicOscillatorStudyResult:
    """Record all comparison results for one exact study definition.

    Parameters
    ----------
    definition
        Exact study definition.
    comparisons
        Ordered Cartesian product of box half-width, grid spacing, and retained
        dimension, with retained dimension varying fastest.

    Raises
    ------
    TypeError
        If the definition or comparison collection has the wrong type.
    ValueError
        If the comparison requests do not equal the declared ordered sweep.
    """

    definition: HarmonicOscillatorStudyDefinition
    comparisons: tuple[HarmonicOscillatorComparisonResult, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.definition, HarmonicOscillatorStudyDefinition):
            raise TypeError("definition must be HarmonicOscillatorStudyDefinition")
        if not isinstance(self.comparisons, tuple) or any(
            not isinstance(item, HarmonicOscillatorComparisonResult)
            for item in self.comparisons
        ):
            raise TypeError("comparisons must contain comparison results")
        expected = tuple(
            (box, spacing, retained)
            for box in self.definition.box_half_widths
            for spacing in self.definition.grid_spacings
            for retained in self.definition.retained_dimensions
        )
        observed = tuple(
            (
                result.request.box_half_width.magnitude,
                result.request.requested_grid_spacing.magnitude,
                result.request.retained_dimension,
            )
            for result in self.comparisons
        )
        if observed != expected:
            raise ValueError("comparisons must equal the declared ordered sweep")
        if any(
            result.request.parameters != self.definition.parameters
            for result in self.comparisons
        ):
            raise ValueError("comparison parameters must equal study parameters")
