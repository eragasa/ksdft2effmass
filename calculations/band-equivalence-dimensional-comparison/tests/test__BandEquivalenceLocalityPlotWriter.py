"""Verification for typed band-equivalence/locality plot writing."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    definitions,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.analysis import (
    BandEquivalenceLocalityAnalyzer,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.plotting import (
    BandEquivalenceLocalityPlotRequest,
    BandEquivalenceLocalityPlotWriter,
    BandEquivalenceToleranceMapRequest,
    BandEquivalenceToleranceMapWriter,
)
from projectkoios.physkit.periodic.lattice import DirectLattice2D, DirectLatticeMetric

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestBandEquivalenceLocalityPlotWriter:
    """Establish the typed plotting boundary and written artifact set."""

    def test_execute__writes_plots_from_domain_diagnostics(
        self, tmp_path: Path
    ) -> None:
        case = definitions.BandEquivalenceLocalityCase(
            name="square-directed",
            dimension=2,
            parent_kind=definitions.ParentEnum.DIRECTED_AXIS,
            gauge_normalization=definitions.GaugeNormalizationEnum.AXIS_MAXIMUM,
            direct_metric=DirectLatticeMetric(
                DirectLattice2D(
                    a1=np.array((1.0, 0.0), dtype=np.float64),
                    a2=np.array((0.0, 1.0), dtype=np.float64),
                )
            ),
            positive_bonds=((1, 0), (0, 1)),
            shell_metric_scale=1.0,
        )
        smoke_request = definitions.BandEquivalenceLocalityRequest(
            family=definitions.BandEquivalenceLocalityFamilyEnum.SQUARE,
            synthetic_model=definitions.FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
            cases=(case,),
            construction_size=4,
            evaluation_size=5,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(1.0,),
            amplitudes=(0.0,),
            band_tolerances=(1.0e-3,),
            shell_cap=2,
        )
        refined_request = replace(
            smoke_request,
            construction_size=6,
            evaluation_size=7,
        )
        smoke = BandEquivalenceLocalityAnalyzer(request=smoke_request).execute()
        refined = BandEquivalenceLocalityAnalyzer(request=refined_request).execute()

        result = BandEquivalenceLocalityPlotWriter(
            request=BandEquivalenceLocalityPlotRequest(
                mesh_results=(smoke, refined),
                output_directory=tmp_path,
                title="Square-family development diagnostics",
            )
        ).execute()

        assert len(result.paths) == 10
        assert all(path.is_file() and path.stat().st_size > 0 for path in result.paths)
        assert {path.suffix for path in result.paths} == {".pdf", ".png"}

    def test_tolerance_map__writes_cross_family_requirements_without_limits(
        self, tmp_path: Path
    ) -> None:
        case = definitions.BandEquivalenceLocalityCase(
            name="synthetic-directed-case",
            dimension=2,
            parent_kind=definitions.ParentEnum.DIRECTED_AXIS,
            gauge_normalization=definitions.GaugeNormalizationEnum.AXIS_MAXIMUM,
            direct_metric=DirectLatticeMetric(
                DirectLattice2D(
                    a1=np.array((1.0, 0.0), dtype=np.float64),
                    a2=np.array((0.0, 1.0), dtype=np.float64),
                )
            ),
            positive_bonds=((1, 0), (0, 1)),
            shell_metric_scale=1.0,
        )
        first_request = definitions.BandEquivalenceLocalityRequest(
            family=definitions.BandEquivalenceLocalityFamilyEnum.SQUARE,
            synthetic_model=definitions.FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
            cases=(case,),
            construction_size=4,
            evaluation_size=5,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(0.0, 1.0),
            amplitudes=(0.0, 0.1),
            band_tolerances=(1.0e-3,),
            shell_cap=2,
        )
        second_request = replace(
            first_request,
            family=definitions.BandEquivalenceLocalityFamilyEnum.GRAPHENE_INSPIRED,
        )
        diagnostics = (
            BandEquivalenceLocalityAnalyzer(request=first_request).execute(),
            BandEquivalenceLocalityAnalyzer(request=second_request).execute(),
        )

        result = BandEquivalenceToleranceMapWriter(
            request=BandEquivalenceToleranceMapRequest(
                family_results=diagnostics,
                output_directory=tmp_path,
                title="Development tolerance requirements",
            )
        ).execute()

        assert result.paths == (
            tmp_path / "tolerance-requirement-map.pdf",
            tmp_path / "tolerance-requirement-map.png",
        )
        assert all(path.is_file() and path.stat().st_size > 0 for path in result.paths)
