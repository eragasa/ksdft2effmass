"""Tests for the calculation-owned structured retained-basis inventory."""

from control_basis import CONTROL_BASIS_INVENTORY, control_parent_model

from ksdft2effmass.periodic.periodic1d.rankN.models import Periodic1DRankNParentModel


class TestPeriodic1DRankNControlBasisInventory:
    """Keep concrete analytic-study bases out of reusable source ownership."""

    def test__inventory__retains_the_exact_rank_order_and_coordinate_counts(
        self,
    ) -> None:
        """Require each reviewed study rank to select one explicit basis value."""
        assert tuple(
            entry.retained_rank for entry in CONTROL_BASIS_INVENTORY.entries
        ) == (3, 4, 8, 16)
        assert all(
            entry.basis_identity.dimension == entry.retained_rank
            for entry in CONTROL_BASIS_INVENTORY.entries
        )

    def test__parent_model__implements_the_reusable_contract_locally(self) -> None:
        """Keep the exact analytic parent formula owned by this calculation."""
        parent = control_parent_model(4)

        assert isinstance(parent, Periodic1DRankNParentModel)
        assert parent.band_subspace_rank == parent.basis_identity.dimension == 4
        assert parent.exact_isolation_gap == 2.1
