"""Plain immutable scientific results for band-equivalence locality analysis."""

from .case import (
    BandEquivalenceHoppingLocalityAmplitudeMidpointAnalysis,
    BandEquivalenceHoppingLocalityCaseAnalysis,
    BandEquivalenceHoppingLocalityFlatAmplitudeResolutionAnalysis,
)
from .channels import BandEquivalenceHoppingLocalityErrorChannels
from .point import (
    BandEquivalenceHoppingLocalityPointAnalysis,
    BandEquivalenceHoppingLocalityRepresentationEquivalenceAnalysis,
)
from .shell import (
    BandEquivalenceHoppingLocalityFirstPassingDecision,
    BandEquivalenceHoppingLocalityShellAnalysis,
)

__all__ = [
    "BandEquivalenceHoppingLocalityAmplitudeMidpointAnalysis",
    "BandEquivalenceHoppingLocalityCaseAnalysis",
    "BandEquivalenceHoppingLocalityErrorChannels",
    "BandEquivalenceHoppingLocalityFirstPassingDecision",
    "BandEquivalenceHoppingLocalityFlatAmplitudeResolutionAnalysis",
    "BandEquivalenceHoppingLocalityPointAnalysis",
    "BandEquivalenceHoppingLocalityRepresentationEquivalenceAnalysis",
    "BandEquivalenceHoppingLocalityShellAnalysis",
]
