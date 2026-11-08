"""Verification for typed band-equivalence/locality plot writing."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from ksdft2effmass.band_equivalence_hopping_locality import (
    definitions,
)
from ksdft2effmass.band_equivalence_hopping_locality.analysis import (
    Rank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.band_equivalence_hopping_locality.plotting import (
    BandEquivalenceHoppingLocalityPlotRequest,
    BandEquivalenceHoppingLocalityPlotWriter,
    BandEquivalenceToleranceMapRequest,
    BandEquivalenceToleranceMapWriter,
)
from ksdft2effmass.sewing import (
    IdentityReciprocalSewing,
    ReciprocalEndpointSewingInventory,
)
from projectkoios.physkit.periodic.lattice import DirectLattice2D, DirectLatticeMetric

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


def _endpoint_sewing() -> ReciprocalEndpointSewingInventory:
    identity_sewing = IdentityReciprocalSewing(ambient_dimension=4)
    return ReciprocalEndpointSewingInventory(
        positive_axis_maps=(identity_sewing.endpoint_map,) * 2
    )


class TestBandEquivalenceHoppingLocalityPlotWriter:
    """Establish the typed plotting boundary and written artifact set."""

    def test_execute__writes_plots_from_domain_diagnostics(
        self, tmp_path: Path
    ) -> None:
        case = definitions.BandEquivalenceHoppingLocalityCase(
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
        smoke_request = definitions.BandEquivalenceHoppingLocalityRequest(
            family=definitions.BandEquivalenceHoppingLocalityFamilyEnum.SQUARE,
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
        smoke = Rank2BandEquivalenceHoppingLocalityAnalyzer(
            request=smoke_request,
            endpoint_sewing=_endpoint_sewing(),
        ).execute()
        refined = Rank2BandEquivalenceHoppingLocalityAnalyzer(
            request=refined_request,
            endpoint_sewing=_endpoint_sewing(),
        ).execute()

        result = BandEquivalenceHoppingLocalityPlotWriter(
            request=BandEquivalenceHoppingLocalityPlotRequest(
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
        case = definitions.BandEquivalenceHoppingLocalityCase(
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
        first_request = definitions.BandEquivalenceHoppingLocalityRequest(
            family=definitions.BandEquivalenceHoppingLocalityFamilyEnum.SQUARE,
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
            family=definitions.BandEquivalenceHoppingLocalityFamilyEnum.GRAPHENE_INSPIRED,
        )
        diagnostics = (
            Rank2BandEquivalenceHoppingLocalityAnalyzer(
                request=first_request,
                endpoint_sewing=_endpoint_sewing(),
            ).execute(),
            Rank2BandEquivalenceHoppingLocalityAnalyzer(
                request=second_request,
                endpoint_sewing=_endpoint_sewing(),
            ).execute(),
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
