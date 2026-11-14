"""Generic immutable periodic basis-inventory contracts."""

import subprocess
import sys
from pathlib import Path

import pytest

from ksdft2effmass.periodic.operators import (
    LabeledComponentBasisCoordinate,
    PeriodicBasisInventory,
    PeriodicBasisInventoryEntry,
)
from ksdft2effmass.periodic.periodic1d.operators import Periodic1DBasisIdentity
from ksdft2effmass.periodic.periodic2d.operators import Periodic2DBasisIdentity

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


def _periodic2d_inventory() -> PeriodicBasisInventory[Periodic2DBasisIdentity]:
    return PeriodicBasisInventory(
        entries=tuple(
            PeriodicBasisInventoryEntry(
                retained_rank=rank,
                basis_identity=Periodic2DBasisIdentity(
                    display_identifier=f"periodic2d-test-basis-r{rank}",
                    coordinates=tuple(
                        LabeledComponentBasisCoordinate(
                            label=f"retained-orbital-{index:02d}"
                        )
                        for index in range(rank)
                    ),
                ),
            )
            for rank in (3, 4, 8)
        )
    )


class TestPeriodicBasisInventory:
    """Require explicit, homogeneous, calculation-composed basis inventories."""

    def test_resolves_exact_rank_bases(self) -> None:
        inventory = _periodic2d_inventory()

        assert type(inventory) is PeriodicBasisInventory
        assert inventory.retained_ranks == (3, 4, 8)
        for rank in inventory.retained_ranks:
            basis = inventory.basis_identity_for_rank(rank)
            assert type(basis) is Periodic2DBasisIdentity
            assert basis.dimension == rank

    def test_rejects_duplicate_ranks_and_dimension_mismatch(self) -> None:
        basis = Periodic2DBasisIdentity(
            display_identifier="rank-two-test-basis",
            coordinates=(
                LabeledComponentBasisCoordinate(label="first"),
                LabeledComponentBasisCoordinate(label="second"),
            ),
        )
        entry = PeriodicBasisInventoryEntry(
            retained_rank=2,
            basis_identity=basis,
        )

        with pytest.raises(ValueError, match="unique retained ranks"):
            PeriodicBasisInventory(entries=(entry, entry))
        with pytest.raises(ValueError, match="dimension"):
            PeriodicBasisInventoryEntry(retained_rank=3, basis_identity=basis)

    def test_rejects_mixed_dimensional_basis_types(self) -> None:
        one_dimensional = Periodic1DBasisIdentity(
            display_identifier="periodic1d-rank-one",
            coordinates=(LabeledComponentBasisCoordinate(label="one"),),
        )
        two_dimensional = Periodic2DBasisIdentity(
            display_identifier="periodic2d-rank-two",
            coordinates=(
                LabeledComponentBasisCoordinate(label="one"),
                LabeledComponentBasisCoordinate(label="two"),
            ),
        )

        with pytest.raises(ValueError, match="concrete dimensional basis type"):
            PeriodicBasisInventory(
                entries=(
                    PeriodicBasisInventoryEntry(
                        retained_rank=1,
                        basis_identity=one_dimensional,
                    ),
                    PeriodicBasisInventoryEntry(
                        retained_rank=2,
                        basis_identity=two_dimensional,
                    ),
                )
            )

    def test_lookup_rejects_noninteger_and_undeclared_rank(self) -> None:
        inventory = _periodic2d_inventory()

        with pytest.raises(TypeError, match="built-in integer"):
            inventory.basis_identity_for_rank(True)
        with pytest.raises(ValueError, match="not declared"):
            inventory.basis_identity_for_rank(16)

    def test_calculation_owned_periodic2d_inventory_constructs(self) -> None:
        repository_root = Path(__file__).resolve().parents[5]
        completed = subprocess.run(
            [
                sys.executable,
                str(repository_root / "calculations/periodic2d/rankN/control_basis.py"),
            ],
            cwd=repository_root,
            env={"PYTHONPATH": str(repository_root / "python/src")},
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode == 0, completed.stderr
