"""Immutable scalar hopping models and localized lattice perturbations.

These records describe reduced scalar lattice Hamiltonian data independently of atomic
crystal structures, DFT provenance, model-class fitting, or scientific acceptance.
Energy units use the Pint-backed operator unit records, and every model retains an
explicit energy-reference identity.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from ksdft2effmass.operators import PhysicalUnit, Unitless

from .geometry import LatticeCoordinate, LatticeDimension, LatticeDisplacement

type SolidStateUnit = PhysicalUnit | Unitless
"""Explicit physical or dimensionless unit admitted by solid-state records."""


@dataclass(frozen=True, slots=True)
class ScalarHoppingTerm:
    """Represent one scalar translation-invariant hopping coefficient.

    Parameters
    ----------
    displacement
        Integer primitive-cell displacement from row cell to column cell.
    real
        Finite built-in-float real part of the coefficient.
    imaginary
        Finite built-in-float imaginary part of the coefficient.
    """

    displacement: LatticeDisplacement
    real: float
    imaginary: float

    def __post_init__(self) -> None:
        """Validate displacement and finite binary64 components."""
        if type(self.displacement) is not LatticeDisplacement:
            raise TypeError("displacement must be LatticeDisplacement")
        if type(self.real) is not float or type(self.imaginary) is not float:
            raise TypeError("hopping components must be built-in floats")
        if not math.isfinite(self.real) or not math.isfinite(self.imaginary):
            raise ValueError("hopping components must be finite")

    @property
    def value(self) -> complex:
        """Return the represented built-in complex coefficient."""
        return complex(self.real, self.imaginary)


@dataclass(frozen=True, slots=True)
class ScalarHoppingModel:
    """Represent one ordered scalar translation-invariant lattice Hamiltonian.

    Parameters
    ----------
    identifier
        Nonempty model identity.
    dimension
        Exact supported spatial dimension.
    terms
        Nonempty hopping terms sorted lexicographically by displacement with no
        duplicates. Hermiticity is not inferred by construction.
    energy_unit
        Explicit Pint-backed physical or dimensionless unit shared by every term.
    energy_reference
        Nonempty identity for the common energy zero.
    basis_identifier
        Nonempty identity for the scalar primitive-cell basis.
    """

    identifier: str
    dimension: LatticeDimension
    terms: tuple[ScalarHoppingTerm, ...]
    energy_unit: SolidStateUnit
    energy_reference: str
    basis_identifier: str

    def __post_init__(self) -> None:
        """Validate intrinsic identity, dimensional, ordering, and unit invariants."""
        for value, name in (
            (self.identifier, "identifier"),
            (self.energy_reference, "energy_reference"),
            (self.basis_identifier, "basis_identifier"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if type(self.dimension) is not LatticeDimension:
            raise TypeError("dimension must be LatticeDimension")
        if type(self.terms) is not tuple:
            raise TypeError("terms must be a tuple")
        if not self.terms:
            raise ValueError("terms must be nonempty")
        if any(type(term) is not ScalarHoppingTerm for term in self.terms):
            raise TypeError("terms must contain ScalarHoppingTerm values")
        if any(
            term.displacement.dimension is not self.dimension for term in self.terms
        ):
            raise ValueError("term dimensions must match model dimension")
        displacements = tuple(term.displacement.components for term in self.terms)
        if displacements != tuple(sorted(set(displacements))):
            raise ValueError("term displacements must be sorted and unique")
        if not isinstance(self.energy_unit, PhysicalUnit | Unitless):
            raise TypeError("energy_unit must be PhysicalUnit or Unitless")


@dataclass(frozen=True, slots=True)
class LocalizedOnsiteTerm:
    """Represent one scalar localized onsite coefficient.

    Parameters
    ----------
    site
        Integer lattice site relative to an explicitly identified defect origin.
    real
        Finite built-in-float real part.
    imaginary
        Finite built-in-float imaginary part. Hermitian onsite perturbations require
        this value to be zero, but this structural record does not impose that policy.
    """

    site: LatticeCoordinate
    real: float
    imaginary: float

    def __post_init__(self) -> None:
        """Validate site and finite coefficient components."""
        if type(self.site) is not LatticeCoordinate:
            raise TypeError("site must be LatticeCoordinate")
        if type(self.real) is not float or type(self.imaginary) is not float:
            raise TypeError("onsite components must be built-in floats")
        if not math.isfinite(self.real) or not math.isfinite(self.imaginary):
            raise ValueError("onsite components must be finite")

    @property
    def value(self) -> complex:
        """Return the represented built-in complex coefficient."""
        return complex(self.real, self.imaginary)


@dataclass(frozen=True, slots=True)
class LocalizedBondTerm:
    """Represent one directed localized scalar bond coefficient.

    Parameters
    ----------
    start
        Integer start site relative to the defect origin.
    displacement
        Nonzero integer displacement from start to target.
    real
        Finite built-in-float real part.
    imaginary
        Finite built-in-float imaginary part.
    """

    start: LatticeCoordinate
    displacement: LatticeDisplacement
    real: float
    imaginary: float

    def __post_init__(self) -> None:
        """Validate dimensions, nonzero displacement, and finite coefficient."""
        if type(self.start) is not LatticeCoordinate:
            raise TypeError("start must be LatticeCoordinate")
        if type(self.displacement) is not LatticeDisplacement:
            raise TypeError("displacement must be LatticeDisplacement")
        if self.start.dimension is not self.displacement.dimension:
            raise ValueError("start and displacement dimensions must agree")
        if self.displacement.is_zero:
            raise ValueError("bond displacement must be nonzero")
        if type(self.real) is not float or type(self.imaginary) is not float:
            raise TypeError("bond components must be built-in floats")
        if not math.isfinite(self.real) or not math.isfinite(self.imaginary):
            raise ValueError("bond components must be finite")

    @property
    def value(self) -> complex:
        """Return the represented built-in complex coefficient."""
        return complex(self.real, self.imaginary)


type LocalizedTerm = LocalizedOnsiteTerm | LocalizedBondTerm
"""Closed scalar localized-term union."""


@dataclass(frozen=True, slots=True)
class LocalizedPerturbation:
    """Represent one deterministic finite localized scalar perturbation.

    Parameters
    ----------
    identifier
        Nonempty perturbation identity.
    dimension
        Exact supported spatial dimension.
    terms
        Nonempty tuple of onsite and directed bond terms. Terms must be in canonical
        order: onsite terms first by site, then bond terms by start and displacement.
        Duplicate represented terms are rejected.
    energy_unit
        Explicit Pint-backed unit shared by every coefficient.
    energy_reference
        Nonempty identity for the common energy zero.
    basis_identifier
        Nonempty scalar basis identity.
    """

    identifier: str
    dimension: LatticeDimension
    terms: tuple[LocalizedTerm, ...]
    energy_unit: SolidStateUnit
    energy_reference: str
    basis_identifier: str

    def __post_init__(self) -> None:
        """Validate identity, dimensional compatibility, canonical order, and unit."""
        for value, name in (
            (self.identifier, "identifier"),
            (self.energy_reference, "energy_reference"),
            (self.basis_identifier, "basis_identifier"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if type(self.dimension) is not LatticeDimension:
            raise TypeError("dimension must be LatticeDimension")
        if type(self.terms) is not tuple:
            raise TypeError("terms must be a tuple")
        if not self.terms:
            raise ValueError("terms must be nonempty")
        keys: list[tuple[int, ...]] = []
        for term in self.terms:
            if type(term) is LocalizedOnsiteTerm:
                if term.site.dimension is not self.dimension:
                    raise ValueError("onsite term dimension must match perturbation")
                keys.append((0, *term.site.components))
            elif type(term) is LocalizedBondTerm:
                if term.start.dimension is not self.dimension:
                    raise ValueError("bond term dimension must match perturbation")
                keys.append((1, *term.start.components, *term.displacement.components))
            else:
                raise TypeError("terms must contain supported localized term values")
        if tuple(keys) != tuple(sorted(set(keys))):
            raise ValueError("localized terms must be canonically sorted and unique")
        if not isinstance(self.energy_unit, PhysicalUnit | Unitless):
            raise TypeError("energy_unit must be PhysicalUnit or Unitless")
