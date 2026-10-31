"""Independent in-memory comparison for embedded rank-two momentum refinement."""

from __future__ import annotations

from collections.abc import Mapping

from ksdft2effmass.verification import CompositeVerification, VerificationObservation

from .refinement import (
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalysis,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementConverged,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementQualificationStopped,
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementUnresolved,
)
from .refinement_reference import (
    Periodic1DEmbeddedSubspaceRank2MomentumRefinementIndependentReferenceAnalyzer,
    _IndependentMomentumConverged,
    _IndependentMomentumQualificationStopped,
    _IndependentMomentumReference,
    _IndependentMomentumUnresolved,
)
from .verification import _compare_analyses, _observation


class EmbeddedSubspaceRank2MomentumRefinementVerification(CompositeVerification):
    """Group independent mesh and nested-refinement comparisons."""


class Periodic1DEmbeddedSubspaceRank2MomentumRefinementIndependentVerifier:
    """Compare one scientific value with an independently rebuilt refinement.

    This owner verifies the in-memory scientific value. It deliberately does not
    define a new retained-wire format; canonical artifact authentication remains a
    separate lifecycle boundary.
    """

    __slots__ = ("_observed",)

    def __init__(
        self,
        observed: Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalysis,
    ) -> None:
        if type(observed) not in (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementQualificationStopped,
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementConverged,
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementUnresolved,
        ):
            raise TypeError("observed must be a closed momentum-refinement outcome")
        self._observed = observed

    def result(self) -> EmbeddedSubspaceRank2MomentumRefinementVerification:
        """Return independent discrepancies without defining artifact bytes."""
        reference = (
            Periodic1DEmbeddedSubspaceRank2MomentumRefinementIndependentReferenceAnalyzer(
                self._observed.request
            ).execute()
        )
        return EmbeddedSubspaceRank2MomentumRefinementVerification(
            _compare_momentum_refinements(self._observed, reference)
        )


def _compare_momentum_refinements(
    observed: Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalysis,
    reference: _IndependentMomentumReference,
) -> Mapping[str, VerificationObservation]:
    if observed.request != reference.request:
        raise ValueError(
            "independent refinement request does not match observed request"
        )
    tolerance = observed.request.template_request.verification_absolute_tolerance
    observations: dict[str, VerificationObservation] = {
        "outcome_variant_defect": _observation(
            float(not _variants_agree(observed, reference)),
            0.0,
        ),
        "mesh_inventory_defect": _observation(
            float(
                tuple(
                    item.request.reciprocal_mesh_size
                    for item in observed.mesh_analyses
                )
                != tuple(
                    item.request.reciprocal_mesh_size
                    for item in reference.mesh_analyses
                )
            ),
            0.0,
        ),
    }
    if len(observed.mesh_analyses) != len(reference.mesh_analyses):
        observations["mesh_count_defect"] = _observation(
            float(abs(len(observed.mesh_analyses) - len(reference.mesh_analyses))),
            0.0,
        )
        return observations
    for index, (candidate, expected) in enumerate(
        zip(observed.mesh_analyses, reference.mesh_analyses, strict=True)
    ):
        for name, comparison in _compare_analyses(candidate, expected).items():
            observations[f"mesh_{index}_{name}"] = comparison
    observations["refinement_count_defect"] = _observation(
        float(abs(len(observed.refinements) - len(reference.refinements))),
        0.0,
    )
    if len(observed.refinements) != len(reference.refinements):
        return observations
    scalar_names = (
        "maximum_parent_diagnostic_change",
        "maximum_shared_parent_eigenvalue_defect",
        "maximum_shared_parent_projector_defect",
        "maximum_correlation_change",
        "maximum_threshold_change",
        "maximum_hopping_weight_change",
        "maximum_hopping_power_change",
        "maximum_angle_change",
        "maximum_band_defect",
        "maximum_reconstruction_defect",
        "maximum_parseval_defect",
    )
    for index, (candidate_step, expected_step) in enumerate(
        zip(observed.refinements, reference.refinements, strict=True)
    ):
        observations[f"refinement_{index}_mesh_pair_defect"] = _observation(
            float(
                (
                    candidate_step.coarse_mesh_size,
                    candidate_step.fine_mesh_size,
                )
                != (
                    expected_step.coarse_mesh_size,
                    expected_step.fine_mesh_size,
                )
            ),
            0.0,
        )
        for name in scalar_names:
            observations[f"refinement_{index}_{name}_absolute_defect"] = (
                _observation(
                    abs(
                        getattr(candidate_step, name)
                        - getattr(expected_step, name)
                    ),
                    tolerance,
                )
            )
        observations[f"refinement_{index}_angle_disposition_defect"] = (
            _observation(
                float(
                    candidate_step.maximizing_angle_dispositions_stable
                    is not expected_step.maximizing_angle_dispositions_stable
                ),
                0.0,
            )
        )
        observations[f"refinement_{index}_threshold_disposition_defect"] = (
            _observation(
                float(
                    candidate_step.within_tolerances
                    is not expected_step.within_tolerances
                ),
                0.0,
            )
        )
    return observations


def _variants_agree(
    observed: Periodic1DEmbeddedSubspaceRank2MomentumRefinementAnalysis,
    reference: _IndependentMomentumReference,
) -> bool:
    return (
        type(observed)
        is Periodic1DEmbeddedSubspaceRank2MomentumRefinementQualificationStopped
        and type(reference) is _IndependentMomentumQualificationStopped
    ) or (
        type(observed) is Periodic1DEmbeddedSubspaceRank2MomentumRefinementConverged
        and type(reference) is _IndependentMomentumConverged
    ) or (
        type(observed) is Periodic1DEmbeddedSubspaceRank2MomentumRefinementUnresolved
        and type(reference) is _IndependentMomentumUnresolved
    )


__all__ = [
    "EmbeddedSubspaceRank2MomentumRefinementVerification",
    "Periodic1DEmbeddedSubspaceRank2MomentumRefinementIndependentVerifier",
]
