"""Bounded parent-hopping family for the embedded-subspace rank-two control."""

from __future__ import annotations

from dataclasses import dataclass, replace

from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ..parent_scale.analysis import Periodic1DRank2Analyzer
from ..parent_scale.request import Periodic1DRank2Request
from ..parent_scale.results import Periodic1DRank2Analysis


@dataclass(frozen=True, slots=True)
class Periodic1DRank2ParentFamilyRequest:
    """Bind an ordered onsite-to-full parent-hopping homotopy."""

    template_request: Periodic1DRank2Request
    parent_hopping_scales: tuple[float, ...]

    def __post_init__(self) -> None:
        if type(self.template_request) is not Periodic1DRank2Request:
            raise TypeError("template_request must be Periodic1DRank2Request")
        if self.template_request.parent_hopping_scale != 1.0:
            raise ValueError("template_request must describe the full parent")
        if type(self.parent_hopping_scales) is not tuple:
            raise TypeError("parent_hopping_scales must be a tuple")
        if len(self.parent_hopping_scales) < 2:
            raise ValueError("parent_hopping_scales must contain at least two values")
        if any(type(value) is not float for value in self.parent_hopping_scales):
            raise TypeError("parent_hopping_scales must contain built-in floats")
        if any(not 0.0 <= value <= 1.0 for value in self.parent_hopping_scales):
            raise ValueError("parent_hopping_scales must lie in [0, 1]")
        if self.parent_hopping_scales[0] != 0.0:
            raise ValueError("parent_hopping_scales must begin at zero")
        if self.parent_hopping_scales[-1] != 1.0:
            raise ValueError("parent_hopping_scales must end at one")
        if tuple(sorted(set(self.parent_hopping_scales))) != (
            self.parent_hopping_scales
        ):
            raise ValueError("parent_hopping_scales must be unique and increasing")

    def request_at(
        self,
        parent_hopping_scale: float,
    ) -> Periodic1DRank2Request:
        """Return one family member without changing any other control."""
        if type(parent_hopping_scale) is not float:
            raise TypeError("parent_hopping_scale must be a built-in float")
        if parent_hopping_scale not in self.parent_hopping_scales:
            raise ValueError("parent_hopping_scale is not in the declared family")
        template = self.template_request
        return Periodic1DRank2Request(
            reciprocal_mesh_size=template.reciprocal_mesh_size,
            amplitudes=template.amplitudes,
            parent_hopping_scale=parent_hopping_scale,
            minimum_external_gap=template.minimum_external_gap,
            minimum_transport_singular_value=(
                template.minimum_transport_singular_value
            ),
            frame_absolute_tolerance=template.frame_absolute_tolerance,
            transport_rank_relative_tolerance=(
                template.transport_rank_relative_tolerance
            ),
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


@dataclass(frozen=True, slots=True)
class Periodic1DRank2ParentFamilyAnalysis:
    """Retain every explicitly declared parent-hopping family member."""

    request: Periodic1DRank2ParentFamilyRequest
    members: tuple[Periodic1DRank2Analysis, ...]

    def __post_init__(self) -> None:
        if type(self.request) is not (Periodic1DRank2ParentFamilyRequest):
            raise TypeError("request must be Periodic1DRank2ParentFamilyRequest")
        if type(self.members) is not tuple or any(
            type(member) is not Periodic1DRank2Analysis for member in self.members
        ):
            raise TypeError("members must be a typed tuple")
        template = self.request.template_request
        for member, scale in zip(
            self.members,
            self.request.parent_hopping_scales,
            strict=True,
        ):
            if member.request.parent_hopping_scale != scale:
                raise ValueError("member hopping scale does not match family inventory")
            if replace(member.request, parent_hopping_scale=1.0) != template:
                raise ValueError("member controls do not match the family template")


class Periodic1DRank2ParentFamilyAnalyzer:
    """Evaluate all members of one bounded parent-hopping homotopy."""

    __slots__ = ("_request", "_transporter")

    def __init__(
        self,
        *,
        request: Periodic1DRank2ParentFamilyRequest,
        transporter: ClosedLoopPolarFrameTransporter,
    ) -> None:
        if type(request) is not (Periodic1DRank2ParentFamilyRequest):
            raise TypeError("request must be Periodic1DRank2ParentFamilyRequest")
        if type(transporter) is not ClosedLoopPolarFrameTransporter:
            raise TypeError("transporter must be ClosedLoopPolarFrameTransporter")
        self._request = request
        self._transporter = transporter

    @property
    def request(self) -> Periodic1DRank2ParentFamilyRequest:
        """Return the immutable constructor-bound family request."""
        return self._request

    def execute(self) -> Periodic1DRank2ParentFamilyAnalysis:
        """Analyze every scale while preserving all other controls exactly."""
        return Periodic1DRank2ParentFamilyAnalysis(
            request=self.request,
            members=tuple(
                Periodic1DRank2Analyzer(
                    request=self.request.request_at(scale),
                    transporter=self._transporter,
                ).execute()
                for scale in self.request.parent_hopping_scales
            ),
        )


__all__ = [
    "Periodic1DRank2ParentFamilyAnalysis",
    "Periodic1DRank2ParentFamilyAnalyzer",
    "Periodic1DRank2ParentFamilyRequest",
]
