"""Parent-family momentum refinement for embedded-subspace rank two."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import pairwise

from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.numerical_consistency import (
    NestedReciprocalMeshInventory,
    NumericalConsistency,
    ReciprocalMeshRefinementFamily,
    ReciprocalMeshRefinementFamilyMember,
    ReciprocalMeshRefinementFamilyRequest,
    ReciprocalMeshShape,
)

from ..parent_family.analysis import (
    Periodic1DRank2ParentFamilyRequest,
)
from .analysis import (
    Periodic1DRank2MomentumRefinementAnalysis,
    Periodic1DRank2MomentumRefinementAnalyzer,
    Periodic1DRank2MomentumRefinementConverged,
    Periodic1DRank2MomentumRefinementQualificationStopped,
    Periodic1DRank2MomentumRefinementRequest,
    Periodic1DRank2MomentumRefinementThresholds,
    Periodic1DRank2MomentumRefinementUnresolved,
)


@dataclass(frozen=True, slots=True)
class Periodic1DRank2MomentumRefinementFamilyRequest:
    """Bind one nested-mesh refinement policy to a parent-hopping family."""

    parent_family_request: Periodic1DRank2ParentFamilyRequest
    reciprocal_mesh_sizes: tuple[int, ...]
    thresholds: Periodic1DRank2MomentumRefinementThresholds
    required_stable_refinements: int

    def __post_init__(self) -> None:
        if type(self.parent_family_request) is not (Periodic1DRank2ParentFamilyRequest):
            raise TypeError("parent_family_request must be a parent-family request")
        if (
            type(self.reciprocal_mesh_sizes) is not tuple
            or len(self.reciprocal_mesh_sizes) < 2
        ):
            raise TypeError("reciprocal_mesh_sizes must contain at least two integers")
        for size in self.reciprocal_mesh_sizes:
            if type(size) is not int:
                raise TypeError("reciprocal_mesh_sizes must contain built-in integers")
        if self.reciprocal_mesh_sizes[0] != (
            self.parent_family_request.template_request.reciprocal_mesh_size
        ):
            raise ValueError("parent-family template must describe the first mesh")
        for coarse, fine in pairwise(self.reciprocal_mesh_sizes):
            if fine != 2 * coarse:
                raise ValueError("reciprocal_mesh_sizes must be nested doubling meshes")
        if type(self.thresholds) is not (Periodic1DRank2MomentumRefinementThresholds):
            raise TypeError("thresholds must be momentum-refinement thresholds")
        if type(self.required_stable_refinements) is not int:
            raise TypeError("required_stable_refinements must be a built-in int")
        if not 1 <= self.required_stable_refinements < len(self.reciprocal_mesh_sizes):
            raise ValueError("required_stable_refinements exceeds available mesh pairs")

    @property
    def refinement_family_request(
        self,
    ) -> ReciprocalMeshRefinementFamilyRequest[float]:
        """Return the dimension-independent numerical-consistency request."""
        return ReciprocalMeshRefinementFamilyRequest(
            family_coordinates=self.parent_family_request.parent_hopping_scales,
            reciprocal_meshes=NestedReciprocalMeshInventory(
                tuple(
                    ReciprocalMeshShape((size,)) for size in self.reciprocal_mesh_sizes
                )
            ),
        )

    def request_at(
        self,
        parent_hopping_scale: float,
    ) -> Periodic1DRank2MomentumRefinementRequest:
        """Return one scale-specific refinement with all other controls unchanged."""
        return Periodic1DRank2MomentumRefinementRequest(
            template_request=self.parent_family_request.request_at(
                parent_hopping_scale
            ),
            reciprocal_mesh_sizes=self.reciprocal_mesh_sizes,
            thresholds=self.thresholds,
            required_stable_refinements=self.required_stable_refinements,
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRank2MomentumRefinementFamilyAnalysis(NumericalConsistency):
    """Adapt a generic reciprocal-mesh family to the rank-two 1D owner."""

    request: Periodic1DRank2MomentumRefinementFamilyRequest
    refinement_family: ReciprocalMeshRefinementFamily[
        float,
        Periodic1DRank2MomentumRefinementAnalysis,
    ]

    def __post_init__(self) -> None:
        if type(self.request) is not (Periodic1DRank2MomentumRefinementFamilyRequest):
            raise TypeError("request must be a momentum-refinement family request")
        if type(self.refinement_family) is not ReciprocalMeshRefinementFamily:
            raise TypeError("refinement_family must be a reciprocal-mesh family")
        if self.refinement_family.request != self.request.refinement_family_request:
            raise ValueError(
                "refinement_family request does not match the family request"
            )
        outcome_types = (
            Periodic1DRank2MomentumRefinementQualificationStopped,
            Periodic1DRank2MomentumRefinementConverged,
            Periodic1DRank2MomentumRefinementUnresolved,
        )
        for member in self.refinement_family.members:
            if type(member.outcome) not in outcome_types:
                raise TypeError(
                    "family members must contain closed refinement outcomes"
                )
            if member.outcome.request != self.request.request_at(
                member.family_coordinate
            ):
                raise ValueError("member request does not match its parent scale")

    @property
    def members(
        self,
    ) -> tuple[Periodic1DRank2MomentumRefinementAnalysis, ...]:
        """Project the family-specific ordered outcomes."""
        return tuple(member.outcome for member in self.refinement_family.members)


class Periodic1DRank2MomentumRefinementFamilyAnalyzer:
    """Evaluate the declared nested-mesh study for every parent-family member."""

    __slots__ = ("_request", "_transporter")

    def __init__(
        self,
        *,
        request: Periodic1DRank2MomentumRefinementFamilyRequest,
        transporter: ClosedLoopPolarFrameTransporter,
    ) -> None:
        if type(request) is not (Periodic1DRank2MomentumRefinementFamilyRequest):
            raise TypeError("request must be a momentum-refinement family request")
        if type(transporter) is not ClosedLoopPolarFrameTransporter:
            raise TypeError("transporter must be ClosedLoopPolarFrameTransporter")
        self._request = request
        self._transporter = transporter

    @property
    def request(
        self,
    ) -> Periodic1DRank2MomentumRefinementFamilyRequest:
        """Return the immutable constructor-bound family request."""
        return self._request

    def execute(
        self,
    ) -> Periodic1DRank2MomentumRefinementFamilyAnalysis:
        """Return one ordered closed refinement outcome for each parent scale."""
        refinement_family = ReciprocalMeshRefinementFamily(
            request=self.request.refinement_family_request,
            members=tuple(
                ReciprocalMeshRefinementFamilyMember(
                    family_coordinate=scale,
                    outcome=(
                        Periodic1DRank2MomentumRefinementAnalyzer(
                            request=self.request.request_at(scale),
                            transporter=self._transporter,
                        ).execute()
                    ),
                )
                for scale in (self.request.parent_family_request.parent_hopping_scales)
            ),
        )
        return Periodic1DRank2MomentumRefinementFamilyAnalysis(
            request=self.request,
            refinement_family=refinement_family,
        )


__all__ = [
    "Periodic1DRank2MomentumRefinementFamilyAnalysis",
    "Periodic1DRank2MomentumRefinementFamilyAnalyzer",
    "Periodic1DRank2MomentumRefinementFamilyRequest",
]
