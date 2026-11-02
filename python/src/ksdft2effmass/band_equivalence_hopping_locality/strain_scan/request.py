"""Typed request for a bounded synthetic-strain scan."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..strain import SyntheticStrainPathEnum


@dataclass(frozen=True, slots=True)
class SyntheticStrainScanRequest(BaseTypedRecord):
    """Define one finite synthetic-strain scan and its refinement controls."""

    path: SyntheticStrainPathEnum
    strain_fractions: tuple[float, ...]
    geometry_construction_size: int
    witness_construction_size: int
    response_construction_size: int
    response_evaluation_size: int
    response_evaluation_shift: float
    maximum_rotation_amplitude: float
    radial_decay_beta: float
    tail_tolerances: tuple[float, ...]
    maximum_transition_refinement_depth: int

    def __post_init__(self) -> None:
        if type(self.path) is not SyntheticStrainPathEnum:
            raise TypeError("path must be SyntheticStrainPathEnum")
        for name, value in (
            ("geometry_construction_size", self.geometry_construction_size),
            ("witness_construction_size", self.witness_construction_size),
            ("response_construction_size", self.response_construction_size),
        ):
            if type(value) is not int or value < 4 or value % 2:
                raise ValueError(
                    f"{name} must be an even built-in integer at least four"
                )
        if (
            type(self.response_evaluation_size) is not int
            or self.response_evaluation_size < 3
        ):
            raise ValueError(
                "response_evaluation_size must be a built-in integer at least three"
            )
        if (
            type(self.response_evaluation_shift) is not float
            or not 0.0 < self.response_evaluation_shift < 1.0
        ):
            raise ValueError(
                "response_evaluation_shift must be a built-in float in (0, 1)"
            )
        if (
            type(self.strain_fractions) is not tuple
            or not self.strain_fractions
            or self.strain_fractions != tuple(sorted(set(self.strain_fractions)))
            or any(
                type(value) is not float or not 0.0 <= value <= 1.0
                for value in self.strain_fractions
            )
        ):
            raise ValueError(
                "strain_fractions must be a nonempty, sorted, unique tuple of built-in "
                "floats in [0, 1]"
            )
        if (
            type(self.maximum_rotation_amplitude) is not float
            or not 0.0 <= self.maximum_rotation_amplitude <= math.pi / 4.0
        ):
            raise ValueError(
                "maximum_rotation_amplitude must be a built-in float in [0, pi/4]"
            )
        if type(self.radial_decay_beta) is not float or self.radial_decay_beta != 1.0:
            raise ValueError("radial_decay_beta must be the built-in float 1.0")
        if (
            type(self.tail_tolerances) is not tuple
            or not self.tail_tolerances
            or any(
                type(value) is not float or not math.isfinite(value) or value <= 0.0
                for value in self.tail_tolerances
            )
        ):
            raise ValueError(
                "tail_tolerances must be a nonempty tuple of positive built-in floats"
            )
        if (
            type(self.maximum_transition_refinement_depth) is not int
            or not 1 <= self.maximum_transition_refinement_depth <= 20
        ):
            raise ValueError(
                "maximum_transition_refinement_depth must be a built-in integer in "
                "[1, 20]"
            )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "path": self.path.to_wire(),
            "strain_fractions": self.strain_fractions,
            "geometry_construction_size": self.geometry_construction_size,
            "witness_construction_size": self.witness_construction_size,
            "response_construction_size": self.response_construction_size,
            "response_evaluation_size": self.response_evaluation_size,
            "response_evaluation_shift": self.response_evaluation_shift,
            "maximum_rotation_amplitude": self.maximum_rotation_amplitude,
            "radial_decay_beta": self.radial_decay_beta,
            "tail_tolerances": self.tail_tolerances,
            "maximum_transition_refinement_depth": (
                self.maximum_transition_refinement_depth
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "path",
            "strain_fractions",
            "geometry_construction_size",
            "witness_construction_size",
            "response_construction_size",
            "response_evaluation_size",
            "response_evaluation_shift",
            "maximum_rotation_amplitude",
            "radial_decay_beta",
            "tail_tolerances",
            "maximum_transition_refinement_depth",
        }
        if set(values) != required:
            raise ValueError("SyntheticStrainScanRequest fields do not match")
        path_wire = values["path"]
        strain_fractions = values["strain_fractions"]
        tail_tolerances = values["tail_tolerances"]
        geometry_construction_size = values["geometry_construction_size"]
        witness_construction_size = values["witness_construction_size"]
        response_construction_size = values["response_construction_size"]
        response_evaluation_size = values["response_evaluation_size"]
        maximum_transition_refinement_depth = values[
            "maximum_transition_refinement_depth"
        ]
        response_evaluation_shift = values["response_evaluation_shift"]
        maximum_rotation_amplitude = values["maximum_rotation_amplitude"]
        radial_decay_beta = values["radial_decay_beta"]
        if (
            type(response_evaluation_shift) is not float
            or type(maximum_rotation_amplitude) is not float
            or type(radial_decay_beta) is not float
        ):
            raise TypeError("float fields must use exact built-in types")
        if (
            type(geometry_construction_size) is not int
            or type(witness_construction_size) is not int
            or type(response_construction_size) is not int
            or type(response_evaluation_size) is not int
            or type(maximum_transition_refinement_depth) is not int
        ):
            raise TypeError("integer fields must use exact built-in types")
        if type(path_wire) is not str:
            raise TypeError("enum fields must decode to built-in strings")
        if not isinstance(strain_fractions, tuple):
            raise TypeError("strain_fractions must decode to a tuple")
        if not isinstance(tail_tolerances, tuple):
            raise TypeError("tail_tolerances must decode to a tuple")
        return cls(
            path=SyntheticStrainPathEnum.from_wire(path_wire),
            strain_fractions=strain_fractions,
            geometry_construction_size=geometry_construction_size,
            witness_construction_size=witness_construction_size,
            response_construction_size=response_construction_size,
            response_evaluation_size=response_evaluation_size,
            response_evaluation_shift=response_evaluation_shift,
            maximum_rotation_amplitude=maximum_rotation_amplitude,
            radial_decay_beta=radial_decay_beta,
            tail_tolerances=tail_tolerances,
            maximum_transition_refinement_depth=maximum_transition_refinement_depth,
        )
