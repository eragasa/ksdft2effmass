"""Verification for typed band-equivalence/locality plot writing."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import DirectLattice2D, DirectLatticeMetric

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    definitions,
)
from ksdft2effmass.application.band_equivalence_locality import (
    BandEquivalenceLocalityResultConstructor,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.plotting import (  # noqa: E501
    BandEquivalenceLocalityPlotRequest,
    BandEquivalenceLocalityPlotWriter,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestBandEquivalenceLocalityPlotWriter:
    """Establish the typed plotting boundary and written artifact set."""

    def test_execute__writes_plots_from_domain_diagnostics(
        self, tmp_path: Path
    ) -> None:
        case = definitions.BandEquivalenceLocalityCase(
            name="square-directed",
            dimension=2,
            parent_kind=definitions.ParentKind.DIRECTED_AXIS,
            gauge_normalization=definitions.GaugeNormalization.AXIS_MAXIMUM,
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
            family=definitions.BandEquivalenceLocalityFamily.SQUARE,
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
        constructor = BandEquivalenceLocalityResultConstructor()
        smoke = constructor.execute(smoke_request)
        refined = constructor.execute(refined_request)

        result = BandEquivalenceLocalityPlotWriter().execute(
            BandEquivalenceLocalityPlotRequest(
                mesh_results=(smoke.diagnostics, refined.diagnostics),
                output_directory=tmp_path,
                title="Square-family development diagnostics",
            )
        )

        assert len(result.paths) == 10
        assert all(path.is_file() and path.stat().st_size > 0 for path in result.paths)
        assert {path.suffix for path in result.paths} == {".pdf", ".png"}
