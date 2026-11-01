"""Parent-family real-space-support truncation for embedded rank two."""

from __future__ import annotations

import math
from dataclasses import dataclass

from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_family.analysis import (  # noqa: E501
    Periodic1DRank2ParentFamilyRequest,
)
from ksdft2effmass.periodic1d.support_truncation import (
    Periodic1DSupportTruncation,
)
from ksdft2effmass.real_space_support_truncation import (
    RealSpaceSupportTruncationFamily,
    RealSpaceSupportTruncationFamilyMember,
    RealSpaceSupportTruncationFamilyRequest,
    RealSpaceSupportTruncationToleranceSelection,
)

from .analysis import Periodic1DRank2TruncationAnalyzer
from .request import Periodic1DRank2TruncationRequest
from .results import (
    Periodic1DRank2TruncationAnalysis,
    Periodic1DRank2TruncationCompleted,
    Periodic1DRank2TruncationQualificationStopped,
)
from .tolerance_selection import (
    Periodic1DRank2TruncationToleranceSelector,
)


@dataclass(frozen=True, slots=True)
class Periodic1DRank2TruncationFamilyRequest:
    """Bind one support inventory and tolerance to a parent-hopping family."""

    parent_family_request: Periodic1DRank2ParentFamilyRequest
    maximum_ranges: tuple[int, ...]
    evaluation_mesh_size: int
    support_tolerance: float

    def __post_init__(self) -> None:
        if type(self.parent_family_request) is not (Periodic1DRank2ParentFamilyRequest):
            raise TypeError("parent_family_request must be a parent-family request")
        Periodic1DRank2TruncationRequest(
            template_request=self.parent_family_request.template_request,
            maximum_ranges=self.maximum_ranges,
            evaluation_mesh_size=self.evaluation_mesh_size,
        )
        if type(self.support_tolerance) is not float:
            raise TypeError("support_tolerance must be a built-in float")
        if not math.isfinite(self.support_tolerance) or self.support_tolerance <= 0.0:
            raise ValueError("support_tolerance must be finite and positive")

    @classmethod
    def every_integer_through(
        cls,
        *,
        parent_family_request: Periodic1DRank2ParentFamilyRequest,
        maximum_range: int,
        evaluation_mesh_size: int,
        support_tolerance: float,
    ) -> Periodic1DRank2TruncationFamilyRequest:
        """Construct the common candidate inventory ``0, ..., maximum_range``."""
        if type(maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        return cls(
            parent_family_request=parent_family_request,
            maximum_ranges=tuple(range(maximum_range + 1)),
            evaluation_mesh_size=evaluation_mesh_size,
            support_tolerance=support_tolerance,
        )

    @property
    def truncation_family_request(
        self,
    ) -> RealSpaceSupportTruncationFamilyRequest[float]:
        """Return the dimension- and rank-independent family request."""
        return RealSpaceSupportTruncationFamilyRequest(
            family_coordinates=self.parent_family_request.parent_hopping_scales
        )

    def request_at(
        self,
        parent_hopping_scale: float,
    ) -> Periodic1DRank2TruncationRequest:
        """Return one scale-specific truncation request with common controls."""
        return Periodic1DRank2TruncationRequest(
            template_request=self.parent_family_request.request_at(
                parent_hopping_scale
            ),
            maximum_ranges=self.maximum_ranges,
            evaluation_mesh_size=self.evaluation_mesh_size,
        )


@dataclass(frozen=True, slots=True, init=False)
class Periodic1DRank2TruncationFamilyAnalysis(Periodic1DSupportTruncation):
    """Adapt aligned truncation outcomes and derive their support decisions."""

    request: Periodic1DRank2TruncationFamilyRequest
    truncation_family: RealSpaceSupportTruncationFamily[
        float,
        Periodic1DRank2TruncationAnalysis,
    ]
    support_tolerance_selections_by_member: tuple[
        tuple[RealSpaceSupportTruncationToleranceSelection, ...],
        ...,
    ]

    def __init__(
        self,
        request: Periodic1DRank2TruncationFamilyRequest,
        truncation_family: RealSpaceSupportTruncationFamily[
            float,
            Periodic1DRank2TruncationAnalysis,
        ],
    ) -> None:
        if type(request) is not (Periodic1DRank2TruncationFamilyRequest):
            raise TypeError("request must be a truncation-family request")
        if type(truncation_family) is not RealSpaceSupportTruncationFamily:
            raise TypeError("truncation_family must be a support-truncation family")
        if truncation_family.request != request.truncation_family_request:
            raise ValueError("truncation_family request does not match the adapter")
        selections: list[tuple[RealSpaceSupportTruncationToleranceSelection, ...]] = []
        for member in truncation_family.members:
            if type(member.outcome) not in (
                Periodic1DRank2TruncationQualificationStopped,
                Periodic1DRank2TruncationCompleted,
            ):
                raise TypeError(
                    "family members must contain closed truncation outcomes"
                )
            if member.outcome.request != request.request_at(member.family_coordinate):
                raise ValueError("member request does not match its parent scale")
            if type(member.outcome) is (Periodic1DRank2TruncationCompleted):
                selections.append(
                    tuple(
                        Periodic1DRank2TruncationToleranceSelector(
                            point=point,
                            tolerance=request.support_tolerance,
                        ).execute()
                        for point in member.outcome.points
                    )
                )
            else:
                selections.append(())
        object.__setattr__(self, "request", request)
        object.__setattr__(self, "truncation_family", truncation_family)
        object.__setattr__(
            self, "support_tolerance_selections_by_member", tuple(selections)
        )

    @property
    def members(
        self,
    ) -> tuple[Periodic1DRank2TruncationAnalysis, ...]:
        """Project the family-specific ordered truncation outcomes."""
        return tuple(member.outcome for member in self.truncation_family.members)


class Periodic1DRank2TruncationFamilyAnalyzer:
    """Evaluate one common support policy for every declared parent scale."""

    __slots__ = ("_request", "_transporter")

    def __init__(
        self,
        *,
        request: Periodic1DRank2TruncationFamilyRequest,
        transporter: ClosedLoopPolarFrameTransporter,
    ) -> None:
        if type(request) is not (Periodic1DRank2TruncationFamilyRequest):
            raise TypeError("request must be a truncation-family request")
        if type(transporter) is not ClosedLoopPolarFrameTransporter:
            raise TypeError("transporter must be ClosedLoopPolarFrameTransporter")
        self._request = request
        self._transporter = transporter

    @property
    def request(self) -> Periodic1DRank2TruncationFamilyRequest:
        """Return the immutable constructor-bound family request."""
        return self._request

    def execute(self) -> Periodic1DRank2TruncationFamilyAnalysis:
        """Return one truncation outcome and derived selection set per scale."""
        truncation_family = RealSpaceSupportTruncationFamily(
            request=self.request.truncation_family_request,
            members=tuple(
                RealSpaceSupportTruncationFamilyMember(
                    family_coordinate=scale,
                    outcome=Periodic1DRank2TruncationAnalyzer(
                        request=self.request.request_at(scale),
                        transporter=self._transporter,
                    ).execute(),
                )
                for scale in self.request.parent_family_request.parent_hopping_scales
            ),
        )
        return Periodic1DRank2TruncationFamilyAnalysis(
            request=self.request,
            truncation_family=truncation_family,
        )


__all__ = [
    "Periodic1DRank2TruncationFamilyAnalysis",
    "Periodic1DRank2TruncationFamilyAnalyzer",
    "Periodic1DRank2TruncationFamilyRequest",
]
