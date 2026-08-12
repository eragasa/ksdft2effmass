"""Backend-neutral immutable periodic geometry.

The objects in this module distinguish a unit system, physical dimension,
concrete unit, coordinate convention, and scale convention.  They contain no
Quantum ESPRESSO, QEXSD, Kohn--Sham spectral, FFT-grid, or complete-calculation
semantics.
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
    if type(vector) is not tuple or len(vector) != 3:
        raise ValueError(f"{name} must be a three-component tuple")
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


@dataclass(frozen=True, slots=True)
class DirectLattice:
    """Three Cartesian direct-lattice vectors in concrete length units."""

    vectors: Vector3Sequence
    unit_system: UnitSystem
    dimension: PhysicalDimension
    unit: LengthUnit
    coordinate_convention: CoordinateConvention
    vector_order: str

    def __post_init__(self) -> None:
        _vectors(self.vectors, "direct lattice vectors", count=3)
        if self.unit_system is not UnitSystem.HARTREE_ATOMIC:
            raise ValueError("direct lattice requires the represented unit system")
        if self.dimension is not PhysicalDimension.LENGTH:
            raise ValueError("direct lattice dimension must be length")
        if self.unit is not LengthUnit.BOHR:
            raise ValueError("direct lattice unit must be bohr")
        if self.coordinate_convention is not CoordinateConvention.CARTESIAN:
            raise ValueError("direct lattice coordinates must be Cartesian")
        if type(self.vector_order) is not str or not self.vector_order:
            raise ValueError("direct lattice vector_order must be nonempty")


@dataclass(frozen=True, slots=True)
class ReciprocalLattice:
    """Raw reciprocal coefficients and their explicitly scaled physical vectors.

    ``physical_vectors = raw_coefficients * (2*pi/alat)``.  Construction checks
    both that conversion and ``A B^T = 2*pi I`` with an absolute componentwise
    residual not exceeding ``duality_absolute_tolerance``.
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
    duality_absolute_tolerance: float
    direct_lattice: DirectLattice

    def __post_init__(self) -> None:
        _vectors(self.raw_coefficients, "raw reciprocal coefficients", count=3)
        _vectors(self.physical_vectors, "physical reciprocal vectors", count=3)
        if self.raw_dimension is not PhysicalDimension.DIMENSIONLESS:
            raise ValueError("raw reciprocal coefficients must be dimensionless")
        if self.raw_coordinate_convention is not CoordinateConvention.CARTESIAN:
            raise ValueError("raw reciprocal coefficients must be Cartesian")
        if self.scale_convention is not ReciprocalScaleConvention.TWO_PI_OVER_ALAT:
            raise ValueError("unsupported reciprocal scale convention")
        if type(self.scale_alat) is not float or not math.isfinite(self.scale_alat):
            raise TypeError("scale_alat must be a finite built-in float")
        if self.scale_alat <= 0:
            raise ValueError("scale_alat must be positive")
        if self.scale_alat_unit is not LengthUnit.BOHR:
            raise ValueError("reciprocal scale alat unit must be bohr")
        if self.incorporates_two_pi is not True:
            raise ValueError("2pi_over_alat must explicitly incorporate two pi")
        if self.physical_dimension is not PhysicalDimension.INVERSE_LENGTH:
            raise ValueError("physical reciprocal dimension must be inverse length")
        if self.physical_unit is not InverseLengthUnit.PER_BOHR:
            raise ValueError("physical reciprocal unit must be bohr^-1")
        if self.physical_coordinate_convention is not CoordinateConvention.CARTESIAN:
            raise ValueError("physical reciprocal vectors must be Cartesian")
        if (
            type(self.duality_absolute_tolerance) is not float
            or not math.isfinite(self.duality_absolute_tolerance)
            or self.duality_absolute_tolerance <= 0
        ):
            raise ValueError("duality_absolute_tolerance must be a positive float")
        scale = 2.0 * math.pi / self.scale_alat
        for raw, physical in zip(
            self.raw_coefficients, self.physical_vectors, strict=True
        ):
            for raw_value, physical_value in zip(raw, physical, strict=True):
                if physical_value != raw_value * scale:
                    raise ValueError("physical reciprocal vectors disagree with scale")
        for i, direct in enumerate(self.direct_lattice.vectors):
            for j, reciprocal in enumerate(self.physical_vectors):
                value = math.fsum(
                    a * b for a, b in zip(direct, reciprocal, strict=True)
                )
                expected = 2.0 * math.pi if i == j else 0.0
                if abs(value - expected) > self.duality_absolute_tolerance:
                    raise ValueError("direct and reciprocal lattices are inconsistent")


@dataclass(frozen=True, slots=True)
class AtomicSpecies:
    """One ordered species declaration used by a periodic structure."""

    name: str
    mass: float
    mass_dimension: PhysicalDimension
    mass_unit: str
    pseudopotential_label: str

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name:
            raise ValueError("species name must be nonempty")
        if (
            type(self.mass) is not float
            or not math.isfinite(self.mass)
            or self.mass <= 0
        ):
            raise ValueError("species mass must be a positive built-in float")
        if self.mass_dimension is not PhysicalDimension.MASS:
            raise ValueError("species mass dimension must be mass")
        if self.mass_unit != "unified_atomic_mass_unit":
            raise ValueError("species mass unit must be unified_atomic_mass_unit")
        if (
            type(self.pseudopotential_label) is not str
            or not self.pseudopotential_label
        ):
            raise ValueError("pseudopotential_label must be nonempty")


@dataclass(frozen=True, slots=True)
class PeriodicSite:
    """One source-ordered Cartesian site in a periodic structure."""

    index: int
    species_name: str
    coordinates: Vector3
    coordinate_convention: CoordinateConvention
    coordinate_dimension: PhysicalDimension
    coordinate_unit: LengthUnit

    def __post_init__(self) -> None:
        if type(self.index) is not int or self.index <= 0:
            raise ValueError("site index must be a positive built-in integer")
        if type(self.species_name) is not str or not self.species_name:
            raise ValueError("site species_name must be nonempty")
        _finite_vector(self.coordinates, "site coordinates")
        if self.coordinate_convention is not CoordinateConvention.CARTESIAN:
            raise ValueError("site coordinates must be Cartesian")
        if self.coordinate_dimension is not PhysicalDimension.LENGTH:
            raise ValueError("site coordinate dimension must be length")
        if self.coordinate_unit is not LengthUnit.BOHR:
            raise ValueError("Cartesian site coordinate unit must be bohr")


@dataclass(frozen=True, slots=True)
class PeriodicStructure:
    """Direct lattice, ordered species, and ordered sites."""

    direct_lattice: DirectLattice
    species: tuple[AtomicSpecies, ...]
    sites: tuple[PeriodicSite, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.direct_lattice, DirectLattice):
            raise TypeError("direct_lattice must be DirectLattice")
        if type(self.species) is not tuple or not self.species:
            raise ValueError("species must be a nonempty tuple")
        names = tuple(item.name for item in self.species)
        if len(set(names)) != len(names):
            raise ValueError("species names must be unique")
        if type(self.sites) is not tuple or not self.sites:
            raise ValueError("sites must be a nonempty tuple")
        for expected, site in enumerate(self.sites, start=1):
            if site.index != expected:
                raise ValueError("site indices must preserve contiguous source order")
            if site.species_name not in names:
                raise ValueError("site has an unresolved species reference")


@dataclass(frozen=True, slots=True)
class KPointSampling:
    """Ordered Cartesian k points with explicit reciprocal scale and weights."""

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
        if (
            type(self.scale_alat) is not float
            or not math.isfinite(self.scale_alat)
            or self.scale_alat <= 0
        ):
            raise ValueError("k-point scale_alat must be a positive built-in float")
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
        if type(self.weights) is not tuple or len(self.weights) != len(
            self.raw_coordinates
        ):
            raise ValueError("k-point weight count must match coordinate count")
        if any(
            type(value) is not float or not math.isfinite(value) or value < 0
            for value in self.weights
        ):
            raise ValueError("k-point weights must be finite nonnegative floats")
        if self.weight_normalization is KPointWeightNormalization.SUM_TO_TWO:
            if math.fsum(self.weights) != 2.0:
                raise ValueError("sum_to_two k-point weights must sum exactly to 2.0")
        elif self.weight_normalization is not KPointWeightNormalization.UNAVAILABLE:
            raise ValueError("unsupported k-point weight normalization")
