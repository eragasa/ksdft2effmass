"""Backend-neutral immutable periodic crystal geometry.

This module owns direct and reciprocal lattices, atomic species declarations,
source-ordered sites, periodic structures, and their intrinsic conventions.  It does
not own molecular topology, calculator execution, native formats, k-point sampling,
pseudopotential identity, or scientific acceptance.

The transitional :class:`AtomicSpecies` ``pseudopotential_label`` field is retained
only for the existing schema-version-1 plane-wave record.  It is not reusable
structure meaning and will move to the plane-wave calculator owner when that
aggregate's compatibility migration is authorized.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

type Vector3 = tuple[float, float, float]
type Vector3Sequence = tuple[Vector3, ...]

__all__ = [
    "AtomicSpecies",
    "CoordinateConvention",
    "DirectLattice",
    "InverseLengthUnit",
    "LengthUnit",
    "PeriodicSite",
    "PeriodicStructure",
    "PhysicalDimension",
    "ReciprocalLattice",
    "ReciprocalLatticeCompatibilityValidator",
    "ReciprocalScaleConvention",
    "UnitSystem",
]


class UnitSystem(StrEnum):
    """Supported field-level unit systems."""

    METAL = "metal"
    HARTREE_ATOMIC = "hartree_atomic"


class PhysicalDimension(StrEnum):
    """Physical dimensions represented by periodic geometry."""

    DIMENSIONLESS = "dimensionless"
    LENGTH = "length"
    INVERSE_LENGTH = "inverse_length"
    MASS = "mass"


class LengthUnit(StrEnum):
    """Concrete length units represented by periodic geometry."""

    ANGSTROM = "angstrom"
    BOHR = "bohr"


class InverseLengthUnit(StrEnum):
    """Concrete inverse-length units represented by retained native records."""

    PER_BOHR = "bohr^-1"


class CoordinateConvention(StrEnum):
    """Coordinate conventions represented by periodic geometry."""

    CARTESIAN = "cartesian"


class ReciprocalScaleConvention(StrEnum):
    """Scale relating raw reciprocal coefficients to physical vectors."""

    TWO_PI_OVER_ALAT = "2pi_over_alat"


@dataclass(frozen=True, slots=True)
class DirectLattice:
    """Three source-ordered Cartesian direct-lattice vectors.

    Parameters
    ----------
    vectors
        Exactly three finite Cartesian three-vectors. New project-owned structures
        use angstrom; bohr is retained only for accepted native version-one records.
    unit_system
        :attr:`UnitSystem.METAL` for canonical structures or
        :attr:`UnitSystem.HARTREE_ATOMIC` for retained native records.
    dimension
        Must be :attr:`PhysicalDimension.LENGTH`.
    unit
        Must match the selected unit system: angstrom for metal and bohr for retained
        Hartree-atomic records.
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
        """Validate intrinsic lattice representation and conventions."""
        self._validate_vectors(self.vectors)
        if type(self.unit_system) is not UnitSystem:
            raise TypeError("direct lattice unit_system must be UnitSystem")
        if type(self.dimension) is not PhysicalDimension:
            raise TypeError("direct lattice dimension must be PhysicalDimension")
        if type(self.unit) is not LengthUnit:
            raise TypeError("direct lattice unit must be LengthUnit")
        if type(self.coordinate_convention) is not CoordinateConvention:
            raise TypeError(
                "direct lattice coordinate_convention must be CoordinateConvention"
            )
        if self.dimension is not PhysicalDimension.LENGTH:
            raise ValueError("direct lattice dimension must be length")
        expected_unit = (
            LengthUnit.ANGSTROM
            if self.unit_system is UnitSystem.METAL
            else LengthUnit.BOHR
        )
        if self.unit is not expected_unit:
            raise ValueError("direct lattice unit must match its unit system")
        if self.coordinate_convention is not CoordinateConvention.CARTESIAN:
            raise ValueError("direct lattice coordinates must be Cartesian")
        if type(self.vector_order) is not str:
            raise TypeError("direct lattice vector_order must be str")
        if not self.vector_order:
            raise ValueError("direct lattice vector_order must be nonempty")

    @staticmethod
    def _validate_vectors(vectors: Vector3Sequence) -> None:
        """Validate the exact immutable three-by-three built-in-float array."""
        if type(vectors) is not tuple:
            raise TypeError("direct lattice vectors must be a tuple")
        if len(vectors) != 3:
            raise ValueError("direct lattice vectors must contain exactly 3 vectors")
        for vector in vectors:
            if type(vector) is not tuple:
                raise TypeError("direct lattice vectors must contain tuples")
            if len(vector) != 3:
                raise ValueError("direct lattice vectors must contain three components")
            for component in vector:
                if type(component) is not float:
                    raise TypeError(
                        "direct lattice vector components must be built-in floats"
                    )
                if not math.isfinite(component):
                    raise ValueError("direct lattice vector components must be finite")


@dataclass(frozen=True, slots=True)
class ReciprocalLattice:
    """Raw reciprocal coefficients and explicitly scaled physical vectors.

    ``physical_vectors = raw_coefficients * (2*pi/alat)``. Construction checks
    this intrinsic represented equality. Compatibility with an independently
    represented direct lattice belongs to
    :class:`ReciprocalLatticeCompatibilityValidator`.

    Parameters
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
        Must be the built-in Boolean ``True``.
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
        """Validate intrinsic reciprocal representation and exact scaling."""
        self._validate_vectors(self.raw_coefficients, "raw reciprocal coefficients")
        self._validate_vectors(self.physical_vectors, "physical reciprocal vectors")
        if type(self.raw_dimension) is not PhysicalDimension:
            raise TypeError("raw_dimension must be PhysicalDimension")
        if type(self.raw_coordinate_convention) is not CoordinateConvention:
            raise TypeError("raw_coordinate_convention must be CoordinateConvention")
        if type(self.scale_convention) is not ReciprocalScaleConvention:
            raise TypeError("scale_convention must be ReciprocalScaleConvention")
        if type(self.scale_alat) is not float:
            raise TypeError("scale_alat must be a built-in float")
        if type(self.scale_alat_unit) is not LengthUnit:
            raise TypeError("scale_alat_unit must be LengthUnit")
        if type(self.incorporates_two_pi) is not bool:
            raise TypeError("incorporates_two_pi must be bool")
        if type(self.physical_dimension) is not PhysicalDimension:
            raise TypeError("physical_dimension must be PhysicalDimension")
        if type(self.physical_unit) is not InverseLengthUnit:
            raise TypeError("physical_unit must be InverseLengthUnit")
        if type(self.physical_coordinate_convention) is not CoordinateConvention:
            raise TypeError(
                "physical_coordinate_convention must be CoordinateConvention"
            )
        if self.raw_dimension is not PhysicalDimension.DIMENSIONLESS:
            raise ValueError("raw reciprocal coefficients must be dimensionless")
        if self.raw_coordinate_convention is not CoordinateConvention.CARTESIAN:
            raise ValueError("raw reciprocal coefficients must be Cartesian")
        if self.scale_convention is not ReciprocalScaleConvention.TWO_PI_OVER_ALAT:
            raise ValueError("unsupported reciprocal scale convention")
        if not math.isfinite(self.scale_alat) or self.scale_alat <= 0:
            raise ValueError("scale_alat must be positive and finite")
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
        scale = 2.0 * math.pi / self.scale_alat
        for raw, physical in zip(
            self.raw_coefficients, self.physical_vectors, strict=True
        ):
            for raw_value, physical_value in zip(raw, physical, strict=True):
                if physical_value != raw_value * scale:
                    raise ValueError("physical reciprocal vectors disagree with scale")

    @staticmethod
    def _validate_vectors(vectors: Vector3Sequence, name: str) -> None:
        """Validate one exact immutable sequence of finite three-vectors."""
        if type(vectors) is not tuple:
            raise TypeError(f"{name} must be a tuple")
        if len(vectors) != 3:
            raise ValueError(f"{name} must contain exactly 3 vectors")
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


class ReciprocalLatticeCompatibilityValidator:
    """Validate direct--reciprocal lattice compatibility.

    The validator owns the absolute componentwise residual policy for the represented
    relation ``A B^T = 2*pi I``. It does not mutate either lattice or establish
    physical adequacy of the represented geometry.
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
            ``A B^T - 2*pi I``.

        Raises
        ------
        TypeError
            If an argument has the wrong semantic type.
        ValueError
            If the tolerance is invalid or a residual exceeds it.
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
                    component * reciprocal_component
                    for component, reciprocal_component in zip(
                        direct, reciprocal, strict=True
                    )
                )
                expected = 2.0 * math.pi if i == j else 0.0
                if abs(value - expected) > absolute_tolerance:
                    raise ValueError("direct and reciprocal lattices are inconsistent")


@dataclass(frozen=True, slots=True)
class AtomicSpecies:
    """One ordered species declaration used by a periodic structure.

    Parameters
    ----------
    name
        Nonempty species identifier.
    mass
        Positive finite built-in float. Canonical structures use grams per mole;
        unified atomic mass units are retained only for native version-one records.
    mass_dimension
        Must be :attr:`PhysicalDimension.MASS`.
    mass_unit
        ``"gram_per_mole"`` for canonical structures or
        ``"unified_atomic_mass_unit"`` for retained native version-one records.
    pseudopotential_label
        ``None`` for canonical structure identity. A nonempty source label is retained
        only for the existing schema-version-1 plane-wave record.
    """

    name: str
    mass: float
    mass_dimension: PhysicalDimension
    mass_unit: str
    pseudopotential_label: str | None

    def __post_init__(self) -> None:
        """Validate intrinsic species and transitional compatibility fields."""
        if type(self.name) is not str:
            raise TypeError("species name must be str")
        if not self.name:
            raise ValueError("species name must be nonempty")
        if type(self.mass) is not float:
            raise TypeError("species mass must be a built-in float")
        if not math.isfinite(self.mass) or self.mass <= 0:
            raise ValueError("species mass must be positive and finite")
        if type(self.mass_dimension) is not PhysicalDimension:
            raise TypeError("mass_dimension must be PhysicalDimension")
        if self.mass_dimension is not PhysicalDimension.MASS:
            raise ValueError("species mass dimension must be mass")
        if type(self.mass_unit) is not str:
            raise TypeError("species mass_unit must be str")
        if self.mass_unit not in {"gram_per_mole", "unified_atomic_mass_unit"}:
            raise ValueError("species mass unit is unsupported")
        if self.pseudopotential_label is not None:
            if type(self.pseudopotential_label) is not str:
                raise TypeError("pseudopotential_label must be str or None")
            if not self.pseudopotential_label:
                raise ValueError("pseudopotential_label must be nonempty when present")


@dataclass(frozen=True, slots=True)
class PeriodicSite:
    """One source-ordered Cartesian site in a periodic structure.

    Parameters
    ----------
    index
        Positive one-based built-in integer source index.
    species_name
        Nonempty reference to an owning structure's species declaration.
    coordinates
        Finite Cartesian three-vector. New project-owned structures use angstrom;
        bohr is retained only for native version-one records.
    coordinate_convention
        Must be :attr:`CoordinateConvention.CARTESIAN`.
    coordinate_dimension
        Must be :attr:`PhysicalDimension.LENGTH`.
    coordinate_unit
        :attr:`LengthUnit.ANGSTROM` for canonical structures or
        :attr:`LengthUnit.BOHR` for retained native records.
    """

    index: int
    species_name: str
    coordinates: Vector3
    coordinate_convention: CoordinateConvention
    coordinate_dimension: PhysicalDimension
    coordinate_unit: LengthUnit

    def __post_init__(self) -> None:
        """Validate intrinsic site identity, position, and conventions."""
        if type(self.index) is not int:
            raise TypeError("site index must be a built-in integer")
        if self.index <= 0:
            raise ValueError("site index must be positive")
        if type(self.species_name) is not str:
            raise TypeError("site species_name must be str")
        if not self.species_name:
            raise ValueError("site species_name must be nonempty")
        self._validate_coordinates(self.coordinates)
        if type(self.coordinate_convention) is not CoordinateConvention:
            raise TypeError("coordinate_convention must be CoordinateConvention")
        if type(self.coordinate_dimension) is not PhysicalDimension:
            raise TypeError("coordinate_dimension must be PhysicalDimension")
        if type(self.coordinate_unit) is not LengthUnit:
            raise TypeError("coordinate_unit must be LengthUnit")
        if self.coordinate_convention is not CoordinateConvention.CARTESIAN:
            raise ValueError("site coordinates must be Cartesian")
        if self.coordinate_dimension is not PhysicalDimension.LENGTH:
            raise ValueError("site coordinate dimension must be length")
        if self.coordinate_unit not in {LengthUnit.ANGSTROM, LengthUnit.BOHR}:
            raise ValueError("unsupported Cartesian site coordinate unit")

    @staticmethod
    def _validate_coordinates(coordinates: Vector3) -> None:
        """Validate one exact immutable finite built-in-float three-vector."""
        if type(coordinates) is not tuple:
            raise TypeError("site coordinates must be a tuple")
        if len(coordinates) != 3:
            raise ValueError("site coordinates must contain exactly three components")
        for component in coordinates:
            if type(component) is not float:
                raise TypeError("site coordinates must contain built-in floats")
            if not math.isfinite(component):
                raise ValueError("site coordinates must be finite")


@dataclass(frozen=True, slots=True)
class PeriodicStructure:
    """Direct lattice, ordered species, and ordered sites.

    Parameters
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
        """Validate aggregate types, ordering, uniqueness, and references."""
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
            if site.coordinate_unit is not self.direct_lattice.unit:
                raise ValueError("site and direct-lattice length units must agree")
        if self.direct_lattice.unit_system is UnitSystem.METAL:
            if any(item.mass_unit != "gram_per_mole" for item in self.species):
                raise ValueError("canonical species masses must use grams per mole")
            if any(item.pseudopotential_label is not None for item in self.species):
                raise ValueError(
                    "canonical structure species must not own pseudopotentials"
                )
        else:
            if any(
                item.mass_unit != "unified_atomic_mass_unit" for item in self.species
            ):
                raise ValueError(
                    "native Hartree-atomic species masses must use atomic mass units"
                )
            if any(item.pseudopotential_label is None for item in self.species):
                raise ValueError(
                    "native version-one species require pseudopotential labels"
                )
