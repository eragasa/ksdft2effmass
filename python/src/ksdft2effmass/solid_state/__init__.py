"""Public solid-state lattice-model composition contracts.

The package owns reusable finite lattice geometry, boundary twists, reciprocal paths,
plane-wave bases, scalar hopping models, localized perturbations, and exact lattice
operations. Atomic crystal geometry remains in
:mod:`ksdft2effmass.structures.periodic`, general reciprocal weighted sampling remains
in :mod:`ksdft2effmass.electronic_structure`, finite represented matrices remain in
:mod:`ksdft2effmass.operators`, and scientific analysis and campaigns retain their
existing owners.
"""

from .band_frames import (
    PolarBandFrameTransporter1D,
    PolarBandFrameTransportResult1D,
    ReciprocalBandFramePath1D,
)
from .boundary_phases import (
    BoundaryTwistLift,
    BoundaryTwistMesh,
    BoundaryTwistMeshEnumerator,
    BoundaryTwistReducer,
    BoundaryTwistReductionResult,
    BoundaryTwistRepresentative,
    TwistFiber,
    TwistGaugeRepresentation,
)
from .bravais import (
    BravaisCentering,
    BravaisLattice1D,
    BravaisLattice2D,
    BravaisLattice3D,
    BravaisMetricCompatibilityAnalyzer,
    BravaisMetricCompatibilityResult,
    LatticeSystem1D,
    LatticeSystem2D,
    LatticeSystem3D,
)
from .duality import LatticeDualityAnalyzer, LatticeDualityResult
from .frame_alignment import (
    BandFrameAligner1D,
    BandFrameAlignmentResult1D,
    BandProjectorPathConstructor1D,
    BandProjectorPathResult1D,
)
from .gauge_bridges import (
    TwistGaugeBridgeConstructor,
    TwistGaugeBridgeConvention,
    TwistGaugeBridgeResult,
    TwistGaugeEquivalenceAnalyzer,
    TwistGaugeEquivalenceIssueCode,
    TwistGaugeEquivalenceResult,
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
from .hopping_transforms import (
    BandProjectedOperatorPathConstructor1D,
    BlockHoppingInterpolator1D,
    BlockHoppingModel1D,
    BlockHoppingTruncationResult1D,
    BlockHoppingTruncator1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorFourierTransformResult1D,
    ReciprocalOperatorSamples1D,
)
from .lattice_models import (
    LocalizedBondTerm,
    LocalizedOnsiteTerm,
    LocalizedPerturbation,
    ScalarHoppingModel,
    ScalarHoppingTerm,
)
from .lattices import (
    DirectLattice1D,
    DirectLattice2D,
    DirectLattice3D,
    Lattice1D,
    Lattice2D,
    Lattice3D,
    ReciprocalLattice1D,
    ReciprocalLattice2D,
    ReciprocalLattice3D,
    ReciprocalLatticeConvention,
)
from .operator_composition import (
    ScalarFiniteLatticeOperatorAdder,
    ScalarFiniteLatticeOperatorCompatibilityAnalyzer,
    ScalarFiniteLatticeOperatorCompatibilityIssueCode,
    ScalarFiniteLatticeOperatorCompatibilityResult,
)
from .operator_construction import (
    LocalizedPerturbationOperatorConstructor,
    TwistedSupercellOperatorConstructor,
)
from .quotient_seam import QuotientSeamOperatorConstructor
from .reciprocal_paths import (
    CenteredUniformReciprocalMesh1D,
    PlaneWaveBasis1D,
    PlaneWaveReciprocalSewingConstructor,
    PlaneWaveReciprocalSewingResult,
    ReciprocalSewingDirection1D,
)
from .represented_operators import ScalarFiniteLatticeOperator
from .route_reconciliation import (
    ScalarFiniteLatticeRouteReconciliationResult,
    ScalarFiniteLatticeRouteReconciliationWorkflow,
)
from .symmetry import (
    BoundaryTwistTransformer,
    IntegralLatticeOperation,
    LatticeCoordinateTransformer,
    LatticeDisplacementTransformer,
    LatticeOperationCompatibilityAuditor,
    LatticeOperationCompatibilityResult,
)
from .wilson_loops import (
    WilsonCenterConvention1D,
    WilsonLoopPhaseSetComparator1D,
    WilsonLoopPhaseSetComparisonResult1D,
    WilsonLoopSpectrum1D,
    WilsonLoopSpectrumCanonicalizer1D,
)

__all__ = [
    "BoundaryTwistLift",
    "BoundaryTwistMesh",
    "BoundaryTwistMeshEnumerator",
    "BoundaryTwistReducer",
    "BoundaryTwistReductionResult",
    "BoundaryTwistRepresentative",
    "BoundaryTwistTransformer",
    "BandFrameAligner1D",
    "BandFrameAlignmentResult1D",
    "BandProjectedOperatorPathConstructor1D",
    "BandProjectorPathConstructor1D",
    "BandProjectorPathResult1D",
    "BlockHoppingInterpolator1D",
    "BlockHoppingModel1D",
    "BlockHoppingTruncationResult1D",
    "BlockHoppingTruncator1D",
    "BravaisCentering",
    "BravaisLattice1D",
    "BravaisLattice2D",
    "BravaisLattice3D",
    "BravaisMetricCompatibilityAnalyzer",
    "BravaisMetricCompatibilityResult",
    "CenteredUniformReciprocalMesh1D",
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
    "LocalizedPerturbationOperatorConstructor",
    "PeriodicImageResolver",
    "PeriodicImageResult",
    "PlaneWaveBasis1D",
    "PlaneWaveReciprocalSewingConstructor",
    "PlaneWaveReciprocalSewingResult",
    "PolarBandFrameTransporter1D",
    "PolarBandFrameTransportResult1D",
    "ReciprocalBandFramePath1D",
    "ReciprocalLattice1D",
    "ReciprocalLattice2D",
    "ReciprocalLattice3D",
    "ReciprocalLatticeConvention",
    "ReciprocalOperatorFourierTransformer1D",
    "ReciprocalOperatorFourierTransformResult1D",
    "ReciprocalOperatorSamples1D",
    "ReciprocalSewingDirection1D",
    "QuotientSeamOperatorConstructor",
    "ScalarFiniteLatticeOperator",
    "ScalarFiniteLatticeOperatorAdder",
    "ScalarFiniteLatticeOperatorCompatibilityAnalyzer",
    "ScalarFiniteLatticeOperatorCompatibilityIssueCode",
    "ScalarFiniteLatticeOperatorCompatibilityResult",
    "ScalarFiniteLatticeRouteReconciliationResult",
    "ScalarFiniteLatticeRouteReconciliationWorkflow",
    "ScalarHoppingModel",
    "ScalarHoppingTerm",
    "TwistFiber",
    "TwistGaugeBridgeConstructor",
    "TwistGaugeBridgeConvention",
    "TwistGaugeBridgeResult",
    "TwistGaugeEquivalenceAnalyzer",
    "TwistGaugeEquivalenceIssueCode",
    "TwistGaugeEquivalenceResult",
    "TwistGaugeRepresentation",
    "TwistedSupercellOperatorConstructor",
    "WilsonCenterConvention1D",
    "WilsonLoopPhaseSetComparator1D",
    "WilsonLoopPhaseSetComparisonResult1D",
    "WilsonLoopSpectrum1D",
    "WilsonLoopSpectrumCanonicalizer1D",
]
