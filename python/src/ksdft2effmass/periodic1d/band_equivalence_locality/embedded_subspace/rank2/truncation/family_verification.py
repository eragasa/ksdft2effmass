"""Independent in-memory verification of parent-family truncation."""

from __future__ import annotations

from ksdft2effmass.real_space_support_truncation import (
    MinimumToleranceSatisfyingSupport,
    SupportToleranceUnresolved,
)
from ksdft2effmass.verification import (
    CompositeVerification,
    MemberwiseCompositeVerificationComposer,
    VerificationObservation,
)

from .family import Periodic1DRank2TruncationFamilyAnalysis
from .reference import (
    Periodic1DRank2TruncationIndependentReferenceAnalyzer,
)
from .results import Periodic1DRank2TruncationCompleted
from .tolerance_selection_reference import (
    Periodic1DRank2TruncationToleranceSelectionIndependentReferenceAnalyzer,
)
from .verification import (
    Periodic1DRank2TruncationVerificationAssessor,
)


class EmbeddedSubspaceRank2TruncationFamilyVerification(CompositeVerification):
    """Group independent truncation and support-selection comparisons."""


class Periodic1DRank2TruncationFamilyIndependentVerifier:
    """Independently reconstruct every member and derived support decision."""

    __slots__ = ("_observed",)

    def __init__(
        self,
        observed: Periodic1DRank2TruncationFamilyAnalysis,
    ) -> None:
        if type(observed) is not Periodic1DRank2TruncationFamilyAnalysis:
            raise TypeError("observed must be a truncation-family analysis")
        self._observed = observed

    def result(self) -> EmbeddedSubspaceRank2TruncationFamilyVerification:
        """Return member reconstruction and support-selection discrepancies."""
        declared_scales = (
            self._observed.request.parent_family_request.parent_hopping_scales
        )
        observed_scales = tuple(
            member.request.template_request.parent_hopping_scale
            for member in self._observed.members
        )
        observations: dict[str, VerificationObservation] = {
            "member_count_defect": VerificationObservation.dimensionless(
                float(abs(len(self._observed.members) - len(declared_scales))),
                0.0,
            ),
            "parent_scale_inventory_defect": VerificationObservation.dimensionless(
                float(observed_scales != declared_scales),
                0.0,
            ),
        }
        references = tuple(
            Periodic1DRank2TruncationIndependentReferenceAnalyzer(
                member.request
            ).execute()
            for member in self._observed.members
        )
        memberwise = MemberwiseCompositeVerificationComposer(
            tuple(
                Periodic1DRank2TruncationVerificationAssessor(
                    observed=member,
                    reference=reference,
                ).assess()
                for member, reference in zip(
                    self._observed.members,
                    references,
                    strict=True,
                )
            )
        ).result()
        observations.update(memberwise.observations)

        for member_index, reference in enumerate(references):
            observed_selections = self._observed.support_tolerance_selections_by_member[
                member_index
            ]
            if type(reference) is Periodic1DRank2TruncationCompleted:
                reference_selections = tuple(
                    Periodic1DRank2TruncationToleranceSelectionIndependentReferenceAnalyzer(
                        point=point,
                        tolerance=self._observed.request.support_tolerance,
                    ).execute()
                    for point in reference.points
                )
            else:
                reference_selections = ()
            observations[f"member_{member_index}_selection_point_count_defect"] = (
                VerificationObservation.dimensionless(
                    float(abs(len(observed_selections) - len(reference_selections))),
                    0.0,
                )
            )
            if len(observed_selections) != len(reference_selections):
                continue
            for point_index, (observed, expected) in enumerate(
                zip(observed_selections, reference_selections, strict=True)
            ):
                outcomes = (
                    (
                        "reference_matrix_frobenius_maximum",
                        observed.reference_model.matrix_frobenius_maximum_error,
                        expected.reference_matrix_frobenius_maximum_error,
                    ),
                    (
                        "reference_ordered_eigenvalue_maximum_absolute",
                        observed.reference_model.ordered_eigenvalue_maximum_absolute_error,
                        expected.reference_ordered_eigenvalue_maximum_absolute_error,
                    ),
                    (
                        "comparison_matrix_frobenius_maximum",
                        observed.comparison_model.matrix_frobenius_maximum_error,
                        expected.comparison_matrix_frobenius_maximum_error,
                    ),
                    (
                        "comparison_ordered_eigenvalue_maximum_absolute",
                        (
                            observed.comparison_model.ordered_eigenvalue_maximum_absolute_error
                        ),
                        expected.comparison_ordered_eigenvalue_maximum_absolute_error,
                    ),
                )
                for channel, observed_outcome, expected_outcome in outcomes:
                    decision_defect = type(observed_outcome) is not type(
                        expected_outcome
                    )
                    if type(observed_outcome) is MinimumToleranceSatisfyingSupport and (
                        type(expected_outcome) is MinimumToleranceSatisfyingSupport
                    ):
                        decision_defect = (
                            observed_outcome.comparison_index
                            != expected_outcome.comparison_index
                            or observed_outcome.support != expected_outcome.support
                        )
                    elif (
                        type(observed_outcome) is SupportToleranceUnresolved
                        and type(expected_outcome) is SupportToleranceUnresolved
                    ):
                        decision_defect = (
                            observed_outcome.comparison_count
                            != expected_outcome.comparison_count
                        )
                    observations[
                        f"member_{member_index}_point_{point_index}_{channel}"
                        "_support_selection_defect"
                    ] = VerificationObservation.dimensionless(
                        float(decision_defect), 0.0
                    )
        return EmbeddedSubspaceRank2TruncationFamilyVerification(observations)


__all__ = [
    "EmbeddedSubspaceRank2TruncationFamilyVerification",
    "Periodic1DRank2TruncationFamilyIndependentVerifier",
]
