"""Irreversible truncation of represented real-space operator support."""

from .base import RealSpaceSupportTruncation
from .geometry import BasisResolvedMetricGeometry, MetricGeometry
from .metric_shells import (
    MetricShellClassification,
    MetricShellSupportClassifier,
    MetricShellValueAnalysis,
    MetricShellValueAnalyzer,
)
from .support import (
    ConjugateClosedSupport,
    MetricShellSupportInventory,
    SymmetricRangeSupport1D,
)
from .tolerance_selection import (
    MinimumToleranceSatisfyingSupport,
    OrderedEigenvalueErrors,
    RankNormalizedMatrixFrobeniusErrors,
    RealSpaceSupportTruncationComparison,
    RealSpaceSupportTruncationErrors,
    RealSpaceSupportTruncationModelToleranceSelection,
    RealSpaceSupportTruncationToleranceSelection,
    RealSpaceSupportTruncationToleranceSelectionRequest,
    RealSpaceSupportTruncationToleranceSelector,
    SupportToleranceSelectionOutcome,
    SupportToleranceUnresolved,
)

__all__ = [
    "BasisResolvedMetricGeometry",
    "ConjugateClosedSupport",
    "MetricGeometry",
    "MetricShellClassification",
    "MetricShellSupportClassifier",
    "MetricShellSupportInventory",
    "MetricShellValueAnalysis",
    "MetricShellValueAnalyzer",
    "MinimumToleranceSatisfyingSupport",
    "OrderedEigenvalueErrors",
    "RankNormalizedMatrixFrobeniusErrors",
    "RealSpaceSupportTruncation",
    "RealSpaceSupportTruncationComparison",
    "RealSpaceSupportTruncationErrors",
    "RealSpaceSupportTruncationModelToleranceSelection",
    "RealSpaceSupportTruncationToleranceSelection",
    "RealSpaceSupportTruncationToleranceSelectionRequest",
    "RealSpaceSupportTruncationToleranceSelector",
    "SupportToleranceSelectionOutcome",
    "SupportToleranceUnresolved",
    "SymmetricRangeSupport1D",
]
