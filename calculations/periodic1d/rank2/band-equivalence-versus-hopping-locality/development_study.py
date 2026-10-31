"""Maintained development-study composition over installed scientific owners.

This module binds the calculation's historical finite controls to the installed
``ksdft2effmass.periodic1d`` request, analyzer, and independent-verification
boundaries.  It does not define a competing scientific implementation or a retained
execution identity.
"""

from __future__ import annotations

from ksdft2effmass.periodic1d import (
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalyzer,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeConverged,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeEvaluationsExhausted,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeIndependentVerifier,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeLevelsExhausted,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeQualificationStopped,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest,
    Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel,
    Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementThresholds,
    Periodic1DEmbeddedSubspaceRank2Analysis,
    Periodic1DEmbeddedSubspaceRank2AnalysisRecord,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalysis,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalyzer,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementIndependentVerifier,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysis,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysisRecord,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalyzer,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyRequest,
    Periodic1DEmbeddedSubspaceRank2ParentFamilyVerifier,
    Periodic1DEmbeddedSubspaceRank2QualifiedParent,
    Periodic1DEmbeddedSubspaceRank2Request,
    Periodic1DEmbeddedSubspaceRank2TruncationAnalysis,
    Periodic1DEmbeddedSubspaceRank2TruncationAnalyzer,
    Periodic1DEmbeddedSubspaceRank2TruncationCompleted,
    Periodic1DEmbeddedSubspaceRank2TruncationIndependentVerifier,
    Periodic1DEmbeddedSubspaceRank2TruncationRequest,
    Periodic1DEmbeddedSubspaceRank2Verifier,
)
from ksdft2effmass.verification import CompositeVerification
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)


def embedded_rank2_request(
    *,
    reciprocal_mesh_size: int,
    amplitudes: tuple[float, ...],
    parent_hopping_scale: float,
) -> Periodic1DEmbeddedSubspaceRank2Request:
    """Bind one historical development grid to the installed rank-two request."""
    return Periodic1DEmbeddedSubspaceRank2Request(
        reciprocal_mesh_size=reciprocal_mesh_size,
        amplitudes=amplitudes,
        parent_hopping_scale=parent_hopping_scale,
        minimum_external_gap=1.0,
        minimum_transport_singular_value=0.99,
        frame_absolute_tolerance=1.0e-10,
        transport_rank_relative_tolerance=1.0e-12,
        transport_validation_relative_tolerance=1.0e-10,
        harmonic_absolute_degeneracy_tolerance=1.0e-14,
        harmonic_relative_degeneracy_tolerance=1.0e-13,
    )


def amplitude_refinement_levels(
    analysis: Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis,
) -> tuple[Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel, ...]:
    """Project levels from the closed adaptive outcome without widening variants."""
    if (
        type(analysis)
        is Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeQualificationStopped
    ):
        return ()
    if type(analysis) is Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeConverged:
        return analysis.levels
    if (
        type(analysis)
        is Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeEvaluationsExhausted
    ):
        return analysis.levels
    if (
        type(analysis)
        is Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeLevelsExhausted
    ):
        return analysis.levels
    raise TypeError("analysis must be a closed adaptive-amplitude outcome")


def analysis_verification_defect(
    analysis: Periodic1DEmbeddedSubspaceRank2Analysis,
) -> float:
    """Authenticate and independently compare one installed mesh analysis."""
    if type(analysis) is not Periodic1DEmbeddedSubspaceRank2Analysis:
        raise TypeError("analysis must be an installed rank-two analysis")
    verification = Periodic1DEmbeddedSubspaceRank2Verifier(
        Periodic1DEmbeddedSubspaceRank2AnalysisRecord(analysis).to_json()
    ).result()
    if not verification.passed:
        raise ValueError("installed independent mesh verification failed")
    return max(
        float(observation.value.magnitude)
        for component in verification.components
        for observation in component.observations.values()
    )


def adaptive_amplitude(
    *,
    reciprocal_mesh_size: int,
    initial_amplitudes: tuple[float, ...],
    parent_hopping_scale: float,
    draft_tolerance: float,
    maximum_refinement_levels: int,
    maximum_evaluated_amplitudes: int,
) -> Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis:
    """Calculate and independently verify one installed adaptive-amplitude study."""
    analysis = Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalyzer(
        request=Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeRequest(
            template_request=embedded_rank2_request(
                reciprocal_mesh_size=reciprocal_mesh_size,
                amplitudes=initial_amplitudes,
                parent_hopping_scale=parent_hopping_scale,
            ),
            thresholds=Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementThresholds(
                maximum_correlation_defect=draft_tolerance,
                maximum_operator_threshold_defect=draft_tolerance,
                maximum_joint_threshold_defect=draft_tolerance,
                maximum_hopping_weight_defect=draft_tolerance,
                maximum_hopping_power_defect=draft_tolerance,
            ),
            maximum_refinement_levels=maximum_refinement_levels,
            maximum_evaluated_amplitudes=maximum_evaluated_amplitudes,
        ),
        transporter=ClosedLoopPolarFrameTransporter(),
    ).execute()
    verification = Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeIndependentVerifier(
        analysis
    ).result()
    if not verification.passed:
        raise ValueError("installed independent amplitude verification failed")
    return analysis


def momentum_refinement(
    *,
    reciprocal_mesh_sizes: tuple[int, ...],
    amplitudes: tuple[float, ...],
    parent_hopping_scale: float,
    draft_tolerance: float,
    required_stable_refinements: int = 2,
) -> Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalysis:
    """Calculate and independently verify one installed nested-momentum study."""
    template = embedded_rank2_request(
        reciprocal_mesh_size=reciprocal_mesh_sizes[0],
        amplitudes=amplitudes,
        parent_hopping_scale=parent_hopping_scale,
    )
    thresholds = Periodic1DEmbeddedSubspaceRank2MomentumRefinementThresholds(
        maximum_parent_diagnostic_change=draft_tolerance,
        maximum_correlation_change=draft_tolerance,
        maximum_threshold_change=draft_tolerance,
        maximum_hopping_weight_change=draft_tolerance,
        maximum_hopping_power_change=draft_tolerance,
        maximum_angle_change=draft_tolerance,
        maximum_band_defect=draft_tolerance,
        maximum_reconstruction_defect=draft_tolerance,
        maximum_parseval_defect=draft_tolerance,
    )
    analysis = Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalyzer(
        request=Periodic1DEmbeddedSubspaceRank2MomentumRefinementRequest(
            template_request=template,
            reciprocal_mesh_sizes=reciprocal_mesh_sizes,
            thresholds=thresholds,
            required_stable_refinements=required_stable_refinements,
        ),
        transporter=ClosedLoopPolarFrameTransporter(),
    ).execute()
    verification = Periodic1DEmbeddedSubspaceRank2MomentumRefinementIndependentVerifier(
        analysis
    ).result()
    if not verification.passed:
        raise ValueError("installed independent momentum verification failed")
    return analysis


def qualified_parent(
    analysis: Periodic1DEmbeddedSubspaceRank2Analysis,
) -> Periodic1DEmbeddedSubspaceRank2QualifiedParent:
    """Require and return the installed qualified-parent outcome."""
    if type(analysis) is not Periodic1DEmbeddedSubspaceRank2Analysis:
        raise TypeError("analysis must be an installed rank-two analysis")
    if (
        type(analysis.qualification)
        is not Periodic1DEmbeddedSubspaceRank2QualifiedParent
    ):
        raise ValueError("development study requires a qualified parent")
    return analysis.qualification


def parent_family(
    *,
    reciprocal_mesh_size: int,
    amplitudes: tuple[float, ...],
    parent_hopping_scales: tuple[float, ...],
) -> Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysis:
    """Calculate one five-scale family through the installed family owner."""
    template = embedded_rank2_request(
        reciprocal_mesh_size=reciprocal_mesh_size,
        amplitudes=amplitudes,
        parent_hopping_scale=parent_hopping_scales[-1],
    )
    analysis = Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalyzer(
        request=Periodic1DEmbeddedSubspaceRank2ParentFamilyRequest(
            template_request=template,
            parent_hopping_scales=parent_hopping_scales,
        ),
        transporter=ClosedLoopPolarFrameTransporter(),
    ).execute()
    verification = Periodic1DEmbeddedSubspaceRank2ParentFamilyVerifier(
        Periodic1DEmbeddedSubspaceRank2ParentFamilyAnalysisRecord(analysis).to_json()
    ).result()
    if not verification.passed:
        raise ValueError("installed independent parent-family verification failed")
    return analysis


def completed_truncation(
    analysis: Periodic1DEmbeddedSubspaceRank2TruncationAnalysis,
) -> Periodic1DEmbeddedSubspaceRank2TruncationCompleted:
    """Require and return the installed completed-truncation outcome."""
    if type(analysis) is not Periodic1DEmbeddedSubspaceRank2TruncationCompleted:
        raise ValueError("development study requires completed truncation")
    return analysis


def truncation_verification_defect(
    analysis: Periodic1DEmbeddedSubspaceRank2TruncationAnalysis,
) -> float:
    """Return the largest installed independent truncation discrepancy."""
    verification = Periodic1DEmbeddedSubspaceRank2TruncationIndependentVerifier(
        analysis
    ).result()
    if not verification.passed:
        raise ValueError("installed independent truncation verification failed")
    return maximum_verification_defect(verification)


def truncation_analysis(
    *,
    construction_mesh_size: int,
    evaluation_mesh_size: int,
    amplitudes: tuple[float, ...],
    parent_hopping_scale: float,
    maximum_range: int,
) -> Periodic1DEmbeddedSubspaceRank2TruncationAnalysis:
    """Calculate and independently verify one dense installed truncation inventory."""
    template = embedded_rank2_request(
        reciprocal_mesh_size=construction_mesh_size,
        amplitudes=amplitudes,
        parent_hopping_scale=parent_hopping_scale,
    )
    analysis = Periodic1DEmbeddedSubspaceRank2TruncationAnalyzer(
        request=Periodic1DEmbeddedSubspaceRank2TruncationRequest.every_integer_through(
            template_request=template,
            maximum_range=maximum_range,
            evaluation_mesh_size=evaluation_mesh_size,
        ),
        transporter=ClosedLoopPolarFrameTransporter(),
    ).execute()
    truncation_verification_defect(analysis)
    return analysis


def maximum_verification_defect(verification: CompositeVerification) -> float:
    """Return the largest independently observed discrepancy in one comparison."""
    return max(
        float(observation.value.magnitude)
        for observation in verification.observations.values()
    )


__all__ = [
    "adaptive_amplitude",
    "amplitude_refinement_levels",
    "analysis_verification_defect",
    "completed_truncation",
    "embedded_rank2_request",
    "maximum_verification_defect",
    "momentum_refinement",
    "parent_family",
    "qualified_parent",
    "truncation_analysis",
    "truncation_verification_defect",
]
