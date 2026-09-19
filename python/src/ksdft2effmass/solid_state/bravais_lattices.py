"""Direct, reciprocal, and Bravais lattice records in one to three dimensions.

Bravais classification is factored into lattice system and conventional-cell
centering. These bases define reduced lattice-model translation coordinates; they are
not atomic ``PeriodicStructure`` geometry, and no implicit conversion from that package
is provided. Direct and reciprocal bases are independently valid immutable DataObjects;
tolerance-dependent duality belongs to :class:`LatticeDualityAnalyzer`. Construction of
a composed ``Lattice1D``, ``Lattice2D``, or ``Lattice3D`` therefore records a declared
pair and classification but does not itself prove duality or metric classification.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    PhysicalUnit,
)

type Vector1D = tuple[float]
type Vector2D = tuple[float, float]
type Vector3D = tuple[float, float, float]
type LatticeBasisVectors = (
    tuple[Vector1D] | tuple[Vector2D, Vector2D] | tuple[Vector3D, Vector3D, Vector3D]
)
type DirectLattice = DirectLattice1D | DirectLattice2D | DirectLattice3D
type ReciprocalLattice = ReciprocalLattice1D | ReciprocalLattice2D | ReciprocalLattice3D


class BravaisCentering(StrEnum):
    """Conventional-cell centering used by supported Bravais classifications.

    ``P`` is primitive, ``C`` is the canonical base-centered setting, ``I`` is
    body-centered, ``F`` is face-centered, and ``R`` is rhombohedral centering.
    Axis-specific ``A`` or ``B`` settings must be transformed to the declared
    canonical ``C`` setting before construction.
    """

    P = "P"
    C = "C"
    I = "I"  # noqa: E741 - conventional body-centering symbol
    F = "F"
    R = "R"


class LatticeSystem1D(StrEnum):
    """One-dimensional lattice systems."""

    LINE = "line"


class LatticeSystem2D(StrEnum):
    """Two-dimensional lattice systems before centering is applied."""

    OBLIQUE = "oblique"
    RECTANGULAR = "rectangular"
    SQUARE = "square"
    HEXAGONAL = "hexagonal"


class LatticeSystem3D(StrEnum):
    """Three-dimensional lattice systems before centering is applied."""

    TRICLINIC = "triclinic"
    MONOCLINIC = "monoclinic"
    ORTHORHOMBIC = "orthorhombic"
    TETRAGONAL = "tetragonal"
    RHOMBOHEDRAL = "rhombohedral"
    HEXAGONAL = "hexagonal"
    CUBIC = "cubic"


@dataclass(frozen=True, slots=True)
class BravaisLattice1D:
    """Represent the unique one-dimensional Bravais classification.

    Parameters
    ----------
    system
        Must be :attr:`LatticeSystem1D.LINE`.
    centering
        Must be :attr:`BravaisCentering.P`.
    """

    system: LatticeSystem1D
    centering: BravaisCentering

    def __post_init__(self) -> None:
        """Validate the unique 1D system-centering combination."""
        if type(self.system) is not LatticeSystem1D:
            raise TypeError("system must be LatticeSystem1D")
        if type(self.centering) is not BravaisCentering:
            raise TypeError("centering must be BravaisCentering")
        if (
            self.system is not LatticeSystem1D.LINE
            or self.centering is not BravaisCentering.P
        ):
            raise ValueError("one-dimensional Bravais lattice must be line P")


@dataclass(frozen=True, slots=True)
class BravaisLattice2D:
    """Represent one of the five two-dimensional Bravais classifications.

    The valid combinations are oblique P, rectangular P/C, square P, and hexagonal
    P. Rectangular C is the centered-rectangular Bravais lattice.

    Parameters
    ----------
    system
        Declared two-dimensional lattice system.
    centering
        Conventional-cell centering valid for ``system``.
    """

    system: LatticeSystem2D
    centering: BravaisCentering

    def __post_init__(self) -> None:
        """Validate the selected 2D system-centering combination."""
        if type(self.system) is not LatticeSystem2D:
            raise TypeError("system must be LatticeSystem2D")
        if type(self.centering) is not BravaisCentering:
            raise TypeError("centering must be BravaisCentering")
        allowed = {
            LatticeSystem2D.OBLIQUE: (BravaisCentering.P,),
            LatticeSystem2D.RECTANGULAR: (
                BravaisCentering.P,
                BravaisCentering.C,
            ),
            LatticeSystem2D.SQUARE: (BravaisCentering.P,),
            LatticeSystem2D.HEXAGONAL: (BravaisCentering.P,),
        }
        if self.centering not in allowed[self.system]:
            raise ValueError("unsupported two-dimensional system-centering combination")


@dataclass(frozen=True, slots=True)
class BravaisLattice3D:
    """Represent one of the fourteen three-dimensional Bravais classifications.

    The valid combinations are triclinic P; monoclinic P/C; orthorhombic P/C/I/F;
    tetragonal P/I; rhombohedral R; hexagonal P; and cubic P/I/F.

    Parameters
    ----------
    system
        Declared three-dimensional lattice system.
    centering
        Conventional-cell centering valid for ``system``.
    """

    system: LatticeSystem3D
    centering: BravaisCentering

    def __post_init__(self) -> None:
        """Validate the selected 3D system-centering combination."""
        if type(self.system) is not LatticeSystem3D:
            raise TypeError("system must be LatticeSystem3D")
        if type(self.centering) is not BravaisCentering:
            raise TypeError("centering must be BravaisCentering")
        allowed = {
            LatticeSystem3D.TRICLINIC: (BravaisCentering.P,),
            LatticeSystem3D.MONOCLINIC: (
                BravaisCentering.P,
                BravaisCentering.C,
            ),
            LatticeSystem3D.ORTHORHOMBIC: (
                BravaisCentering.P,
                BravaisCentering.C,
                BravaisCentering.I,
                BravaisCentering.F,
            ),
            LatticeSystem3D.TETRAGONAL: (
                BravaisCentering.P,
                BravaisCentering.I,
            ),
            LatticeSystem3D.RHOMBOHEDRAL: (BravaisCentering.R,),
            LatticeSystem3D.HEXAGONAL: (BravaisCentering.P,),
            LatticeSystem3D.CUBIC: (
                BravaisCentering.P,
                BravaisCentering.I,
                BravaisCentering.F,
            ),
        }
        if self.centering not in allowed[self.system]:
            raise ValueError(
                "unsupported three-dimensional system-centering combination"
            )


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
    """Compose declared 1D direct, reciprocal, and Bravais representations.

    Parameters
    ----------
    direct
        One-dimensional direct basis.
    reciprocal
        One-dimensional reciprocal basis. Construction does not prove duality.
    bravais
        Declared one-dimensional Bravais classification.
    """

    direct: DirectLattice1D
    reciprocal: ReciprocalLattice1D
    bravais: BravaisLattice1D

    def __post_init__(self) -> None:
        """Validate exact component types without claiming duality."""
        if type(self.direct) is not DirectLattice1D:
            raise TypeError("direct must be DirectLattice1D")
        if type(self.reciprocal) is not ReciprocalLattice1D:
            raise TypeError("reciprocal must be ReciprocalLattice1D")
        if type(self.bravais) is not BravaisLattice1D:
            raise TypeError("bravais must be BravaisLattice1D")


@dataclass(frozen=True, slots=True)
class Lattice2D:
    """Compose declared 2D direct, reciprocal, and Bravais representations.

    Parameters
    ----------
    direct
        Two-dimensional direct basis.
    reciprocal
        Two-dimensional reciprocal basis. Construction does not prove duality.
    bravais
        Declared two-dimensional Bravais classification.
    """

    direct: DirectLattice2D
    reciprocal: ReciprocalLattice2D
    bravais: BravaisLattice2D

    def __post_init__(self) -> None:
        """Validate exact component types without claiming duality."""
        if type(self.direct) is not DirectLattice2D:
            raise TypeError("direct must be DirectLattice2D")
        if type(self.reciprocal) is not ReciprocalLattice2D:
            raise TypeError("reciprocal must be ReciprocalLattice2D")
        if type(self.bravais) is not BravaisLattice2D:
            raise TypeError("bravais must be BravaisLattice2D")


@dataclass(frozen=True, slots=True)
class Lattice3D:
    """Compose declared 3D direct, reciprocal, and Bravais representations.

    Parameters
    ----------
    direct
        Three-dimensional direct basis.
    reciprocal
        Three-dimensional reciprocal basis. Construction does not prove duality.
    bravais
        Declared three-dimensional Bravais classification.
    """

    direct: DirectLattice3D
    reciprocal: ReciprocalLattice3D
    bravais: BravaisLattice3D

    def __post_init__(self) -> None:
        """Validate exact component types without claiming duality."""
        if type(self.direct) is not DirectLattice3D:
            raise TypeError("direct must be DirectLattice3D")
        if type(self.reciprocal) is not ReciprocalLattice3D:
            raise TypeError("reciprocal must be ReciprocalLattice3D")
        if type(self.bravais) is not BravaisLattice3D:
            raise TypeError("bravais must be BravaisLattice3D")


@dataclass(frozen=True, slots=True)
class LatticeDualityResult:
    """Record direct--reciprocal duality analysis.

    Parameters
    ----------
    compatible
        True exactly when no issue code is retained.
    maximum_absolute_residual
        Maximum absolute component of ``A B^T - 2*pi*I`` after reciprocal-unit
        conversion, or ``None`` when dimensions or units prevent evaluation.
    issue_codes
        Sorted unique deterministic issue codes.
    """

    compatible: bool
    maximum_absolute_residual: float | None
    issue_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate status, optional residual, and issue ordering."""
        if type(self.compatible) is not bool:
            raise TypeError("compatible must be bool")
        if self.maximum_absolute_residual is not None:
            if type(self.maximum_absolute_residual) is not float:
                raise TypeError("maximum_absolute_residual must be float or None")
            if not math.isfinite(self.maximum_absolute_residual):
                raise ValueError("maximum_absolute_residual must be finite")
            if self.maximum_absolute_residual < 0.0:
                raise ValueError("maximum_absolute_residual must be nonnegative")
        if type(self.issue_codes) is not tuple or any(
            type(code) is not str for code in self.issue_codes
        ):
            raise TypeError("issue_codes must be a tuple of strings")
        if self.issue_codes != tuple(sorted(set(self.issue_codes))):
            raise ValueError("issue_codes must be sorted and unique")
        if self.compatible == bool(self.issue_codes):
            raise ValueError("compatible status must agree with issue_codes")


class LatticeDualityAnalyzer:
    """Analyze the represented relation ``A B^T = 2*pi*I``."""

    __slots__ = ()

    def execute(
        self,
        direct: DirectLattice,
        reciprocal: ReciprocalLattice,
        *,
        absolute_tolerance: float,
    ) -> LatticeDualityResult:
        """Return duality residuals after explicit reciprocal-unit conversion.

        Parameters
        ----------
        direct
            One supported direct lattice.
        reciprocal
            One supported reciprocal lattice.
        absolute_tolerance
            Positive finite built-in float applied componentwise to the dimensionless
            duality residual.
        """
        if not isinstance(direct, DirectLattice1D | DirectLattice2D | DirectLattice3D):
            raise TypeError("direct must be a supported direct lattice")
        if not isinstance(
            reciprocal,
            ReciprocalLattice1D | ReciprocalLattice2D | ReciprocalLattice3D,
        ):
            raise TypeError("reciprocal must be a supported reciprocal lattice")
        if type(absolute_tolerance) is not float:
            raise TypeError("absolute_tolerance must be a built-in float")
        if not math.isfinite(absolute_tolerance) or absolute_tolerance <= 0.0:
            raise ValueError("absolute_tolerance must be positive and finite")
        direct_dimension = (
            1
            if type(direct) is DirectLattice1D
            else 2
            if type(direct) is DirectLattice2D
            else 3
        )
        reciprocal_dimension = (
            1
            if type(reciprocal) is ReciprocalLattice1D
            else 2
            if type(reciprocal) is ReciprocalLattice2D
            else 3
        )
        if direct_dimension != reciprocal_dimension:
            return LatticeDualityResult(
                False, None, ("SOLID_STATE.LATTICE_DUALITY.DIMENSION_MISMATCH",)
            )
        target = PhysicalUnit(f"1 / ({direct.unit.expression})")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(reciprocal.unit, target):
            return LatticeDualityResult(
                False, None, ("SOLID_STATE.LATTICE_DUALITY.UNIT_MISMATCH",)
            )
        factor = MODEL_SYSTEM_UNIT_CONVERTER.conversion_factor(reciprocal.unit, target)
        direct_vectors: LatticeBasisVectors
        reciprocal_vectors: LatticeBasisVectors
        if type(direct) is DirectLattice1D and type(reciprocal) is ReciprocalLattice1D:
            direct_vectors = (direct.vector,)
            reciprocal_vectors = (reciprocal.vector,)
        elif (
            type(direct) is DirectLattice2D and type(reciprocal) is ReciprocalLattice2D
        ):
            direct_vectors = direct.vectors
            reciprocal_vectors = reciprocal.vectors
        elif (
            type(direct) is DirectLattice3D and type(reciprocal) is ReciprocalLattice3D
        ):
            direct_vectors = direct.vectors
            reciprocal_vectors = reciprocal.vectors
        else:
            return LatticeDualityResult(
                False, None, ("SOLID_STATE.LATTICE_DUALITY.DIMENSION_MISMATCH",)
            )
        maximum = 0.0
        for row, direct_vector in enumerate(direct_vectors):
            for column, reciprocal_vector in enumerate(reciprocal_vectors):
                value = math.fsum(
                    direct_component * reciprocal_component * factor
                    for direct_component, reciprocal_component in zip(
                        direct_vector, reciprocal_vector, strict=True
                    )
                )
                expected = 2.0 * math.pi if row == column else 0.0
                maximum = max(maximum, abs(value - expected))
        issues = (
            ()
            if maximum <= absolute_tolerance
            else ("SOLID_STATE.LATTICE_DUALITY.RESIDUAL_EXCEEDED",)
        )
        return LatticeDualityResult(not issues, maximum, issues)
