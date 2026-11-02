"""Independent scientific verification of an embedded rank-two parent family."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.verification import CompositeVerification, VerificationObservation

from ..parent_scale.verification import (
    Periodic1DRank2AnalysisVerificationAssessor,
)
from .analysis import Periodic1DRank2ParentFamilyAnalysis
from .independent_reference import (
    Periodic1DRank2ParentFamilyIndependentReference,
    Periodic1DRank2ParentFamilyIndependentReferenceAnalyzer,
)


class EmbeddedSubspaceRank2ParentFamilyVerification(CompositeVerification):
    """Group independent comparisons across a parent-hopping family."""


@dataclass(frozen=True, slots=True)
class Periodic1DRank2ParentFamilyIndependentVerification:
    """Bind one independent family reference to its comparison observations."""

    reference: Periodic1DRank2ParentFamilyIndependentReference
    verification: EmbeddedSubspaceRank2ParentFamilyVerification


class Periodic1DRank2ParentFamilyIndependentVerifier:
    """Independently reconstruct and compare one parent-hopping family."""

    __slots__ = ("_observed",)

    def __init__(
        self,
        observed: Periodic1DRank2ParentFamilyAnalysis,
    ) -> None:
        if type(observed) is not Periodic1DRank2ParentFamilyAnalysis:
            raise TypeError("observed must be an embedded rank-two parent family")
        self._observed = observed

    def result(
        self,
    ) -> Periodic1DRank2ParentFamilyIndependentVerification:
        """Return the independently reconstructed family and its observations."""
        observed = self._observed
        reference = Periodic1DRank2ParentFamilyIndependentReferenceAnalyzer(
            observed.request
        ).execute()
        if observed.request != reference.request:
            raise ValueError(
                "independent family request does not match subject request"
            )
        observed_inventory = tuple(
            member.request.parent_hopping_scale for member in observed.members
        )
        reference_inventory = tuple(
            member.request.parent_hopping_scale for member in reference.members
        )
        observations: dict[str, VerificationObservation] = {
            "member_inventory_defect": VerificationObservation.dimensionless(
                float(observed_inventory != reference_inventory),
                0.0,
            )
        }
        if observed_inventory == reference_inventory:
            for index, (candidate, expected) in enumerate(
                zip(observed.members, reference.members, strict=True)
            ):
                member_verification = Periodic1DRank2AnalysisVerificationAssessor(
                    candidate,
                    expected,
                ).assess()
                for name, observation in member_verification.observations.items():
                    observations[f"member_{index}_{name}"] = observation
        return Periodic1DRank2ParentFamilyIndependentVerification(
            reference=reference,
            verification=EmbeddedSubspaceRank2ParentFamilyVerification(observations),
        )


__all__ = [
    "EmbeddedSubspaceRank2ParentFamilyVerification",
    "Periodic1DRank2ParentFamilyIndependentVerification",
    "Periodic1DRank2ParentFamilyIndependentVerifier",
]
