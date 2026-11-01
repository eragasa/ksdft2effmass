"""Software ownership contracts for :class:`SubspaceReduction`."""

from __future__ import annotations

import pytest

from ksdft2effmass.hamiltonian import SpectralReduction
from ksdft2effmass.subspace_reduction import SubspaceReduction

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestSubspaceReduction:
    def test__spectral_reduction__has_nominal_owner(self) -> None:
        """Existing Hamiltonian compression adopts the reduction base."""
        assert issubclass(SpectralReduction, SubspaceReduction)

    def test__unrelated_shape__does_not_gain_structural_membership(self) -> None:
        """Matching vocabulary alone cannot admit an unrelated implementation."""

        class UnrelatedResult:
            __slots__ = ()

        assert not isinstance(UnrelatedResult(), SubspaceReduction)
