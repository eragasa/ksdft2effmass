"""Tests for retained mesh-refinement record validation."""

from dataclasses import replace

import pytest

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    BandEquivalenceLocalityFamilyEnum,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.records import (
    BandEquivalenceLocalityRefinementAssessmentRecord,
    BandEquivalenceLocalityRefinementPairRecord,
)


def _pair(coarse_construction_size: int) -> BandEquivalenceLocalityRefinementPairRecord:
    return BandEquivalenceLocalityRefinementPairRecord(
        coarse_construction_size=coarse_construction_size,
        fine_construction_size=2 * coarse_construction_size,
        maximum_parent_diagnostic_change=1.0e-8,
        maximum_final_parent_invariant_change=2.0e-8,
        maximum_correlation_change=3.0e-8,
        maximum_threshold_change=4.0e-8,
        maximum_hopping_weight_change=5.0e-8,
        maximum_hopping_block_power_change=6.0e-8,
        maximum_angle_change=7.0e-8,
        maximum_band_defect=8.0e-8,
        maximum_reconstruction_defect=9.0e-8,
        maximum_parseval_defect=1.0e-7,
        maximum_final_outcome_change=0,
        first_passing_dispositions_stable=True,
        transport_closure_and_plaquette_applicability_stable=True,
        shared_mesh_quantities_applicable=True,
        shared_mesh_inapplicable_reason="",
        maximum_shared_parent_eigenvalue_defect=1.1e-7,
        maximum_shared_projector_defect=1.2e-7,
        within_draft_tolerances=True,
        tolerance_disposition_reason="within draft tolerances",
    )


def _assessment() -> BandEquivalenceLocalityRefinementAssessmentRecord:
    return BandEquivalenceLocalityRefinementAssessmentRecord(
        family=BandEquivalenceLocalityFamilyEnum.SQUARE,
        refinements=(_pair(4), _pair(8)),
        required_stable_refinements=2,
        momentum_disposition="resolved",
        momentum_disposition_reason="two stable adjacent refinements",
        passes_draft_tolerance=True,
        passes_unit_scale_draft_tolerance=True,
        tolerance_inapplicable_reason="",
        paper1_literal_range_endpoints_applicable=False,
        paper1_literal_range_endpoints_inapplicable_reason=(
            "this family does not own the Paper 1 literal endpoints"
        ),
    )


class TestBandEquivalenceLocalityRefinementRecords:
    """Establish strict retained-record admission and canonical bytes."""

    def test_assessment__canonical_bytes__readmit_exactly(self) -> None:
        assessment = _assessment()

        wire = assessment.to_json()
        admitted = BandEquivalenceLocalityRefinementAssessmentRecord.from_json(wire)

        assert admitted == assessment
        assert admitted.to_json() == wire

    def test_pair__boolean_integer__is_rejected(self) -> None:
        values = dict(_pair(4).to_dict())
        values["coarse_construction_size"] = True

        with pytest.raises(TypeError, match="coarse_construction_size"):
            BandEquivalenceLocalityRefinementPairRecord.from_dict(values)

    def test_pair__unexpected_field__is_rejected(self) -> None:
        values = dict(_pair(4).to_dict())
        values["unexpected"] = "field"

        with pytest.raises(ValueError, match="fields do not match"):
            BandEquivalenceLocalityRefinementPairRecord.from_dict(values)

    def test_assessment__invalid_inventory__is_rejected(self) -> None:
        assessment = _assessment()

        with pytest.raises(ValueError, match="at least two"):
            replace(assessment, refinements=(assessment.refinements[0],))
        with pytest.raises(TypeError, match="required_stable_refinements"):
            replace(assessment, required_stable_refinements=True)
