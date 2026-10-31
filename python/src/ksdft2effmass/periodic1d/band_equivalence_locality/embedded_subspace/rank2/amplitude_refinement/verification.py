"""Independent in-memory comparison for adaptive amplitude refinement."""

from __future__ import annotations

from ksdft2effmass.verification import CompositeVerification, VerificationObservation

from ..parent_scale.verification import (
    Periodic1DRank2AnalysisVerificationAssessor,
)
from .analysis import (
    Periodic1DRank2AdaptiveAmplitudeAnalysis,
    Periodic1DRank2AdaptiveAmplitudeConverged,
    Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted,
    Periodic1DRank2AdaptiveAmplitudeLevelsExhausted,
    Periodic1DRank2AdaptiveAmplitudeQualificationStopped,
)
from .independent_reference import (
    Periodic1DRank2AdaptiveAmplitudeIndependentReferenceAnalyzer,
)

_AdaptiveAmplitudeReferenceAnalyzer = (
    Periodic1DRank2AdaptiveAmplitudeIndependentReferenceAnalyzer
)


class EmbeddedSubspaceRank2AdaptiveAmplitudeVerification(CompositeVerification):
    """Group independent direct-evaluation and adaptive-decision comparisons."""


class Periodic1DRank2AdaptiveAmplitudeIndependentVerifier:
    """Compare one adaptive result with independently rebuilt direct samples."""

    __slots__ = ("_observed",)

    def __init__(
        self,
        observed: Periodic1DRank2AdaptiveAmplitudeAnalysis,
    ) -> None:
        if type(observed) not in (
            Periodic1DRank2AdaptiveAmplitudeQualificationStopped,
            Periodic1DRank2AdaptiveAmplitudeConverged,
            Periodic1DRank2AdaptiveAmplitudeLevelsExhausted,
            Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted,
        ):
            raise TypeError("observed must be a closed adaptive-amplitude outcome")
        self._observed = observed

    def result(self) -> EmbeddedSubspaceRank2AdaptiveAmplitudeVerification:
        """Return independent discrepancies without defining retained bytes."""
        observed = self._observed
        reference_analyzer = _AdaptiveAmplitudeReferenceAnalyzer(observed.request)
        reference = reference_analyzer.execute()
        if observed.request != reference.request:
            raise ValueError(
                "independent adaptive request does not match observed request"
            )
        observations: dict[str, VerificationObservation] = {
            "outcome_variant_defect": VerificationObservation.dimensionless(
                float(type(observed) is not type(reference)),
                0.0,
            ),
            "evaluation_count_defect": VerificationObservation.dimensionless(
                float(abs(len(observed.evaluations) - len(reference.evaluations))),
                0.0,
            ),
            "evaluation_inventory_defect": VerificationObservation.dimensionless(
                float(
                    tuple(item.request.amplitudes for item in observed.evaluations)
                    != tuple(item.request.amplitudes for item in reference.evaluations)
                ),
                0.0,
            ),
        }
        if len(observed.evaluations) != len(reference.evaluations):
            return EmbeddedSubspaceRank2AdaptiveAmplitudeVerification(observations)
        for index, (candidate, expected) in enumerate(
            zip(observed.evaluations, reference.evaluations, strict=True)
        ):
            evaluation_verification = Periodic1DRank2AnalysisVerificationAssessor(
                candidate,
                expected,
            ).assess()
            for name, comparison in evaluation_verification.observations.items():
                observations[f"evaluation_{index}_{name}"] = comparison
        if type(observed) is (
            Periodic1DRank2AdaptiveAmplitudeQualificationStopped
        ) or type(reference) is (Periodic1DRank2AdaptiveAmplitudeQualificationStopped):
            return EmbeddedSubspaceRank2AdaptiveAmplitudeVerification(observations)
        if type(observed) is Periodic1DRank2AdaptiveAmplitudeConverged:
            observed_levels = observed.levels
            observed_validations = observed.validations
        elif type(observed) is (Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted):
            observed_levels = observed.levels
            observed_validations = observed.validations
        elif type(observed) is (Periodic1DRank2AdaptiveAmplitudeLevelsExhausted):
            observed_levels = observed.levels
            observed_validations = observed.validations
        else:
            raise TypeError("observed must remain a qualified outcome")
        if type(reference) is (Periodic1DRank2AdaptiveAmplitudeConverged):
            reference_levels = reference.levels
            reference_validations = reference.validations
        elif type(reference) is (Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted):
            reference_levels = reference.levels
            reference_validations = reference.validations
        elif type(reference) is (Periodic1DRank2AdaptiveAmplitudeLevelsExhausted):
            reference_levels = reference.levels
            reference_validations = reference.validations
        else:
            raise TypeError("reference must remain a qualified outcome")
        tolerance = observed.request.template_request.verification_absolute_tolerance
        observations.update(
            {
                "level_count_defect": VerificationObservation.dimensionless(
                    float(abs(len(observed_levels) - len(reference_levels))),
                    0.0,
                ),
                "validation_count_defect": VerificationObservation.dimensionless(
                    float(abs(len(observed_validations) - len(reference_validations))),
                    0.0,
                ),
                "all_evaluated_amplitude_inventory_defect": (
                    VerificationObservation.dimensionless(
                        float(
                            tuple(
                                point.amplitude
                                for point in observed.all_evaluated_points
                            )
                            != tuple(
                                point.amplitude
                                for point in reference.all_evaluated_points
                            )
                        ),
                        0.0,
                    )
                ),
            }
        )
        defect_names = (
            "maximum_correlation_defect",
            "maximum_operator_threshold_defect",
            "maximum_joint_threshold_defect",
            "maximum_hopping_weight_defect",
            "maximum_hopping_power_defect",
        )
        if len(observed_levels) == len(reference_levels):
            for index, (candidate_level, expected_level) in enumerate(
                zip(observed_levels, reference_levels, strict=True)
            ):
                observations[f"level_{index}_identity_defect"] = (
                    VerificationObservation.dimensionless(
                        float(
                            (
                                candidate_level.level_index,
                                candidate_level.interpolation_nodes,
                                candidate_level.evaluated_amplitudes,
                                candidate_level.failing_interval_indices,
                                candidate_level.within_tolerances,
                            )
                            != (
                                expected_level.level_index,
                                expected_level.interpolation_nodes,
                                expected_level.evaluated_amplitudes,
                                expected_level.failing_interval_indices,
                                expected_level.within_tolerances,
                            )
                        ),
                        0.0,
                    )
                )
                for name in defect_names:
                    observations[f"level_{index}_{name}_absolute_defect"] = (
                        VerificationObservation.dimensionless(
                            abs(
                                getattr(candidate_level, name)
                                - getattr(expected_level, name)
                            ),
                            tolerance,
                        )
                    )
        if len(observed_validations) == len(reference_validations):
            for index, (candidate_validation, expected_validation) in enumerate(
                zip(observed_validations, reference_validations, strict=True)
            ):
                observations[f"validation_{index}_identity_defect"] = (
                    VerificationObservation.dimensionless(
                        float(
                            (
                                candidate_validation.level_index,
                                candidate_validation.interpolation_nodes,
                                candidate_validation.evaluated_amplitudes,
                                candidate_validation.failing_point_indices,
                                candidate_validation.within_tolerances,
                            )
                            != (
                                expected_validation.level_index,
                                expected_validation.interpolation_nodes,
                                expected_validation.evaluated_amplitudes,
                                expected_validation.failing_point_indices,
                                expected_validation.within_tolerances,
                            )
                        ),
                        0.0,
                    )
                )
                for name in defect_names:
                    observations[f"validation_{index}_{name}_absolute_defect"] = (
                        VerificationObservation.dimensionless(
                            abs(
                                getattr(candidate_validation, name)
                                - getattr(expected_validation, name)
                            ),
                            tolerance,
                        )
                    )
        if type(observed) is (
            Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted
        ) and type(reference) is (Periodic1DRank2AdaptiveAmplitudeEvaluationsExhausted):
            observations["blocked_amplitude_inventory_defect"] = (
                VerificationObservation.dimensionless(
                    float(observed.blocked_amplitudes != reference.blocked_amplitudes),
                    0.0,
                )
            )
        return EmbeddedSubspaceRank2AdaptiveAmplitudeVerification(observations)


__all__ = [
    "EmbeddedSubspaceRank2AdaptiveAmplitudeVerification",
    "Periodic1DRank2AdaptiveAmplitudeIndependentVerifier",
]
