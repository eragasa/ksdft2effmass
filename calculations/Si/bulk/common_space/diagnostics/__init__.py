"""Bulk-silicon common-space diagnostic composition.

The public surface is deliberately limited to the CSD0/CSD1 producer records, action,
reporter, request decoder, and independently testable mathematical definitions.
"""

from .diagnosis import (
    DEFAULT_REQUEST,
    CommonSpaceDiagnosisRequest,
    CommonSpaceRankDiagnosis,
    HumanReadableProgressReporter,
    KPointDiagnosis,
    NativePrecisionDefinition,
    RetainedDiagnosisComparison,
    StateSpaceDefinition,
    atomic_to_projection_transform,
    gamma_grid,
    read_request,
    singular_value_uncertainty_bound,
)

__all__ = [
    "DEFAULT_REQUEST",
    "CommonSpaceDiagnosisRequest",
    "CommonSpaceRankDiagnosis",
    "HumanReadableProgressReporter",
    "KPointDiagnosis",
    "NativePrecisionDefinition",
    "RetainedDiagnosisComparison",
    "StateSpaceDefinition",
    "atomic_to_projection_transform",
    "gamma_grid",
    "read_request",
    "singular_value_uncertainty_bound",
]
