"""Authenticated QHO1D visualization projection."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.visualizations import BaseVisualizationData

from ..configuration import Qho1dConfiguration
from ..result import Qho1dCaseResult, Qho1dStateComparisonResult


@dataclass(frozen=True, slots=True, eq=False)
class Qho1dVisualizationData(BaseVisualizationData):
    """Retain the verifier-derived QHO1D rendering projection.

    Parameters
    ----------
    configuration
        Exact sweep and selected-state configuration.
    cases
        Ordered typed cases supplying diagnostic curves.
    selected_state_comparison
        State-resolved selected-case values.

    Raises
    ------
    TypeError
        A field has the wrong domain type.
    ValueError
        Cases do not equal the configured sweep or selected values disagree.
    """

    configuration: Qho1dConfiguration
    cases: tuple[Qho1dCaseResult, ...]
    selected_state_comparison: Qho1dStateComparisonResult

    def __post_init__(self) -> None:
        if not isinstance(self.configuration, Qho1dConfiguration):
            raise TypeError("configuration must be Qho1dConfiguration")
        if not isinstance(self.cases, tuple) or any(
            not isinstance(case, Qho1dCaseResult) for case in self.cases
        ):
            raise TypeError("cases must be a tuple of Qho1dCaseResult")
        expected = tuple(
            (box, spacing, retained)
            for box in self.configuration.box_half_widths
            for spacing in self.configuration.grid_spacings
            for retained in self.configuration.retained_dimensions
        )
        if tuple(case.key for case in self.cases) != expected:
            raise ValueError("visualization cases differ from the configured sweep")
        if not isinstance(self.selected_state_comparison, Qho1dStateComparisonResult):
            raise TypeError(
                "selected_state_comparison must be Qho1dStateComparisonResult"
            )
        selected = self.selected_state_comparison
        if (
            selected.box_half_width.magnitude
            != self.configuration.selected_box_half_width
            or selected.retained_dimension
            != self.configuration.selected_retained_dimension
            or selected.displayed_states != self.configuration.displayed_states
        ):
            raise ValueError("selected visualization data differs from configuration")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "configuration": self.configuration,
            "cases": self.cases,
            "selected_state_comparison": self.selected_state_comparison,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "configuration",
            "cases",
            "selected_state_comparison",
        }:
            raise ValueError("QHO1D visualization fields do not match")
        configuration_value = values["configuration"]
        cases_value = values["cases"]
        selected_value = values["selected_state_comparison"]
        if not isinstance(configuration_value, Mapping):
            raise TypeError("configuration must decode to a mapping")
        if not isinstance(cases_value, tuple) or any(
            not isinstance(case, Mapping) for case in cases_value
        ):
            raise TypeError("cases must decode to a tuple of mappings")
        if not isinstance(selected_value, Mapping):
            raise TypeError("selected_state_comparison must decode to a mapping")
        return cls(
            configuration=Qho1dConfiguration.from_dict(configuration_value),
            cases=tuple(Qho1dCaseResult.from_dict(case) for case in cases_value),
            selected_state_comparison=Qho1dStateComparisonResult.from_dict(
                selected_value
            ),
        )
