"""Independent in-memory comparison for adaptive amplitude refinement."""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from ksdft2effmass.verification import CompositeVerification, VerificationObservation

from .amplitude_refinement import (
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeConverged,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeEvaluationsExhausted,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeLevelsExhausted,
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeQualificationStopped,
    Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel,
    Periodic1DEmbeddedSubspaceRank2AmplitudeValidation,
)
from .amplitude_refinement_reference import (
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeIndependentReferenceAnalyzer,
)
from .verification import _compare_analyses, _observation


class EmbeddedSubspaceRank2AdaptiveAmplitudeVerification(CompositeVerification):
    """Group independent direct-evaluation and adaptive-decision comparisons."""


_QualifiedAdaptiveAmplitude = (
    Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeConverged
    | Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeEvaluationsExhausted
    | Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeLevelsExhausted
)


class Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeIndependentVerifier:
    """Compare one adaptive result with independently rebuilt direct samples."""

    __slots__ = ("_observed",)

    def __init__(
        self,
        observed: Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis,
    ) -> None:
        if type(observed) not in (
            Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeQualificationStopped,
            Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeConverged,
            Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeLevelsExhausted,
            Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeEvaluationsExhausted,
        ):
            raise TypeError("observed must be a closed adaptive-amplitude outcome")
        self._observed = observed

    def result(self) -> EmbeddedSubspaceRank2AdaptiveAmplitudeVerification:
        """Return independent discrepancies without defining retained bytes."""
        reference = (
            Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeIndependentReferenceAnalyzer(
                self._observed.request
            ).execute()
        )
        return EmbeddedSubspaceRank2AdaptiveAmplitudeVerification(
            _compare_adaptive_amplitude(self._observed, reference)
        )


def _compare_adaptive_amplitude(
    observed: Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis,
    reference: Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeAnalysis,
) -> Mapping[str, VerificationObservation]:
    if observed.request != reference.request:
        raise ValueError("independent adaptive request does not match observed request")
    observations: dict[str, VerificationObservation] = {
        "outcome_variant_defect": _observation(
            float(type(observed) is not type(reference)),
            0.0,
        ),
        "evaluation_count_defect": _observation(
            float(abs(len(observed.evaluations) - len(reference.evaluations))),
            0.0,
        ),
        "evaluation_inventory_defect": _observation(
            float(
                tuple(item.request.amplitudes for item in observed.evaluations)
                != tuple(item.request.amplitudes for item in reference.evaluations)
            ),
            0.0,
        ),
    }
    if len(observed.evaluations) != len(reference.evaluations):
        return observations
    for index, (candidate, expected) in enumerate(
        zip(observed.evaluations, reference.evaluations, strict=True)
    ):
        for name, comparison in _compare_analyses(candidate, expected).items():
            observations[f"evaluation_{index}_{name}"] = comparison
    if type(observed) is (
        Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeQualificationStopped
    ):
        return observations
    if type(reference) is (
        Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeQualificationStopped
    ):
        return observations
    qualified_observed = cast(_QualifiedAdaptiveAmplitude, observed)
    qualified_reference = cast(_QualifiedAdaptiveAmplitude, reference)
    _compare_levels(
        observations,
        qualified_observed,
        qualified_reference,
        observed.request.template_request.verification_absolute_tolerance,
    )
    if type(observed) is (
        Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeEvaluationsExhausted
    ) and type(reference) is (
        Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeEvaluationsExhausted
    ):
        observations["blocked_amplitude_inventory_defect"] = _observation(
            float(observed.blocked_amplitudes != reference.blocked_amplitudes),
            0.0,
        )
    return observations


def _compare_levels(
    observations: dict[str, VerificationObservation],
    observed: _QualifiedAdaptiveAmplitude,
    reference: _QualifiedAdaptiveAmplitude,
    tolerance: float,
) -> None:
    observations["level_count_defect"] = _observation(
        float(abs(len(observed.levels) - len(reference.levels))),
        0.0,
    )
    observations["validation_count_defect"] = _observation(
        float(abs(len(observed.validations) - len(reference.validations))),
        0.0,
    )
    observations["all_evaluated_amplitude_inventory_defect"] = _observation(
        float(
            tuple(point.amplitude for point in observed.all_evaluated_points)
            != tuple(point.amplitude for point in reference.all_evaluated_points)
        ),
        0.0,
    )
    if len(observed.levels) == len(reference.levels):
        for index, (candidate, expected) in enumerate(
            zip(observed.levels, reference.levels, strict=True)
        ):
            observations[f"level_{index}_identity_defect"] = _observation(
                float(
                    (
                        candidate.level_index,
                        candidate.interpolation_nodes,
                        candidate.evaluated_amplitudes,
                        candidate.failing_interval_indices,
                        candidate.within_tolerances,
                    )
                    != (
                        expected.level_index,
                        expected.interpolation_nodes,
                        expected.evaluated_amplitudes,
                        expected.failing_interval_indices,
                        expected.within_tolerances,
                    )
                ),
                0.0,
            )
            _compare_defects(
                observations,
                f"level_{index}",
                candidate,
                expected,
                tolerance,
            )
    if len(observed.validations) == len(reference.validations):
        for index, (validation_candidate, validation_expected) in enumerate(
            zip(observed.validations, reference.validations, strict=True)
        ):
            observations[f"validation_{index}_identity_defect"] = _observation(
                float(
                    (
                        validation_candidate.level_index,
                        validation_candidate.interpolation_nodes,
                        validation_candidate.evaluated_amplitudes,
                        validation_candidate.failing_point_indices,
                        validation_candidate.within_tolerances,
                    )
                    != (
                        validation_expected.level_index,
                        validation_expected.interpolation_nodes,
                        validation_expected.evaluated_amplitudes,
                        validation_expected.failing_point_indices,
                        validation_expected.within_tolerances,
                    )
                ),
                0.0,
            )
            _compare_defects(
                observations,
                f"validation_{index}",
                validation_candidate,
                validation_expected,
                tolerance,
            )


def _compare_defects(
    observations: dict[str, VerificationObservation],
    prefix: str,
    observed: (
        Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel
        | Periodic1DEmbeddedSubspaceRank2AmplitudeValidation
    ),
    reference: (
        Periodic1DEmbeddedSubspaceRank2AmplitudeRefinementLevel
        | Periodic1DEmbeddedSubspaceRank2AmplitudeValidation
    ),
    tolerance: float,
) -> None:
    for name in (
        "maximum_correlation_defect",
        "maximum_operator_threshold_defect",
        "maximum_joint_threshold_defect",
        "maximum_hopping_weight_defect",
        "maximum_hopping_power_defect",
    ):
        observations[f"{prefix}_{name}_absolute_defect"] = _observation(
            abs(getattr(observed, name) - getattr(reference, name)),
            tolerance,
        )


__all__ = [
    "EmbeddedSubspaceRank2AdaptiveAmplitudeVerification",
    "Periodic1DEmbeddedSubspaceRank2AdaptiveAmplitudeIndependentVerifier",
]
