"""Immutable reciprocal-space sampling for electronic-structure calculations.

K-point sampling is an electronic-structure discretization, not intrinsic crystal
structure state. This module retains the existing Cartesian ``2*pi/alat``
representation, explicit weights, and normalization semantics without selecting or
claiming a converged Brillouin-zone mesh.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

from ksdft2effmass.structures.periodic import (
    CoordinateConvention,
    InverseLengthUnit,
    LengthUnit,
    PhysicalDimension,
    ReciprocalScaleConvention,
    Vector3Sequence,
)


class KPointWeightNormalization(StrEnum):
    """Normalization state of represented k-point weights."""

    SUM_TO_TWO = "sum_to_two"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class KPointSampling:
    """Ordered Cartesian k points with explicit reciprocal scale and weights.

    Parameters
    ----------
    raw_coordinates
        Nonempty ordered dimensionless Cartesian built-in-float three-vectors.
    raw_dimension
        Must be
        :attr:`~ksdft2effmass.structures.periodic.PhysicalDimension.DIMENSIONLESS`.
    coordinate_convention
        Must be
        :attr:`~ksdft2effmass.structures.periodic.CoordinateConvention.CARTESIAN`.
    scale_convention
        Must be
        :attr:`~ksdft2effmass.structures.periodic.ReciprocalScaleConvention.TWO_PI_OVER_ALAT`.
    scale_alat
        Positive finite built-in float in bohr.
    scale_alat_unit
        Must be :attr:`~ksdft2effmass.structures.periodic.LengthUnit.BOHR`.
    incorporates_two_pi
        Must be the built-in Boolean ``True``.
    physical_coordinates
        Nonempty equally sized coordinates scaled exactly into bohr^-1.
    physical_dimension
        Must be
        :attr:`~ksdft2effmass.structures.periodic.PhysicalDimension.INVERSE_LENGTH`.
    physical_unit
        Must be
        :attr:`~ksdft2effmass.structures.periodic.InverseLengthUnit.PER_BOHR`.
    weights
        Finite nonnegative built-in floats, one per coordinate.
    weight_normalization
        Exact represented normalization state.

    Notes
    -----
    Construction verifies represented scaling and weight state only. It does not
    establish Brillouin-zone integration convergence or scientific adequacy.
    """

    raw_coordinates: Vector3Sequence
    raw_dimension: PhysicalDimension
    coordinate_convention: CoordinateConvention
    scale_convention: ReciprocalScaleConvention
    scale_alat: float
    scale_alat_unit: LengthUnit
    incorporates_two_pi: bool
    physical_coordinates: Vector3Sequence
    physical_dimension: PhysicalDimension
    physical_unit: InverseLengthUnit
    weights: tuple[float, ...]
    weight_normalization: KPointWeightNormalization

    def __post_init__(self) -> None:
        """Validate exact sampling representation, scale, and weights."""
        self._validate_vectors(self.raw_coordinates, "raw k-point coordinates")
        self._validate_vectors(
            self.physical_coordinates, "physical k-point coordinates"
        )
        if type(self.raw_dimension) is not PhysicalDimension:
            raise TypeError("raw_dimension must be PhysicalDimension")
        if type(self.coordinate_convention) is not CoordinateConvention:
            raise TypeError("coordinate_convention must be CoordinateConvention")
        if type(self.scale_convention) is not ReciprocalScaleConvention:
            raise TypeError("scale_convention must be ReciprocalScaleConvention")
        if type(self.scale_alat) is not float:
            raise TypeError("k-point scale_alat must be a built-in float")
        if type(self.scale_alat_unit) is not LengthUnit:
            raise TypeError("scale_alat_unit must be LengthUnit")
        if type(self.incorporates_two_pi) is not bool:
            raise TypeError("incorporates_two_pi must be bool")
        if type(self.physical_dimension) is not PhysicalDimension:
            raise TypeError("physical_dimension must be PhysicalDimension")
        if type(self.physical_unit) is not InverseLengthUnit:
            raise TypeError("physical_unit must be InverseLengthUnit")
        if type(self.weight_normalization) is not KPointWeightNormalization:
            raise TypeError("weight_normalization must be KPointWeightNormalization")
        if len(self.raw_coordinates) != len(self.physical_coordinates):
            raise ValueError("raw and physical k-point counts must agree")
        if not self.raw_coordinates:
            raise ValueError("k-point coordinates must be nonempty")
        if self.raw_dimension is not PhysicalDimension.DIMENSIONLESS:
            raise ValueError("raw k-point coordinates must be dimensionless")
        if self.coordinate_convention is not CoordinateConvention.CARTESIAN:
            raise ValueError("k-point coordinates must be Cartesian")
        if self.scale_convention is not ReciprocalScaleConvention.TWO_PI_OVER_ALAT:
            raise ValueError("unsupported k-point reciprocal scale")
        if not math.isfinite(self.scale_alat) or self.scale_alat <= 0:
            raise ValueError("k-point scale_alat must be positive and finite")
        if self.scale_alat_unit is not LengthUnit.BOHR:
            raise ValueError("k-point scale_alat unit must be bohr")
        if self.incorporates_two_pi is not True:
            raise ValueError("k-point scale must explicitly incorporate two pi")
        if self.physical_dimension is not PhysicalDimension.INVERSE_LENGTH:
            raise ValueError("physical k-point dimension must be inverse length")
        if self.physical_unit is not InverseLengthUnit.PER_BOHR:
            raise ValueError("physical k-point unit must be bohr^-1")
        scale = 2.0 * math.pi / self.scale_alat
        for raw, physical in zip(
            self.raw_coordinates, self.physical_coordinates, strict=True
        ):
            if physical != tuple(value * scale for value in raw):
                raise ValueError("physical k points disagree with reciprocal scale")
        if type(self.weights) is not tuple:
            raise TypeError("k-point weights must be a tuple")
        if len(self.weights) != len(self.raw_coordinates):
            raise ValueError("k-point weight count must match coordinate count")
        if any(type(value) is not float for value in self.weights):
            raise TypeError("k-point weights must be built-in floats")
        if any(not math.isfinite(value) or value < 0 for value in self.weights):
            raise ValueError("k-point weights must be finite and nonnegative")
        if self.weight_normalization is KPointWeightNormalization.SUM_TO_TWO:
            if math.fsum(self.weights) != 2.0:
                raise ValueError("sum_to_two k-point weights must sum exactly to 2.0")
        elif self.weight_normalization is not KPointWeightNormalization.UNAVAILABLE:
            raise ValueError("unsupported k-point weight normalization")

    @staticmethod
    def _validate_vectors(vectors: Vector3Sequence, name: str) -> None:
        """Validate one exact immutable sequence of finite three-vectors."""
        if type(vectors) is not tuple:
            raise TypeError(f"{name} must be a tuple")
        for vector in vectors:
            if type(vector) is not tuple:
                raise TypeError(f"{name} must contain tuples")
            if len(vector) != 3:
                raise ValueError(f"{name} vectors must contain three components")
            for component in vector:
                if type(component) is not float:
                    raise TypeError(f"{name} components must be built-in floats")
                if not math.isfinite(component):
                    raise ValueError(f"{name} components must be finite")
