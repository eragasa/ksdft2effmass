"""Abstract scientific sewing categories.

The package preserves distinct sewing problems without defining shared scientific
inputs, outputs, source types, target types, or executable implementations.
"""

from .finite_boundary import FiniteBoundarySewing
from .projected import ProjectedSubspaceSewing
from .reciprocal import (
    EmbeddedPositionReciprocalSewing,
    IdentityReciprocalSewing,
    PermutationPhaseReciprocalSewing,
    PlaneWaveIndexSewing,
)
from .symmetry import SymmetrySewing

__all__ = [
    "EmbeddedPositionReciprocalSewing",
    "FiniteBoundarySewing",
    "IdentityReciprocalSewing",
    "PermutationPhaseReciprocalSewing",
    "PlaneWaveIndexSewing",
    "ProjectedSubspaceSewing",
    "SymmetrySewing",
]
