"""Independent reconstruction of the embedded rank-two parent family."""

from __future__ import annotations

from dataclasses import dataclass

from ..parent_scale.independent_reference import (
    Periodic1DRank2IndependentReferenceAnalyzer,
)
from ..parent_scale.request import Periodic1DRank2Request
from ..parent_scale.results import Periodic1DRank2Analysis
from .analysis import Periodic1DRank2ParentFamilyRequest


@dataclass(frozen=True, slots=True)
class Periodic1DRank2ParentFamilyIndependentReference:
    request: Periodic1DRank2ParentFamilyRequest
    members: tuple[Periodic1DRank2Analysis, ...]


class Periodic1DRank2ParentFamilyIndependentReferenceAnalyzer:
    """Independently reconstruct every declared parent-hopping family member."""

    __slots__ = ("_request",)

    def __init__(
        self,
        request: Periodic1DRank2ParentFamilyRequest,
    ) -> None:
        if type(request) is not Periodic1DRank2ParentFamilyRequest:
            raise TypeError("request must be Periodic1DRank2ParentFamilyRequest")
        self._request = request

    def execute(
        self,
    ) -> Periodic1DRank2ParentFamilyIndependentReference:
        """Return a direct-formula reference for the complete family."""
        return Periodic1DRank2ParentFamilyIndependentReference(
            request=self._request,
            members=tuple(
                Periodic1DRank2IndependentReferenceAnalyzer(
                    _independent_member_request(self._request, scale)
                ).execute()
                for scale in self._request.parent_hopping_scales
            ),
        )


def _independent_member_request(
    family: Periodic1DRank2ParentFamilyRequest,
    scale: float,
) -> Periodic1DRank2Request:
    template = family.template_request
    return Periodic1DRank2Request(
        reciprocal_mesh_size=template.reciprocal_mesh_size,
        amplitudes=template.amplitudes,
        parent_hopping_scale=scale,
        minimum_external_gap=template.minimum_external_gap,
        minimum_transport_singular_value=template.minimum_transport_singular_value,
        frame_absolute_tolerance=template.frame_absolute_tolerance,
        transport_rank_relative_tolerance=template.transport_rank_relative_tolerance,
        transport_validation_relative_tolerance=(
            template.transport_validation_relative_tolerance
        ),
        harmonic_absolute_degeneracy_tolerance=(
            template.harmonic_absolute_degeneracy_tolerance
        ),
        harmonic_relative_degeneracy_tolerance=(
            template.harmonic_relative_degeneracy_tolerance
        ),
    )


__all__ = [
    "Periodic1DRank2ParentFamilyIndependentReference",
    "Periodic1DRank2ParentFamilyIndependentReferenceAnalyzer",
]
