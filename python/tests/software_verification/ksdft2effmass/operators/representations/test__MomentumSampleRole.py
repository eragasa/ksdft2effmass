"""Software verification for :class:`MomentumSampleRole`."""

from __future__ import annotations

import pytest

from ksdft2effmass.operators.representations.domains import MomentumSampleRole

pytestmark = pytest.mark.software_verification


class TestMomentumSampleRole:
    """Establish the exact nontext momentum-sample role inventory."""

    def test_members__are_named_nontext_discriminants(self) -> None:
        """Callers select named members rather than raw string discriminators."""
        assert tuple(MomentumSampleRole) == (
            MomentumSampleRole.general,
            MomentumSampleRole.construction,
            MomentumSampleRole.evaluation,
        )
        assert all(not isinstance(member.value, str) for member in MomentumSampleRole)
