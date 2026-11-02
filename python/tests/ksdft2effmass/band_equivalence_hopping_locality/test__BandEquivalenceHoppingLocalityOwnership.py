"""Ownership contracts for the thin band-equivalence/locality aggregate."""

from __future__ import annotations

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence.base import BandEquivalence
from ksdft2effmass.band_equivalence_hopping_locality.base import (
    BandEquivalenceHoppingLocality,
    BandEquivalenceHoppingLocalityAnalysis,
    BandEquivalenceHoppingLocalityAnalyzer,
    BandEquivalenceHoppingLocalityRequest,
    PeriodicBandEquivalenceHoppingLocality,
)
from ksdft2effmass.hopping_locality.base import HoppingLocality
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.base import (
    Periodic1DRank2BandEquivalenceHoppingLocalityCapability,
)
from ksdft2effmass.periodic1d.rank2.band_equivalence_hopping_locality.request import (
    Periodic1DRank2BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.assembly import (
    Periodic1DRankNGaugeAlignmentAssemblyRequest,
    Periodic1DRankNGaugeAlignmentResultAssembler,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.base import (
    Periodic1DRankNBandEquivalenceHoppingLocalityAction,
    Periodic1DRankNBandEquivalenceHoppingLocalityCapability,
    Periodic1DRankNBandEquivalenceHoppingLocalityValue,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.construction_mesh import (  # noqa: E501
    Periodic1DRankNConstructionMeshAnalysisRequest,
    Periodic1DRankNConstructionMeshAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.evaluation import (  # noqa: E501
    Periodic1DRankNEvaluationIndependenceAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.refinement import (  # noqa: E501
    Periodic1DRankNRefinementAnalysisRequest,
    Periodic1DRankNRefinementAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.request import (
    Periodic1DRankNBandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.result import (
    Periodic1DRankNBandEquivalenceHoppingLocalityAnalysis,
)
from ksdft2effmass.periodic2d.band_equivalence_hopping_locality.base import (
    Periodic2DBandEquivalenceHoppingLocality,
)
from ksdft2effmass.periodic2d.base import Periodic2DCapability
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis,
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.base import (
    Periodic2DRank2BandEquivalenceHoppingLocalityCapability,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.lifecycle import (
    Periodic2DRank2BandEquivalenceHoppingLocalityExecution,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.request import (
    Periodic2DRank2BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.analysis import (
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.base import (
    Periodic2DRankNBandEquivalenceHoppingLocalityCapability,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAction,
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseValue,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.model import (
    Periodic2DRankNAnalyticCase,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.request import (
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.result import (
    Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
)
from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.verification import (  # noqa: E501
    Periodic2DRankNBandEquivalenceHoppingLocalityVerification,
)
from ksdft2effmass.periodic3d.base import Periodic3DCapability
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.base import (
    Periodic3DRank2BandEquivalenceHoppingLocalityCapability,
)
from ksdft2effmass.periodic3d.rank2.band_equivalence_hopping_locality.lifecycle import (
    Periodic3DRank2BandEquivalenceHoppingLocalityExecution,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.base import (
    Periodic3DRankNBandEquivalenceHoppingLocalityCapability,
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseValue,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.model import (
    Periodic3DRankNAnalyticCase,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.request import (
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.verification import (  # noqa: E501
    Periodic3DRankNBandEquivalenceHoppingLocalityVerification,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestBandEquivalenceHoppingLocalityOwnership:
    def test_aggregate_is_band_equivalence_without_absorbing_locality_owner(
        self,
    ) -> None:
        assert issubclass(BandEquivalenceHoppingLocality, BandEquivalence)
        assert not issubclass(BandEquivalenceHoppingLocality, HoppingLocality)
        assert issubclass(
            BandEquivalenceHoppingLocalityRequest,
            BandEquivalenceHoppingLocality,
        )
        assert issubclass(
            BandEquivalenceHoppingLocalityAnalysis,
            BandEquivalenceHoppingLocality,
        )
        assert issubclass(
            BandEquivalenceHoppingLocalityAnalyzer,
            BandEquivalenceHoppingLocality,
        )
        assert issubclass(
            Periodic2DBandEquivalenceHoppingLocality,
            PeriodicBandEquivalenceHoppingLocality,
        )

    def test_rank_two_and_rank_n_are_abstract_sibling_owners(self) -> None:
        for capability in (
            Periodic1DRank2BandEquivalenceHoppingLocalityCapability,
            Periodic1DRankNBandEquivalenceHoppingLocalityCapability,
            Periodic2DRank2BandEquivalenceHoppingLocalityCapability,
            Periodic2DRankNBandEquivalenceHoppingLocalityCapability,
            Periodic3DRank2BandEquivalenceHoppingLocalityCapability,
            Periodic3DRankNBandEquivalenceHoppingLocalityCapability,
        ):
            assert capability.__abstractmethods__ in (
                {"band_subspace_rank"},
                {"band_subspace_ranks"},
            )
        assert not issubclass(
            Periodic2DRank2BandEquivalenceHoppingLocalityCapability,
            Periodic2DRankNBandEquivalenceHoppingLocalityCapability,
        )
        assert not issubclass(
            Periodic2DRankNBandEquivalenceHoppingLocalityCapability,
            Periodic2DRank2BandEquivalenceHoppingLocalityCapability,
        )

    def test_concrete_top_level_and_case_roles_use_truthful_rank_ownership(
        self,
    ) -> None:
        assert issubclass(
            Periodic1DRank2BandEquivalenceHoppingLocalityRequest,
            Periodic1DRank2BandEquivalenceHoppingLocalityCapability,
        )
        for concrete in (
            Periodic1DRankNBandEquivalenceHoppingLocalityRequest,
            Periodic1DRankNBandEquivalenceHoppingLocalityAnalysis,
            Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzer,
        ):
            assert issubclass(
                concrete,
                Periodic1DRankNBandEquivalenceHoppingLocalityCapability,
            )
        for periodic2d_concrete in (
            Periodic2DRank2BandEquivalenceHoppingLocalityRequest,
            Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis,
            Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer,
        ):
            assert issubclass(
                periodic2d_concrete,
                Periodic2DRank2BandEquivalenceHoppingLocalityCapability,
            )
        assert issubclass(
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalysis,
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseValue,
        )
        assert issubclass(
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseAnalyzer,
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseAction,
        )
        assert issubclass(
            Periodic2DRankNAnalyticCase,
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseValue,
        )
        assert issubclass(
            Periodic3DRankNAnalyticCase,
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseValue,
        )

    def test_periodic1d_rank_n_supporting_stages_retain_case_rank_ownership(
        self,
    ) -> None:
        for request_type in (
            Periodic1DRankNGaugeAlignmentAssemblyRequest,
            Periodic1DRankNConstructionMeshAnalysisRequest,
            Periodic1DRankNRefinementAnalysisRequest,
        ):
            assert issubclass(
                request_type,
                Periodic1DRankNBandEquivalenceHoppingLocalityValue,
            )
        for action_type in (
            Periodic1DRankNGaugeAlignmentResultAssembler,
            Periodic1DRankNConstructionMeshAnalyzer,
            Periodic1DRankNEvaluationIndependenceAnalyzer,
            Periodic1DRankNRefinementAnalyzer,
        ):
            assert issubclass(
                action_type,
                Periodic1DRankNBandEquivalenceHoppingLocalityAction,
            )

    def test_wire_records_do_not_use_dimensional_capability_identity(self) -> None:
        for record_type in (
            Periodic2DRank2BandEquivalenceHoppingLocalityExecution,
            Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition,
            Periodic2DRankNBandEquivalenceHoppingLocalityVerification,
        ):
            assert not issubclass(record_type, Periodic2DCapability)
        for periodic3d_record_type in (
            Periodic3DRank2BandEquivalenceHoppingLocalityExecution,
            Periodic3DRankNBandEquivalenceHoppingLocalityCaseDefinition,
            Periodic3DRankNBandEquivalenceHoppingLocalityVerification,
        ):
            assert not issubclass(periodic3d_record_type, Periodic3DCapability)
