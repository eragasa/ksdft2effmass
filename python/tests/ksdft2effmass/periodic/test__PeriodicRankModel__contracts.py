"""Software verification for dimension- and rank-owned model bases."""

from __future__ import annotations

import importlib.util
import inspect
from dataclasses import dataclass

import pytest

from ksdft2effmass.models import Model
from ksdft2effmass.periodic.models import PeriodicModel, PeriodicModelRole
from ksdft2effmass.periodic.operators import LabeledComponentBasisCoordinate
from ksdft2effmass.periodic.periodic1d.models import Periodic1DModel
from ksdft2effmass.periodic.periodic1d.operators import Periodic1DBasisIdentity
from ksdft2effmass.periodic.periodic1d.rank2.models import Periodic1DRank2Model
from ksdft2effmass.periodic.periodic1d.rankN.models import Periodic1DRankNModel
from ksdft2effmass.periodic.periodic2d.models import Periodic2DModel
from ksdft2effmass.periodic.periodic2d.rank2.models import Periodic2DRank2Model
from ksdft2effmass.periodic.periodic2d.rankN.models import Periodic2DRankNModel
from ksdft2effmass.periodic.periodic3d.models import Periodic3DModel
from ksdft2effmass.periodic.periodic3d.rank2.models import Periodic3DRank2Model
from ksdft2effmass.periodic.periodic3d.rankN.models import Periodic3DRankNModel
from ksdft2effmass.periodic1d.rank1.models import Periodic1DRank1Model
from ksdft2effmass.periodic2d.rank1.models import Periodic2DRank1Model
from ksdft2effmass.periodic3d.rank1.models import Periodic3DRank1Model

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodicRankModel:
    """Verify the nominal model hierarchy follows domain, dimension, then rank."""

    @dataclass(frozen=True, slots=True)
    class Rank1Control(Periodic1DRank1Model):
        """Represent one synthetic rank-one control model."""

        @property
        def model_id(self) -> str:
            """Return the test-owned model identity."""
            return "test.periodic1d.rank1.control"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the control-model role."""
            return PeriodicModelRole.CONTROL_MODEL

    @dataclass(frozen=True, slots=True)
    class Rank2Control(Periodic1DRank2Model):
        """Represent one synthetic rank-two control model."""

        @property
        def basis_identity(self) -> Periodic1DBasisIdentity:
            """Return the explicit two-coordinate test basis."""
            return Periodic1DBasisIdentity(
                display_identifier="rank2-control-basis",
                coordinates=tuple(
                    LabeledComponentBasisCoordinate(label=f"component-{index}")
                    for index in range(2)
                ),
            )

        @property
        def model_id(self) -> str:
            """Return the test-owned model identity."""
            return "test.periodic1d.rank2.control"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the control-model role."""
            return PeriodicModelRole.CONTROL_MODEL

    @dataclass(frozen=True, slots=True)
    class RankNControl(Periodic1DRankNModel):
        """Represent one synthetic arbitrary-rank control model."""

        retained_rank: int

        @property
        def basis_identity(self) -> Periodic1DBasisIdentity:
            """Return the explicit runtime-rank test basis."""
            return Periodic1DBasisIdentity(
                display_identifier=f"rank{self.retained_rank}-control-basis",
                coordinates=tuple(
                    LabeledComponentBasisCoordinate(label=f"component-{index}")
                    for index in range(self.retained_rank)
                ),
            )

        @property
        def model_id(self) -> str:
            """Return the test-owned model identity."""
            return f"test.periodic1d.rankN.control:r{self.retained_rank}"

        @property
        def model_role(self) -> PeriodicModelRole:
            """Return the control-model role."""
            return PeriodicModelRole.CONTROL_MODEL

        @property
        def band_subspace_rank(self) -> int:
            """Return the test-owned finite retained-space rank."""
            return self.retained_rank

    def test__PeriodicRankModel__inheritance__orders_domain_dimension_and_rank(
        self,
    ) -> None:
        """Order each owner through its dimension and finite-rank refinements."""
        rank_owners = (
            (Periodic1DRank1Model, Periodic1DModel),
            (Periodic1DRank2Model, Periodic1DModel),
            (Periodic1DRankNModel, Periodic1DModel),
            (Periodic2DRank1Model, Periodic2DModel),
            (Periodic2DRank2Model, Periodic2DModel),
            (Periodic2DRankNModel, Periodic2DModel),
            (Periodic3DRank1Model, Periodic3DModel),
            (Periodic3DRank2Model, Periodic3DModel),
            (Periodic3DRankNModel, Periodic3DModel),
        )

        assert all(issubclass(owner, dimension) for owner, dimension in rank_owners)
        assert all(issubclass(owner, PeriodicModel) for owner, _ in rank_owners)
        assert all(issubclass(owner, Model) for owner, _ in rank_owners)
        assert issubclass(Periodic1DRank2Model, Periodic1DRankNModel)
        assert issubclass(Periodic2DRank2Model, Periodic2DRankNModel)
        assert issubclass(Periodic3DRank2Model, Periodic3DRankNModel)

    def test__PeriodicRankModel__class__nominal_owners_remain_abstract(self) -> None:
        """Nominal rank owners cannot instantiate without model identity and role."""
        owners = (
            Periodic1DRank1Model,
            Periodic1DRank2Model,
            Periodic1DRankNModel,
            Periodic2DRank1Model,
            Periodic2DRank2Model,
            Periodic2DRankNModel,
            Periodic3DRank1Model,
            Periodic3DRank2Model,
            Periodic3DRankNModel,
        )

        assert all(inspect.isabstract(owner) for owner in owners)

    def test__PeriodicRankModel__property__fixed_and_arbitrary_ranks_are_distinct(
        self,
    ) -> None:
        """Fixed-rank refinements and a runtime finite-rank case report exact ranks."""
        rank1 = self.Rank1Control()
        rank2 = self.Rank2Control()
        rank_n = self.RankNControl(retained_rank=5)

        assert (rank1.band_subspace_rank, rank2.band_subspace_rank) == (1, 2)
        assert rank_n.band_subspace_rank == 5
        assert tuple(type(value) for value in (1, 2, rank_n.band_subspace_rank)) == (
            int,
            int,
            int,
        )
        assert isinstance(rank2, Periodic1DRankNModel)
        assert not isinstance(rank_n, Periodic1DRank2Model)
        assert rank2.basis_identity.dimension == 2
        assert rank_n.basis_identity.dimension == 5

    def test__PeriodicRankModel__module__each_owner_resides_with_its_rank(self) -> None:
        """Module identities expose the complete dimension and rank ownership path."""
        assert (
            Periodic1DRank1Model.__module__,
            Periodic2DRank2Model.__module__,
            Periodic3DRankNModel.__module__,
        ) == (
            "ksdft2effmass.periodic1d.rank1.models.base",
            "ksdft2effmass.periodic.periodic2d.rank2.models.base",
            "ksdft2effmass.periodic.periodic3d.rankN.models.base",
        )

    def test__PeriodicRankModel__package__singular_model_namespaces_are_absent(
        self,
    ) -> None:
        """The plural owner migration leaves no compatibility package aliases."""
        retired = (
            "ksdft2effmass.model",
            "ksdft2effmass.periodic1d.model",
            "ksdft2effmass.periodic1d.rank1.model",
            "ksdft2effmass.periodic1d.rank2.model",
            "ksdft2effmass.periodic1d.rankN.model",
            "ksdft2effmass.periodic2d.model",
        )
        maintained = (
            "ksdft2effmass.models",
            "ksdft2effmass.periodic.models",
            "ksdft2effmass.periodic.periodic1d.models",
            "ksdft2effmass.periodic1d.rank1.models",
            "ksdft2effmass.periodic.periodic2d.models",
            "ksdft2effmass.periodic.periodic3d.rankN.models",
        )

        assert all(importlib.util.find_spec(name) is None for name in retired)
        assert all(importlib.util.find_spec(name) is not None for name in maintained)
