"""Calculation-local rank-two control analysis over installed scientific owners.

This non-entrypoint module binds the calculation's historical finite controls to the
installed rank-two request, analyzer, and independent-verification package boundaries.
The numbered ``run_10`` through ``run_14`` scripts compose it in execution order. It
does not define a competing scientific implementation or a retained execution identity.
"""

from __future__ import annotations

from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.amplitude_refinement.analysis import (  # noqa: E501
    Periodic1DRank2AdaptiveAmplitudeAnalysis,
    Periodic1DRank2AdaptiveAmplitudeAnalyzer,
    Periodic1DRank2AdaptiveAmplitudeConverged,
    Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted,
    Periodic1DRank2AdaptiveAmplitudeLevelsExhausted,
    Periodic1DRank2AdaptiveAmplitudeQualificationStopped,
    Periodic1DRank2AdaptiveAmplitudeRequest,
    Periodic1DRank2AmplitudeRefinementLevel,
    Periodic1DRank2AmplitudeRefinementThresholds,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.amplitude_refinement.verification import (  # noqa: E501
    Periodic1DRank2AdaptiveAmplitudeIndependentVerifier,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.momentum_refinement.analysis import (  # noqa: E501
    Periodic1DRank2MomentumRefinementAnalysis,
    Periodic1DRank2MomentumRefinementAnalyzer,
    Periodic1DRank2MomentumRefinementRequest,
    Periodic1DRank2MomentumRefinementThresholds,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.momentum_refinement.verification import (  # noqa: E501
    Periodic1DRank2MomentumRefinementIndependentVerifier,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_family.analysis import (  # noqa: E501
    Periodic1DRank2ParentFamilyAnalysis,
    Periodic1DRank2ParentFamilyAnalyzer,
    Periodic1DRank2ParentFamilyRequest,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_scale.request import (  # noqa: E501
    Periodic1DRank2Request,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_scale.results import (  # noqa: E501
    Periodic1DRank2Analysis,
    Periodic1DRank2QualifiedParent,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.retention.records import (  # noqa: E501
    Periodic1DRank2AnalysisRecord,
    Periodic1DRank2ParentFamilyAnalysisRecord,
)
from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.retention.verification import (  # noqa: E501
    Periodic1DRank2ParentFamilyVerifier,
    Periodic1DRank2Verifier,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.analysis import (
    Periodic1DRank2TruncationAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.request import (
    Periodic1DRank2TruncationRequest,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.results import (
    Periodic1DRank2TruncationAnalysis,
    Periodic1DRank2TruncationCompleted,
)
from ksdft2effmass.periodic1d.rank2.support_truncation.verification import (
    Periodic1DRank2TruncationIndependentVerifier,
)
from ksdft2effmass.verification import CompositeVerification


def embedded_rank2_request(
    *,
    reciprocal_mesh_size: int,
    amplitudes: tuple[float, ...],
    parent_hopping_scale: float,
) -> Periodic1DRank2Request:
    """Bind one historical development grid to the installed rank-two request."""
    return Periodic1DRank2Request(
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
    analysis: Periodic1DRank2AdaptiveAmplitudeAnalysis,
) -> tuple[Periodic1DRank2AmplitudeRefinementLevel, ...]:
    """Project levels from the closed adaptive outcome without widening variants."""
    if type(analysis) is Periodic1DRank2AdaptiveAmplitudeQualificationStopped:
        return ()
    if type(analysis) is Periodic1DRank2AdaptiveAmplitudeConverged:
        return analysis.levels
    if type(analysis) is Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted:
        return analysis.levels
    if type(analysis) is Periodic1DRank2AdaptiveAmplitudeLevelsExhausted:
        return analysis.levels
    raise TypeError("analysis must be a closed adaptive-amplitude outcome")


def analysis_verification_defect(
    analysis: Periodic1DRank2Analysis,
) -> float:
    """Authenticate and independently compare one installed mesh analysis."""
    if type(analysis) is not Periodic1DRank2Analysis:
        raise TypeError("analysis must be an installed rank-two analysis")
    verification = Periodic1DRank2Verifier(
        Periodic1DRank2AnalysisRecord(analysis).to_json()
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
) -> Periodic1DRank2AdaptiveAmplitudeAnalysis:
    """Calculate and independently verify one installed adaptive-amplitude study."""
    analysis = Periodic1DRank2AdaptiveAmplitudeAnalyzer(
        request=Periodic1DRank2AdaptiveAmplitudeRequest(
            template_request=embedded_rank2_request(
                reciprocal_mesh_size=reciprocal_mesh_size,
                amplitudes=initial_amplitudes,
                parent_hopping_scale=parent_hopping_scale,
            ),
            thresholds=Periodic1DRank2AmplitudeRefinementThresholds(
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
    verification = Periodic1DRank2AdaptiveAmplitudeIndependentVerifier(
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
) -> Periodic1DRank2MomentumRefinementAnalysis:
    """Calculate and independently verify one installed nested-momentum study."""
    template = embedded_rank2_request(
        reciprocal_mesh_size=reciprocal_mesh_sizes[0],
        amplitudes=amplitudes,
        parent_hopping_scale=parent_hopping_scale,
    )
    thresholds = Periodic1DRank2MomentumRefinementThresholds(
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
    analysis = Periodic1DRank2MomentumRefinementAnalyzer(
        request=Periodic1DRank2MomentumRefinementRequest(
            template_request=template,
            reciprocal_mesh_sizes=reciprocal_mesh_sizes,
            thresholds=thresholds,
            required_stable_refinements=required_stable_refinements,
        ),
        transporter=ClosedLoopPolarFrameTransporter(),
    ).execute()
    verification = Periodic1DRank2MomentumRefinementIndependentVerifier(
        analysis
    ).result()
    if not verification.passed:
        raise ValueError("installed independent momentum verification failed")
    return analysis


def qualified_parent(
    analysis: Periodic1DRank2Analysis,
) -> Periodic1DRank2QualifiedParent:
    """Require and return the installed qualified-parent outcome."""
    if type(analysis) is not Periodic1DRank2Analysis:
        raise TypeError("analysis must be an installed rank-two analysis")
    if type(analysis.qualification) is not Periodic1DRank2QualifiedParent:
        raise ValueError("development study requires a qualified parent")
    return analysis.qualification


def parent_family(
    *,
    reciprocal_mesh_size: int,
    amplitudes: tuple[float, ...],
    parent_hopping_scales: tuple[float, ...],
) -> Periodic1DRank2ParentFamilyAnalysis:
    """Calculate one five-scale family through the installed family owner."""
    template = embedded_rank2_request(
        reciprocal_mesh_size=reciprocal_mesh_size,
        amplitudes=amplitudes,
        parent_hopping_scale=parent_hopping_scales[-1],
    )
    analysis = Periodic1DRank2ParentFamilyAnalyzer(
        request=Periodic1DRank2ParentFamilyRequest(
            template_request=template,
            parent_hopping_scales=parent_hopping_scales,
        ),
        transporter=ClosedLoopPolarFrameTransporter(),
    ).execute()
    verification = Periodic1DRank2ParentFamilyVerifier(
        Periodic1DRank2ParentFamilyAnalysisRecord(analysis).to_json()
    ).result()
    if not verification.passed:
        raise ValueError("installed independent parent-family verification failed")
    return analysis


def completed_truncation(
    analysis: Periodic1DRank2TruncationAnalysis,
) -> Periodic1DRank2TruncationCompleted:
    """Require and return the installed completed-truncation outcome."""
    if type(analysis) is not Periodic1DRank2TruncationCompleted:
        raise ValueError("development study requires completed truncation")
    return analysis


def truncation_verification_defect(
    analysis: Periodic1DRank2TruncationAnalysis,
) -> float:
    """Return the largest installed independent truncation discrepancy."""
    verification = Periodic1DRank2TruncationIndependentVerifier(analysis).result()
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
) -> Periodic1DRank2TruncationAnalysis:
    """Calculate and independently verify one dense installed truncation inventory."""
    template = embedded_rank2_request(
        reciprocal_mesh_size=construction_mesh_size,
        amplitudes=amplitudes,
        parent_hopping_scale=parent_hopping_scale,
    )
    analysis = Periodic1DRank2TruncationAnalyzer(
        request=Periodic1DRank2TruncationRequest.every_integer_through(
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
