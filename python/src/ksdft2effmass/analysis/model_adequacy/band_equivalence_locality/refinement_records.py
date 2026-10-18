"""Immutable records for band-equivalence/locality mesh refinement."""

from __future__ import annotations

from dataclasses import dataclass

from .definitions import BandEquivalenceLocalityFamily


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityRefinementPair:
    """Retain changes across one adjacent mesh-doubling pair."""

    coarse_construction_size: int
    fine_construction_size: int
    maximum_parent_diagnostic_change: float
    maximum_final_parent_invariant_change: float
    maximum_correlation_change: float
    maximum_threshold_change: float
    maximum_hopping_weight_change: float
    maximum_hopping_block_power_change: float
    maximum_angle_change: float
    maximum_band_defect: float
    maximum_reconstruction_defect: float
    maximum_parseval_defect: float
    maximum_final_outcome_change: int | None
    first_passing_dispositions_stable: bool
    transport_closure_and_plaquette_applicability_stable: bool
    shared_mesh_quantities_applicable: bool
    shared_mesh_inapplicable_reason: str
    maximum_shared_parent_eigenvalue_defect: float | None
    maximum_shared_projector_defect: float | None
    within_draft_tolerances: bool | None
    tolerance_disposition_reason: str


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityRefinementAssessment:
    """Retain a conservative hash-free family refinement assessment."""

    family: BandEquivalenceLocalityFamily
    refinements: tuple[BandEquivalenceLocalityRefinementPair, ...]
    required_stable_refinements: int
    momentum_disposition: str
    momentum_disposition_reason: str
    passes_draft_tolerance: bool | None
    passes_unit_scale_draft_tolerance: bool | None
    tolerance_inapplicable_reason: str
    paper1_literal_range_endpoints_applicable: bool
    paper1_literal_range_endpoints_inapplicable_reason: str


__all__ = [
    "BandEquivalenceLocalityRefinementPair",
    "BandEquivalenceLocalityRefinementAssessment",
]
