"""Software verification for :class:`CellHoppingRepresentationRole`."""

from __future__ import annotations

import pytest

from ksdft2effmass.operators.representations.identities import (
    CellHoppingRepresentationRole,
)

pytestmark = pytest.mark.software_verification


class TestCellHoppingRepresentationRole:
    """Establish the explicit nontext cell-hopping role inventory."""

    def test_members__separate_complete_inventory_from_truncated_support(self) -> None:
        """Cell-hopping nodes select one exact inventory-role enum member."""
        assert tuple(CellHoppingRepresentationRole) == (
            CellHoppingRepresentationRole.complete_declared_inventory,
            CellHoppingRepresentationRole.support_truncated,
        )
        assert all(
            not isinstance(member.value, str)
            for member in CellHoppingRepresentationRole
        )
