"""Authenticated visualization projection for band-equivalence locality."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import SerializableValue
from ksdft2effmass.visualizations import BaseVisualizationData

from ..definitions import BandEquivalenceLocalityFamilyEnum


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityVisualizationData(BaseVisualizationData):
    """Retain the closed scalar projection used by the baseline figure."""

    family: BandEquivalenceLocalityFamilyEnum
    point_case_names: tuple[str, ...]
    parent_scales: tuple[float, ...]
    amplitudes: tuple[float, ...]
    minimum_operator_thresholds: tuple[float, ...]
    joint_operator_thresholds: tuple[float, ...]
    normalized_excess_nonzero_hopping_weights: tuple[float | None, ...]

    def __post_init__(self) -> None:
        if type(self.family) is not BandEquivalenceLocalityFamilyEnum:
            raise TypeError("family must be BandEquivalenceLocalityFamilyEnum")
        if type(self.point_case_names) is not tuple or not self.point_case_names:
            raise TypeError("point_case_names must be a nonempty tuple")
        if any(type(value) is not str or not value for value in self.point_case_names):
            raise TypeError("point_case_names must contain nonempty strings")
        length = len(self.point_case_names)
        required_lengths = (
            len(self.parent_scales),
            len(self.amplitudes),
            len(self.minimum_operator_thresholds),
            len(self.joint_operator_thresholds),
            len(self.normalized_excess_nonzero_hopping_weights),
        )
        if any(value != length for value in required_lengths):
            raise ValueError("visualization projection lengths must agree")
        for values, name in (
            (self.parent_scales, "parent_scales"),
            (self.amplitudes, "amplitudes"),
            (self.minimum_operator_thresholds, "minimum_operator_thresholds"),
            (self.joint_operator_thresholds, "joint_operator_thresholds"),
        ):
            if type(values) is not tuple or any(
                type(value) is not float or not math.isfinite(value) for value in values
            ):
                raise TypeError(f"{name} must contain finite built-in floats")
        optional_values = self.normalized_excess_nonzero_hopping_weights
        if type(optional_values) is not tuple or any(
            value is not None and (type(value) is not float or not math.isfinite(value))
            for value in optional_values
        ):
            raise TypeError(
                "normalized hopping weights must contain finite floats or None"
            )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "family": self.family.to_wire(),
            "point_case_names": self.point_case_names,
            "parent_scales": self.parent_scales,
            "amplitudes": self.amplitudes,
            "minimum_operator_thresholds": self.minimum_operator_thresholds,
            "joint_operator_thresholds": self.joint_operator_thresholds,
            "normalized_excess_nonzero_hopping_weights": (
                self.normalized_excess_nonzero_hopping_weights
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "family",
            "point_case_names",
            "parent_scales",
            "amplitudes",
            "minimum_operator_thresholds",
            "joint_operator_thresholds",
            "normalized_excess_nonzero_hopping_weights",
        }
        if set(values) != required:
            raise ValueError("band-equivalence visualization fields do not match")
        family = values["family"]
        names = values["point_case_names"]
        if type(family) is not str:
            raise TypeError("family must decode to a built-in string")
        if type(names) is not tuple or any(type(value) is not str for value in names):
            raise TypeError("point_case_names must decode to built-in strings")
        decoded_floats: dict[str, tuple[float, ...]] = {}
        for name in (
            "parent_scales",
            "amplitudes",
            "minimum_operator_thresholds",
            "joint_operator_thresholds",
        ):
            value = values[name]
            if type(value) is not tuple or any(
                type(item) is not float for item in value
            ):
                raise TypeError(f"{name} must decode to built-in floats")
            decoded_floats[name] = value
        optional = values["normalized_excess_nonzero_hopping_weights"]
        if type(optional) is not tuple or any(
            item is not None and type(item) is not float for item in optional
        ):
            raise TypeError("normalized hopping weights must decode to floats or None")
        return cls(
            family=BandEquivalenceLocalityFamilyEnum.from_wire(family),
            point_case_names=names,
            parent_scales=decoded_floats["parent_scales"],
            amplitudes=decoded_floats["amplitudes"],
            minimum_operator_thresholds=decoded_floats["minimum_operator_thresholds"],
            joint_operator_thresholds=decoded_floats["joint_operator_thresholds"],
            normalized_excess_nonzero_hopping_weights=optional,
        )


__all__ = ["BandEquivalenceLocalityVisualizationData"]
