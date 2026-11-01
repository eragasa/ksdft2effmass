"""Rank-two irreversible support-removal capability.

This capability namespace exposes the existing rank-two truncation owners without
changing class identity or retained wire formats.
"""

from ...band_equivalence_locality.embedded_subspace.rank2.truncation import (
    EmbeddedSubspaceRank2TruncationFamilyVerification,
    EmbeddedSubspaceRank2TruncationVerification,
    Periodic1DRank2TruncationFamilyIndependentVerifier,
    Periodic1DRank2TruncationIndependentReferenceAnalyzer,
    Periodic1DRank2TruncationIndependentVerifier,
    Periodic1DRank2TruncationMeshStabilityAssessment,
    Periodic1DRank2TruncationToleranceSelectionIndependentReference,
    Periodic1DRank2TruncationToleranceSelectionIndependentReferenceAnalyzer,
)
from .analysis import (
    Periodic1DRank2SupportTruncationAnalysisRequest,
    Periodic1DRank2SupportTruncationAnalyzer,
    Periodic1DRank2TruncationAnalyzer,
    Periodic1DRank2TruncationFamilyAnalysis,
    Periodic1DRank2TruncationFamilyAnalyzer,
    Periodic1DRank2TruncationFamilyRequest,
    Periodic1DRank2TruncationRequest,
    Periodic1DRank2TruncationToleranceSelector,
)
from .result import (
    Periodic1DRank2SupportTruncationAnalysis,
    Periodic1DRank2TruncationAnalysis,
    Periodic1DRank2TruncationCompleted,
    Periodic1DRank2TruncationPoint,
    Periodic1DRank2TruncationQualificationStopped,
    Periodic1DRank2TruncationRange,
)

__all__ = [
    "EmbeddedSubspaceRank2TruncationFamilyVerification",
    "EmbeddedSubspaceRank2TruncationVerification",
    "Periodic1DRank2SupportTruncationAnalysis",
    "Periodic1DRank2SupportTruncationAnalysisRequest",
    "Periodic1DRank2SupportTruncationAnalyzer",
    "Periodic1DRank2TruncationAnalysis",
    "Periodic1DRank2TruncationAnalyzer",
    "Periodic1DRank2TruncationCompleted",
    "Periodic1DRank2TruncationFamilyAnalysis",
    "Periodic1DRank2TruncationFamilyAnalyzer",
    "Periodic1DRank2TruncationFamilyIndependentVerifier",
    "Periodic1DRank2TruncationFamilyRequest",
    "Periodic1DRank2TruncationIndependentReferenceAnalyzer",
    "Periodic1DRank2TruncationIndependentVerifier",
    "Periodic1DRank2TruncationMeshStabilityAssessment",
    "Periodic1DRank2TruncationPoint",
    "Periodic1DRank2TruncationQualificationStopped",
    "Periodic1DRank2TruncationRange",
    "Periodic1DRank2TruncationRequest",
    "Periodic1DRank2TruncationToleranceSelector",
    "Periodic1DRank2TruncationToleranceSelectionIndependentReference",
    "Periodic1DRank2TruncationToleranceSelectionIndependentReferenceAnalyzer",
]
