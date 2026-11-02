"""Immutable result records for band-equivalence locality analysis."""

from .case import (
    AmplitudeMidpointDiagnostic,
    CaseDiagnostic,
    FlatAmplitudeResolutionDiagnostic,
)
from .channels import ErrorChannels
from .diagnostics import (
    BandEquivalenceHoppingLocalityDiagnostics,
    BandEquivalenceHoppingLocalityVerificationDiagnostics,
)
from .loss import BandEquivalenceHoppingLocalityLossRecord
from .point import PointDiagnostic
from .refinement import (
    BandEquivalenceHoppingLocalityRefinementAssessmentRecord,
    BandEquivalenceHoppingLocalityRefinementPairRecord,
)
from .shell import FirstPassingDecision, ShellDiagnostic

__all__ = [
    "AmplitudeMidpointDiagnostic",
    "BandEquivalenceHoppingLocalityDiagnostics",
    "BandEquivalenceHoppingLocalityLossRecord",
    "BandEquivalenceHoppingLocalityRefinementAssessmentRecord",
    "BandEquivalenceHoppingLocalityRefinementPairRecord",
    "BandEquivalenceHoppingLocalityVerificationDiagnostics",
    "CaseDiagnostic",
    "ErrorChannels",
    "FirstPassingDecision",
    "FlatAmplitudeResolutionDiagnostic",
    "PointDiagnostic",
    "ShellDiagnostic",
]
