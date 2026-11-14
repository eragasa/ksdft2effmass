"""In-memory Wannier represented-field adaptation for periodic-3D analysis."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor

from ksdft2effmass.periodic3d.rankN.gauge_alignment.transformation import (
    Periodic3DRankNGivensGaugeTransformation,
)

from .represented_fields import Periodic3DRankNBandEquivalenceFieldSamples


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
class Periodic3DRankNWannierFieldSource:
    """Retain one in-memory Wannier frame and represented-operator source.

    The source owns arrays and representation metadata only. It makes no claim about
    file provenance, DFT convergence, Wannier90 convergence, subspace acceptance, or
    material validation.
    """

    retained_rank: int
    operator_identifier: str
    energy_reference: str
    energy_unit: str
    basis_identifier: str
    construction_coordinates: Float64Array = field(repr=False)
    evaluation_coordinates: Float64Array = field(repr=False)
    construction_frames: Complex128Array = field(repr=False)
    evaluation_frames: Complex128Array = field(repr=False)
    construction_operators: Complex128Array = field(repr=False)
    evaluation_operators: Complex128Array = field(repr=False)

    def __post_init__(self) -> None:
        """Validate metadata, shapes, finiteness, and operational immutability."""
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank < 2:
            raise ValueError("retained_rank must be at least two")
        for value, name in (
            (self.operator_identifier, "operator_identifier"),
            (self.energy_reference, "energy_reference"),
            (self.energy_unit, "energy_unit"),
            (self.basis_identifier, "basis_identifier"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in string")
            if not value:
                raise ValueError(f"{name} must be nonempty")

        construction = self._coordinates(
            self.construction_coordinates,
            "construction_coordinates",
        )
        evaluation = self._coordinates(
            self.evaluation_coordinates,
            "evaluation_coordinates",
        )
        construction_frames = self._frames(
            self.construction_frames,
            construction,
            "construction_frames",
        )
        evaluation_frames = self._frames(
            self.evaluation_frames,
            evaluation,
            "evaluation_frames",
        )
        if construction_frames.shape[-2] != evaluation_frames.shape[-2]:
            raise ValueError(
                "construction and evaluation ambient dimensions must agree"
            )
        construction_operators = self._operators(
            self.construction_operators,
            construction,
            "construction_operators",
        )
        evaluation_operators = self._operators(
            self.evaluation_operators,
            evaluation,
            "evaluation_operators",
        )
        object.__setattr__(self, "construction_coordinates", construction)
        object.__setattr__(self, "evaluation_coordinates", evaluation)
        object.__setattr__(self, "construction_frames", construction_frames)
        object.__setattr__(self, "evaluation_frames", evaluation_frames)
        object.__setattr__(self, "construction_operators", construction_operators)
        object.__setattr__(self, "evaluation_operators", evaluation_operators)

    @staticmethod
    def _coordinates(value: Float64Array, name: str) -> Float64Array:
        admitted = _immutable_float(value, name)
        if admitted.ndim < 2 or admitted.shape[-1] != 3:
            raise ValueError(f"{name} must have shape (..., 3)")
        if any(size <= 0 for size in admitted.shape[:-1]):
            raise ValueError(f"{name} mesh axes must be nonempty")
        return admitted

    def _frames(
        self,
        value: Complex128Array,
        coordinates: Float64Array,
        name: str,
    ) -> Complex128Array:
        admitted = _immutable_complex(value, name)
        if admitted.shape[:-2] != coordinates.shape[:-1]:
            raise ValueError(f"{name} sample shape must match its coordinates")
        if admitted.shape[-2] < self.retained_rank:
            raise ValueError(f"{name} ambient dimension must be at least retained rank")
        if admitted.shape[-1] != self.retained_rank:
            raise ValueError(f"{name} column count must match retained rank")
        return admitted

    def _operators(
        self,
        value: Complex128Array,
        coordinates: Float64Array,
        name: str,
    ) -> Complex128Array:
        admitted = _immutable_complex(value, name)
        expected_shape = (
            *coordinates.shape[:-1],
            self.retained_rank,
            self.retained_rank,
        )
        if admitted.shape != expected_shape:
            raise ValueError(f"{name} must match its coordinates and retained rank")
        return admitted


class Periodic3DRankNWannierFieldProducer:
    """Adapt admitted in-memory Wannier fields to the generic analysis boundary."""

    __slots__ = (
        "_transformation",
        "_frame_isometry_absolute_tolerance",
        "_operator_hermiticity_absolute_tolerance",
        "_source",
    )

    def __init__(
        self,
        *,
        source: Periodic3DRankNWannierFieldSource,
        transformation: Periodic3DRankNGivensGaugeTransformation | None,
        frame_isometry_absolute_tolerance: float,
        operator_hermiticity_absolute_tolerance: float,
    ) -> None:
        if type(source) is not Periodic3DRankNWannierFieldSource:
            raise TypeError("source must be the exact periodic-3D Wannier field source")
        if (
            transformation is not None
            and type(transformation) is not Periodic3DRankNGivensGaugeTransformation
        ):
            raise TypeError(
                "transformation must be the exact periodic-3D transformation or None"
            )
        if (
            transformation is not None
            and transformation.retained_rank != source.retained_rank
        ):
            raise ValueError(
                "transformation retained rank must match the Wannier source"
            )
        for value, name in (
            (frame_isometry_absolute_tolerance, "frame_isometry_absolute_tolerance"),
            (
                operator_hermiticity_absolute_tolerance,
                "operator_hermiticity_absolute_tolerance",
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        self._source = source
        self._transformation = transformation
        self._frame_isometry_absolute_tolerance = frame_isometry_absolute_tolerance
        self._operator_hermiticity_absolute_tolerance = (
            operator_hermiticity_absolute_tolerance
        )

    @staticmethod
    def _maximum_frame_isometry_defect(frames: Complex128Array) -> float:
        rank = frames.shape[-1]
        identity = np.eye(rank, dtype=np.complex128)
        defects = np.swapaxes(frames.conjugate(), -1, -2) @ frames - identity
        return float(np.max(np.linalg.norm(defects, axis=(-2, -1))))

    @staticmethod
    def _maximum_hermiticity_defect(operators: Complex128Array) -> float:
        defects = operators - np.swapaxes(operators.conjugate(), -1, -2)
        return float(np.max(np.linalg.norm(defects, axis=(-2, -1))))

    def execute(self) -> Periodic3DRankNBandEquivalenceFieldSamples:
        """Validate fields, apply an optional transformation, and freeze samples."""
        source = self._source
        for frames in (source.construction_frames, source.evaluation_frames):
            if self._maximum_frame_isometry_defect(frames) > (
                self._frame_isometry_absolute_tolerance
            ):
                raise ValueError("Wannier frames exceed the isometry tolerance")
        for operators in (
            source.construction_operators,
            source.evaluation_operators,
        ):
            if self._maximum_hermiticity_defect(operators) > (
                self._operator_hermiticity_absolute_tolerance
            ):
                raise ValueError(
                    "represented operators exceed the Hermiticity tolerance"
                )

        transformation = self._transformation
        if transformation is None:
            comparison_construction_frames = source.construction_frames
            comparison_evaluation_frames = source.evaluation_frames
            comparison_construction_operators = source.construction_operators
            comparison_evaluation_operators = source.evaluation_operators
            construction_inverse = None
            evaluation_inverse = None
        else:
            comparison_construction_frames = transformation.transform_frames(
                source.construction_coordinates,
                source.construction_frames,
            )
            comparison_evaluation_frames = transformation.transform_frames(
                source.evaluation_coordinates,
                source.evaluation_frames,
            )
            comparison_construction_operators = transformation.transform_operators(
                source.construction_coordinates,
                source.construction_operators,
            )
            comparison_evaluation_operators = transformation.transform_operators(
                source.evaluation_coordinates,
                source.evaluation_operators,
            )
            construction_inverse = transformation.inverse_right_actions(
                source.construction_coordinates
            )
            evaluation_inverse = transformation.inverse_right_actions(
                source.evaluation_coordinates
            )

        return Periodic3DRankNBandEquivalenceFieldSamples(
            retained_rank=source.retained_rank,
            operator_identifier=source.operator_identifier,
            energy_reference=source.energy_reference,
            energy_unit=source.energy_unit,
            basis_identifier=source.basis_identifier,
            construction_coordinates=source.construction_coordinates,
            evaluation_coordinates=source.evaluation_coordinates,
            reference_construction_frames=source.construction_frames,
            reference_evaluation_frames=source.evaluation_frames,
            comparison_construction_frames=comparison_construction_frames,
            comparison_evaluation_frames=comparison_evaluation_frames,
            reference_construction_operators=source.construction_operators,
            reference_evaluation_operators=source.evaluation_operators,
            comparison_construction_operators=comparison_construction_operators,
            comparison_evaluation_operators=comparison_evaluation_operators,
            comparison_inverse_construction_right_actions=construction_inverse,
            comparison_inverse_evaluation_right_actions=evaluation_inverse,
        )


__all__ = [
    "Periodic3DRankNWannierFieldProducer",
    "Periodic3DRankNWannierFieldSource",
]
