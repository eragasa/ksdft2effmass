"""Independent in-memory comparison for embedded rank-two momentum refinement."""

from __future__ import annotations

from ksdft2effmass.verification import CompositeVerification, VerificationObservation

from ..parent_scale.verification import (
    Periodic1DRank2AnalysisVerificationAssessor,
)
from .analysis import (
    Periodic1DRank2MomentumRefinementAnalysis,
    Periodic1DRank2MomentumRefinementConverged,
    Periodic1DRank2MomentumRefinementQualificationStopped,
    Periodic1DRank2MomentumRefinementUnresolved,
)
from .independent_reference import (
    Periodic1DRank2MomentumRefinementIndependentReferenceAnalyzer,
    _IndependentMomentumConverged,
    _IndependentMomentumQualificationStopped,
    _IndependentMomentumUnresolved,
)

_MomentumRefinementReferenceAnalyzer = (
    Periodic1DRank2MomentumRefinementIndependentReferenceAnalyzer
)


class EmbeddedSubspaceRank2MomentumRefinementVerification(CompositeVerification):
    """Group independent mesh and nested-refinement comparisons."""


class Periodic1DRank2MomentumRefinementIndependentVerifier:
    """Compare one scientific value with an independently rebuilt refinement."""

    __slots__ = ("_observed",)

    def __init__(
        self,
        observed: Periodic1DRank2MomentumRefinementAnalysis,
    ) -> None:
        if type(observed) not in (
            Periodic1DRank2MomentumRefinementQualificationStopped,
            Periodic1DRank2MomentumRefinementConverged,
            Periodic1DRank2MomentumRefinementUnresolved,
        ):
            raise TypeError("observed must be a closed momentum-refinement outcome")
        self._observed = observed

    def result(self) -> EmbeddedSubspaceRank2MomentumRefinementVerification:
        """Return independent discrepancies without defining artifact bytes."""
        observed = self._observed
        reference_analyzer = _MomentumRefinementReferenceAnalyzer(observed.request)
        reference = reference_analyzer.execute()
        if observed.request != reference.request:
            raise ValueError(
                "independent refinement request does not match observed request"
            )
        tolerance = observed.request.template_request.verification_absolute_tolerance
        variants_agree = (
            (
                type(observed) is Periodic1DRank2MomentumRefinementQualificationStopped
                and type(reference) is _IndependentMomentumQualificationStopped
            )
            or (
                type(observed) is Periodic1DRank2MomentumRefinementConverged
                and type(reference) is _IndependentMomentumConverged
            )
            or (
                type(observed) is Periodic1DRank2MomentumRefinementUnresolved
                and type(reference) is _IndependentMomentumUnresolved
            )
        )
        observations: dict[str, VerificationObservation] = {
            "outcome_variant_defect": VerificationObservation.dimensionless(
                float(not variants_agree),
                0.0,
            ),
            "mesh_inventory_defect": VerificationObservation.dimensionless(
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
            observations["mesh_count_defect"] = VerificationObservation.dimensionless(
                float(abs(len(observed.mesh_analyses) - len(reference.mesh_analyses))),
                0.0,
            )
            return EmbeddedSubspaceRank2MomentumRefinementVerification(observations)
        for index, (candidate, expected) in enumerate(
            zip(observed.mesh_analyses, reference.mesh_analyses, strict=True)
        ):
            mesh_verification = Periodic1DRank2AnalysisVerificationAssessor(
                candidate,
                expected,
            ).assess()
            for name, comparison in mesh_verification.observations.items():
                observations[f"mesh_{index}_{name}"] = comparison
        observations["refinement_count_defect"] = VerificationObservation.dimensionless(
            float(abs(len(observed.refinements) - len(reference.refinements))),
            0.0,
        )
        if len(observed.refinements) != len(reference.refinements):
            return EmbeddedSubspaceRank2MomentumRefinementVerification(observations)
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
            observations[f"refinement_{index}_mesh_pair_defect"] = (
                VerificationObservation.dimensionless(
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
            )
            for name in scalar_names:
                observations[f"refinement_{index}_{name}_absolute_defect"] = (
                    VerificationObservation.dimensionless(
                        abs(
                            getattr(candidate_step, name) - getattr(expected_step, name)
                        ),
                        tolerance,
                    )
                )
            observations[f"refinement_{index}_angle_disposition_defect"] = (
                VerificationObservation.dimensionless(
                    float(
                        candidate_step.maximizing_angle_dispositions_stable
                        is not expected_step.maximizing_angle_dispositions_stable
                    ),
                    0.0,
                )
            )
            observations[f"refinement_{index}_threshold_disposition_defect"] = (
                VerificationObservation.dimensionless(
                    float(
                        candidate_step.within_tolerances
                        is not expected_step.within_tolerances
                    ),
                    0.0,
                )
            )
        return EmbeddedSubspaceRank2MomentumRefinementVerification(observations)


__all__ = [
    "EmbeddedSubspaceRank2MomentumRefinementVerification",
    "Periodic1DRank2MomentumRefinementIndependentVerifier",
]
