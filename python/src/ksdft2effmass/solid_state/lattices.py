"""Dimension-specific direct, reciprocal, and verified lattice compositions.

These bases define reduced lattice-model translation coordinates; they are not atomic
``PeriodicStructure`` geometry, and no implicit conversion from that package is
provided. Direct and reciprocal bases are independently valid immutable DataObjects.
A composed ``Lattice1D``, ``Lattice2D``, or ``Lattice3D`` additionally requires
correlated passing duality and Bravais-metric results.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from ksdft2effmass.operators import MODEL_SYSTEM_UNIT_CONVERTER, PhysicalUnit

from .bravais import (
    BravaisLattice1D,
    BravaisLattice2D,
    BravaisLattice3D,
    BravaisMetricCompatibilityResult,
)

if TYPE_CHECKING:
    from .duality import LatticeDualityResult


type Vector1D = tuple[float]
type Vector2D = tuple[float, float]
type Vector3D = tuple[float, float, float]
type LatticeBasisVectors = (
    tuple[Vector1D] | tuple[Vector2D, Vector2D] | tuple[Vector3D, Vector3D, Vector3D]
)
type DirectLattice = DirectLattice1D | DirectLattice2D | DirectLattice3D
type ReciprocalLattice = ReciprocalLattice1D | ReciprocalLattice2D | ReciprocalLattice3D


class ReciprocalLatticeConvention(StrEnum):
    """Supported direct--reciprocal scale conventions."""

    TWO_PI_DUAL = "two_pi_dual"


@dataclass(frozen=True, slots=True)
class DirectLattice1D:
    """Represent one nonzero one-dimensional direct basis vector.

    Parameters
    ----------
    vector
        One finite built-in-float component in ``unit``.
    unit
        Pint-backed physical length unit.
    """

    vector: Vector1D
    unit: PhysicalUnit

    def __post_init__(self) -> None:
        """Validate exact shape, finiteness, length unit, and nonzero basis."""
        if type(self.vector) is not tuple or len(self.vector) != 1:
            raise TypeError("vector must be a one-component tuple")
        if any(type(value) is not float for value in self.vector):
            raise TypeError("vector components must be built-in floats")
        if any(not math.isfinite(value) for value in self.vector):
            raise ValueError("vector components must be finite")
        if self.vector[0] == 0.0:
            raise ValueError("direct basis vector must be nonzero")
        if type(self.unit) is not PhysicalUnit:
            raise TypeError("unit must be PhysicalUnit")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(self.unit, PhysicalUnit("meter")):
            raise ValueError("direct lattice unit must have length dimensionality")


@dataclass(frozen=True, slots=True)
class DirectLattice2D:
    """Represent two linearly independent two-dimensional direct basis vectors.

    Parameters
    ----------
    vectors
        Two finite built-in-float two-vectors in ``unit``.
    unit
        Pint-backed physical length unit.
    """

    vectors: tuple[Vector2D, Vector2D]
    unit: PhysicalUnit

    def __post_init__(self) -> None:
        """Validate exact finite 2D basis storage and length dimensionality."""
        if type(self.vectors) is not tuple or len(self.vectors) != 2:
            raise TypeError("vectors must contain two tuples")
        for vector in self.vectors:
            if type(vector) is not tuple or len(vector) != 2:
                raise TypeError("direct lattice vectors must be two-component tuples")
            if any(type(value) is not float for value in vector):
                raise TypeError("vector components must be built-in floats")
            if any(not math.isfinite(value) for value in vector):
                raise ValueError("vector components must be finite")
        if self.determinant == 0.0:
            raise ValueError("direct lattice vectors must be linearly independent")
        if type(self.unit) is not PhysicalUnit:
            raise TypeError("unit must be PhysicalUnit")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(self.unit, PhysicalUnit("meter")):
            raise ValueError("direct lattice unit must have length dimensionality")

    @property
    def determinant(self) -> float:
        """Return the signed 2D basis determinant in squared ``unit``."""
        return (
            self.vectors[0][0] * self.vectors[1][1]
            - self.vectors[0][1] * self.vectors[1][0]
        )


@dataclass(frozen=True, slots=True)
class DirectLattice3D:
    """Represent three linearly independent three-dimensional direct basis vectors.

    Parameters
    ----------
    vectors
        Three finite built-in-float three-vectors in ``unit``.
    unit
        Pint-backed physical length unit.
    """

    vectors: tuple[Vector3D, Vector3D, Vector3D]
    unit: PhysicalUnit

    def __post_init__(self) -> None:
        """Validate exact finite 3D basis storage and length dimensionality."""
        if type(self.vectors) is not tuple or len(self.vectors) != 3:
            raise TypeError("vectors must contain three tuples")
        for vector in self.vectors:
            if type(vector) is not tuple or len(vector) != 3:
                raise TypeError("direct lattice vectors must be three-component tuples")
            if any(type(value) is not float for value in vector):
                raise TypeError("vector components must be built-in floats")
            if any(not math.isfinite(value) for value in vector):
                raise ValueError("vector components must be finite")
        if self.determinant == 0.0:
            raise ValueError("direct lattice vectors must be linearly independent")
        if type(self.unit) is not PhysicalUnit:
            raise TypeError("unit must be PhysicalUnit")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(self.unit, PhysicalUnit("meter")):
            raise ValueError("direct lattice unit must have length dimensionality")

    @property
    def determinant(self) -> float:
        """Return the signed 3D basis determinant in cubed ``unit``."""
        a, b, c = self.vectors
        return (
            a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0])
        )


@dataclass(frozen=True, slots=True)
class ReciprocalLattice1D:
    """Represent one nonzero one-dimensional reciprocal basis vector.

    Parameters
    ----------
    vector
        One finite built-in-float component in ``unit``.
    unit
        Pint-backed physical inverse-length unit.
    convention
        Must be :attr:`ReciprocalLatticeConvention.TWO_PI_DUAL`.
    """

    vector: Vector1D
    unit: PhysicalUnit
    convention: ReciprocalLatticeConvention = ReciprocalLatticeConvention.TWO_PI_DUAL

    def __post_init__(self) -> None:
        """Validate exact shape, inverse-length unit, and convention."""
        if type(self.vector) is not tuple or len(self.vector) != 1:
            raise TypeError("vector must be a one-component tuple")
        if any(type(value) is not float for value in self.vector):
            raise TypeError("vector components must be built-in floats")
        if any(not math.isfinite(value) for value in self.vector):
            raise ValueError("vector components must be finite")
        if self.vector[0] == 0.0:
            raise ValueError("reciprocal basis vector must be nonzero")
        if type(self.unit) is not PhysicalUnit:
            raise TypeError("unit must be PhysicalUnit")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.unit, PhysicalUnit("1 / meter")
        ):
            raise ValueError(
                "reciprocal lattice unit must have inverse-length dimensionality"
            )
        if type(self.convention) is not ReciprocalLatticeConvention:
            raise TypeError("convention must be ReciprocalLatticeConvention")


@dataclass(frozen=True, slots=True)
class ReciprocalLattice2D:
    """Represent two linearly independent two-dimensional reciprocal basis vectors.

    Parameters
    ----------
    vectors
        Two finite built-in-float two-vectors in ``unit``.
    unit
        Pint-backed physical inverse-length unit.
    convention
        Must be :attr:`ReciprocalLatticeConvention.TWO_PI_DUAL`.
    """

    vectors: tuple[Vector2D, Vector2D]
    unit: PhysicalUnit
    convention: ReciprocalLatticeConvention = ReciprocalLatticeConvention.TWO_PI_DUAL

    def __post_init__(self) -> None:
        """Validate exact finite 2D reciprocal basis and convention."""
        if type(self.vectors) is not tuple or len(self.vectors) != 2:
            raise TypeError("vectors must contain two tuples")
        for vector in self.vectors:
            if type(vector) is not tuple or len(vector) != 2:
                raise TypeError("reciprocal vectors must be two-component tuples")
            if any(type(value) is not float for value in vector):
                raise TypeError("vector components must be built-in floats")
            if any(not math.isfinite(value) for value in vector):
                raise ValueError("vector components must be finite")
        if self.determinant == 0.0:
            raise ValueError("reciprocal vectors must be linearly independent")
        if type(self.unit) is not PhysicalUnit:
            raise TypeError("unit must be PhysicalUnit")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.unit, PhysicalUnit("1 / meter")
        ):
            raise ValueError(
                "reciprocal lattice unit must have inverse-length dimensionality"
            )
        if type(self.convention) is not ReciprocalLatticeConvention:
            raise TypeError("convention must be ReciprocalLatticeConvention")

    @property
    def determinant(self) -> float:
        """Return the signed 2D reciprocal-basis determinant."""
        return (
            self.vectors[0][0] * self.vectors[1][1]
            - self.vectors[0][1] * self.vectors[1][0]
        )


@dataclass(frozen=True, slots=True)
class ReciprocalLattice3D:
    """Represent three linearly independent three-dimensional reciprocal vectors.

    Parameters
    ----------
    vectors
        Three finite built-in-float three-vectors in ``unit``.
    unit
        Pint-backed physical inverse-length unit.
    convention
        Must be :attr:`ReciprocalLatticeConvention.TWO_PI_DUAL`.
    """

    vectors: tuple[Vector3D, Vector3D, Vector3D]
    unit: PhysicalUnit
    convention: ReciprocalLatticeConvention = ReciprocalLatticeConvention.TWO_PI_DUAL

    def __post_init__(self) -> None:
        """Validate exact finite 3D reciprocal basis and convention."""
        if type(self.vectors) is not tuple or len(self.vectors) != 3:
            raise TypeError("vectors must contain three tuples")
        for vector in self.vectors:
            if type(vector) is not tuple or len(vector) != 3:
                raise TypeError("reciprocal vectors must be three-component tuples")
            if any(type(value) is not float for value in vector):
                raise TypeError("vector components must be built-in floats")
            if any(not math.isfinite(value) for value in vector):
                raise ValueError("vector components must be finite")
        if self.determinant == 0.0:
            raise ValueError("reciprocal vectors must be linearly independent")
        if type(self.unit) is not PhysicalUnit:
            raise TypeError("unit must be PhysicalUnit")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.unit, PhysicalUnit("1 / meter")
        ):
            raise ValueError(
                "reciprocal lattice unit must have inverse-length dimensionality"
            )
        if type(self.convention) is not ReciprocalLatticeConvention:
            raise TypeError("convention must be ReciprocalLatticeConvention")

    @property
    def determinant(self) -> float:
        """Return the signed 3D reciprocal-basis determinant."""
        a, b, c = self.vectors
        return (
            a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0])
        )


@dataclass(frozen=True, slots=True)
class Lattice1D:
    """Compose verified 1D direct, reciprocal, and Bravais representations.

    Parameters
    ----------
    direct
        One-dimensional direct basis.
    reciprocal
        One-dimensional reciprocal basis.
    bravais
        Declared one-dimensional Bravais classification.
    duality
        Passing result correlated to ``direct`` and ``reciprocal``.
    metric
        Passing result correlated to ``direct`` and ``bravais``.
    """

    direct: DirectLattice1D
    reciprocal: ReciprocalLattice1D
    bravais: BravaisLattice1D
    duality: LatticeDualityResult
    metric: BravaisMetricCompatibilityResult

    def __post_init__(self) -> None:
        """Require exact component types and correlated passing analyses."""
        from .duality import LatticeDualityResult

        if type(self.direct) is not DirectLattice1D:
            raise TypeError("direct must be DirectLattice1D")
        if type(self.reciprocal) is not ReciprocalLattice1D:
            raise TypeError("reciprocal must be ReciprocalLattice1D")
        if type(self.bravais) is not BravaisLattice1D:
            raise TypeError("bravais must be BravaisLattice1D")
        if type(self.duality) is not LatticeDualityResult:
            raise TypeError("duality must be LatticeDualityResult")
        if type(self.metric) is not BravaisMetricCompatibilityResult:
            raise TypeError("metric must be BravaisMetricCompatibilityResult")
        self._validate_results()

    def _validate_results(self) -> None:
        """Validate correlation and passing status for owned analysis results."""
        if (
            self.duality.direct != self.direct
            or self.duality.reciprocal != self.reciprocal
            or not self.duality.compatible
        ):
            raise ValueError("duality must be passing and correlated to lattice bases")
        if (
            self.metric.direct != self.direct
            or self.metric.bravais != self.bravais
            or not self.metric.compatible
        ):
            raise ValueError("metric must be passing and correlated to Bravais data")


@dataclass(frozen=True, slots=True)
class Lattice2D:
    """Compose verified 2D direct, reciprocal, and Bravais representations."""

    direct: DirectLattice2D
    reciprocal: ReciprocalLattice2D
    bravais: BravaisLattice2D
    duality: LatticeDualityResult
    metric: BravaisMetricCompatibilityResult

    def __post_init__(self) -> None:
        """Require exact component types and correlated passing analyses."""
        from .duality import LatticeDualityResult

        if type(self.direct) is not DirectLattice2D:
            raise TypeError("direct must be DirectLattice2D")
        if type(self.reciprocal) is not ReciprocalLattice2D:
            raise TypeError("reciprocal must be ReciprocalLattice2D")
        if type(self.bravais) is not BravaisLattice2D:
            raise TypeError("bravais must be BravaisLattice2D")
        if type(self.duality) is not LatticeDualityResult:
            raise TypeError("duality must be LatticeDualityResult")
        if type(self.metric) is not BravaisMetricCompatibilityResult:
            raise TypeError("metric must be BravaisMetricCompatibilityResult")
        if (
            self.duality.direct != self.direct
            or self.duality.reciprocal != self.reciprocal
            or not self.duality.compatible
        ):
            raise ValueError("duality must be passing and correlated to lattice bases")
        if (
            self.metric.direct != self.direct
            or self.metric.bravais != self.bravais
            or not self.metric.compatible
        ):
            raise ValueError("metric must be passing and correlated to Bravais data")


@dataclass(frozen=True, slots=True)
class Lattice3D:
    """Compose verified 3D direct, reciprocal, and Bravais representations."""

    direct: DirectLattice3D
    reciprocal: ReciprocalLattice3D
    bravais: BravaisLattice3D
    duality: LatticeDualityResult
    metric: BravaisMetricCompatibilityResult

    def __post_init__(self) -> None:
        """Require exact component types and correlated passing analyses."""
        from .duality import LatticeDualityResult

        if type(self.direct) is not DirectLattice3D:
            raise TypeError("direct must be DirectLattice3D")
        if type(self.reciprocal) is not ReciprocalLattice3D:
            raise TypeError("reciprocal must be ReciprocalLattice3D")
        if type(self.bravais) is not BravaisLattice3D:
            raise TypeError("bravais must be BravaisLattice3D")
        if type(self.duality) is not LatticeDualityResult:
            raise TypeError("duality must be LatticeDualityResult")
        if type(self.metric) is not BravaisMetricCompatibilityResult:
            raise TypeError("metric must be BravaisMetricCompatibilityResult")
        if (
            self.duality.direct != self.direct
            or self.duality.reciprocal != self.reciprocal
            or not self.duality.compatible
        ):
            raise ValueError("duality must be passing and correlated to lattice bases")
        if (
            self.metric.direct != self.direct
            or self.metric.bravais != self.bravais
            or not self.metric.compatible
        ):
            raise ValueError("metric must be passing and correlated to Bravais data")
