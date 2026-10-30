"""Immutable result records for band-equivalence locality analysis."""

from .case import (
    AmplitudeMidpointDiagnostic,
    CaseDiagnostic,
    FlatAmplitudeResolutionDiagnostic,
)
from .channels import ErrorChannels
from .diagnostics import (
    BandEquivalenceLocalityDiagnostics,
    BandEquivalenceLocalityVerificationDiagnostics,
)
from .point import PointDiagnostic
from .refinement import (
    BandEquivalenceLocalityRefinementAssessmentRecord,
    BandEquivalenceLocalityRefinementPairRecord,
)
from .shell import FirstPassingDecision, ShellDiagnostic

__all__ = [
    "AmplitudeMidpointDiagnostic",
    "BandEquivalenceLocalityDiagnostics",
    "BandEquivalenceLocalityRefinementAssessmentRecord",
    "BandEquivalenceLocalityRefinementPairRecord",
    "BandEquivalenceLocalityVerificationDiagnostics",
    "CaseDiagnostic",
    "ErrorChannels",
    "FirstPassingDecision",
    "FlatAmplitudeResolutionDiagnostic",
    "PointDiagnostic",
    "ShellDiagnostic",
]
