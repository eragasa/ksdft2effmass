"""Tests for dimension-independent support-truncation families."""

from __future__ import annotations

import pytest

from ksdft2effmass.real_space_support_truncation import (
    RealSpaceSupportTruncation,
    RealSpaceSupportTruncationFamily,
    RealSpaceSupportTruncationFamilyMember,
    RealSpaceSupportTruncationFamilyRequest,
    SymmetricRangeSupport1D,
)


class TestRealSpaceSupportTruncationFamily:
    """Establish nominal outcome admission and coordinate alignment."""

    def test_init__aligns_one_nominal_outcome_per_coordinate(self) -> None:
        request = RealSpaceSupportTruncationFamilyRequest(
            family_coordinates=("onsite", "full")
        )
        family = RealSpaceSupportTruncationFamily(
            request=request,
            members=(
                RealSpaceSupportTruncationFamilyMember(
                    family_coordinate="onsite",
                    outcome=SymmetricRangeSupport1D(0),
                ),
                RealSpaceSupportTruncationFamilyMember(
                    family_coordinate="full",
                    outcome=SymmetricRangeSupport1D(2),
                ),
            ),
        )

        assert isinstance(family, RealSpaceSupportTruncation)
        assert tuple(member.family_coordinate for member in family.members) == (
            "onsite",
            "full",
        )
        assert tuple(member.outcome.maximum_range for member in family.members) == (
            0,
            2,
        )

    def test_request__rejects_non_tuple_coordinate_inventory(self) -> None:
        with pytest.raises(TypeError, match="family_coordinates must be a tuple"):
            RealSpaceSupportTruncationFamilyRequest(
                family_coordinates=["onsite", "full"]  # type: ignore[arg-type]
            )

    def test_request__rejects_insufficient_coordinate_inventory(self) -> None:
        with pytest.raises(ValueError, match="contain at least two values"):
            RealSpaceSupportTruncationFamilyRequest(family_coordinates=("onsite",))

    def test_init__rejects_duplicate_or_misaligned_coordinates(self) -> None:
        with pytest.raises(ValueError, match="unique"):
            RealSpaceSupportTruncationFamilyRequest(family_coordinates=("same", "same"))

        request = RealSpaceSupportTruncationFamilyRequest(
            family_coordinates=("onsite", "full")
        )
        with pytest.raises(ValueError, match="request order"):
            RealSpaceSupportTruncationFamily(
                request=request,
                members=(
                    RealSpaceSupportTruncationFamilyMember(
                        family_coordinate="full",
                        outcome=SymmetricRangeSupport1D(0),
                    ),
                    RealSpaceSupportTruncationFamilyMember(
                        family_coordinate="onsite",
                        outcome=SymmetricRangeSupport1D(2),
                    ),
                ),
            )
