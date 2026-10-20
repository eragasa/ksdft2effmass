"""Software verification for :class:`BlochSpaceRole`."""

from __future__ import annotations

import pytest

from ksdft2effmass.operators.representations.identities import BlochSpaceRole

pytestmark = pytest.mark.software_verification


class TestBlochSpaceRole:
    """Establish the explicit nontext Bloch-space role inventory."""

    def test_members__are_exactly_ambient_and_retained(self) -> None:
        """Bloch nodes select an explicit ambient or retained enum member."""
        assert tuple(BlochSpaceRole) == (
            BlochSpaceRole.ambient,
            BlochSpaceRole.retained,
        )
        assert all(not isinstance(member.value, str) for member in BlochSpaceRole)
