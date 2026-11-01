"""Tests for rank-two hopping-locality analysis."""

import numpy as np
import pytest
from projectkoios.physkit.units import ComplexMatrixQuantity, ScalarQuantity, Unitless

from ksdft2effmass.periodic1d.rank2 import hopping_locality as namespace
from ksdft2effmass.periodic1d.rank2.band_alignment.configuration import (
    Periodic1DCompositeBandAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.rank2.hopping_locality import (
    analysis as analysis_module,
)
from ksdft2effmass.periodic1d.rank2.hopping_locality import request as request_module
from ksdft2effmass.periodic1d.rank2.hopping_locality import result as result_module
from ksdft2effmass.periodic1d.rank2.hopping_locality.analysis import (
    Periodic1DRank2HoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic1d.rank2.hopping_locality.request import (
    Periodic1DRank2HoppingLocalityAnalysisRequest,
)
from ksdft2effmass.periodic1d.rank2.hopping_locality.result import (
    Periodic1DRank2HoppingLocalityAnalysis,
)
from ksdft2effmass.periodic1d.translations import (
    Periodic1DOrdinaryTranslationInventory,
)
from ksdft2effmass.solidstate.hopping_transforms import (
    BlockHoppingModel1D,
    BlockHoppingTruncationRequest1D,
    BlockHoppingTruncator1D,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DRank2HoppingLocalityAnalyzer:
    """Establish unchanged-tail diagnostics as a dedicated capability."""

    def test__namespace__is_inert_and_action_modules_are_authoritative(self) -> None:
        assert not hasattr(namespace, "Periodic1DRank2HoppingLocalityAnalyzer")
        assert analysis_module.__all__ == ["Periodic1DRank2HoppingLocalityAnalyzer"]
        assert request_module.__all__ == [
            "Periodic1DRank2HoppingLocalityAnalysisRequest"
        ]

    def test__request__requires_one_frozen_channel(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> None:
        with pytest.raises(ValueError, match="frozen locality inventory"):
            Periodic1DRank2HoppingLocalityAnalysisRequest(
                configuration=composite_configuration,
                channel="unknown",
                ordinary_model=self._model(),
            )

    def test__execute__matches_owner_omitted_norms_without_exposing_truncations(
        self,
        composite_configuration: Periodic1DCompositeBandAlignmentConfiguration,
    ) -> None:
        model = self._model()
        request = Periodic1DRank2HoppingLocalityAnalysisRequest(
            configuration=composite_configuration,
            channel="reference",
            ordinary_model=model,
        )

        analysis = Periodic1DRank2HoppingLocalityAnalyzer(request=request).execute()

        assert type(analysis) is Periodic1DRank2HoppingLocalityAnalysis
        assert analysis.request is request
        assert type(request.ordinary_translation_inventory) is (
            Periodic1DOrdinaryTranslationInventory
        )
        assert request.ordinary_translation_inventory.translations == (
            model.representatives
        )
        assert tuple(item.maximum_range for item in analysis.tails) == (
            composite_configuration.hopping_ranges
        )
        assert result_module.__all__ == [
            "Periodic1DRank2HoppingLocalityAnalysis",
            "Periodic1DRank2HoppingPower",
            "Periodic1DRank2HoppingTailResult",
        ]
        for tail in analysis.tails:
            owner = BlockHoppingTruncator1D(
                BlockHoppingTruncationRequest1D(
                    model,
                    tail.maximum_range,
                )
            ).execute()
            assert tail.ordinary_omitted_block_l2_norm == (owner.omitted_block_l2_norm)
            assert not hasattr(tail, "truncated")

    @staticmethod
    def _model() -> BlockHoppingModel1D:
        unit = Unitless()
        representatives = tuple(range(-31, 32))
        return BlockHoppingModel1D(
            reciprocal_period=ScalarQuantity(1.0, unit),
            representatives=representatives,
            hopping_blocks=tuple(
                ComplexMatrixQuantity(
                    np.eye(2, dtype=np.complex128) / float(abs(value) + 1),
                    unit,
                )
                for value in representatives
            ),
        )
