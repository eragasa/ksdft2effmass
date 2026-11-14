"""Periodic-1D Givens gauge transformations with explicit angle fields."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray

from ksdft2effmass.gauge_transformation import (
    FiniteRankGivensCircuit,
    FiniteRankGivensCircuitTransformationConstructor,
    SampledFiniteRankGaugeTransformation,
)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DFourierGivensGaugeTransformation:
    """Define a Givens circuit whose angles are explicit real Fourier series."""

    transformation_identifier: str
    circuit: FiniteRankGivensCircuit
    continuum_angle_maximum_bound: float
    constant_angles: RealArray = field(repr=False)
    cosine_coefficients: RealArray = field(repr=False)
    sine_coefficients: RealArray = field(repr=False)

    def __post_init__(self) -> None:
        if type(self.transformation_identifier) is not str:
            raise TypeError("transformation_identifier must be a string")
        if self.transformation_identifier == "":
            raise ValueError("transformation_identifier must be nonempty")
        if type(self.circuit) is not FiniteRankGivensCircuit:
            raise TypeError("circuit must be FiniteRankGivensCircuit")
        if type(self.continuum_angle_maximum_bound) is not float:
            raise TypeError("continuum_angle_maximum_bound must be a built-in float")
        if (
            not np.isfinite(self.continuum_angle_maximum_bound)
            or self.continuum_angle_maximum_bound < 0.0
        ):
            raise ValueError(
                "continuum_angle_maximum_bound must be finite and nonnegative"
            )
        constants = NumpyImmutableArrayConstructor(
            self.constant_angles,
            "constant_angles",
            np.dtype(np.float64),
        ).execute()
        cosine = NumpyImmutableArrayConstructor(
            self.cosine_coefficients,
            "cosine_coefficients",
            np.dtype(np.float64),
        ).execute()
        sine = NumpyImmutableArrayConstructor(
            self.sine_coefficients,
            "sine_coefficients",
            np.dtype(np.float64),
        ).execute()
        rotation_count = self.circuit.rotation_count
        if constants.shape != (rotation_count,):
            raise ValueError("constant_angles must have shape (rotation_count,)")
        if cosine.ndim != 2 or cosine.shape[0] != rotation_count:
            raise ValueError(
                "cosine_coefficients must have shape (rotation_count, harmonic_count)"
            )
        if sine.shape != cosine.shape:
            raise ValueError("sine_coefficients must match cosine_coefficients")
        if cosine.shape[1] == 0:
            raise ValueError("at least one positive Fourier harmonic is required")
        object.__setattr__(self, "constant_angles", constants)
        object.__setattr__(self, "cosine_coefficients", cosine)
        object.__setattr__(self, "sine_coefficients", sine)

    @property
    def retained_rank(self) -> int:
        """Return the finite represented rank."""
        return self.circuit.represented_rank

    @property
    def circuit_depth(self) -> int:
        """Return the number of ordered Givens layers."""
        return len(self.circuit.layers)

    @property
    def transformation_id(self) -> str:
        """Return the explicitly supplied transformation identity."""
        return self.transformation_identifier

    @property
    def exact_angle_maximum(self) -> float:
        """Return the supplied continuum maximum-angle bound."""
        return self.continuum_angle_maximum_bound

    def angle_samples(self, reduced_coordinates: RealArray) -> RealArray:
        """Evaluate every ordered rotation angle on supplied reduced coordinates."""
        coordinates = self._coordinates(reduced_coordinates)
        harmonics = np.arange(
            1,
            self.cosine_coefficients.shape[1] + 1,
            dtype=np.float64,
        )
        phase = 2.0 * np.pi * coordinates[:, None] * harmonics[None, :]
        values = (
            self.constant_angles[None, :]
            + np.cos(phase) @ self.cosine_coefficients.T
            + np.sin(phase) @ self.sine_coefficients.T
        )
        return NumpyImmutableArrayConstructor(
            np.asarray(values, dtype=np.float64),
            "givens_angle_samples",
            np.dtype(np.float64),
        ).execute()

    def sampled_angle_maximum(self, reduced_coordinates: RealArray) -> float:
        """Return the sampled maximum absolute rotation angle."""
        return float(np.max(np.abs(self.angle_samples(reduced_coordinates))))

    def sampled_transformation(
        self,
        reduced_coordinates: RealArray,
    ) -> SampledFiniteRankGaugeTransformation:
        """Return the generic sampled transformation on supplied coordinates."""
        return FiniteRankGivensCircuitTransformationConstructor(
            circuit=self.circuit,
            angle_samples=self.angle_samples(reduced_coordinates),
        ).execute()

    def unitaries(self, reduced_coordinates: RealArray) -> ComplexArray:
        """Return the sampled unitary matrix field."""
        return self.sampled_transformation(reduced_coordinates).unitaries

    def inverse_right_actions(self, reduced_coordinates: RealArray) -> ComplexArray:
        """Return the sampled inverse right-action field."""
        return self.sampled_transformation(reduced_coordinates).inverse_right_actions

    def transform_frames(
        self,
        reduced_coordinates: RealArray,
        frames: ComplexArray,
    ) -> ComplexArray:
        """Apply the sampled transformation from the right to frames."""
        return self.sampled_transformation(reduced_coordinates).transform_frames(frames)

    def transform_operators(
        self,
        reduced_coordinates: RealArray,
        operators: ComplexArray,
    ) -> ComplexArray:
        """Represent operators in the sampled transformed basis."""
        return self.sampled_transformation(reduced_coordinates).transform_operators(
            operators
        )

    @staticmethod
    def _coordinates(value: RealArray) -> RealArray:
        coordinates = NumpyImmutableArrayConstructor(
            value,
            "reduced_coordinates",
            np.dtype(np.float64),
        ).execute()
        if coordinates.ndim != 1 or coordinates.size == 0:
            raise ValueError("reduced_coordinates must be a nonempty vector")
        return coordinates


__all__ = ["Periodic1DFourierGivensGaugeTransformation"]
