"""Compatibility imports for PhysKit-owned finite periodic index domains.

PhysKit owns integer lattice coordinates, finite periodic domains, indexing, and
periodic-image resolution. Legacy ksdft2effmass names remain aliases during the
migration so retained callers do not acquire a second nominal type hierarchy.
"""

from physkit.periodic.lattice.finite_domain import (
    FinitePeriodicCoordinateResolver,
    FinitePeriodicDomain,
    FinitePeriodicDomainIndexer,
    LatticeCoordinate,
    LatticeDimension,
    LatticeDisplacement,
    LatticeIntegerComponents,
    LatticeSiteOrdering,
    PeriodicImageResolver,
    PeriodicImageResult,
)

FiniteLatticeShape = FinitePeriodicDomain
FiniteLatticeIndexer = FinitePeriodicDomainIndexer
FiniteLatticeCoordinateResolver = FinitePeriodicCoordinateResolver

__all__ = [
    "FiniteLatticeCoordinateResolver",
    "FiniteLatticeIndexer",
    "FiniteLatticeShape",
    "FinitePeriodicCoordinateResolver",
    "FinitePeriodicDomain",
    "FinitePeriodicDomainIndexer",
    "LatticeCoordinate",
    "LatticeDimension",
    "LatticeDisplacement",
    "LatticeIntegerComponents",
    "LatticeSiteOrdering",
    "PeriodicImageResolver",
    "PeriodicImageResult",
]
