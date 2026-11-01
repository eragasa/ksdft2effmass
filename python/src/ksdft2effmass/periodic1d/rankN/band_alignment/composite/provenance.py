"""Immutable evaluation and selection provenance for higher-rank alignment."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ._record_admission import _decoded_bool, _decoded_int
from .configuration import Periodic1DRankNAlignmentConfiguration


@dataclass(frozen=True, slots=True)
class Periodic1DRankNEvaluationIndependenceResult(BaseTypedRecord):
    """Retain exact mesh separation and selection-input provenance."""

    construction_mesh_sizes: tuple[int, ...]
    evaluation_mesh_size: int
    evaluation_shift_numerator: int
    evaluation_shift_denominator: int
    global_selection_mesh_size: int
    pointwise_selection_mesh_sizes: tuple[int, ...]
    construction_evaluation_disjoint: bool
    evaluation_mesh_excluded_from_selection: bool

    def __post_init__(self) -> None:
        configuration = Periodic1DRankNAlignmentConfiguration
        if self.construction_mesh_sizes != configuration.CONSTRUCTION_MESH_SIZES:
            raise ValueError("construction mesh provenance must match the protocol")
        if self.evaluation_mesh_size != configuration.EVALUATION_MESH_SIZE:
            raise ValueError("evaluation mesh provenance must match the protocol")
        if (
            self.evaluation_shift_numerator != configuration.EVALUATION_SHIFT_NUMERATOR
            or self.evaluation_shift_denominator
            != configuration.EVALUATION_SHIFT_DENOMINATOR
        ):
            raise ValueError("evaluation shift provenance must match the protocol")
        if (
            self.global_selection_mesh_size
            != configuration.GLOBAL_UNITARY_SELECTION_MESH_SIZE
        ):
            raise ValueError("global selection provenance must match the protocol")
        if self.pointwise_selection_mesh_sizes != self.construction_mesh_sizes:
            raise ValueError("pointwise selection must use every construction mesh")
        if type(self.construction_evaluation_disjoint) is not bool:
            raise TypeError("construction_evaluation_disjoint must be a built-in bool")
        evaluation_coordinates = {
            Fraction(
                index * self.evaluation_shift_denominator
                + self.evaluation_shift_numerator,
                self.evaluation_mesh_size * self.evaluation_shift_denominator,
            )
            for index in range(self.evaluation_mesh_size)
        }
        expected_disjointness = all(
            evaluation_coordinates.isdisjoint(
                Fraction(index, mesh_size) for index in range(mesh_size)
            )
            for mesh_size in self.construction_mesh_sizes
        )
        if self.construction_evaluation_disjoint is not expected_disjointness:
            raise ValueError(
                "construction/evaluation disjointness provenance is inconsistent"
            )
        if not expected_disjointness:
            raise ValueError("construction and evaluation coordinates must be disjoint")
        if type(self.evaluation_mesh_excluded_from_selection) is not bool:
            raise TypeError(
                "evaluation_mesh_excluded_from_selection must be a built-in bool"
            )
        expected_exclusion = (
            self.evaluation_mesh_size != self.global_selection_mesh_size
            and self.evaluation_mesh_size not in self.pointwise_selection_mesh_sizes
        )
        if self.evaluation_mesh_excluded_from_selection is not expected_exclusion:
            raise ValueError("selection-input mesh provenance is inconsistent")
        if self.evaluation_mesh_excluded_from_selection is not True:
            raise ValueError("evaluation mesh must not be a selection input")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "construction_mesh_sizes": self.construction_mesh_sizes,
            "evaluation_mesh_size": self.evaluation_mesh_size,
            "evaluation_shift_numerator": self.evaluation_shift_numerator,
            "evaluation_shift_denominator": self.evaluation_shift_denominator,
            "global_selection_mesh_size": self.global_selection_mesh_size,
            "pointwise_selection_mesh_sizes": self.pointwise_selection_mesh_sizes,
            "construction_evaluation_disjoint": (self.construction_evaluation_disjoint),
            "evaluation_mesh_excluded_from_selection": (
                self.evaluation_mesh_excluded_from_selection
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "construction_mesh_sizes",
            "evaluation_mesh_size",
            "evaluation_shift_numerator",
            "evaluation_shift_denominator",
            "global_selection_mesh_size",
            "pointwise_selection_mesh_sizes",
            "construction_evaluation_disjoint",
            "evaluation_mesh_excluded_from_selection",
        }:
            raise ValueError("evaluation-independence fields do not match")
        construction_sizes = values["construction_mesh_sizes"]
        pointwise_sizes = values["pointwise_selection_mesh_sizes"]
        if not isinstance(construction_sizes, tuple) or any(
            type(value) is not int for value in construction_sizes
        ):
            raise TypeError("construction mesh sizes must decode to integers")
        if not isinstance(pointwise_sizes, tuple) or any(
            type(value) is not int for value in pointwise_sizes
        ):
            raise TypeError("pointwise selection mesh sizes must decode to integers")
        return cls(
            construction_mesh_sizes=construction_sizes,
            evaluation_mesh_size=_decoded_int(
                values["evaluation_mesh_size"], "evaluation_mesh_size"
            ),
            evaluation_shift_numerator=_decoded_int(
                values["evaluation_shift_numerator"],
                "evaluation_shift_numerator",
            ),
            evaluation_shift_denominator=_decoded_int(
                values["evaluation_shift_denominator"],
                "evaluation_shift_denominator",
            ),
            global_selection_mesh_size=_decoded_int(
                values["global_selection_mesh_size"],
                "global_selection_mesh_size",
            ),
            pointwise_selection_mesh_sizes=pointwise_sizes,
            construction_evaluation_disjoint=_decoded_bool(
                values["construction_evaluation_disjoint"],
                "construction_evaluation_disjoint",
            ),
            evaluation_mesh_excluded_from_selection=_decoded_bool(
                values["evaluation_mesh_excluded_from_selection"],
                "evaluation_mesh_excluded_from_selection",
            ),
        )
