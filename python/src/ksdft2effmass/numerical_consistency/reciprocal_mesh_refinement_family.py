"""Dimension- and rank-independent reciprocal-mesh refinement families."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import pairwise

from .base import NumericalConsistency


@dataclass(frozen=True, slots=True)
class ReciprocalMeshShape:
    """Retain the axis sizes of one finite periodic reciprocal mesh."""

    axis_sizes: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.axis_sizes) is not tuple or not 1 <= len(self.axis_sizes) <= 3:
            raise TypeError(
                "axis_sizes must describe a one-, two-, or three-dimensional mesh"
            )
        for size in self.axis_sizes:
            if type(size) is not int:
                raise TypeError("axis_sizes must contain built-in integers")
            if size < 1:
                raise ValueError("axis_sizes must be positive")

    @property
    def dimension(self) -> int:
        """Return the reciprocal-space dimension."""
        return len(self.axis_sizes)


@dataclass(frozen=True, slots=True)
class NestedReciprocalMeshInventory:
    """Retain ordered reciprocal meshes related by exact axiswise nesting."""

    meshes: tuple[ReciprocalMeshShape, ...]

    def __post_init__(self) -> None:
        if type(self.meshes) is not tuple or len(self.meshes) < 2:
            raise TypeError("meshes must contain at least two reciprocal-mesh shapes")
        for mesh in self.meshes:
            if type(mesh) is not ReciprocalMeshShape:
                raise TypeError("meshes must contain exact ReciprocalMeshShape values")
        dimension = self.meshes[0].dimension
        for mesh in self.meshes:
            if mesh.dimension != dimension:
                raise ValueError("all reciprocal meshes must have one common dimension")
        for coarse, fine in pairwise(self.meshes):
            strictly_refined = False
            for coarse_size, fine_size in zip(
                coarse.axis_sizes, fine.axis_sizes, strict=True
            ):
                if fine_size < coarse_size or fine_size % coarse_size != 0:
                    raise ValueError(
                        "each fine axis size must be an integer multiple "
                        "of its coarse size"
                    )
                if fine_size > coarse_size:
                    strictly_refined = True
            if not strictly_refined:
                raise ValueError("each reciprocal mesh must refine at least one axis")

    @property
    def dimension(self) -> int:
        """Return the common reciprocal-space dimension."""
        return self.meshes[0].dimension


@dataclass(frozen=True, slots=True)
class ReciprocalMeshRefinementFamilyRequest[FamilyCoordinateT]:
    """Bind an ordered family-coordinate inventory to nested reciprocal meshes."""

    family_coordinates: tuple[FamilyCoordinateT, ...]
    reciprocal_meshes: NestedReciprocalMeshInventory

    def __post_init__(self) -> None:
        if (
            type(self.family_coordinates) is not tuple
            or len(self.family_coordinates) < 2
        ):
            raise TypeError("family_coordinates must contain at least two values")
        for index, coordinate in enumerate(self.family_coordinates):
            for earlier in self.family_coordinates[:index]:
                if coordinate == earlier:
                    raise ValueError("family_coordinates must be unique")
        if type(self.reciprocal_meshes) is not NestedReciprocalMeshInventory:
            raise TypeError(
                "reciprocal_meshes must be an exact NestedReciprocalMeshInventory"
            )


@dataclass(frozen=True, slots=True)
class ReciprocalMeshRefinementFamilyMember[
    FamilyCoordinateT,
    RefinementOutcomeT: NumericalConsistency,
]:
    """Bind one family coordinate to its numerical-refinement outcome."""

    family_coordinate: FamilyCoordinateT
    outcome: RefinementOutcomeT

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, NumericalConsistency):
            raise TypeError("outcome must nominally inherit NumericalConsistency")


@dataclass(frozen=True, slots=True)
class ReciprocalMeshRefinementFamily[
    FamilyCoordinateT,
    RefinementOutcomeT: NumericalConsistency,
](NumericalConsistency):
    """Retain one aligned numerical-refinement outcome per family coordinate."""

    request: ReciprocalMeshRefinementFamilyRequest[FamilyCoordinateT]
    members: tuple[
        ReciprocalMeshRefinementFamilyMember[
            FamilyCoordinateT,
            RefinementOutcomeT,
        ],
        ...,
    ]

    def __post_init__(self) -> None:
        if not isinstance(self.request, ReciprocalMeshRefinementFamilyRequest):
            raise TypeError("request must be a ReciprocalMeshRefinementFamilyRequest")
        if type(self.members) is not tuple:
            raise TypeError("members must be a tuple")
        if len(self.members) != len(self.request.family_coordinates):
            raise ValueError("members must cover every declared family coordinate")
        for member, coordinate in zip(
            self.members,
            self.request.family_coordinates,
            strict=True,
        ):
            if not isinstance(member, ReciprocalMeshRefinementFamilyMember):
                raise TypeError(
                    "members must contain ReciprocalMeshRefinementFamilyMember values"
                )
            if member.family_coordinate != coordinate:
                raise ValueError("member coordinates must match the request order")


__all__ = [
    "NestedReciprocalMeshInventory",
    "ReciprocalMeshRefinementFamily",
    "ReciprocalMeshRefinementFamilyMember",
    "ReciprocalMeshRefinementFamilyRequest",
    "ReciprocalMeshShape",
]
