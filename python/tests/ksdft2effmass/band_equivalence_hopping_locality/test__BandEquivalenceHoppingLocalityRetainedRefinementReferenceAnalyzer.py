"""Tests for square-study refinement assessment without an aggregate owner."""

import math
from dataclasses import replace

import numpy as np
import pytest
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    DirectLatticeMetric,
)

from ksdft2effmass.band_equivalence_hopping_locality import (
    definitions,
    refinement_reference,
)
from ksdft2effmass.band_equivalence_hopping_locality.analysis import (
    Rank2BandEquivalenceHoppingLocalityAnalyzer,
)
from ksdft2effmass.band_equivalence_hopping_locality.definitions import (
    BandEquivalenceHoppingLocalityCase,
    BandEquivalenceHoppingLocalityFamilyEnum,
    BandEquivalenceHoppingLocalityRequest,
    GaugeNormalizationEnum,
    ParentEnum,
)
from ksdft2effmass.band_equivalence_hopping_locality.records import (
    BandEquivalenceHoppingLocalityDiagnostics,
)
from ksdft2effmass.band_equivalence_hopping_locality.result import (
    BandEquivalenceHoppingLocalityAnalysisRecorder,
)
from ksdft2effmass.solidstate.reciprocal_sewing import (
    IdentityReciprocalSewing,
    ReciprocalEndpointSewingInventory,
)

RefinementReferenceAnalyzer = refinement_reference.BandEquivalenceHoppingLocalityRetainedRefinementReferenceAnalyzer  # noqa: E501

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


def _request() -> BandEquivalenceHoppingLocalityRequest:
    metric = DirectLatticeMetric(
        DirectLattice2D(
            a1=np.array((1.0, 0.0)),
            a2=np.array((0.0, 1.0)),
        )
    )
    return BandEquivalenceHoppingLocalityRequest(
        family=BandEquivalenceHoppingLocalityFamilyEnum.SQUARE,
        synthetic_model=definitions.FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1,
        cases=(
            BandEquivalenceHoppingLocalityCase(
                name="square-refinement-control",
                dimension=2,
                parent_kind=ParentEnum.DIRECTED_AXIS,
                gauge_normalization=GaugeNormalizationEnum.AXIS_MAXIMUM,
                positive_bonds=((1, 0), (0, 1)),
                direct_metric=metric,
                shell_metric_scale=1.0,
            ),
        ),
        construction_size=4,
        evaluation_size=9,
        evaluation_shift=1.0 / 3.0,
        parent_scales=(1.0,),
        amplitudes=(math.pi / 8.0,),
        band_tolerances=(1.0e-3,),
        shell_cap=3,
    )


def _endpoint_sewing() -> ReciprocalEndpointSewingInventory:
    identity_sewing = IdentityReciprocalSewing(ambient_dimension=4)
    return ReciprocalEndpointSewingInventory(
        positive_axis_maps=(identity_sewing.endpoint_map,) * 2
    )


def _diagnostics() -> tuple[BandEquivalenceHoppingLocalityDiagnostics, ...]:
    base = _request()
    requests = (
        base,
        replace(base, construction_size=8, evaluation_size=17),
        replace(base, construction_size=16, evaluation_size=33),
    )
    return tuple(
        BandEquivalenceHoppingLocalityAnalysisRecorder(
            Rank2BandEquivalenceHoppingLocalityAnalyzer(
                request=request,
                endpoint_sewing=_endpoint_sewing(),
            ).execute()
        )
        .result()
        .diagnostics
        for request in requests
    )


class TestBandEquivalenceHoppingLocalityRetainedRefinementReferenceAnalyzer:
    """Establish the minimal square cross-result assessment boundary."""

    def test_execute__square_doubling_ladder__remains_unresolved(self) -> None:
        assessment = RefinementReferenceAnalyzer(results=_diagnostics()).execute()

        assert assessment.family is BandEquivalenceHoppingLocalityFamilyEnum.SQUARE
        assert tuple(
            (pair.coarse_construction_size, pair.fine_construction_size)
            for pair in assessment.refinements
        ) == ((4, 8), (8, 16))
        assert assessment.momentum_disposition == "unresolved"
        assert assessment.passes_draft_tolerance is None
        assert assessment.passes_unit_scale_draft_tolerance is None
        for refinement in assessment.refinements:
            assert refinement.shared_mesh_quantities_applicable is False
            assert refinement.within_draft_tolerances is None

    def test_init__non_tuple_results__is_rejected(self) -> None:
        with pytest.raises(TypeError, match="results must be a tuple"):
            RefinementReferenceAnalyzer(results=[])  # type: ignore[arg-type]

    def test_init__fewer_than_three_levels__is_rejected(self) -> None:
        with pytest.raises(ValueError, match="at least three mesh levels"):
            RefinementReferenceAnalyzer(results=_diagnostics()[:2])
