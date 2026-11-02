"""Tests for periodic-2D rank-two band-equivalence/locality ownership."""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import DirectLattice2D, DirectLatticeMetric
from projectkoios.physkit.units import ScalarQuantity, Unitless

from ksdft2effmass.band_equivalence_hopping_locality.definitions import (
    FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
    BandEquivalenceHoppingLocalityCase,
    BandEquivalenceHoppingLocalityFamilyEnum,
    GaugeNormalizationEnum,
    ParentEnum,
)
from ksdft2effmass.band_equivalence_hopping_locality.verification import (
    BandEquivalenceHoppingLocalityVerificationThresholds,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.analysis import (
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis,
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.reference import (
    Periodic2DRank2BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer,
    Periodic2DRank2BandEquivalenceHoppingLocalityIndependentShellPowerReference,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.request import (
    Periodic2DRank2BandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.result import (
    Periodic2DRank2BandEquivalenceHoppingLocalityAnalysisRecorder,
    Periodic2DRank2BandEquivalenceHoppingLocalityCalculationResult,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.verification import (  # noqa: E501
    Periodic2DRank2BandEquivalenceHoppingLocalityDiagnosticVerifier,
    Periodic2DRank2BandEquivalenceHoppingLocalityResultVerifier,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.visualizations.data import (  # noqa: E501
    Periodic2DRank2BandEquivalenceHoppingLocalityVisualizationData,
)
from ksdft2effmass.periodic2d.rank2.band_equivalence_hopping_locality.visualizations.visualizer import (  # noqa: E501
    Periodic2DRank2BandEquivalenceHoppingLocalityVisualizer,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic2DRank2BandEquivalenceHoppingLocality:
    """Establish rank-first delegation and typed serialization boundaries."""

    @staticmethod
    def _request() -> Periodic2DRank2BandEquivalenceHoppingLocalityRequest:
        return Periodic2DRank2BandEquivalenceHoppingLocalityRequest(
            family=BandEquivalenceHoppingLocalityFamilyEnum.SQUARE,
            cases=(
                BandEquivalenceHoppingLocalityCase(
                    name="square",
                    dimension=2,
                    parent_kind=ParentEnum.DIRECTED_AXIS,
                    gauge_normalization=GaugeNormalizationEnum.AXIS_MAXIMUM,
                    positive_bonds=((1, 0), (0, 1)),
                    direct_metric=DirectLatticeMetric(
                        DirectLattice2D(
                            a1=np.array((1.0, 0.0), dtype=np.float64),
                            a2=np.array((0.0, 1.0), dtype=np.float64),
                        )
                    ),
                    shell_metric_scale=1.0,
                ),
            ),
            synthetic_model=FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
            construction_size=4,
            evaluation_size=3,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(1.0,),
            amplitudes=(0.0,),
            band_tolerances=(1.0e-3,),
            shell_cap=1,
        )

    def test__request__round_trips_through_the_rank_first_type(self) -> None:
        request = self._request()
        restored = Periodic2DRank2BandEquivalenceHoppingLocalityRequest.from_json(
            request.to_json()
        )

        assert type(restored) is Periodic2DRank2BandEquivalenceHoppingLocalityRequest
        assert restored.to_json() == request.to_json()
        assert type(restored.cases[0].direct_metric.direct_lattice) is DirectLattice2D

    def test__analysis_and_result__retain_rank_first_owner_types(self) -> None:
        analysis = Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer(
            request=self._request()
        ).execute()
        result = Periodic2DRank2BandEquivalenceHoppingLocalityAnalysisRecorder(
            analysis
        ).result()
        restored = (
            Periodic2DRank2BandEquivalenceHoppingLocalityCalculationResult.from_json(
                result.to_json()
            )
        )

        assert type(analysis) is Periodic2DRank2BandEquivalenceHoppingLocalityAnalysis
        assert (
            type(result)
            is Periodic2DRank2BandEquivalenceHoppingLocalityCalculationResult
        )
        assert (
            type(restored)
            is Periodic2DRank2BandEquivalenceHoppingLocalityCalculationResult
        )
        assert (
            type(restored.request)
            is Periodic2DRank2BandEquivalenceHoppingLocalityRequest
        )
        assert restored.to_json() == result.to_json()

    def test__verification_and_visualization__retain_rank_first_actions(self) -> None:
        analysis = Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer(
            request=self._request()
        ).execute()
        result = Periodic2DRank2BandEquivalenceHoppingLocalityAnalysisRecorder(
            analysis
        ).result()
        reference_analyzer = (
            Periodic2DRank2BandEquivalenceHoppingLocalityIndependentShellPowerAnalyzer(
                request=result.request
            )
        )
        reference = reference_analyzer.execute()
        verified = Periodic2DRank2BandEquivalenceHoppingLocalityResultVerifier(
            result_wire=result.to_json(),
            diagnostic_verifier=(
                Periodic2DRank2BandEquivalenceHoppingLocalityDiagnosticVerifier(
                    request=result.request,
                    result=result.diagnostics,
                )
            ),
            shell_power_analyzer=reference_analyzer,
            thresholds=BandEquivalenceHoppingLocalityVerificationThresholds(
                stored_identity_maximum_defect=ScalarQuantity(1.0e-8, Unitless()),
                independent_parent_maximum_defect=ScalarQuantity(1.0e-8, Unitless()),
                independent_band_maximum_defect=ScalarQuantity(1.0e-8, Unitless()),
                independent_shell_power_maximum_defect=ScalarQuantity(
                    1.0e-8,
                    Unitless(),
                ),
            ),
        ).result()
        figures = Periodic2DRank2BandEquivalenceHoppingLocalityVisualizer(
            data=verified.visualization_data,
            verification=verified.verification,
            dpi=72,
        ).visualize()

        assert (
            type(reference)
            is Periodic2DRank2BandEquivalenceHoppingLocalityIndependentShellPowerReference  # noqa: E501
        )
        assert (
            type(verified.visualization_data)
            is Periodic2DRank2BandEquivalenceHoppingLocalityVisualizationData
        )
        assert len(figures) == 1

    def test__request__rejects_a_periodic3d_family(self) -> None:
        with pytest.raises(ValueError, match="periodic-2D"):
            replace(
                self._request(),
                family=BandEquivalenceHoppingLocalityFamilyEnum.SIMPLE_CUBIC,
            )
