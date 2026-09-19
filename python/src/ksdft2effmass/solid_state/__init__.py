"""Public solid-state lattice-model composition contracts.

The package owns reusable finite lattice geometry, boundary twists, scalar hopping
models, localized perturbations, and exact lattice operations. Atomic crystal geometry
remains in :mod:`ksdft2effmass.structures.periodic`, reciprocal weighted sampling
remains in :mod:`ksdft2effmass.electronic_structure`, finite represented matrices
remain in :mod:`ksdft2effmass.operators`, and scientific analysis and campaigns retain
their existing owners.
"""

from .boundary_phases import (
    BoundaryTwistLift,
    BoundaryTwistMesh,
    BoundaryTwistMeshEnumerator,
    BoundaryTwistReducer,
    BoundaryTwistReductionResult,
    BoundaryTwistRepresentative,
    TwistGaugeRepresentation,
)
from .bravais_lattices import (
    BravaisCentering,
    BravaisLattice1D,
    BravaisLattice2D,
    BravaisLattice3D,
    DirectLattice1D,
    DirectLattice2D,
    DirectLattice3D,
    Lattice1D,
    Lattice2D,
    Lattice3D,
    LatticeDualityAnalyzer,
    LatticeDualityResult,
    LatticeSystem1D,
    LatticeSystem2D,
    LatticeSystem3D,
    ReciprocalLattice1D,
    ReciprocalLattice2D,
    ReciprocalLattice3D,
    ReciprocalLatticeConvention,
)
from .geometry import (
    FiniteLatticeCoordinateResolver,
    FiniteLatticeIndexer,
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
    LatticeDisplacement,
    LatticeSiteOrdering,
    PeriodicImageResolver,
    PeriodicImageResult,
)
from .lattice_models import (
    LocalizedBondTerm,
    LocalizedOnsiteTerm,
    LocalizedPerturbation,
    ScalarHoppingModel,
    ScalarHoppingTerm,
)
from .symmetry import (
    BoundaryTwistTransformer,
    IntegralLatticeOperation,
    LatticeCoordinateTransformer,
    LatticeDisplacementTransformer,
    LatticeOperationCompatibilityAuditor,
    LatticeOperationCompatibilityResult,
)

__all__ = [
    "BoundaryTwistLift",
    "BoundaryTwistMesh",
    "BoundaryTwistMeshEnumerator",
    "BoundaryTwistReducer",
    "BoundaryTwistReductionResult",
    "BoundaryTwistRepresentative",
    "BoundaryTwistTransformer",
    "BravaisCentering",
    "BravaisLattice1D",
    "BravaisLattice2D",
    "BravaisLattice3D",
    "DirectLattice1D",
    "DirectLattice2D",
    "DirectLattice3D",
    "FiniteLatticeCoordinateResolver",
    "FiniteLatticeIndexer",
    "FiniteLatticeShape",
    "IntegralLatticeOperation",
    "Lattice1D",
    "Lattice2D",
    "Lattice3D",
    "LatticeCoordinate",
    "LatticeCoordinateTransformer",
    "LatticeDimension",
    "LatticeDisplacement",
    "LatticeDisplacementTransformer",
    "LatticeDualityAnalyzer",
    "LatticeDualityResult",
    "LatticeOperationCompatibilityAuditor",
    "LatticeOperationCompatibilityResult",
    "LatticeSiteOrdering",
    "LatticeSystem1D",
    "LatticeSystem2D",
    "LatticeSystem3D",
    "LocalizedBondTerm",
    "LocalizedOnsiteTerm",
    "LocalizedPerturbation",
    "PeriodicImageResolver",
    "PeriodicImageResult",
    "ReciprocalLattice1D",
    "ReciprocalLattice2D",
    "ReciprocalLattice3D",
    "ReciprocalLatticeConvention",
    "ScalarHoppingModel",
    "ScalarHoppingTerm",
    "TwistGaugeRepresentation",
]
