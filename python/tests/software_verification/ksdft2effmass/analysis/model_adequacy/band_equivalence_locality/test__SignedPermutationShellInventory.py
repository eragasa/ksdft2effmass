"""Software verification for dense square and cubic shell inventories."""

import pytest
from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    SignedPermutationShellInventoryBuilder,
    SignedPermutationShellInventoryDefinition,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestSignedPermutationShellInventory:
    """Own dense attainable radii, multiplicities, and conjugate closure."""

    def test_execute__square_inventory__contains_every_attainable_shell(self) -> None:
        """All square support changes through squared radius five are included."""
        result = SignedPermutationShellInventoryBuilder().execute(
            SignedPermutationShellInventoryDefinition(LatticeDimension.TWO, 5)
        )

        assert tuple(shell.squared_radius for shell in result.shells) == (0, 1, 2, 4, 5)
        assert tuple(
            tuple(len(orbit.members) for orbit in shell.orbits)
            for shell in result.shells
        ) == ((1,), (4,), (4,), (4,), (8,))
        assert tuple(len(shell.cumulative_support) for shell in result.shells) == (
            1,
            5,
            9,
            13,
            21,
        )

    def test_execute__cubic_inventory__uses_distinct_orbit_multiplicities(self) -> None:
        """Zero and repeated coordinates reduce the nominal 48-operation orbit."""
        result = SignedPermutationShellInventoryBuilder().execute(
            SignedPermutationShellInventoryDefinition(LatticeDimension.THREE, 3)
        )

        assert tuple(shell.squared_radius for shell in result.shells) == (0, 1, 2, 3)
        assert tuple(
            tuple(len(orbit.members) for orbit in shell.orbits)
            for shell in result.shells
        ) == ((1,), (6,), (12,), (8,))
        assert tuple(len(shell.cumulative_support) for shell in result.shells) == (
            1,
            7,
            19,
            27,
        )
        for shell in result.shells:
            components = {item.components for item in shell.cumulative_support}
            assert {
                tuple(-value for value in item) for item in components
            } == components

    def test_definition__unsupported_controls__fail_closed(self) -> None:
        """One-dimensional, Boolean, negative, and nonintegral caps are rejected."""
        with pytest.raises(ValueError, match="TWO or THREE"):
            SignedPermutationShellInventoryDefinition(LatticeDimension.ONE, 4)
        with pytest.raises(TypeError, match="built-in int"):
            SignedPermutationShellInventoryDefinition(LatticeDimension.TWO, True)
        with pytest.raises(ValueError, match="nonnegative"):
            SignedPermutationShellInventoryDefinition(LatticeDimension.TWO, -1)
