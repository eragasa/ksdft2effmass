"""Backend-neutral immutable periodic geometry.

The objects in this module distinguish a unit system, physical dimension,
concrete unit, coordinate convention, and scale convention. Vectors are ordered
three-tuples of finite built-in :class:`float` values. Public integer fields
accept built-in :class:`int` values but reject booleans; numeric strings and
NumPy scalars are not converted. Values must already be finite when supplied, so
external parsing and overflow handling belong to the calling integration.

The records contain no Quantum ESPRESSO, QEXSD, Kohn--Sham spectral, FFT-grid,
or complete-calculation semantics. Constructor checks are software-contract
verification boundaries, not scientific validation of a represented structure
or sampling.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

type Vector3 = tuple[float, float, float]
type Vector3Sequence = tuple[Vector3, ...]


class UnitSystem(StrEnum):
    """Supported field-level unit systems."""

    HARTREE_ATOMIC = "hartree_atomic"


class PhysicalDimension(StrEnum):
    """Physical dimensions demonstrated by the retained periodic artifact."""

    DIMENSIONLESS = "dimensionless"
    LENGTH = "length"
    INVERSE_LENGTH = "inverse_length"
    MASS = "mass"


class LengthUnit(StrEnum):
    """Concrete length units demonstrated by the retained artifact."""

    BOHR = "bohr"


class InverseLengthUnit(StrEnum):
    """Concrete inverse-length units demonstrated by the retained artifact."""

    PER_BOHR = "bohr^-1"


class CoordinateConvention(StrEnum):
    """Coordinate conventions used by retained geometry arrays."""

    CARTESIAN = "cartesian"


class ReciprocalScaleConvention(StrEnum):
    """Scale relating raw reciprocal coefficients to physical vectors."""

    TWO_PI_OVER_ALAT = "2pi_over_alat"


class KPointWeightNormalization(StrEnum):
    """Normalization state of represented k-point weights."""

    SUM_TO_TWO = "sum_to_two"
    UNAVAILABLE = "unavailable"


def _finite_vector(vector: object, name: str) -> None:
    if type(vector) is not tuple:
        raise TypeError(f"{name} must be a tuple")
    if len(vector) != 3:
        raise ValueError(f"{name} must contain exactly three components")
    for component in vector:
        if type(component) is not float:
            raise TypeError(f"{name} components must be built-in floats")
        if not math.isfinite(component):
            raise ValueError(f"{name} components must be finite")


def _vectors(vectors: object, name: str, *, count: int | None = None) -> None:
    if type(vectors) is not tuple:
        raise TypeError(f"{name} must be a tuple")
    if count is not None and len(vectors) != count:
        raise ValueError(f"{name} must contain exactly {count} vectors")
    for vector in vectors:
        _finite_vector(vector, name)


def _require_enum(value: object, enum_type: type[StrEnum], name: str) -> None:
    if type(value) is not enum_type:
        raise TypeError(f"{name} must be {enum_type.__name__}")


@dataclass(frozen=True, slots=True)
class DirectLattice:
    """Three source-ordered Cartesian direct-lattice vectors.

    Attributes
    ----------
    vectors
        Exactly three finite three-vectors in bohr.
    unit_system
        Must be :attr:`UnitSystem.HARTREE_ATOMIC`.
    dimension
        Must be :attr:`PhysicalDimension.LENGTH`.
    unit
        Must be :attr:`LengthUnit.BOHR`.
    coordinate_convention
        Must be :attr:`CoordinateConvention.CARTESIAN`.
    vector_order
        Nonempty description of the preserved source ordering.
    """

    vectors: Vector3Sequence
    unit_system: UnitSystem
    dimension: PhysicalDimension
    unit: LengthUnit
    coordinate_convention: CoordinateConvention
    vector_order: str

    def __post_init__(self) -> None:
        _vectors(self.vectors, "direct lattice vectors", count=3)
        _require_enum(self.unit_system, UnitSystem, "direct lattice unit_system")
        _require_enum(self.dimension, PhysicalDimension, "direct lattice dimension")
        _require_enum(self.unit, LengthUnit, "direct lattice unit")
        _require_enum(
            self.coordinate_convention,
            CoordinateConvention,
            "direct lattice coordinate_convention",
        )
        if self.unit_system is not UnitSystem.HARTREE_ATOMIC:
            raise ValueError("direct lattice requires the represented unit system")
        if self.dimension is not PhysicalDimension.LENGTH:
            raise ValueError("direct lattice dimension must be length")
        if self.unit is not LengthUnit.BOHR:
            raise ValueError("direct lattice unit must be bohr")
        if self.coordinate_convention is not CoordinateConvention.CARTESIAN:
            raise ValueError("direct lattice coordinates must be Cartesian")
        if type(self.vector_order) is not str:
            raise TypeError("direct lattice vector_order must be str")
        if not self.vector_order:
            raise ValueError("direct lattice vector_order must be nonempty")


@dataclass(frozen=True, slots=True)
class ReciprocalLattice:
    """Raw reciprocal coefficients and explicitly scaled physical vectors.

    ``physical_vectors = raw_coefficients * (2*pi/alat)``. Construction checks
    this intrinsic represented equality. Compatibility with an independently
    represented direct lattice belongs to
    :class:`ReciprocalLatticeCompatibilityValidator`.

    Attributes
    ----------
    raw_coefficients
        Exactly three dimensionless Cartesian built-in-float three-vectors.
    raw_dimension
        Must be :attr:`PhysicalDimension.DIMENSIONLESS`.
    raw_coordinate_convention
        Must be :attr:`CoordinateConvention.CARTESIAN`.
    scale_convention
        Must be :attr:`ReciprocalScaleConvention.TWO_PI_OVER_ALAT`.
    scale_alat
        Positive finite built-in float in bohr.
    scale_alat_unit
        Must be :attr:`LengthUnit.BOHR`.
    incorporates_two_pi
        Must be the built-in boolean ``True``.
    physical_vectors
        Exactly scaled Cartesian vectors in bohr^-1.
    physical_dimension
        Must be :attr:`PhysicalDimension.INVERSE_LENGTH`.
    physical_unit
        Must be :attr:`InverseLengthUnit.PER_BOHR`.
    physical_coordinate_convention
        Must be :attr:`CoordinateConvention.CARTESIAN`.
    """

    raw_coefficients: Vector3Sequence
    raw_dimension: PhysicalDimension
    raw_coordinate_convention: CoordinateConvention
    scale_convention: ReciprocalScaleConvention
    scale_alat: float
    scale_alat_unit: LengthUnit
    incorporates_two_pi: bool
    physical_vectors: Vector3Sequence
    physical_dimension: PhysicalDimension
    physical_unit: InverseLengthUnit
    physical_coordinate_convention: CoordinateConvention

    def __post_init__(self) -> None:
        _vectors(self.raw_coefficients, "raw reciprocal coefficients", count=3)
        _vectors(self.physical_vectors, "physical reciprocal vectors", count=3)
        _require_enum(self.raw_dimension, PhysicalDimension, "raw_dimension")
        _require_enum(
            self.raw_coordinate_convention,
            CoordinateConvention,
            "raw_coordinate_convention",
        )
        _require_enum(
            self.scale_convention,
            ReciprocalScaleConvention,
            "scale_convention",
        )
        _require_enum(self.scale_alat_unit, LengthUnit, "scale_alat_unit")
        _require_enum(self.physical_dimension, PhysicalDimension, "physical_dimension")
        _require_enum(self.physical_unit, InverseLengthUnit, "physical_unit")
        _require_enum(
            self.physical_coordinate_convention,
            CoordinateConvention,
            "physical_coordinate_convention",
        )
        if self.raw_dimension is not PhysicalDimension.DIMENSIONLESS:
            raise ValueError("raw reciprocal coefficients must be dimensionless")
        if self.raw_coordinate_convention is not CoordinateConvention.CARTESIAN:
            raise ValueError("raw reciprocal coefficients must be Cartesian")
        if self.scale_convention is not ReciprocalScaleConvention.TWO_PI_OVER_ALAT:
            raise ValueError("unsupported reciprocal scale convention")
        if type(self.scale_alat) is not float:
            raise TypeError("scale_alat must be a built-in float")
        if not math.isfinite(self.scale_alat) or self.scale_alat <= 0:
            raise ValueError("scale_alat must be positive and finite")
        if self.scale_alat_unit is not LengthUnit.BOHR:
            raise ValueError("reciprocal scale alat unit must be bohr")
        if type(self.incorporates_two_pi) is not bool:
            raise TypeError("incorporates_two_pi must be bool")
        if self.incorporates_two_pi is not True:
            raise ValueError("2pi_over_alat must explicitly incorporate two pi")
        if self.physical_dimension is not PhysicalDimension.INVERSE_LENGTH:
            raise ValueError("physical reciprocal dimension must be inverse length")
        if self.physical_unit is not InverseLengthUnit.PER_BOHR:
            raise ValueError("physical reciprocal unit must be bohr^-1")
        if self.physical_coordinate_convention is not CoordinateConvention.CARTESIAN:
            raise ValueError("physical reciprocal vectors must be Cartesian")
        scale = 2.0 * math.pi / self.scale_alat
        for raw, physical in zip(
            self.raw_coefficients, self.physical_vectors, strict=True
        ):
            for raw_value, physical_value in zip(raw, physical, strict=True):
                if physical_value != raw_value * scale:
                    raise ValueError("physical reciprocal vectors disagree with scale")


class ReciprocalLatticeCompatibilityValidator:
    """Validate direct--reciprocal lattice compatibility.

    The validator owns the absolute componentwise residual policy for the
    represented relation ``A B^T = 2*pi I``. It does not mutate either lattice
    or establish physical adequacy of the represented geometry.
    """

    __slots__ = ()

    def execute(
        self,
        direct_lattice: DirectLattice,
        reciprocal_lattice: ReciprocalLattice,
        *,
        absolute_tolerance: float,
    ) -> None:
        """Raise when two lattices violate the declared duality tolerance.

        Parameters
        ----------
        direct_lattice
            Direct-lattice representation ``A`` in bohr.
        reciprocal_lattice
            Reciprocal-lattice representation ``B`` in bohr^-1.
        absolute_tolerance
            Positive finite built-in float applied componentwise to
            ``A B^T - 2*pi I``. Booleans, numeric strings, NumPy scalars, and
            nonfinite values are rejected rather than converted.

        Raises
        ------
        TypeError
            If an argument has the wrong semantic type.
        ValueError
            If the tolerance is not positive and finite or a residual exceeds
            the tolerance.
        """
        if type(direct_lattice) is not DirectLattice:
            raise TypeError("direct_lattice must be DirectLattice")
        if type(reciprocal_lattice) is not ReciprocalLattice:
            raise TypeError("reciprocal_lattice must be ReciprocalLattice")
        if type(absolute_tolerance) is not float:
            raise TypeError("absolute_tolerance must be a built-in float")
        if not math.isfinite(absolute_tolerance) or absolute_tolerance <= 0:
            raise ValueError("absolute_tolerance must be positive and finite")
        for i, direct in enumerate(direct_lattice.vectors):
            for j, reciprocal in enumerate(reciprocal_lattice.physical_vectors):
                value = math.fsum(
                    a * b for a, b in zip(direct, reciprocal, strict=True)
                )
                expected = 2.0 * math.pi if i == j else 0.0
                if abs(value - expected) > absolute_tolerance:
                    raise ValueError("direct and reciprocal lattices are inconsistent")


@dataclass(frozen=True, slots=True)
class AtomicSpecies:
    """One ordered species declaration used by a periodic structure.

    Attributes
    ----------
    name
        Nonempty species identifier.
    mass
        Positive finite built-in float in unified atomic mass units.
    mass_dimension
        Must be :attr:`PhysicalDimension.MASS`.
    mass_unit
        Must be ``"unified_atomic_mass_unit"``.
    pseudopotential_label
        Nonempty retained source label; it is not a pseudopotential identity.
    """

    name: str
    mass: float
    mass_dimension: PhysicalDimension
    mass_unit: str
    pseudopotential_label: str

    def __post_init__(self) -> None:
        if type(self.name) is not str:
            raise TypeError("species name must be str")
        if not self.name:
            raise ValueError("species name must be nonempty")
        if type(self.mass) is not float:
            raise TypeError("species mass must be a built-in float")
        if not math.isfinite(self.mass) or self.mass <= 0:
            raise ValueError("species mass must be positive and finite")
        _require_enum(self.mass_dimension, PhysicalDimension, "mass_dimension")
        if self.mass_dimension is not PhysicalDimension.MASS:
            raise ValueError("species mass dimension must be mass")
        if type(self.mass_unit) is not str:
            raise TypeError("species mass_unit must be str")
        if self.mass_unit != "unified_atomic_mass_unit":
            raise ValueError("species mass unit must be unified_atomic_mass_unit")
        if type(self.pseudopotential_label) is not str:
            raise TypeError("pseudopotential_label must be str")
        if not self.pseudopotential_label:
            raise ValueError("pseudopotential_label must be nonempty")


@dataclass(frozen=True, slots=True)
class PeriodicSite:
    """One source-ordered Cartesian site in a periodic structure.

    Attributes
    ----------
    index
        Positive one-based built-in integer source index; booleans are rejected.
    species_name
        Nonempty reference to an owning structure's species declaration.
    coordinates
        Finite Cartesian three-vector in bohr.
    coordinate_convention
        Must be :attr:`CoordinateConvention.CARTESIAN`.
    coordinate_dimension
        Must be :attr:`PhysicalDimension.LENGTH`.
    coordinate_unit
        Must be :attr:`LengthUnit.BOHR`.
    """

    index: int
    species_name: str
    coordinates: Vector3
    coordinate_convention: CoordinateConvention
    coordinate_dimension: PhysicalDimension
    coordinate_unit: LengthUnit

    def __post_init__(self) -> None:
        if type(self.index) is not int:
            raise TypeError("site index must be a built-in integer")
        if self.index <= 0:
            raise ValueError("site index must be positive")
        if type(self.species_name) is not str:
            raise TypeError("site species_name must be str")
        if not self.species_name:
            raise ValueError("site species_name must be nonempty")
        _finite_vector(self.coordinates, "site coordinates")
        _require_enum(
            self.coordinate_convention, CoordinateConvention, "coordinate_convention"
        )
        _require_enum(
            self.coordinate_dimension, PhysicalDimension, "coordinate_dimension"
        )
        _require_enum(self.coordinate_unit, LengthUnit, "coordinate_unit")
        if self.coordinate_convention is not CoordinateConvention.CARTESIAN:
            raise ValueError("site coordinates must be Cartesian")
        if self.coordinate_dimension is not PhysicalDimension.LENGTH:
            raise ValueError("site coordinate dimension must be length")
        if self.coordinate_unit is not LengthUnit.BOHR:
            raise ValueError("Cartesian site coordinate unit must be bohr")


@dataclass(frozen=True, slots=True)
class PeriodicStructure:
    """Direct lattice, ordered species, and ordered sites.

    Attributes
    ----------
    direct_lattice
        Backend-neutral direct lattice.
    species
        Nonempty tuple of uniquely named :class:`AtomicSpecies` values.
    sites
        Nonempty tuple of :class:`PeriodicSite` values with contiguous one-based
        indices and species references resolved within ``species``.
    """

    direct_lattice: DirectLattice
    species: tuple[AtomicSpecies, ...]
    sites: tuple[PeriodicSite, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.direct_lattice, DirectLattice):
            raise TypeError("direct_lattice must be DirectLattice")
        if type(self.species) is not tuple:
            raise TypeError("species must be a tuple")
        if not self.species:
            raise ValueError("species must be nonempty")
        if any(type(item) is not AtomicSpecies for item in self.species):
            raise TypeError("species members must be AtomicSpecies")
        names = tuple(item.name for item in self.species)
        if len(set(names)) != len(names):
            raise ValueError("species names must be unique")
        if type(self.sites) is not tuple:
            raise TypeError("sites must be a tuple")
        if not self.sites:
            raise ValueError("sites must be nonempty")
        if any(type(site) is not PeriodicSite for site in self.sites):
            raise TypeError("sites members must be PeriodicSite")
        for expected, site in enumerate(self.sites, start=1):
            if site.index != expected:
                raise ValueError("site indices must preserve contiguous source order")
            if site.species_name not in names:
                raise ValueError("site has an unresolved species reference")


@dataclass(frozen=True, slots=True)
class KPointSampling:
    """Ordered Cartesian k points with explicit reciprocal scale and weights.

    Raw coordinates are dimensionless built-in-float three-vectors. Physical
    coordinates are the exact represented product of each raw component and
    ``2*pi/scale_alat`` in bohr^-1; no tolerance is applied to this represented
    equality.

    Attributes
    ----------
    raw_coordinates
        Nonempty ordered dimensionless Cartesian built-in-float three-vectors.
    raw_dimension
        Must be :attr:`PhysicalDimension.DIMENSIONLESS`.
    coordinate_convention
        Must be :attr:`CoordinateConvention.CARTESIAN`.
    scale_convention
        Must be :attr:`ReciprocalScaleConvention.TWO_PI_OVER_ALAT`.
    scale_alat
        Positive finite built-in float in bohr.
    scale_alat_unit
        Must be :attr:`LengthUnit.BOHR`.
    incorporates_two_pi
        Must be the built-in boolean ``True``.
    physical_coordinates
        Nonempty equally sized coordinates scaled exactly into bohr^-1.
    physical_dimension
        Must be :attr:`PhysicalDimension.INVERSE_LENGTH`.
    physical_unit
        Must be :attr:`InverseLengthUnit.PER_BOHR`.
    weights
        Finite nonnegative built-in floats, one per coordinate.
    weight_normalization
        Either an exact sum-to-two declaration or explicitly unavailable.
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
        _vectors(self.raw_coordinates, "raw k-point coordinates")
        _vectors(self.physical_coordinates, "physical k-point coordinates")
        _require_enum(self.raw_dimension, PhysicalDimension, "raw_dimension")
        _require_enum(
            self.coordinate_convention, CoordinateConvention, "coordinate_convention"
        )
        _require_enum(
            self.scale_convention,
            ReciprocalScaleConvention,
            "scale_convention",
        )
        _require_enum(self.scale_alat_unit, LengthUnit, "scale_alat_unit")
        _require_enum(self.physical_dimension, PhysicalDimension, "physical_dimension")
        _require_enum(self.physical_unit, InverseLengthUnit, "physical_unit")
        _require_enum(
            self.weight_normalization,
            KPointWeightNormalization,
            "weight_normalization",
        )
        if (
            len(self.raw_coordinates) != len(self.physical_coordinates)
            or not self.raw_coordinates
        ):
            raise ValueError(
                "raw and physical k-point counts must agree and be nonzero"
            )
        if self.raw_dimension is not PhysicalDimension.DIMENSIONLESS:
            raise ValueError("raw k-point coordinates must be dimensionless")
        if self.coordinate_convention is not CoordinateConvention.CARTESIAN:
            raise ValueError("k-point coordinates must be Cartesian")
        if self.scale_convention is not ReciprocalScaleConvention.TWO_PI_OVER_ALAT:
            raise ValueError("unsupported k-point reciprocal scale")
        if type(self.scale_alat) is not float:
            raise TypeError("k-point scale_alat must be a built-in float")
        if not math.isfinite(self.scale_alat) or self.scale_alat <= 0:
            raise ValueError("k-point scale_alat must be positive and finite")
        if type(self.incorporates_two_pi) is not bool:
            raise TypeError("incorporates_two_pi must be bool")
        if (
            self.scale_alat_unit is not LengthUnit.BOHR
            or self.incorporates_two_pi is not True
        ):
            raise ValueError("k-point scale must explicitly be 2pi over alat in bohr")
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
