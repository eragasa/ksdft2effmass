"""Threshold-adjacent truncation decisions across reciprocal meshes."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import pairwise

from ksdft2effmass.numerical_consistency import NumericalConsistency
from ksdft2effmass.real_space_support_truncation import (
    MinimumToleranceSatisfyingSupport,
    SupportToleranceSelectionOutcome,
    SupportToleranceUnresolved,
)

from .family import Periodic1DRank2TruncationFamilyAnalysis


@dataclass(frozen=True, slots=True)
class Periodic1DRank2TruncationMeshStabilityAssessment(NumericalConsistency):
    """Retain aligned truncation-family decisions on nested construction meshes.

    This assessment compares discrete support decisions only. It does not combine their
    scientific error channels, change the support tolerance, or establish continuum
    convergence.
    """

    refinement_families: tuple[Periodic1DRank2TruncationFamilyAnalysis, ...]

    def __post_init__(self) -> None:
        if type(self.refinement_families) is not tuple:
            raise TypeError("refinement_families must be a tuple")
        if len(self.refinement_families) < 2:
            raise ValueError("refinement_families must contain at least two analyses")
        if any(
            type(family) is not Periodic1DRank2TruncationFamilyAnalysis
            for family in self.refinement_families
        ):
            raise TypeError(
                "refinement_families must contain exact truncation-family analyses"
            )
        first = self.refinement_families[0].request
        scales = first.parent_family_request.parent_hopping_scales
        amplitudes = first.parent_family_request.template_request.amplitudes
        for family in self.refinement_families:
            request = family.request
            if request.parent_family_request.parent_hopping_scales != scales:
                raise ValueError("all refinement families must use one scale inventory")
            if request.parent_family_request.template_request.amplitudes != amplitudes:
                raise ValueError(
                    "all refinement families must use one amplitude inventory"
                )
            if request.maximum_ranges != first.maximum_ranges:
                raise ValueError(
                    "all refinement families must use one support inventory"
                )
            if request.support_tolerance != first.support_tolerance:
                raise ValueError(
                    "all refinement families must use one support tolerance"
                )
            construction_size = (
                request.parent_family_request.template_request.reciprocal_mesh_size
            )
            if request.evaluation_mesh_size != 4 * construction_size + 1:
                raise ValueError(
                    "evaluation meshes must contain four intervals per construction "
                    "interval plus the periodic endpoint"
                )
        for coarse, fine in pairwise(self.construction_mesh_sizes):
            if fine != 2 * coarse:
                raise ValueError("construction meshes must be nested doubling meshes")

    @property
    def construction_mesh_sizes(self) -> tuple[int, ...]:
        """Return construction-mesh sizes in refinement order."""
        return tuple(
            family.request.parent_family_request.template_request.reciprocal_mesh_size
            for family in self.refinement_families
        )

    @property
    def evaluation_mesh_sizes(self) -> tuple[int, ...]:
        """Return evaluation-mesh sizes in refinement order."""
        return tuple(
            family.request.evaluation_mesh_size for family in self.refinement_families
        )

    @property
    def adjacent_decision_change_counts(self) -> tuple[int, ...]:
        """Count exact support-decision changes for each adjacent mesh pair."""
        counts: list[int] = []
        for coarse, fine in pairwise(self.refinement_families):
            changes = 0
            for coarse_member, fine_member in zip(
                coarse.support_tolerance_selections_by_member,
                fine.support_tolerance_selections_by_member,
                strict=True,
            ):
                if len(coarse_member) != len(fine_member):
                    changes += max(len(coarse_member), len(fine_member), 1)
                    continue
                for coarse_selection, fine_selection in zip(
                    coarse_member, fine_member, strict=True
                ):
                    coarse_outcomes = (
                        coarse_selection.reference_model.matrix_frobenius_maximum_error,
                        coarse_selection.reference_model.ordered_eigenvalue_maximum_absolute_error,
                        coarse_selection.comparison_model.matrix_frobenius_maximum_error,
                        coarse_selection.comparison_model.ordered_eigenvalue_maximum_absolute_error,
                    )
                    fine_outcomes = (
                        fine_selection.reference_model.matrix_frobenius_maximum_error,
                        fine_selection.reference_model.ordered_eigenvalue_maximum_absolute_error,
                        fine_selection.comparison_model.matrix_frobenius_maximum_error,
                        fine_selection.comparison_model.ordered_eigenvalue_maximum_absolute_error,
                    )
                    changes += sum(
                        self._decision_identity(coarse_outcome)
                        != self._decision_identity(fine_outcome)
                        for coarse_outcome, fine_outcome in zip(
                            coarse_outcomes, fine_outcomes, strict=True
                        )
                    )
            counts.append(changes)
        return tuple(counts)

    @staticmethod
    def _decision_identity(
        outcome: SupportToleranceSelectionOutcome,
    ) -> tuple[str, int]:
        if type(outcome) is MinimumToleranceSatisfyingSupport:
            return ("minimum_tolerance_satisfying_support", outcome.comparison_index)
        if type(outcome) is SupportToleranceUnresolved:
            return ("support_tolerance_unresolved", outcome.comparison_count)
        raise TypeError(
            "selection outcome must be one closed support-selection variant"
        )


__all__ = ["Periodic1DRank2TruncationMeshStabilityAssessment"]
