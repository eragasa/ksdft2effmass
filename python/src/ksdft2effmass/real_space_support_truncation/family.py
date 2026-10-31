"""Dimension- and rank-independent real-space-support truncation families."""

from __future__ import annotations

from dataclasses import dataclass

from .base import RealSpaceSupportTruncation


@dataclass(frozen=True, slots=True)
class RealSpaceSupportTruncationFamilyRequest[FamilyCoordinateT]:
    """Retain one ordered, unique family-coordinate inventory."""

    family_coordinates: tuple[FamilyCoordinateT, ...]

    def __post_init__(self) -> None:
        if type(self.family_coordinates) is not tuple:
            raise TypeError("family_coordinates must be a tuple")
        if len(self.family_coordinates) < 2:
            raise ValueError("family_coordinates must contain at least two values")
        for index, coordinate in enumerate(self.family_coordinates):
            for earlier in self.family_coordinates[:index]:
                if coordinate == earlier:
                    raise ValueError("family_coordinates must be unique")


@dataclass(frozen=True, slots=True)
class RealSpaceSupportTruncationFamilyMember[
    FamilyCoordinateT,
    TruncationOutcomeT: RealSpaceSupportTruncation,
]:
    """Bind one family coordinate to one support-truncation outcome."""

    family_coordinate: FamilyCoordinateT
    outcome: TruncationOutcomeT

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, RealSpaceSupportTruncation):
            raise TypeError("outcome must nominally inherit RealSpaceSupportTruncation")


@dataclass(frozen=True, slots=True)
class RealSpaceSupportTruncationFamily[
    FamilyCoordinateT,
    TruncationOutcomeT: RealSpaceSupportTruncation,
](RealSpaceSupportTruncation):
    """Retain one aligned support-truncation outcome per family coordinate."""

    request: RealSpaceSupportTruncationFamilyRequest[FamilyCoordinateT]
    members: tuple[
        RealSpaceSupportTruncationFamilyMember[
            FamilyCoordinateT,
            TruncationOutcomeT,
        ],
        ...,
    ]

    def __post_init__(self) -> None:
        if not isinstance(self.request, RealSpaceSupportTruncationFamilyRequest):
            raise TypeError("request must be a RealSpaceSupportTruncationFamilyRequest")
        if type(self.members) is not tuple:
            raise TypeError("members must be a tuple")
        if len(self.members) != len(self.request.family_coordinates):
            raise ValueError("members must cover every declared family coordinate")
        for member, coordinate in zip(
            self.members,
            self.request.family_coordinates,
            strict=True,
        ):
            if not isinstance(member, RealSpaceSupportTruncationFamilyMember):
                raise TypeError(
                    "members must contain RealSpaceSupportTruncationFamilyMember values"
                )
            if member.family_coordinate != coordinate:
                raise ValueError("member coordinates must match the request order")


__all__ = [
    "RealSpaceSupportTruncationFamily",
    "RealSpaceSupportTruncationFamilyMember",
    "RealSpaceSupportTruncationFamilyRequest",
]
