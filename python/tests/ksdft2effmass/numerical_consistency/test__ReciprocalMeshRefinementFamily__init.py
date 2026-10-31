"""Tests for dimension- and rank-independent reciprocal-mesh families."""

from __future__ import annotations

from dataclasses import dataclass, replace

import pytest

from ksdft2effmass.numerical_consistency import (
    NestedReciprocalMeshInventory,
    NumericalConsistency,
    ReciprocalMeshRefinementFamily,
    ReciprocalMeshRefinementFamilyMember,
    ReciprocalMeshRefinementFamilyRequest,
    ReciprocalMeshShape,
)


@dataclass(frozen=True, slots=True)
class _RefinementOutcome(NumericalConsistency):
    label: str


class TestReciprocalMeshRefinementFamily:
    """Establish dimension-independent mesh nesting and family alignment."""

    @pytest.mark.parametrize(
        ("coarse", "fine", "dimension"),
        [
            ((8,), (16,), 1),
            ((8, 10), (16, 10), 2),
            ((8, 10, 12), (16, 20, 12), 3),
        ],
    )
    def test_inventory__admits_nested_one_two_and_three_dimensional_meshes(
        self,
        coarse: tuple[int, ...],
        fine: tuple[int, ...],
        dimension: int,
    ) -> None:
        inventory = NestedReciprocalMeshInventory(
            (ReciprocalMeshShape(coarse), ReciprocalMeshShape(fine))
        )

        assert inventory.dimension == dimension
        assert inventory.meshes[0].axis_sizes == coarse
        assert inventory.meshes[1].axis_sizes == fine

    def test_init__aligns_generic_outcomes_with_ordered_family_coordinates(
        self,
    ) -> None:
        request = ReciprocalMeshRefinementFamilyRequest(
            family_coordinates=("parent-a", "parent-b"),
            reciprocal_meshes=NestedReciprocalMeshInventory(
                (ReciprocalMeshShape((8, 8)), ReciprocalMeshShape((16, 16)))
            ),
        )
        family = ReciprocalMeshRefinementFamily(
            request=request,
            members=(
                ReciprocalMeshRefinementFamilyMember(
                    family_coordinate="parent-a",
                    outcome=_RefinementOutcome("converged"),
                ),
                ReciprocalMeshRefinementFamilyMember(
                    family_coordinate="parent-b",
                    outcome=_RefinementOutcome("unresolved"),
                ),
            ),
        )

        assert isinstance(family, NumericalConsistency)
        assert tuple(member.outcome.label for member in family.members) == (
            "converged",
            "unresolved",
        )

    def test_init__rejects_boolean_axes_non_nested_meshes_and_misaligned_members(
        self,
    ) -> None:
        with pytest.raises(TypeError, match="built-in integers"):
            ReciprocalMeshShape((True,))
        with pytest.raises(ValueError, match="integer multiple"):
            NestedReciprocalMeshInventory(
                (ReciprocalMeshShape((8, 8)), ReciprocalMeshShape((12, 16)))
            )
        request = ReciprocalMeshRefinementFamilyRequest(
            family_coordinates=(0.0, 1.0),
            reciprocal_meshes=NestedReciprocalMeshInventory(
                (ReciprocalMeshShape((8,)), ReciprocalMeshShape((16,)))
            ),
        )
        family = ReciprocalMeshRefinementFamily(
            request=request,
            members=(
                ReciprocalMeshRefinementFamilyMember(
                    family_coordinate=0.0,
                    outcome=_RefinementOutcome("first"),
                ),
                ReciprocalMeshRefinementFamilyMember(
                    family_coordinate=1.0,
                    outcome=_RefinementOutcome("second"),
                ),
            ),
        )

        with pytest.raises(ValueError, match="request order"):
            replace(family, members=tuple(reversed(family.members)))
