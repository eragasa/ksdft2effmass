"""Parent-independent sampled fields for periodic-3D rank-N comparison analysis."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor

from .model import Periodic3DRankNAnalyticCase


def _immutable_float(value: Float64Array, name: str) -> Float64Array:
    return NumpyImmutableArrayConstructor(
        value,
        name,
        np.dtype(np.float64),
    ).execute()


def _immutable_complex(value: Complex128Array, name: str) -> Complex128Array:
    return NumpyImmutableArrayConstructor(
        value,
        name,
        np.dtype(np.complex128),
    ).execute()


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRankNBandEquivalenceFieldSamples:
    """Retain immutable fields on construction and evaluation sample inventories.

    The value contains represented scientific operands only.  It does not identify
    a block-hopping parent, a DFT provider, or the transformation that produced the
    comparison channel.
    """

    retained_rank: int
    operator_identifier: str
    energy_reference: str
    energy_unit: str
    basis_identifier: str
    construction_coordinates: Float64Array = field(repr=False)
    evaluation_coordinates: Float64Array = field(repr=False)
    reference_construction_frames: Complex128Array = field(repr=False)
    reference_evaluation_frames: Complex128Array = field(repr=False)
    comparison_construction_frames: Complex128Array = field(repr=False)
    comparison_evaluation_frames: Complex128Array = field(repr=False)
    reference_construction_operators: Complex128Array = field(repr=False)
    reference_evaluation_operators: Complex128Array = field(repr=False)
    comparison_construction_operators: Complex128Array = field(repr=False)
    comparison_evaluation_operators: Complex128Array = field(repr=False)
    comparison_inverse_construction_right_actions: Complex128Array | None = field(
        repr=False
    )
    comparison_inverse_evaluation_right_actions: Complex128Array | None = field(
        repr=False
    )

    def __post_init__(self) -> None:
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank < 2:
            raise ValueError("retained_rank must be at least two")
        for text_value, name in (
            (self.operator_identifier, "operator_identifier"),
            (self.energy_reference, "energy_reference"),
            (self.energy_unit, "energy_unit"),
            (self.basis_identifier, "basis_identifier"),
        ):
            if type(text_value) is not str:
                raise TypeError(f"{name} must be a built-in string")
            if not text_value:
                raise ValueError(f"{name} must be nonempty")

        construction = self._coordinates(
            self.construction_coordinates,
            "construction_coordinates",
        )
        evaluation = self._coordinates(
            self.evaluation_coordinates,
            "evaluation_coordinates",
        )
        object.__setattr__(self, "construction_coordinates", construction)
        object.__setattr__(self, "evaluation_coordinates", evaluation)

        construction_frame_shape = self._frame_shape(
            self.reference_construction_frames,
            construction,
            "reference_construction_frames",
        )
        evaluation_frame_shape = self._frame_shape(
            self.reference_evaluation_frames,
            evaluation,
            "reference_evaluation_frames",
        )
        for name, frame_value, coordinates, expected_shape in (
            (
                "comparison_construction_frames",
                self.comparison_construction_frames,
                construction,
                construction_frame_shape,
            ),
            (
                "comparison_evaluation_frames",
                self.comparison_evaluation_frames,
                evaluation,
                evaluation_frame_shape,
            ),
        ):
            admitted = _immutable_complex(frame_value, name)
            if admitted.shape != expected_shape:
                raise ValueError(f"{name} must match the reference frame shape")
            if admitted.shape[:-2] != coordinates.shape[:-1]:
                raise ValueError(f"{name} sample shape must match its coordinates")
            object.__setattr__(self, name, admitted)

        object.__setattr__(
            self,
            "reference_construction_frames",
            _immutable_complex(
                self.reference_construction_frames,
                "reference_construction_frames",
            ),
        )
        object.__setattr__(
            self,
            "reference_evaluation_frames",
            _immutable_complex(
                self.reference_evaluation_frames,
                "reference_evaluation_frames",
            ),
        )

        for name, operator_value, coordinates in (
            (
                "reference_construction_operators",
                self.reference_construction_operators,
                construction,
            ),
            (
                "reference_evaluation_operators",
                self.reference_evaluation_operators,
                evaluation,
            ),
            (
                "comparison_construction_operators",
                self.comparison_construction_operators,
                construction,
            ),
            (
                "comparison_evaluation_operators",
                self.comparison_evaluation_operators,
                evaluation,
            ),
        ):
            admitted = _immutable_complex(operator_value, name)
            expected_shape = (
                *coordinates.shape[:-1],
                self.retained_rank,
                self.retained_rank,
            )
            if admitted.shape != expected_shape:
                raise ValueError(f"{name} must match its coordinates and retained rank")
            object.__setattr__(self, name, admitted)

        construction_inverse = self.comparison_inverse_construction_right_actions
        evaluation_inverse = self.comparison_inverse_evaluation_right_actions
        if (construction_inverse is None) is not (evaluation_inverse is None):
            raise ValueError(
                "comparison inverse actions must be both present or absent"
            )
        for name, inverse_value, coordinates in (
            (
                "comparison_inverse_construction_right_actions",
                construction_inverse,
                construction,
            ),
            (
                "comparison_inverse_evaluation_right_actions",
                evaluation_inverse,
                evaluation,
            ),
        ):
            if inverse_value is None:
                continue
            admitted = _immutable_complex(inverse_value, name)
            expected_shape = (
                *coordinates.shape[:-1],
                self.retained_rank,
                self.retained_rank,
            )
            if admitted.shape != expected_shape:
                raise ValueError(f"{name} must match its coordinates and retained rank")
            object.__setattr__(self, name, admitted)

    @property
    def has_comparison_inverse_right_actions(self) -> bool:
        """Return whether both prescribed inverse-action fields are available."""
        return self.comparison_inverse_construction_right_actions is not None

    @staticmethod
    def _coordinates(value: Float64Array, name: str) -> Float64Array:
        coordinates = _immutable_float(value, name)
        if coordinates.ndim < 2 or coordinates.shape[-1] != 3:
            raise ValueError(f"{name} must have shape (..., 3)")
        if any(size <= 0 for size in coordinates.shape[:-1]):
            raise ValueError(f"{name} mesh axes must be nonempty")
        return coordinates

    def _frame_shape(
        self,
        value: Complex128Array,
        coordinates: Float64Array,
        name: str,
    ) -> tuple[int, ...]:
        admitted = _immutable_complex(value, name)
        if admitted.shape[:-2] != coordinates.shape[:-1]:
            raise ValueError(f"{name} sample shape must match its coordinates")
        if admitted.shape[-2] < self.retained_rank:
            raise ValueError(f"{name} ambient dimension must be at least retained rank")
        if admitted.shape[-1] != self.retained_rank:
            raise ValueError(f"{name} column count must match retained rank")
        return admitted.shape


class Periodic3DRankNAnalyticCaseFieldSampler:
    """Adapt one synthetic case to parent-independent sampled comparison fields."""

    __slots__ = ("_model",)

    def __init__(self, model: Periodic3DRankNAnalyticCase) -> None:
        if type(model) is not Periodic3DRankNAnalyticCase:
            raise TypeError("model must be the exact periodic-3D synthetic case")
        self._model = model

    @property
    def model(self) -> Periodic3DRankNAnalyticCase:
        """Return the analytic source bound to this adapter."""
        return self._model

    def execute(
        self,
        construction_coordinates: Float64Array,
        evaluation_coordinates: Float64Array,
    ) -> Periodic3DRankNBandEquivalenceFieldSamples:
        """Sample reference fields and apply the independently owned transformation."""
        model = self._model
        transformation = model.gauge_transformation
        reference_construction_frames = model.reference_frames(construction_coordinates)
        reference_evaluation_frames = model.reference_frames(evaluation_coordinates)
        reference_construction_operators = model.exact_reduced_hamiltonians(
            construction_coordinates
        )
        reference_evaluation_operators = model.exact_reduced_hamiltonians(
            evaluation_coordinates
        )
        return Periodic3DRankNBandEquivalenceFieldSamples(
            retained_rank=model.retained_rank,
            operator_identifier="retained-hamiltonian",
            energy_reference="dimensionless-zero-v1",
            energy_unit="dimensionless",
            basis_identifier=(
                f"{model.MODEL_FAMILY_IDENTITY}:retained-coordinate-basis"
            ),
            construction_coordinates=construction_coordinates,
            evaluation_coordinates=evaluation_coordinates,
            reference_construction_frames=reference_construction_frames,
            reference_evaluation_frames=reference_evaluation_frames,
            comparison_construction_frames=transformation.transform_frames(
                construction_coordinates,
                reference_construction_frames,
            ),
            comparison_evaluation_frames=transformation.transform_frames(
                evaluation_coordinates,
                reference_evaluation_frames,
            ),
            reference_construction_operators=reference_construction_operators,
            reference_evaluation_operators=reference_evaluation_operators,
            comparison_construction_operators=transformation.transform_operators(
                construction_coordinates,
                reference_construction_operators,
            ),
            comparison_evaluation_operators=transformation.transform_operators(
                evaluation_coordinates,
                reference_evaluation_operators,
            ),
            comparison_inverse_construction_right_actions=(
                transformation.inverse_right_actions(construction_coordinates)
            ),
            comparison_inverse_evaluation_right_actions=(
                transformation.inverse_right_actions(evaluation_coordinates)
            ),
        )


__all__ = [
    "Periodic3DRankNAnalyticCaseFieldSampler",
    "Periodic3DRankNBandEquivalenceFieldSamples",
]
