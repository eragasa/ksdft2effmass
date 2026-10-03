"""Public one-dimensional periodic scientific-model API.

The package owns one-dimensional scientific definitions that compose the general
:mod:`ksdft2effmass.periodic` hierarchy. Campaign execution, encoded documents,
and retained calculation payloads remain outside this package.
"""

from .hopping import (
    Periodic1DCompleteHoppingRepresentationResult,
    Periodic1DFiniteHoppingToyModel,
    Periodic1DFittedHoppingEffectiveModelResult,
    Periodic1DHoppingBlock,
    Periodic1DTruncatedHoppingEffectiveModelResult,
)
from .model import Periodic1DFourierHamiltonianToyModel
from .retention import (
    Periodic1DBandFrameRetainedSubspace,
    Periodic1DOrthogonalSpectralRetainedSubspace,
    Periodic1DRetainedBandGroupDefinition,
    Periodic1DSelectedBandRetentionDefinition,
)

__all__ = [
    "Periodic1DBandFrameRetainedSubspace",
    "Periodic1DCompleteHoppingRepresentationResult",
    "Periodic1DFiniteHoppingToyModel",
    "Periodic1DFittedHoppingEffectiveModelResult",
    "Periodic1DFourierHamiltonianToyModel",
    "Periodic1DHoppingBlock",
    "Periodic1DOrthogonalSpectralRetainedSubspace",
    "Periodic1DRetainedBandGroupDefinition",
    "Periodic1DSelectedBandRetentionDefinition",
    "Periodic1DTruncatedHoppingEffectiveModelResult",
]
