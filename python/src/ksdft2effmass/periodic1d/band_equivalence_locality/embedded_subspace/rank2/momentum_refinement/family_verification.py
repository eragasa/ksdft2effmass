"""Independent in-memory verification of parent-family momentum refinement."""

from __future__ import annotations

from ksdft2effmass.verification import (
    CompositeVerification,
    MemberwiseCompositeVerificationComposer,
    VerificationObservation,
)

from .family import (
    Periodic1DRank2MomentumRefinementFamilyAnalysis,
)
from .verification import (
    Periodic1DRank2MomentumRefinementIndependentVerifier,
)


class EmbeddedSubspaceRank2MomentumRefinementFamilyVerification(CompositeVerification):
    """Group independent comparisons across all declared parent scales."""


class Periodic1DRank2MomentumRefinementFamilyIndependentVerifier:
    """Independently reconstruct every member of one refinement family."""

    __slots__ = ("_observed",)

    def __init__(
        self,
        observed: Periodic1DRank2MomentumRefinementFamilyAnalysis,
    ) -> None:
        if type(observed) is not (Periodic1DRank2MomentumRefinementFamilyAnalysis):
            raise TypeError("observed must be a momentum-refinement family analysis")
        self._observed = observed

    def result(
        self,
    ) -> EmbeddedSubspaceRank2MomentumRefinementFamilyVerification:
        """Return independently reconstructed discrepancies for every family member."""
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
        memberwise = MemberwiseCompositeVerificationComposer(
            tuple(
                Periodic1DRank2MomentumRefinementIndependentVerifier(member).result()
                for member in self._observed.members
            )
        ).result()
        observations.update(memberwise.observations)
        return EmbeddedSubspaceRank2MomentumRefinementFamilyVerification(observations)


__all__ = [
    "EmbeddedSubspaceRank2MomentumRefinementFamilyVerification",
    "Periodic1DRank2MomentumRefinementFamilyIndependentVerifier",
]
