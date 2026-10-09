"""Public one-dimensional periodic scientific-model API.

The package owns one-dimensional scientific definitions that compose the general
:mod:`ksdft2effmass.periodic` hierarchy. The :mod:`ksdft2effmass.periodic1d.campaign`
subpackage separately owns campaign records and operations; those records do not
become scientific models merely by sharing this dimensional namespace.
"""

from .fibers import Periodic1DFiberHamiltonianRequest
from .finite_differences import (
    PeriodicFiniteDifferenceFiberHamiltonian1DConstructor,
    PeriodicFiniteDifferenceFiberHamiltonian1DResult,
    PeriodicUniformGrid1D,
)
from .hopping import (
    Periodic1DCompleteHoppingRepresentationResult,
    Periodic1DFiniteHoppingToyModel,
    Periodic1DFittedHoppingEffectiveModelResult,
    Periodic1DHoppingBlock,
    Periodic1DTruncatedHoppingEffectiveModelResult,
)
from .model import (
    Periodic1DFourierHamiltonianToyModel,
    Periodic1DPlaneWaveParentRepresentation,
    Periodic1DPlaneWaveParentRepresentationConstructor,
)
from .plane_waves import (
    PlaneWaveFiberHamiltonian1DConstructor,
    PlaneWaveFiberHamiltonian1DResult,
)
from .representations import (
    Periodic1DRetainedOperatorHoppingRepresentation,
    Periodic1DRetainedOperatorReciprocalRepresentation,
)
from .retention import (
    Periodic1DBandFrameRetainedSubspace,
    Periodic1DOrthogonalSpectralRetainedSubspace,
    Periodic1DRetainedBandGroupDefinition,
    Periodic1DSelectedBandRetentionDefinition,
)
from .supercell_operators import (
    Periodic1DSupercellOperatorConstructor,
    Periodic1DSupercellOperatorMetadata,
    Periodic1DSupercellOperatorProvenance,
)

__all__ = [
    "Periodic1DBandFrameRetainedSubspace",
    "Periodic1DFiberHamiltonianRequest",
    "Periodic1DCompleteHoppingRepresentationResult",
    "Periodic1DRetainedOperatorHoppingRepresentation",
    "Periodic1DFiniteHoppingToyModel",
    "Periodic1DFittedHoppingEffectiveModelResult",
    "Periodic1DFourierHamiltonianToyModel",
    "Periodic1DHoppingBlock",
    "Periodic1DOrthogonalSpectralRetainedSubspace",
    "Periodic1DPlaneWaveParentRepresentation",
    "Periodic1DPlaneWaveParentRepresentationConstructor",
    "Periodic1DRetainedOperatorReciprocalRepresentation",
    "Periodic1DRetainedBandGroupDefinition",
    "Periodic1DSelectedBandRetentionDefinition",
    "Periodic1DSupercellOperatorConstructor",
    "Periodic1DSupercellOperatorMetadata",
    "Periodic1DSupercellOperatorProvenance",
    "Periodic1DTruncatedHoppingEffectiveModelResult",
    "PeriodicFiniteDifferenceFiberHamiltonian1DConstructor",
    "PeriodicFiniteDifferenceFiberHamiltonian1DResult",
    "PeriodicUniformGrid1D",
    "PlaneWaveFiberHamiltonian1DConstructor",
    "PlaneWaveFiberHamiltonian1DResult",
]
